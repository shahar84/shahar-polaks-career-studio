"""Protocol checks with synthetic CLI events; these do not evaluate a model."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_eval


class SourceProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "plugin"
        (self.root / ".claude-plugin").mkdir(parents=True)
        (self.root / "skills" / "example").mkdir(parents=True)
        self.skill = self.root / "skills" / "example" / "SKILL.md"
        self.skill.write_text("---\nname: example\ndescription: Example\n---\n", encoding="utf-8")
        self.manifest = {"name": run_eval.EXPECTED_PLUGIN_NAME, "version": "1.2.3"}
        (self.root / ".claude-plugin" / "plugin.json").write_text(json.dumps(self.manifest))
        (self.root / "plugin.json").write_text(json.dumps(self.manifest))
        self.source = run_eval.plugin_source(self.root)

    def events(self, *, path=None, skills=None, result="Useful response"):
        return [
            {
                "type": "system", "subtype": "init", "model": "synthetic-model",
                "claude_code_version": "synthetic-cli",
                "plugins": [{"name": self.manifest["name"], "path": str(path or self.root)}],
                "skills": skills if skills is not None else [self.manifest["name"] + ":example"],
            },
            {"type": "result", "subtype": "success", "is_error": False, "result": result},
        ]

    def parse(self, events):
        return run_eval.parse_plugin_stream("\n".join(json.dumps(e) for e in events), self.source)

    def test_exact_source_loads_and_plain_result_is_returned(self):
        ok, response, observed = self.parse(self.events())
        self.assertTrue(ok)
        self.assertEqual(response, "Useful response")
        self.assertTrue(observed["plugin_load_verified"])
        self.assertEqual(observed["actual_model"], "synthetic-model")

    def test_installed_copy_cannot_pass_as_local_source(self):
        ok, reason, observed = self.parse(self.events(path=self.root.parent / "old-install"))
        self.assertFalse(ok)
        self.assertIn("absent from system/init", reason)
        self.assertFalse(observed["plugin_load_verified"])

    def test_missing_skill_is_a_load_error(self):
        ok, reason, _ = self.parse(self.events(skills=[]))
        self.assertFalse(ok)
        self.assertIn("skills are missing", reason)

    def test_missing_init_and_plain_text_are_rejected(self):
        ok, _, _ = self.parse(self.events()[1:])
        self.assertFalse(ok)
        ok, _, _ = run_eval.parse_plugin_stream("Generic unassisted answer", self.source)
        self.assertFalse(ok)

    def test_error_result_is_not_a_pass(self):
        events = self.events()
        events[-1].update(is_error=True, subtype="error_max_turns")
        ok, reason, _ = self.parse(events)
        self.assertFalse(ok)
        self.assertIn("not successful", reason)

    def test_source_digest_changes_for_runtime_but_not_reports(self):
        (self.root / "skills" / "example" / "eval").mkdir()
        (self.root / "skills" / "example" / "eval" / "report.json").write_text("{}")
        self.assertEqual(self.source, run_eval.plugin_source(self.root))
        self.skill.write_text(self.skill.read_text() + "New guidance.\n")
        self.assertNotEqual(self.source["runtime_sha256"], run_eval.plugin_source(self.root)["runtime_sha256"])

    def test_manifest_version_disagreement_is_rejected(self):
        (self.root / "plugin.json").write_text(json.dumps({**self.manifest, "version": "1.2.2"}))
        with self.assertRaisesRegex(ValueError, "disagree"):
            run_eval.plugin_source(self.root)

    def test_scenario_command_loads_exact_source_without_permission_bypass(self):
        stdout = "\n".join(json.dumps(e) for e in self.events())
        with patch.object(run_eval.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, stdout, "")) as call:
            ok, _, _ = run_eval.run_claude("Synthetic request", "claude", None, 30, self.source)
        self.assertTrue(ok)
        command = call.call_args.args[0]
        self.assertEqual(command[command.index("--plugin-dir") + 1], str(self.root))
        self.assertEqual(command[command.index("--output-format") + 1], "stream-json")
        self.assertNotIn("--dangerously-skip-permissions", command)

    def test_skill_and_read_calls_are_recorded_as_observations(self):
        events = self.events()
        events.insert(1, {"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Skill", "input": {"skill": self.manifest["name"] + ":example"}},
            {"type": "tool_use", "name": "Read", "input": {"file_path": str(self.skill)}},
            {"type": "tool_use", "name": "Read", "input": {"file_path": "/unrelated/private.txt"}},
        ]}})
        ok, _, observed = self.parse(events)
        self.assertTrue(ok)
        self.assertEqual(observed["source_read_calls"], ["skills/example/SKILL.md"])
        self.assertEqual(observed["skill_invocations"], [self.manifest["name"] + ":example"])


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Behavior regression harness for the shahar-cv-optimizer skill.

Runs each scenario in scenarios.json against a real `claude -p` invocation
(so the actual installed plugin/skill is exercised, not a re-implementation
of it), then checks the response against deterministic string/regex checks
and, optionally, an LLM-judge rubric using a second `claude -p` call.

This intentionally targets Claude Code, not Codex: Codex's non-interactive
CLI, PDF/vision handling, and skill-discovery mechanics differ enough that a
single script can't treat them as equivalent. Use tests/*.md manually to
spot-check Codex behavior.

Requirements:
  - The `claude` CLI installed and authenticated.
  - The shahar-polaks-career-studio plugin installed (or otherwise
    discoverable) in that Claude Code environment, so the skill actually
    triggers instead of running as a bare model with no skill context.
  - No third-party Python packages: standard library only.

Usage:
  python3 run_eval.py                       # run everything
  python3 run_eval.py --category truth-policy
  python3 run_eval.py --id job-4-ambiguous-market
  python3 run_eval.py --skip-judge          # deterministic checks only (fast, free)
  python3 run_eval.py --list                # show scenarios without running them

Exit code is 1 if any non-skipped scenario fails, 0 otherwise, so this can
be wired into a pre-release checklist or CI.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SCENARIOS = SCRIPT_DIR / "scenarios.json"
FIXTURES_DIR = SCRIPT_DIR / "fixtures"
FIXTURE_RE = re.compile(r"\{\{fixture:([\w.\-]+)\}\}")

JUDGE_PROMPT_TEMPLATE = """You are grading a single response from an AI career-coaching assistant \
against one pass/fail criterion. Be strict: if the response is ambiguous or \
only partially satisfies the criterion, fail it.

Criterion:
{rubric}

Response to grade:
---
{response}
---

Reply with exactly one line starting with PASS or FAIL, then a one-sentence reason on the next line.
"""


def load_fixture(name: str) -> str:
    path = FIXTURES_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Fixture not found: {path}")
    return path.read_text(encoding="utf-8")


def resolve_prompt(prompt: str) -> str:
    def _sub(match: re.Match) -> str:
        return load_fixture(match.group(1))

    return FIXTURE_RE.sub(_sub, prompt)


def run_claude(prompt: str, claude_bin: str, model: str | None, timeout: int) -> tuple[bool, str]:
    """Run `claude -p <prompt>` and return (ok, output_text)."""
    cmd = [claude_bin, "-p", prompt]
    if model:
        cmd.extend(["--model", model])
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        return False, f"ERROR: '{claude_bin}' not found on PATH. Is Claude Code installed?"
    except subprocess.TimeoutExpired:
        return False, f"ERROR: timed out after {timeout}s"

    if result.returncode != 0 and not result.stdout.strip():
        return False, f"ERROR: claude exited {result.returncode}: {result.stderr.strip()[:500]}"

    return True, result.stdout.strip()


def check_contains_all(response: str, values: list[str], case_sensitive: bool) -> tuple[bool, str]:
    haystack = response if case_sensitive else response.lower()
    missing = [v for v in values if (v if case_sensitive else v.lower()) not in haystack]
    if missing:
        return False, f"missing: {missing}"
    return True, "all present"


def check_contains_any(response: str, values: list[str], case_sensitive: bool) -> tuple[bool, str]:
    haystack = response if case_sensitive else response.lower()
    for v in values:
        if (v if case_sensitive else v.lower()) in haystack:
            return True, f"found: {v!r}"
    return False, f"none of {values} found"


def check_not_contains_any(response: str, values: list[str], case_sensitive: bool) -> tuple[bool, str]:
    haystack = response if case_sensitive else response.lower()
    present = [v for v in values if (v if case_sensitive else v.lower()) in haystack]
    if present:
        return False, f"forbidden strings present: {present}"
    return True, "none present"


def check_regex_all(response: str, patterns: list[str]) -> tuple[bool, str]:
    missing = [p for p in patterns if not re.search(p, response)]
    if missing:
        return False, f"patterns not matched: {missing}"
    return True, "all matched"


CHECK_DISPATCH = {
    "contains_all": lambda r, c: check_contains_all(r, c["values"], c.get("case_sensitive", False)),
    "contains_any": lambda r, c: check_contains_any(r, c["values"], c.get("case_sensitive", False)),
    "not_contains_any": lambda r, c: check_not_contains_any(r, c["values"], c.get("case_sensitive", False)),
    "regex_all": lambda r, c: check_regex_all(r, c["values"]),
}


def run_judge(response: str, rubric: str, claude_bin: str, model: str | None, timeout: int) -> tuple[bool, str]:
    prompt = JUDGE_PROMPT_TEMPLATE.format(rubric=rubric, response=response)
    ok, output = run_claude(prompt, claude_bin, model, timeout)
    if not ok:
        return False, output
    first_line = output.strip().splitlines()[0] if output.strip() else ""
    passed = first_line.upper().startswith("PASS")
    return passed, output.strip()


def run_scenario(scenario: dict, args: argparse.Namespace) -> dict:
    scenario_id = scenario["id"]

    if scenario.get("skip_automated"):
        return {
            "id": scenario_id,
            "category": scenario.get("category"),
            "status": "skipped",
            "reason": scenario.get("skip_reason", "marked skip_automated"),
        }

    prompt = resolve_prompt(scenario["prompt"])
    ok, response = run_claude(prompt, args.claude_bin, args.model, args.timeout)
    if not ok:
        return {
            "id": scenario_id,
            "category": scenario.get("category"),
            "status": "error",
            "reason": response,
        }

    check_results = []
    all_passed = True
    for check in scenario.get("checks", []):
        fn = CHECK_DISPATCH.get(check["type"])
        if fn is None:
            check_results.append({"type": check["type"], "pass": False, "detail": "unknown check type"})
            all_passed = False
            continue
        passed, detail = fn(response, check)
        check_results.append({"type": check["type"], "pass": passed, "detail": detail})
        all_passed = all_passed and passed

    judge_result = None
    if scenario.get("judge_rubric") and not args.skip_judge:
        judge_passed, judge_detail = run_judge(
            response, scenario["judge_rubric"], args.claude_bin, args.judge_model or args.model, args.timeout
        )
        judge_result = {"pass": judge_passed, "detail": judge_detail}
        all_passed = all_passed and judge_passed

    return {
        "id": scenario_id,
        "category": scenario.get("category"),
        "status": "pass" if all_passed else "fail",
        "checks": check_results,
        "judge": judge_result,
        "response_preview": response[:400],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scenarios", default=str(DEFAULT_SCENARIOS), help="Path to scenarios.json")
    parser.add_argument("--id", help="Run only the scenario with this id")
    parser.add_argument("--category", help="Run only scenarios in this category")
    parser.add_argument("--claude-bin", default="claude", help="Path to the claude CLI binary")
    parser.add_argument("--model", default=None, help="Model to pass to claude -p")
    parser.add_argument("--judge-model", default=None, help="Model to use for judge calls (defaults to --model)")
    parser.add_argument("--timeout", type=int, default=180, help="Per-call timeout in seconds")
    parser.add_argument("--workers", type=int, default=3, help="Parallel scenarios")
    parser.add_argument("--skip-judge", action="store_true", help="Run only deterministic checks, skip LLM-judge rubrics")
    parser.add_argument("--list", action="store_true", help="List scenarios and exit without running")
    parser.add_argument("--out", default=str(SCRIPT_DIR / "report.json"), help="Where to write the JSON report")
    args = parser.parse_args()

    data = json.loads(Path(args.scenarios).read_text(encoding="utf-8"))
    scenarios = data["scenarios"]

    if args.id:
        scenarios = [s for s in scenarios if s["id"] == args.id]
    if args.category:
        scenarios = [s for s in scenarios if s.get("category") == args.category]

    if not scenarios:
        print("No scenarios matched the given filters.", file=sys.stderr)
        return 1

    if args.list:
        for s in scenarios:
            flag = " [manual]" if s.get("skip_automated") else ""
            print(f"{s['id']:32s} [{s.get('category')}]{flag}  {s.get('description', '')}")
        return 0

    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_to_id = {executor.submit(run_scenario, s, args): s["id"] for s in scenarios}
        for future in as_completed(future_to_id):
            results.append(future.result())

    order = {s["id"]: i for i, s in enumerate(scenarios)}
    results.sort(key=lambda r: order[r["id"]])

    passed = sum(1 for r in results if r["status"] == "pass")
    failed = sum(1 for r in results if r["status"] == "fail")
    errored = sum(1 for r in results if r["status"] == "error")
    skipped = sum(1 for r in results if r["status"] == "skipped")

    print(f"\n{'ID':32s} STATUS")
    print("-" * 60)
    for r in results:
        print(f"{r['id']:32s} {r['status'].upper()}")
        if r["status"] == "fail":
            for c in r.get("checks", []):
                if not c["pass"]:
                    print(f"    - {c['type']}: {c['detail']}")
            if r.get("judge") and not r["judge"]["pass"]:
                print(f"    - judge: {r['judge']['detail'][:200]}")
        if r["status"] == "error":
            print(f"    - {r['reason']}")
        if r["status"] == "skipped":
            print(f"    - {r['reason']}")

    print("-" * 60)
    print(f"pass={passed} fail={failed} error={errored} skipped={skipped} total={len(results)}\n")

    Path(args.out).write_text(json.dumps({"summary": {
        "pass": passed, "fail": failed, "error": errored, "skipped": skipped, "total": len(results)
    }, "results": results}, indent=2), encoding="utf-8")
    print(f"Full report written to {args.out}")

    return 1 if (failed or errored) else 0


if __name__ == "__main__":
    sys.exit(main())

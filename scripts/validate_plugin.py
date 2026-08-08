#!/usr/bin/env python3
"""Validate the Career Studio plugin package without external dependencies."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "shahar-polaks-career-studio"
PLUGIN_NAME = "shahar-polaks-career-studio"


def read_json(path: Path, errors: list[str]) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
        return {}
    if not isinstance(data, dict):
        errors.append(f"{path.relative_to(ROOT)}: expected a JSON object")
        return {}
    return data


def require_value(data: dict, key: str, label: str, errors: list[str]) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}: missing non-empty {key!r}")
        return ""
    return value


def validate_skill(skill_path: Path, errors: list[str]) -> None:
    label = str(skill_path.relative_to(ROOT))
    try:
        text = skill_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"{label}: cannot read file ({exc})")
        return

    if not text.startswith("---\n"):
        errors.append(f"{label}: missing YAML frontmatter opening delimiter")
        return

    closing = text.find("\n---\n", 4)
    if closing == -1:
        errors.append(f"{label}: missing YAML frontmatter closing delimiter")
        return

    frontmatter = text[4:closing]
    keys = {
        line.split(":", 1)[0].strip()
        for line in frontmatter.splitlines()
        if line and not line[0].isspace() and ":" in line
    }
    for required_key in ("name", "description"):
        if required_key not in keys:
            errors.append(f"{label}: frontmatter is missing {required_key!r}")


def main() -> int:
    errors: list[str] = []

    required_paths = [
        ROOT / "README.md",
        ROOT / "LICENSE",
        ROOT / ".claude-plugin" / "marketplace.json",
        ROOT / ".agents" / "plugins" / "marketplace.json",
        PLUGIN / ".claude-plugin" / "plugin.json",
        PLUGIN / ".codex-plugin" / "plugin.json",
    ]
    for path in required_paths:
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")

    claude = read_json(PLUGIN / ".claude-plugin" / "plugin.json", errors)
    codex = read_json(PLUGIN / ".codex-plugin" / "plugin.json", errors)
    claude_marketplace = read_json(ROOT / ".claude-plugin" / "marketplace.json", errors)
    codex_marketplace = read_json(ROOT / ".agents" / "plugins" / "marketplace.json", errors)

    versions: list[tuple[str, str]] = []
    for label, manifest in (("Claude manifest", claude), ("Codex manifest", codex)):
        if require_value(manifest, "name", label, errors) not in ("", PLUGIN_NAME):
            errors.append(f"{label}: name must be {PLUGIN_NAME!r}")
        version = require_value(manifest, "version", label, errors)
        if version:
            versions.append((label, version))

    claude_plugins = claude_marketplace.get("plugins")
    if not isinstance(claude_plugins, list) or len(claude_plugins) != 1 or not isinstance(claude_plugins[0], dict):
        errors.append("Claude marketplace: expected exactly one plugin object")
    else:
        listed = claude_plugins[0]
        if listed.get("name") != PLUGIN_NAME:
            errors.append("Claude marketplace: plugin name does not match the package name")
        if listed.get("source") != "./plugins/shahar-polaks-career-studio":
            errors.append("Claude marketplace: plugin source must point at the package directory")
        version = require_value(listed, "version", "Claude marketplace", errors)
        if version:
            versions.append(("Claude marketplace", version))

    codex_plugins = codex_marketplace.get("plugins")
    if not isinstance(codex_plugins, list) or len(codex_plugins) != 1 or not isinstance(codex_plugins[0], dict):
        errors.append("Codex marketplace: expected exactly one plugin object")
    else:
        listed = codex_plugins[0]
        source = listed.get("source")
        if listed.get("name") != PLUGIN_NAME:
            errors.append("Codex marketplace: plugin name does not match the package name")
        if not isinstance(source, dict) or source.get("path") != "./plugins/shahar-polaks-career-studio":
            errors.append("Codex marketplace: plugin source must point at the package directory")

    if versions and len({version for _, version in versions}) != 1:
        rendered = ", ".join(f"{label}={version}" for label, version in versions)
        errors.append(f"plugin versions must match across manifests ({rendered})")

    skills_dir = PLUGIN / "skills"
    skill_files = sorted(skills_dir.glob("*/SKILL.md")) if skills_dir.is_dir() else []
    if not skill_files:
        errors.append("no skills found at plugins/shahar-polaks-career-studio/skills/*/SKILL.md")
    for skill_file in skill_files:
        validate_skill(skill_file, errors)

    if errors:
        print("Plugin validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    version = versions[0][1] if versions else "unknown"
    print(f"Plugin package is valid: {PLUGIN_NAME} v{version} ({len(skill_files)} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

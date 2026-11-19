#!/usr/bin/env python3
"""Validate the Career Studio plugin package without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "shahar-polaks-career-studio"
PLUGIN_NAME = "shahar-polaks-career-studio"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
EXPECTED_SKILLS = {"interview-pitch", "shahar-cv-optimizer"}
SEMVER = re.compile(
    r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
)
CATEGORIES = {
    "Business & Operations", "Communication", "Creativity", "Data & Analytics",
    "Developer Tools", "Education & Research", "Entertainment", "Finance",
    "Healthcare", "Other", "Productivity", "Scientific Research", "Security", "Travel",
}


def read_json(path: Path, errors: list[str]) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
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
    except (OSError, UnicodeError) as exc:
        errors.append(f"{label}: cannot read file ({exc})")
        return

    if len(text.encode("utf-8")) > 1024 * 1024:
        errors.append(f"{label}: SKILL.md exceeds 1 MiB")
    if not text.startswith("---\n"):
        errors.append(f"{label}: missing YAML frontmatter opening delimiter")
        return

    closing = text.find("\n---\n", 4)
    if closing == -1:
        errors.append(f"{label}: missing YAML frontmatter closing delimiter")
        return

    frontmatter = text[4:closing]
    # These repository skills deliberately use plain strings and folded text.
    # This is a structural check of that subset, not a general YAML parser.
    entries = re.findall(r"^([A-Za-z_-]+):[ \t]*(.*(?:\n[ \t]+.*)*)", frontmatter, re.MULTILINE)
    values = dict(entries)
    if len(entries) != len(values):
        errors.append(f"{label}: duplicate frontmatter keys")
    for required_key in ("name", "description"):
        value = values.get(required_key, "").strip()
        if value in {"", "null", "~", "true", "false", "[]", "{}", "''", '""', ">", ">-", "|", "|-"}:
            errors.append(f"{label}: frontmatter needs a nonblank string {required_key!r}")
    if values.get("name", "").strip() != skill_path.parent.name:
        errors.append(f"{label}: frontmatter name must match its skill directory")

    references = re.findall(r"\]\(([^)]+)\)|`((?:references|templates|assets)/[^`]+)`", text)
    for markdown_link, code_path in references:
        target = (markdown_link or code_path).split("#", 1)[0]
        if not target or urlsplit(target).scheme:
            continue
        referenced = (skill_path.parent / target).resolve()
        if not referenced.is_relative_to(PLUGIN.resolve()) or not referenced.exists():
            errors.append(f"{label}: missing or external local reference {target!r}")


def validate_interface(interface: object, errors: list[str]) -> None:
    label = "Portable interface"
    if not isinstance(interface, dict):
        errors.append(f"{label}: expected an object at extensions.com.openai.interface")
        return
    for field in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        value = require_value(interface, field, label, errors)
        if field in {"displayName", "shortDescription"} and len(value) > 30:
            errors.append(f"{label}: {field} must be at most 30 characters")
    if not isinstance(interface.get("category"), str) or interface["category"] not in CATEGORIES:
        errors.append(f"{label}: unsupported category")
    capabilities = interface.get("capabilities", [])
    if not isinstance(capabilities, list) or any(not isinstance(x, str) or not x.strip() for x in capabilities):
        errors.append(f"{label}: capabilities must be an array of nonblank strings")
    prompts = interface.get("defaultPrompt")
    prompts = [prompts] if isinstance(prompts, str) else prompts
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3 or any(
        not isinstance(prompt, str) or not prompt.strip() or "\n" in prompt or len(prompt) > 128
        for prompt in (prompts if isinstance(prompts, list) else [])
    ):
        errors.append(f"{label}: defaultPrompt must contain 1-3 nonblank single-line prompts of at most 128 characters")
    for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        if field in interface:
            value = interface[field]
            try:
                parsed = urlsplit(value) if isinstance(value, str) else None
            except ValueError:
                parsed = None
            if parsed is None or parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
                errors.append(f"{label}: {field} must be an absolute HTTPS URL without credentials")
    for field in ("logo", "composerIcon", "logoDark", "composerIconDark"):
        if field not in interface:
            continue
        value = interface[field]
        if not isinstance(value, str) or not value.strip() or Path(value).is_absolute():
            errors.append(f"{label}: {field} must be a contained relative asset path")
            continue
        asset = PLUGIN / value
        if asset.is_symlink() or not asset.resolve().is_relative_to(PLUGIN.resolve()) or not asset.is_file():
            errors.append(f"{label}: missing, symlinked or external {field} asset")
        elif asset.stat().st_size > 5 * 1024 * 1024 or asset.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".svg"}:
            errors.append(f"{label}: {field} must be a supported image no larger than 5 MiB")
    for field in ("brandColor", "brandColorDark"):
        if field in interface and (not isinstance(interface[field], str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", interface[field])):
            errors.append(f"{label}: {field} must be a six-digit hexadecimal color")


def validate_repository() -> list[str]:
    errors: list[str] = []

    required_paths = [
        ROOT / "README.md",
        ROOT / "LICENSE",
        ROOT / ".claude-plugin" / "marketplace.json",
        ROOT / ".agents" / "plugins" / "marketplace.json",
        PLUGIN / "plugin.json",
        PLUGIN / ".claude-plugin" / "plugin.json",
        PLUGIN / ".codex-plugin" / "plugin.json",
        PLUGIN / "LICENSE",
        PLUGIN / "PRIVACY.md",
        PLUGIN / "README.md",
        PLUGIN / "CHANGELOG.md",
    ]
    for path in required_paths:
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")

    portable = read_json(PLUGIN / "plugin.json", errors)
    claude = read_json(PLUGIN / ".claude-plugin" / "plugin.json", errors)
    codex = read_json(PLUGIN / ".codex-plugin" / "plugin.json", errors)
    claude_marketplace = read_json(ROOT / ".claude-plugin" / "marketplace.json", errors)
    codex_marketplace = read_json(ROOT / ".agents" / "plugins" / "marketplace.json", errors)

    versions: list[tuple[str, str]] = []
    for label, manifest in (("Portable manifest", portable), ("Claude manifest", claude), ("Codex manifest", codex)):
        if require_value(manifest, "name", label, errors) not in ("", PLUGIN_NAME):
            errors.append(f"{label}: name must be {PLUGIN_NAME!r}")
        version = require_value(manifest, "version", label, errors)
        if version:
            versions.append((label, version))
            if SEMVER.fullmatch(version) is None:
                errors.append(f"{label}: version must be strict SemVer")

    if portable.get("$schema") != PLUGIN_SCHEMA:
        errors.append("Portable manifest: missing or incorrect Agent Plugins 1.0 schema")
    for field in ("skills", "mcpServers", "apps", "interface"):
        if field in portable:
            errors.append(f"Portable manifest: {field!r} is not a supported root field")
    extensions = portable.get("extensions", {})
    openai = extensions.get("com.openai", {}) if isinstance(extensions, dict) else {}
    interface = openai.get("interface") if isinstance(openai, dict) else None
    validate_interface(interface, errors)
    if codex.get("interface") != interface:
        errors.append("Codex interface must match the portable OpenAI interface")
    if codex.get("skills") != "./skills/":
        errors.append("Codex manifest: skills must point at ./skills/")

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
    if {path.parent.name for path in skill_files} != EXPECTED_SKILLS:
        errors.append("plugin must contain both interview-pitch and shahar-cv-optimizer skills")
    for skill_file in skill_files:
        validate_skill(skill_file, errors)
    for style in ("classic", "crimson", "warm"):
        reference = skills_dir / "shahar-cv-optimizer" / "assets" / "cv-design-examples" / f"{style}-reference.pdf"
        if not reference.is_file() or not reference.read_bytes().startswith(b"%PDF-"):
            errors.append(f"missing or invalid {style} PDF design reference")

    return errors


def main() -> int:
    errors = validate_repository()

    if errors:
        print("Plugin validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    version = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))["version"]
    print(f"Plugin package is valid: {PLUGIN_NAME} v{version} ({len(EXPECTED_SKILLS)} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

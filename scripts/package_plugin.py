#!/usr/bin/env python3
"""Build and verify a reproducible, self-contained ChatGPT plugin ZIP."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path

from validate_plugin import BROWSER_APP_ID, EXPECTED_SKILLS, PLUGIN, PLUGIN_NAME, ROOT, validate_repository


ROOT_FILES = {"plugin.json", ".app.json", "LICENSE", "README.md", "PRIVACY.md", "CHANGELOG.md"}
SKILL_DIRECTORIES = {"references", "templates", "assets", "agents", "scripts"}
EXCLUDED_DIRECTORIES = {"tests", "eval", "__pycache__", ".cache", ".git", "node_modules", "dist"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".tmp", ".log", ".key", ".pem", ".p12", ".pfx"}


def included(path: Path) -> bool:
    """Only package known runtime locations; never follow symlinks."""
    relative = path.relative_to(PLUGIN)
    parts = relative.parts
    ancestors = [PLUGIN.joinpath(*parts[:index]) for index in range(1, len(parts) + 1)]
    if not path.is_file() or any(item.is_symlink() for item in ancestors):
        return False
    if any(part in EXCLUDED_DIRECTORIES for part in parts):
        return False
    if len(parts) == 1:
        return parts[0] in ROOT_FILES
    if any(part.startswith(".") and part not in {".codex-plugin", ".claude-plugin"} for part in parts):
        return False
    if path.stem.lower() in {"credentials", "secrets"} or path.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    if parts[0] in {".codex-plugin", ".claude-plugin"}:
        return parts[1:] == ("plugin.json",)
    if parts[0] == "assets":
        return True
    return parts[0] == "skills" and len(parts) >= 3 and (
        parts[2:] == ("SKILL.md",) or parts[2] in SKILL_DIRECTORIES
    )


def verify_archive(archive: Path, expected: dict[str, bytes]) -> None:
    """Check the exact inventory and bytes, including hidden compatibility files."""
    required = ROOT_FILES | {".codex-plugin/plugin.json", ".claude-plugin/plugin.json"}
    required |= {f"skills/{skill}/SKILL.md" for skill in EXPECTED_SKILLS}
    required |= {
        f"skills/shahar-cv-optimizer/assets/cv-design-examples/{style}-reference.pdf"
        for style in ("classic", "crimson", "warm")
    }
    missing = {f"{PLUGIN_NAME}/{path}" for path in required} - expected.keys()
    if missing:
        raise ValueError(f"archive is missing required runtime files: {', '.join(sorted(missing))}")
    with zipfile.ZipFile(archive) as packaged:
        names = packaged.namelist()
        if len(names) != len(set(names)) or set(names) != set(expected):
            raise ValueError("archive inventory differs from the selected plugin files")
        if packaged.testzip() is not None:
            raise ValueError("archive has a corrupt entry")
        for name, content in expected.items():
            if packaged.read(name) != content:
                raise ValueError(f"archive content differs from source: {name}")
        manifest = json.loads(packaged.read(f"{PLUGIN_NAME}/plugin.json"))
        if manifest["name"] != PLUGIN_NAME:
            raise ValueError("archive plugin identity differs from the source")
        apps = json.loads(packaged.read(f"{PLUGIN_NAME}/.app.json"))
        if manifest["extensions"]["com.openai"]["apps"] != "./.app.json" or apps != {"apps": {"browser": {"id": BROWSER_APP_ID}}}:
            raise ValueError("archive Browser dependency differs from the verified app binding")
        for field in ("logo", "composerIcon", "logoDark", "composerIconDark"):
            icon = manifest["extensions"]["com.openai"]["interface"].get(field)
            if icon and f"{PLUGIN_NAME}/{icon.removeprefix('./')}" not in expected:
                raise ValueError(f"archive is missing the {field} asset")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="ZIP destination (default: dist/<name>-<version>.zip)")
    args = parser.parse_args()
    errors = validate_repository()
    if errors:
        print("Plugin validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    manifest = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
    archive = (args.output or ROOT / "dist" / f"{PLUGIN_NAME}-{manifest['version']}.zip").resolve()
    if archive.is_relative_to(PLUGIN.resolve()):
        parser.error("archive must be outside the plugin source directory")
    if archive.suffix.lower() != ".zip":
        parser.error("output path must end with .zip")
    expected = {
        f"{PLUGIN_NAME}/{path.relative_to(PLUGIN).as_posix()}": path.read_bytes()
        for path in sorted(PLUGIN.rglob("*")) if included(path)
    }
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as packaged:
        for name, content in expected.items():
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            packaged.writestr(info, content, compresslevel=9)
    verify_archive(archive, expected)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    print(f"Built and verified {archive} ({len(expected)} files, {archive.stat().st_size} bytes)")
    print(f"SHA-256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

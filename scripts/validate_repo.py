#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
README_PATH = ROOT / "README.md"
CODEX_PLUGIN_PATH = ROOT / ".codex-plugin" / "plugin.json"
JSON_PATHS = [
    ROOT / ".codex-plugin" / "plugin.json",
    ROOT / ".claude-plugin" / "plugin.json",
    ROOT / ".claude-plugin" / "marketplace.json",
    ROOT / ".agents" / "plugins" / "marketplace.json",
]
SKILL_EXCLUDE_DIRS = {"_template", "plugin-skills", "tasks", "docs", "scripts"}
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
FIELD_RE = re.compile(r"^([a-zA-Z0-9_-]+):\s*(.+)$", re.MULTILINE)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        raise SystemExit(f"Missing required JSON file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"Invalid JSON in {path.relative_to(ROOT)}:{exc.lineno}:{exc.colno}: {exc.msg}"
        )


def discover_skills() -> list[Path]:
    skills: list[Path] = []
    for child in sorted(ROOT.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith(".") or child.name in SKILL_EXCLUDE_DIRS:
            continue
        if (child / "SKILL.md").exists():
            skills.append(child)
    return skills


def parse_frontmatter(skill_path: Path) -> dict[str, str]:
    text = skill_path.read_text()
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise SystemExit(f"Missing YAML frontmatter in {skill_path.relative_to(ROOT)}")

    fields = {key: value.strip() for key, value in FIELD_RE.findall(match.group(1))}
    required_fields = {"name", "description"}
    missing = required_fields - fields.keys()
    if missing:
        missing_fields = ", ".join(sorted(missing))
        raise SystemExit(
            f"Missing frontmatter field(s) in {skill_path.relative_to(ROOT)}: {missing_fields}"
        )
    return fields


def validate_readme(skills: list[Path]) -> None:
    readme_text = README_PATH.read_text()
    for skill_dir in skills:
        snippet = f"[{skill_dir.name}]({skill_dir.name}/)"
        if snippet not in readme_text:
            raise SystemExit(
                f"README.md is missing a discoverable link for skill '{skill_dir.name}'"
            )


def validate_packaged_skills(skills: list[Path], codex_plugin: dict) -> None:
    packaged_path = codex_plugin.get("skills")
    if packaged_path != "./plugin-skills/":
        return

    packaged_root = ROOT / "plugin-skills"
    if not packaged_root.is_dir():
        raise SystemExit("Codex plugin expects ./plugin-skills/, but that directory is missing")

    expected = {skill_dir.name for skill_dir in skills}
    actual = {entry.name for entry in packaged_root.iterdir()}

    missing = sorted(expected - actual)
    if missing:
        raise SystemExit(
            "plugin-skills/ is missing packaged entries for: " + ", ".join(missing)
        )

    unexpected = sorted(actual - expected)
    if unexpected:
        raise SystemExit(
            "plugin-skills/ contains unexpected entries: " + ", ".join(unexpected)
        )

    for entry in packaged_root.iterdir():
        try:
            entry.resolve(strict=True)
        except FileNotFoundError:
            raise SystemExit(f"Broken packaged skill entry: {entry.relative_to(ROOT)}")


def main() -> int:
    codex_plugin = load_json(CODEX_PLUGIN_PATH)
    for path in JSON_PATHS[1:]:
        load_json(path)

    skills = discover_skills()
    if not skills:
        raise SystemExit("No top-level skills were found")

    for skill_dir in skills:
        fields = parse_frontmatter(skill_dir / "SKILL.md")
        if fields["name"] != skill_dir.name:
            raise SystemExit(
                f"Frontmatter name mismatch in {skill_dir / 'SKILL.md'}: "
                f"expected '{skill_dir.name}', found '{fields['name']}'"
            )

    validate_readme(skills)
    validate_packaged_skills(skills, codex_plugin)

    print(
        f"Validated {len(JSON_PATHS)} JSON files, {len(skills)} skills, and README skill links."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

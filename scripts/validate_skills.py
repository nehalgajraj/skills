#!/usr/bin/env python3
"""Lightweight validation for skills in ./skills."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening frontmatter delimiter")

    lines = text.splitlines()
    try:
        end = lines[1:].index("---") + 1
    except ValueError as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc

    frontmatter = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip()
    return frontmatter


def validate_skill_dir(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir.name}: missing SKILL.md"]

    try:
        fm = parse_frontmatter(skill_md)
    except ValueError as err:
        return [f"{skill_dir.name}: {err}"]

    allowed = {"name", "description"}
    keys = set(fm)
    if not {"name", "description"}.issubset(keys):
        errors.append(f"{skill_dir.name}: frontmatter must include name and description")
    extra = keys - allowed
    if extra:
        errors.append(f"{skill_dir.name}: unsupported frontmatter keys: {sorted(extra)}")

    skill_name = fm.get("name", "")
    if skill_name and not NAME_RE.match(skill_name):
        errors.append(f"{skill_dir.name}: invalid name '{skill_name}'")
    if skill_name and skill_name != skill_dir.name:
        errors.append(
            f"{skill_dir.name}: frontmatter name '{skill_name}' must match folder name"
        )

    description = fm.get("description", "")
    if not description:
        errors.append(f"{skill_dir.name}: description cannot be empty")

    return errors


def main() -> int:
    if not SKILLS_DIR.exists():
        raise SystemExit("skills directory does not exist")

    all_errors: list[str] = []
    for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        all_errors.extend(validate_skill_dir(skill_dir))

    if all_errors:
        print("Validation failed:")
        for err in all_errors:
            print(f"- {err}")
        return 1

    print("All skills valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

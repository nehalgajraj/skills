#!/usr/bin/env python3
"""Scaffold a new portable skill folder."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")


def normalize_name(raw: str) -> str:
    normalized = raw.strip().lower().replace("_", "-").replace(" ", "-")
    normalized = re.sub(r"[^a-z0-9-]", "", normalized)
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    return normalized


def write_skill_md(path: Path, name: str) -> None:
    content = f"""---
name: {name}
description: TODO: describe what this skill does and when to use it.
---

# {name}

Add concise, imperative instructions for this skill.
"""
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new skill scaffold.")
    parser.add_argument("name", help="Skill name (will be normalized to lowercase hyphen-case).")
    parser.add_argument(
        "--with-scripts",
        action="store_true",
        help="Also create a scripts directory.",
    )
    parser.add_argument(
        "--with-references",
        action="store_true",
        help="Also create a references directory.",
    )
    parser.add_argument(
        "--with-agents",
        action="store_true",
        help="Also create an agents directory.",
    )
    parser.add_argument(
        "--with-assets",
        action="store_true",
        help="Also create an assets directory.",
    )
    args = parser.parse_args()

    name = normalize_name(args.name)
    if not NAME_RE.match(name):
        raise SystemExit(f"Invalid skill name: '{name}'")

    skill_dir = SKILLS_DIR / name
    if skill_dir.exists():
        raise SystemExit(f"Skill already exists: {skill_dir}")

    skill_dir.mkdir(parents=True)
    if args.with_scripts:
        (skill_dir / "scripts").mkdir()
    if args.with_references:
        (skill_dir / "references").mkdir()
    if args.with_agents:
        (skill_dir / "agents").mkdir()
    if args.with_assets:
        (skill_dir / "assets").mkdir()

    write_skill_md(skill_dir / "SKILL.md", name)
    print(f"Created skill scaffold: {skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

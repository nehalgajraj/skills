# Agent Skill Library

This repository is a catalog of portable skills.

## Rules

1. Keep each skill in `skills/<skill-name>/`.
2. Every skill must include `SKILL.md` with YAML frontmatter:
   - `name`
   - `description`
3. Keep instructions concise and action-oriented.
4. Put reusable code in `scripts/`, docs in `references/`, and output assets in `assets/`.
5. Run `python3 scripts/validate_skills.py` before commits.

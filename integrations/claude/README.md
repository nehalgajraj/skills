# Claude Integration Assets

This directory contains example workflow assets for Claude-style setups.

Template root:
`integrations/claude/template/.claude/`

Includes:
- `hooks/session-audit.sh`
- `hooks/session-end-report.sh`
- `skills/start/skill.md`
- `skills/end/skill.md`
- `settings.local.json`

Usage:
1. Copy `integrations/claude/template/.claude/` into your target repo as `.claude/`.
2. Review hook command paths and permissions in `.claude/settings.local.json`.
3. Ensure your repo has `scripts/generate_session_doc.py` if you keep `session-end-report.sh` unchanged.

# Skills

Nehal's skills for AI coding agents.

## Available Skills

| Skill | What it does |
|---|---|
| `attack` | Runs a multi-angle adversarial critique of a plan, patch, PR, architecture, incident analysis, or answer. |
| `babysit` | Drives a GitHub pull request toward merge readiness by checking CI, review state, conflicts, branch freshness, and blockers. |
| `beforeafter` | Explains behavior changes with side-by-side ASCII Before/After flow diagrams. |
| `graph` | Generates polished matplotlib PNG charts from metrics data, with simple and detailed modes. |
| `teachback` | Teaches a complex session, code change, bug, or architecture incrementally until the user can explain it back. |

## Layout

```text
skills/
  attack/
    SKILL.md
  babysit/
    SKILL.md
  beforeafter/
    SKILL.md
  graph/
    SKILL.md
    style.py
    example_simple.py
    example_detailed.py
  teachback/
    SKILL.md
```

## Usage

Copy a skill directory into your local agent skills folder:

```bash
cp -R skills/attack ~/.codex/skills/
cp -R skills/graph ~/.claude/skills/
```

Then invoke the skill by name in an agent session, such as `/attack`,
`/babysit`, `/beforeafter`, `/graph`, or `/teachback`.

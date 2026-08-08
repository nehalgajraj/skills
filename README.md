# Agent Skill Library

Portable agent skills I use regularly, packaged so other people can install them with `npx skills`.

The repo uses `skills/<name>/SKILL.md` as the source of truth. Optional helper scripts and references live inside each skill folder only when the skill actually needs them.

This is personal infrastructure, not a dump of work-specific agent code. Skills that mention employer systems, private repos, or proprietary workflows should stay out of this public catalog.

## Included Skills

- `start`: start a scoped work session with a worktree and session metadata
- `end`: wrap up a scoped work session with a summary, commit flow, and cleanup

## Install

List the skills in this repo:

```bash
npx skills add https://github.com/nehalgajraj/skills --list
```

Install both skills:

```bash
npx skills add https://github.com/nehalgajraj/skills \
  --skill start,end \
  --agent codex \
  --agent claude-code
```

Install one skill:

```bash
npx skills add https://github.com/nehalgajraj/skills \
  --skill start \
  --agent codex
```

## Repo Layout

```text
skills/
  start/
    SKILL.md
  end/
    SKILL.md
scripts/
  new_skill.py
  validate_skills.py
integrations/
  claude/
  codex/
```

## Authoring

Create a new skill scaffold:

```bash
python3 scripts/new_skill.py my-skill
```

Validate the skill set:

```bash
python3 scripts/validate_skills.py
```

## Integrations

`integrations/` contains optional setup examples for Claude and Codex workflows. They are not required for `npx skills` packaging.

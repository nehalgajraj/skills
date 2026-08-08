---
name: start
description: Start a tracked work session for a task by creating a git worktree, branch, and session metadata file. Use when the user asks to begin scoped work in an isolated branch/worktree with preserved task context.
---

# Start

Start a tracked work session for a task in an isolated worktree. The task description drives the session slug and is embedded in context docs for the new agent session.

## Steps

1. Parse the user task description from the prompt.
2. Derive a slug from the first meaningful words (lowercase, hyphenated).
3. If `.claude/sessions/{slug}.json` exists, ask whether to resume or recreate.
4. Create the worktree and branch:
   `mkdir -p worktrees && git worktree add worktrees/{slug} -b work/{slug}`
5. Save session metadata to `.claude/sessions/{slug}.json` with name, slug, started_at, base_branch, base_sha, worktree_path, branch, and optional reference_file.
6. Write `CLAUDE.md` in the new worktree with task context. If repo root already has a `CLAUDE.md`, prepend session context and keep existing instructions below a separator.
7. Print a short summary with task, worktree, branch, and next command to launch the agent in that worktree.
8. Do not perform implementation work in this step.

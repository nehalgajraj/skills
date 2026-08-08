---
name: start
description: Start a work session for a task — creates a git worktree and CLAUDE.md with the task context.
argument-hint: "task description (e.g., fix backtester buy logic, add grid bot stop-loss)"
disable-model-invocation: false
---

Start a tracked work session for a task in an isolated worktree. The task description drives the session name and is embedded in CLAUDE.md so the new Claude instance knows exactly what to work on.

## Steps

1. Parse `$ARGUMENTS` to get the **task description**. If empty, ask what task they want to work on.
   - The full argument string is the task (e.g., "fix backtester buy logic" or "add stop-loss to grid bot").
   - If the argument contains a file path (contains `/` or ends in `.md`, `.py`, `.json`, etc.), extract it as a **reference file** and use the rest as the task description. If no text remains after extracting the path, use the filename (without extension) as the task description.

2. Derive a **slug** from the task description: take the first 4-6 meaningful words, lowercase, hyphenated, no spaces. E.g., "fix backtester buy logic for oscillator" → `fix-backtester-buy-logic`.

3. Check if `.claude/sessions/{slug}.json` already exists. If yes, warn the user that this session exists (show start time and worktree path) and ask if they want to resume it (just cd to existing worktree) or start fresh (delete old worktree + branch + session file, recreate).

4. Create the worktree and branch:
   ```bash
   mkdir -p worktrees
   git worktree add worktrees/{slug} -b work/{slug}
   ```

5. Save session metadata to `.claude/sessions/{slug}.json`:
   ```json
   {
     "name": "<original task description from arguments>",
     "slug": "<slug>",
     "started_at": "<ISO 8601 timestamp>",
     "base_branch": "<current branch at time of start>",
     "base_sha": "<HEAD sha at time of start>",
     "worktree_path": "<absolute path to worktree>",
     "branch": "work/<slug>",
     "reference_file": "<path if a file was given, null otherwise>"
   }
   ```
   Create `.claude/sessions/` directory if needed.

6. **Context transfer:** Write a `CLAUDE.md` in the worktree root with the task context:

   - If a reference file was identified, read its contents.
   - Write:

   ```markdown
   # Task: <task description>

   Branch: work/<slug> (based on <base_branch> @ <short sha>)
   Started: <date>

   ## Task

   <task description — the full original argument>

   ## Reference

   <Full contents of the reference file, or "No reference file provided." if none>

   ## Instructions

   Complete the task described above. Read the reference (if any) carefully before starting.
   When done, run `/end` to wrap up (commit, report, PR, cleanup).
   ```

   **Important:** If a `CLAUDE.md` already exists in the repo root, prepend the session context above a `---` separator, then include the original CLAUDE.md contents below it. Do NOT overwrite existing project instructions.

7. Print confirmation:
   ```
   Session started: "<task description>"
   Worktree: worktrees/{slug}
   Branch: work/{slug} (based on <base_branch> @ <short sha>)

   Open a new Claude there:
     cd worktrees/{slug} && claude

   Task context has been written to CLAUDE.md — the new Claude will auto-load it.
   Run /end from that session when done.
   ```

8. Do NOT do any other work. This skill only sets up the workspace.

$ARGUMENTS

---
name: end
description: End a work session — commit, generate analysis report, create PR, clean up worktree.
argument-hint: "session slug (optional — auto-detects from current branch or worktree)"
disable-model-invocation: true
---

End the current work session: generate a report, commit everything, create a PR, and clean up.

## Steps

### 1. Find the session

- If `$ARGUMENTS` is provided, sanitize it into a slug and look for `.claude/sessions/{slug}.json` (check both current repo and parent repo's `.claude/`).
- If no arguments, detect automatically:
  - Check current branch: if it starts with `work/`, extract the slug.
  - Check if we're in a worktree: `git rev-parse --show-toplevel` vs `git rev-parse --git-common-dir` — if they differ, we're in a worktree.
  - Look for the session file in the **main repo's** `.claude/sessions/` directory (the common git dir's parent).
- **If found:** Read it to get `base_sha`, `base_branch`, `worktree_path`, `branch`, `name`, `reference_file`.
- **If not found:** Fall back — use current branch, diff against `main`, infer session name from `$ARGUMENTS` or branch name. Warn that no `/start` session was found.

### 2. Gather changes

Run these in parallel:
- `git diff {base_sha}..HEAD --stat` — all changes since session start
- `git diff {base_sha}..HEAD` — full diff for analysis
- `git log {base_sha}..HEAD --oneline` — commits made during session
- `git diff HEAD` — any uncommitted changes
- `git status --porcelain` — dirty files

If there are uncommitted changes, commit them first (stage all, use a descriptive message based on what changed).

### 3. Review conversation

Review the full conversation to identify:
- What strategy/feature was worked on
- Bugs found and fixed
- What was tested (backtests, parameter sweeps, paper runs)
- Key results and numbers

### 4. Write the report

Find the main repo path (parent of worktree, or current repo if not in a worktree).
Check existing reports with `ls {main_repo}/reports/` to find the next number suffix.

Format: `reports/{topic_snake_case}_analysis_{NNN}.md`

Write the report to the **main repo's** `reports/` directory (so it's accessible after worktree cleanup).

Create the report with these sections:

#### Required Sections

- **TLDR** — 2-3 sentences. What was done, bottom line result.
- **What Was Broken / Changed** — Bugs found, fixes applied, file names.
- **Parameter Sweep Results** — If optimization was done, summarize search levels and key findings. Skip if no sweep was run.
- **Best Config Found** — Code block with optimal parameter values and brief annotations. Skip if not applicable.
- **Robustness Stats** — Results across data subsets (chrono chunks, random splits, bootstrap, rolling windows). Skip if not tested.
- **What Works** — Numbered list of what drives the edge.
- **What Doesn't Work** — Numbered list of what hurts performance.
- **Known Risks / Caveats** — Overfitting, sample size, fill realism, param sensitivity.
- **Files Changed** — List of modified files with one-line descriptions.
- **Next Steps** — Checkbox list of follow-up work.

Commit the report file after writing it.

### 5. Push and create PR

- Push the branch: `git push -u origin work/{slug}`
- Create a PR targeting `{base_branch}` using `gh pr create`:
  - **Title:** Session name (from session file or arguments)
  - **Body:** Use the report's TLDR as summary, list files changed, link to the report file in the repo.
  - Format:
    ```
    ## Summary
    <TLDR from report>

    ## Changes
    <bulleted list of files changed with one-line descriptions>

    ## Report
    See `reports/{filename}` for full analysis.

    🤖 Generated with [Claude Code](https://claude.com/claude-code)
    ```
- Print the PR URL.

### 6. Clean up

- Find the main repo path: use `git rev-parse --git-common-dir` to get the `.git` path, then derive the main repo root from it.
- Delete the session file using its absolute path: `rm {main_repo_path}/.claude/sessions/{slug}.json`
- Remove the worktree **from outside it** — you can't remove a directory you're standing in. Run:
  ```bash
  git -C {main_repo_path} worktree remove {worktree_path}
  ```
  This runs git from the main repo's context, so it works even though your cwd is the worktree being deleted.
- If the worktree remove fails (e.g., dirty files), force it: `git -C {main_repo_path} worktree remove --force {worktree_path}`
- Print summary:
  ```
  Session ended: "<name>"
  Report: reports/{filename}
  PR: <url>
  Worktree cleaned up.
  ```

### Guidelines

- Keep the report concise. Goal: reading it cold gets someone fully up to speed in under 2 minutes.
- Prefer conversation context over git diffs when both are available — conversation has the "why", git has the "what".
- If the session was long with many changes, group related changes under subheadings.
- Skip report sections that don't apply (no sweep = skip Parameter Sweep Results).
- If `gh` is not available or PR creation fails, skip the PR step and tell the user to create it manually.

$ARGUMENTS

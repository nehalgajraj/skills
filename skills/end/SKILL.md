---
name: end
description: End a tracked work session by summarizing changes, committing pending work, creating a report, opening a PR, and cleaning up session/worktree artifacts. Use when the user asks to wrap up a scoped branch session.
---

# End

End the current work session: generate a report, commit work, optionally create a PR, and clean up.

## Steps

1. Locate the session file from argument slug or infer from current `work/<slug>` branch/worktree.
2. Collect diffs, commit history, and working tree status since session start (`base_sha`).
3. If there are uncommitted changes, stage and commit with a descriptive message.
4. Write a concise report in the main repo `reports/` directory with TLDR, changes, risks, changed files, and next steps.
5. Commit the report.
6. Push the branch and open a PR targeting the base branch when `gh` is available.
7. Remove the session file and delete the worktree from the main repo context.
8. Print a final summary with report path and PR URL (or note if PR could not be created).

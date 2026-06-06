---
name: babysit
description: "Drive a GitHub pull request from current state to mergeable: inspect CI, conflicts, review state, unresolved threads, branch freshness, and scope; take the smallest unblocking action; then push and watch checks until green or report the exact blocker."
---

# Babysit A Pull Request

Take a pull request from its current state to either mergeable or a precise
"blocked because..." report. This is a merge-readiness workflow, not a feature
development workflow.

## When To Use

- User says "babysit this PR", "get it mergeable", "health check this PR", or
  "get this PR ready to merge".
- User shares a GitHub PR URL or number and wants blockers resolved.
- The current branch has an open PR and the user wants it pushed through CI.

Do not use this skill to add unrelated scope, perform broad code review, or
argue against merging. Use a review or critique workflow for that.

## Inputs

- A PR URL, PR number, or the current branch's PR.
- A local checkout of the repository when code changes, rebases, or focused
  test runs are needed.
- Repository conventions from `AGENTS.md`, `CONTRIBUTING.md`, or the PR
  template, if present.

## Procedure

1. Snapshot PR state.
   - `gh pr view <N> --json number,title,url,author,mergeable,mergeStateStatus,reviewDecision,isDraft,additions,deletions,changedFiles,headRefName,baseRefName,updatedAt,createdAt,labels,statusCheckRollup`
   - `gh pr view <N> --json reviewThreads`
   - `gh pr view <N> --json reviews`
   - `gh pr view <N> --json commits`
   - Fetch the base branch and count how far the PR is behind it.
   - If a required check is failing, inspect the failing job log.

2. Render a compact status table.

   | Signal | Status | Detail |
   |---|---|---|
   | CI | PASS/WARN/FAIL | required checks and failing job names |
   | Human approval | PASS/WARN | latest reviewer decisions |
   | Review decision | PASS/FAIL | APPROVED / CHANGES_REQUESTED / REVIEW_REQUIRED |
   | Mergeable | PASS/FAIL | MERGEABLE / CONFLICTING / UNKNOWN |
   | Branch freshness | PASS/WARN | commits ahead/behind base |
   | Scope | PASS/WARN | additions/deletions/files |
   | Review threads | PASS/WARN | unresolved count and highest severity |

3. Work blockers in this order.
   - Conflicts or rebase needed.
   - Failing required CI checks.
   - Unresolved human review threads.
   - User-approved nits or mechanical cleanup.

4. Apply the smallest useful action.
   - Rebase or merge according to repository convention.
   - Resolve conflicts only when both sides are clear. Stop and report when the
     intent is ambiguous.
   - Fix failing checks by reading the log, finding the smallest local cause,
     and running the focused validation command that covers it.
   - Address unresolved review threads with code when needed. Do not mark a
     thread resolved unless the requested change is actually made.

5. Push and watch.
   - Push the branch using the repository's normal push convention.
   - Watch the next CI run instead of repeatedly polling blindly.
   - Re-snapshot only the rows that can change after the push.

## Stop Conditions

Stop and report success when the PR is mergeable, required checks are green, and
there are no unresolved blocking threads.

Stop and report a blocker when:

- a design decision is needed from the user;
- a secret, credential, or destructive operation is required;
- the same CI failure recurs after two attempted fixes;
- a conflict cannot be resolved without guessing.

## Output Shape

When done:

- one short paragraph explaining what changed and the final state;
- the PR URL;
- any commits pushed or rebases performed.

When blocked:

- the current status table;
- the specific blocker;
- one to three minimum-action options;
- the files or checks involved.

## Anti-Patterns

- Adding unrelated fixes while the PR is already close to mergeable.
- Force-pushing without saying why.
- Dismissing requested changes without addressing them.
- Editing unrelated dirty files in the worktree.
- Reinstalling dependencies unless the failing check points directly at
  dependency state.

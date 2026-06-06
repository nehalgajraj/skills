---
name: attack
description: Run an adversarial multi-angle critique of a proposed change, patch, plan, PR, architecture, incident analysis, or answer before accepting it. Use when the user invokes /attack or asks for a critic attack, red-team pass, adversarial review, three-angle critique, subagent critique, or independent challenge of work in progress.
---

# Attack

## Core Workflow

Use this skill to challenge the current work before it is shipped or relied on.

1. Define the target under attack: code diff, plan, answer, design, PR, incident analysis, or other artifact.
2. Choose three distinct critique angles that match the target.
3. Run each angle independently enough that one perspective does not bias the others.
4. Consolidate findings into concrete risks, fixes, and residual uncertainty.
5. If the attack identifies actionable issues and the user asked for implementation, patch the work and rerun relevant checks.

## Angle Selection

Prefer angles that cover different failure modes. Use the defaults below when the user does not specify angles:

- Correctness: logic, edge cases, contracts, state transitions, data flow, race conditions.
- Security: trust boundaries, authorization, token/session handling, injection, data leakage, destructive behavior.
- Verification: test coverage, brittle tests, missing regressions, validation gaps, maintainability.

Swap in more relevant angles when needed:

- Product: user journey, compatibility, rollout behavior, support burden.
- Performance: hot paths, caching, memory, network calls, scaling risks.
- Operations: observability, rollback, migrations, alerts, failure recovery.
- Architecture: coupling, abstractions, invariants, future extension, cross-service contracts.

## Subagent Use

Use subagents only when the user explicitly asks for subagents, delegation, or parallel agent work. When authorized:

- Spawn one subagent per angle.
- Give each subagent a bounded prompt with the target, its assigned angle, and an instruction not to edit files unless the user asked for patch workers.
- Keep prompts independent; avoid giving one subagent another subagent's conclusions.
- Continue local non-overlapping review while they run.
- Integrate results after they return; do not paste raw agent transcripts unless the user asks.

When subagents are not authorized, perform the three angles locally and label them clearly.

## Reporting

Lead with findings, ordered by severity and confidence. For each finding, include:

- A short title.
- The affected file, line, route, command, or artifact when applicable.
- Why it matters.
- The smallest credible fix or follow-up.

If no actionable issues are found, say so clearly and list residual risks or assumptions. Keep summaries brief; the value of this skill is concrete challenge, not broad commentary.

## Patch Loop

When the user wants fixes:

1. Patch only the issues surfaced by the attack.
2. Preserve unrelated dirty work.
3. Run focused verification first, then broader checks if the blast radius warrants it.
4. Re-run a shorter attack pass on the changed area before finalizing.

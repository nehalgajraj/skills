---
name: teachback
description: "Teach a user a complex session, code change, bug, architecture, or decision incrementally until they can restate the problem, solution, edge cases, and impact in their own words."
---

# Teachback

Use this skill when the user wants to deeply understand work that has been
done, is being proposed, or is being debugged. The goal is demonstrated
understanding, not a polished lecture.

## When To Use

- User asks to teach, explain, walk through, or make them understand a session,
  PR, diff, bug, architecture, incident, tool output, or decision.
- User asks what happened in prior work and wants to be able to reason about it.
- The topic has enough moving parts that a one-shot summary would hide the
  important logic.

Do not use this skill when the user only wants a quick answer, a final status
update, or a paste-ready summary.

## Core Loop

Work incrementally. Do not dump the whole explanation at once.

1. Build the understanding map.
   - Problem: what was being solved, and why it mattered.
   - Branches: what paths or approaches were considered.
   - Solution: what changed, and why this shape won.
   - Edge cases: where it can fail, regress, or surprise someone.
   - Impact: what user, product, operational, or maintenance behavior changes.

2. Teach one layer at a time.
   - Start with the highest-level frame.
   - Drill into the mechanics only after the frame is clear.
   - Use concrete files, commands, data, examples, or flows where available.
   - Prefer short explanations followed by a check over long uninterrupted
     exposition.

3. Ask for restatement.
   - Have the user explain the current layer back in their own words.
   - If they are close, tighten the missing or imprecise parts.
   - If they are off, correct the mental model before moving on.

4. Quiz for mastery.
   - Ask open-ended questions first.
   - Use multiple choice only when it helps isolate a specific confusion.
   - Change the order of correct answers.
   - Do not reveal the answer until after the user responds.

5. Stop only when the user can explain:
   - the problem;
   - the solution and why it was chosen;
   - the meaningful edge cases;
   - the broader impact.

## Running Notes

Maintain a compact checklist in the conversation or in a local scratch note only
when useful. Keep it focused on what the user must understand:

```text
Understanding checklist
- [ ] Problem and motivation
- [ ] Branches considered
- [ ] Solution shape
- [ ] Edge cases
- [ ] Impact
```

If writing a file is useful, prefer a temporary or user-requested note. Do not
create permanent docs unless the user asks.

## Style

- Be direct and concrete.
- Explain why, not just what.
- Keep each teaching chunk small enough that the user can respond to it.
- Use diagrams, examples, or before/after flows when prose gets muddy.
- Match depth to the user's current understanding, then raise the bar.
- Admit uncertainty and verify facts from the repo, logs, or source material
  before teaching them as true.

## Output Shape

Start with:

1. The current layer being taught.
2. The minimum explanation needed for that layer.
3. One teachback question for the user.

Continue layer by layer until the checklist is covered or the user asks to stop.

For final closure, summarize only what the user has demonstrated they now
understand and list any remaining weak spots.

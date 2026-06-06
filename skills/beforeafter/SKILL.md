---
name: beforeafter
description: "Explain a bug, proposed change, or diff via side-by-side ASCII Before and After flow diagrams that show how control or data flows through the system and where behavior differs."
---

# Before/After Flow Explainer

Produce a clear Before -> After explanation of a bug or change, grounded in the
actual code, using compact ASCII box-and-arrow diagrams.

## When To Use

- User invokes `/beforeafter`.
- User asks for a flow diagram, before/after explanation, or a walkthrough of
  how a bug breaks versus how a fix works.
- A non-trivial bug fix or architecture change is easier to understand with
  parallel flows than prose alone.

Do not use this skill for single-function changes, pure refactors with no
observable behavior change, or questions that only need one "what does this
code do?" flow.

## Required Structure

1. One-line framing: what bug or change is being visualized, and where it
   lives.
2. Bug list: only when multiple independent bugs are being fixed together.
3. Before diagram: top-to-bottom flow showing the broken path. Mark the exact
   failure point with `<-- BUG`.
4. After diagram: same shape when possible, showing the fixed path. Mark new
   logic with `<-- NEW` or `<-- fixes A`.
5. Caveats / follow-ups: anything the diagram does not capture.

## Diagram Conventions

- Use plain ASCII boxes and arrows so the diagram renders in any terminal.
- One box per logical component or call site.
- Label each box with the component name and file path when relevant.
- Show concrete decisions, values, and branches instead of vague prose.
- Mark the root-cause node, not the final user-visible error.
- Before and After should keep the same shape whenever possible.

## Workflow

1. Trace the current code path. Read the files involved before drawing.
2. Pin the failure point: the first line or branch where behavior diverges.
3. Trace the fixed path from the diff or proposed change.
4. Draft the Before diagram using only the nodes needed to understand the bug.
5. Draft the After diagram in the same shape, changing only the affected nodes.
6. Sanity-check function names, keys, and file paths with search.

## Example

```text
Before

+-- UI loads project settings (src/settings.ts) ------------------+
| read session.projectId -> empty                                 |
| fallback project id -> "default"                         <-- BUG |
+-------------------------------+---------------------------------+
                                |
                                v
+-- API request builder (src/api.ts) -----------------------------+
| GET /api/projects/default/config                                |
| returns unrelated config                                        |
+-------------------------------+---------------------------------+
                                |
                                v
+-- Renderer (src/render.ts) -------------------------------------+
| displays stale feature flags                                    |
+-----------------------------------------------------------------+

After

+-- UI loads project settings (src/settings.ts) ------------------+
| read route.params.projectId -> "acme"                    <-- NEW |
| fallback only when route param is absent                         |
+-------------------------------+---------------------------------+
                                |
                                v
+-- API request builder (src/api.ts) -----------------------------+
| GET /api/projects/acme/config                                   |
| returns requested project config                                |
+-------------------------------+---------------------------------+
                                |
                                v
+-- Renderer (src/render.ts) -------------------------------------+
| displays current feature flags                                  |
+-----------------------------------------------------------------+
```

## Output Format

- Markdown.
- Diagrams inside fenced `text` code blocks.
- File references as clickable markdown links when the client supports them.
- Tight prose around the diagrams. The diagrams should carry the explanation.

## Anti-Patterns

- Inventing function names or file paths.
- Drawing arrows with no concrete values.
- Marking the symptom instead of the root-cause branch.
- Making the Before and After diagrams so different that comparison becomes
  work.
- Boxing every trivial call instead of grouping obvious sequential steps.

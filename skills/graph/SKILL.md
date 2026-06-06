---
name: graph
description: "Generate a polished PNG chart from metrics data using matplotlib. Two modes: 'simple' (one or two clean panels, fast) and 'detailed' (KPI cards plus multi-panel dashboard with callouts, ready to share in chat, docs, or leadership updates). Trigger when the user asks for a graph, chart, pretty graph, shareable image, dashboard image, visualization, or wants to turn analytics output, SQL, CSV, retention tables, or growth metrics into a PNG."
---

# /graph - Polished metric charts (simple or detailed)

Turn raw metrics into a PNG that reads well in docs, chat, or a written update. Two modes:

- **simple** - one or two panels, minimal chrome. Use when the user just wants to see the data.
- **detailed** - KPI cards + 2-3 panels with annotations, reference lines, and outlier highlights. Use when the user wants to share with stakeholders.

## Picking the mode

| Signal | Mode |
|---|---|
| "graph this", "plot it", "show me a chart" | simple |
| "make it pretty", "shareable", "send to the team", "for leadership" | detailed |
| One series, no comparisons | simple |
| KPI roll-up + trend + retention | detailed |
| User explicitly says `simple` or `detailed` | obey |

If unclear, default to **simple** and offer to upgrade to detailed.

## Output contract

- One PNG, white background, 150 dpi.
- Saved next to the data the user is working with (or `/tmp/<slug>_chart.png` if no obvious location).
- Print the absolute path on completion.

| Mode | Canvas | Panels | KPI cards |
|---|---|---|---|
| simple | 12x6 in | 1 (or 2 stacked at 12x9) | none |
| detailed | 12x14 in | 2-3 stacked | 3 across the top |

## Visual conventions (both modes)

**Palette** - defined in `style.py`, use exclusively. Max **4 hues** in one chart.

| Name | Hex | Use for |
|---|---|---|
| `BLUE` | `#2E5BFF` | primary metric |
| `ORANGE` | `#FF8B3D` | secondary metric |
| `GREEN` | `#22C55E` | positive deltas, retention, "current" |
| `RED` | `#EF4444` | regressions, negative deltas, anomalies |
| `GREY` | `#94A3B8` | references, baselines, axis labels |
| `DARK` | `#1E293B` | titles, value labels |

**Typography**:
- Title: 22pt bold (simple) / 26pt bold (detailed), `DARK`.
- Panel title: 14pt bold (simple) / 16pt bold (detailed), `DARK`, left-aligned (`loc="left"`, `pad=12`).
- KPI number (detailed only): 30pt bold, palette color.
- KPI label: 12pt bold uppercase, `GREY`.
- Axis labels: 11pt. Tick labels: 10pt.
- Value labels on bars/points: 10-11pt bold, `DARK`.

**Fonts:** Helvetica Neue -> Helvetica -> Arial -> DejaVu Sans (set in `apply_style`).

**Style rules**:
- Top + right spines off. `grid(axis="y", linestyle=":", alpha=0.5)` with `set_axisbelow(True)`.
- No twin axes. Need two units? Stack two panels.
- No legend if there's a single series - title or annotation it instead.
- Do not rotate x-tick labels 45 degrees. Pick fewer ticks or shorten labels (`%b %d`).
- Avoid non-ASCII arrow glyphs. Use `to`, `-`, or mathtext `$\\rightarrow$`.

**Annotations** - reserved for things the reader must notice:
- Outlier bars: `RED` fill + arrow callout in white-bg box with `RED` border.
- Rebound bars: `GREEN` fill.
- Reference lines: `axhline` in `GREY` dashed, with text label sitting on the line.

## Component patterns

Use the helpers in `style.py` (read it first):

```python
from style import (
    apply_style,         # call once after importing pyplot
    PALETTE,             # named colors (BLUE, ORANGE, GREEN, RED, GREY, DARK)
    title_block,         # main title + date subtitle (detailed)
    kpi_card,            # tinted KPI card (detailed only)
    bar_with_labels,     # bars + value labels + outlier highlights
    smoothed_timeseries, # daily series + 7-day rolling avg + reference lines
    retention_curve,     # single curve with point labels
    save_chart,          # savefig with the right dpi/padding/bg
)
```

If the file is missing, restore it from this repository's `skills/graph/style.py`.

## Workflow

1. **Confirm the data is in hand.** Print it once for sanity-check. Do not paraphrase numbers; copy them in.
2. **Pick the mode** per the table above. Confirm with the user only if their intent is ambiguous.
3. **Identify outliers / anomalies** in the data before rendering, so the reader does not have to scan.
4. **Adapt the right example**:
   - simple -> `example_simple.py`
   - detailed -> `example_detailed.py`
5. **Run it.** Read the rendered PNG to confirm cropped text, overlapping annotations, and missing glyph warnings.
6. **Always provide share copy alongside the chart.** A short, paste-ready block in a fenced code block so the user can copy it as-is:
   - **simple mode:** 3-5 bullets, one per finding/number.
   - **detailed mode:** 2-3 line narrative summary that complements (not duplicates) the chart's KPI cards.
   - Lead with the punchline number, not preamble. Do not restate things the chart already shows visually; pull out the meaning.

## Sanity checks before declaring done

- [ ] Read the rendered PNG to confirm.
- [ ] No `glyph missing` matplotlib warnings.
- [ ] Title fits one line.
- [ ] Every KPI number / value label sourced from the data.
- [ ] x-axis has no more than 8 visible tick labels.
- [ ] Outliers are color-coded **and** annotated.
- [ ] No legend bigger than the data it explains.
- [ ] Share copy provided in a fenced code block (3-5 bullets for simple, 2-3 line summary for detailed).

## Anti-patterns

- Pasting raw query output as a table when the user asked for a chart.
- 3D effects, gradients, and drop shadows.
- Twin axes (line over bars on a secondary y-axis). Stack two panels instead.
- Heatmaps with more than 40 cells.
- One color per data point. Reserve color for meaning.
- Default matplotlib style. Always call `apply_style()` first.
- KPI cards in simple mode (defeats the point of "simple").

## Reference files (always present alongside this SKILL.md)

- `style.py` - palette + helpers. Read first.
- `example_simple.py` - minimal worked example (single time-series with summary number).
- `example_detailed.py` - full worked example (KPI cards + 3 panels, generic product metrics).

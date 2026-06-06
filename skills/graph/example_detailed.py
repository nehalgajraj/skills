"""Detailed-mode example - KPI cards + 3 stacked panels.

Use this template when the user wants a shareable or leadership-update
dashboard. Adapt the data, callouts, and panel choices to the specific metrics.
Output: 12x14 in PNG.

This example uses generic product usage metrics. Replace the sample data with
the user's actual data before rendering.
"""
import sys
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

SKILL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SKILL_DIR))
from style import (  # noqa: E402
    apply_style, BLUE, ORANGE, GREEN, RED, GREY, DARK,
    title_block, kpi_card, bar_with_labels, smoothed_timeseries,
    retention_curve, save_chart,
)

# ---- Data ---------------------------------------------------------------
weekly_actions = [
    ("2026-02-02", 21857), ("2026-02-09", 26401), ("2026-02-16", 27169),
    ("2026-02-23", 29548), ("2026-03-02", 33002), ("2026-03-09", 35528),
    ("2026-03-16", 33599), ("2026-03-23", 34069), ("2026-03-30", 32690),
    ("2026-04-06", 34888), ("2026-04-13", 40741),
    ("2026-04-20", 20649),  # outlier (regression)
    ("2026-04-27", 49570),  # rebound
]

dau = [
    ("2026-02-03", 3204), ("2026-02-04", 3190), ("2026-02-05", 2951),
    ("2026-02-06", 2957), ("2026-02-07", 1372), ("2026-02-08", 1441),
    # ... abbreviated; in real use, paste the full series ...
    ("2026-04-27", 4566), ("2026-04-28", 4785), ("2026-04-29", 4570),
    ("2026-04-30", 4614), ("2026-05-01", 3580),
]

retention_pct = {0: 100, 1: 24, 2: 19, 3: 17, 4: 15, 6: 12, 8: 12}

# ---- Layout -------------------------------------------------------------
apply_style()
fig = plt.figure(figsize=(12, 14), facecolor="white")
gs = fig.add_gridspec(
    5, 3, hspace=0.55, wspace=0.25,
    height_ratios=[0.35, 0.7, 1.6, 1.4, 1.4],
)

# Title
title_block(
    fig.add_subplot(gs[0, :]),
    "Product Usage - Last 90 Days",
    "Feb 02, 2026 to May 03, 2026 - Source: analytics export",
)

# KPIs
kpi_card(fig.add_subplot(gs[1, 0]), "WEEKLY ACTIONS", "49.6K",
         "avg WoW growth: +8.7%", color=BLUE)
kpi_card(fig.add_subplot(gs[1, 1]), "DAILY ACTIVE USERS", "4,566",
         "+22% vs. start of window", color=ORANGE)
kpi_card(fig.add_subplot(gs[1, 2]), "WEEK-4 RETENTION", "15%",
         "plateaus near 12% by W8", color=GREEN)

# Panel 1: weekly actions
labels = [datetime.strptime(w, "%Y-%m-%d").strftime("%b %d") for w, _ in weekly_actions]
values = [v for _, v in weekly_actions]
deltas = [None] + [(values[i] - values[i - 1]) / values[i - 1] * 100
                   for i in range(1, len(values))]
bar_with_labels(
    fig.add_subplot(gs[2, :]),
    labels, values,
    title="Actions completed per week",
    ylabel="Actions / week",
    fmt=lambda v: f"{v/1000:.1f}K",
    deltas=deltas,
    outliers={11: "RED", 12: "GREEN"},
    color=BLUE,
)

# Panel 2: DAU
ax2 = fig.add_subplot(gs[3, :])
dates = [datetime.strptime(d, "%Y-%m-%d") for d, _ in dau]
vals = [v for _, v in dau]
smoothed_timeseries(
    ax2, dates, vals,
    title="Daily active CLI users",
    ylabel="Users (7-day avg)",
    color=ORANGE,
    references=[
        (3000, "start: 3,000", "GREY"),
        (4500, "recent: 4,500", "GREEN"),
    ],
)

# Panel 3: retention
retention_curve(
    fig.add_subplot(gs[4, :]),
    retention_pct,
    title="Average retention curve  (% of new users still active N weeks later)",
    callout="After the first month,\nretention plateaus near 12%\n- stable long-tail usage.",
)

OUTPUT = "/tmp/product_metrics_detailed.png"
save_chart(OUTPUT)
print(f"saved: {OUTPUT}")

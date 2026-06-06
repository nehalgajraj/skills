"""Shared plotting helpers for the /graph skill.

Import these instead of styling each chart by hand. Keeps the visual
language consistent across simple and detailed modes.
"""
from __future__ import annotations

from datetime import datetime
from typing import Iterable, Sequence

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import FancyBboxPatch

# ---------------------------------------------------------------- palette --

PALETTE = {
    "BLUE":   "#2E5BFF",
    "ORANGE": "#FF8B3D",
    "GREEN":  "#22C55E",
    "RED":    "#EF4444",
    "GREY":   "#94A3B8",
    "DARK":   "#1E293B",
}

BLUE   = PALETTE["BLUE"]
ORANGE = PALETTE["ORANGE"]
GREEN  = PALETTE["GREEN"]
RED    = PALETTE["RED"]
GREY   = PALETTE["GREY"]
DARK   = PALETTE["DARK"]


# ------------------------------------------------------------- base style --

def apply_style() -> None:
    """Set global matplotlib rcParams. Call once after `import matplotlib.pyplot`."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": "#999",
        "axes.labelcolor": "#333",
        "xtick.color": "#555",
        "ytick.color": "#555",
        "axes.grid": False,
    })


# ---------------------------------------------------------- title + KPIs --

def title_block(
    ax: Axes, title: str, subtitle: str | None = None, *, big: bool = True,
) -> None:
    """Render the top title strip. `ax` should be a no-axis subplot above the chart panels."""
    ax.axis("off")
    ax.text(
        0.0, 0.7 if subtitle else 0.45, title,
        fontsize=26 if big else 22, fontweight="bold", color=DARK,
        transform=ax.transAxes,
    )
    if subtitle:
        ax.text(
            0.0, 0.15, subtitle,
            fontsize=12, color=GREY, transform=ax.transAxes,
        )


def kpi_card(
    ax: Axes, label: str, value: str, sub: str = "", *, color: str = BLUE,
) -> None:
    """Render a tinted KPI card on a no-axis subplot."""
    ax.axis("off")
    card = FancyBboxPatch(
        (0.02, 0.05), 0.96, 0.9,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        linewidth=0, facecolor=color, alpha=0.08,
        transform=ax.transAxes,
    )
    ax.add_patch(card)
    ax.text(
        0.06, 0.78, label, fontsize=12, color=GREY, fontweight="bold",
        transform=ax.transAxes,
    )
    ax.text(
        0.06, 0.40, value, fontsize=30, color=color, fontweight="bold",
        transform=ax.transAxes,
    )
    if sub:
        ax.text(
            0.06, 0.13, sub, fontsize=10, color="#666",
            transform=ax.transAxes,
        )


# ---------------------------------------------------------- chart panels --

def bar_with_labels(
    ax: Axes,
    labels: Sequence[str],
    values: Sequence[float],
    *,
    title: str,
    ylabel: str = "",
    fmt = "{:.0f}",
    deltas: Sequence[float | None] | None = None,
    outliers: dict[int, str] | None = None,
    color: str = BLUE,
) -> None:
    """Bar chart with value labels above each bar.

    - `fmt`: either a format string (`"{:.1f}K"`) or a callable
      (`lambda v: f"{v/1000:.1f}K"`) for the value label.
    - `deltas`: optional sequence (same length as values) of WoW % changes,
      shown in small text above the value label. Use None to skip a bar.
    - `outliers`: {index: color_name} to recolor specific bars
      (e.g. {11: 'RED', 12: 'GREEN'}).
    """
    label_fn = fmt if callable(fmt) else fmt.format
    bars = ax.bar(
        range(len(values)), values, color=color,
        edgecolor="white", linewidth=1.5, width=0.7,
    )
    if outliers:
        for idx, name in outliers.items():
            bars[idx].set_color(PALETTE.get(name, name))

    ax.set_title(title, fontsize=16, fontweight="bold", color=DARK,
                 loc="left", pad=14)
    ax.set_xticks(range(len(values)))
    ax.set_xticklabels(labels, fontsize=10)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11)
    ymax = max(values) * 1.20
    ax.set_ylim(0, ymax)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)

    for i, (b, v) in enumerate(zip(bars, values)):
        ax.text(
            b.get_x() + b.get_width() / 2, v + ymax * 0.012,
            label_fn(v), ha="center", fontsize=10, fontweight="bold",
            color=DARK,
        )
        if deltas and deltas[i] is not None and (not outliers or i not in outliers):
            ax.text(
                b.get_x() + b.get_width() / 2, v + ymax * 0.055,
                f"{deltas[i]:+.0f}%",
                ha="center", fontsize=8.5,
                color=GREEN if deltas[i] > 0 else RED,
                fontweight="bold",
            )


def smoothed_timeseries(
    ax: Axes,
    dates: Sequence[datetime],
    values: Sequence[float],
    *,
    title: str,
    ylabel: str = "",
    color: str = ORANGE,
    smoothing: int = 7,
    show_raw: bool = False,
    references: Sequence[tuple[float, str, str]] = (),
) -> None:
    """Time-series with rolling average and optional reference lines.

    `references`: list of (y_value, label, color_name) - drawn as horizontal
    dashed lines with a text annotation on the right side.
    """
    half = smoothing // 2
    smooth = []
    for i in range(len(values)):
        lo = max(0, i - half)
        hi = min(len(values), i + half + 1)
        smooth.append(sum(values[lo:hi]) / (hi - lo))

    ax.fill_between(dates, smooth, color=color, alpha=0.18)
    if show_raw:
        ax.plot(dates, values, color=color, linewidth=1, alpha=0.4)
    ax.plot(dates, smooth, color=color, linewidth=3,
            label=f"{smoothing}-day rolling avg")

    ax.set_title(title, fontsize=16, fontweight="bold", color=DARK,
                 loc="left", pad=14)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11)
    ax.set_ylim(0, max(smooth) * 1.25)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=8))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)

    for y, label, color_name in references:
        c = PALETTE.get(color_name, color_name)
        ax.axhline(y, color=c, linestyle="--", linewidth=1, alpha=0.7)
        ax.text(
            dates[int(len(dates) * 0.92)], y * 1.05, label,
            fontsize=10, color=c, fontweight="bold", ha="right",
        )


def retention_curve(
    ax: Axes,
    points: dict[int, float],
    *,
    title: str = "Retention curve",
    callout: str | None = None,
    color: str = GREEN,
) -> None:
    """Single retention curve with point labels.

    `points`: {week_offset: pct_retained}.
    `callout`: optional plain-English explanation rendered as a tinted box.
    """
    xs = sorted(points.keys())
    ys = [points[x] for x in xs]
    ax.plot(
        xs, ys, "o-", color=color, linewidth=3, markersize=10,
        markerfacecolor="white", markeredgewidth=2.5, markeredgecolor=color,
    )
    ax.fill_between(xs, ys, alpha=0.12, color=color)

    for x, y in zip(xs, ys):
        ax.text(x, y + 4, f"{y:.0f}%", ha="center", fontsize=11,
                fontweight="bold", color=DARK)

    ax.set_title(title, fontsize=16, fontweight="bold", color=DARK,
                 loc="left", pad=14)
    ax.set_xlabel("Weeks since first seen", fontsize=11)
    ax.set_ylabel("% retained", fontsize=11)
    ax.set_ylim(0, max(ys) * 1.15)
    ax.set_xticks(xs)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.set_axisbelow(True)

    if callout:
        ax.text(
            xs[len(xs) // 2] + 0.3, max(ys) * 0.7, callout,
            fontsize=10.5, color=DARK, ha="left",
            bbox=dict(boxstyle="round,pad=0.6", fc=color, alpha=0.10, ec=color),
        )


# ---------------------------------------------------------------- output --

def save_chart(out_path: str) -> str:
    """Save the current figure with share-friendly image conventions."""
    plt.savefig(
        out_path, dpi=150, bbox_inches="tight",
        facecolor="white", pad_inches=0.4,
    )
    return out_path

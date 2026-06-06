"""Simple-mode example - one chart, one number, no clutter.

Use this template when the user wants a quick visual, not a leadership deck.

Output: 12x6 in PNG, single panel + headline number in the title.
"""
import sys
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

# Importing from the skill directory:
SKILL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SKILL_DIR))
from style import (  # noqa: E402
    apply_style, BLUE, ORANGE, GREEN, RED, GREY, DARK,
    smoothed_timeseries, save_chart,
)

# ---- Replace with the user's data ---------------------------------------
# Example: weekday active users for the last 60 days
data = [
    ("2026-03-09", 3695), ("2026-03-10", 3865), ("2026-03-11", 4102),
    ("2026-03-12", 4182), ("2026-03-13", 3779), ("2026-03-16", 4046),
    ("2026-03-17", 4354), ("2026-03-18", 4320), ("2026-03-19", 4062),
    ("2026-03-20", 3626), ("2026-03-23", 3868), ("2026-03-24", 4209),
    ("2026-03-25", 4397), ("2026-03-26", 4195), ("2026-03-27", 3816),
    ("2026-03-30", 3865), ("2026-03-31", 4171), ("2026-04-01", 4211),
    ("2026-04-02", 4373), ("2026-04-03", 3269), ("2026-04-06", 3306),
    ("2026-04-07", 4105), ("2026-04-08", 4131), ("2026-04-09", 4983),
    ("2026-04-10", 4310), ("2026-04-13", 4339), ("2026-04-14", 4563),
    ("2026-04-15", 4696), ("2026-04-16", 4947), ("2026-04-17", 4586),
    ("2026-04-23", 3664), ("2026-04-24", 4186), ("2026-04-27", 4566),
    ("2026-04-28", 4785), ("2026-04-29", 4570), ("2026-04-30", 4614),
    ("2026-05-01", 3580),
]

TITLE = "Weekday active users - 60 days"
HEADLINE = "+22% growth"
OUTPUT = "/tmp/active_users_simple.png"

# ---- Render -------------------------------------------------------------
apply_style()
fig, ax = plt.subplots(figsize=(12, 6), facecolor="white")

dates = [datetime.strptime(d, "%Y-%m-%d") for d, _ in data]
values = [v for _, v in data]

smoothed_timeseries(
    ax, dates, values,
    title=f"{TITLE}    {HEADLINE}",
    ylabel="DAU",
    color=BLUE,
)

save_chart(OUTPUT)
print(f"saved: {OUTPUT}")

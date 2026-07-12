# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib"]
# ///
"""Generate SVG charts for the Dobbs London Marathon 2027 training plan.

Run from the repo root:  uv run scripts/generate_plan_charts.py
Writes to assets/img/ and prints per-phase totals used in the plan tables.
"""

from datetime import date, timedelta
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerPatch
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT = Path(__file__).resolve().parent.parent / "assets" / "img"

START = date(2026, 9, 14)  # Monday of week 1
RACE = date(2027, 4, 25)  # Sunday of week 32

# Weekly running volume (km), weeks 1-32. Cutback weeks every ~4th week;
# week 15 cutback lands on Christmas; week 24 mini-taper into the tune-up
# half; week 32 is pre-race running only (race 42.2 km shown separately).
WEEKLY_KM = [
    15, 17, 19, 15, 21, 23, 25, 19,        # P1 base rebuild
    27, 29, 31, 24, 32, 34, 26, 35,        # P2 aerobic build
    37, 39, 41, 31, 43, 45, 47, 35,        # P3 marathon build
    44, 47, 50, 42, 49,                    # P4 peak
    38, 28, 16,                            # P5 taper (wk 32 excl. race)
]

# Sunday long run (km), weeks 1-32. Week 24 long run is the tune-up half
# race; week 32's "long run" is the marathon itself.
LONG_RUN = [
    6, 7, 8, 6, 9, 10, 11, 8,
    12, 13, 15, 10, 16, 17, 12, 18,
    19, 20, 21.1, 16, 24, 26, 28, 21.1,
    24, 27, 30, 22, 32,
    20, 14, 42.2,
]

PHASES = [
    ("Base rebuild", 1, 8, "#2a78d6"),
    ("Aerobic build", 9, 16, "#1baf7a"),
    ("Marathon build", 17, 24, "#eda100"),
    ("Peak", 25, 29, "#008300"),
    ("Taper", 30, 32, "#4a3aa7"),
]

INK = "#16161a"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
SURFACE = "#ffffff"

mpl.rcParams.update({
    "svg.fonttype": "none",
    "font.family": ["Helvetica Neue", "Arial", "sans-serif"],
    "font.size": 10,
    "text.color": INK,
    "axes.edgecolor": BASELINE,
    "axes.labelcolor": MUTED,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
})

assert len(WEEKLY_KM) == 32 and len(LONG_RUN) == 32


def week_color(week: int) -> str:
    for _, lo, hi, hex_ in PHASES:
        if lo <= week <= hi:
            return hex_
    raise ValueError(week)


def monday(week: int) -> date:
    return START + timedelta(weeks=week - 1)


def style_axes(ax):
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_linewidth(1)
    ax.yaxis.grid(True, color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


def month_ticks(ax):
    ticks = range(1, 33, 4)
    ax.set_xticks(list(ticks))
    ax.set_xticklabels([monday(w).strftime("%-d %b") for w in ticks])


def chart_weekly_volume():
    fig, ax = plt.subplots(figsize=(8.6, 4.1))
    style_axes(ax)

    for wk, km in enumerate(WEEKLY_KM, start=1):
        # 4px-radius rounded data-end, square at the baseline: round the top
        # of a slightly shortened box and square-fill the base underneath.
        c = week_color(wk)
        r = 0.9  # km of rounding ~ 4px at this scale
        ax.add_patch(FancyBboxPatch(
            (wk - 0.38, 0), 0.76, km,
            boxstyle=f"round,pad=0,rounding_size={r}",
            mutation_aspect=0.76 / (2 * r),
            facecolor=c, edgecolor="none",
        ))
        ax.add_patch(Rectangle((wk - 0.38, 0), 0.76, km / 2,
                               facecolor=c, edgecolor="none"))

    peak_wk = WEEKLY_KM.index(max(WEEKLY_KM)) + 1
    ax.annotate(f"peak {max(WEEKLY_KM)} km", (peak_wk, max(WEEKLY_KM)),
                xytext=(0, 6), textcoords="offset points",
                ha="center", fontsize=9, color=INK)
    ax.annotate("race week\n+ 42.2 km", (32, WEEKLY_KM[31]),
                xytext=(0, 6), textcoords="offset points",
                ha="center", fontsize=9, color=MUTED)

    handles = [
        Rectangle((0, 0), 1, 1, facecolor=hex_, edgecolor="none")
        for _, _, _, hex_ in PHASES
    ]
    ax.legend(
        handles, [name for name, *_ in PHASES],
        handler_map={Rectangle: HandlerPatch()},
        loc="upper left", frameon=False, fontsize=9,
        handlelength=1.0, handleheight=1.0, labelcolor=INK,
        ncols=3, columnspacing=1.2,
    )

    ax.set_xlim(0.3, 32.7)
    ax.set_ylim(0, 62)
    ax.set_yticks(range(0, 61, 10))
    month_ticks(ax)
    ax.set_ylabel("km per week")
    fig.tight_layout()
    fig.savefig(OUT / "dobbs-plan-weekly-volume.svg")
    plt.close(fig)


def chart_long_run():
    fig, ax = plt.subplots(figsize=(8.6, 4.1))
    style_axes(ax)

    weeks = list(range(1, 33))
    ax.plot(weeks[:-1], LONG_RUN[:-1], color="#2a78d6", linewidth=2,
            solid_joinstyle="round", solid_capstyle="round", zorder=3)

    milestones = [
        (6, "first 10 km", (-2, 10)),
        (11, "first 15 km", (-4, 10)),
        (19, "half distance", (-14, 10)),
        (24, "tune-up half race", (8, -14)),
        (29, "longest run 32 km", (-40, 12)),
        (32, "race day 42.2 km", (-84, -4)),
    ]
    for wk, label, (dx, dy) in milestones:
        ax.plot(wk, LONG_RUN[wk - 1], "o", markersize=8,
                markerfacecolor="#2a78d6", markeredgecolor=SURFACE,
                markeredgewidth=2, zorder=4)
        ax.annotate(label, (wk, LONG_RUN[wk - 1]),
                    xytext=(dx, dy), textcoords="offset points",
                    fontsize=9, color=INK, zorder=5)

    ax.axhline(21.1, color=GRID, linewidth=1, zorder=1)
    ax.text(0.6, 21.7, "half marathon", fontsize=8.5, color=MUTED)

    ax.set_xlim(0.3, 33.6)
    ax.set_ylim(0, 47)
    ax.set_yticks(range(0, 41, 10))
    month_ticks(ax)
    ax.set_ylabel("Sunday long run, km")
    fig.tight_layout()
    fig.savefig(OUT / "dobbs-plan-long-run.svg")
    plt.close(fig)


def print_phase_summary():
    print(f"{'phase':<16} {'weeks':<7} {'km/wk':<9} {'run h/wk':<10} longest run")
    for name, lo, hi, _ in PHASES:
        kms = WEEKLY_KM[lo - 1:hi]
        lrs = LONG_RUN[lo - 1:hi]
        # ~7:10/km average easy pace -> hours
        h = [k * 7.17 / 60 for k in kms]
        print(f"{name:<16} {lo}-{hi:<5} {min(kms)}-{max(kms):<6} "
              f"{min(h):.1f}-{max(h):<7.1f} {max(lrs)} km")
    print(f"total training km (excl. race): {sum(WEEKLY_KM)}")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    chart_weekly_volume()
    chart_long_run()
    print_phase_summary()
    print(f"charts written to {OUT}")

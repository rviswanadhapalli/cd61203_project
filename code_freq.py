
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

dates = []
additions = []
deletions = []

with open("code_frequency.csv", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)

    # Clean column names
    reader.fieldnames = [name.strip() for name in reader.fieldnames]

    for row in reader:
        dates.append(
            datetime.strptime(row["DateTime"].strip(), "%Y-%m-%d")
        )
        additions.append(int(row["Additions"]))
        deletions.append(int(row["Deletions"]))

fig, ax = plt.subplots(figsize=(12, 5))

# Green bars: additions
ax.bar(
    dates, additions,
    width=8,
    color="#2da44e",
    label="Additions",
    linewidth=0
)

# Red bars: deletions (already negative in CSV)
ax.bar(
    dates, deletions,
    width=8,
    color="#cf222e",
    label="Deletions",
    linewidth=0
)

# Right-side Y-axis
ax.yaxis.tick_right()
ax.yaxis.set_label_position("right")
ax.set_ylabel("Frequency", rotation=270, labelpad=18)

ax.set_title(
    "Code frequency",
    loc="left",
    fontweight="bold",
    pad=18
)

# X-axis: six-month intervals
ax.xaxis.set_major_locator(
    mdates.MonthLocator(bymonth=[1, 7])
)
ax.xaxis.set_major_formatter(
    mdates.DateFormatter("%b %Y")
)

# Grid styling
ax.grid(
    axis="both",
    linestyle="--",
    color="#d0d7de",
    linewidth=0.7
)
ax.set_axisbelow(True)

# Zero baseline
ax.axhline(0, color="#d0d7de", linewidth=0.8)

# Axis limits and appearance
ax.spines["top"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_color("#d0d7de")

ax.tick_params(
    axis="both",
    colors="#57606a",
    length=0,
    pad=10
)

# Legend on the right
ax.legend(
    loc="center left",
    bbox_to_anchor=(1.08, 0.5),
    frameon=False
)

plt.tight_layout()
plt.savefig("code_frequency.png", dpi=150, bbox_inches="tight")
plt.show()


import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from datetime import datetime

dates = []
additions = []
deletions = []

# Read CSV
with open("code_frequency.csv", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    reader.fieldnames = [name.strip() for name in reader.fieldnames]

    for row in reader:
        dates.append(
            datetime.strptime(row["DateTime"].strip(), "%Y-%m-%d")
        )
        additions.append(int(row["Additions"]))
        deletions.append(int(row["Deletions"]))

# Aggregate every two consecutive weeks
# Aggregate every three consecutive weeks
grouped_dates = []
grouped_additions = []
grouped_deletions = []

for i in range(0, len(dates), 3):
    grouped_dates.append(dates[i])
    grouped_additions.append(sum(additions[i:i+3]))
    grouped_deletions.append(sum(deletions[i:i+3]))


# Create figure
fig, ax = plt.subplots(figsize=(9, 5))

# Plot additions and deletions
ax.bar(
    grouped_dates,
    grouped_additions,
    width=13,
    color="#2da44e",
    label="Additions",
    linewidth=0
)

ax.bar(
    grouped_dates,
    grouped_deletions,
    width=13,
    color="#cf222e",
    label="Deletions",
    linewidth=0
)

# X-axis
ax.set_xlim(dates[0], dates[-1])

ax.xaxis.set_major_locator(
    mdates.MonthLocator(bymonth=[1, 7])
)
ax.xaxis.set_major_formatter(
    mdates.DateFormatter("%b %Y")
)

# Y-axis
ax.set_ylim(-40000, 80000)
ax.set_yticks([-40000, -20000, 0, 20000, 40000, 60000])

ax.yaxis.set_major_formatter(
    FuncFormatter(
        lambda x, _: "0" if x == 0 else f"{int(x/1000)}k"
    )
)

ax.yaxis.tick_right()
ax.yaxis.set_label_position("right")
ax.set_ylabel("Frequency", rotation=270, labelpad=16)

# Title
ax.set_title(
    "Code frequency",
    loc="left",
    fontweight="bold",
    fontsize=12,
    pad=18
)

ax.text(
    0, 1.055,
    "Additions and deletions per week",
    transform=ax.transAxes,
    fontsize=8.5,
    color="#57606a"
)

# Grid
ax.grid(
    axis="both",
    linestyle=(0, (3, 3)),
    color="#d0d7de",
    linewidth=0.7
)

ax.set_axisbelow(True)
ax.axhline(0, color="#d0d7de", linewidth=0.8)

# Spines
ax.spines["top"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_color("#d0d7de")

# Ticks
ax.tick_params(
    axis="both",
    colors="#57606a",
    length=0,
    pad=9
)

# Legend
ax.legend(
    loc="center left",
    bbox_to_anchor=(1.08, 0.5),
    frameon=False
)

plt.tight_layout()
plt.savefig("code_frequency.png", dpi=150, bbox_inches="tight")
plt.show()

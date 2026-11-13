
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

dates = []
commits = []

with open("contributors.csv", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)

    # Clean column names
    reader.fieldnames = [name.strip() for name in reader.fieldnames]

    for row in reader:
        dates.append(
            datetime.strptime(row["Week of"].strip(), "%Y-%m-%d")
        )
        commits.append(int(row["Commits"]))

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(dates, commits, color="#2da44e", linewidth=1.8)

ax.set_title("Contributions over time", loc="left",
             fontweight="bold", pad=18)
ax.set_ylabel("Commits")

ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

ax.grid(axis="y", linestyle="--", color="#d0d7de", linewidth=0.7)
ax.set_axisbelow(True)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_color("#d0d7de")

ax.tick_params(axis="both", colors="#57606a", length=0, pad=10)

plt.tight_layout()
plt.savefig("contributors.png", dpi=150)
plt.show()

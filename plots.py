import json, datetime as dt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

REPO = "huggingface/huggingface.js"
GREEN, RED, BLUE = "#2da44e", "#cf222e", "#0969da"
d = lambda t: dt.datetime.fromtimestamp(t, dt.UTC).date()
kfmt = FuncFormatter(lambda v, _: f"{v/1000:g}k" if abs(v) >= 1000 else f"{v:g}")

co = json.load(open("cd.json"))          # contributors-data
ca = json.load(open("cm.json"))          # commit-activity-data
cf = json.load(open("cfq.json"))         # code-frequency-data
co.sort(key=lambda a: -a["total"])
weeks = [d(w["w"]) for w in co[0]["weeks"]]

def style(ax):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#d0d7de", lw=0.6); ax.set_axisbelow(True)

# ---------- 1. Contributors ----------
tot = [sum(a["weeks"][i]["c"] for a in co) for i in range(len(weeks))]
ncol = 5; n = len(co); nrow = -(-n // ncol)
fig = plt.figure(figsize=(8.0, 10.4))
gs = fig.add_gridspec(nrow + 4, ncol, hspace=0.9, wspace=0.35, left=0.05, right=0.98, top=0.975, bottom=0.02)
ax = fig.add_subplot(gs[:3, :])
ax.fill_between(weeks, tot, color=GREEN, alpha=0.9, lw=0); ax.plot(weeks, tot, color=GREEN, lw=1)
ax.set_title(f"Commits to main, excluding merge commits — {REPO} (top {n} contributors)", fontsize=9, loc="left")
ax.set_ylabel("Commits per week", fontsize=8); ax.set_xlabel("Week", fontsize=8)
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7))); ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.tick_params(labelsize=7); ax.set_xlim(weeks[0], weeks[-1]); ax.set_ylim(bottom=0); style(ax)
for i, a in enumerate(co):
    r, c = divmod(i, ncol)
    s = fig.add_subplot(gs[4 + r, c])
    y = [w["c"] for w in a["weeks"]]
    s.fill_between(weeks, y, color=GREEN, lw=0); s.plot(weeks, y, color=GREEN, lw=0.5)
    s.set_xlim(weeks[0], weeks[-1]); s.set_ylim(bottom=0)
    s.set_title(f"#{i+1} {a['author']['login']} ({a['total']})", fontsize=5.5, loc="left", pad=2)
    s.tick_params(labelsize=4, length=2, pad=1)
    s.xaxis.set_major_locator(mdates.YearLocator()); s.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    for sp in ("top", "right"): s.spines[sp].set_visible(False)
    for sp in s.spines.values(): sp.set_linewidth(0.4)
fig.savefig("out/contributors.pdf"); fig.savefig("out/contributors.png", dpi=200); plt.close(fig)

# ---------- 2. Commits (last 52 weeks) ----------
x = [d(w["week"]) for w in ca]; y = [w["total"] for w in ca]
fig, ax = plt.subplots(figsize=(7.5, 3.4))
ax.bar(x, y, width=5.6, color=GREEN, align="edge")
ax.set_xlabel("Week"); ax.set_ylabel("Commits")
ax.set_title(f"Commits per week over the last year — {REPO}", fontsize=10, loc="left")
ax.xaxis.set_major_locator(mdates.MonthLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.set_xlim(x[0] - dt.timedelta(days=3), x[-1] + dt.timedelta(days=10)); style(ax)
fig.tight_layout(); fig.savefig("out/commits.pdf"); fig.savefig("out/commits.png", dpi=200); plt.close(fig)

# ---------- 3. Code frequency ----------
x = [d(r[0]) for r in cf]; add = [r[1] for r in cf]; dele = [r[2] for r in cf]
fig, ax = plt.subplots(figsize=(7.5, 3.6))
ax.fill_between(x, add, color=GREEN, lw=0, label="Additions"); ax.plot(x, add, color=GREEN, lw=0.8)
ax.fill_between(x, dele, color=RED, lw=0, label="Deletions"); ax.plot(x, dele, color=RED, lw=0.8)
ax.axhline(0, color="#57606a", lw=0.6)
ax.set_xlabel("Week"); ax.set_ylabel("Lines changed per week")
ax.set_title(f"Code frequency (weekly additions and deletions) — {REPO}", fontsize=10, loc="left")
ax.yaxis.set_major_formatter(kfmt); ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y")); ax.set_xlim(x[0], x[-1]); ax.legend(frameon=False, loc="upper left")
style(ax); fig.tight_layout(); fig.savefig("out/code_frequency.pdf"); fig.savefig("out/code_frequency.png", dpi=200); plt.close(fig)

# ---------- 4. Top committers ----------
names = [a["author"]["login"] for a in co]; vals = [a["total"] for a in co]
fig, ax = plt.subplots(figsize=(7.0, 9.4))
ypos = range(len(names))
ax.barh(ypos, vals, color=BLUE, height=0.75)
ax.set_yticks(list(ypos)); ax.set_yticklabels(names, fontsize=5.5); ax.invert_yaxis()
for i, v in enumerate(vals): ax.text(v + 6, i, str(v), va="center", fontsize=5)
ax.set_xlabel("Commits"); ax.set_ylabel("Author")
ax.set_title(f"Top committers (commits per author, top {len(names)}) — {REPO}", fontsize=10, loc="left")
ax.set_ylim(len(names) - 0.4, -0.6); ax.tick_params(axis="y", length=0)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.grid(axis="x", color="#d0d7de", lw=0.6); ax.set_axisbelow(True)
fig.tight_layout(); fig.savefig("out/top_committers.pdf"); fig.savefig("out/top_committers.png", dpi=200); plt.close(fig)
print("done", sum(vals), sum(y for y in [w['total'] for w in ca]))
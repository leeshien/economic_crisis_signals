import sys, io, contextlib, runpy
import pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
S = sys.argv[1]
sys.argv = ["x", S]
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(f"{S}/validate_all_2022.py")
sigs = {**g["CORE"], **g["CANDIDATES"]}
rows = [k for k in sigs if "from 19" not in k and k != "NFCI >0"]
crises = list(g["CRISES"])
fig, ax = plt.subplots(figsize=(13, 0.42 * len(rows) + 1.8), dpi=110)
core = set(g["CORE"])
for i, r in enumerate(rows):
    for j, c in enumerate(crises):
        p, b = g["CRISES"][c]
        v = g["score"](sigs[r], pd.Timestamp(p), pd.Timestamp(b))
        if v.isdigit(): col, txt, tc = "#dc2626", f"{v} mo", "white"
        elif v.startswith("C"): col, txt, tc = "#fca5a5", "long on", "#7f1d1d"
        elif v.startswith("late"): col, txt, tc = "#d1d5db", v.replace("late", "late "), "#374151"
        else: col, txt, tc = "#f3f4f6", "", "#000"
        ax.add_patch(plt.Rectangle((j + 0.04, i + 0.08), 0.92, 0.84, color=col))
        ax.text(j + 0.5, i + 0.5, txt, ha="center", va="center", fontsize=8.5, color=tc, fontweight="bold")
    base = 100 * sigs[r].dropna().astype(bool).loc["1972":"2019"].mean()
    ax.text(len(crises) + 0.15, i + 0.5, f"{base:.0f}%", va="center", fontsize=9, color="#374151")
ax.set_xlim(0, len(crises) + 0.8); ax.set_ylim(len(rows), -0.6)
ax.set_xticks([j + 0.5 for j in range(len(crises))] + [len(crises) + 0.35])
ax.set_xticklabels([f"{c}\npeak" for c in crises] + ["false\nalarm"], fontsize=9)
ax.xaxis.tick_top()
ax.set_yticks([i + 0.5 for i in range(len(rows))])
ax.set_yticklabels([("★ " if r in core else "   ") + r.lstrip("12345678 ") for r in rows], fontsize=9)
ax.axhline(len(core), color="#111827", lw=1.2)
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0)
fig.suptitle("Validated scoreboard: which signals warned before each S&P 500 peak? (FRED + Shiller data)", x=0.01, ha="left", fontsize=12, fontweight="bold")
fig.text(0.01, 0.005, "Red = switched on 1-24 months before peak (number = months early). Pink = already on for years. Grey = fired only after the peak. "
         "★ = current core-8. 'false alarm' = % of months ON 1972-2019. 2022 cells partly distorted by 2020 Covid after-effects.", fontsize=8, color="#4b5563", wrap=True)
fig.tight_layout(rect=(0, 0.03, 1, 0.97)); fig.savefig(f"{S}/validation-scoreboard.png")

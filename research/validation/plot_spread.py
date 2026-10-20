import sys
from pathlib import Path
import pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
D = Path(sys.argv[1])
def load(sid):
    df = pd.read_csv(D / f"{sid}.csv"); df.columns = ["date", sid]
    s = pd.to_numeric(df[sid], errors="coerce"); s.index = pd.to_datetime(df["date"])
    return s.dropna().resample("MS").mean()
spread = (load("BAA") - load("GS10")).loc["1970":]
on = (spread - spread.rolling(24).min()) >= 0.5
peaks = {"1973": "1973-01", "1980": "1980-11", "1990": "1990-07", "2000": "2000-03", "2007": "2007-10", "2020": "2020-02"}
fig, ax = plt.subplots(figsize=(14, 5), dpi=110)
ax.fill_between(spread.index, 0, spread.max() * 1.05, where=on.reindex(spread.index).fillna(False), color="#fecaca", step="mid", label="Rule ON (spread ≥0.5 pt above 24-mo low)")
ax.plot(spread.index, spread, color="#1d4ed8", lw=1.6, label="Baa corporate yield − 10Y Treasury (pts)")
for k, d in peaks.items():
    x = pd.Timestamp(d); ax.axvline(x, color="#111827", ls="--", lw=1)
    ax.text(x, spread.max() * 1.0, f" {k} peak", fontsize=9, va="top")
ax.set_ylim(0, spread.max() * 1.05); ax.set_xlim(spread.index[0], spread.index[-1])
ax.set_title("Corporate credit spread vs. S&P 500 peaks (FRED BAA − GS10, monthly)", loc="left", fontsize=13, fontweight="bold")
ax.legend(loc="upper left", frameon=False, fontsize=9); ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig(sys.argv[2])

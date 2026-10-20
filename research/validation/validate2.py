# Stricter scoring: a warning must switch ON inside the 24-mo window and be ON within 12 mo of the peak.
import sys
from pathlib import Path
import pandas as pd
D = Path(sys.argv[1])
def load(sid):
    df = pd.read_csv(D / f"{sid}.csv"); df.columns = ["date", sid]
    s = pd.to_numeric(df[sid], errors="coerce"); s.index = pd.to_datetime(df["date"])
    return s.dropna().resample("MS").mean()
baa, gs10 = load("BAA"), load("GS10")
spread = baa - gs10
CRISES = {"1973": ("1973-01-01","1974-10-01"), "1980": ("1980-11-01","1982-08-01"), "1990": ("1990-07-01","1990-10-01"),
          "2000": ("2000-03-01","2002-10-01"), "2008": ("2007-10-01","2009-03-01"), "2020": ("2020-02-01","2020-03-01")}
def m(a,b): return (b.year-a.year)*12+(b.month-a.month)
def score(sig, peak, bottom):
    sig = sig.dropna()
    w0 = peak - pd.DateOffset(months=24)
    win = sig.loc[w0:peak]
    starts = win & ~sig.shift(1).reindex(win.index).fillna(False).astype(bool)
    recent = sig.loc[peak - pd.DateOffset(months=12):peak]
    if starts.any() and recent.any():
        st = starts[starts].index[0]
        return f"{m(st,peak):>2} mo early"
    after = sig.loc[peak + pd.DateOffset(months=1):bottom]
    if after.any(): return f"late +{m(peak, after[after].index[0])}"
    return "  -"
for thr in (0.5, 0.75, 1.0):
    sig = (spread - spread.rolling(24).min()) >= thr
    base = 100 * sig.loc["1972":"2019"].dropna().mean()
    row = "  ".join(f"{k}: {score(sig, pd.Timestamp(p), pd.Timestamp(b)):<12}" for k,(p,b) in CRISES.items())
    print(f"widen >= {thr:<4}  on {base:4.1f}% of months | {row}")

import sys
from pathlib import Path
import pandas as pd

D = Path(sys.argv[1])

def load(sid):
    df = pd.read_csv(D / f"{sid}.csv")
    df.columns = ["date", sid]
    df["date"] = pd.to_datetime(df["date"])
    s = pd.to_numeric(df[sid], errors="coerce").dropna()
    s.index = df.loc[s.index, "date"]
    return s.resample("MS").mean()

baa, gs10, tb3, ff, cpi, oil, ur, nfci = (load(s) for s in
    ["BAA", "GS10", "TB3MS", "FEDFUNDS", "CPIAUCSL", "WTISPLC", "UNRATE", "NFCI"])

spread = baa - gs10
sahm = ur.rolling(3).mean() - ur.rolling(3).mean().rolling(12).min()
signals = {
    "Yield curve inverted": (gs10 - tb3) < 0,
    "Fed hiking fast": (ff - ff.shift(18)) >= 1.5,
    "Inflation > 4%": (cpi.pct_change(12) * 100) > 4,
    "Oil shock": (oil.pct_change(12) * 100) > 50,
    "Credit spread widening": (spread - spread.rolling(24).min()) >= 0.5,
    "NFCI > 0 (old)": nfci > 0,
    "Jobs turning (Sahm)": sahm >= 0.5,
}

CRISES = {  # S&P 500 closing high -> closing low
    "1973 Oil":      ("1973-01-01", "1974-10-01"),
    "1980 Volcker":  ("1980-11-01", "1982-08-01"),
    "1990 Gulf War": ("1990-07-01", "1990-10-01"),
    "2000 Dot-com":  ("2000-03-01", "2002-10-01"),
    "2008 GFC":      ("2007-10-01", "2009-03-01"),
    "2020 Covid":    ("2020-02-01", "2020-03-01"),
}

def months(a, b):
    return (b.year - a.year) * 12 + (b.month - a.month)

def score(sig, peak, bottom):
    sig = sig.dropna()
    win = sig.loc[peak - pd.DateOffset(months=24):peak]
    if win.any():
        last_on = win[win].index[-1]
        before = sig.loc[:last_on]
        offs = before[~before]
        start = offs.index[-1] + pd.DateOffset(months=1) if len(offs) else before.index[0]
        state = "on at peak" if bool(sig.get(peak, False)) else f"off by peak"
        return f"WARNED {months(start, peak):>3} mo  ({start:%Y-%m}, {state})"
    after = sig.loc[peak + pd.DateOffset(months=1):bottom]
    if after.any():
        return f"late   +{months(peak, after[after].index[0])} mo ({after[after].index[0]:%Y-%m})"
    return "-"

for name, (p, b) in CRISES.items():
    peak, bottom = pd.Timestamp(p), pd.Timestamp(b)
    print(f"\n=== {name}  peak {peak:%Y-%m}  bottom {bottom:%Y-%m}")
    s0 = spread.loc[peak - pd.DateOffset(months=24)]
    print(f"    Baa-10Y spread: 24mo before {s0:.2f} | 24mo min {spread.loc[peak - pd.DateOffset(months=24):peak].min():.2f} | at peak {spread.loc[peak]:.2f} | max to bottom {spread.loc[peak:bottom].max():.2f}")
    for sname, sig in signals.items():
        print(f"    {sname:<24} {score(sig, peak, bottom)}")

print("\n=== Base rate: % of months ON, 1972-2019 (how often it cries wolf)")
for sname, sig in signals.items():
    s = sig.loc["1972":"2019"].dropna()
    print(f"    {sname:<24} {100 * s.mean():5.1f}%")

print("\n=== Credit spread rule switch-on episodes (start month, length)")
s = signals["Credit spread widening"].loc["1971":].fillna(False)
starts = s & ~s.shift(1, fill_value=False)
for st in s[starts].index:
    run = s.loc[st:]
    ln = (~run).idxmax() if (~run).any() else run.index[-1]
    print(f"    {st:%Y-%m}  {months(st, ln)} mo")

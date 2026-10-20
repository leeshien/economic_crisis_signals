"""Score every candidate signal against 6 crashes with the strict rule; report false-alarm rate."""
import sys
from pathlib import Path
import pandas as pd

S = Path(sys.argv[1])
D = S / "fred"


def load(sid, how="mean"):
    df = pd.read_csv(D / f"{sid}.csv")
    df.columns = ["date", sid]
    s = pd.to_numeric(df[sid], errors="coerce")
    s.index = pd.to_datetime(df["date"])
    s = s.dropna()
    r = s.resample("MS")
    out = r.mean() if how == "mean" else r.last()
    return out.ffill() if how == "ffill" else out


def quarterly(sid):  # quarterly -> monthly, forward-filled
    return load(sid).resample("MS").ffill()


# ── Shiller (earnings, CAPE) ──────────────────────────────────────────────
raw = pd.read_excel(S / "shiller" / "ie_data.xls", sheet_name="Data", header=7, engine="xlrd")
raw = raw[pd.to_numeric(raw["Fraction"], errors="coerce").notna()].copy()
frac = raw["Fraction"].astype(float)
yr = frac.astype(int)
mo = ((frac - yr) * 12 + 0.5).round().astype(int).clip(1, 12)
raw.index = pd.to_datetime(dict(year=yr, month=mo, day=1))
E = pd.to_numeric(raw["E"], errors="coerce").dropna()
CAPE = pd.to_numeric(raw["CAPE"], errors="coerce").dropna()
P = pd.to_numeric(raw["P"], errors="coerce").dropna()

# ── FRED ──────────────────────────────────────────────────────────────────
baa, gs10, tb3, ff = load("BAA"), load("GS10"), load("TB3MS"), load("FEDFUNDS")
cpi, oil, ur, nfci = load("CPIAUCSL"), load("WTISPLC"), load("UNRATE"), load("NFCI")
houst, permit, icsa, m2 = load("HOUST"), load("PERMIT"), load("ICSA"), load("M2SL")
sent, indpro, hours, sav = load("UMCSENT").resample("MS").mean().ffill(), load("INDPRO"), load("AWHMAN"), load("PSAVERT")
cp, gdp, hh, corp = quarterly("CP"), quarterly("GDP"), quarterly("CMDEBT"), quarterly("BCNSDODNS")
hpi, sloos, busl = quarterly("USSTHPI"), quarterly("DRTSCILM"), load("BUSLOANS")

yoy = lambda s: s.pct_change(12) * 100
spread = baa - gs10
sahm_ma = ur.rolling(3).mean()
cpi_yoy = yoy(cpi)

CORE = {
    "1 Yield curve inverted (10Y<3M)":      (gs10 - tb3) < 0,
    "2 Fed hiking fast (+1.5pt/18mo)":      (ff - ff.shift(18)) >= 1.5,
    "3 Inflation >4% YoY":                  cpi_yoy > 4,
    "4 Oil shock (+50% YoY)":               yoy(oil) > 50,
    "5 Credit spread widening (+0.5)":      (spread - spread.rolling(24).min()) >= 0.5,
    "6 Stocks expensive (CAPE>25)":         CAPE > 25,
    "7 Earnings falling (EPS YoY<0)":       yoy(E) < 0,
    "8 Jobs turning (Sahm >=0.5)":          (sahm_ma - sahm_ma.rolling(12).min()) >= 0.5,
}
CANDIDATES = {
    "Housing starts -20% YoY (3mo avg)":    yoy(houst.rolling(3).mean()) <= -20,
    "Building permits -20% YoY (3mo avg)":  yoy(permit.rolling(3).mean()) <= -20,
    "Jobless claims +20% vs 12mo low":      icsa / icsa.rolling(12).min() - 1 >= 0.20,
    "Real M2 shrinking (YoY<0)":            (yoy(m2) - cpi_yoy) < 0,
    "Sentiment -15pt vs 12mo high":         (sent.rolling(12).max() - sent) >= 15,
    "Industrial production YoY<0":          yoy(indpro) < 0,
    "Factory hours -0.5h vs 12mo high":     (hours.rolling(12).max() - hours) >= 0.5,
    "Corp profits (CP) YoY<0":              yoy(cp) < 0,
    "Real rate rising +3pt/24mo":           ((ff - cpi_yoy) - (ff - cpi_yoy).shift(24)) >= 3,
    "Household debt/GDP +5pt/3y":           ((hh / gdp) * 100 - ((hh / gdp) * 100).shift(36)) >= 5,
    "Corp debt/GDP +3pt/3y":                ((corp / gdp) * 100 - ((corp / gdp) * 100).shift(36)) >= 3,
    "Business loans >+15% YoY":             yoy(busl) > 15,
    "Saving rate -2pt vs 24mo high":        (sav.rolling(24).max() - sav) >= 2,
    "NFCI >0":                              nfci > 0,
    "Home prices YoY<0 (from 1976)":        yoy(hpi) < 0,
    "Banks tightening >20% (from 1990)":    sloos > 20,
}

CRISES = {  # S&P 500 closing-high month -> closing-low month
    "1973": ("1973-01-01", "1974-10-01"),
    "1980": ("1980-11-01", "1982-08-01"),
    "1990": ("1990-07-01", "1990-10-01"),
    "2000": ("2000-03-01", "2002-10-01"),
    "2008": ("2007-10-01", "2009-03-01"),
    "2020": ("2020-02-01", "2020-03-01"),
    "2022": ("2022-01-01", "2022-10-01"),
}


def months(a, b):
    return (b.year - a.year) * 12 + (b.month - a.month)


def score(sig, peak, bottom):
    sig = sig.dropna().astype(bool)
    if sig.empty or sig.index[0] > peak - pd.DateOffset(months=24):
        return "n/a"
    win = sig.loc[peak - pd.DateOffset(months=24):peak]
    prev = sig.shift(1).reindex(win.index).fillna(False).astype(bool)
    starts = win & ~prev
    if starts.any() and sig.loc[peak - pd.DateOffset(months=12):peak].any():
        return f"{months(starts[starts].index[0], peak)}"
    if sig.loc[peak - pd.DateOffset(months=12):peak].any():   # chronic: switched on before the window
        on_since = sig.loc[:peak][~sig.loc[:peak]].index
        return f"C{months(on_since[-1], peak) if len(on_since) else 99}"
    after = sig.loc[peak + pd.DateOffset(months=1):bottom]
    if after.any():
        return f"late+{months(peak, after[after].index[0])}"
    return "·"


def table(group):
    hdr = f"{'signal':<38}" + "".join(f"{k:>9}" for k in CRISES) + f"{'early':>7}{'%on':>7}"
    print(hdr)
    for name, sig in group.items():
        cells = [score(sig, pd.Timestamp(p), pd.Timestamp(b)) for p, b in CRISES.values()]
        early = sum(c.isdigit() for c in cells); chronic = sum(c.startswith("C") for c in cells)
        base = sig.dropna().astype(bool).loc["1972":"2019"]
        print(f"{name:<38}" + "".join(f"{c:>9}" for c in cells) + f"{early:>5}/7 +{chronic}C{100 * base.mean():6.0f}%")


print("Cells: number = months early (switched on inside 24-mo window, on within 12 mo of peak);")
print("C<N> = chronic: already on, switched on N months before peak (before the 24-mo window).")
print("late+N = first on N months after peak; · = never; n/a = no data. %on = share of months ON 1972-2019.\n")
print("── CORE 8 ──"); table(CORE)
print("\n── CANDIDATES ──"); table(CANDIDATES)

print("\nData end dates: Shiller E", E.index[-1].date(), "| CAPE", CAPE.index[-1].date())

# ── Bear markets not in the list: daily S&P (FRED, last 10y) + Shiller monthly ─
sp = pd.read_csv(D / "SP500.csv"); sp.columns = ["date", "v"]
sp = pd.Series(pd.to_numeric(sp["v"], errors="coerce").values, index=pd.to_datetime(sp["date"])).dropna()
print("\nS&P 500 drawdowns >= 15% (daily closes, FRED 2016-):")
peak_v, peak_d, trough_v, trough_d, in_dd = sp.iloc[0], sp.index[0], None, None, False
for d, v in sp.items():
    if v > peak_v:
        if in_dd and (1 - trough_v / peak_v) >= 0.15:
            print(f"   peak {peak_d.date()} {peak_v:.0f} -> low {trough_d.date()} {trough_v:.0f}  -{100 * (1 - trough_v / peak_v):.1f}%")
        peak_v, peak_d, trough_v, trough_d, in_dd = v, d, v, d, False
    elif trough_v is None or v < trough_v:
        trough_v, trough_d, in_dd = v, d, True
if in_dd:
    print(f"   current: from peak {peak_d.date()} {peak_v:.0f} low {trough_d.date()} {trough_v:.0f}  -{100 * (1 - trough_v / peak_v):.1f}%  (latest {sp.index[-1].date()} {sp.iloc[-1]:.0f})")

"""Signal metrics and on/off rules. Pure functions: monthly Series in, Series out."""
import operator

import pandas as pd

_OPS = {"<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge}


def yoy(s: pd.Series) -> pd.Series:
    """% change vs 12 months earlier (by date, not by position)."""
    prev = s.shift(12, freq="MS").reindex(s.index)
    return (s / prev - 1) * 100


def _corp_debt(d):
    # BCNSDODNS is in millions of dollars, GDP in billions (annual rate).
    pct = d["BCNSDODNS"] / 1000 / d["GDP"] * 100
    return pct - pct.shift(36, freq="MS").reindex(pct.index)


def _rise_above_low(s: pd.Series, months: int) -> pd.Series:
    return s - s.rolling(months).min()


def _drop_below_high(s: pd.Series, months: int) -> pd.Series:
    return s.rolling(months).max() - s


METRICS = {
    "yield_curve":   lambda d: (d["GS10"] - d["TB3MS"]).dropna(),
    "fed_hiking":    lambda d: (d["FEDFUNDS"] - d["FEDFUNDS"].shift(18, freq="MS")).dropna(),
    "inflation":     lambda d: yoy(d["CPIAUCSL"]),
    "oil_shock":     lambda d: yoy(d["WTISPLC"]),
    "credit_spread": lambda d: _rise_above_low((d["BAA"] - d["GS10"]).dropna(), 24),
    "corp_debt":     _corp_debt,
    "cape":          lambda d: d["CAPE"],
    "profits":       lambda d: yoy(d["CP"]),
    "housing":       lambda d: yoy(d["HOUST"].rolling(3).mean()),
    "factory_hours": lambda d: _drop_below_high(d["AWHMAN"], 12),
    "sahm":          lambda d: _rise_above_low(d["UNRATE"].rolling(3).mean(), 12),
}


def metric(signal: dict, data: dict) -> pd.Series:
    return METRICS[signal["id"]](data).dropna().rename(signal["id"])


def lights(signal: dict, data: dict) -> pd.Series:
    """Boolean monthly Series: True where the signal's light is ON."""
    m = metric(signal, data)
    return _OPS[signal["op"]](m, signal["threshold"]).rename(signal["id"])

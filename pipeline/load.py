"""Read data/raw/ into monthly pandas Series (index = month start)."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"

FRED_SERIES = [
    "GS10", "TB3MS", "FEDFUNDS", "CPIAUCSL", "WTISPLC", "BAA",
    "BCNSDODNS", "GDP", "CP", "HOUST", "AWHMAN", "UNRATE", "USREC", "SP500",
]
# Quarterly series are dated at the quarter's first month by FRED. We re-date them to the
# quarter's last month so no rule "sees" a quarter's value before the quarter has ended.
QUARTERLY = {"BCNSDODNS", "GDP", "CP"}


def monthly(s: pd.Series, quarterly: bool = False) -> pd.Series:
    s = s.dropna().sort_index()
    if quarterly:
        s.index = s.index + pd.DateOffset(months=2)
        return s.resample("MS").ffill()
    return s.resample("MS").mean().dropna()


def read_fred(series_id: str, raw_dir: Path = RAW_DIR) -> pd.Series:
    df = pd.read_csv(raw_dir / "fred" / f"{series_id}.csv")
    s = pd.Series(pd.to_numeric(df.iloc[:, 1], errors="coerce").values,
                  index=pd.to_datetime(df.iloc[:, 0]), name=series_id)
    return s


def last_observation(series_id: str, raw_dir: Path = RAW_DIR) -> pd.Timestamp:
    """Date of the latest real observation (quarterly: the quarter's last month)."""
    if series_id in ("CAPE", "SHILLER_P"):
        df = pd.read_csv(raw_dir / "shiller.csv", parse_dates=["date"])
        col = "CAPE" if series_id == "CAPE" else "P"
        return df.dropna(subset=[col])["date"].max()
    s = read_fred(series_id, raw_dir).dropna()
    last = s.index.max()
    return last + pd.DateOffset(months=2) if series_id in QUARTERLY else last


def load_all(raw_dir: Path = RAW_DIR) -> dict:
    """Return {series_id: monthly Series}, plus CAPE and SP500M (monthly S&P 500 level)."""
    data = {sid: monthly(read_fred(sid, raw_dir), sid in QUARTERLY)
            for sid in FRED_SERIES if (raw_dir / "fred" / f"{sid}.csv").exists()}
    shiller = pd.read_csv(raw_dir / "shiller.csv", parse_dates=["date"]).set_index("date")
    data["CAPE"] = shiller["CAPE"].dropna().rename("CAPE")
    # S&P 500 monthly average: Shiller history, FRED daily closes where available (last ~10y).
    sp = shiller["P"].dropna()
    if "SP500" in data:
        recent = data["SP500"]
        sp = pd.concat([sp[sp.index < recent.index[0]], recent])
    data["SP500M"] = sp.rename("SP500M")
    return data

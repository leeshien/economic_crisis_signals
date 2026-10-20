"""Download raw data into data/raw/. Never fails the whole run: a series that cannot be
fetched keeps its previous file. Usage: python -m pipeline.fetch [data_dir]
"""
import io
import logging
import sys
from pathlib import Path

import pandas as pd
import requests

from pipeline.load import FRED_SERIES, RAW_DIR

_log = logging.getLogger(__name__)
_FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
_SHILLER_XLS = "http://www.econ.yale.edu/~shiller/data/ie_data.xls"


def fetch_fred(series_id: str, out_dir: Path) -> bool:
    try:
        resp = requests.get(_FRED_CSV.format(series_id), timeout=60)
        resp.raise_for_status()
        df = pd.read_csv(io.StringIO(resp.text))
        if df.shape[1] != 2 or df.dropna().empty:
            raise ValueError(f"unexpected CSV shape {df.shape}")
    except Exception as exc:
        _log.warning("FRED %s: fetch failed (%s); keeping previous file", series_id, exc)
        return False
    (out_dir / "fred").mkdir(parents=True, exist_ok=True)
    (out_dir / "fred" / f"{series_id}.csv").write_text(resp.text)
    return True


def parse_shiller(xls_bytes: bytes) -> pd.DataFrame:
    """Shiller ie_data.xls -> DataFrame(date, P, CAPE), monthly."""
    raw = pd.read_excel(io.BytesIO(xls_bytes), sheet_name="Data", header=7, engine="xlrd")
    frac = pd.to_numeric(raw["Fraction"], errors="coerce")
    raw = raw[frac.notna()].copy()
    frac = frac[frac.notna()]
    year = frac.astype(int)
    month = ((frac - year) * 12 + 0.5).round().astype(int).clip(1, 12)
    out = pd.DataFrame({
        "date": pd.to_datetime(dict(year=year, month=month, day=1)),
        "P": pd.to_numeric(raw["P"], errors="coerce"),
        "CAPE": pd.to_numeric(raw["CAPE"], errors="coerce"),
    })
    return out.dropna(subset=["P"]).reset_index(drop=True)


def fetch_shiller(out_dir: Path) -> bool:
    try:
        resp = requests.get(_SHILLER_XLS, timeout=120)
        resp.raise_for_status()
        df = parse_shiller(resp.content)
    except Exception as exc:
        _log.warning("Shiller: fetch failed (%s); keeping previous file", exc)
        return False
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / "shiller.csv", index=False, date_format="%Y-%m-%d")
    return True


def fetch_all(out_dir: Path = RAW_DIR) -> dict:
    results = {sid: fetch_fred(sid, out_dir) for sid in FRED_SERIES}
    results["SHILLER"] = fetch_shiller(out_dir)
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else RAW_DIR
    res = fetch_all(target)
    ok = [k for k, v in res.items() if v]
    failed = [k for k, v in res.items() if not v]
    print(f"fetched {len(ok)}/{len(res)}" + (f"; failed (kept old): {', '.join(failed)}" if failed else ""))

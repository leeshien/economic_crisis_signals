"""Scoring: did a signal warn before a crisis peak? Pure functions, no I/O.

States (see spec section 5):
  early   switched on inside [W, P] and on at some month in [P-12, P]
  chronic on in [P-12, P] but its run started before W ("long on")
  late    first on in (P, B]
  none    did not fire
  na      no data at W
W = max(P - 24 months, previous crisis bottom + 12 months).
"""
from dataclasses import dataclass, asdict
from typing import Optional

import pandas as pd

WINDOW_MONTHS = 24
RECENT_MONTHS = 12
GUARD_MONTHS = 12
FALSE_ALARM_SPAN = ("1972-01-01", "2019-12-01")


@dataclass
class Cell:
    state: str
    months: Optional[int] = None  # early: months before peak; chronic: months on; late: months after

    def to_dict(self):
        return asdict(self)


def month_floor(ts) -> pd.Timestamp:
    ts = pd.Timestamp(ts)
    return pd.Timestamp(year=ts.year, month=ts.month, day=1)


def months_between(a: pd.Timestamp, b: pd.Timestamp) -> int:
    return (b.year - a.year) * 12 + (b.month - a.month)


def window_start(peak: pd.Timestamp, prev_bottom: Optional[pd.Timestamp] = None) -> pd.Timestamp:
    w = peak - pd.DateOffset(months=WINDOW_MONTHS)
    if prev_bottom is not None:
        w = max(w, prev_bottom + pd.DateOffset(months=GUARD_MONTHS))
    return w


def _clean(sig: pd.Series) -> pd.Series:
    return sig.dropna().astype(bool).sort_index()


def run_start(sig: pd.Series, at: pd.Timestamp) -> pd.Timestamp:
    """First month of the ON run containing month `at` (sig must be ON at `at`)."""
    before = sig.loc[:at]
    offs = before[~before]
    if offs.empty:
        return before.index[0]
    return offs.index[-1] + pd.DateOffset(months=1)


def score_cell(sig: pd.Series, peak, bottom, w_start) -> Cell:
    sig = _clean(sig)
    peak, bottom, w_start = month_floor(peak), month_floor(bottom), month_floor(w_start)
    if sig.empty or sig.index[0] > w_start:
        return Cell("na")
    recent = sig.loc[peak - pd.DateOffset(months=RECENT_MONTHS):peak]
    if recent.any():
        last_on = recent[recent].index[-1]
        win = sig.loc[w_start:peak]
        prev = sig.shift(1).reindex(win.index)
        prev = prev.where(prev.notna(), False).astype(bool)
        switch_ons = win & ~prev
        # the first month of the window counts as a switch-on only if the light was off before it
        if switch_ons.any():
            first = switch_ons[switch_ons].index[0]
            return Cell("early", months_between(first, peak))
        return Cell("chronic", months_between(run_start(sig, last_on), peak))
    after = sig.loc[peak + pd.DateOffset(months=1):bottom]
    if after.any():
        return Cell("late", months_between(peak, after[after].index[0]))
    return Cell("none")


def score_crises(lights: dict, crises: list) -> dict:
    """{crisis_id: {signal_id: Cell}} with the back-to-back guard applied."""
    out, prev_bottom = {}, None
    for c in sorted(crises, key=lambda c: c["peak"]):
        peak, bottom = month_floor(c["peak"]), month_floor(c["bottom"])
        w = window_start(peak, prev_bottom)
        out[c["id"]] = {sid: score_cell(sig, peak, bottom, w) for sid, sig in lights.items()}
        prev_bottom = bottom
    return out


def false_alarm_rate(sig: pd.Series, span=FALSE_ALARM_SPAN) -> Optional[float]:
    s = _clean(sig).loc[span[0]:span[1]]
    return None if s.empty else round(100 * s.mean(), 1)


def on_runs(sig: pd.Series, start, end) -> list:
    """ON runs overlapping [start, end] as [(first_month, last_month)], clipped to the range."""
    s = _clean(sig).loc[month_floor(start):month_floor(end)]
    runs, cur = [], None
    for ts, on in s.items():
        if on and cur is None:
            cur = ts
        elif not on and cur is not None:
            runs.append((cur, ts - pd.DateOffset(months=1)))
            cur = None
    if cur is not None:
        runs.append((cur, s.index[-1]))
    return runs


def run_kind(run_first, run_last, peak, w_start, sig: pd.Series, cell_state: str) -> str:
    """Colour class for a timeline bar, consistent with the scored cell:
    red only if the cell is 'early', pink only if 'chronic'; other pre-peak runs are 'old'."""
    if run_first > peak:
        return "after"
    true_start = run_start(_clean(sig), run_first)
    if cell_state == "early" and true_start >= w_start:
        return "early"
    recent = run_last >= peak - pd.DateOffset(months=RECENT_MONTHS)
    if cell_state == "chronic" and true_start < w_start and recent:
        return "chronic"
    return "old"


def first_fire(sig: pd.Series, after, until) -> Optional[pd.Timestamp]:
    """First switch-on in (after, until]."""
    s = _clean(sig)
    prev = s.shift(1)
    prev = prev.where(prev.notna(), False).astype(bool)
    ons = (s & ~prev).loc[month_floor(after) + pd.DateOffset(months=1):month_floor(until)]
    return ons[ons].index[0] if ons.any() else None

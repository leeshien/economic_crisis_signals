"""Assemble everything the site shows into plain dicts (JSON-serialisable)."""
import datetime as dt

import pandas as pd

from config.crises import CRISES
from config.signals import SIGNALS, SAHM, GROUPS
from pipeline import rules, score
from pipeline.load import last_observation, QUARTERLY

TIMELINE_BEFORE = 36
TIMELINE_AFTER = 6
STALE_DAYS = {"monthly": 100, "quarterly": 200}  # FRED dates obs at period start; ~1.5-month publication lag


def _rel(ts, peak) -> int:
    return score.months_between(score.month_floor(peak), ts)


def _points(s: pd.Series, start, end, peak, digits=2):
    s = s.dropna().loc[start:end]
    return [[_rel(ts, peak), round(float(v), digits)] for ts, v in s.items()]


def _usrec_ranges(usrec: pd.Series, start, end, peak):
    on = usrec.loc[start:end] > 0.5
    return [[_rel(a, peak), _rel(b, peak)] for a, b in score.on_runs(on, start, end)]


def _timeline(lights, metrics, data, peak, bottom, w_start, end=None):
    start = peak - pd.DateOffset(months=TIMELINE_BEFORE)
    end = end or (bottom + pd.DateOffset(months=TIMELINE_AFTER))
    rows = []
    for sig in SIGNALS:
        lt = lights[sig["id"]]
        cell = score.score_cell(lt, peak, bottom, w_start)
        runs = [{"a": _rel(a, peak), "b": _rel(b, peak),
                 "kind": score.run_kind(a, b, peak, w_start, lt, cell.state)}
                for a, b in score.on_runs(lt, start, end)]
        rows.append({"id": sig["id"], "name": sig["name"], "runs": runs, "cell": cell.to_dict()})
    sahm_fire = score.first_fire(lights["sahm"], w_start, end)
    return {
        "x0": -TIMELINE_BEFORE, "x1": _rel(end, peak),
        "window": _rel(w_start, peak),
        "sp500": _points(data["SP500M"], start, end, peak, 1),
        "recessions": _usrec_ranges(data["USREC"], start, end, peak) if "USREC" in data else [],
        "rows": rows,
        "sahm": _rel(sahm_fire, peak) if sahm_fire is not None else None,
    }


def _small_multiples(metrics, peak, start, end):
    out = []
    for sig in SIGNALS:
        out.append({
            "id": sig["id"], "name": sig["name"], "label": sig["metric_label"],
            "threshold": sig["threshold"], "op": sig["op"],
            "points": _points(metrics[sig["id"]], start, end, peak),
        })
    return out


def _signal_inputs_as_of(sig, raw_dir=None):
    kwargs = {"raw_dir": raw_dir} if raw_dir else {}
    dates = [last_observation(i, **kwargs) for i in sig["inputs"]]
    return min(dates)


def build_report(data: dict, today: dt.date, raw_dir=None) -> dict:
    lights = {s["id"]: rules.lights(s, data) for s in SIGNALS + [SAHM]}
    metrics = {s["id"]: rules.metric(s, data) for s in SIGNALS + [SAHM]}
    scored = score.score_crises({s["id"]: lights[s["id"]] for s in SIGNALS}, CRISES)

    signals = []
    for s in SIGNALS:
        signals.append({**s, "group_name": GROUPS[s["group"]],
                        "false_alarm": score.false_alarm_rate(lights[s["id"]])})

    crises, prev_bottom = [], None
    for c in sorted(CRISES, key=lambda c: c["peak"]):
        peak, bottom = score.month_floor(c["peak"]), score.month_floor(c["bottom"])
        w = score.window_start(peak, prev_bottom)
        cells = {sid: cell.to_dict() for sid, cell in scored[c["id"]].items()}
        unemp = data["UNRATE"].loc[peak:bottom + pd.DateOffset(months=24)]
        start = peak - pd.DateOffset(months=TIMELINE_BEFORE)
        end = bottom + pd.DateOffset(months=TIMELINE_AFTER)
        crises.append({
            **{k: v for k, v in c.items()},
            "fall_pct": round(100 * (c["bottom_close"] / c["peak_close"] - 1), 1),
            "duration_months": score.months_between(peak, bottom),
            "peak_unemployment": round(float(unemp.max()), 1) if not unemp.empty else None,
            "cells": cells,
            "early_count": sum(v["state"] == "early" for v in cells.values()),
            "chronic_count": sum(v["state"] == "chronic" for v in cells.values()),
            "timeline": _timeline(lights, metrics, data, peak, bottom, w),
            "small_multiples": _small_multiples(metrics, peak, start, end),
        })
        prev_bottom = bottom

    return {
        "generated": today.isoformat(),
        "signals": signals,
        "sahm": SAHM,
        "crises": crises,
        "today": _today(lights, metrics, data, today, crises, raw_dir),
    }


_OP_WORDS = {">": "above", ">=": "at or above", "<": "below", "<=": "at or below"}


def fmt_value(v: float, unit: str, sign: bool = True) -> str:
    """Display a metric value: '+0.17 pts', '-12.4%', '31.2', '0.3 hrs'."""
    if unit == "pts":
        return f"{v:+.2f} pts" if sign else f"{v:.2f} pts"
    if unit == "%":
        return f"{v:+.1f}%" if sign else f"{v:.1f}%"
    if unit == "hrs":
        return f"{v:.1f} hrs"
    return f"{v:.1f}"


def _detail(sid: str, d: dict, m) -> str:
    """The underlying figures behind a signal's latest value, in words."""
    def at(key, t=m):
        return float(d[key].dropna().loc[:t].iloc[-1])

    def ago(n):
        return m - pd.DateOffset(months=n)

    if sid == "yield_curve":
        return f"10-year yield {at('GS10'):.2f}% minus 3-month yield {at('TB3MS'):.2f}%"
    if sid == "fed_hiking":
        return f"Fed funds rate {at('FEDFUNDS'):.2f}% now, {at('FEDFUNDS', ago(18)):.2f}% in {ago(18):%b %Y}"
    if sid == "inflation":
        return f"Consumer price index {at('CPIAUCSL'):.1f} now, {at('CPIAUCSL', ago(12)):.1f} in {ago(12):%b %Y}"
    if sid == "oil_shock":
        return f"US crude ${at('WTISPLC'):.2f} a barrel now, ${at('WTISPLC', ago(12)):.2f} in {ago(12):%b %Y}"
    if sid == "credit_spread":
        spread = (d["BAA"] - d["GS10"]).dropna().loc[:m]
        return (f"Baa bonds {at('BAA'):.2f}% minus 10-year {at('GS10'):.2f}% = {spread.iloc[-1]:.2f} pts; "
                f"lowest in 24 months {spread.iloc[-24:].min():.2f} pts")
    if sid == "corp_debt":
        pct = lambda t: at("BCNSDODNS", t) / 1000 / at("GDP", t) * 100
        return f"Company debt {pct(m):.1f}% of GDP now, {pct(ago(36)):.1f}% in {ago(36):%b %Y}"
    if sid == "cape":
        return f"Shiller CAPE {at('CAPE'):.1f} (last published {m:%b %Y})"
    if sid == "profits":
        return f"Profits ${at('CP') / 1000:.2f} trillion a year now, ${at('CP', ago(12)) / 1000:.2f} trillion in {ago(12):%b %Y}"
    if sid == "housing":
        avg = d["HOUST"].rolling(3).mean().dropna()
        return (f"{avg.loc[:m].iloc[-1] / 1000:.2f} million homes a year (3-month average) now, "
                f"{avg.loc[:ago(12)].iloc[-1] / 1000:.2f} million in {ago(12):%b %Y}")
    if sid == "factory_hours":
        hrs = d["AWHMAN"].dropna().loc[:m]
        return f"Factory week {hrs.iloc[-1]:.1f} hours now; 12-month high {hrs.iloc[-12:].max():.1f} hours"
    return ""


def _reading(s: dict, metric_s: pd.Series, data: dict, latest) -> dict:
    """Latest value of a signal's metric, its trigger, and how far the value is from it."""
    m = metric_s.dropna()
    v, t, unit = float(m.iloc[-1]), s["threshold"], s["unit"]
    rising = s["op"] in (">", ">=")
    gap = (t - v) if rising else (v - t)  # > 0: still needs to move this far to switch on
    start = latest - pd.DateOffset(months=TIMELINE_BEFORE)
    return {
        "value": round(v, 4), "value_text": fmt_value(v, unit),
        "value_month": m.index[-1].strftime("%b %Y"),
        "trigger_text": f"{_OP_WORDS[s['op']]} {fmt_value(t, unit, sign=False)}",
        # a gap in a % measure is in percentage points
        "gap_text": f"{abs(gap):.1f} pts" if unit == "%" else fmt_value(abs(gap), unit, sign=False),
        "direction": ("rise" if rising else "fall"),
        "detail": _detail(s["id"], data, m.index[-1]),
        "spark": {"id": s["id"], "name": s["name"], "label": s["metric_label"],
                  "threshold": t, "op": s["op"], "points": _points(m, start, latest, latest)},
    }


def _today(lights, metrics, data, today, crises, raw_dir):
    today_ts = pd.Timestamp(today)
    latest = max(score.month_floor(lights[s["id"]].dropna().index[-1]) for s in SIGNALS)
    rows, on_count, valid = [], 0, 0
    for s in SIGNALS:
        lt = lights[s["id"]].dropna()
        as_of = _signal_inputs_as_of(s, raw_dir)
        freq = "quarterly" if any(i in QUARTERLY for i in s["inputs"]) else "monthly"
        age = (today_ts - as_of).days
        stale = age > STALE_DAYS[freq]
        on = bool(lt.iloc[-1]) if not lt.empty else None
        if not stale and on is not None:
            valid += 1
            on_count += int(on)
        since = score.run_start(lt, lt.index[-1]) if on and not stale else None
        rows.append({
            "id": s["id"], "name": s["name"], "group": s["group"], "on": on, "stale": stale,
            "as_of": as_of.strftime("%Y-%m"), "age_days": age,
            "on_since": since.strftime("%Y-%m") if since is not None else None,
            "on_months": score.months_between(since, lt.index[-1]) + 1 if since is not None else None,
            "what": s["what"], "rule": s["rule"],
            **_reading(s, metrics[s["id"]], data, latest),
        })
    lit_at_peak = [c["early_count"] + c["chronic_count"] for c in crises]
    tl = _timeline(lights, None, data, latest, latest, latest - pd.DateOffset(months=24), end=latest)
    # On the today page a light is red only if it is on in the latest month (matches the table).
    by_id = {r["id"]: r for r in rows}
    for row in tl["rows"]:
        r = by_id[row["id"]]
        lit_now = bool(r["on"]) and not r["stale"]
        last = _rel(lights[row["id"]].dropna().index[-1], latest)
        for run in row["runs"]:
            run["kind"] = "early" if lit_now and run["b"] == last else "old"
        label = "no current data" if r["stale"] else (f"ON since {r['on_since']}" if lit_now else "off")
        row["cell"] = {"state": "early" if lit_now else ("na" if r["stale"] else "none"),
                       "months": None, "label": label}
    return {
        "rows": rows, "on": on_count, "valid": valid, "total": len(SIGNALS),
        "typical_min": min(lit_at_peak), "typical_max": max(lit_at_peak),
        "latest_month": latest.strftime("%Y-%m"),
        "timeline": tl,
    }

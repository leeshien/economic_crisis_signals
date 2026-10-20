import pandas as pd
import pytest

from pipeline import score


def lights(start, on_ranges, end="2010-12-01"):
    """Monthly bool series, ON within each (first, last) month range (inclusive)."""
    idx = pd.date_range(start, end, freq="MS")
    s = pd.Series(False, index=idx)
    for a, b in on_ranges:
        s.loc[a:b] = True
    return s


PEAK, BOTTOM = pd.Timestamp("2007-10-01"), pd.Timestamp("2009-03-01")
W = score.window_start(PEAK)


def test_window_start_default_and_guard():
    assert W == pd.Timestamp("2005-10-01")
    assert score.window_start(pd.Timestamp("2022-01-01"), pd.Timestamp("2020-03-01")) == pd.Timestamp("2021-03-01")


def test_early_counts_first_switch_on_in_window():
    s = lights("2000-01-01", [("2006-08-01", "2007-06-01")])
    assert score.score_cell(s, PEAK, BOTTOM, W) == score.Cell("early", 14)


def test_switched_on_but_off_for_last_12_months_is_not_early():
    s = lights("2000-01-01", [("2006-01-01", "2006-06-01")])
    assert score.score_cell(s, PEAK, BOTTOM, W).state == "none"


def test_chronic_when_run_started_before_window():
    s = lights("2000-01-01", [("2003-01-01", "2008-01-01")])
    assert score.score_cell(s, PEAK, BOTTOM, W) == score.Cell("chronic", 57)


def test_late_when_first_on_after_peak():
    s = lights("2000-01-01", [("2008-02-01", "2009-01-01")])
    assert score.score_cell(s, PEAK, BOTTOM, W) == score.Cell("late", 4)


def test_on_after_bottom_only_is_none():
    s = lights("2000-01-01", [("2009-06-01", "2009-08-01")])
    assert score.score_cell(s, PEAK, BOTTOM, W).state == "none"


def test_na_when_data_starts_after_window():
    s = lights("2006-01-01", [("2007-01-01", "2007-05-01")])
    assert score.score_cell(s, PEAK, BOTTOM, W).state == "na"


def test_on_exactly_at_peak_month_counts_zero_months():
    s = lights("2000-01-01", [("2007-10-01", "2008-05-01")])
    assert score.score_cell(s, PEAK, BOTTOM, W) == score.Cell("early", 0)


def test_back_to_back_guard_turns_leftover_into_chronic():
    # light switched on during the previous crash and stayed on: not a fresh warning
    peak, bottom, prev_bottom = pd.Timestamp("2022-01-01"), pd.Timestamp("2022-10-01"), pd.Timestamp("2020-03-01")
    s = lights("2000-01-01", [("2020-04-01", "2021-12-01")], end="2023-12-01")
    guarded = score.window_start(peak, prev_bottom)
    assert score.score_cell(s, peak, bottom, score.window_start(peak)).state == "early"
    assert score.score_cell(s, peak, bottom, guarded) == score.Cell("chronic", 21)


def test_score_crises_applies_guard_in_date_order():
    crises = [{"id": "b", "peak": "2022-01-03", "bottom": "2022-10-12"},
              {"id": "a", "peak": "2020-02-19", "bottom": "2020-03-23"}]
    s = lights("2000-01-01", [("2020-04-01", "2021-12-01")], end="2023-12-01")
    out = score.score_crises({"x": s}, crises)
    assert out["b"]["x"].state == "chronic"


def test_false_alarm_rate():
    s = lights("1972-01-01", [("1972-01-01", "1983-12-01")], end="2019-12-01")
    assert score.false_alarm_rate(s) == 25.0


def test_on_runs_and_kinds():
    s = lights("2000-01-01", [("2003-01-01", "2004-01-01"), ("2006-08-01", "2007-06-01"), ("2008-02-01", "2008-04-01")])
    runs = score.on_runs(s, PEAK - pd.DateOffset(months=36), BOTTOM)
    assert runs == [(pd.Timestamp("2006-08-01"), pd.Timestamp("2007-06-01")),
                    (pd.Timestamp("2008-02-01"), pd.Timestamp("2008-04-01"))]
    assert [score.run_kind(a, b, PEAK, W, s, "early") for a, b in runs] == ["early", "after"]
    old = score.on_runs(s, "2002-01-01", "2004-06-01")[0]
    assert score.run_kind(*old, PEAK, W, s, "early") == "old"


def test_run_kind_never_red_unless_cell_is_early():
    # switched on inside the window but off for the final 12 months -> cell is not early
    s = lights("2000-01-01", [("2006-01-01", "2006-06-01")])
    assert score.score_cell(s, PEAK, BOTTOM, W).state == "none"
    run = score.on_runs(s, "2005-01-01", "2008-01-01")[0]
    assert score.run_kind(*run, PEAK, W, s, "none") == "old"


@pytest.mark.parametrize("a,b,expected", [("2007-10-01", "2007-10-01", 0), ("2006-08-01", "2007-10-01", 14)])
def test_months_between(a, b, expected):
    assert score.months_between(pd.Timestamp(a), pd.Timestamp(b)) == expected

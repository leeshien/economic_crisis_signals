import pandas as pd
import pytest

from config.signals import SIGNALS, SAHM
from pipeline import rules
from pipeline.load import monthly

IDX = pd.date_range("2000-01-01", "2004-12-01", freq="MS")
BY_ID = {s["id"]: s for s in SIGNALS + [SAHM]}


def const(v, idx=IDX):
    return pd.Series(float(v), index=idx)


def ramp(start, step, idx=IDX):
    return pd.Series([start + step * i for i in range(len(idx))], index=idx, dtype=float)


def test_yoy_uses_dates():
    s = ramp(100, 1)
    y = rules.yoy(s)
    assert y.loc["2001-01-01"] == pytest.approx(12.0)
    assert y.loc[:"2000-12-01"].isna().all()


def test_yield_curve_inverted_when_short_above_long():
    data = {"GS10": const(4.0), "TB3MS": const(4.5)}
    assert rules.lights(BY_ID["yield_curve"], data).all()
    data["TB3MS"] = const(3.0)
    assert not rules.lights(BY_ID["yield_curve"], data).any()


def test_fed_hiking_threshold_edge():
    ff = const(1.0)
    ff.loc["2001-07-01":] = 2.5  # exactly +1.5 vs 18 months earlier
    lt = rules.lights(BY_ID["fed_hiking"], {"FEDFUNDS": ff})
    assert lt.index[0] == pd.Timestamp("2001-07-01")  # first month with 18 months of history
    assert lt.loc["2001-07-01"] and lt.loc["2002-12-01"]
    assert not lt.loc["2003-01-01"]  # 18 months later the rise has aged out


def test_corp_debt_units_millions_vs_billions():
    # debt $5,000bn (=5,000,000 in millions) on GDP $10,000bn = 50% of GDP, rising 0.1 pt/month
    gdp = const(10_000)
    debt = pd.Series([5_000_000 + 1_000 * i * 10 for i in range(len(IDX))], index=IDX, dtype=float)
    m = rules.metric(BY_ID["corp_debt"], {"BCNSDODNS": debt, "GDP": gdp})
    assert m.iloc[0] == pytest.approx(3.6)  # 36 months x 0.1 pt
    assert rules.lights(BY_ID["corp_debt"], {"BCNSDODNS": debt, "GDP": gdp}).all()


def test_credit_spread_rise_above_24m_low():
    baa = const(6.0)
    baa.loc["2003-01-01":] = 6.6
    lt = rules.lights(BY_ID["credit_spread"], {"BAA": baa, "GS10": const(4.0)})
    assert not lt.loc[:"2002-12-01"].any() and lt.loc["2003-01-01":"2004-11-01"].all()
    assert not lt.loc["2004-12-01"]  # after 24 months at the new level, the low catches up


def test_factory_hours_drop_below_12m_high():
    h = const(41.0)
    h.loc["2002-06-01"] = 40.4
    lt = rules.lights(BY_ID["factory_hours"], {"AWHMAN": h})
    assert lt[lt].index.tolist() == [pd.Timestamp("2002-06-01")]


def test_housing_uses_3_month_average():
    h = const(1000)
    h.loc["2002-01-01":] = 700  # -30%
    lt = rules.lights(BY_ID["housing"], {"HOUST": h})
    assert not lt.loc["2002-01-01"]  # 3-mo avg only -10%
    assert lt.loc["2002-03-01"]


def test_sahm_rule():
    ur = const(4.0)
    ur.loc["2003-01-01":] = 4.6
    lt = rules.lights(SAHM, {"UNRATE": ur})
    # 3-month averages: Jan 4.2 (+0.2), Feb 4.4 (+0.4), Mar 4.6 (+0.6) -> fires in March
    assert lt[lt].index[0] == pd.Timestamp("2003-03-01")


def test_quarterly_redated_to_quarter_end():
    q = pd.Series([1.0, 2.0], index=pd.to_datetime(["2020-01-01", "2020-04-01"]))
    m = monthly(q, quarterly=True)
    assert m.index[0] == pd.Timestamp("2020-03-01")
    assert m.loc["2020-05-01"] == 1.0 and m.loc["2020-06-01"] == 2.0


def test_every_signal_has_a_metric():
    for s in SIGNALS + [SAHM]:
        assert s["id"] in rules.METRICS


def test_shiller_link_found_on_page():
    from pipeline.fetch import shiller_xls_url
    html = '<a href="//img1.wsimg.com/blobby/go/x/downloads/y/ie_data.xls?ver=17">Download</a>'
    assert shiller_xls_url(html) == "https://img1.wsimg.com/blobby/go/x/downloads/y/ie_data.xls?ver=17"

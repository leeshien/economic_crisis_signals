"""End-to-end checks on the committed data in data/raw/."""
import datetime as dt
import json

import pytest

from config.crises import CRISES
from config.signals import SIGNALS
from pipeline.load import RAW_DIR, load_all
from pipeline.report import build_report
from web import build

pytestmark = pytest.mark.skipif(not (RAW_DIR / "fred").exists(), reason="no data/raw — run python -m pipeline.fetch")


@pytest.fixture(scope="module")
def report():
    return build_report(load_all(), dt.date(2026, 10, 20))


def test_scoreboard_matches_reference(report):
    assert build.REFERENCE.exists(), "run python -m web.build --update-reference once and review it"
    assert build.check_reference(report, update=False) == []


def test_every_crisis_and_signal_scored(report):
    assert [c["id"] for c in report["crises"]] == sorted(c["id"] for c in CRISES)
    for c in report["crises"]:
        assert set(c["cells"]) == {s["id"] for s in SIGNALS}
        assert c["timeline"]["sp500"], c["id"]


def test_falls_match_bear_market_sizes(report):
    falls = {c["id"]: c["fall_pct"] for c in report["crises"]}
    assert falls["2008"] == pytest.approx(-56.8, abs=0.1)
    assert falls["1990"] == pytest.approx(-19.9, abs=0.1)


def test_render_smoke(report, tmp_path):
    build.render(report, tmp_path)
    pages = ["index.html", "today.html", "method.html"] + [f"crisis/{c['id']}.html" for c in CRISES]
    for p in pages:
        html = (tmp_path / p).read_text()
        assert "<svg" in html or p in ("index.html", "method.html"), p
    index = (tmp_path / "index.html").read_text()
    for s in SIGNALS:
        assert s["name"] in index
    json.loads((tmp_path / "data" / "report.json").read_text())

"""Every comic page renders to well-formed SVG (no Chrome needed)."""
import importlib
import xml.etree.ElementTree as ET

import pytest

STORIES = ["dotcom", "gfc", "covid"]


@pytest.mark.parametrize("story", STORIES)
def test_pages_are_valid_svg(story):
    mod = importlib.import_module(f"comics.{story}")
    assert len(mod.PAGES) == 12
    for name, fn in mod.PAGES:
        root = ET.fromstring(fn())
        assert root.tag.endswith("svg"), name


def test_gfc_timeline_marks_the_crash():
    from comics import gfc_story as st
    stamps = [e[5] for e in st.TIMELINE_UP + st.TIMELINE_DOWN if len(e) > 5]
    assert stamps == ["CRASH STARTS", "THE CRASH", "CRASH ENDS"]


def test_covid_timeline_marks_the_crash():
    from comics import covid_story as st
    stamps = [e[5] for e in st.TIMELINE_UP + st.TIMELINE_DOWN if len(e) > 5]
    assert stamps == ["CRASH STARTS", "THE CRASH", "CRASH ENDS"]

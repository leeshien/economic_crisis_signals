"""Build the static site into dist/. Usage:
    python -m web.build [--out dist] [--update-reference]
Fails (exit 1) if the computed scoreboard differs from tests/reference/scoreboard.json,
unless --update-reference is given.
"""
import argparse
import datetime as dt
import json
import shutil
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from config.signals import GROUPS
from pipeline.load import load_all, RAW_DIR, ROOT
from pipeline.report import build_report
from web import svg

WEB = Path(__file__).resolve().parent
REFERENCE = ROOT / "tests" / "reference" / "scoreboard.json"
README_IMAGE = ROOT / "docs" / "scoreboard.svg"  # committed copy shown in README.md


def cell_text(cell: dict) -> str:
    st, m = cell["state"], cell["months"]
    return {"early": f"{m} mo", "chronic": "long on", "late": f"late +{m}",
            "none": "", "na": "n/a"}[st]


def cell_title(cell: dict, signal_name: str) -> str:
    st, m = cell["state"], cell["months"]
    return {
        "early": f"{signal_name}: switched on {m} months before the peak",
        "chronic": f"{signal_name}: already on for {m} months at the peak",
        "late": f"{signal_name}: only fired {m} months after the peak",
        "none": f"{signal_name}: did not fire",
        "na": f"{signal_name}: no data for this period",
    }[st]


def scoreboard(report: dict) -> dict:
    return {c["id"]: {sid: c["cells"][sid] for sid in sorted(c["cells"])} for c in report["crises"]}


def check_reference(report: dict, update: bool) -> list:
    current = scoreboard(report)
    if update or not REFERENCE.exists():
        REFERENCE.parent.mkdir(parents=True, exist_ok=True)
        REFERENCE.write_text(json.dumps(current, indent=1, sort_keys=True) + "\n")
        return []
    expected = json.loads(REFERENCE.read_text())
    diffs = []
    for cid in sorted(set(expected) | set(current)):
        for sid in sorted(set(expected.get(cid, {})) | set(current.get(cid, {}))):
            a, b = expected.get(cid, {}).get(sid), current.get(cid, {}).get(sid)
            if a != b:
                diffs.append(f"{cid}/{sid}: reference {a} != computed {b}")
    return diffs


def render(report: dict, out: Path) -> None:
    env = Environment(loader=FileSystemLoader(WEB / "templates"), autoescape=True,
                      undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True)
    env.globals.update(cell_text=cell_text, cell_title=cell_title,
                       timeline_svg=svg.timeline_svg, sparkline_svg=svg.sparkline_svg,
                       groups=GROUPS)
    if out.exists():
        shutil.rmtree(out)
    (out / "crisis").mkdir(parents=True)
    shutil.copytree(WEB / "static", out / "static")
    (out / "data").mkdir()
    (out / "data" / "report.json").write_text(json.dumps(report, indent=1, default=str))
    (out / "scoreboard.svg").write_text(svg.scoreboard_svg(report, cell_text), encoding="utf-8")

    signals_by_id = {s["id"]: s for s in report["signals"]}
    common = {"report": report, "signals": report["signals"], "signals_by_id": signals_by_id,
              "crises": report["crises"], "today": report["today"]}
    pages = {"index.html": ("index.html", "", {}),
             "today.html": ("today.html", "", {}),
             "method.html": ("method.html", "", {})}
    for name, (tpl, root, extra) in pages.items():
        (out / name).write_text(env.get_template(tpl).render(root=root, page=name, **common, **extra))
    crises = report["crises"]
    for i, c in enumerate(crises):
        html = env.get_template("crisis.html").render(
            root="../", page="crisis", crisis=c,
            prev=crises[i - 1] if i > 0 else None,
            next=crises[i + 1] if i + 1 < len(crises) else None, **common)
        (out / "crisis" / f"{c['id']}.html").write_text(html)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "dist"))
    ap.add_argument("--raw", default=str(RAW_DIR))
    ap.add_argument("--update-reference", action="store_true")
    ap.add_argument("--today", default=None, help="YYYY-MM-DD (default: today)")
    args = ap.parse_args(argv)

    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    raw = Path(args.raw)
    report = build_report(load_all(raw), today, raw_dir=raw)

    for c in report["crises"]:
        if not c["dates_checked"]:
            print(f"WARNING: crisis {c['id']}: peak/bottom closes not yet checked against a daily source")
    diffs = check_reference(report, args.update_reference)
    if diffs:
        print("Scoreboard differs from tests/reference/scoreboard.json:", *diffs, sep="\n  ")
        print("If the change is intended, rerun with --update-reference and review the diff.")
        return 1
    render(report, Path(args.out))
    shutil.copyfile(Path(args.out) / "scoreboard.svg", README_IMAGE)
    t = report["today"]
    print(f"Built {args.out}: {len(report['crises'])} crises, {len(report['signals'])} signals; "
          f"today {t['on']} of {t['valid']} lights on (latest data {t['latest_month']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Render a crisis comic to PDF (and PNG previews) with headless Chrome. Usage:
    python -m comics.build [--story dotcom] [--out dist/comics] [--chrome PATH] [--png]
"""
import argparse
import importlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from pipeline.load import ROOT

ASSETS = Path(__file__).resolve().parent / "assets"
_CHROMES = ["google-chrome", "chromium", "chromium-browser", "chrome",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]


def find_chrome(given=None) -> str:
    for c in ([given] if given else []) + [os.environ.get("CHROME", "")] + _CHROMES:
        if c and (shutil.which(c) or Path(c).exists()):
            return shutil.which(c) or c
    raise SystemExit("Chrome/Chromium not found: pass --chrome or set CHROME")


def html_doc(svgs: list) -> str:
    font = lambda fam, f, w: (f"@font-face{{font-family:'{fam}';font-weight:{w};"
                              f"src:url('{(ASSETS / f).as_uri()}') format('truetype');}}")
    css = (font("Bangers", "Bangers-Regular.ttf", 400) + font("Comic Neue", "ComicNeue-Regular.ttf", 400)
           + font("Comic Neue", "ComicNeue-Bold.ttf", 700)
           + "@page{size:210mm 297mm;margin:0}html,body{margin:0;padding:0}"
           + ".page{width:210mm;height:297mm;overflow:hidden;page-break-after:always;break-after:page}"
           + ".page:last-child{page-break-after:auto;break-after:auto}.page svg{width:210mm;height:297mm;display:block}")
    pages = "".join(f'<div class="page">{s}</div>' for s in svgs)
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{pages}</body></html>"


def _chrome(chrome, *args):
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    "--allow-file-access-from-files", "--virtual-time-budget=4000", *args],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)


def build(story: str, out: Path, chrome: str, png: bool = False) -> Path:
    mod = importlib.import_module(f"comics.{story}")
    out = out.resolve()  # Chrome needs absolute output paths
    svgs = [fn() for _, fn in mod.PAGES]
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        doc = Path(tmp) / "comic.html"
        doc.write_text(html_doc(svgs), encoding="utf-8")
        pdf = out / f"{mod.SLUG}.pdf"
        _chrome(chrome, "--no-pdf-header-footer", f"--print-to-pdf={pdf}", doc.as_uri())
        if png:
            for (name, _), svg in zip(mod.PAGES, svgs):
                one = Path(tmp) / f"{name}.html"
                one.write_text(html_doc([svg]), encoding="utf-8")
                _chrome(chrome, "--window-size=794,1123", f"--screenshot={out / f'{mod.SLUG}-{name}.png'}", one.as_uri())
    return pdf


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--story", default="dotcom")
    ap.add_argument("--out", default=str(ROOT / "web" / "static" / "comics"))  # served with the site
    ap.add_argument("--chrome", default=None)
    ap.add_argument("--png", action="store_true", help="also write one PNG preview per page")
    args = ap.parse_args(argv)
    pdf = build(args.story, Path(args.out), find_chrome(args.chrome), args.png)
    print(f"Wrote {pdf}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

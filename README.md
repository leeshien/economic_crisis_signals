# MacroPulse — Did the crash give warnings?

A static website that teaches how the major US stock-market crashes since 1973 happened, and
which economic warning lights switched on before each market peak — scored with one fixed rule
for every crash. Design: `docs/superpowers/specs/2026-10-20-macro-pulse-design.md`.

## Run it

```bash
PY=~/anaconda3/envs/py312/bin/python      # any Python 3.12 with requirements.txt installed
$PY -m pipeline.fetch                     # download FRED + Shiller data into data/raw/ (no API key)
$PY -m pytest -q                          # unit tests + frozen reference scoreboard
$PY -m web.build                          # writes dist/ — open dist/index.html in a browser
$PY tools/print_scoreboard.py             # the scoreboard as text
```

If you change a rule, threshold or crisis date, the build stops because the scoreboard no longer
matches `tests/reference/scoreboard.json`. Review the change, then run
`$PY -m web.build --update-reference`.

## Layout

| Path | What |
|---|---|
| `config/crises.py` | 7 crises: peak/bottom closes, cause chain, notes, lesson, sources |
| `config/signals.py` | 10 signals + Sahm rule: inputs, threshold, plain-English text |
| `pipeline/fetch.py` | downloads raw data (keeps old files if a source fails) |
| `pipeline/load.py` | raw CSV → monthly series (quarterly dated at quarter end) |
| `pipeline/rules.py` | metric + threshold → light on/off per month |
| `pipeline/score.py` | early / long on / late / did not fire, lead times, false-alarm rate |
| `pipeline/report.py` | assembles everything the pages show |
| `web/` | Jinja2 templates, server-side SVG charts, CSS → `dist/` |
| `.github/workflows/refresh.yml` | weekly fetch → test → build → GitHub Pages |

Data: FRED (Federal Reserve Bank of St. Louis), Robert Shiller (CAPE; no updates since 2023-09),
NBER recession dates. Education only — not financial advice.

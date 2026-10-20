# MacroPulse v4 — "Did the crash give warnings?" — Design

Date: 2026-10-20 · Status: draft for review

## 1. Goal

A public, static website (GitHub Pages) that teaches non-experts two things about the major US
stock-market crashes since 1970:

1. **Why it happened** — a short cause chain per crisis.
2. **What warned beforehand** — which economic signals lit up, and how many months before the
   market peak.

Success test: a first-time visitor understands the home page's main chart within ~10 seconds,
without reading the methodology.

Core message the site must carry honestly: *no single light predicts a crash; several lights on at
once is meaningful; some crashes gave almost no warning.*

## 2. Scope

**In scope (v1)**
- 7 crises (section 3), 10 scored signals (section 4), one fixed scoring method (section 5).
- Pages: Home, 7 Crisis pages, Lights Today, Method (section 6).
- Weekly automated data refresh + deploy via GitHub Actions.

**Out of scope (v1)**
- Pre-1970 crises (1929, 1987), non-US crises.
- "As-published" data vintages (ALFRED). Site uses today's revised data and says so.
- Any prediction, "closest historical match", or buy/sell framing.
- The old Dash app (`macro-pulse-v3`) — retired, not ported. Its cause-chain text is reused as
  draft content.

## 3. Crises

Peak = S&P 500 closing high; bottom = closing low. Dates marked † were verified against FRED
`SP500` daily data during brainstorming; others must be verified against a cited source during
implementation (source URL stored in config).

| id | Name | Peak | Bottom | Fall |
|---|---|---|---|---|
| 1973 | Oil crisis & stagflation | 1973-01-11 | 1974-10-03 | −48% |
| 1980 | Volcker double-dip | 1980-11-28 | 1982-08-12 | −27% |
| 1990 | Gulf War recession | 1990-07-16 | 1990-10-11 | −20% |
| 2000 | Dot-com bust | 2000-03-24 | 2002-10-09 | −49% |
| 2008 | Global Financial Crisis | 2007-10-09 | 2009-03-09 | −57% |
| 2020 | Covid crash | 2020-02-19 † | 2020-03-23 † | −34% |
| 2022 | Inflation & rate shock | 2022-01-03 † | 2022-10-12 † | −25% |

Notes the content must state:
- **1973:** the market peaked in January, nine months *before* the October oil embargo. The v3 claim
  "all 11 indicators warned 18 months early" measured from the embargo and is withdrawn.
- **1990:** −19.9%, just short of the −20% bear-market convention; included as a recession crash.
- **2000:** the S&P made a near-equal second high on 2000-09-01; the site uses the March high and
  mentions the double top.
- 2018 (−19.8%) and 2025 (−18.9%) are near-misses, not included in v1.

## 4. Signals (10)

All monthly. Quarterly series are dated at the quarter's last month, then forward-filled.
"Lit before peak" = output of `pipeline/` (frozen in `tests/reference/scoreboard.json`), with the
back-to-back guard. Numbers = months early; **C** = already on for years.

> Correction (2026-10-20): the brainstorming scripts in `research/validation/` mis-scored quarterly
> series (empty in-between months counted as "off") and had a units bug for debt/GDP. Their
> corporate-debt, household-debt and profits figures are wrong; the table above supersedes them.

| # | Signal | Group | Source | Rule — light ON when | Lit before peak | False-alarm* |
|---|---|---|---|---|---|---|
| 1 | Yield curve inverted | Money & rates | FRED `GS10 − TB3MS` | spread < 0 | 1980·23, 2008·14, 2020·8 | 10% |
| 2 | Fed hiking fast | Money & rates | FRED `FEDFUNDS` | rate ≥ 1.5 pt above 18 months earlier | 1980·1, 1990·23; C 2008 | 23% |
| 3 | Inflation high | Prices | FRED `CPIAUCSL` | YoY > 4% | 1990·24, 2022·9; C 1980 | 32% |
| 4 | Oil shock | Prices | FRED `WTISPLC` | YoY > +50% | 1980·15, 2000·7, 2022·10 | 11% |
| 5 | Credit spread widening | Credit | FRED `BAA − GS10` | ≥ 0.5 pt above its 24-month low | 1980·17, 1990·12, 2000·18, 2008·1, 2020·14; C 1973 | 42% |
| 6 | Corporate debt build-up | Credit | FRED `BCNSDODNS / GDP` | ratio ≥ 3 pt above 36 months earlier | 2000·18; C 1973, 1990, 2022 | 30% |
| 7 | Stocks expensive | Markets | Shiller `CAPE` | CAPE > 25 | 2008·23; C 2000, 2020, 2022 | 33% |
| 8 | Profits falling | Real economy | FRED `CP` | YoY < 0 | 1980·5, 1990·10, 2008·7, 2020·17 | 31% |
| 9 | Housing slump | Real economy | FRED `HOUST` | 3-month avg YoY ≤ −20% | 1980·11, 2008·12 | 15% |
| 10 | Factory hours cut | Real economy | FRED `AWHMAN` | ≥ 0.5 h below its 12-month high | 1980·19, 1990·8, 2008·8, 2020·15 | 24% |

\* share of months ON, 1972-01 to 2019-12.

Rules and thresholds are conventional rules of thumb fixed **once**; they are not tuned to make
crises light up. Changing one requires updating the Method page and the reference test.

**Not scored, shown as context on crisis pages:** the Sahm rule (FRED `UNRATE`: 3-month average
≥ 0.5 pt above its 12-month low) as a "recession confirmed here" marker. It fired late in 1973,
1990, 2000 and 2008 — layoffs come after the market and business have already turned.

Each signal has an explainer card: what it is, why it matters (one sentence each), the exact rule,
its false-alarm rate, and its data source link.

## 5. Scoring method

For crisis with peak month `P`, bottom month `B`, previous crisis bottom `Bprev`:

- Window start `W = max(P − 24 months, Bprev + 12 months)` (back-to-back guard; for the first
  crisis, `W = P − 24`).
- **Early (red):** the signal switches ON (off→on) at a month in `[W, P]` **and** is ON at some
  month in `[P − 12, P]`. Lead time = `P −` first such switch-on month.
- **Long on (pink):** ON at some month in `[P − 12, P]` but its current run started before `W`.
- **Late (grey):** none of the above, and first ON in `(P, B]`. Shows months after peak.
- **Did not fire (empty):** otherwise. **n/a** if the series starts after `W`.
- **Verdict** per crisis = the computed count ("5 of 10 signals early") plus a hand-written
  one-sentence lesson in `config/crises.py`. No automatic "Predictable" label: e.g. 2020 scores
  5 early signals from a softening economy, yet the crash itself was an external shock — only
  written context can say that.
- **False-alarm rate:** share of months ON, 1972-01 to 2019-12.

The guard changes some 2022 cells (Covid after-effects). The reference results (section 9) are
regenerated once with the guard, reviewed by the owner, then frozen.

## 6. Pages

**Home** (`index.html`)
1. Headline: "Every crash left warning signs. Could you have seen them coming?" + badge
   "Today: X of 10 lights on →".
2. **Scoreboard** — rows = 7 crises, columns = 10 signals, cells per section 5, "N of 10 early"
   count per row. Click row → crisis page; click column header → signal explainer.
3. The 10 signal explainer cards (grouped by the 5 groups).
4. Crisis cards (name, fall %) and footer (method link, data sources, "not financial advice",
   GitHub link).

**Crisis page** (`crisis/<id>.html`)
1. Header: name, S&P fall, peak→bottom duration, peak unemployment.
2. **Why it happened:** 5-step cause chain (Root → Amplifier → Trigger → Spread → Outcome).
3. **What warned us:** warning-light timeline (section 7).
4. **Signal by signal:** small chart per signal — line, threshold, shaded ON period, peak marker.
5. Verdict + one-sentence lesson + sources list. Prev/next crisis links.

**Lights Today** (`today.html`)
- Disclaimer banner: education only, not financial advice. Last-updated date.
- "X of 10 lights on" vs "before past crashes, at the peak: typically Y–Z of 10" (computed).
- Same timeline component over the last 36 months, "now" marker instead of peak.
- Per-signal "data as of" date; stale or unavailable series shown grey with the reason
  (e.g. CAPE: "no data since 2023-09").

**Method** (`method.html`) — rules, scoring, false-alarm rates, data sources, limitations
(revised data, Shiller staleness, threshold choice, no tuning).

## 7. Visual design

- **Warning-light timeline:** x = months relative to peak (−36 … bottom + 6). Top: S&P 500 monthly
  line with peak marker and NBER recession shading (FRED `USREC`). Below: one row per signal; ON
  periods drawn as rounded bars — red if Early, pink if Long on, grey if after the peak — with the
  lead time written on the bar ("14 mo early"). Sahm marker drawn as a labeled vertical tick.
- **Scoreboard:** cell text always states the value ("14 mo", "long on", "late +5") so meaning
  never depends on color alone. Sticky first column; horizontal scroll on phones.
- Palette: red `#dc2626` early, pink `#fca5a5` long on, grey `#d1d5db` late, `#f3f4f6` empty;
  S&P line blue. Color tokens on `:root` with a dark-mode variant.
- Charts rendered at build time as inline SVG (web/svg.py) — works offline, no JavaScript; hover
  text via SVG <title>. (Changed from client-side Observable Plot during implementation.)
- Plain English everywhere; numbers rounded; jargon defined on first use.

## 8. Architecture

```
macro-pulse-v4/
├─ config/
│  ├─ crises.py       7 crises: dates (+ source URLs), impact stats, cause chain, lesson, sources
│  └─ signals.py      10 signals + Sahm: series ids, rule params, group, explainer text
├─ pipeline/
│  ├─ fetch.py        FRED CSV endpoint (no API key) + Shiller xls → data/raw/*.csv
│  ├─ rules.py        signal → monthly bool Series (pure functions)
│  └─ score.py        cell states, lead times, verdicts, false-alarm rates (pure functions)
├─ web/              (named web/, not site/, to avoid clashing with Python's `site` module)
│  ├─ build.py        writes dist/data/report.json, renders templates → dist/*.html
│  ├─ templates/      base, home, crisis, today, method (Jinja2)
│  ├─ svg.py          timeline + small-multiple charts rendered server-side as inline SVG
│  └─ static/         styles.css (no JavaScript, no CDN)
├─ data/raw/          fetched series, committed
├─ research/validation/   brainstorming validation scripts + outputs (reference only)
├─ tests/
└─ .github/workflows/refresh.yml
```

Data flow: `fetch → rules → score → build → dist/` → GitHub Pages.
Each stage is importable and testable alone; `rules.py` and `score.py` do no I/O.

Runtime: Python 3.12 (server4: conda env `py312`; CI: 3.12). Dependencies: pandas, requests, xlrd,
jinja2, pytest. No API keys.

## 9. Error handling

- `fetch.py` per series: on failure, keep the existing `data/raw` file, log a warning, continue.
  Build never depends on network access.
- Each series records its last observation date; Lights Today marks a series stale when it is older
  than 100 days (monthly) or 200 days (quarterly), measured from the observation date, and excludes it from "X of 10" with a note.
- Shiller CAPE is known stale (ends 2023-09): historical scoring uses it; Lights Today shows it as
  unavailable.
- Build fails loudly (non-zero exit) if a crisis has a missing date, a signal references an unknown
  series, or the reference test fails — so a broken deploy never ships.

## 10. Testing

- **Rules:** unit tests on small synthetic series for each rule (threshold edges, YoY lag,
  rolling windows, quarterly forward-fill).
- **Scoring:** synthetic cases for Early, Long on, Late, Did not fire, n/a, and the back-to-back
  guard.
- **Reference results:** `tests/reference/scoreboard.json` — the frozen 7×10 cell table. A test
  rebuilds it from `data/raw` and fails on any difference. Updating it is a deliberate, reviewed
  commit.
- **Build smoke test:** build into a temp dir; assert every page exists and every crisis/signal id
  appears in the JSON.

## 11. Deployment

`.github/workflows/refresh.yml`: weekly (Monday) and on push to `main` — fetch, test, build,
deploy `dist/` to GitHub Pages; commit updated `data/raw` if changed. Creating the GitHub repo and
enabling Pages is a manual owner step.

## 12. Known limitations (stated on the Method page)

- Revised data, not what was known at the time.
- Thresholds are rules of thumb; different thresholds give different lead times.
- 7 crises is a small sample; hit rates are illustrative, not statistical proof.
- Covid (2020) was an external shock; any "warnings" there reflect a softening economy, not a
  forecast of a pandemic.

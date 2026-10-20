# Validation (brainstorming, 2026-10-19/20)

Throwaway research scripts that checked each candidate signal against real data before the
design was fixed. They produced the "Lit before peak" and false-alarm numbers in
`docs/superpowers/specs/2026-10-20-macro-pulse-design.md`. Not part of the site build;
`pipeline/score.py` will supersede them.

Layout expected by the scripts (pass the folder as the first argument):

    <dir>/fred/<SERIES>.csv        from https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIES>
    <dir>/shiller/ie_data.xls      from http://www.econ.yale.edu/~shiller/data/ie_data.xls (ends 2023-09)

| Script | Purpose |
|---|---|
| `validate.py` | First pass: core 8 rules, loose scoring, credit-spread episodes |
| `validate2.py` | Credit-spread threshold comparison (0.5 / 0.75 / 1.0) under strict scoring |
| `validate_all.py` | Core 8 + 16 candidates × 6 crises, strict scoring, "chronic" category, false-alarm rate, recent drawdowns |
| `validate_all_2022.py` | Same, with 2022 added (no back-to-back guard yet) |
| `plot_spread.py` | `validation-credit-spread.png` |
| `plot_scoreboard.py` | `validation-scoreboard.png` |

"""The 7 crises. Peak/bottom = S&P 500 closing high/low (daily closes).

`dates_checked`: True once the closes were checked against a daily price source
(see `date_source`). The build prints a warning for unchecked crises.
Cause chains and lessons are written content — keep them consistent with the computed
scoreboard (the build does not check prose).
"""

_WIKI_BEARS = "https://en.wikipedia.org/wiki/List_of_stock_market_crashes_and_bear_markets"
_YAHOO = "https://finance.yahoo.com/quote/%5EGSPC/history/"  # daily closes, checked 2026-10-20
_NBER = "https://www.nber.org/research/data/us-business-cycle-expansions-and-contractions"

CRISES = [
    {
        "id": "1973", "name": "1973 Oil crisis & stagflation", "short": "1973 Oil crisis",
        "peak": "1973-01-11", "peak_close": 120.24,
        "bottom": "1974-10-03", "bottom_close": 62.28,
        "dates_checked": True, "date_source": _YAHOO,
        "cause_chain": [
            ("Root cause", "Easy money and the Nixon Shock",
             "In 1971 the US ended the dollar's link to gold. Loose monetary policy and "
             "temporary price controls bottled up inflation."),
            ("Amplifier", "\"Nifty Fifty\" stocks priced for perfection",
             "Investors paid very high prices for a small group of popular growth stocks, "
             "assuming they could only go up."),
            ("Trigger", "Inflation returns, the Fed tightens",
             "The Fed had been raising rates through 1972. The market peaked in January "
             "1973; as price controls were lifted, inflation and rates then climbed fast."),
            ("Spread", "OPEC oil embargo (October 1973)",
             "Arab oil producers cut supplies to the US. OPEC's oil price roughly "
             "quadrupled (US crude about 2½ times), turning a falling market into a crash."),
            ("Outcome", "Stagflation",
             "Prices kept rising while the economy shrank: recession from November 1973 to "
             "March 1975, inflation above 12%."),
        ],
        "notes": "The market peaked nine months before the oil embargo. The famous trigger "
                 "made the crash worse, but it did not start it.",
        "lesson": "Not every crash gives a warning: none of the 10 lights switched on "
                  "before this peak, and the famous oil shock came nine months later.",
        "sources": [_WIKI_BEARS, _NBER, "https://www.federalreservehistory.org/essays/oil-shock-of-1973-74"],
    },
    {
        "id": "1980", "name": "1980–82 Volcker double-dip", "short": "1980 Volcker",
        "peak": "1980-11-28", "peak_close": 140.52,
        "bottom": "1982-08-12", "bottom_close": 102.42,
        "dates_checked": True, "date_source": _YAHOO,
        "cause_chain": [
            ("Root cause", "A decade of high inflation",
             "Inflation had been high since the early 1970s, and people expected it to "
             "stay high."),
            ("Amplifier", "Second oil shock (1979)",
             "The Iranian revolution more than doubled oil prices; consumer inflation peaked "
             "near 15% in 1980."),
            ("Trigger", "Volcker's Fed squeezes inflation out",
             "From October 1979 the Fed under Paul Volcker tightened hard; short-term rates "
             "approached 20%."),
            ("Spread", "Back-to-back recessions",
             "A short recession in 1980 was followed by a deeper one from July 1981 to "
             "November 1982; unemployment passed 10%."),
            ("Outcome", "Inflation broken",
             "Stocks fell about 27%, but inflation was tamed — setting up the long bull "
             "market that began in August 1982."),
        ],
        "notes": "This crash came right after a first recession in early 1980, so some "
                 "lights were still on from that downturn.",
        "lesson": "When the Fed is determined to crush inflation, many warning lights "
                  "flash at once — and they are telling the truth.",
        "sources": [_WIKI_BEARS, _NBER, "https://www.federalreservehistory.org/essays/recession-of-1981-82"],
    },
    {
        "id": "1990", "name": "1990 Gulf War recession", "short": "1990 Gulf War",
        "peak": "1990-07-16", "peak_close": 368.95,
        "bottom": "1990-10-11", "bottom_close": 295.46,
        "dates_checked": True, "date_source": _YAHOO,
        "cause_chain": [
            ("Root cause", "Late-1980s debt boom",
             "Leveraged buyouts, junk bonds and commercial property lending piled up debt; "
             "the savings-and-loan industry collapsed."),
            ("Amplifier", "Fed rate rises (1988–89)",
             "The Fed raised rates to keep inflation near 5% in check, slowing the economy."),
            ("Trigger", "Iraq invades Kuwait (August 1990)",
             "Oil prices nearly doubled within three months."),
            ("Spread", "Credit crunch and gloom",
             "Banks hit by property losses cut lending, and consumer confidence collapsed."),
            ("Outcome", "Short recession",
             "Recession from July 1990 to March 1991; stocks fell about 20%."),
        ],
        "notes": "A fall of 19.9% — just short of the usual −20% bear-market line. The market "
                 "peaked two weeks before the invasion.",
        "lesson": "Debt problems and tighter money had already weakened the economy; the "
                  "oil shock only pushed it over the edge.",
        "sources": [_WIKI_BEARS, _NBER],
    },
    {
        "id": "2000", "name": "2000 Dot-com bust", "short": "2000 Dot-com",
        "peak": "2000-03-24", "peak_close": 1527.46,
        "bottom": "2002-10-09", "bottom_close": 776.76,
        "dates_checked": True, "date_source": _YAHOO,
        "cause_chain": [
            ("Root cause", "Internet euphoria",
             "Investors poured money into technology companies, many of which had never "
             "made a profit."),
            ("Amplifier", "Record valuations",
             "The Shiller CAPE reached about 44, the highest on record; IPOs often doubled "
             "on their first day."),
            ("Trigger", "Rate rises and cash running out",
             "The Fed raised rates from 4.75% to 6.5% in 1999–2000, and young tech firms ran "
             "short of money."),
            ("Spread", "Investment bust, 9/11 and scandals",
             "Companies slashed tech spending; the 2001 attacks and the Enron and WorldCom "
             "accounting scandals deepened the fall."),
            ("Outcome", "Long, deep bear market",
             "The S&P 500 fell about 49% over 2½ years and the Nasdaq about 78%; recession "
             "from March to November 2001."),
        ],
        "notes": "The S&P 500 made an almost equal second high on 1 September 2000 (1520 vs "
                 "1527). This site always uses the highest close.",
        "lesson": "A bubble can be obvious for years — the valuation light was on long "
                  "before — but its timing is not. Rising corporate borrowing and bond "
                  "spreads gave the nearer warning.",
        "sources": [_WIKI_BEARS, _NBER],
    },
    {
        "id": "2008", "name": "2008 Global Financial Crisis", "short": "2008 Financial crisis",
        "peak": "2007-10-09", "peak_close": 1565.15,
        "bottom": "2009-03-09", "bottom_close": 676.53,
        "dates_checked": True, "date_source": _YAHOO,
        "cause_chain": [
            ("Root cause", "Housing bubble",
             "Low rates and loose lending standards (subprime mortgages) pushed home prices "
             "far above incomes."),
            ("Amplifier", "Leverage and complex securities",
             "Mortgages were bundled into securities held worldwide, and banks borrowed "
             "heavily against them."),
            ("Trigger", "Home prices fall",
             "After the Fed raised rates to 5.25% (2004–06), home prices began falling and "
             "subprime defaults surged in 2007."),
            ("Spread", "Bank failures",
             "Bear Stearns was rescued in March 2008; Lehman Brothers collapsed on "
             "15 September 2008 and credit froze worldwide."),
            ("Outcome", "Great Recession",
             "Stocks fell about 57%; recession from December 2007 to June 2009, "
             "unemployment reached 10%."),
        ],
        "notes": "The trouble started in mortgage credit, so corporate bond spreads stayed "
                 "calm until just before the peak.",
        "lesson": "Housing gave the clearest warning — the stress showed up where the "
                  "borrowing was. Home building had collapsed and the yield curve had "
                  "inverted more than a year before the peak.",
        "sources": [_WIKI_BEARS, _NBER, "https://www.federalreservehistory.org/essays/great-recession-of-200709"],
    },
    {
        "id": "2020", "name": "2020 Covid crash", "short": "2020 Covid",
        "peak": "2020-02-19", "peak_close": 3386.15,
        "bottom": "2020-03-23", "bottom_close": 2237.40,
        "dates_checked": True, "date_source": "https://fred.stlouisfed.org/series/SP500",
        "cause_chain": [
            ("Root cause", "Late-cycle economy",
             "After a decade-long expansion, corporate debt was at record levels."),
            ("Amplifier", "2019 slowdown",
             "A trade war and a manufacturing slowdown; the yield curve inverted in 2019."),
            ("Trigger", "Covid-19 pandemic",
             "Lockdowns in March 2020 shut large parts of the economy almost overnight."),
            ("Spread", "Fastest crash on record",
             "Stocks fell 34% in about a month; unemployment jumped to nearly 15% in "
             "April 2020."),
            ("Outcome", "Rapid rescue and rebound",
             "Rates were cut to zero and huge stimulus followed; the market regained its "
             "high by August 2020. Recession February–April 2020."),
        ],
        "notes": "An outside shock. Lights that were on reflect a softening economy, not a "
                 "forecast of a pandemic.",
        "lesson": "Some crashes come from outside the economy; warning lights can show "
                  "fragility, but not the shock itself.",
        "sources": [_NBER, "https://fred.stlouisfed.org/series/SP500"],
    },
    {
        "id": "2022", "name": "2022 Inflation & rate shock", "short": "2022 Rate shock",
        "peak": "2022-01-03", "peak_close": 4796.56,
        "bottom": "2022-10-12", "bottom_close": 3577.03,
        "dates_checked": True, "date_source": "https://fred.stlouisfed.org/series/SP500",
        "cause_chain": [
            ("Root cause", "Pandemic stimulus and zero rates",
             "Money supply (M2) grew about 40% in 2020–21 while rates stayed near zero."),
            ("Amplifier", "Supply shocks",
             "Supply-chain bottlenecks, then Russia's invasion of Ukraine in February 2022, "
             "pushed up energy and food prices."),
            ("Trigger", "Inflation and the fastest rate rises in decades",
             "Inflation hit 9.1% in June 2022; the Fed raised rates from near zero to over "
             "4% within the year."),
            ("Spread", "Expensive stocks hit hardest",
             "High-valuation technology and growth stocks fell most; the Nasdaq lost about a "
             "third in 2022."),
            ("Outcome", "Bear market without a recession",
             "The S&P 500 fell about 25%; the economy kept growing and no recession was "
             "declared."),
        ],
        "notes": "This crash came less than two years after the 2020 crash, so lights still "
                 "reacting to Covid are not counted as warnings (see Method).",
        "lesson": "Inflation and a fast-hiking Fed can sink the market even when the economy "
                  "holds up.",
        "sources": [_NBER, "https://fred.stlouisfed.org/series/SP500", "https://fred.stlouisfed.org/series/M2SL"],
    },
]

CRISIS_IDS = [c["id"] for c in CRISES]

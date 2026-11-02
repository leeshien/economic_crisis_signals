"""Facts for the 2020 Covid crash comic. Each item: the words on the page + where it was checked.

Computed figures (jobs, claims, unemployment, debt, index moves) were calculated from the named FRED /
Yahoo series on 2026-10-21; chart data is saved in comics/data/covid_series.json and the country falls
in comics/data/covid_falls.json. FRED figures are the current (revised) vintage, so a few differ
slightly from the first headlines in 2020 (e.g. April unemployment 14.8%, first reported as 14.7%).
"""
import json
from pathlib import Path

FRED = "https://fred.stlouisfed.org/series/"
DATA = Path(__file__).resolve().parent / "data"
FALLS = json.loads((DATA / "covid_falls.json").read_text(encoding="utf-8"))
SERIES = json.loads((DATA / "covid_series.json").read_text(encoding="utf-8"))

SLUG = "2020-covid"
CRISIS_ID = "2020"
ORDER = ["cover", "machine", "good-times", "boom-to-danger", "warning-signs", "timeline-up", "timeline-down",
         "what-popped", "map", "fixing-rules", "lesson", "sources"]

# ---- page 2: the sudden stop -----------------------------------------------------------------

MACHINE = [  # (station, what happens, icon)
    ("A NEW VIRUS SPREADS", "Covid-19 was first found in Wuhan, China, in December 2019. Within three months it "
                            "had reached every continent except Antarctica.", "globe_virus"),
    ("THE WORLD SHUTS ITS DOORS", "To slow it, governments closed shops, offices, schools and borders. By 2 April "
                                  "2020, 3.9 billion people, half the world, were told to stay home.", "lockdown"),
    ("PAYCHECKS STOP", "No customers means no wages. In March and April 2020, 21.9 million Americans lost their jobs.",
     "jobs_lost"),
    ("SPENDING STOPS", "One person's spending is another person's paycheck. US shop sales fell 22% in two months, "
                       "so more firms cut more jobs.", "cart_x"),
    ("A DASH FOR CASH", "Firms and investors sold anything they could, even \"safe\" US government bonds, to get cash. "
                        "Markets everywhere fell at once.", "cash_dash"),
]
MACHINE_STATS = {
    "claims": ("New US claims for jobless benefits each week", FRED + "ICSA"),
    "unrate": (3.5, 14.8, "Unemployment: 3.5% (Feb 2020) to 14.8% (Apr 2020), the highest since records began in 1948.",
               FRED + "UNRATE"),
}
MACHINE_SOURCES = ["https://www.euronews.com/2020/04/02/coronavirus-in-europe-spain-s-death-toll-hits-10-000-after-record-950-new-deaths-in-24-hou",
                   FRED + "PAYEMS", FRED + "RSAFS",
                   "https://www.newyorkfed.org/research/epr/2023/epr_2023_dash-for-cash_barone"]
JARGON_MACHINE = [
    ("Pandemic", "A disease spreading across the whole world at the same time.", "globe_virus"),
    ("Lockdown", "Orders to stay at home and close places where people gather.", "lockdown"),
    ("Recession", "When a country's economy shrinks and jobs are lost. 2020's lasted just 2 months (Feb–Apr).", "recession"),
    ("Dash for cash", "Everyone selling at once, even safe things, because they need money right now.", "cash_dash"),
]

# ---- page 3: the good times ------------------------------------------------------------------

GOOD_TIMES = [  # (big number, headline, explanation, icon, source)
    ("+400%", "Shares at a record", "From its 2009 low, the S&P 500 rose 400% to a record 3,386.15 on 19 February 2020.",
     "chart_up", "https://finance.yahoo.com/quote/%5EGSPC/history/"),
    ("3.5%", "Jobs for almost everyone",
     "In February 2020, only 3.5% of Americans who wanted a job could not find one: the lowest since 1969.",
     "worker", FRED + "UNRATE"),
    ("128", "The longest boom ever",
     "The US economy had grown for 128 months in a row, since June 2009: the longest run on record.",
     "calendar", "https://www.nber.org/research/data/us-business-cycle-expansions-and-contractions"),
    ("DEAL", "Trade war calming",
     "On 15 January 2020 the US and China signed a \"phase one\" deal to cool their two-year trade war.",
     "trade_deal", "https://ustr.gov/countries-regions/china-mongolia-taiwan/peoples-republic-china/phase-one-trade-agreement"),
    ("1.75%", "Cheap money",
     "The Fed cut interest rates three times in 2019, to 1.5–1.75%, to keep the boom going.",
     "rate_down", FRED + "DFEDTARU"),
    ("101", "Shoppers felt great",
     "US consumer confidence hit 101.0 in February 2020, close to its best level in 16 years.",
     "piggy", FRED + "UMCSENT"),
]

# ---- page 4: hidden weak spots ---------------------------------------------------------------

DANGER_STEPS = [  # (date, title, text, icon, source)
    ("END OF 2019", "Companies borrowed a record",
     "US companies (not counting banks) owed $11.2 trillion: 51% of the whole economy, the highest share on record.",
     "leverage", FRED + "BCNSDODNS"),
    ("2019", "One step above junk",
     "About half of all \"investment grade\" company bonds were rated BBB, the lowest safe grade. In 2001 it was 17%.",
     "bbb_stamp", "https://www.everycrsreport.com/reports/IN11275.html"),
    ("2018", "Cash spent on their own shares",
     "S&P 500 companies spent a record $806 billion buying back their own shares, cash that was not kept for a rainy day.",
     "buyback", "https://spglobal.com/spdji/en/documents/index-news-and-announcements/20190325-sp-500-buybacks-2018-q4-pr.pdf"),
    ("17 SEP 2019", "A cash-crunch warning",
     "Banks suddenly ran short of overnight cash and some short-term loan rates hit 10%. The Fed pumped in $75 billion a day.",
     "frozen", "https://en.wikipedia.org/wiki/September_2019_events_in_the_U.S._repo_market"),
    ("37%", "No cushion for a rainy day",
     "In 2019, 37% of American adults could not pay a surprise $400 bill from cash or savings. If paychecks stopped, "
     "they were in trouble within weeks.",
     "wallet_empty", "https://www.federalreserve.gov/consumerscommunities/sheddataviz/unexpectedexpenses-table.html"),
    ("CAPE 31", "Shares were pricey",
     "In January 2020, shares cost 31 times their average yearly profits of the past 10 years (the \"CAPE\" ratio). The "
     "long-run average is 18. Shares had cost this much only around 1929, 2000 and briefly in 2018.",
     "gauge", "http://www.econ.yale.edu/~shiller/data.htm"),
]
JARGON_DANGER = [
    ("Company bond", "An IOU a company sells to investors to borrow money. It pays interest, then repays.", "bundle"),
    ("Junk bond", "A bond rated below BBB: riskier, so it must pay more interest.", "bbb_stamp"),
    ("Share buyback", "A company buying its own shares from the market, which can lift the share price.", "buyback"),
    ("CAPE ratio", "Share price divided by 10 years of average profits. High = shares are expensive.", "gauge"),
]

# ---- page 5: warning signs -------------------------------------------------------------------

WARNING = {"stock_peak": "2020-02", "hours_peak": ("2018-04", 42.4), "hours_low": ("2020-01", 41.3)}
WARNING_SOURCES = [FRED + "T10Y3M", FRED + "AWHMAN"]

# ---- pages 6-7: timeline (date, title, text, mood, icon[, stamp]) ----------------------------

TIMELINE_TEXT = {
    "up_title": "TIMELINE PART 1: UP, UP...", "up_intro": "Read from the bottom up. Green = good news, red = trouble, "
                                                          "blue = a warning or a rescue. Red stamp = the crash.",
    "down_title": "PART 2: ...AND DOWN!", "down_intro": "Read from the bottom up. The whole crash took just 33 days: "
                                                        "19 Feb to 23 Mar 2020 (red stamps).",
}
TIMELINE_UP = [
    ("31 JUL 2019", "Fed cuts rates", "The first cut since 2008, to protect the economy from the trade war.", "neutral", "rate_down"),
    ("17 SEP 2019", "Cash crunch", "Short-term loan rates spike to 10%. The Fed pumps in cash.", "neutral", "frozen"),
    ("31 DEC 2019", "Mystery illness", "China reports a cluster of pneumonia cases in Wuhan.", "neutral", "virus"),
    ("15 JAN 2020", "Trade deal signed", "The US and China sign a \"phase one\" deal. Shares keep rising.", "up", "trade_deal"),
    ("21 JAN 2020", "First US case", "A traveller back from Wuhan tests positive in Washington state.", "down", "virus"),
    ("23 JAN 2020", "Wuhan locked down", "China seals off a city of 11 million people.", "down", "lockdown"),
    ("30 JAN 2020", "Global emergency", "The World Health Organization declares a global health emergency.", "down", "siren"),
    ("19 FEB 2020", "THE PEAK", "S&P 500 closes at a record 3,386.15. Unemployment is just 3.5%.", "down", "peak_flag", "CRASH STARTS"),
    ("24 FEB 2020", "Italy shuts towns", "Europe's first big outbreak: 11 towns sealed off. S&P 500 −3.4%.", "down", "globe_virus"),
]
TIMELINE_DOWN = [
    ("3 MAR 2020", "Emergency rate cut", "The Fed cuts by 0.5% without waiting for its meeting: the first time since 2008.", "neutral", "rate_down"),
    ("9 MAR 2020", "Oil price war", "Saudi Arabia and Russia fall out: US oil −25%. S&P 500 −7.6%, trading halted.", "down", "oil_barrel"),
    ("11 MAR 2020", "A pandemic", "The WHO says Covid-19 is now a pandemic.", "down", "globe_virus"),
    ("12 MAR 2020", "Fastest fall ever", "S&P 500 −9.5%. It is now 20% below its peak after only 16 trading days.", "down", "chart_down"),
    ("15 MAR 2020", "Rates cut to zero", "The Fed cuts to 0–0.25% and starts buying $700 billion of bonds.", "neutral", "rate_zero"),
    ("16 MAR 2020", "Worst day since 1987", "S&P 500 −12.0%. Wall Street's \"fear gauge\" (VIX) hits a record 82.69.", "down", "circuit_breaker", "THE CRASH"),
    ("23 MAR 2020", "THE BOTTOM", "S&P 500 2,237.40 (−34%). The Fed promises to buy bonds \"in the amounts needed\".", "up", "floor_hit", "CRASH ENDS"),
    ("27 MAR 2020", "$2.2 trillion rescue", "The CARES Act: $1,200 cheques, extra jobless pay, loans to small firms.", "neutral", "signed_law"),
    ("20 APR 2020", "Oil below zero", "So little demand that US oil sellers paid buyers $37 a barrel to take it.", "down", "oil_negative"),
    ("18 AUG 2020", "Back to a record", "The S&P 500 closes at 3,389.78: a new high just 6 months after the peak.", "up", "chart_up"),
]

# ---- page 8: what popped it ------------------------------------------------------------------

PINS_TEXT = {
    "intro": "An 11-year boom met six pins at once. Most came from outside the economy:",
    "balloon": "BOOM",
    "balloon_art": "bubble_boom",
    "bear": "Our warning lights were already showing a tired economy. But no light could have seen a virus coming.",
}
PINS = [  # (title, text, icon)
    ("The virus", "A new disease spread around the world in weeks. Nobody knew how bad it would get.", "virus"),
    ("Lockdowns", "Shops, offices, flights and factories closed by order, all at the same time.", "lockdown"),
    ("Jobs vanished", "6 million new jobless claims in one week: more than 8 times the old record from 1982.", "jobless_queue"),
    ("Oil price war", "Oil fell 25% in one day (9 Mar), then below zero in April. Energy firms with big debts were hit hard.", "oil_barrel"),
    ("Debt-heavy firms", "With sales gone, firms that owed a lot could not pay. Lenders demanded twice as much extra interest.", "bbb_stamp"),
    ("Dash for cash", "Even US government bonds, the world's \"safest\" asset, were dumped to raise cash.", "safe_bonds_sold"),
]
PINS_SOURCES = [FRED + "ICSA", FRED + "DCOILWTICO", FRED + "BAA10Y", FRED + "DGS10",
                "https://www.spglobal.com/en/research-insights/articles/oil-prices-plunge-in-response-to-the-collapse-of-the-opec-alliance"]

# ---- page 9: map -----------------------------------------------------------------------------

MAP_TEXT = {
    "intro": "The virus went everywhere, so did the crash. Each country is shaded by how far its main stock index fell from "
             "its high (Dec 2019 to Feb 2020) to its low in 2020. Almost every market bottomed in the same week of March.",
    "bear": "Every market fell at once.",
    "penny": "Why did China fall least?",
    "bear2": "The virus began there, so China locked down first and reopened first: factories restarted in March.",
    "burst": ("CHINA", "−15%", (88, 60), (104, 34)),
    "foot": ["Local-currency index closes, Yahoo Finance. Grey = no daily data for 2020 (monthly averages would hide a one-month crash). "
             "Map: Natural Earth.",
             "Argentina's index is in pesos, which were also losing value fast."],
}

MAP_BUCKETS = [(-45, "#9b1c1c", "45% or more"), (-40, "#e63b2e", "40–45%"), (-35, "#f78c2e", "35–40%"),
               (-30, "#ffd23f", "30–35%"), (-100, "#fff1a8", "less than 30%")]

# ---- page 10: the rescue ---------------------------------------------------------------------

POLICY_TEXT = {
    "title": "THE GREAT RESCUE",
    "intro": "This time governments and central banks moved in days, not years, and spent more than ever before. The "
             "aim: keep people paid and firms alive until the virus passed.",
    "bear": "It worked fast: shares were back at a record by August. But all that new money helped push prices up in "
            "2021–22. America's money supply grew almost 40% in under two years.",
    "penny": "Can a cure have side effects?",
}
POLICIES = [  # (flag, country, law, date, what it did, source)
    ("US", "United States", "Rates to zero + bond buying", "15 MAR 2020",
     "The Fed cut rates to 0–0.25% and bought bonds. Its balance sheet grew from $4.2 to $7.4 trillion in 2020.",
     "https://www.federalreserve.gov/newsevents/pressreleases/monetary20200315a.htm"),
    ("US", "United States", "Fed buys company bonds", "23 MAR 2020",
     "For the first time ever, the Fed offered to buy company bonds, so firms could still borrow.",
     "https://www.federalreserve.gov/newsevents/pressreleases/monetary20200323b.htm"),
    ("US", "United States", "CARES Act", "27 MAR 2020",
     "$2.2 trillion: $1,200 cheques per adult, $600 a week extra jobless pay, and loans to keep small firms' staff paid.",
     "https://www.congress.gov/bill/116th-congress/house-bill/748"),
    ("FED", "Worldwide", "Dollar swap lines", "19 MAR 2020",
     "The Fed lent US dollars to 9 more central banks, from Brazil to Korea, so the world did not run short of dollars.",
     "https://www.federalreserve.gov/newsevents/pressreleases/monetary20200319b.htm"),
    ("EU", "Euro area", "ECB emergency buying (PEPP)", "18 MAR 2020",
     "The European Central Bank set aside €750 billion to buy bonds, later raised to €1.85 trillion.",
     "https://www.ecb.europa.eu/press/pr/date/2020/html/ecb.pr200318_1~3949d6f266.en.html"),
    ("UK", "United Kingdom", "Furlough scheme", "20 MAR 2020",
     "The government paid 80% of wages, up to £2,500 a month, for workers firms could not use.",
     "https://en.wikipedia.org/wiki/Coronavirus_Job_Retention_Scheme"),
    ("JP", "Japan", "¥108 trillion package", "7 APR 2020",
     "Japan's biggest-ever rescue, later including ¥100,000 (about $930) for every resident.",
     "https://www.aljazeera.com/economy/2020/4/7/japans-abe-unveils-massive-1-trillion-coronavirus-aid-package"),
    ("EU", "European Union", "NextGenerationEU", "21 JUL 2020",
     "€750 billion recovery fund. For the first time, the EU itself borrowed on the markets for its members.",
     "https://commission.europa.eu/news-and-media/news/eu-leaders-agreed-182-trillion-budget-next-seven-years-2020-07-21_en"),
    ("US", "United States", "American Rescue Plan", "11 MAR 2021",
     "$1.9 trillion more, with $1,400 cheques, signed when the economy was already recovering.",
     "https://www.congress.gov/bill/117th-congress/house-bill/1319"),
]

# ---- page 11: what our lights said -----------------------------------------------------------

LIGHTS_TEXT = {
    "intro": "The same 10 rules we use for every crash, applied to the months before the February 2020 peak.",
    "summary": "4 of 10 lights warned early: the yield curve, credit spreads, falling profits and shorter factory hours "
               "all said the economy was getting tired, and stocks had been expensive for years. But they were warning "
               "of a slowdown, not a pandemic.",
    "penny": "So the lights can't predict a virus?",
    "bear": "No. But they told us the economy had little room to absorb a shock.",
    "next": "2022 INFLATION SHOCK",
}

# ---- page 12: sources ------------------------------------------------------------------------

SOURCE_NOTE = ("Every number in this comic was checked against the sources below on 21 October 2026. Index falls use the highest "
               "close from December 2019 to February 2020 and the lowest close after it up to December 2020, in local currency. "
               "Jobs, claims, rates, debt and spending: official US data (BLS, Census, BEA, Federal Reserve) via FRED, current "
               "revised figures. Characters are fictional. For education only, not investment advice.")
EXTRA_SOURCES = [
    "https://www.who.int/news/item/27-04-2020-who-timeline---covid-19 (WHO timeline)",
    "https://archive.cdc.gov/www_cdc_gov/media/releases/2020/p0121-novel-coronavirus-travel-case.html",
    "https://www.federalreserve.gov/newsevents/pressreleases/monetary20200303a.htm (emergency cut)",
    "https://fortune.com/2020/03/09/market-wide-stock-trading-halts-after-sp-500-plunges-7-stock-market-crash",
    "https://www.federalreserve.gov/newsevents/pressreleases/monetary20200323a.htm (\"amounts needed\")",
    FRED + "VIXCLS · " + FRED + "WALCL · " + FRED + "M2SL",
    "https://www.nber.org/research/data/us-business-cycle-expansions-and-contractions",
    "https://finance.yahoo.com/ (daily index closes) · https://www.naturalearthdata.com/ (map outlines)",
]


def source_groups(page_no):
    return [
        (f"The sudden stop (page {page_no('machine')})", MACHINE_SOURCES + [v[-1] for v in MACHINE_STATS.values()]),
        (f"The good times (page {page_no('good-times')})", [g[4] for g in GOOD_TIMES]),
        (f"Hidden weak spots (page {page_no('boom-to-danger')})", [b[4] for b in DANGER_STEPS]),
        (f"Warning signs and what popped it (pages {page_no('warning-signs')}, {page_no('what-popped')})", WARNING_SOURCES + PINS_SOURCES),
        (f"The great rescue (page {page_no('fixing-rules')})", [p[5] for p in POLICIES]),
        ("Timeline and data", EXTRA_SOURCES),
    ]


SOURCE_GROUPS = source_groups(lambda name: ORDER.index(name) + 1)

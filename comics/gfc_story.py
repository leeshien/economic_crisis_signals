"""Facts for the 2008 Global Financial Crisis comic. Each item: the words on the page + where it was checked.

Computed figures (home prices, jobs, mortgage debt, net worth, delinquencies, index moves) were calculated
from the named FRED / Yahoo series on 2026-10-21; chart data is saved in comics/data/gfc_series.json and
the country falls in comics/data/gfc_falls.json.
"""
import json
from pathlib import Path

FRED = "https://fred.stlouisfed.org/series/"
DATA = Path(__file__).resolve().parent / "data"
FALLS = json.loads((DATA / "gfc_falls.json").read_text(encoding="utf-8"))
SERIES = json.loads((DATA / "gfc_series.json").read_text(encoding="utf-8"))

SLUG = "2008-gfc"
CRISIS_ID = "2008"
ORDER = ["cover", "machine", "good-times", "boom-to-danger", "warning-signs", "timeline-up", "timeline-down",
         "what-popped", "map", "fixing-rules", "lesson", "sources"]

# ---- page 2: the mortgage machine ------------------------------------------------------------

MACHINE = [  # (station, what happens, icon)
    ("A FAMILY BORROWS", "A family takes out a mortgage: a loan to buy a home, paid back over about 30 years.", "mortgage"),
    ("THE LENDER SELLS THE LOAN", "The old way: the bank kept your loan, so it checked you could pay. The new way: "
                                  "sell the loan on within weeks. If it goes bad, it's someone else's problem.", "handshake_sell"),
    ("WALL STREET BUNDLES IT", "Investment banks pack thousands of mortgages into one bond, then slice it into "
                               "layers. Families' monthly payments flow to the bond's owners.", "bundle"),
    ("RATED \"AAA\"", "Rating agencies stamped most layers AAA: as safe as it gets. Their fees were paid by the "
                      "banks selling the bonds.", "aaa_stamp"),
    ("SOLD WORLDWIDE", "Pension funds, insurers and banks everywhere bought them, even eight small towns in "
                       "Norway, which lost tens of millions of dollars.", "globe_arrows"),
]
MACHINE_STATS = {
    "subprime": (5, 20, "Subprime share of new US mortgages: 5% in 2001, over 20% in 2006.",
                 "https://archive.fdic.gov/view/fdic/915/fdic_915_DS1.pdf"),
    "debt": (4.5, 10.6, "US home-mortgage debt: $4.5 trillion (2000) to $10.6 trillion (2008).", FRED + "HHMSDODNS"),
}
MACHINE_SOURCES = ["https://www.federalreservehistory.org/essays/subprime-mortgage-crisis",
                   "https://en.wikipedia.org/wiki/Terra_Securities_scandal",
                   "https://www.bondbuyer.com/news/norwegian-cities-left-in-the-cold"]
JARGON_MACHINE = [
    ("Mortgage", "A loan to buy a home. If you stop paying, the lender can take the house.", "mortgage"),
    ("Subprime", "A loan to someone with a weak credit record or low income: riskier, so it charges more.", "liar_loan"),
    ("Mortgage bond", "Thousands of mortgages bundled together and sold to investors (an \"MBS\").", "bundle"),
    ("AAA", "The top safety grade a rating agency can give. It means \"almost no chance of loss\".", "aaa_stamp"),
]

# ---- page 3: the good times ------------------------------------------------------------------

GOOD_TIMES = [  # (big number, headline, explanation, icon, source)
    ("+85%", "Home prices kept climbing",
     "US home prices rose 85% from January 2000 to their peak in July 2006.",
     "house_up", FRED + "CSUSHPINSA"),
    ("69.2%", "Record home ownership",
     "In 2004, 69.2% of US households owned their home, the highest ever recorded.",
     "house_record", FRED + "RHORUSQ156N"),
    ("4.4%", "Plenty of jobs",
     "Unemployment fell to 4.4% in late 2006 and stayed low into 2007.",
     "worker", FRED + "UNRATE"),
    ("$70.7tn", "Families felt rich",
     "US household wealth hit a record $70.7 trillion in mid-2007, much of it in rising house values.",
     "net_worth", FRED + "TNWBSHNO"),
    ("CALM", "\"The Great Moderation\"",
     "Since the mid-1980s, growth and inflation had been unusually steady. Fed governor Ben Bernanke gave it that name in 2004.",
     "calm_sea", "https://www.federalreserve.gov/boarddocs/speeches/2004/20040220/"),
    ("14,164", "Shares hit a record",
     "The Dow Jones index closed at a record 14,164.53 on 9 October 2007.",
     "chart_up", "https://finance.yahoo.com/quote/%5EDJI/history/"),
]

# ---- page 4: from boom to danger -------------------------------------------------------------

DANGER_STEPS = [  # (date, title, text, icon, source)
    ("2003", "Money on sale",
     "The Fed cut its rate to 1%, the lowest since 1958. 30-year mortgage rates fell to 5.2%, the lowest on record.",
     "rate_down", FRED + "MORTGAGE30US"),
    ("2004–06", "Loans for almost anyone",
     "Some lenders stopped checking incomes at all. Bankers nicknamed these \"liar loans\".",
     "liar_loan", "https://www.federalreservehistory.org/essays/subprime-mortgage-crisis"),
    ("TEASERS", "Cheap now, dear later",
     "Many subprime loans started with a low \"teaser\" rate for 2 years, then jumped. Borrowers hoped to refinance before then.",
     "teaser", "https://www.federalreservehistory.org/essays/subprime-mortgage-crisis"),
    ("2005", "Buying to flip",
     "28% of all US homes bought in 2005 were investments, not homes to live in. Many buyers planned to sell quickly at a profit.",
     "flip_house", "https://inman.com/2006/04/05/second-home-sales-account-40-residential-market"),
    ("30 TO 1", "Banks borrowed to the hilt",
     "At the end of 2007, investment bank Lehman Brothers held $691 billion of assets on only $22.5 billion of its own "
     "money: 30.7 times over. A fall of just over 3% in what it owned would wipe out all of its own money.",
     "leverage", "https://www.sec.gov/Archives/edgar/data/0000806085/000110465907088588/a07-30473_33ex99d1.htm"),
    ("$513BN", "Insurance with no money behind it",
     "AIG, a giant US insurer, had sold $513 billion of \"credit default swaps\": insurance that bonds "
     "would be repaid. It set little money aside to pay claims. When the claims came in 2008, it needed an $85 "
     "billion rescue from the Fed.",
     "umbrella_holes", "https://www.sec.gov/Archives/edgar/data/0000005272/000095012307015058/y38903e10vq.htm"),
]
JARGON_DANGER = [
    ("Leverage", "Using borrowed money to bet bigger. Gains grow faster, but so do losses.", "leverage"),
    ("Credit default swap", "An insurance policy that pays out if a borrower can't repay a bond.", "umbrella_holes"),
]

# ---- page 5: warning signs -------------------------------------------------------------------

WARNING = {
    "starts_peak": ("2006-01", 2273), "starts_low": ("2009-04", 478),
    "price_peak": ("2006-07", 184.61), "price_low": ("2012-02", 133.99),
    "stock_peak": "2007-10",
}
WARNING_SOURCES = [FRED + "HOUST", FRED + "T10Y3M", FRED + "DRSFRMACBS"]

# ---- pages 6-7: timeline (date, title, text, mood, icon[, stamp]) ----------------------------

TIMELINE_TEXT = {
    "up_title": "TIMELINE PART 1: UP, UP...", "up_intro": "Read from the bottom up. Green = good news, red = trouble, "
                                                          "blue = a warning or a rescue. Red stamp = the crash.",
    "down_title": "PART 2: ...AND DOWN!", "down_intro": "Read from the bottom up. The crash: 9 Oct 2007 to 9 Mar 2009 "
                                                        "(red stamps). The worst weeks came after Lehman fell.",
}
TIMELINE_UP = [
    ("25 JUN 2003", "Rates cut to 1%", "The lowest since 1958. Borrowing to buy a home has never been cheaper.", "up", "rate_down"),
    ("2004", "Home ownership record", "69.2% of US households own their home.", "up", "house_record"),
    ("30 JUN 2004", "Fed starts raising rates", "17 rises in a row take rates from 1% to 5.25% by June 2006.", "neutral", "rate_up"),
    ("JUL 2006", "Home prices peak", "After rising 85% since 2000, US home prices start to slide.", "down", "house_down"),
    ("2 APR 2007", "New Century goes bust", "A top subprime lender fails as borrowers stop paying.", "down", "bankrupt"),
    ("9 AUG 2007", "BNP Paribas freezes funds", "A French bank can't value its US mortgage bonds: \"a complete evaporation of liquidity\".", "down", "frozen"),
    ("14 SEP 2007", "Run on Northern Rock", "A British lender needs emergency help. Savers queue to take their money out.", "down", "bank_run"),
    ("18 SEP 2007", "Fed starts cutting", "Rates cut from 5.25% to 4.75%. Shares rally.", "neutral", "rate_down"),
    ("9 OCT 2007", "THE PEAK", "S&P 500 closes at 1,565.15; the Dow at a record 14,164.53.", "down", "peak_flag", "CRASH STARTS"),
]
TIMELINE_DOWN = [
    ("11 JAN 2008", "Countrywide rescued", "Bank of America buys the biggest US mortgage lender for about $4 billion.", "neutral", "big_fish"),
    ("16 MAR 2008", "Bear Stearns sold for $2", "A Wall Street bank is sold to JPMorgan for $2 a share (later $10), backed by the Fed.", "down", "bear_sold"),
    ("7 SEP 2008", "Fannie & Freddie taken over", "The government seizes the two giants behind half of US mortgages.", "neutral", "lifebuoy"),
    ("15 SEP 2008", "Lehman Brothers fails", "$639 billion of assets: the biggest bankruptcy in US history. S&P 500 −4.7%.", "down", "bank_cracked", "THE CRASH"),
    ("16 SEP 2008", "AIG rescued", "The Fed lends $85 billion and takes 79.9% of the insurer.", "neutral", "umbrella_holes"),
    ("29 SEP 2008", "Congress says no", "The House rejects a $700 billion bank rescue: S&P 500 −8.8% in a day.", "down", "vote_no"),
    ("3 OCT 2008", "Rescue law signed", "A revised $700 billion rescue fund (TARP) becomes law.", "neutral", "signed_law"),
    ("6–9 OCT 2008", "Iceland's banks collapse", "All three big banks fail; together they were about 10 times Iceland's economy.", "down", "iceland"),
    ("16 DEC 2008", "Rates cut to zero", "The Fed's rate goes to 0–0.25%. Recession: Dec 2007–Jun 2009.", "neutral", "rate_zero"),
    ("9 MAR 2009", "THE BOTTOM", "S&P 500 676.53 (−57%). Dow 6,547.05 (−54%).", "up", "floor_hit", "CRASH ENDS"),
]

# ---- page 8: what popped it ------------------------------------------------------------------

PINS_TEXT = {
    "intro": "Six pins pressed into the housing bubble. Each made the next one worse:",
    "balloon": "HOUSING",
    "balloon_art": "bubble_subprime",
    "bear": "Our warning lights: home building and the yield curve flashed a year or more before the stock peak. "
            "Credit spreads only switched on one month before.",
}
PINS = [  # (title, text, icon)
    ("Dearer money", "The Fed raised rates 17 times, from 1% to 5.25% (2004–06). Loan payments rose.", "rate_up"),
    ("Teasers ran out", "Cheap starter rates reset higher. Monthly payments jumped for millions of families.", "teaser"),
    ("Prices fell", "Home prices fell 27% from July 2006 to early 2012. Many owed more than their home was worth.", "house_down"),
    ("People stopped paying", "Late mortgage payments rose from 1.4% (2004) to 11.5% (2010) of home loans at banks.", "for_sale"),
    ("Borrowed money", "Banks borrowing 30 times their own money could not survive even small losses.", "leverage"),
    ("Trust froze", "Nobody knew which bank held the bad loans, so banks stopped lending to each other.", "frozen"),
]
PINS_SOURCES = [FRED + "FEDFUNDS", FRED + "CSUSHPINSA", FRED + "DRSFRMACBS", FRED + "TEDRATE"]

# ---- page 9: map -----------------------------------------------------------------------------

MAP_TEXT = {
    "intro": "Bad US mortgages were owned all over the world, so the crash went global. Each country is shaded by how far its "
             "main stock index fell from its 2007–08 high to its low by the end of 2009.",
    "bear": "Banks everywhere owned US mortgage bonds.",
    "penny": "Iceland fell 95%?! How?",
    "bear2": "Its three banks had grown to about 10 times the size of its whole economy. When they failed, so did its market.",
    "burst": ("ICELAND", "−95%", (-40, 50), (-19, 64.8)),
    "foot": ["Local-currency index closes, Yahoo Finance; ‡ = OECD monthly average share prices (FRED), which hide the worst days. "
             "Map: Natural Earth.",
             "† China's market had its own bubble in 2006–07; it peaked on 16 Oct 2007 and fell 72%."],
}
for _m in FALLS["markets"]:
    if _m["a3"] == "CHN":
        _m["note"] = "own bubble in 2006-07"

# ---- page 10: fixing the rules ---------------------------------------------------------------

POLICY_TEXT = {
    "intro": "Governments spent the next ten years rewriting the rules so that banks hold more of their own money and "
             "taxpayers do not have to rescue them again.",
    "bear": "Banks now must hold far more of their own money and pass a yearly \"stress test\". Their rescues are now "
            "planned in advance, so that their owners lose first, not taxpayers.",
    "penny": "So could it happen again?",
}
POLICIES = [  # (flag, country, law, date, what it did, source)
    ("US", "United States", "Dodd-Frank Act", "21 JUL 2010",
     "Yearly stress tests for big banks, a council to spot system-wide risks, and a way to close a failing giant without a bailout.",
     "https://www.congress.gov/bill/111th-congress/house-bill/4173"),
    ("US", "United States", "Consumer Financial Protection Bureau", "21 JUL 2011",
     "A new watchdog for mortgages, credit cards and other loans to families.",
     "https://www.consumerfinance.gov/about-us/the-bureau/"),
    ("US", "United States", "\"Ability to repay\" rule", "10 JAN 2014",
     "Lenders must check that a borrower can afford the loan. No more \"liar loans\".",
     "https://www.consumerfinance.gov/rules-policy/final-rules/ability-to-repay-and-qualified-mortgage-standards-under-the-truth-in-lending-act-regulation-z/"),
    ("BASEL", "Worldwide", "Basel III bank rules", "16 DEC 2010",
     "Banks must hold more of their own money, keep cash for emergencies and limit how much they borrow.",
     "https://www.bis.org/press/p101216.htm"),
    ("G20", "G20 countries", "Derivatives reform", "25 SEP 2009",
     "Swaps like AIG's must go through central clearing houses that hold money to cover losses.",
     "https://www.g20.utoronto.ca/2009/2009communique0925.html"),
    ("FSB", "Worldwide", "Financial Stability Board", "2 APR 2009",
     "Set up by the G20 to watch for risks across the whole world's financial system.",
     "https://www.fsb.org/history-of-the-fsb/"),
    ("UK", "United Kingdom", "Ring-fencing (Banking Reform Act)", "18 DEC 2013",
     "Big banks must wall off everyday savings from riskier investment banking, fully from 1 Jan 2019.",
     "https://www.legislation.gov.uk/ukpga/2013/33/contents"),
    ("EU", "Euro area", "ECB bank supervision", "4 NOV 2014",
     "The European Central Bank checks the biggest eurozone banks, instead of 19 separate national watchdogs.",
     "https://www.bankingsupervision.europa.eu/about/milestones/html/index.en.html"),
    ("EU", "European Union", "\"Bail-in\" rules (BRRD)", "15 MAY 2014",
     "If a bank fails, its owners and lenders take the losses first, not taxpayers.",
     "https://eur-lex.europa.eu/eli/dir/2014/59/oj"),
]

# ---- page 11: what our lights said -----------------------------------------------------------

LIGHTS_TEXT = {
    "intro": "The same 10 rules we use for every crash, applied to the months before the October 2007 peak.",
    "summary": "6 of 10 lights warned early. Home building fell for a year before the peak and the yield curve flipped "
               "14 months ahead; stocks were expensive and profits were falling. Credit spreads, the bond market's "
               "fear gauge, only switched on one month before.",
    "penny": "So the danger was hiding in plain sight: in houses!",
    "bear": "Watch where the borrowing is. That's where the next crack will show.",
    "next": "2020 COVID CRASH",
}

# ---- page 12: sources ------------------------------------------------------------------------

SOURCE_NOTE = ("Every number in this comic was checked against the sources below on 21 October 2026. Index falls use the highest "
               "close from January 2007 to June 2008 and the lowest close after it up to December 2009, in local currency. "
               "US home prices: S&P CoreLogic Case-Shiller national index. Jobs, rates, debt and wealth: official US data "
               "(BLS, Census, Federal Reserve) via FRED. Characters are fictional. For education only, not investment advice.")
EXTRA_SOURCES = [
    "https://www.federalreservehistory.org/essays/great-recession-of-200709",
    "https://www.federalreserve.gov/newsevents/pressreleases/other20080916a.htm (AIG)",
    "https://www.npr.org/2008/09/29/95180529/house-rejects-bailout-bill-wall-street-shudders",
    "https://cepr.org/voxeu/columns/financial-crisis-ten-years (BNP Paribas, 9 Aug 2007)",
    "https://www.heraldnet.com/business/bank-of-america-to-buy-countrywide-for-4-1-billion",
    "https://www.everycrsreport.com/files/20081120_RS22988_da41744f4b88eb21f8891e252e67ce0c02c9e2ae.html (Iceland)",
    "https://www.nber.org/research/data/us-business-cycle-expansions-and-contractions",
    "https://www.federalreserve.gov/regreform/reform-bearstearns.htm (Bear Stearns)",
    "https://www.pbs.org/newshour/show/jp-morgan-raises-bear-stearns-buyout-bid ($2 raised to $10)",
    "https://www.federalreservehistory.org/essays/fannie-mae-and-freddie-mac (Fannie & Freddie)",
    "https://www.federalreserve.gov/newsevents/pressreleases/monetary20081216b.htm (rates to 0-0.25%)",
    "https://finance.yahoo.com/ (daily index closes) · https://www.naturalearthdata.com/ (map outlines)",
]


def source_groups(page_no):
    return [
        (f"The mortgage machine (page {page_no('machine')})", MACHINE_SOURCES + [v[3] for v in MACHINE_STATS.values()]),
        (f"The good times (page {page_no('good-times')})", [g[4] for g in GOOD_TIMES]),
        (f"From boom to danger (page {page_no('boom-to-danger')})", [b[4] for b in DANGER_STEPS]),
        (f"Warning signs and what popped it (pages {page_no('warning-signs')}, {page_no('what-popped')})", WARNING_SOURCES + PINS_SOURCES),
        (f"Fixing the rules (page {page_no('fixing-rules')})", [p[5] for p in POLICIES]),
        ("Timeline and data", EXTRA_SOURCES),
    ]


SOURCE_GROUPS = source_groups(lambda name: ORDER.index(name) + 1)

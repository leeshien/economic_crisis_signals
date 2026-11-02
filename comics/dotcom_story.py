"""Facts for the Dot-com comic. Each item: the words on the page + where the fact was checked.

Computed figures (productivity, jobs, surplus, internet use, CAPE, index moves) were calculated
from the named series on 2026-10-21; see comics/data/ and the README of this folder.
"""

FRED = "https://fred.stlouisfed.org/series/"

INVENTIONS = [  # (date, short label, pictogram, source)
    ("1989", "Web invented", "web", "https://web30.web.cern.ch/web-history.html"),
    ("1993", "Web free + browser", "browser", "https://timeline.web.cern.ch/node/794"),
    ("1994", "Online shops", "parcel", "https://www.history.com/this-day-in-history/july-5/amazon-is-founded-by-jeff-bezos"),
    ("1995", "Online auctions", "gavel", "https://www.elinkdesign.com/popular-websites-a-visual-history"),
    ("1998", "Web search", "magnifier", "https://www.elinkdesign.com/popular-websites-a-visual-history"),
    ("2000", "42m-transistor chip", "chip", "https://www.technologyreview.com/2008/12/22/216817/moores-law/amp/"),
]
INVENTION_NOTE = ("1989 Web proposed at CERN · 1993 CERN makes it free, Mosaic browser · 1994 Amazon · "
                  "1995 eBay · 1998 Google · 2000 Intel Pentium 4")

TECH_STATS = [  # (title, unit, [(label, value)], colour, note, source)
    ("CHIPS GOT MIGHTIER", "Transistors per Intel chip, millions",
     [("486 (1989)", 1.2), ("Pentium (1993)", 3.1), ("Pentium 4 (2000)", 42)], "#2e86de", "x35",
     "https://www.technologyreview.com/2008/12/22/216817/moores-law/amp/"),
    ("COMPUTERS GOT CHEAPER", "Producer prices of computers, quality-adjusted (1995 = 100)",
     [("1995", 100), ("1998", 56), ("2000", 39)], "#e63b2e", "-61%",
     "https://fred.stlouisfed.org/series/PCU334111334111"),
    ("COMPUTERS MOVED IN", "US households with a computer, %",
     [("1984", 8), ("1993", 23), ("2000", 51)], "#3fa34d", "HALF OF HOMES",
     "https://census.gov/history/pdf/internet-computer1984-2009.pdf"),
    ("PHONES WENT MOBILE", "US mobile subscriptions per 100 people",
     [("1990", 2), ("1995", 13), ("2000", 39)], "#f78c2e", "x19",
     "https://data.worldbank.org/indicator/IT.CEL.SETS.P2?locations=US"),
]

FED_STUDY = ("Federal Reserve economists estimated that about two-thirds of the late-1990s speed-up in productivity "
             "came from making and using computers and other IT.",
             "https://www.federalreserve.gov/pubs/feds/2000/200020/200020abs.html")

GOOD_TIMES = [  # (big number, headline, explanation, icon, source)
    ("3.0%", "Workers got more productive",
     "Output per hour grew 3.0% a year in 1995–2000, more than double the 1.4% a year of 1973–95.",
     "chart", FRED + "OPHNFB"),
    ("3.8%", "Jobs for almost everyone",
     "Unemployment fell to 3.8% in April 2000, the lowest since 1969.",
     "worker", FRED + "UNRATE"),
    ("~2%", "Prices stayed calm",
     "Consumer prices rose only about 2% a year in 1997–99, so the Fed had no reason to panic.",
     "tag", FRED + "CPIAUCSL"),
    ("$236bn", "The government saved money",
     "The US budget was in surplus in 1998–2001, the first since 1969. The 2000 surplus was $236 billion.",
     "piggy", FRED + "FYFSD"),
    ("9% → 43%", "Everyone went online",
     "The share of Americans using the internet jumped from 9% in 1995 to 43% in 2000.",
     "computer", "https://data.worldbank.org/indicator/IT.NET.USER.ZS?locations=US"),
    ("1996", "New rules opened telecoms",
     "The Telecommunications Act (8 Feb 1996) let new firms compete in phone and cable markets.",
     "capitol", "https://www.everycrsreport.com/reports/96-223.html"),
]

BUBBLE_STEPS = [  # (date, title, text, icon, source)
    ("9 AUG 1995", "Netscape goes public",
     "Priced at $28, its shares closed the first day at $58.25. A 16-month-old company was worth $2.9 billion overnight.",
     "rocket", "https://en.wikipedia.org/wiki/Netscape"),
    ("5 DEC 1996", "\"Irrational exuberance\"",
     "Fed chair Alan Greenspan asked how we would know when prices had gone too far. Markets dipped, then kept climbing for 3 more years.",
     "capitol", "https://en.wikipedia.org/wiki/Irrational_exuberance"),
    ("1999", "IPO mania",
     "On average, new shares jumped about 71% on their first trading day in 1999. The Nasdaq rose 86% in that one year.",
     "chart", "https://site.warrington.ufl.edu/ritter/ipo-data/"),
    ("\"EYEBALLS\"", "Clicks, not profits",
     "Investors valued websites by visitors, not earnings. In March 2000, 74% of 207 internet firms studied were burning cash.",
     "cash", "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/articles/cashburn.htm"),
    ("FIBRE", "Cables nobody needed (yet)",
     "Telecom firms expected internet traffic to keep exploding. They borrowed heavily and buried far more "
     "fibre-optic cable than anyone needed: by 2002 only about 2–5% of US fibre was in use. Global Crossing, "
     "which built a worldwide fibre network, went bankrupt on 28 Jan 2002, the biggest telecom failure up to then.",
     "cable", "https://www.fdic.gov/bank/analytical/bank-trends/bt0205.pdf"),
    ("10 JAN 2000", "AOL buys Time Warner",
     "AOL had less than a fifth of Time Warner's revenue and staff, yet its shares were worth almost twice as much. "
     "So AOL used its sky-high shares as money to buy the media giant, in the biggest US merger at the time. "
     "In 2002 the merged company lost $98.7 billion, a corporate record, mostly by writing down what it had paid.",
     "handshake", "https://money.cnn.com/2003/01/30/technology/aol/index.htm"),
]

TIMELINE_UP = [  # (date, title, text, mood, icon) — oldest first; drawn bottom-up
    ("9 AUG 1995", "Netscape IPO", "Shares double on day one. The internet gold rush begins.", "up", "rocket"),
    ("8 FEB 1996", "Telecom Act signed", "Phone and cable markets open to new competitors.", "up", "capitol"),
    ("5 DEC 1996", "\"Irrational exuberance\"", "Greenspan's warning. Markets shrug it off.", "neutral", "warning"),
    ("30 JUN 1999", "Fed starts raising rates", "First of six rises: 4.75% up to 6.5% by May 2000.", "down", "rate_up"),
    ("31 DEC 1999", "Nasdaq +86% in a year", "It ends 1999 at 4,069. Y2K passes quietly.", "up", "chart_up"),
    ("10 JAN 2000", "AOL + Time Warner", "Biggest US merger at the time, paid in AOL shares.", "up", "handshake"),
    ("10 MAR 2000", "THE PEAK", "Nasdaq closes at 5,048.62. It won't see this level again for 15 years.", "down", "peak_flag",
     "CRASH STARTS"),
    ("20 MAR 2000", "\"Burning Up\"", "Barron's: 51 internet firms could run out of cash within a year.", "down", "cash"),
    ("24 MAR 2000", "S&P 500 peaks", "1,527.46, the high for the wider US market.", "down", "peak_flag"),
]

TIMELINE_DOWN = [
    ("3 APR 2000", "Microsoft talks fail", "Settlement talks collapse; a judge rules it broke antitrust law. Nasdaq −7.6% that day.", "down", "gavel"),
    ("14 APR 2000", "Black Friday for tech", "Nasdaq −9.7% in one day. Now −34% from the peak in just 5 weeks.", "down",
     "chart_down", "THE CRASH"),
    ("16 MAY 2000", "Rates hit 6.5%", "The Fed's last rise. Borrowing is now expensive.", "down", "rate_up"),
    ("7 NOV 2000", "Pets.com shuts down", "268 days after its IPO. Its sock-puppet mascot becomes a symbol of the bust.", "down", "sock_puppet"),
    ("3 JAN 2001", "Fed starts cutting", "Eleven cuts in 2001 take rates from 6.5% to 1.75%.", "neutral", "rate_down"),
    ("MAR 2001", "Recession begins", "The US economy shrinks until November 2001.", "down", "recession"),
    ("11 SEP 2001", "Terror attacks", "Markets close for 4 trading days. Nasdaq −6.8% when they reopen.", "down", "closed_sign"),
    ("2 DEC 2001", "Enron collapses", "Fake accounts at a Wall Street favourite. Trust starts to crack.", "down", "fake_accounts"),
    ("21 JUL 2002", "WorldCom bankrupt", "Biggest US bankruptcy at the time, after billions in false profits.", "down", "bankrupt"),
    ("9 OCT 2002", "THE BOTTOM", "Nasdaq 1,114.11 (−78%). S&P 500 776.76 (−49%).", "up", "floor_hit",
     "CRASH ENDS"),
]

PINS = [  # what popped the balloon: (title, text, icon)
    ("Dearer money", "The Fed raised rates six times, from 4.75% to 6.5% (Jun 1999–May 2000). Future profits were suddenly worth less.", "rate_up"),
    ("Cash ran out", "Most dot-coms lost money. When investors stopped funding them, they had months, not years, of cash left.", "wallet_empty"),
    ("Insiders could sell", "Founders and staff are usually barred from selling for about 6 months after an IPO. After the record IPOs of 1999, those lock-ups ended in 2000.", "padlock_open"),
    ("Reality check", "The Microsoft ruling and the Barron's cash study in spring 2000 made investors ask: who will actually make money?", "magnifier"),
    ("Spending stopped", "Firms that had over-built cut back hard. Business spending on computers and other IT equipment fell 24% (late 2000 to late 2002).", "cart_x"),
    ("Trust broke", "Enron (2001) and WorldCom (2002) showed some profits were fake. Investors began to doubt every company's accounts.", "broken_trust"),
]

POLICIES = [  # (flag, country, law, year, what it did, source)
    ("US", "United States", "Sarbanes-Oxley Act", "30 JUL 2002",
     "Bosses must personally sign off their company's accounts. A new watchdog, the PCAOB, checks the auditors.",
     "https://www.everycrsreport.com/reports/RL31554.html"),
    ("US", "United States", "Global Research Settlement", "28 APR 2003",
     "10 big Wall Street banks paid about $1.4 billion and had to separate stock research from deal-making.",
     "https://www.sec.gov/litigation/litreleases/lr18438.htm"),
    ("EU", "European Union", "Market Abuse Directive", "28 JAN 2003",
     "One set of EU rules against insider dealing and market manipulation.",
     "https://eur-lex.europa.eu/eli/dir/2003/6"),
    ("EU", "European Union", "IFRS for listed firms", "19 JUL 2002",
     "From 2005, listed EU companies report with the same international accounting standards.",
     "https://www.legislation.gov.uk/eur/2002/1606/data.html"),
    ("DE", "Germany", "Corporate Governance Code", "26 FEB 2002",
     "Good-governance rules for listed firms: comply, or explain why not.",
     "https://dcgk.de/en/"),
    ("DE", "Germany", "Neuer Markt closed", "5 JUN 2003",
     "Germany's dot-com market, whose index lost over 95% from its 2000 peak, was shut down.",
     "https://www.bioworld.com/articles/392498-germany-s-neuer-markt-closing-amid-mounting-losses-scandals"),
    ("UK", "United Kingdom", "Higgs Review", "20 JAN 2003",
     "Led to a stricter Combined Code: at least half of a board should be independent directors.",
     "https://en.wikipedia.org/wiki/Review_of_the_role_and_effectiveness_of_non-executive_directors"),
    ("CA", "Canada", "CEO/CFO certification (52-109)", "30 MAR 2004",
     "Canadian bosses must certify their filings, closely following the US rules.",
     "https://www.osc.ca/sites/default/files/pdfs/irps/rule_20040116_52-109_note-mi.pdf"),
    ("JP", "Japan", "\"J-SOX\" (FIEA 2006)", "2006 / 2008",
     "Listed companies must report on their internal controls, from fiscal years starting April 2008.",
     "https://www.rieti.go.jp/en/rieti_report/097.html"),
]

EXTRA_SOURCES = [
    "https://www.federalreserve.gov/boarddocs/press/general/2000/20000516/",
    "https://money.cnn.com/2001/12/11/economy/fed/",
    "https://money.cnn.com/2000/04/03/markets/markets_newyork/",
    "https://money.cnn.com/2002/07/19/news/worldcom_bankruptcy/",
    "https://en.wikipedia.org/wiki/Pets.com",
    "https://money.cnn.com/2002/01/28/companies/globalcrossing/ (Global Crossing)",
    "https://www.sec.gov/Archives/edgar/data/0001105705/000095014403004064/g81332e10vk.htm (AOL Time Warner 2002 10-K)",
    "https://ideas.repec.org/h/spr/mgmchp/978-3-030-02363-8_3.html (AOL vs Time Warner size)",
    "https://fred.stlouisfed.org/series/OPHNFB (output per hour chart)",
    "https://fred.stlouisfed.org/series/Y034RC1Q027SBEA (IT equipment investment)",
    "https://www.nber.org/research/data/us-business-cycle-expansions-and-contractions",
    "https://shillerdata.com/",
    "https://finance.yahoo.com/ (daily index closes)",
    "https://www.naturalearthdata.com/ (map outlines, public domain)",
]

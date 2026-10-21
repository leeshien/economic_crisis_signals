"""The 10 scored warning signals (+ the Sahm rule, shown as context only).

Each signal = a metric (computed in pipeline/rules.py from `inputs`) compared to a fixed
threshold (`unit` is how the metric is shown). Thresholds are rules of thumb fixed once — never tuned to fit crises.
"""

GROUPS = {
    "rates":   "Money & rates",
    "prices":  "Prices",
    "credit":  "Credit",
    "markets": "Markets",
    "economy": "Real economy",
}

_FRED = "https://fred.stlouisfed.org/series/"

SIGNALS = [
    {
        "id": "yield_curve", "name": "Yield curve inverted", "group": "rates",
        "inputs": ["GS10", "TB3MS"], "op": "<", "threshold": 0.0, "unit": "pts",
        "metric_label": "10-year minus 3-month Treasury yield (pts)",
        "what": "The gap between long-term and short-term government interest rates.",
        "why": "Normally long-term rates are higher. When short rates rise above them, "
               "bond investors are betting the economy will weaken and rates will be cut.",
        "rule": "On when the 10-year Treasury yield is below the 3-month yield.",
        "sources": [_FRED + "GS10", _FRED + "TB3MS"],
    },
    {
        "id": "fed_hiking", "name": "Fed hiking fast", "group": "rates",
        "inputs": ["FEDFUNDS"], "op": ">=", "threshold": 1.5, "unit": "pts",
        "metric_label": "Fed funds rate change vs 18 months earlier (pts)",
        "what": "How quickly the Federal Reserve is raising its key interest rate.",
        "why": "Rapid rate rises make borrowing expensive for households and companies, "
               "which slows spending and investment.",
        "rule": "On when the Fed funds rate is at least 1.5 points higher than 18 months earlier.",
        "sources": [_FRED + "FEDFUNDS"],
    },
    {
        "id": "inflation", "name": "Inflation high", "group": "prices",
        "inputs": ["CPIAUCSL"], "op": ">", "threshold": 4.0, "unit": "%",
        "metric_label": "Consumer prices, % change vs a year earlier",
        "what": "How fast consumer prices are rising.",
        "why": "High inflation eats into incomes and profits, and forces the Fed to raise rates.",
        "rule": "On when consumer prices are more than 4% higher than a year earlier.",
        "sources": [_FRED + "CPIAUCSL"],
    },
    {
        "id": "oil_shock", "name": "Oil shock", "group": "prices",
        "inputs": ["WTISPLC"], "op": ">", "threshold": 50.0, "unit": "%",
        "metric_label": "Crude oil price, % change vs a year earlier",
        "what": "A sudden jump in the price of crude oil.",
        "why": "Energy feeds into almost everything; a spike acts like a tax on consumers "
               "and businesses.",
        "rule": "On when the oil price is more than 50% higher than a year earlier.",
        "sources": [_FRED + "WTISPLC"],
    },
    {
        "id": "credit_spread", "name": "Credit spread widening", "group": "credit",
        "inputs": ["BAA", "GS10"], "op": ">=", "threshold": 0.5, "unit": "pts",
        "metric_label": "Baa corporate minus 10-year Treasury yield, rise above its 24-month low (pts)",
        "what": "The extra interest companies pay to borrow compared with the government.",
        "why": "When lenders start doubting companies can repay, they demand more interest — "
               "often while stocks are still rising.",
        "rule": "On when the Baa corporate bond spread is at least 0.5 points above its "
                "lowest level of the past 24 months.",
        "sources": [_FRED + "BAA", _FRED + "GS10"],
    },
    {
        "id": "corp_debt", "name": "Corporate debt build-up", "group": "credit",
        "inputs": ["BCNSDODNS", "GDP"], "op": ">=", "threshold": 3.0, "unit": "pts",
        "metric_label": "Corporate debt as % of GDP, change vs 3 years earlier (pts)",
        "what": "How fast company borrowing is growing compared with the whole economy.",
        "why": "Debt that grows faster than the economy leaves companies fragile when "
               "growth or credit dries up.",
        "rule": "On when non-financial corporate debt is at least 3 points of GDP higher "
                "than 3 years earlier.",
        "sources": [_FRED + "BCNSDODNS", _FRED + "GDP"],
    },
    {
        "id": "cape", "name": "Stocks expensive", "group": "markets",
        "inputs": ["CAPE"], "op": ">", "threshold": 25.0, "unit": "",
        "metric_label": "Shiller CAPE ratio",
        "what": "Stock prices compared with 10 years of inflation-adjusted company earnings.",
        "why": "Very high valuations mean prices depend on optimism; they show a bubble "
               "but not when it will burst.",
        "rule": "On when the Shiller CAPE ratio is above 25.",
        "sources": ["https://shillerdata.com/"],
    },
    {
        "id": "profits", "name": "Profits falling", "group": "economy",
        "inputs": ["CP"], "op": "<", "threshold": 0.0, "unit": "%",
        "metric_label": "Corporate profits after tax, % change vs a year earlier",
        "what": "Whether US company profits are shrinking.",
        "why": "Share prices ultimately rest on profits; falling profits often precede "
               "falling markets.",
        "rule": "On when after-tax corporate profits are lower than a year earlier.",
        "sources": [_FRED + "CP"],
    },
    {
        "id": "housing", "name": "Housing slump", "group": "economy",
        "inputs": ["HOUST"], "op": "<=", "threshold": -20.0, "unit": "%",
        "metric_label": "Housing starts (3-month average), % change vs a year earlier",
        "what": "How many new homes builders are starting.",
        "why": "Housing is very sensitive to interest rates and reacts early when "
               "conditions tighten.",
        "rule": "On when housing starts (3-month average) are at least 20% lower than a year earlier.",
        "sources": [_FRED + "HOUST"],
    },
    {
        "id": "factory_hours", "name": "Factory hours cut", "group": "economy",
        "inputs": ["AWHMAN"], "op": ">=", "threshold": 0.5, "unit": "hrs",
        "metric_label": "Hours below their 12-month high (hours per week)",
        "what": "The average working week in factories.",
        "why": "Employers cut hours before they cut jobs, so this moves earlier than "
               "unemployment.",
        "rule": "On when the average factory work week is at least 0.5 hours below its "
                "12-month high.",
        "sources": [_FRED + "AWHMAN"],
    },
]

SAHM = {
    "id": "sahm", "name": "Recession confirmed (Sahm rule)",
    "inputs": ["UNRATE"], "op": ">=", "threshold": 0.5, "unit": "pts",
    "metric_label": "3-month average unemployment rate above its 12-month low (pts)",
    "what": "A rise in unemployment big enough to show a recession has started.",
    "why": "Layoffs come after the market and business have already turned, so this "
           "confirms a recession rather than warning of one.",
    "rule": "Fires when the 3-month average unemployment rate is 0.5 points above its 12-month low.",
    "sources": [_FRED + "UNRATE"],
}

SIGNAL_IDS = [s["id"] for s in SIGNALS]

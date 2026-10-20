"""Print the built scoreboard as text. Usage: python tools/print_scoreboard.py [dist/data/report.json]"""
import json
import sys

LABEL = {"early": "{}", "chronic": "C{}", "late": "late+{}", "none": ".", "na": "n/a"}

r = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "dist/data/report.json"))
sids = [s["id"] for s in r["signals"]]
print("crisis".ljust(8) + "".join(s[:11].rjust(12) for s in sids) + "  early")
for c in r["crises"]:
    cells = [LABEL[c["cells"][s]["state"]].format(c["cells"][s]["months"]) for s in sids]
    print(c["id"].ljust(8) + "".join(v.rjust(12) for v in cells)
          + f"  {c['early_count']}  (fall {c['fall_pct']}%, unemp peak {c['peak_unemployment']}, sahm {c['timeline']['sahm']})")
print("false alarm %".ljust(8) + "".join(str(s["false_alarm"]).rjust(12) for s in r["signals"]))
t = r["today"]
print(f"\ntoday: {t['on']} of {t['valid']} valid lights on (of {t['total']}); past peaks {t['typical_min']}-{t['typical_max']}")
for row in t["rows"]:
    print(f"  {row['name']:<26} on={row['on']!s:<5} stale={row['stale']!s:<5} as_of={row['as_of']} since={row['on_since']}")

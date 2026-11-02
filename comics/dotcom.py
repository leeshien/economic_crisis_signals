"""The Dot-com Bubble (1995–2002) — comic pages. Every number comes from comics/data/*.json."""
import json
from pathlib import Path

from comics import art
from comics.art import INK, PAPER, RED, YELLOW, BLUE, HEAD, BODY, W, H
from comics.worldmap import Frame, country_paths

DATA = Path(__file__).resolve().parent / "data"
FALLS = json.loads((DATA / "dotcom_falls.json").read_text(encoding="utf-8"))
NASDAQ = json.loads((DATA / "nasdaq_monthly.json").read_text(encoding="utf-8"))

ISSUE = "ISSUE 4 OF 7"
SLUG = "2000-dotcom"


def _num(v: float, digits: int = 0) -> str:
    return f"{v:,.{digits}f}"


def _date(iso: str) -> str:
    y, m, d = iso.split("-")
    months = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()
    return f"{int(d)} {months[int(m) - 1]} {y}"


def _page(body: str, bg=PAPER) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'{art.defs()}<rect width="{W}" height="{H}" fill="{bg}"/>{body}</svg>')


def _footer(text: str, page_no: int) -> str:
    return (f'<text x="34" y="{H - 22}" style="{BODY}" font-size="12.5" fill="{INK}" fill-opacity="0.75">{text}</text>'
            f'<text x="{W - 34}" y="{H - 22}" style="{HEAD}" font-size="18" text-anchor="end" fill="{INK}">{page_no}</text>')


# ---- page 1: cover ---------------------------------------------------------------------------

def cover() -> str:
    nq = NASDAQ["points"]
    peak, trough = FALLS["nasdaq"], None
    x0, x1, yb, yt, vmax = 70, 770, 800, 400, 5400
    X = lambda i: x0 + (x1 - x0) * i / (len(nq) - 1)
    Y = lambda v: yb - (yb - yt) * v / vmax
    line = " ".join(f"{'M' if i == 0 else 'L'}{X(i):.1f},{Y(v):.1f}" for i, (_, v) in enumerate(nq))
    area = line + f" L{X(len(nq) - 1):.1f},{yb} L{X(0):.1f},{yb} Z"
    ipk = max(range(len(nq)), key=lambda i: nq[i][1])
    itr = min(range(ipk, len(nq)), key=lambda i: nq[i][1])
    px, py = X(ipk), Y(nq[ipk][1])
    tx, ty = X(itr), Y(nq[itr][1])
    years = "".join(
        f'<text x="{X(i):.0f}" y="{yb + 26}" style="{HEAD}" font-size="20" text-anchor="middle" fill="{INK}">{d[:4]}</text>'
        for i, (d, _) in enumerate(nq) if d.endswith("-01") and int(d[:4]) % 2 == 0)
    # balloon shreds flying off the burst
    shreds = "".join(
        f'<path d="M{px + dx},{py + dy} q{qx},{qy} {ex},{ey}" stroke="{RED}" stroke-width="9" fill="none" stroke-linecap="round"/>'
        for dx, dy, qx, qy, ex, ey in [(-70, -95, -20, -30, -45, -20), (75, -100, 25, -25, 40, -10),
                                       (-95, 10, -30, 5, -35, 30), (95, 15, 30, 10, 30, 35)])
    body = (
        art.sunburst(px, py, rays=30)
        + f'<rect width="{W}" height="{H}" fill="url(#dots-big)"/>'
        # masthead strip
        + f'<rect x="0" y="0" width="{W}" height="54" fill="{INK}"/>'
        + f'<text x="30" y="37" style="{HEAD}" font-size="26" fill="{YELLOW}" letter-spacing="1.5">ECONOMIC CRISIS SIGNALS</text>'
        + f'<text x="{W - 30}" y="37" style="{HEAD}" font-size="26" fill="#fff" text-anchor="end">{ISSUE}</text>'
        + art.title(W / 2, 178, "THE DOT-COM", size=124, rot=-3)
        + art.title(W / 2, 300, "BUBBLE!", size=150, fill=BLUE, rot=-3)
        + f'<g transform="rotate(4 700 352)"><rect x="610" y="326" width="190" height="50" fill="{INK}"/>'
          f'<text x="705" y="362" style="{HEAD}" font-size="34" text-anchor="middle" fill="{YELLOW}">1995 – 2002</text></g>'
        # chart
        + f'<path d="{area}" fill="#fff" fill-opacity="0.55"/><path d="{area}" fill="url(#dots)"/>'
        + f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{INK}" stroke-width="5"/>'
        + f'<path d="{line}" fill="none" stroke="#fff" stroke-width="15" stroke-linejoin="round"/>'
        + f'<path d="{line}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
        + years
        + shreds
        + art.burst(px, py - 6, 78, "POP!", size=56)
        # peak + bottom labels
        + f'<g transform="rotate(-3 {px - 250} {py + 40})"><rect x="{px - 370}" y="{py + 22}" width="260" height="64" fill="#fff" stroke="{INK}" stroke-width="3"/>'
          f'<text x="{px - 240}" y="{py + 48}" style="{HEAD}" font-size="22" text-anchor="middle" fill="{INK}">NASDAQ PEAK · {_date(peak["peak_date"])}</text>'
          f'<text x="{px - 240}" y="{py + 78}" style="{HEAD}" font-size="30" text-anchor="middle" fill="{RED}">{_num(peak["peak"], 2)}</text></g>'
        + f'<line x1="{tx}" y1="{ty - 8}" x2="{tx}" y2="{ty - 118}" stroke="{INK}" stroke-width="4"/>'
          f'<circle cx="{tx}" cy="{ty}" r="7" fill="{YELLOW}" stroke="{INK}" stroke-width="3"/>'
        + f'<g transform="rotate(2 {tx + 20} {ty - 160})"><rect x="{tx - 110}" y="{ty - 210}" width="250" height="94" fill="{INK}"/>'
          f'<text x="{tx + 15}" y="{ty - 182}" style="{HEAD}" font-size="22" text-anchor="middle" fill="#fff">BOTTOM · {_date(peak["trough_date"])}</text>'
          f'<text x="{tx + 15}" y="{ty - 134}" style="{HEAD}" font-size="42" text-anchor="middle" fill="{YELLOW}">{_num(peak["trough"], 2)} ({peak["fall_pct"]:.0f}%)</text></g>'
        # narrators
        + art.penny(150, 1132, s=0.68, mood="happy")
        + art.bear(700, 1132, s=0.68, mood="calm", flip=True)
        + art.bubble(232, 862, 300, "The internet changes EVERYTHING. This time it's different!", tail=(185, 950), size=19)
        + art.bubble(332, 1000, 270, "Hmm. That's what they ALWAYS say...", tail=(640, 975), size=19)
        + f'<rect x="0" y="{H - 44}" width="{W}" height="44" fill="{INK}"/>'
        + f'<text x="{W / 2}" y="{H - 16}" style="{BODY}" font-size="15" font-weight="700" text-anchor="middle" fill="#fff">'
          f'A true story, told with real data · Chart: Nasdaq Composite, monthly closes (Yahoo Finance)</text>'
    )
    return _page(body)


# ---- page 8: the world map -------------------------------------------------------------------

BUCKETS = [(-70, "#9b1c1c", "fell 70% or more"), (-60, "#e63b2e", "60–70%"), (-50, "#f78c2e", "50–60%"),
           (-40, "#ffd23f", "40–50%"), (-100, "#fff1a8", "less than 40%")]
NO_DATA = "#e9e2cf"


def _color(fall):
    for limit, col, _ in BUCKETS[:-1]:
        if fall <= limit:
            return col
    return BUCKETS[-1][1]


# where each market's tag sits on the world map (lon, lat of the tag; anchor point in the country)
_TAGS = {"USA": ((-100, 39), (-100, 39)), "CAN": ((-108, 60), (-108, 60)), "MEX": ((-120, 14), (-102, 23)),
         "BRA": ((-52, -8), (-52, -8)), "ARG": ((-90, -38), (-65, -35)), "IND": ((78, 21), (78, 21)),
         "CHN": ((100, 36), (100, 36)), "JPN": ((160, 42), (139, 37)), "KOR": ((152, 28), (128, 36)),
         "TWN": ((150, 14), (121, 23.7)), "HKG": ((120, 2), (114.2, 22.3)), "SGP": ((80, -8), (103.8, 1.35)),
         "MYS": ((92, 8), (102, 4)), "IDN": ((118, -14), (117, -1)), "AUS": ((134, -25), (134, -25)),
         "ISR": ((48, 22), (35, 31.5))}
_EUROPE = {"GBR": (-3.2, 54.6), "DEU": (10.3, 51), "FRA": (2.4, 46.6), "NLD": (4.2, 54.4), "BEL": (1.0, 50.9),
           "CHE": (8.2, 46.8), "AUT": (14.5, 47.6), "ESP": (-3.7, 40.2), "ITA": (12.5, 42.8)}
_SMALL = {"HKG": (114.2, 22.3), "SGP": (103.8, 1.35)}  # too small for the 1:110m outlines


def _tag(x, y, text, fill) -> str:
    w = 16 + len(text) * 11
    return (f'<rect x="{x - w / 2:.0f}" y="{y - 16:.0f}" width="{w}" height="30" rx="4" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>'
            f'<text x="{x:.0f}" y="{y + 7:.0f}" style="{HEAD}" font-size="21" text-anchor="middle" fill="{INK}">{text}</text>')


def map_page() -> str:
    from comics.dotcom_pages import page_no
    mk = {m["a3"]: m for m in FALLS["markets"]}
    style = lambda a3: (f'fill="{_color(mk[a3]["fall_pct"])}" stroke="{INK}" stroke-width="1.2"' if a3 in mk
                        else f'fill="{NO_DATA}" stroke="#9c927a" stroke-width="0.8"')
    hatch = lambda a3: ('fill="url(#dots)" stroke="none"' if a3 in mk else 'fill="url(#hatch)" stroke="none"')
    nq = FALLS["nasdaq"]

    # world map
    fx, fy, fw, fh = 26, 186, 788, 380
    world = Frame(fx, fy, fw, fh, lon=(-168, 190), lat=(-50, 78))
    tags = []
    for a3, ((tl, ta), (al, aa)) in _TAGS.items():
        x, y = world(tl, ta)
        ax, ay = world(al, aa)
        if (tl, ta) != (al, aa):
            tags.append(f'<line x1="{ax:.0f}" y1="{ay:.0f}" x2="{x:.0f}" y2="{y:.0f}" stroke="{INK}" stroke-width="2"/>'
                        f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="3.5" fill="{INK}"/>')
        tags.append(_tag(x, y, f'{mk[a3]["fall_pct"]:.0f}%', "#fff"))
    small = "".join(f'<circle cx="{world(*p)[0]:.1f}" cy="{world(*p)[1]:.1f}" r="6" fill="{_color(mk[a3]["fall_pct"])}" '
                    f'stroke="{INK}" stroke-width="2"/>' for a3, p in _SMALL.items())
    ex0, ey0 = world(-11, 60)
    ex1, ey1 = world(20, 36)
    europe_box = (f'<rect x="{ex0:.0f}" y="{ey0:.0f}" width="{ex1 - ex0:.0f}" height="{ey1 - ey0:.0f}" fill="none" '
                  f'stroke="{INK}" stroke-width="2.5" stroke-dasharray="6 4"/>'
                  f'<text x="{ex0:.0f}" y="{ey0 - 6:.0f}" style="{HEAD}" font-size="16" fill="{INK}">EUROPE: SEE BELOW</text>')
    bx, by = world(-150, 6)
    world_map = (f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="#cfe8f5"/>'
                 f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="url(#dots)"/>'
                 + country_paths(world, style) + country_paths(world, hatch) + small + europe_box + "".join(tags)
                 + art.burst(bx, by, 46, "", points=12, fill=YELLOW)
                 + f'<text x="{bx:.0f}" y="{by - 4:.0f}" style="{HEAD}" font-size="15" text-anchor="middle" fill="{INK}">NASDAQ</text>'
                 + f'<text x="{bx:.0f}" y="{by + 18:.0f}" style="{HEAD}" font-size="22" text-anchor="middle" fill="{RED}">{nq["fall_pct"]:.0f}%</text>')

    # Europe close-up
    ix, iy, iw, ih = 26, 584, 386, 420
    eu = Frame(ix, iy, iw, ih, lon=(-11, 20), lat=(36, 60))
    eu_tags = "".join(_tag(*eu(*p), f'{mk[a3]["fall_pct"]:.0f}%', "#fff") for a3, p in _EUROPE.items())
    inset = (f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" fill="#cfe8f5"/>'
             + country_paths(eu, style) + country_paths(eu, hatch) + eu_tags
             + f'<rect x="{ix}" y="{iy}" width="112" height="30" fill="{INK}"/>'
             + f'<text x="{ix + 10}" y="{iy + 22}" style="{HEAD}" font-size="20" fill="{YELLOW}">EUROPE</text>')

    # ranked bars
    rx, ry, rw = 428, 584, 386
    rows = sorted(FALLS["markets"], key=lambda m: m["fall_pct"])
    rh = (ih - 50) / len(rows)
    bars = [f'<rect x="{rx}" y="{ry}" width="{rw}" height="{ih}" fill="#fff"/>',
            f'<text x="{rx + 12}" y="{ry + 28}" style="{HEAD}" font-size="22" fill="{INK}">THE FALLS, RANKED</text>']
    for i, m in enumerate(rows):
        y = ry + 40 + i * rh
        bw = (rw - 176) * -m["fall_pct"] / 80
        mark = "†" if m["note"] else ""
        bars.append(f'<text x="{rx + 10}" y="{y + rh - 4:.1f}" style="{BODY}" font-size="12.5" font-weight="700" fill="{INK}">{m["country"]}{mark}</text>'
                    f'<rect x="{rx + 122}" y="{y + 2:.1f}" width="{bw:.1f}" height="{rh - 4:.1f}" fill="{_color(m["fall_pct"])}" stroke="{INK}" stroke-width="1.5"/>'
                    f'<text x="{rx + 128 + bw:.1f}" y="{y + rh - 4:.1f}" style="{BODY}" font-size="12.5" font-weight="700" fill="{INK}">{m["fall_pct"]:.0f}%</text>')

    legend = [f'<text x="30" y="1030" style="{HEAD}" font-size="17" fill="{INK}">INDEX FALL:</text>']
    lx = 122
    for _, col, label in BUCKETS + [(None, NO_DATA, "no data used")]:
        legend.append(f'<rect x="{lx}" y="1016" width="18" height="17" fill="{col}" stroke="{INK}" stroke-width="2"/>'
                      + (f'<rect x="{lx}" y="1016" width="18" height="17" fill="url(#hatch)"/>' if col == NO_DATA else "")
                      + f'<text x="{lx + 23}" y="1030" style="{BODY}" font-size="12.5" font-weight="700" fill="{INK}">{label}</text>')
        lx += 32 + len(label) * 6.6

    head, _ = art.caption(26, 112, 788, "When the bubble burst, share prices fell around the world. Each country is "
                                        "shaded by how far its main stock index dropped, from its 1999–2000 high to "
                                        "its lowest point by mid-2003.", size=15)
    narr = (art.bear(64, 1160, s=0.34, mood="calm")
            + art.bubble(112, 1046, 330, "Markets packed with tech and telecom shares fell hardest.", tail=(92, 1066), size=14)
            + art.penny(782, 1160, s=0.34, mood="shock")
            + art.bubble(478, 1046, 260, "But Australia only fell 20%?!", tail=(760, 1064), size=14)
            + art.bubble(112, 1100, 560, "Its market was mostly banks and miners. Very few dot-coms!", tail=(92, 1116), size=14))
    body = (art.title(W / 2, 90, "WHO GOT HURT?", size=80, fill=RED, rot=-2)
            + head + art.panel(fx, fy, fw, fh, content=world_map)
            + art.panel(ix, iy, iw, ih, content=inset)
            + art.panel(rx, ry, rw, ih, content="".join(bars))
            + "".join(legend) + narr
            + f'<text x="34" y="{H - 22}" style="{BODY}" font-size="11" fill="{INK}" fill-opacity="0.75">'
              f'Local-currency index closes, Yahoo Finance. Map: Natural Earth. † Argentina also had its own 2001 debt default;</text>'
            + f'<text x="34" y="{H - 9}" style="{BODY}" font-size="11" fill="{INK}" fill-opacity="0.75">'
              f'Brazil its own 2002 crisis; China = mainland market, then largely closed to foreign investors.</text>'
            + f'<text x="{W - 34}" y="{H - 10}" style="{HEAD}" font-size="18" text-anchor="end" fill="{INK}">{page_no("map")}</text>')
    return _page(body)


from comics import dotcom_pages as _p  # noqa: E402  (inner pages reuse the helpers above)

_FN = {"cover": cover, "tech": _p.tech_revolution, "good-times": _p.good_times, "boom-to-bubble": _p.boom_to_bubble,
       "valuation": _p.valuation, "timeline-up": _p.timeline_up, "timeline-down": _p.timeline_down,
       "what-popped": _p.what_popped, "map": map_page, "fixing-rules": _p.fixing_rules, "lesson": _p.lesson,
       "sources": _p.sources}
PAGES = [(f"{i:02d}-{name}", _FN[name]) for i, name in enumerate(_p.ORDER, 1)]

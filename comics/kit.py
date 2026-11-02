"""Shared page builders for the crisis comics (2008 onwards; the dot-com comic predates this kit).

A crisis is a story module (facts + sources, no drawing) plus a page module that draws its custom
pages and takes the shared ones from here. Shared pages read these story attributes:

  ORDER, CRISIS_ID, TIMELINE_UP/DOWN (+ TIMELINE_TEXT), PINS (+ PINS_TEXT), POLICIES (+ POLICY_TEXT),
  FALLS (+ MAP_TEXT), LIGHTS_TEXT, SOURCE_GROUPS, SOURCE_NOTE
"""
import json
import math
from html import escape

from comics import art, icons
from comics.art import INK, PAPER, RED, YELLOW, BLUE, ORANGE, HEAD, BODY, W, H, text_block, wrap
from comics.worldmap import Frame, country_paths
from pipeline.load import ROOT

GREEN = icons.GREEN


# ---- page frame ------------------------------------------------------------------------------

def page(body: str, bg=PAPER) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'{art.defs()}<rect width="{W}" height="{H}" fill="{bg}"/>{body}</svg>')


def page_no(st, name: str) -> int:
    return st.ORDER.index(name) + 1


def num_footer(n):
    return f'<text x="{W - 30}" y="{H - 16}" style="{HEAD}" font-size="20" text-anchor="end" fill="{INK}">{n}</text>'


def head(title, intro, size=74, y=88, rot=-2, fill=RED):
    cap, h = art.caption(26, y + 22, 788, intro, size=15)
    return art.title(W / 2, y, title, size=size, fill=fill, rot=rot) + cap, y + 22 + h


def sym(name):
    """Look up an icon drawing function by name across the icon modules."""
    from comics import symbols, tech_icons, crisis_icons
    special = {"chart_up": icons.chart_up, "rocket": icons.rocket, "capitol": icons.capitol,
               "cash": icons.cash_fire, "worker": icons.worker, "piggy": icons.piggy}
    if name in special:
        return special[name]
    for mod in (crisis_icons, symbols, tech_icons):
        fn = getattr(mod, name, None)
        if fn:
            return fn
    raise KeyError(f"no icon called {name!r}")


def medallion(cx, cy, r, icon, s):
    return (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="#f6f3ea" stroke="{INK}" stroke-width="2.5"/>'
            + sym(icon)(cx, cy, s))


def step_badge(x, y, n):
    return (f'<circle cx="{x}" cy="{y}" r="17" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
            f'<text x="{x}" y="{y + 8}" style="{HEAD}" font-size="22" text-anchor="middle" fill="#fff">{n}</text>')


# ---- "What does it mean?" jargon box ---------------------------------------------------------

def jargon(x, y, w, items, cols=1, size=13.5):
    """Plain-English glossary box. items = [(term, meaning, icon)]. Returns (svg, height)."""
    cw = (w - 20) / cols
    chars = int((cw - 70) / (size * 0.5))
    rows = []
    for i in range(0, len(items), cols):
        row = items[i:i + cols]
        hs = [24 + max(len(wrap(m, chars)), 1) * size * 1.2 for _, m, _ in row]
        rows.append((row, max(max(hs), 64)))
    h = 44 + sum(rh for _, rh in rows) + 6
    out = [f'<rect x="{x + 5}" y="{y + 5}" width="{w}" height="{h:.0f}" fill="{INK}"/>',
           f'<rect x="{x}" y="{y}" width="{w}" height="{h:.0f}" fill="#eef6ff" stroke="{INK}" stroke-width="3.5"/>',
           f'<rect x="{x}" y="{y}" width="{w}" height="34" fill="{BLUE}" stroke="{INK}" stroke-width="3.5"/>',
           f'<circle cx="{x + 20}" cy="{y + 17}" r="11" fill="#fff" stroke="{INK}" stroke-width="2.5"/>',
           f'<text x="{x + 20}" y="{y + 23}" style="{HEAD}" font-size="17" text-anchor="middle" fill="{BLUE}">?</text>',
           f'<text x="{x + 40}" y="{y + 25}" style="{HEAD}" font-size="21" fill="#fff" letter-spacing="1">WHAT DOES IT MEAN?</text>']
    yy = y + 44
    for row, rh in rows:
        for j, (term, meaning, icon) in enumerate(row):
            xx = x + 10 + j * cw
            out.append(medallion(xx + 28, yy + 28, 24, icon, 0.4)
                       + f'<text x="{xx + 62}" y="{yy + 16}" style="{HEAD}" font-size="18" fill="{INK}">{escape(term.upper())}</text>'
                       + text_block(xx + 62, yy + 18 + size, wrap(meaning, chars), size=size, weight="700", lh=1.2))
        yy += rh
    return "".join(out), h


# ---- timeline (time runs UP the page) --------------------------------------------------------

def crash_tag(cx, cy, label):
    """Red rubber-stamp label marking the crash on a timeline card."""
    w = len(label) * 11.5 + 30
    return (f'<g transform="rotate(-7 {cx} {cy})">'
            f'<rect x="{cx - w / 2 + 4:.0f}" y="{cy - 15}" width="{w:.0f}" height="32" fill="{INK}"/>'
            f'<rect x="{cx - w / 2:.0f}" y="{cy - 19}" width="{w:.0f}" height="32" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
            f'<text x="{cx}" y="{cy + 5}" style="{HEAD}" font-size="21" text-anchor="middle" fill="#fff" '
            f'letter-spacing="1">{escape(label)}</text></g>')


def _timeline(title, events, n, intro, fill):
    hd, top = head(title, intro, size=60, fill=fill)
    cx = W / 2
    y_top, y_bot = top + 56, H - 40
    step = (y_bot - y_top) / len(events)
    out = [hd,
           f'<line x1="{cx}" y1="{y_top - 18}" x2="{cx}" y2="{y_bot}" stroke="{INK}" stroke-width="8"/>',
           f'<line x1="{cx}" y1="{y_top - 18}" x2="{cx}" y2="{y_bot}" stroke="{YELLOW}" stroke-width="3"/>',
           f'<path d="M{cx - 20},{y_top - 12} L{cx},{y_top - 44} L{cx + 20},{y_top - 12} Z" fill="{INK}"/>',
           f'<text x="{cx + 28}" y="{y_top - 22}" style="{HEAD}" font-size="18" fill="{INK}">LATER</text>',
           f'<text x="{cx + 14}" y="{y_bot + 2}" style="{HEAD}" font-size="18" fill="{INK}">EARLIER</text>']
    cw = cx - 52
    for i, (date, ttl, text, mood, icon, *tag) in enumerate(events):
        y = y_bot - (i + 1) * step + 8  # oldest at the bottom
        left = i % 2 == 0
        x = 26 if left else cx + 26
        card, h = icons.event_card(x, y, cw, date, ttl, text, mood=mood, size=13.5, text_w=cw - 92)
        dot_col = {"up": GREEN, "down": RED, "neutral": BLUE}[mood]
        out.append(f'<line x1="{cx}" y1="{y + 26}" x2="{x + cw if left else x}" y2="{y + 26}" stroke="{INK}" stroke-width="3"/>'
                   f'<circle cx="{cx}" cy="{y + 26}" r="11" fill="{dot_col}" stroke="{INK}" stroke-width="3"/>' + card
                   + medallion(x + cw - 46, y + h / 2 + 4, 38, icon, 0.56)
                   + (crash_tag(x + cw - (64 if not left else 120), y - 4, tag[0]) if tag else ''))
    return page("".join(out) + num_footer(n))


def timeline_up(st):
    t = st.TIMELINE_TEXT
    return _timeline(t["up_title"], st.TIMELINE_UP, page_no(st, "timeline-up"), t["up_intro"], GREEN)


def timeline_down(st):
    t = st.TIMELINE_TEXT
    return _timeline(t["down_title"], st.TIMELINE_DOWN, page_no(st, "timeline-down"), t["down_intro"], RED)


# ---- what popped it --------------------------------------------------------------------------

def what_popped(st):
    from comics import symbols
    t = st.PINS_TEXT
    hd, top = head(t.get("title", "WHAT POPPED IT?"), t["intro"])
    bx, by, r = W / 2, top + 196, 118
    heads = [(-268, -128), (268, -128), (-318, 26), (318, 26), (-226, 168), (226, 168)]
    dirs = [math.atan2(dy / 1.12, dx) for dx, dy in heads]
    glow = f'<circle cx="{bx}" cy="{by}" r="{r + 96}" fill="{YELLOW}" opacity="0.35"/>'
    art_fn = t.get("balloon_art")  # a picture of what the bubble was made of, instead of a plain word
    balloon, contacts = symbols.stressed_balloon(bx, by, r, "" if art_fn else t["balloon"], dirs)
    if art_fn:
        from comics import crisis_icons
        balloon += getattr(crisis_icons, art_fn)(bx, by, r)
    needles = "".join(symbols.needle(bx + dx, by + dy, tx, ty, i + 1) for i, ((dx, dy), (tx, ty)) in enumerate(zip(heads, contacts)))
    sfx = (f'<text x="{bx - 200}" y="{by - 138}" style="{HEAD}" font-size="30" fill="{RED}" stroke="{INK}" stroke-width="1.5" '
           f'paint-order="stroke" transform="rotate(-12 {bx - 200} {by - 138})">CREEEAK...</text>'
           f'<text x="{bx + 120}" y="{by - 142}" style="{HEAD}" font-size="26" fill="{INK}" transform="rotate(10 {bx + 120} {by - 142})">SQUEAK!</text>')
    out = [hd, glow, balloon, needles, sfx]
    pw, ph, gap = 386, 152, 12
    y0 = by + 246
    for i, (ttl, text, icon) in enumerate(st.PINS):
        x = 26 + (i % 2) * (pw + gap)
        y = y0 + (i // 2) * (ph + gap)
        inner = (f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="#fff"/>'
                 f'<circle cx="{x + 30}" cy="{y + 30}" r="19" fill="{YELLOW}" stroke="{INK}" stroke-width="3"/>'
                 f'<text x="{x + 30}" y="{y + 38}" style="{HEAD}" font-size="24" text-anchor="middle" fill="{INK}">{i + 1}</text>'
                 + text_block(x + 60, y + 38, [ttl.upper()], size=24, family=HEAD)
                 + text_block(x + 16, y + 68, text, size=13.5, width=38, weight="700")
                 + medallion(x + pw - 52, y + 84, 40, icon, 0.62))
        out.append(art.panel(x, y, pw, ph, content=inner))
    yb = y0 + 3 * (ph + gap) + 4
    out.append(art.bear(80, H - 22, s=0.38, mood="calm")
               + art.bubble(140, yb, 640, t["bear"], tail=(110, yb + 60), size=15))
    return page("".join(out) + num_footer(page_no(st, "what-popped")))


# ---- world map -------------------------------------------------------------------------------

BUCKETS = [(-70, "#9b1c1c", "70% or more"), (-60, "#e63b2e", "60–70%"), (-50, "#f78c2e", "50–60%"),
           (-40, "#ffd23f", "40–50%"), (-100, "#fff1a8", "less than 40%")]
NO_DATA = "#e9e2cf"

# tag position (lon, lat) and, if different, the point in the country the leader line goes to
WORLD_TAGS = {"USA": ((-100, 39), None), "CAN": ((-108, 60), None), "MEX": ((-122, 14), (-102, 23)),
              "BRA": ((-52, -8), None), "ARG": ((-92, -40), (-65, -35)), "CHL": ((-95, -24), (-71, -30)),
              "ZAF": ((24, -30), None), "ISR": ((46, 20), (35, 31.5)), "TUR": ((50, 41), (35, 39)),
              "RUS": ((95, 62), None), "IND": ((78, 21), None), "CHN": ((100, 36), None),
              "JPN": ((160, 42), (139, 37)), "KOR": ((152, 28), (128, 36)), "TWN": ((150, 14), (121, 23.7)),
              "HKG": ((120, 2), (114.2, 22.3)), "SGP": ((80, -8), (103.8, 1.35)), "MYS": ((92, 8), (102, 4)),
              "IDN": ((118, -14), (117, -1)), "AUS": ((134, -25), None), "NZL": ((172, -48), (172, -41)),
              "SAU": ((45, 24), None), "EGY": ((30, 26), None)}
# Europe close-up: tag position and, if different, the point in the country the leader line goes to
EUROPE_TAGS = {"GBR": ((-2.3, 52.8), None), "IRL": ((-8.2, 53.2), None), "PRT": ((-8.4, 39.8), None),
               "ESP": ((-2.8, 39.6), None), "FRA": ((2.0, 46.6), None), "BEL": ((0.6, 49.9), (4.6, 50.6)),
               "NLD": ((3.6, 55.0), (5.6, 52.3)), "DEU": ((10.4, 51.4), None), "CHE": ((7.4, 46.3), None),
               "AUT": ((14.2, 46.9), None), "ITA": ((12.8, 42.4), None), "GRC": ((22.2, 39.4), None),
               "DNK": ((9.6, 56.5), None), "NOR": ((9.0, 61.5), None), "SWE": ((15.6, 61.0), None),
               "FIN": ((26.0, 63.0), None), "POL": ((20.2, 52.7), None), "CZE": ((15.6, 50.6), None),
               "HUN": ((20.4, 46.9), None)}
EUROPE_FRAME = ((-12, 30), (35, 65))
EUROPE_A3 = set(EUROPE_TAGS)
SMALL = {"HKG": (114.2, 22.3), "SGP": (103.8, 1.35)}  # too small for the 1:110m outlines


def bucket_color(fall, buckets=BUCKETS):
    for limit, col, _ in buckets[:-1]:
        if fall <= limit:
            return col
    return buckets[-1][1]


def _tag_box(x, y, text, size):
    w, h = 12 + len(text) * size * 0.52, size + 9
    return x - w / 2, y - h / 2, w, h


def _tag(x, y, text, fill="#fff", size=21):
    bx, by, w, h = _tag_box(x, y, text, size)
    return (f'<rect x="{bx:.0f}" y="{by:.0f}" width="{w:.0f}" height="{h:.0f}" rx="4" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>'
            f'<text x="{x:.0f}" y="{y + size * 0.36:.0f}" style="{HEAD}" font-size="{size}" text-anchor="middle" fill="{INK}">{text}</text>')


def place_tags(frame, items, size, bounds):
    """Draw value tags without overlaps. items = [(text, (lon, lat) tag, (lon, lat) anchor or None)].
    A tag that would overlap an earlier one is nudged to the nearest free spot and gets a leader line."""
    x0, y0, x1, y1 = bounds
    placed, out = [], []
    step = size + 12
    offsets = [(0, 0)] + [(dx * k, dy * k) for k in (1, 2, 3) for dx, dy in
                          ((0, -1), (0, 1), (1.4, 0), (-1.4, 0), (1.2, -1), (-1.2, -1), (1.2, 1), (-1.2, 1))]
    free = lambda b: (b[0] >= x0 + 2 and b[1] >= y0 + 2 and b[0] + b[2] <= x1 - 2 and b[1] + b[3] <= y1 - 2
                      and all(b[0] + b[2] + 3 < p[0] or p[0] + p[2] + 3 < b[0] or b[1] + b[3] + 2 < p[1] or p[1] + p[3] + 2 < b[1]
                              for p in placed))
    for text, pos, anchor in items:
        px, py = frame(*pos)
        for dx, dy in offsets:
            box = _tag_box(px + dx * step, py + dy * step, text, size)
            if free(box):
                break
        placed.append(box)
        tx, ty = box[0] + box[2] / 2, box[1] + box[3] / 2
        ax, ay = frame(*(anchor or pos))
        if anchor or (abs(tx - px) > 1 or abs(ty - py) > 1):
            out.insert(0, f'<line x1="{ax:.0f}" y1="{ay:.0f}" x2="{tx:.0f}" y2="{ty:.0f}" stroke="{INK}" stroke-width="2"/>'
                          f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="3" fill="{INK}"/>')
        out.append(_tag(tx, ty, text, size=size))
    return "".join(out)


def map_page(st):
    t, F = st.MAP_TEXT, st.FALLS
    buckets = getattr(st, "MAP_BUCKETS", BUCKETS)
    color = lambda f: bucket_color(f, buckets)
    mk = {m["a3"]: m for m in F["markets"]}
    style = lambda a3: (f'fill="{color(mk[a3]["fall_pct"])}" stroke="{INK}" stroke-width="1.2"' if a3 in mk
                        else f'fill="{NO_DATA}" stroke="#9c927a" stroke-width="0.8"')
    hatch = lambda a3: ('fill="url(#dots)" stroke="none"' if a3 in mk else 'fill="url(#hatch)" stroke="none"')
    mark = lambda m: ("‡" if m["freq"] == "monthly" else "") + ("†" if m["note"] else "")

    fx, fy, fw, fh = 26, 186, 788, 380
    world = Frame(fx, fy, fw, fh, lon=(-168, 190), lat=(-50, 78))
    tags = [place_tags(world, [(f'{mk[a3]["fall_pct"]:.0f}%', pos, anchor) for a3, (pos, anchor) in WORLD_TAGS.items() if a3 in mk],
                       20, (fx, fy, fx + fw, fy + fh))]
    small = "".join(f'<circle cx="{world(*p)[0]:.1f}" cy="{world(*p)[1]:.1f}" r="6" fill="{color(mk[a3]["fall_pct"])}" '
                    f'stroke="{INK}" stroke-width="2"/>' for a3, p in SMALL.items() if a3 in mk)
    elon, elat = EUROPE_FRAME
    ex0, ey0 = world(elon[0], elat[1])
    ex1, ey1 = world(elon[1], elat[0])
    europe_box = (f'<rect x="{ex0:.0f}" y="{ey0:.0f}" width="{ex1 - ex0:.0f}" height="{ey1 - ey0:.0f}" fill="none" '
                  f'stroke="{INK}" stroke-width="2.5" stroke-dasharray="6 4"/>'
                  f'<text x="{ex0:.0f}" y="{ey0 - 6:.0f}" style="{HEAD}" font-size="16" fill="{INK}">EUROPE: SEE BELOW</text>')
    extra = ""
    if t.get("burst"):  # (label, value, burst position, point it calls out) — e.g. a country too small to tag
        label, val, pos, anchor = t["burst"]
        bx, by = world(*pos)
        ax, ay = world(*anchor)
        extra = (f'<line x1="{ax:.0f}" y1="{ay:.0f}" x2="{bx:.0f}" y2="{by:.0f}" stroke="{INK}" stroke-width="2.5"/>'
                 + f'<circle cx="{ax:.0f}" cy="{ay:.0f}" r="4" fill="{INK}"/>'
                 + art.burst(bx, by, 46, "", points=12, fill=YELLOW)
                 + f'<text x="{bx:.0f}" y="{by - 4:.0f}" style="{HEAD}" font-size="15" text-anchor="middle" fill="{INK}">{label}</text>'
                 + f'<text x="{bx:.0f}" y="{by + 18:.0f}" style="{HEAD}" font-size="22" text-anchor="middle" fill="{RED}">{val}</text>')
    world_map = (f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="#cfe8f5"/>'
                 f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="url(#dots)"/>'
                 + country_paths(world, style) + country_paths(world, hatch) + small + europe_box + "".join(tags) + extra)

    ix, iy, iw, ih = 26, 584, 386, 420
    eu = Frame(ix, iy, iw, ih, lon=elon, lat=elat)
    eu_tags = place_tags(eu, [(f'{mk[a3]["fall_pct"]:.0f}%', pos, anchor) for a3, (pos, anchor) in EUROPE_TAGS.items() if a3 in mk],
                         14, (ix, iy + 32, ix + iw, iy + ih))
    inset = (f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" fill="#cfe8f5"/>'
             + country_paths(eu, style) + country_paths(eu, hatch) + eu_tags
             + f'<rect x="{ix}" y="{iy}" width="112" height="30" fill="{INK}"/>'
             + f'<text x="{ix + 10}" y="{iy + 22}" style="{HEAD}" font-size="20" fill="{YELLOW}">EUROPE</text>')

    rx, ry, rw = 428, 584, 386
    rows = sorted(F["markets"], key=lambda m: m["fall_pct"])
    ncol = 2 if len(rows) > 24 else 1
    per = math.ceil(len(rows) / ncol)
    rh = (ih - 50) / per
    colw = rw / ncol
    fs = 10.5 if ncol == 2 else 12.5
    worst = min(m["fall_pct"] for m in rows)
    bars = [f'<rect x="{rx}" y="{ry}" width="{rw}" height="{ih}" fill="#fff"/>',
            f'<text x="{rx + 12}" y="{ry + 28}" style="{HEAD}" font-size="22" fill="{INK}">THE FALLS, RANKED</text>']
    for i, m in enumerate(rows):
        c, k = divmod(i, per)
        x0 = rx + c * colw
        y = ry + 40 + k * rh
        name_w = 96 if ncol == 2 else 122
        bw = (colw - name_w - 40) * m["fall_pct"] / worst
        bars.append(f'<text x="{x0 + 8}" y="{y + rh - 3:.1f}" style="{BODY}" font-size="{fs}" font-weight="700" fill="{INK}">{escape(m["country"])}{mark(m)}</text>'
                    f'<rect x="{x0 + name_w}" y="{y + 2:.1f}" width="{bw:.1f}" height="{rh - 4:.1f}" fill="{color(m["fall_pct"])}" stroke="{INK}" stroke-width="1.2"/>'
                    f'<text x="{x0 + name_w + 4 + bw:.1f}" y="{y + rh - 3:.1f}" style="{BODY}" font-size="{fs}" font-weight="700" fill="{INK}">{m["fall_pct"]:.0f}%</text>')

    legend = [f'<text x="30" y="1030" style="{HEAD}" font-size="17" fill="{INK}">INDEX FALL:</text>']
    lx = 122
    for _, col, label in buckets + [(None, NO_DATA, "no data used")]:
        legend.append(f'<rect x="{lx}" y="1016" width="18" height="17" fill="{col}" stroke="{INK}" stroke-width="2"/>'
                      + (f'<rect x="{lx}" y="1016" width="18" height="17" fill="url(#hatch)"/>' if col == NO_DATA else "")
                      + f'<text x="{lx + 23}" y="1030" style="{BODY}" font-size="12.5" font-weight="700" fill="{INK}">{label}</text>')
        lx += 32 + len(label) * 6.6

    cap, _ = art.caption(26, 112, 788, t["intro"], size=15)
    narr = (art.bear(64, 1160, s=0.34, mood="calm")
            + art.bubble(112, 1046, 330, t["bear"], tail=(92, 1066), size=14)
            + art.penny(782, 1160, s=0.34, mood="shock")
            + art.bubble(478, 1046, 260, t["penny"], tail=(760, 1064), size=14)
            + (art.bubble(112, 1088, 600, t["bear2"], tail=(92, 1110), size=13) if t.get("bear2") else ""))
    foot = "".join(f'<text x="34" y="{H - 22 + i * 13}" style="{BODY}" font-size="11" fill="{INK}" fill-opacity="0.75">{escape(line)}</text>'
                   for i, line in enumerate(t["foot"]))
    body = (art.title(W / 2, 90, t.get("title", "WHO GOT HURT?"), size=80, fill=RED, rot=-2)
            + cap + art.panel(fx, fy, fw, fh, content=world_map)
            + art.panel(ix, iy, iw, ih, content=inset)
            + art.panel(rx, ry, rw, ih, content="".join(bars))
            + "".join(legend) + narr + foot
            + f'<text x="{W - 34}" y="{H - 10}" style="{HEAD}" font-size="18" text-anchor="end" fill="{INK}">{page_no(st, "map")}</text>')
    return page(body)


# ---- fixing the rules ------------------------------------------------------------------------

def fixing_rules(st):
    t = st.POLICY_TEXT
    hd, top = head(t.get("title", "FIXING THE RULES"), t["intro"], fill=BLUE)
    out = [hd]
    cw, ch, gap = 252, 232, 16
    for i, (code, country, law, when, text, _) in enumerate(st.POLICIES):
        x = 26 + (i % 3) * (cw + gap)
        y = top + 22 + (i // 3) * (ch + gap)
        badge, bw = icons.date_badge(x + cw - 14 - (18 + len(when) * 9), y + 14, when, size=18)
        inner = (f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="#fff"/>'
                 + icons.flag(x + 50, y + 40, code, 0.9) + badge
                 + f'<text x="{x + 14}" y="{y + 88}" style="{BODY}" font-size="13" font-weight="700" fill="{INK}" fill-opacity="0.7">{escape(country.upper())}</text>'
                 + text_block(x + 14, y + 114, wrap(law, 21), size=22, family=HEAD, lh=1.05)
                 + text_block(x + 14, y + 114 + len(wrap(law, 21)) * 23 + 6, text, size=14, width=31, weight="700"))
        out.append(art.panel(x, y, cw, ch, content=inner))
    y = top + 22 + 3 * (ch + gap)
    out.append(art.bear(80, H - 26, s=0.5, mood="calm")
               + art.bubble(150, y + 4, 470, t["bear"], tail=(120, y + 90), size=15)
               + art.penny(770, H - 26, s=0.5, mood="think", flip=True)
               + art.bubble(470, y + 112, 250, t["penny"], tail=(735, y + 150), size=15))
    return page("".join(out) + num_footer(page_no(st, "fixing-rules")))


# ---- what our warning lights said (the lesson) -----------------------------------------------

def lights(st):
    from config.signals import SIGNALS
    from config.crises import CRISES
    t = st.LIGHTS_TEXT
    cells = json.loads((ROOT / "tests" / "reference" / "scoreboard.json").read_text())[st.CRISIS_ID]
    crisis = next(c for c in CRISES if c["id"] == st.CRISIS_ID)
    hd, top = head("WHAT OUR WARNING LIGHTS SAID", t["intro"], size=56)
    style = {"early": (RED, "#fff", "WARNED", lambda m: f"{m} months early"),
             "chronic": ("#fca5a5", "#7f1d1d", "LONG ON", lambda m: f"on for {m} months"),
             "late": ("#d1d5db", INK, "TOO LATE", lambda m: f"{m} months after"),
             "none": ("#f3f4f6", "#6b7280", "NO SIGNAL", lambda m: "did not fire")}
    out = [hd]
    cw, chh, gap = 150, 150, 9.5
    for i, s in enumerate(SIGNALS):
        c = cells[s["id"]]
        bg, fg, word, detail = style[c["state"]]
        x = 26 + (i % 5) * (cw + gap)
        y = top + 24 + (i // 5) * (chh + gap)
        if c["months"] == 1:
            detail = {"early": lambda m: "1 month early", "late": lambda m: "1 month after"}.get(c["state"], detail)
        inner = (f'<rect x="{x}" y="{y}" width="{cw}" height="{chh}" fill="{bg}"/>'
                 + f'<circle cx="{x + 26}" cy="{y + 28}" r="14" fill="{YELLOW if c["state"] in ("early", "chronic") else "#9ca3af"}" stroke="{INK}" stroke-width="3"/>'
                 + text_block(x + 12, y + 72, wrap(s["name"], 14), size=19, family=HEAD, fill=fg, lh=1.05)
                 + f'<text x="{x + 12}" y="{y + chh - 32}" style="{HEAD}" font-size="22" fill="{fg}">{word}</text>'
                 + f'<text x="{x + 12}" y="{y + chh - 12}" style="{BODY}" font-size="13" font-weight="700" fill="{fg}">{detail(c["months"])}</text>')
        out.append(art.panel(x, y, cw, chh, content=inner))
    y = top + 24 + 2 * (chh + gap) + 10
    summ, sh = art.caption(26, y, 788, t["summary"], size=16, fill="#fff")
    les, lh = art.caption(26, y + sh + 18, 788, "THE LESSON: " + crisis["lesson"], size=20, fill=YELLOW)
    yy = y + sh + lh + 40
    out += [summ, les,
            art.penny(170, H - 40, s=0.72, mood="think"),
            art.bubble(60, yy + 20, 320, t["penny"], tail=(175, H - 250), size=18),
            art.bear(660, H - 40, s=0.72, mood="calm", flip=True),
            art.bubble(400, yy + 110, 330, t["bear"], tail=(640, H - 262), size=17)]
    if t.get("next"):
        out.append(f'<g transform="rotate(-4 700 {H - 60})"><rect x="560" y="{H - 92}" width="260" height="56" fill="{INK}"/>'
                   f'<text x="690" y="{H - 70}" style="{HEAD}" font-size="17" text-anchor="middle" fill="#fff">NEXT ISSUE:</text>'
                   f'<text x="690" y="{H - 46}" style="{HEAD}" font-size="22" text-anchor="middle" fill="{YELLOW}">{escape(t["next"])}</text></g>')
    out.append(num_footer(page_no(st, "lesson")))
    return page("".join(out))


# ---- sources ---------------------------------------------------------------------------------

def sources(st):
    out = [art.title(W / 2, 80, "SOURCES & NOTES", size=64, fill=BLUE, rot=-1)]
    y = 130
    cap, h = art.caption(26, y, 788, st.SOURCE_NOTE, size=14.5, fill="#fff")
    out.append(cap)
    y += h + 36
    for name, urls in st.SOURCE_GROUPS:
        out.append(f'<text x="30" y="{y}" style="{HEAD}" font-size="21" fill="{INK}">{escape(name.upper())}</text>')
        y += 20
        for u in dict.fromkeys(urls):
            for line in (part[k:k + 104] for part in wrap(u, 104) for k in range(0, len(part), 104)):
                out.append(f'<text x="40" y="{y}" style="{BODY}" font-size="12" fill="{INK}">{escape(line)}</text>')
                y += 15
        y += 10
    if y > H - 30:
        raise ValueError(f"sources page overflows ({y:.0f} > {H - 30})")
    out.append(num_footer(page_no(st, "sources")))
    return page("".join(out))

"""Inner pages of the Dot-com comic (2–7, 9–11). Words and sources live in dotcom_story.py."""
import json

from comics import art, icons
from comics.art import INK, RED, YELLOW, BLUE, ORANGE, HEAD, BODY, W, H, text_block, wrap
from comics.dotcom import _page, FALLS, DATA
from comics.dotcom_story import (GOOD_TIMES, BUBBLE_STEPS, TIMELINE_UP, TIMELINE_DOWN, PINS, POLICIES,
                                 EXTRA_SOURCES, INVENTIONS, INVENTION_NOTE, TECH_STATS, FED_STUDY)
from pipeline.load import ROOT

GREEN = icons.GREEN

# Reading order of the comic; page numbers are derived from it.
ORDER = ["cover", "tech", "good-times", "boom-to-bubble", "valuation", "timeline-up", "timeline-down",
         "what-popped", "map", "fixing-rules", "lesson", "sources"]


def page_no(name: str) -> int:
    return ORDER.index(name) + 1


def _num_footer(n):
    return f'<text x="{W - 30}" y="{H - 16}" style="{HEAD}" font-size="20" text-anchor="end" fill="{INK}">{n}</text>'


def _head(title, intro, size=74, y=88, rot=-2, fill=RED):
    cap, h = art.caption(26, y + 22, 788, intro, size=15)
    return art.title(W / 2, y, title, size=size, fill=fill, rot=rot) + cap, y + 22 + h


_ICON = {"chart": icons.chart_up, "worker": icons.worker, "tag": icons.price_tag, "piggy": icons.piggy,
         "computer": icons.computer, "capitol": icons.capitol, "rocket": icons.rocket, "cash": icons.cash_fire,
         "cable": icons.cable, "handshake": icons.handshake}


def _icon(name, cx, cy, s):
    if name == "tag":
        return icons.price_tag(cx, cy, s, "2%")
    if name == "handshake":
        return icons.handshake(cx, cy, s * 0.8)
    return _ICON[name](cx, cy, s)


# ---- the tech revolution (before the good times) ---------------------------------------------

def tech_revolution() -> str:
    from comics import tech_icons as ti
    head, top = _head("THE TECH REVOLUTION", "Where the good times came from: computers got cheap and powerful, "
                                             "and the internet linked them all together.", fill=BLUE)
    out = [head]

    # 1. inventions: icon medallions on a timeline
    n = len(INVENTIONS)
    step = 788 / n
    ly = top + 150
    out.append(f'<line x1="40" y1="{ly}" x2="{W - 40}" y2="{ly}" stroke="{INK}" stroke-width="6"/>')
    for i, (date, label, pic, _) in enumerate(INVENTIONS):
        cx = 26 + step * (i + 0.5)
        out.append(f'<circle cx="{cx:.0f}" cy="{top + 76}" r="52" fill="#fff" stroke="{INK}" stroke-width="5"/>'
                   + getattr(ti, pic)(cx, top + 76, 0.78)
                   + f'<line x1="{cx:.0f}" y1="{top + 128}" x2="{cx:.0f}" y2="{ly}" stroke="{INK}" stroke-width="4"/>')
        badge, bw = icons.date_badge(cx - 32, ly - 16, date, fill=BLUE, color="#fff", size=22)
        out.append(badge + text_block(cx, ly + 44, wrap(label, 12), size=19, family=HEAD, anchor="middle", lh=1.05))
    out.append(f'<text x="{W / 2}" y="{ly + 98}" style="{BODY}" font-size="12" text-anchor="middle" fill="{INK}" '
               f'fill-opacity="0.7">{INVENTION_NOTE}</text>')

    # 2. four pictogram panels
    pw, ph, gap = 386, 222, 16
    y0 = ly + 118
    chips, prices, homes, phones = TECH_STATS
    panels = []
    # chips: drawn at a size that grows with the transistor count
    x, y = 26, y0
    inner = [f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="#fff"/>',
             text_block(x + 14, y + 32, ["MORE POWERFUL CHIPS"], size=25, family=HEAD)]
    base = y + ph - 40
    for j, (label, v) in enumerate(chips[2]):
        s = 1.25 * (v / 42) ** 0.5
        cx = x + 70 + j * 120
        inner.append(ti.chip(cx, base - 46 * s, s)
                     + f'<text x="{cx}" y="{base + 22}" style="{HEAD}" font-size="20" text-anchor="middle" fill="{INK}">{v:g}M</text>'
                     + f'<text x="{cx}" y="{base + 36}" style="{BODY}" font-size="12" font-weight="700" text-anchor="middle" fill="{INK}">{label}</text>')
    inner.append(art.burst(x + pw - 56, y + 60, 40, "x35", points=12, size=30))
    panels.append(art.panel(x, y, pw, ph, content="".join(inner)))
    # prices: same computer, shrinking price tag
    x = 26 + pw + gap
    inner = [f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="#fff"/>',
             text_block(x + 14, y + 32, ["CHEAPER COMPUTERS"], size=25, family=HEAD)]
    for j, (label, v) in enumerate(prices[2]):
        cx = x + 70 + j * 120
        inner.append(ti.pc(cx, y + 110, 0.9) + ti.tag(cx + 6, y + 160, 0.5 + 0.5 * v / 100, f"{v:g}", fill=YELLOW)
                     + f'<text x="{cx}" y="{y + ph - 12}" style="{BODY}" font-size="13" font-weight="700" text-anchor="middle" fill="{INK}">{label}</text>')
    inner.append(art.burst(x + pw - 52, y + 50, 40, "-61%", points=12, size=24))
    panels.append(art.panel(x, y, pw, ph, content="".join(inner)))
    # homes and phones: rows of pictograms filled in proportion
    for k, (stat, title_txt, draw, iw, legend) in enumerate(
            [(homes, "HOMES WITH A COMPUTER", ti.house, 48, "each house = 10% of homes"),
             (phones, "MOBILE PHONES", ti.mobile, 26, "each phone = 10 per 100 people")]):
        x = 26 + k * (pw + gap)
        y = y0 + ph + gap
        inner = [f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="#fff"/>',
                 text_block(x + 14, y + 32, [title_txt], size=25, family=HEAD)]
        for j, (label, v) in enumerate(stat[2]):
            ry = y + 74 + j * 50
            inner.append(f'<text x="{x + 14}" y="{ry + 7}" style="{HEAD}" font-size="18" fill="{INK}">{label}</text>'
                         + ti.pictogram_row(x + 82, ry, 10, v / 100, draw, 25, stat[3], iw=iw, s=0.5)
                         + f'<text x="{x + pw - 14}" y="{ry + 9}" style="{HEAD}" font-size="26" text-anchor="end" fill="{stat[3]}" '
                           f'stroke="{INK}" stroke-width="1.2" paint-order="stroke">{v:g}{"%" if k == 0 else ""}</text>')
        inner.append(f'<text x="{x + 14}" y="{y + ph - 10}" style="{BODY}" font-size="12" font-weight="700" fill="{INK}" fill-opacity="0.7">{legend}</text>')
        panels.append(art.panel(x, y, pw, ph, content="".join(inner)))
    out += panels

    # 3. the chain from technology to the good times, as pictures
    y = y0 + 2 * (ph + gap) + 4
    chain = [(ti.chip, "CHEAP, FAST COMPUTERS"), (ti.office, "IN EVERY OFFICE"),
             (ti.gauge, "MORE OUTPUT"), (ti.sun, "THE GOOD TIMES")]
    bw, ag = 170, 36
    for i, (draw, label) in enumerate(chain):
        x = 26 + i * (bw + ag)
        fill = "#d7f0dc" if i == len(chain) - 1 else "#fff6cc"
        out.append(f'<rect x="{x + 4}" y="{y + 4}" width="{bw}" height="128" rx="14" fill="{INK}"/>'
                   f'<rect x="{x}" y="{y}" width="{bw}" height="128" rx="14" fill="{fill}" stroke="{INK}" stroke-width="3.5"/>'
                   + draw(x + bw / 2, y + 52, 0.75)
                   + f'<text x="{x + bw / 2}" y="{y + 116}" style="{HEAD}" font-size="18" text-anchor="middle" fill="{INK}">{label}</text>')
        if i < len(chain) - 1:
            ax = x + bw + 6
            out.append(f'<path d="M{ax},{y + 56} L{ax + 12},{y + 56} L{ax + 12},{y + 46} L{ax + 26},{y + 64} '
                       f'L{ax + 12},{y + 82} L{ax + 12},{y + 72} L{ax},{y + 72} Z" fill="{INK}"/>')

    # 4. the Fed finding as a pie, plus the narrators
    y += 146
    out.append(ti.pie(84, y + 52, 46, 2 / 3, color=BLUE)
               + f'<text x="84" y="{y + 60}" style="{HEAD}" font-size="24" text-anchor="middle" fill="#fff" stroke="{INK}" stroke-width="1" paint-order="stroke">2/3</text>'
               + text_block(146, y + 34, wrap("of the late-1990s productivity speed-up came from making and using "
                                              "computers (Federal Reserve economists)", 44), size=15.5, weight="700")
               + art.bear(640, H - 18, s=0.34, mood="calm")
               + art.penny(770, H - 18, s=0.34, mood="happy", flip=True)
               + art.bubble(470, y - 2, 150, "Real inventions. Real gains.", tail=(622, y + 70), size=14))
    return _page("".join(out) + _num_footer(page_no("tech")))


# ---- page 2 ----------------------------------------------------------------------------------

def _sym(name):
    """Look up a drawing function by name across the icon modules."""
    from comics import symbols, tech_icons
    special = {"chart_up": icons.chart_up, "rocket": icons.rocket, "capitol": icons.capitol,
               "cash": icons.cash_fire, "handshake": lambda cx, cy, s: icons.handshake(cx, cy, s * 0.75)}
    if name in special:
        return special[name]
    return getattr(symbols, name, None) or getattr(tech_icons, name)


def _productivity_panel(x, y, pw, ph):
    """Output per hour, 1973–2000, with the two growth eras shaded, plus 'same hour, more output' bars."""
    pts = json.loads((DATA / "productivity.json").read_text(encoding="utf-8"))["points"]
    cx0, cx1, cy0, cy1 = x + 14, x + 250, y + 52, y + 196
    lo, hi = 70, 120
    X = lambda i: cx0 + (cx1 - cx0) * i / (len(pts) - 1)
    Y = lambda v: cy1 - (cy1 - cy0) * (v - lo) / (hi - lo)
    i95 = next(i for i, (d, _) in enumerate(pts) if d == "1995-10")
    line = " ".join(f"{'M' if i == 0 else 'L'}{X(i):.1f},{Y(v):.1f}" for i, (_, v) in enumerate(pts))
    out = [f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="#fffdf3"/>',
           text_block(x + 14, y + 30, ["WORKERS GOT MORE PRODUCTIVE"], size=21, family=HEAD),
           f'<rect x="{cx0}" y="{cy0}" width="{X(i95) - cx0:.1f}" height="{cy1 - cy0}" fill="#e5e7eb"/>',
           f'<rect x="{X(i95):.1f}" y="{cy0}" width="{cx1 - X(i95):.1f}" height="{cy1 - cy0}" fill="#d7f0dc"/>',
           f'<path d="{line}" fill="none" stroke="{INK}" stroke-width="3.5"/>',
           f'<line x1="{cx0}" y1="{cy1}" x2="{cx1}" y2="{cy1}" stroke="{INK}" stroke-width="2.5"/>',
           f'<text x="{cx0 + 8}" y="{cy0 + 22}" style="{HEAD}" font-size="19" fill="#4b5563">1973–95: +1.4% A YEAR</text>',
           f'<text x="{cx0 + 8}" y="{cy0 + 46}" style="{HEAD}" font-size="19" fill="{GREEN}" stroke="{INK}" stroke-width="0.8" '
           f'paint-order="stroke">1995–2000: +3.0% A YEAR →</text>',
           f'<text x="{cx0}" y="{cy1 + 18}" style="{BODY}" font-size="11.5" font-weight="700" fill="{INK}">1973</text>',
           f'<text x="{cx1}" y="{cy1 + 18}" style="{BODY}" font-size="11.5" font-weight="700" text-anchor="end" fill="{INK}">2000</text>']
    # same hour of work, more output: 1995 vs 2000 (index 100 -> 116)
    v95, v00 = 100, round(pts[-1][1])
    bx, base = x + 270, cy1
    for k, (lab, v, col) in enumerate([("1995", v95, "#9ca3af"), ("2000", v00, GREEN)]):
        bh = (base - cy0 - 56) * v / 120
        out.append(f'<rect x="{bx + k * 54}" y="{base - bh:.0f}" width="40" height="{bh:.0f}" fill="{col}" stroke="{INK}" stroke-width="3"/>'
                   f'<text x="{bx + 20 + k * 54}" y="{base - bh - 6:.0f}" style="{HEAD}" font-size="20" text-anchor="middle" fill="{INK}">{v}</text>'
                   f'<text x="{bx + 20 + k * 54}" y="{base + 18}" style="{BODY}" font-size="11.5" font-weight="700" text-anchor="middle" fill="{INK}">{lab}</text>')
    out.append(f'<text x="{bx + 47}" y="{cy0 + 2}" style="{HEAD}" font-size="14" text-anchor="middle" fill="{INK}">OUTPUT FROM</text>'
               f'<text x="{bx + 47}" y="{cy0 + 18}" style="{HEAD}" font-size="14" text-anchor="middle" fill="{INK}">1 HOUR OF WORK</text>')
    out.append(f'<text x="{x + 14}" y="{y + ph - 12}" style="{BODY}" font-size="12" font-weight="700" fill="{INK}" fill-opacity="0.75">'
               f'Output per hour, US firms (1995 = 100). Same hour: +16% by 2000.</text>')
    return "".join(out)


def good_times() -> str:
    head, top = _head("THE GOOD TIMES", "Before the bubble, the US economy really was booming. These true facts made "
                                        "people believe the boom could go on forever.", fill=GREEN)
    out = [head]
    pw, ph, gap = 386, 248, 16
    for i, (big, title, text, icon, _) in enumerate(GOOD_TIMES):
        x = 26 + (i % 2) * (pw + gap)
        y = top + 18 + (i // 2) * (ph + gap)
        if i == 0:
            out.append(art.panel(x, y, pw, ph, fill="#fffdf3", content=_productivity_panel(x, y, pw, ph)))
            continue
        inner = (f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="url(#dots)"/>'
                 + _icon(icon, x + 74, y + 78, 0.95)
                 + f'<text x="{x + pw - 16}" y="{y + 66}" style="{HEAD}" font-size="{50 if len(big) < 7 else 40}" text-anchor="end" fill="{GREEN}" stroke="{INK}" stroke-width="2" paint-order="stroke">{big}</text>'
                 + text_block(x + 150, y + 100, wrap(title, 22), size=21, family=HEAD, lh=1.1)
                 + text_block(x + 18, y + 158, text, size=15.5, width=44, weight="700"))
        out.append(art.panel(x, y, pw, ph, fill="#fffdf3", content=inner))
    y = top + 18 + 3 * (ph + gap)
    out.append(art.penny(110, H - 24, s=0.5, mood="happy")
               + art.bubble(176, y + 6, 300, "It's a NEW ECONOMY! Shares can only go up!", tail=(140, y + 70), size=17)
               + art.bear(740, H - 24, s=0.5, mood="calm", flip=True)
               + art.bubble(400, y + 70, 300, "The good news was REAL. That's what made the bubble so convincing.",
                            tail=(700, y + 100), size=16))
    return _page("".join(out) + _num_footer(page_no("good-times")))


# ---- page 3 ----------------------------------------------------------------------------------

def _step_badge(x, y, n):
    return (f'<circle cx="{x}" cy="{y}" r="17" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
            f'<text x="{x}" y="{y + 8}" style="{HEAD}" font-size="22" text-anchor="middle" fill="#fff">{n}</text>')


def boom_to_bubble() -> str:
    from comics import symbols
    head, top = _head("FROM BOOM TO BUBBLE", "Real progress turned into wild hope. Step by step, share prices "
                                             "raced far ahead of the profits behind them.")
    out = [head]
    pw, ph, gap = 386, 200, 14
    for i, (date, title, text, icon, _) in enumerate(BUBBLE_STEPS[:4]):
        x = 26 + (i % 2) * (pw + gap)
        y = top + 24 + (i // 2) * (ph + gap)
        badge, _ = icons.date_badge(x + 14, y + 12, date, size=20)
        inner = (f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="#fff"/>'
                 + badge + _icon(icon, x + pw - 62, y + 64, 0.66)
                 + text_block(x + 16, y + 78, wrap(title, 22), size=24, family=HEAD, lh=1.05)
                 + text_block(x + 16, y + 112 + (len(wrap(title, 22)) - 1) * 24, text, size=14.5, width=46, weight="700"))
        out.append(art.panel(x, y, pw, ph, content=inner) + _step_badge(x + pw - 18, y + ph - 18, i + 1))
    fw = 788
    # 5. fibre: strands of cable, only one lit
    date, title, text, _, _ = BUBBLE_STEPS[4]
    x, y, fh = 26, top + 24 + 2 * (ph + gap), 214
    badge, _ = icons.date_badge(x + 14, y + 12, date, size=20)
    inner = (f'<rect x="{x}" y="{y}" width="{fw}" height="{fh}" fill="#fff"/>' + badge
             + f'<rect x="{x + 14}" y="{y + 52}" width="236" height="150" rx="10" fill="#1f2937"/>'
             + symbols.fibre_bundle(x + 26, y + 66, 212, n=18)
             + f'<text x="{x + 132}" y="{y + 196}" style="{HEAD}" font-size="18" text-anchor="middle" fill="{YELLOW}">ONLY ~2–5% LIT (IN USE)</text>'
             + text_block(x + 270, y + 40, [title.upper()], size=26, family=HEAD)
             + text_block(x + 270, y + 72, text, size=15, width=60, weight="700")
             + symbols.bankrupt(x + fw - 60, y + 60, 0.62))
    out.append(art.panel(x, y, fw, fh, content=inner) + _step_badge(x + fw - 18, y + fh - 18, 5))
    # 6. AOL + Time Warner: small business, huge share price
    date, title, text, _, _ = BUBBLE_STEPS[5]
    y = y + fh + gap
    ah = 228
    badge, _ = icons.date_badge(x + 14, y + 12, date, size=20)
    bars = []
    for k, (lab, aol, tw, note) in enumerate([("REVENUE", 1, 5.4, "AOL: less than 1/5"), ("SHARE VALUE", 2, 1, "AOL: almost 2x")]):
        by = y + 64 + k * 74
        bars.append(f'<text x="{x + 16}" y="{by}" style="{HEAD}" font-size="17" fill="{INK}">{lab}</text>'
                    f'<text x="{x + 16}" y="{by + 24}" style="{HEAD}" font-size="15" fill="{BLUE}">AOL</text>'
                    f'<rect x="{x + 52}" y="{by + 8}" width="{32 * aol:.0f}" height="20" fill="{BLUE}" stroke="{INK}" stroke-width="2.5"/>'
                    f'<text x="{x + 16}" y="{by + 48}" style="{HEAD}" font-size="15" fill="{RED}">TW</text>'
                    f'<rect x="{x + 52}" y="{by + 32}" width="{32 * tw:.0f}" height="20" fill="{RED}" stroke="{INK}" stroke-width="2.5"/>'
                    f'<text x="{x + 246}" y="{by}" style="{BODY}" font-size="12" font-weight="700" text-anchor="end" fill="{INK}">{note}</text>')
    inner = (f'<rect x="{x}" y="{y}" width="{fw}" height="{ah}" fill="#fff"/>' + badge + "".join(bars)
             + text_block(x + 270, y + 40, [title.upper()], size=26, family=HEAD)
             + text_block(x + 270, y + 72, text, size=15, width=60, weight="700")
             + art.burst(x + fw - 78, y + ah - 62, 50, "", points=14, fill=YELLOW)
             + f'<text x="{x + fw - 78}" y="{y + ah - 64}" style="{HEAD}" font-size="18" text-anchor="middle" fill="{RED}">-$98.7BN</text>'
             + f'<text x="{x + fw - 78}" y="{y + ah - 46}" style="{HEAD}" font-size="14" text-anchor="middle" fill="{INK}">LOSS, 2002</text>')
    out.append(art.panel(x, y, fw, ah, content=inner) + _step_badge(x + fw - 18, y + 22, 6))
    y += ah + 10
    out.append(art.penny(60, H - 14, s=0.3, mood="happy")
               + art.bubble(100, y, 320, "Everyone I know is getting rich. I'm buying too!", tail=(80, y + 44), size=14)
               + art.bear(772, H - 14, s=0.3, mood="stern", flip=True)
               + art.bubble(430, y, 300, "Prices were rising because prices were rising.", tail=(748, y + 44), size=14))
    return _page("".join(out) + _num_footer(page_no("boom-to-bubble")))


# ---- page 4 ----------------------------------------------------------------------------------

def _hot_thermometer(x, y, h, value, vmax, marks):
    """Thermometer whose liquid deepens from yellow (cool) to dark red (record hot)."""
    w = 50
    top_y, bot_y = y + 10, y + h - 40
    fill_h = (bot_y - top_y) * min(value, vmax) / vmax
    grad = (f'<defs><linearGradient id="hot" gradientUnits="userSpaceOnUse" x1="0" y1="{bot_y + 40}" x2="0" y2="{top_y}">'
            f'<stop offset="0" stop-color="#ffe066"/><stop offset="0.3" stop-color="#ffb020"/>'
            f'<stop offset="0.6" stop-color="#f4511e"/><stop offset="0.85" stop-color="#c62828"/>'
            f'<stop offset="1" stop-color="#6d0f0f"/></linearGradient></defs>')
    out = [grad,
           f'<rect x="{x - w / 2}" y="{y}" width="{w}" height="{h - 30}" rx="{w / 2}" fill="#fff" stroke="{INK}" stroke-width="5"/>',
           f'<rect x="{x - 14}" y="{bot_y - fill_h:.0f}" width="28" height="{fill_h + 40:.0f}" fill="url(#hot)"/>',
           f'<circle cx="{x}" cy="{y + h - 20}" r="42" fill="#ffe066" stroke="{INK}" stroke-width="5"/>',
           f'<rect x="{x - 14}" y="{bot_y - 10}" width="28" height="30" fill="#ffe066"/>']
    for v, label, col in marks:
        ty = bot_y - (bot_y - top_y) * v / vmax
        out.append(f'<line x1="{x + w / 2}" y1="{ty:.0f}" x2="{x + w / 2 + 24}" y2="{ty:.0f}" stroke="{INK}" stroke-width="4"/>'
                   f'<text x="{x + w / 2 + 32}" y="{ty + 9:.0f}" style="{HEAD}" font-size="28" fill="{col}" stroke="{INK}" stroke-width="0.8" paint-order="stroke">{v:.1f}</text>'
                   + text_block(x + w / 2 + 100, ty + 6, label if isinstance(label, list) else [label], size=16, weight="700", lh=1.15))
    return "".join(out)


def valuation() -> str:
    head, top = _head("PRICED FOR PERFECTION", "How expensive were shares? The Shiller CAPE compares share prices "
                                               "with 10 years of company profits, adjusted for inflation. Higher = hotter.")
    th = _hot_thermometer(130, top + 36, 720, 44.2, 46,
                          [(14.8, ["Long-run average,", "1881–1995"], "#ffb020"),
                           (20.2, ["January 1995,", "the boom begins"], "#ff8f00"),
                           (32.6, ["Sept 1929: the OLD record,", "just before the Great Crash"], "#d84315"),
                           (44.2, ["Dec 1999: NEW", "ALL-TIME RECORD"], "#8e0000")])
    why, wh = art.caption(470, top + 300, 340, "WHY 1929? It was the highest CAPE ever seen before the 1990s. Weeks "
                                               "later came the Wall Street Crash and the Great Depression. In 1999 that "
                                               "old danger mark was beaten by more than a third.", size=15, fill="#fff")
    explain, eh = art.caption(470, top + 316 + wh, 340, "A CAPE of 44 means paying $44 for every $1 of yearly profit "
                                                        "(averaged over 10 years). At the long-run average, people paid about $15.",
                              size=15, fill="#fff")
    light, lh = art.caption(470, top + 332 + wh + eh, 340, "Our \"stocks expensive\" light (CAPE above 25) had been ON "
                                                           "for 43 months when the market peaked.", size=15, fill=YELLOW)
    body = (head + th + art.burst(690, top + 110, 86, "RECORD!", points=16, size=38)
            + why + explain + light
            + art.penny(470, H - 30, s=0.46, mood="shock")
            + art.bubble(180, H - 250, 260, "So everyone KNEW shares were expensive?", tail=(445, H - 165), size=15)
            + art.bear(740, H - 30, s=0.46, mood="calm", flip=True)
            + art.bubble(530, H - 288, 290, "Yes! Seeing that shares are expensive is easy. Knowing WHEN prices will fall is the hard part.",
                         tail=(720, H - 195), size=15)
            + _num_footer(page_no("valuation")))
    return _page(body)


# ---- pages 5-6: timeline (time runs UP the page) ---------------------------------------------

def _crash_tag(cx, cy, label):
    """Red rubber-stamp label marking the crash on a timeline card."""
    w = len(label) * 11.5 + 30
    return (f'<g transform="rotate(-7 {cx} {cy})">'
            f'<rect x="{cx - w / 2 + 4:.0f}" y="{cy - 15}" width="{w:.0f}" height="32" fill="{INK}"/>'
            f'<rect x="{cx - w / 2:.0f}" y="{cy - 19}" width="{w:.0f}" height="32" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
            f'<text x="{cx}" y="{cy + 5}" style="{HEAD}" font-size="21" text-anchor="middle" fill="#fff" '
            f'letter-spacing="1">{label}</text></g>')


def _timeline(title, events, n, intro, fill):
    head, top = _head(title, intro, size=60, fill=fill)
    cx = W / 2
    y_top, y_bot = top + 56, H - 40
    step = (y_bot - y_top) / len(events)
    out = [head,
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
                   + f'<circle cx="{x + cw - 46}" cy="{y + h / 2 + 4:.0f}" r="38" fill="#f6f3ea" stroke="{INK}" stroke-width="2.5"/>'
                   + _sym(icon)(x + cw - 46, y + h / 2 + 4, 0.56)
                   + (_crash_tag(x + cw - (64 if not left else 120), y - 4, tag[0]) if tag else ''))
    return _page("".join(out) + _num_footer(n))


def timeline_up() -> str:
    return _timeline("TIMELINE PART 1: UP, UP...", TIMELINE_UP, page_no("timeline-up"),
                     "Read from the bottom up. Green = good news, red = trouble, blue = a warning. Red stamp = the crash.", GREEN)


def timeline_down() -> str:
    return _timeline("PART 2: ...AND DOWN!", TIMELINE_DOWN, page_no("timeline-down"),
                     "Read from the bottom up. The crash proper: 10 Mar 2000 to 9 Oct 2002 (red stamps).", RED)


# ---- page 7 ----------------------------------------------------------------------------------

def what_popped() -> str:
    import math
    from comics import symbols
    head, top = _head("WHAT POPPED IT?", "No single event burst the bubble. Six pins pressed in, one after another:")
    bx, by, r = W / 2, top + 196, 118
    heads = [(-268, -128), (268, -128), (-318, 26), (318, 26), (-226, 168), (226, 168)]
    dirs = [math.atan2(dy / 1.12, dx) for dx, dy in heads]
    glow = f'<circle cx="{bx}" cy="{by}" r="{r + 96}" fill="{YELLOW}" opacity="0.35"/>'
    balloon, contacts = symbols.stressed_balloon(bx, by, r, ".COM", dirs)
    needles = "".join(symbols.needle(bx + dx, by + dy, tx, ty, i + 1) for i, ((dx, dy), (tx, ty)) in enumerate(zip(heads, contacts)))
    sfx = (f'<text x="{bx - 200}" y="{by - 138}" style="{HEAD}" font-size="30" fill="{RED}" stroke="{INK}" stroke-width="1.5" '
           f'paint-order="stroke" transform="rotate(-12 {bx - 200} {by - 138})">CREEEAK...</text>'
           f'<text x="{bx + 120}" y="{by - 142}" style="{HEAD}" font-size="26" fill="{INK}" transform="rotate(10 {bx + 120} {by - 142})">SQUEAK!</text>')
    out = [head, glow, balloon, needles, sfx]
    pw, ph, gap = 386, 152, 12
    y0 = by + 246
    for i, (ttl, text, icon) in enumerate(PINS):
        x = 26 + (i % 2) * (pw + gap)
        y = y0 + (i // 2) * (ph + gap)
        inner = (f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="#fff"/>'
                 f'<circle cx="{x + 30}" cy="{y + 30}" r="19" fill="{YELLOW}" stroke="{INK}" stroke-width="3"/>'
                 f'<text x="{x + 30}" y="{y + 38}" style="{HEAD}" font-size="24" text-anchor="middle" fill="{INK}">{i + 1}</text>'
                 + text_block(x + 60, y + 38, [ttl.upper()], size=24, family=HEAD)
                 + text_block(x + 16, y + 68, text, size=13.5, width=38, weight="700")
                 + f'<circle cx="{x + pw - 52}" cy="{y + 84}" r="40" fill="#f6f3ea" stroke="{INK}" stroke-width="2.5"/>'
                 + _sym(icon)(x + pw - 52, y + 84, 0.62))
        out.append(art.panel(x, y, pw, ph, content=inner))
    yb = y0 + 3 * (ph + gap) + 4
    out.append(art.bear(80, H - 22, s=0.38, mood="calm")
               + art.bubble(140, yb, 640, "Our warning lights: credit spreads and company borrowing switched on 18 months "
                                          "before the peak. The Fed-hiking light only fired 3 months after it.", tail=(110, yb + 60), size=15))
    return _page("".join(out) + _num_footer(page_no("what-popped")))


# ---- page 9 ----------------------------------------------------------------------------------

def fixing_rules() -> str:
    head, top = _head("FIXING THE RULES", "After the crash and the accounting scandals, governments rewrote the rules "
                                          "for companies, auditors and banks.", fill=BLUE)
    out = [head]
    cw, ch, gap = 252, 232, 16
    for i, (code, country, law, when, text, _) in enumerate(POLICIES):
        x = 26 + (i % 3) * (cw + gap)
        y = top + 22 + (i // 3) * (ch + gap)
        badge, bw = icons.date_badge(x + cw - 14 - (18 + len(when) * 9), y + 14, when, size=18)
        inner = (f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="#fff"/>'
                 + icons.flag(x + 50, y + 40, code, 0.9) + badge
                 + f'<text x="{x + 14}" y="{y + 88}" style="{BODY}" font-size="13" font-weight="700" fill="{INK}" fill-opacity="0.7">{country.upper()}</text>'
                 + text_block(x + 14, y + 114, wrap(law, 21), size=22, family=HEAD, lh=1.05)
                 + text_block(x + 14, y + 114 + len(wrap(law, 21)) * 23 + 6, text, size=14, width=31, weight="700"))
        out.append(art.panel(x, y, cw, ch, content=inner))
    y = top + 22 + 3 * (ch + gap)
    out.append(art.bear(80, H - 26, s=0.5, mood="calm")
               + art.bubble(150, y + 4, 470, "Notice something? Most of these rules target CHEATING: fake accounts and "
                                             "biased research. No law can stop people paying too much for exciting shares.",
                            tail=(120, y + 90), size=15)
               + art.penny(770, H - 26, s=0.5, mood="think", flip=True)
               + art.bubble(470, y + 112, 250, "So spotting the next bubble is up to us?", tail=(735, y + 150), size=15))
    return _page("".join(out) + _num_footer(page_no("fixing-rules")))


# ---- page 10 ---------------------------------------------------------------------------------

def lesson() -> str:
    from config.signals import SIGNALS
    from config.crises import CRISES
    cells = json.loads((ROOT / "tests" / "reference" / "scoreboard.json").read_text())["2000"]
    crisis = next(c for c in CRISES if c["id"] == "2000")
    head, top = _head("WHAT OUR WARNING LIGHTS SAID", "The same 10 rules we use for every crash, applied to the months "
                                                      "before the March 2000 peak.", size=56)
    style = {"early": (RED, "#fff", "WARNED", lambda m: f"{m} months early"),
             "chronic": ("#fca5a5", "#7f1d1d", "LONG ON", lambda m: f"on for {m} months"),
             "late": ("#d1d5db", INK, "TOO LATE", lambda m: f"{m} months after"),
             "none": ("#f3f4f6", "#6b7280", "NO SIGNAL", lambda m: "did not fire")}
    out = [head]
    cw, chh, gap = 150, 150, 9.5
    for i, s in enumerate(SIGNALS):
        c = cells[s["id"]]
        bg, fg, word, detail = style[c["state"]]
        x = 26 + (i % 5) * (cw + gap)
        y = top + 24 + (i // 5) * (chh + gap)
        inner = (f'<rect x="{x}" y="{y}" width="{cw}" height="{chh}" fill="{bg}"/>'
                 + f'<circle cx="{x + 26}" cy="{y + 28}" r="14" fill="{YELLOW if c["state"] in ("early", "chronic") else "#9ca3af"}" stroke="{INK}" stroke-width="3"/>'
                 + text_block(x + 12, y + 72, wrap(s["name"], 14), size=19, family=HEAD, fill=fg, lh=1.05)
                 + f'<text x="{x + 12}" y="{y + chh - 32}" style="{HEAD}" font-size="22" fill="{fg}">{word}</text>'
                 + f'<text x="{x + 12}" y="{y + chh - 12}" style="{BODY}" font-size="13" font-weight="700" fill="{fg}">{detail(c["months"])}</text>')
        out.append(art.panel(x, y, cw, chh, content=inner))
    y = top + 24 + 2 * (chh + gap) + 10
    n_early = sum(v["state"] == "early" for v in cells.values())
    summ, sh = art.caption(26, y, 788, f"{n_early} of 10 lights warned early: credit spreads and company borrowing "
                                       f"18 months ahead, oil 7 months ahead. Valuations had been flashing for years. "
                                       f"The yield curve, Fed hikes and falling profits only showed up after the peak.",
                           size=16, fill="#fff")
    les, lh = art.caption(26, y + sh + 18, 788, "THE LESSON: " + crisis["lesson"], size=20, fill=YELLOW)
    yy = y + sh + lh + 40
    out += [summ, les,
            art.penny(170, H - 40, s=0.72, mood="think"),
            art.bubble(60, yy + 20, 320, "A great story is not the same as a great price.", tail=(175, H - 250), size=18),
            art.bear(660, H - 40, s=0.72, mood="calm", flip=True),
            art.bubble(400, yy + 110, 330, "And a warning light tells you WHAT is wrong, not WHEN it ends.",
                       tail=(640, H - 262), size=17),
            f'<g transform="rotate(-4 700 {H - 60})"><rect x="560" y="{H - 92}" width="260" height="56" fill="{INK}"/>'
            f'<text x="690" y="{H - 70}" style="{HEAD}" font-size="17" text-anchor="middle" fill="#fff">NEXT ISSUE:</text>'
            f'<text x="690" y="{H - 46}" style="{HEAD}" font-size="22" text-anchor="middle" fill="{YELLOW}">2008 FINANCIAL CRISIS</text></g>',
            _num_footer(page_no("lesson"))]
    return _page("".join(out))


# ---- page 11 ---------------------------------------------------------------------------------

def sources() -> str:
    from comics.dotcom_story import GOOD_TIMES as G
    groups = [(f"The tech revolution (page {page_no('tech')})", [i[3] for i in INVENTIONS] + [t[5] for t in TECH_STATS] + [FED_STUDY[1]]),
              (f"The good times (page {page_no('good-times')})", [g[4] for g in G]),
              (f"From boom to bubble (page {page_no('boom-to-bubble')})", [b[4] for b in BUBBLE_STEPS]),
              (f"Fixing the rules (page {page_no('fixing-rules')})", [p[5] for p in POLICIES]),
              ("Timeline, triggers and data", EXTRA_SOURCES)]
    out = [art.title(W / 2, 80, "SOURCES & NOTES", size=64, fill=BLUE, rot=-1)]
    y = 130
    notes = ("Every number in this comic was checked against the sources below on 21 October 2026. Index falls use the "
             "highest daily close in 1999–2000 and the lowest close after it up to June 2003, in local currency. "
             "Productivity, jobs, prices, the budget and interest rates come from official US data (BLS, BEA, Treasury, "
             "Federal Reserve) via FRED. Characters are fictional. For education only, not investment advice.")
    cap, h = art.caption(26, y, 788, notes, size=14.5, fill="#fff")
    out.append(cap)
    y += h + 40
    for name, urls in groups:
        out.append(f'<text x="30" y="{y}" style="{HEAD}" font-size="22" fill="{INK}">{name.upper()}</text>')
        y += 22
        for u in dict.fromkeys(urls):
            for line in wrap(u, 100):
                out.append(f'<text x="40" y="{y}" style="{BODY}" font-size="12.5" fill="{INK}">{line}</text>')
                y += 16
        y += 14
    out.append(_num_footer(page_no("sources")))
    return _page("".join(out))

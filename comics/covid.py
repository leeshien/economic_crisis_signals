"""The 2020 Covid crash — comic pages. Facts and sources live in covid_story.py."""
from comics import art, icons, kit, crisis_icons as ci, tech_icons
from comics import covid_story as st
from comics.art import INK, RED, YELLOW, BLUE, ORANGE, HEAD, BODY, W, H, text_block, wrap
from comics.kit import GREEN, page, head, num_footer, medallion, step_badge, jargon

SLUG = st.SLUG
pno = lambda name: kit.page_no(st, name)


def _pts(name, start=None, end=None):
    return [(d, v) for d, v in st.SERIES[name]["points"] if (not start or d >= start) and (not end or d <= end)]


def _path(pts, X, Y):
    return " ".join(f"{'M' if i == 0 else 'L'}{X(i):.1f},{Y(v):.1f}" for i, (_, v) in enumerate(pts))


def _idx(pts, date):
    return next(i for i, (d, _) in enumerate(pts) if d.startswith(date))


# ---- page 1: cover ---------------------------------------------------------------------------

def cover() -> str:
    sp = _pts("sp_daily", "2019-11-01", "2020-09-30")
    x0, x1, yb, yt, lo, hi = 70, 770, 800, 470, 1600, 3600
    X = lambda i: x0 + (x1 - x0) * i / (len(sp) - 1)
    Y = lambda v: yb - (yb - yt) * (v - lo) / (hi - lo)
    line = _path(sp, X, Y)
    area = line + f" L{X(len(sp) - 1):.1f},{yb} L{X(0):.1f},{yb} Z"
    ipk, itr, irec = _idx(sp, "2020-02-19"), _idx(sp, "2020-03-23"), _idx(sp, "2020-08-18")
    px, py = X(ipk), Y(sp[ipk][1])
    tx, ty = X(itr), Y(sp[itr][1])
    rx, ry = X(irec), Y(sp[irec][1])
    months = "".join(f'<text x="{X(i):.0f}" y="{yb + 26}" style="{HEAD}" font-size="18" text-anchor="middle" fill="{INK}">'
                     f'{["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"][int(d[5:7]) - 1]}</text>'
                     for i, (d, _) in enumerate(sp) if i == 0 or d[5:7] != sp[i - 1][0][5:7])
    viruses = "".join(ci.virus(px + dx, py + dy, k) for dx, dy, k in ((40, -60, 0.5), (110, -20, 0.38), (-20, 62, 0.34), (190, -60, 0.42)))
    body = (art.sunburst(tx, ty, rays=30)
            + f'<rect width="{W}" height="{H}" fill="url(#dots-big)"/>'
            + f'<rect x="0" y="0" width="{W}" height="54" fill="{INK}"/>'
            + f'<text x="30" y="37" style="{HEAD}" font-size="26" fill="{YELLOW}" letter-spacing="1.5">ECONOMIC CRISIS SIGNALS</text>'
            + art.title(W / 2, 170, "THE 2020", size=110, rot=-3)
            + art.title(W / 2, 286, "COVID CRASH!", size=112, fill=BLUE, rot=-3)
            + f'<g transform="rotate(4 690 344)"><rect x="560" y="318" width="250" height="50" fill="{INK}"/>'
              f'<text x="685" y="354" style="{HEAD}" font-size="32" text-anchor="middle" fill="{YELLOW}">FEB – MAR 2020</text></g>'
            + f'<g transform="rotate(-4 190 350)"><rect x="40" y="326" width="310" height="46" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
              f'<text x="195" y="360" style="{HEAD}" font-size="30" text-anchor="middle" fill="#fff">THE FASTEST CRASH EVER</text></g>'
            + f'<path d="{area}" fill="#fff" fill-opacity="0.55"/><path d="{area}" fill="url(#dots)"/>'
            + f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{INK}" stroke-width="5"/>'
            + f'<path d="{line}" fill="none" stroke="#fff" stroke-width="13" stroke-linejoin="round"/>'
            + f'<path d="{line}" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            + months + viruses
            # the peak
            + f'<circle cx="{px}" cy="{py}" r="7" fill="{YELLOW}" stroke="{INK}" stroke-width="3"/>'
            + f'<line x1="{px - 6}" y1="{py - 4}" x2="{px - 60}" y2="{py - 30}" stroke="{INK}" stroke-width="4"/>'
            + f'<g transform="rotate(-3 {px - 180} {py - 50})"><rect x="{px - 300}" y="{py - 86}" width="240" height="64" fill="#fff" stroke="{INK}" stroke-width="3"/>'
              f'<text x="{px - 180}" y="{py - 60}" style="{HEAD}" font-size="21" text-anchor="middle" fill="{INK}">RECORD · 19 FEB 2020</text>'
              f'<text x="{px - 180}" y="{py - 30}" style="{HEAD}" font-size="30" text-anchor="middle" fill="{GREEN}">3,386.15</text></g>'
            # the bottom
            + f'<circle cx="{tx}" cy="{ty}" r="7" fill="{YELLOW}" stroke="{INK}" stroke-width="3"/>'
            + f'<line x1="{x0 + 262}" y1="{yb - 72}" x2="{tx - 8}" y2="{ty + 2}" stroke="{INK}" stroke-width="4"/>'
            + f'<g transform="rotate(-2 {x0 + 135} {yb - 72})"><rect x="{x0 + 10}" y="{yb - 122}" width="252" height="94" fill="{INK}"/>'
              f'<text x="{x0 + 136}" y="{yb - 94}" style="{HEAD}" font-size="22" text-anchor="middle" fill="#fff">BOTTOM · 23 MAR 2020</text>'
              f'<text x="{x0 + 136}" y="{yb - 46}" style="{HEAD}" font-size="40" text-anchor="middle" fill="{YELLOW}">2,237 (−34%)</text></g>'
            + f'<text x="{px - 14:.0f}" y="{(py + ty) / 2 + 10:.0f}" style="{HEAD}" font-size="28" text-anchor="end" fill="{RED}" stroke="#fff" '
              f'stroke-width="5" paint-order="stroke">33 DAYS</text>'
            # back to a record
            + f'<circle cx="{rx}" cy="{ry}" r="7" fill="{GREEN}" stroke="{INK}" stroke-width="3"/>'
            + f'<g transform="rotate(-3 {rx} {ry - 60})"><rect x="{rx - 110}" y="{ry - 92}" width="200" height="58" fill="{GREEN}" stroke="{INK}" stroke-width="3"/>'
              f'<text x="{rx - 10}" y="{ry - 68}" style="{HEAD}" font-size="19" text-anchor="middle" fill="#fff">BACK TO A RECORD</text>'
              f'<text x="{rx - 10}" y="{ry - 44}" style="{HEAD}" font-size="19" text-anchor="middle" fill="{YELLOW}">18 AUG 2020</text></g>'
            + art.penny(150, 1132, s=0.68, mood="happy")
            + art.bear(700, 1132, s=0.68, mood="calm", flip=True)
            + art.bubble(232, 862, 300, "Record shares and the fewest jobless in 50 years! What could go wrong?", tail=(185, 950), size=18)
            + art.bubble(332, 1010, 270, "Something that wasn't on anyone's chart...", tail=(640, 985), size=19)
            + f'<rect x="0" y="{H - 44}" width="{W}" height="44" fill="{INK}"/>'
            + f'<text x="{W / 2}" y="{H - 16}" style="{BODY}" font-size="15" font-weight="700" text-anchor="middle" fill="#fff">'
              f'A true story, told with real data · Chart: S&amp;P 500, daily closes (Yahoo Finance)</text>')
    return page(body)


# ---- page 2: the sudden stop -----------------------------------------------------------------

def _money_circle(x, y, w, h):
    """Spending is someone's wages: the circle that lockdown cut."""
    cx, cy, r = x + w / 2, y + 238, 84
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fffdf3"/>',
           text_block(x + 14, y + 30, ["THE MONEY CIRCLE"], size=22, family=HEAD),
           text_block(x + 14, y + 52, wrap("Your spending is someone else's wages.", 34), size=13, weight="700")]
    # two arcs: wages (left, going down), spending (right, going up)
    out.append(f'<path d="M{cx - 30},{cy - r + 6} A{r},{r} 0 0 0 {cx - 30},{cy + r - 6}" fill="none" stroke="{GREEN}" stroke-width="9"/>'
               f'<path d="M{cx - 44},{cy + r - 20} L{cx - 26},{cy + r - 4} L{cx - 48},{cy + r + 6} Z" fill="{GREEN}" stroke="{INK}" stroke-width="2"/>'
               f'<path d="M{cx + 30},{cy + r - 6} A{r},{r} 0 0 0 {cx + 30},{cy - r + 6}" fill="none" stroke="{GREEN}" stroke-width="9"/>'
               f'<path d="M{cx + 44},{cy - r + 20} L{cx + 26},{cy - r + 4} L{cx + 48},{cy - r - 6} Z" fill="{GREEN}" stroke="{INK}" stroke-width="2"/>'
               f'<text x="{cx - r + 16}" y="{cy + 6}" style="{HEAD}" font-size="17" fill="{GREEN}">WAGES</text>'
               f'<text x="{cx + r - 16}" y="{cy + 6}" style="{HEAD}" font-size="17" text-anchor="end" fill="{GREEN}">SPENDING</text>')
    out.append(tech_icons.office(cx, cy - r - 24, 0.62)
               + f'<text x="{cx}" y="{cy - r - 64}" style="{HEAD}" font-size="15" text-anchor="middle" fill="{INK}">SHOPS &amp; FIRMS</text>'
               + "".join(ci._person(cx + dx, cy + r + 38, c, 1.0) for dx, c in ((-22, TEAL_), (0, ORANGE), (22, BLUE)))
               + f'<text x="{cx}" y="{cy + r + 68}" style="{HEAD}" font-size="15" text-anchor="middle" fill="{INK}">FAMILIES</text>')
    # the cut
    kx, ky = cx + r + 2, cy - 36
    out.append(f'<path d="M{kx - 22},{ky - 22} L{kx + 22},{ky + 22} M{kx + 22},{ky - 22} L{kx - 22},{ky + 22}" stroke="{RED}" stroke-width="10" stroke-linecap="round"/>'
               f'<rect x="{x + 14}" y="{cy + r + 82}" width="{w - 28}" height="30" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
               f'<text x="{cx}" y="{cy + r + 104}" style="{HEAD}" font-size="18" text-anchor="middle" fill="#fff">LOCKDOWN CUT THE CIRCLE</text>')
    out.append(text_block(x + 14, y + h - 40, wrap("No spending, no wages. No wages, no spending. It stopped everywhere at once.", 36),
                          size=13, weight="700"))
    return "".join(out)


TEAL_ = "#26a69a"


def machine() -> str:
    hd, top = head("THE SUDDEN STOP", "What changed: nothing inside the economy broke first. A virus forced the world to stop "
                                      "working and shopping, almost overnight.", fill=BLUE, size=74)
    out = [hd]
    lx, lw = 26, 470
    rows, sh = len(st.MACHINE), 104
    y0 = top + 20
    for i, (name, text, icon) in enumerate(st.MACHINE):
        y = y0 + i * sh
        out.append(f'<rect x="{lx + 4}" y="{y + 4}" width="{lw}" height="{sh - 18}" rx="12" fill="{INK}"/>'
                   f'<rect x="{lx}" y="{y}" width="{lw}" height="{sh - 18}" rx="12" fill="#fff" stroke="{INK}" stroke-width="3.5"/>'
                   + medallion(lx + 50, y + (sh - 18) / 2, 38, icon, 0.58)
                   + step_badge(lx + 18, y + 14, i + 1)
                   + text_block(lx + 100, y + 26, [name], size=21, family=HEAD)
                   + text_block(lx + 100, y + 46, wrap(text, 52), size=13, weight="700", lh=1.18))
        if i < rows - 1:
            ax = lx + 50
            out.append(f'<path d="M{ax - 9},{y + sh - 18} h18 v6 h8 l-17,12 l-17,-12 h8 Z" fill="{ORANGE}" stroke="{INK}" stroke-width="2"/>')
    tx, tw, th = lx + lw + 22, W - 26 - (lx + lw + 22), rows * sh - 18
    out.append(art.panel(tx, y0, tw, th, content=_money_circle(tx, y0, tw, th)))
    # weekly jobless claims, and the jobless rate
    y = y0 + rows * sh + 4
    pw, ph = 386, 150
    cl = _pts("claims", "2020-01-01", "2020-05-31")
    inner = [f'<rect x="26" y="{y}" width="{pw}" height="{ph}" fill="#fff"/>',
             text_block(40, y + 28, ["JOBLESS CLAIMS EXPLODED"], size=22, family=HEAD)]
    bx0, bw, base, top_h = 44, (pw - 40) / len(cl), y + ph - 30, 82
    for i, (d, v) in enumerate(cl):
        hh = top_h * v / 6.2e6
        inner.append(f'<rect x="{bx0 + i * bw:.1f}" y="{base - hh:.1f}" width="{bw - 3:.1f}" height="{max(hh, 1.5):.1f}" '
                     f'fill="{RED if v > 1e6 else "#9ca3af"}" stroke="{INK}" stroke-width="1.2"/>')
    imax = next(i for i, (_, v) in enumerate(cl) if v > 1e6)
    inner.append(f'<text x="{bx0 + imax * bw - 6:.0f}" y="{base - top_h + 14:.0f}" style="{HEAD}" font-size="17" text-anchor="end" fill="{RED}">6 MILLION</text>'
                 f'<text x="{bx0 + 4}" y="{base - 10}" style="{HEAD}" font-size="14" fill="{INK}">normal: 0.2M a week</text>'
                 f'<line x1="{bx0}" y1="{base}" x2="{26 + pw - 12}" y2="{base}" stroke="{INK}" stroke-width="2"/>')
    inner.append(text_block(40, y + ph - 10, ["new US claims each week, Jan–May 2020 (FRED)"], size=12, weight="700"))
    out.append(art.panel(26, y, pw, ph, content="".join(inner)))
    u0, u1, _, _ = st.MACHINE_STATS["unrate"]
    x = 26 + pw + 16
    inner = [f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="#fff"/>',
             text_block(x + 14, y + 28, ["UNEMPLOYMENT x4 IN 2 MONTHS"], size=22, family=HEAD)]
    for j, (lab, v, col) in enumerate([("FEB 2020", u0, "#9ca3af"), ("APR 2020", u1, RED)]):
        bw = 230 * v / u1
        by = y + 50 + j * 44
        inner.append(f'<text x="{x + 14}" y="{by + 24}" style="{HEAD}" font-size="17" fill="{INK}">{lab}</text>'
                     f'<rect x="{x + 96}" y="{by + 4}" width="{bw:.0f}" height="28" fill="{col}" stroke="{INK}" stroke-width="3"/>'
                     f'<text x="{x + 104 + bw:.0f}" y="{by + 26}" style="{HEAD}" font-size="20" fill="{INK}">{v}%</text>')
    inner.append(text_block(x + 14, y + ph - 12, ["14.8%: the highest since records began in 1948"], size=12, weight="700"))
    out.append(art.panel(x, y, pw, ph, content="".join(inner)))
    y += ph + 18
    box, bh = jargon(26, y, 640, st.JARGON_MACHINE, cols=2, size=12.5)
    out.append(box)
    out.append(art.bear(752, H - 18, s=0.4, mood="stern", flip=True)
               + art.bubble(678, y - 4, 140, "The economy is a circle. Cut it and it all stops.", tail=(745, H - 130), size=13))
    return page("".join(out) + num_footer(pno("machine")))


# ---- page 3: the good times ------------------------------------------------------------------

def _stock_panel(x, y, pw, ph):
    pts = _pts("sp_month", "2008-01", "2020-02")
    cx0, cx1, cy0, cy1 = x + 16, x + pw - 16, y + 56, y + ph - 34
    lo, hi = 0, 3600
    X = lambda i: cx0 + (cx1 - cx0) * i / (len(pts) - 1)
    Y = lambda v: cy1 - (cy1 - cy0) * (v - lo) / (hi - lo)
    i09, ipk = _idx(pts, "2009-02"), len(pts) - 1
    line = _path(pts, X, Y)
    area = line + f" L{X(ipk):.1f},{cy1} L{X(0):.1f},{cy1} Z"
    out = [f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="#fffdf3"/>',
           text_block(x + 14, y + 30, ["SHARES CLIMBED FOR 11 YEARS"], size=22, family=HEAD),
           f'<path d="{area}" fill="#d7f0dc"/>',
           f'<path d="{line}" fill="none" stroke="{INK}" stroke-width="3.5"/>',
           f'<line x1="{cx0}" y1="{cy1}" x2="{cx1}" y2="{cy1}" stroke="{INK}" stroke-width="2.5"/>',
           f'<circle cx="{X(i09):.0f}" cy="{Y(pts[i09][1]):.0f}" r="6" fill="#fff" stroke="{INK}" stroke-width="2.5"/>',
           f'<text x="{X(i09) + 8:.0f}" y="{Y(pts[i09][1]) + 20:.0f}" style="{BODY}" font-size="12" font-weight="700" fill="{INK}">2009 low: 676.53</text>',
           f'<circle cx="{X(ipk):.0f}" cy="{Y(pts[ipk][1]):.0f}" r="7" fill="{GREEN}" stroke="{INK}" stroke-width="2.5"/>',
           f'<text x="{X(ipk) - 10:.0f}" y="{Y(pts[ipk][1]) + 46:.0f}" style="{HEAD}" font-size="30" text-anchor="end" fill="{GREEN}" '
           f'stroke="{INK}" stroke-width="1.2" paint-order="stroke">+400%</text>']
    for i, (d, _) in enumerate(pts):
        if d.endswith("-01") and int(d[:4]) % 3 == 2:
            out.append(f'<text x="{X(i):.0f}" y="{cy1 + 16}" style="{BODY}" font-size="11.5" font-weight="700" text-anchor="middle" fill="{INK}">{d[:4]}</text>')
    out.append(f'<text x="{x + 14}" y="{y + ph - 4}" style="{BODY}" font-size="11.5" font-weight="700" fill="{INK}" fill-opacity="0.75">'
               f'S&amp;P 500 share index, month-end, 2008 – Feb 2020</text>')
    return "".join(out)


def good_times() -> str:
    hd, top = head("THE GOOD TIMES", "Before the crash, America was enjoying its longest boom ever. These true facts made "
                                     "people feel safe.", fill=GREEN)
    out = [hd]
    pw, ph, gap = 386, 248, 16
    for i, (big, title, text, icon, _) in enumerate(st.GOOD_TIMES):
        x = 26 + (i % 2) * (pw + gap)
        y = top + 18 + (i // 2) * (ph + gap)
        if i == 0:
            out.append(art.panel(x, y, pw, ph, fill="#fffdf3", content=_stock_panel(x, y, pw, ph)))
            continue
        inner = (f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="url(#dots)"/>'
                 + medallion(x + 74, y + 78, 56, icon, 0.95)
                 + f'<text x="{x + pw - 16}" y="{y + 66}" style="{HEAD}" font-size="{50 if len(big) < 7 else 40}" text-anchor="end" fill="{GREEN}" stroke="{INK}" stroke-width="2" paint-order="stroke">{big}</text>'
                 + text_block(x + 150, y + 100, wrap(title, 22), size=21, family=HEAD, lh=1.1)
                 + text_block(x + 18, y + 158, text, size=15.5, width=44, weight="700"))
        out.append(art.panel(x, y, pw, ph, fill="#fffdf3", content=inner))
    y = top + 18 + 3 * (ph + gap)
    out.append(art.penny(110, H - 24, s=0.5, mood="happy")
               + art.bubble(176, y + 6, 300, "Jobs, record shares, a trade deal... this boom will run forever!", tail=(140, y + 70), size=16)
               + art.bear(740, H - 24, s=0.5, mood="calm", flip=True)
               + art.bubble(400, y + 70, 300, "Long booms make people forget to keep a spare tyre.", tail=(700, y + 100), size=16))
    return page("".join(out) + num_footer(pno("good-times")))


# ---- page 4: hidden weak spots ---------------------------------------------------------------

def boom_to_danger() -> str:
    hd, top = head("HIDDEN WEAK SPOTS", "Underneath the good news, companies and families had little room for a shock. "
                                        "When one came, these made the fall harder.")
    out = [hd]
    pw, ph, gap = 386, 158, 12
    for i, (date, title, text, icon, _) in enumerate(st.DANGER_STEPS[:4]):
        x = 26 + (i % 2) * (pw + gap)
        y = top + 20 + (i // 2) * (ph + gap)
        badge, _ = icons.date_badge(x + 14, y + 12, date, size=20)
        tl = wrap(title, 20)
        inner = (f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="#fff"/>'
                 + badge + medallion(x + pw - 54, y + 54, 40, icon, 0.6)
                 + text_block(x + 16, y + 72, tl, size=23, family=HEAD, lh=1.05)
                 + text_block(x + 16, y + 96 + (len(tl) - 1) * 23, wrap(text, 48), size=13.5, weight="700"))
        out.append(art.panel(x, y, pw, ph, content=inner) + step_badge(x + pw - 18, y + ph - 18, i + 1))
    fw, fh = 788, 158
    # 5. the $400 test: ten people, four can't pay
    _, title, text, _, _ = st.DANGER_STEPS[4]
    x, y = 26, top + 20 + 2 * (ph + gap)
    people = "".join(ci._person(x + 34 + (k % 5) * 40, y + 82 + (k // 5) * 44, RED if k < 4 else "#9ccc65", 0.92) for k in range(10))
    inner = (f'<rect x="{x}" y="{y}" width="{fw}" height="{fh}" fill="#fff"/>' + people
             + f'<text x="{x + 112}" y="{y + 36}" style="{HEAD}" font-size="20" text-anchor="middle" fill="{RED}">ABOUT 4 IN 10</text>'
             + f'<text x="{x + 112}" y="{y + fh - 10}" style="{BODY}" font-size="12" font-weight="700" text-anchor="middle" fill="{INK}">red = can\'t cover $400</text>'
             + text_block(x + 240, y + 38, [title.upper()], size=25, family=HEAD)
             + text_block(x + 240, y + 66, wrap(text, 64), size=14.5, weight="700"))
    out.append(art.panel(x, y, fw, fh, content=inner) + step_badge(x + fw - 18, y + fh - 18, 5))
    # 6. CAPE: how pricey shares were, compared with history
    _, title, text, _, _ = st.DANGER_STEPS[5]
    y += fh + gap
    bars = [("AVERAGE", 17.8, "#9ccc65"), ("1929", 32.6, ORANGE), ("2000", 44.2, RED), ("JAN 2020", 31.0, RED)]
    base, sc = y + fh - 26, 2.4
    inner = [f'<rect x="{x}" y="{y}" width="{fw}" height="{fh}" fill="#fff"/>']
    for j, (lab, v, col) in enumerate(bars):
        bx = x + 22 + j * 52
        inner.append(f'<rect x="{bx}" y="{base - v * sc:.0f}" width="38" height="{v * sc:.0f}" fill="{col}" stroke="{INK}" stroke-width="2.5"'
                     + (' stroke-dasharray="0"' if lab != "JAN 2020" else '') + '/>'
                     f'<text x="{bx + 19}" y="{base - v * sc - 5:.0f}" style="{HEAD}" font-size="15" text-anchor="middle" fill="{INK}">{v:.0f}</text>'
                     f'<text x="{bx + 19}" y="{base + 15}" style="{HEAD}" font-size="{11 if len(lab) > 5 else 13}" text-anchor="middle" fill="{INK}">{lab}</text>')
    inner.append(f'<line x1="{x + 16}" y1="{base}" x2="{x + 228}" y2="{base}" stroke="{INK}" stroke-width="2.5"/>'
                 + text_block(x + 240, y + 38, [title.upper()], size=25, family=HEAD)
                 + text_block(x + 240, y + 66, wrap(text, 64), size=14.5, weight="700"))
    out.append(art.panel(x, y, fw, fh, content="".join(inner)) + step_badge(x + fw - 18, y + fh - 18, 6))
    y += fh + 16
    box, bh = jargon(26, y, 788, st.JARGON_DANGER, cols=2, size=12.5)
    out.append(box)
    y += bh + 12
    out.append(art.penny(60, H - 10, s=0.26, mood="think")
               + art.bubble(100, y, 300, "So a sudden stop would hurt more than usual?", tail=(80, y + 34), size=14)
               + art.bear(776, H - 10, s=0.26, mood="stern", flip=True)
               + art.bubble(420, y, 320, "Yes: little cash, lots of debt, pricey shares.", tail=(752, y + 34), size=14))
    return page("".join(out) + num_footer(pno("boom-to-danger")))


# ---- page 5: warning signs -------------------------------------------------------------------

def _x_axis(pts, X, y, size=12):
    return "".join(f'<text x="{X(i):.0f}" y="{y}" style="{BODY}" font-size="{size}" font-weight="700" text-anchor="middle" fill="{INK}">{d[:4]}</text>'
                   for i, (d, _) in enumerate(pts) if d.endswith("-01") and d[5:7] == "01")


def warning_signs() -> str:
    hd, top = head("THE ECONOMY WAS ALREADY TIRED", "Nobody's chart showed a virus. But in 2019 two of our warning lights "
                                                    "said the long boom was slowing down.", size=54)
    out = [hd]
    x, w = 26, 788
    # chart 1: the yield curve
    y, h = top + 20, 300
    cv = _pts("curve", "2018-01", "2020-12")
    cx0, cx1, cy0, cy1 = x + 20, x + w - 20, y + 96, y + h - 36
    X = lambda i: cx0 + (cx1 - cx0) * i / (len(cv) - 1)
    Y = lambda v: (cy0 + cy1) / 2 - (cy1 - cy0) / 2 * v / 1.15
    zero = Y(0)
    bars = "".join(f'<rect x="{X(i) - 7:.1f}" y="{min(zero, Y(v)):.1f}" width="14" height="{abs(Y(v) - zero):.1f}" '
                   f'fill="{RED if v < 0 else "#9ccc65"}" stroke="{INK}" stroke-width="1"/>' for i, (_, v) in enumerate(cv))
    i_s = _idx(cv, st.WARNING["stock_peak"])
    first_neg = next(i for i, (_, v) in enumerate(cv) if v < 0)
    mid = (X(first_neg) + X(i_s)) / 2
    inner = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff"/>',
             text_block(x + 16, y + 32, ["1. THE YIELD CURVE TURNED UPSIDE DOWN"], size=26, family=HEAD),
             text_block(x + 16, y + 54, wrap("Lending for 10 years normally pays more than lending for 3 months. In 2019 it paid LESS "
                                             "(red bars): investors expected the economy to weaken and rates to fall.", 110), size=13.5, weight="700"),
             bars,
             f'<line x1="{cx0}" y1="{zero:.0f}" x2="{cx1}" y2="{zero:.0f}" stroke="{INK}" stroke-width="2.5"/>',
             _x_axis(cv, X, cy1 + 18),
             f'<line x1="{X(i_s):.0f}" y1="{cy0}" x2="{X(i_s):.0f}" y2="{cy1}" stroke="{RED}" stroke-width="3" stroke-dasharray="6 4"/>',
             f'<text x="{X(i_s) - 8:.0f}" y="{cy0 + 14}" style="{HEAD}" font-size="17" text-anchor="end" fill="{RED}">SHARES PEAK</text>',
             f'<text x="{X(i_s) - 8:.0f}" y="{cy0 + 32}" style="{HEAD}" font-size="17" text-anchor="end" fill="{RED}">FEB 2020</text>',
             f'<path d="M{X(first_neg) - 7:.0f},{zero + 62:.0f} H{X(i_s) - 4:.0f}" stroke="{INK}" stroke-width="3"/>'
             f'<path d="M{X(i_s) - 14:.0f},{zero + 54:.0f} L{X(i_s) - 4:.0f},{zero + 62:.0f} L{X(i_s) - 14:.0f},{zero + 70:.0f} Z" fill="{INK}"/>',
             f'<rect x="{mid - 110:.0f}" y="{zero + 70:.0f}" width="220" height="26" fill="{YELLOW}" stroke="{INK}" stroke-width="2"/>',
             f'<text x="{mid:.0f}" y="{zero + 90:.0f}" style="{HEAD}" font-size="18" text-anchor="middle" fill="{INK}">UPSIDE DOWN FROM MAY 2019</text>',
             f'<text x="{cx0 + 4}" y="{cy1 - 4}" style="{BODY}" font-size="12" font-weight="700" fill="{INK}">10-year minus 3-month US rates, monthly average</text>']
    out.append(art.panel(x, y, w, h, content="".join(inner)))
    # chart 2: factory hours
    y += h + 16
    h2 = 300
    hr = _pts("hours", "2018-01", "2020-12")
    cx0, cx1, cy0, cy1 = x + 20, x + w - 20, y + 84, y + h2 - 36
    X2 = lambda i: cx0 + (cx1 - cx0) * i / (len(hr) - 1)
    Y2 = lambda v: cy1 - (cy1 - cy0) * (v - 38) / (43 - 38)
    i_pk = _idx(hr, st.WARNING["hours_peak"][0])
    i_lo = _idx(hr, st.WARNING["hours_low"][0])
    i_s2 = _idx(hr, st.WARNING["stock_peak"])
    i_apr = _idx(hr, "2020-04")
    inner = [f'<rect x="{x}" y="{y}" width="{w}" height="{h2}" fill="#fff"/>',
             text_block(x + 16, y + 32, ["2. FACTORIES WERE CUTTING HOURS"], size=26, family=HEAD),
             text_block(x + 16, y + 54, wrap("When orders dry up, factories cut workers' hours before they cut jobs. Average weekly hours "
                                             "slid through 2019, during the US-China trade war.", 110), size=13.5, weight="700"),
             f'<rect x="{X2(i_pk):.0f}" y="{cy0}" width="{X2(i_lo) - X2(i_pk):.0f}" height="{cy1 - cy0}" fill="{YELLOW}" opacity="0.35"/>',
             f'<path d="{_path(hr, X2, Y2)}" fill="none" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>',
             f'<line x1="{cx0}" y1="{cy1}" x2="{cx1}" y2="{cy1}" stroke="{INK}" stroke-width="2.5"/>',
             _x_axis(hr, X2, cy1 + 18),
             f'<circle cx="{X2(i_pk):.0f}" cy="{Y2(hr[i_pk][1]):.0f}" r="6" fill="{GREEN}" stroke="{INK}" stroke-width="2.5"/>',
             f'<text x="{X2(i_pk) + 4:.0f}" y="{Y2(hr[i_pk][1]) - 12:.0f}" style="{HEAD}" font-size="16" fill="{INK}">42.4 HOURS (APR 2018)</text>',
             f'<circle cx="{X2(i_lo):.0f}" cy="{Y2(hr[i_lo][1]):.0f}" r="6" fill="{ORANGE}" stroke="{INK}" stroke-width="2.5"/>',
             f'<text x="{X2(i_lo) - 8:.0f}" y="{Y2(hr[i_lo][1]) + 26:.0f}" style="{HEAD}" font-size="16" text-anchor="end" fill="{ORANGE}">41.3 (JAN 2020)</text>',
             f'<text x="{(X2(i_pk) + X2(i_lo)) / 2:.0f}" y="{cy1 - 14}" style="{HEAD}" font-size="18" text-anchor="middle" fill="#b7791f">SLOWING FOR 21 MONTHS</text>',
             f'<line x1="{X2(i_s2):.0f}" y1="{cy0}" x2="{X2(i_s2):.0f}" y2="{cy1}" stroke="{RED}" stroke-width="3" stroke-dasharray="6 4"/>',
             f'<text x="{X2(i_apr) + 10:.0f}" y="{Y2(hr[i_apr][1]) + 6:.0f}" style="{HEAD}" font-size="16" fill="{RED}">LOCKDOWN: 38.4</text>']
    out.append(art.panel(x, y, w, h2, content="".join(inner)))
    y += h2 + 16
    box, bh = jargon(26, y, 560, [("Yield curve", "Interest rates for short and long loans, side by side. Upside down = a warning.", "rate_up"),
                                  ("Factory hours", "How long factory staff work each week. Fewer hours = fewer orders.", "factory_hours")],
                     cols=1, size=12.5)
    out.append(box + art.penny(760, H - 18, s=0.42, mood="shock", flip=True)
               + art.bubble(600, y, 210, "So the lights were on BEFORE the virus?", tail=(735, H - 140), size=14)
               + art.bear(70, H - 14, s=0.3, mood="calm")
               + art.bubble(120, y + bh + 14, 460, "Yes, for a slowdown. The virus turned a slowdown into a sudden stop.",
                            tail=(100, y + bh + 50), size=14))
    return page("".join(out) + num_footer(pno("warning-signs")))


# ---- assemble --------------------------------------------------------------------------------

_FN = {"cover": cover, "machine": machine, "good-times": good_times, "boom-to-danger": boom_to_danger,
       "warning-signs": warning_signs, "timeline-up": lambda: kit.timeline_up(st),
       "timeline-down": lambda: kit.timeline_down(st), "what-popped": lambda: kit.what_popped(st),
       "map": lambda: kit.map_page(st), "fixing-rules": lambda: kit.fixing_rules(st),
       "lesson": lambda: kit.lights(st), "sources": lambda: kit.sources(st)}
PAGES = [(f"{i:02d}-{name}", _FN[name]) for i, name in enumerate(st.ORDER, 1)]

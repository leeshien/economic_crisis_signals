"""The 2008 Global Financial Crisis — comic pages. Facts and sources live in gfc_story.py."""
from comics import art, icons, kit, crisis_icons as ci
from comics import gfc_story as st
from comics.art import INK, RED, YELLOW, BLUE, ORANGE, HEAD, BODY, W, H, text_block, wrap
from comics.kit import GREEN, page, head, num_footer, medallion, step_badge, jargon

SLUG, ISSUE = st.SLUG, st.ISSUE
pno = lambda name: kit.page_no(st, name)


def _pts(name, start=None, end=None):
    return [(d, v) for d, v in st.SERIES[name]["points"] if (not start or d >= start) and (not end or d <= end)]


def _path(pts, X, Y):
    return " ".join(f"{'M' if i == 0 else 'L'}{X(i):.1f},{Y(v):.1f}" for i, (_, v) in enumerate(pts))


# ---- page 1: cover ---------------------------------------------------------------------------

def cover() -> str:
    sp = _pts("sp500", "2002-01", "2012-12")
    x0, x1, yb, yt, vmax = 70, 770, 800, 530, 1700
    X = lambda i: x0 + (x1 - x0) * i / (len(sp) - 1)
    Y = lambda v: yb - (yb - yt) * v / vmax
    line = _path(sp, X, Y)
    area = line + f" L{X(len(sp) - 1):.1f},{yb} L{X(0):.1f},{yb} Z"
    ipk = max(range(len(sp)), key=lambda i: sp[i][1] if sp[i][0] < "2009" else 0)
    itr = min(range(ipk, len(sp)), key=lambda i: sp[i][1])
    px, py = X(ipk), Y(sp[ipk][1])
    tx, ty = X(itr), Y(sp[itr][1])
    years = "".join(f'<text x="{X(i):.0f}" y="{yb + 26}" style="{HEAD}" font-size="20" text-anchor="middle" fill="{INK}">{d[:4]}</text>'
                    for i, (d, _) in enumerate(sp) if d.endswith("-01") and int(d[:4]) % 2 == 0)
    flying = "".join(f'<g transform="translate({px + dx},{py + dy}) rotate({a})"><rect x="-15" y="-22" width="30" height="44" rx="3" fill="#fff" '
                     f'stroke="{INK}" stroke-width="3"/><text y="5" style="{HEAD}" font-size="10" text-anchor="middle" fill="{RED}">{lab}</text></g>'
                     for dx, dy, a, lab in [(-96, -128, -35, "AAA"), (96, -134, 28, "CDO"), (132, -64, 62, "LOAN"), (-130, -56, -60, "BANK")])
    body = (art.sunburst(px, py, rays=30)
            + f'<rect width="{W}" height="{H}" fill="url(#dots-big)"/>'
            + f'<rect x="0" y="0" width="{W}" height="54" fill="{INK}"/>'
            + f'<text x="30" y="37" style="{HEAD}" font-size="26" fill="{YELLOW}" letter-spacing="1.5">ECONOMIC CRISIS SIGNALS</text>'
            + f'<text x="{W - 30}" y="37" style="{HEAD}" font-size="26" fill="#fff" text-anchor="end">{ISSUE}</text>'
            + art.title(W / 2, 170, "THE 2008", size=110, rot=-3)
            + art.title(W / 2, 286, "FINANCIAL CRISIS!", size=104, fill=BLUE, rot=-3)
            + f'<g transform="rotate(4 690 344)"><rect x="560" y="318" width="250" height="50" fill="{INK}"/>'
              f'<text x="685" y="354" style="{HEAD}" font-size="32" text-anchor="middle" fill="{YELLOW}">2003 – 2009</text></g>'
            + f'<g transform="rotate(-4 170 350)"><rect x="40" y="326" width="270" height="46" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
              f'<text x="175" y="360" style="{HEAD}" font-size="30" text-anchor="middle" fill="#fff">A HOUSE OF CARDS</text></g>'
            + f'<path d="{area}" fill="#fff" fill-opacity="0.55"/><path d="{area}" fill="url(#dots)"/>'
            + f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{INK}" stroke-width="5"/>'
            + f'<path d="{line}" fill="none" stroke="#fff" stroke-width="15" stroke-linejoin="round"/>'
            + f'<path d="{line}" fill="none" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            + years + flying
            + ci.house_of_cards(px, py - 62, 0.9)
            + f'<line x1="{px - 130}" y1="{py + 50}" x2="{px - 6}" y2="{py + 4}" stroke="{INK}" stroke-width="4"/><circle cx="{px}" cy="{py}" r="7" fill="{YELLOW}" stroke="{INK}" stroke-width="3"/>'
            + f'<g transform="rotate(-3 {px - 250} {py + 60})"><rect x="{px - 380}" y="{py + 30}" width="250" height="64" fill="#fff" stroke="{INK}" stroke-width="3"/>'
              f'<text x="{px - 255}" y="{py + 56}" style="{HEAD}" font-size="21" text-anchor="middle" fill="{INK}">S&amp;P 500 PEAK · 9 OCT 2007</text>'
              f'<text x="{px - 255}" y="{py + 86}" style="{HEAD}" font-size="30" text-anchor="middle" fill="{RED}">1,565.15</text></g>'
            + f'<line x1="{tx}" y1="{ty + 8}" x2="{tx}" y2="{ty + 26}" stroke="{INK}" stroke-width="4"/>'
              f'<circle cx="{tx}" cy="{ty}" r="7" fill="{YELLOW}" stroke="{INK}" stroke-width="3"/>'
            + f'<g transform="rotate(2 {tx + 40} {ty + 70})"><rect x="{tx - 60}" y="{ty + 26}" width="250" height="94" fill="{INK}"/>'
              f'<text x="{tx + 65}" y="{ty + 54}" style="{HEAD}" font-size="22" text-anchor="middle" fill="#fff">BOTTOM · 9 MAR 2009</text>'
              f'<text x="{tx + 65}" y="{ty + 102}" style="{HEAD}" font-size="40" text-anchor="middle" fill="{YELLOW}">676.53 (−57%)</text></g>'
            + art.penny(150, 1132, s=0.68, mood="happy")
            + art.bear(700, 1132, s=0.68, mood="calm", flip=True)
            + art.bubble(232, 862, 300, "House prices never fall. Everybody knows that!", tail=(185, 950), size=19)
            + art.bubble(332, 1000, 270, "Unless everybody borrowed too much to buy them...", tail=(640, 975), size=19)
            + f'<rect x="0" y="{H - 44}" width="{W}" height="44" fill="{INK}"/>'
            + f'<text x="{W / 2}" y="{H - 16}" style="{BODY}" font-size="15" font-weight="700" text-anchor="middle" fill="#fff">'
              f'A true story, told with real data · Chart: S&amp;P 500, month-end closes (Yahoo Finance)</text>')
    return page(body)


# ---- page 2: the mortgage machine ------------------------------------------------------------

def _tranche_tower(x, y, w, h):
    """A mortgage bond sliced into layers; losses hit the bottom first."""
    layers = [("AAA", 0.62, "#3fa34d", "PAID FIRST"), ("AA / A", 0.16, "#9ccc65", ""), ("BBB", 0.12, ORANGE, ""),
              ("FIRST LOSS", 0.10, RED, "LOSES FIRST")]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fffdf3"/>',
           text_block(x + 14, y + 30, ["ONE BOND, SLICED"], size=22, family=HEAD)]
    tx, tw, ty, th = x + 24, 120, y + 52, h - 120
    yy = ty
    for name, frac, col, note in layers:
        lh = th * frac
        out.append(f'<rect x="{tx}" y="{yy:.0f}" width="{tw}" height="{lh:.0f}" fill="{col}" stroke="{INK}" stroke-width="3"/>'
                   f'<text x="{tx + tw / 2}" y="{yy + lh / 2 + 7:.0f}" style="{HEAD}" font-size="{20 if lh > 30 else 15}" text-anchor="middle" fill="#fff" '
                   f'stroke="{INK}" stroke-width="0.8" paint-order="stroke">{name}</text>')
        if note:
            out.append(f'<text x="{tx + tw + 30}" y="{yy + lh / 2 + 6:.0f}" style="{HEAD}" font-size="16" fill="{INK}">{note}</text>')
        yy += lh
    # cash pouring in on top, losses rising from below
    out.append(f'<path d="M{tx + tw + 14},{ty + th - 6} V{ty + th * 0.55} " stroke="{RED}" stroke-width="5"/>'
               + f'<path d="M{tx + tw + 6},{ty + th * 0.55 + 8} L{tx + tw + 14},{ty + th * 0.55 - 6} L{tx + tw + 22},{ty + th * 0.55 + 8} Z" fill="{RED}"/>'
               + f'<text x="{tx + tw + 26}" y="{ty + th * 0.72:.0f}" style="{HEAD}" font-size="14" fill="{RED}">LOSSES</text>'
               + f'<text x="{tx + tw + 26}" y="{ty + th * 0.72 + 16:.0f}" style="{HEAD}" font-size="14" fill="{RED}">RISE UP</text>')
    out.append(text_block(x + 14, y + h - 52, wrap("Payments flow in at the top. When families stop paying, the "
                                                   "bottom layers lose first, so the top looked safe.", 34), size=13, weight="700"))
    return "".join(out)


def machine() -> str:
    hd, top = head("THE MORTGAGE MACHINE", "What changed: home loans became something banks could sell. A new money "
                                           "machine turned family mortgages into bonds for investors all over the world.",
                   fill=BLUE, size=70)
    out = [hd]
    lx, lw = 26, 470
    rows = len(st.MACHINE)
    sh = 104
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
    # the sliced bond, beside the stations
    tx, tw, th = lx + lw + 22, W - 26 - (lx + lw + 22), rows * sh - 18
    out.append(art.panel(tx, y0, tw, th, content=_tranche_tower(tx, y0, tw, th)))
    # two numbers that show how big it got
    y = y0 + rows * sh + 4
    pw, ph = 386, 150
    sub0, sub1, sub_txt, _ = st.MACHINE_STATS["subprime"]
    inner = [f'<rect x="26" y="{y}" width="{pw}" height="{ph}" fill="#fff"/>',
             text_block(40, y + 28, ["RISKY LOANS GREW"], size=22, family=HEAD)]
    for j, (lab, k) in enumerate([("2001", 1), ("2006", 4)]):
        ry = y + 52 + j * 42
        inner.append(f'<text x="40" y="{ry + 22}" style="{HEAD}" font-size="18" fill="{INK}">{lab}</text>')
        for n in range(20):
            inner.append(ci._g(92 + n * 15.5, ry + 18, 0.28, ci._house(0, 26, fill=(RED if n < k else "#fff"), roof=(RED if n < k else "#b0bec5"))))
    inner.append(text_block(40, y + ph - 12, ["red = subprime: 1 in 20 loans, then 1 in 5"], size=12, weight="700"))
    out.append(art.panel(26, y, pw, ph, content="".join(inner)))
    d0, d1, d_txt, _ = st.MACHINE_STATS["debt"]
    x = 26 + pw + 16
    inner = [f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="#fff"/>',
             text_block(x + 14, y + 28, ["MORTGAGE DEBT DOUBLED"], size=22, family=HEAD)]
    for j, (lab, v, col) in enumerate([("2000", d0, "#9ca3af"), ("2008", d1, RED)]):
        bw = 250 * v / d1
        by = y + 50 + j * 44
        inner.append(f'<text x="{x + 14}" y="{by + 24}" style="{HEAD}" font-size="18" fill="{INK}">{lab}</text>'
                     f'<rect x="{x + 62}" y="{by + 4}" width="{bw:.0f}" height="28" fill="{col}" stroke="{INK}" stroke-width="3"/>'
                     f'<text x="{x + 70 + bw:.0f}" y="{by + 26}" style="{HEAD}" font-size="20" fill="{INK}">${v}tn</text>')
    inner.append(text_block(x + 14, y + ph - 12, ["US home loans owed by households, trillions"], size=12, weight="700"))
    out.append(art.panel(x, y, pw, ph, content="".join(inner)))
    # glossary + narrator
    y += ph + 18
    box, bh = jargon(26, y, 640, st.JARGON_MACHINE, cols=2, size=12.5)
    out.append(box)
    out.append(art.bear(752, H - 18, s=0.4, mood="stern", flip=True)
               + art.bubble(678, y - 4, 140, "A loan you sell is a loan you don't check.", tail=(745, H - 130), size=13))
    return page("".join(out) + num_footer(pno("machine")))


# ---- page 3: the good times ------------------------------------------------------------------

def _home_price_panel(x, y, pw, ph):
    pts = _pts("homeprices", "1996-01", "2012-12")
    cx0, cx1, cy0, cy1 = x + 16, x + pw - 16, y + 56, y + ph - 34
    lo, hi = 60, 200
    X = lambda i: cx0 + (cx1 - cx0) * i / (len(pts) - 1)
    Y = lambda v: cy1 - (cy1 - cy0) * (v - lo) / (hi - lo)
    ipk = max(range(len(pts)), key=lambda i: pts[i][1])
    i00 = next(i for i, (d, _) in enumerate(pts) if d == "2000-01")
    line = _path(pts, X, Y)
    area = line + f" L{X(len(pts) - 1):.1f},{cy1} L{X(0):.1f},{cy1} Z"
    out = [f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="#fffdf3"/>',
           text_block(x + 14, y + 30, ["HOME PRICES SOARED"], size=24, family=HEAD),
           f'<path d="{area}" fill="#d7f0dc"/>',
           f'<path d="{line}" fill="none" stroke="{INK}" stroke-width="3.5"/>',
           f'<line x1="{cx0}" y1="{cy1}" x2="{cx1}" y2="{cy1}" stroke="{INK}" stroke-width="2.5"/>',
           f'<circle cx="{X(i00):.0f}" cy="{Y(pts[i00][1]):.0f}" r="6" fill="#fff" stroke="{INK}" stroke-width="2.5"/>',
           f'<circle cx="{X(ipk):.0f}" cy="{Y(pts[ipk][1]):.0f}" r="7" fill="{GREEN}" stroke="{INK}" stroke-width="2.5"/>',
           f'<text x="{X(ipk) - 10:.0f}" y="{Y(pts[ipk][1]) - 12:.0f}" style="{HEAD}" font-size="30" text-anchor="end" fill="{GREEN}" '
           f'stroke="{INK}" stroke-width="1.2" paint-order="stroke">+85%</text>',
           f'<text x="{X(ipk) + 12:.0f}" y="{Y(pts[ipk][1]) + 30:.0f}" style="{BODY}" font-size="12" font-weight="700" fill="{INK}">peak Jul 2006</text>',
           f'<text x="{X(i00):.0f}" y="{Y(pts[i00][1]) + 22:.0f}" style="{BODY}" font-size="12" font-weight="700" text-anchor="middle" fill="{INK}">Jan 2000</text>']
    for d_i, (d, _) in enumerate(pts):
        if d.endswith("-01") and int(d[:4]) % 4 == 0:
            out.append(f'<text x="{X(d_i):.0f}" y="{cy1 + 16}" style="{BODY}" font-size="11.5" font-weight="700" text-anchor="middle" fill="{INK}">{d[:4]}</text>')
    out.append(f'<text x="{x + 14}" y="{y + ph - 4}" style="{BODY}" font-size="11.5" font-weight="700" fill="{INK}" fill-opacity="0.75">'
               f'US home prices (Case-Shiller national index), 1996–2012</text>')
    return "".join(out)


def good_times() -> str:
    hd, top = head("THE GOOD TIMES", "Before the crash, life felt good. These true facts made people believe that "
                                     "houses, jobs and shares could only go up.", fill=GREEN)
    out = [hd]
    pw, ph, gap = 386, 248, 16
    for i, (big, title, text, icon, _) in enumerate(st.GOOD_TIMES):
        x = 26 + (i % 2) * (pw + gap)
        y = top + 18 + (i // 2) * (ph + gap)
        if i == 0:
            out.append(art.panel(x, y, pw, ph, fill="#fffdf3", content=_home_price_panel(x, y, pw, ph)))
            continue
        inner = (f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="url(#dots)"/>'
                 + medallion(x + 74, y + 78, 56, icon, 0.95)
                 + f'<text x="{x + pw - 16}" y="{y + 66}" style="{HEAD}" font-size="{50 if len(big) < 7 else 40}" text-anchor="end" fill="{GREEN}" stroke="{INK}" stroke-width="2" paint-order="stroke">{big}</text>'
                 + text_block(x + 150, y + 100, wrap(title, 22), size=21, family=HEAD, lh=1.1)
                 + text_block(x + 18, y + 158, text, size=15.5, width=44, weight="700"))
        out.append(art.panel(x, y, pw, ph, fill="#fffdf3", content=inner))
    y = top + 18 + 3 * (ph + gap)
    out.append(art.penny(110, H - 24, s=0.5, mood="happy")
               + art.bubble(176, y + 6, 300, "Buy a house now, before prices go even higher!", tail=(140, y + 70), size=17)
               + art.bear(740, H - 24, s=0.5, mood="calm", flip=True)
               + art.bubble(400, y + 70, 300, "Prices were rising because loans were easy, and loans were easy because prices were rising.",
                            tail=(700, y + 100), size=15))
    return page("".join(out) + num_footer(pno("good-times")))


# ---- page 4: from boom to danger -------------------------------------------------------------

def boom_to_danger() -> str:
    hd, top = head("FROM BOOM TO DANGER", "Cheap money and easy loans pushed prices up. Underneath, the whole system was "
                                          "built on borrowed money.")
    out = [hd]
    pw, ph, gap = 386, 168, 12
    for i, (date, title, text, icon, _) in enumerate(st.DANGER_STEPS[:4]):
        x = 26 + (i % 2) * (pw + gap)
        y = top + 22 + (i // 2) * (ph + gap)
        badge, _ = icons.date_badge(x + 14, y + 12, date, size=20)
        tl = wrap(title, 20)
        inner = (f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" fill="#fff"/>'
                 + badge + medallion(x + pw - 56, y + 56, 42, icon, 0.62)
                 + text_block(x + 16, y + 74, tl, size=24, family=HEAD, lh=1.05)
                 + text_block(x + 16, y + 100 + (len(tl) - 1) * 24, wrap(text, 48), size=13.5, weight="700"))
        out.append(art.panel(x, y, pw, ph, content=inner) + step_badge(x + pw - 18, y + ph - 18, i + 1))
    fw = 788
    # 5. leverage: one green block of own money under thirty borrowed ones
    date, title, text, _, _ = st.DANGER_STEPS[4]
    x, y, fh = 26, top + 22 + 2 * (ph + gap), 200
    badge, _ = icons.date_badge(x + 14, y + 12, "LEHMAN, END OF 2007", size=18)
    blocks = []
    for k in range(30):
        c, r = divmod(k, 10)
        bx, by = x + 64 + r * 19, y + 70 + c * 22
        blocks.append(f'<rect x="{bx}" y="{by}" width="16" height="18" fill="{YELLOW}" stroke="{INK}" stroke-width="1.8"/>')
    blocks.append(f'<rect x="{x + 22}" y="{y + 70}" width="30" height="62" fill="{GREEN}" stroke="{INK}" stroke-width="2.5"/>'
                  f'<text x="{x + 37}" y="{y + 108}" style="{HEAD}" font-size="16" text-anchor="middle" fill="#fff">$1</text>'
                  f'<text x="{x + 37}" y="{y + 152}" style="{HEAD}" font-size="14" text-anchor="middle" fill="{GREEN}">OWN</text>'
                  f'<text x="{x + 158}" y="{y + 152}" style="{HEAD}" font-size="14" text-anchor="middle" fill="#b7791f">$30 BORROWED</text>'
                  f'<text x="{x + 22}" y="{y + 182}" style="{BODY}" font-size="12.5" font-weight="700" fill="{INK}">Lose $1 in every $31 and its own money is gone.</text>')
    inner = (f'<rect x="{x}" y="{y}" width="{fw}" height="{fh}" fill="#fff"/>' + badge + "".join(blocks)
             + text_block(x + 270, y + 40, [title.upper()], size=26, family=HEAD)
             + text_block(x + 270, y + 70, wrap(text, 62), size=14.5, weight="700"))
    out.append(art.panel(x, y, fw, fh, content=inner) + step_badge(x + fw - 18, y + fh - 18, 5))
    # 6. AIG: a big umbrella with holes over a pile of bonds
    date, title, text, _, _ = st.DANGER_STEPS[5]
    y += fh + gap
    ah = 186
    inner = (f'<rect x="{x}" y="{y}" width="{fw}" height="{ah}" fill="#fff"/>'
             + icons.date_badge(x + 14, y + 12, "AIG, 2007", size=18)[0]
             + ci.umbrella_holes(x + 140, y + 112, 1.2)
             + text_block(x + 270, y + 40, [title.upper()], size=26, family=HEAD)
             + text_block(x + 270, y + 70, wrap(text, 62), size=14.5, weight="700")
             + art.burst(x + fw - 70, y + ah - 50, 44, "", points=14, fill=YELLOW)
             + f'<text x="{x + fw - 70}" y="{y + ah - 52}" style="{HEAD}" font-size="17" text-anchor="middle" fill="{RED}">$85BN</text>'
             + f'<text x="{x + fw - 70}" y="{y + ah - 35}" style="{HEAD}" font-size="13" text-anchor="middle" fill="{INK}">RESCUE</text>')
    out.append(art.panel(x, y, fw, ah, content=inner) + step_badge(x + fw - 18, y + 22, 6))
    y += ah + 16
    box, bh = jargon(26, y, 788, st.JARGON_DANGER, cols=2, size=13)
    out.append(box)
    y += bh + 14
    out.append(art.penny(60, H - 12, s=0.28, mood="think")
               + art.bubble(100, y, 300, "So if house prices fell just a little...?", tail=(80, y + 40), size=14)
               + art.bear(776, H - 12, s=0.28, mood="stern", flip=True)
               + art.bubble(420, y, 320, "...the whole borrowed tower could topple.", tail=(752, y + 40), size=14))
    return page("".join(out) + num_footer(pno("boom-to-danger")))


# ---- page 5: warning signs -------------------------------------------------------------------

def _x_axis(pts, X, y, every=2, size=12):
    return "".join(f'<text x="{X(i):.0f}" y="{y}" style="{BODY}" font-size="{size}" font-weight="700" text-anchor="middle" fill="{INK}">{d[:4]}</text>'
                   for i, (d, _) in enumerate(pts) if d.endswith("-01") and int(d[:4]) % every == 0)


def warning_signs() -> str:
    hd, top = head("THE CRACKS SHOWED FIRST", "Shares kept rising until October 2007. But two warning signs had been "
                                              "flashing for more than a year before that.", size=66)
    out = [hd]
    # chart 1: housing starts vs the S&P 500
    x, y, w, h = 26, top + 20, 788, 340
    starts = _pts("starts", "2003-01", "2009-12")
    sp = _pts("sp500", "2003-01", "2009-12")
    cx0, cx1, cy0, cy1 = x + 20, x + w - 20, y + 70, y + h - 40
    X = lambda i: cx0 + (cx1 - cx0) * i / (len(starts) - 1)
    Ys = lambda v: cy1 - (cy1 - cy0) * v / 2400
    Yp = lambda v: cy1 - (cy1 - cy0) * (v - 600) / 1100
    i_h = next(i for i, (d, _) in enumerate(starts) if d == st.WARNING["starts_peak"][0])
    i_s = next(i for i, (d, _) in enumerate(sp) if d == st.WARNING["stock_peak"])
    bars = "".join(f'<rect x="{X(i) - 2.4:.1f}" y="{Ys(v):.1f}" width="4.8" height="{cy1 - Ys(v):.1f}" fill="#f3b37a"/>' for i, (_, v) in enumerate(starts))
    inner = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff"/>',
             text_block(x + 16, y + 32, ["1. AMERICA STOPPED BUILDING HOMES"], size=26, family=HEAD),
             f'<text x="{x + 16}" y="{y + 54}" style="{BODY}" font-size="13.5" font-weight="700" fill="{INK}">'
             f'Bars: new homes started each month (thousands, yearly rate). Line: the S&amp;P 500 share index.</text>',
             bars,
             f'<path d="{_path(sp, X, Yp)}" fill="none" stroke="{INK}" stroke-width="3.5"/>',
             f'<line x1="{cx0}" y1="{cy1}" x2="{cx1}" y2="{cy1}" stroke="{INK}" stroke-width="2.5"/>',
             _x_axis(starts, X, cy1 + 18, every=1),
             f'<line x1="{X(i_h):.0f}" y1="{cy0 - 4}" x2="{X(i_h):.0f}" y2="{cy1}" stroke="{ORANGE}" stroke-width="3" stroke-dasharray="6 4"/>',
             f'<line x1="{X(i_s):.0f}" y1="{cy0 - 4}" x2="{X(i_s):.0f}" y2="{cy1}" stroke="{RED}" stroke-width="3" stroke-dasharray="6 4"/>',
             f'<text x="{X(i_h) - 6:.0f}" y="{cy0 + 8}" style="{HEAD}" font-size="17" text-anchor="end" fill="{ORANGE}">HOME BUILDING PEAKS</text>',
             f'<text x="{X(i_h) - 6:.0f}" y="{cy0 + 26}" style="{HEAD}" font-size="17" text-anchor="end" fill="{ORANGE}">JAN 2006: 2.27M</text>',
             f'<text x="{X(i_s) + 6:.0f}" y="{cy0 + 8}" style="{HEAD}" font-size="17" fill="{RED}">SHARES PEAK</text>',
             f'<text x="{X(i_s) + 6:.0f}" y="{cy0 + 26}" style="{HEAD}" font-size="17" fill="{RED}">OCT 2007</text>',
             f'<path d="M{X(i_h) + 4:.0f},{cy0 + 50} H{X(i_s) - 4:.0f}" stroke="{INK}" stroke-width="3"/>'
             f'<path d="M{X(i_s) - 14:.0f},{cy0 + 42} L{X(i_s) - 4:.0f},{cy0 + 50} L{X(i_s) - 14:.0f},{cy0 + 58} Z" fill="{INK}"/>',
             f'<rect x="{(X(i_h) + X(i_s)) / 2 - 56:.0f}" y="{cy0 + 58}" width="112" height="26" fill="{YELLOW}" stroke="{INK}" stroke-width="2"/>',
             f'<text x="{(X(i_h) + X(i_s)) / 2:.0f}" y="{cy0 + 78}" style="{HEAD}" font-size="19" text-anchor="middle" fill="{INK}">21 MONTHS</text>',
             f'<text x="{cx1 - 4}" y="{cy1 - 8}" style="{HEAD}" font-size="16" text-anchor="end" fill="{INK}">2009 LOW: 478K (−79%)</text>']
    out.append(art.panel(x, y, w, h, content="".join(inner)))
    # chart 2: the yield curve
    y += h + 16
    h2 = 290
    cv = _pts("curve", "2004-01", "2009-12")
    cx0, cx1, cy0, cy1 = x + 20, x + w - 20, y + 74, y + h2 - 36
    X2 = lambda i: cx0 + (cx1 - cx0) * i / (len(cv) - 1)
    Y2 = lambda v: (cy0 + cy1) / 2 - (cy1 - cy0) / 2 * v / 4
    zero = Y2(0)
    neg = "".join(f'<rect x="{X2(i) - 2.6:.1f}" y="{zero:.1f}" width="5.2" height="{Y2(v) - zero:.1f}" fill="{RED}"/>' for i, (_, v) in enumerate(cv) if v < 0)
    pos = "".join(f'<rect x="{X2(i) - 2.6:.1f}" y="{Y2(v):.1f}" width="5.2" height="{zero - Y2(v):.1f}" fill="#9ccc65"/>' for i, (_, v) in enumerate(cv) if v >= 0)
    i_s2 = next(i for i, (d, _) in enumerate(cv) if d == st.WARNING["stock_peak"])
    first_neg = next(i for i, (d, v) in enumerate(cv) if v < 0)
    inner = [f'<rect x="{x}" y="{y}" width="{w}" height="{h2}" fill="#fff"/>',
             text_block(x + 16, y + 32, ["2. THE YIELD CURVE TURNED UPSIDE DOWN"], size=26, family=HEAD),
             text_block(x + 16, y + 54, wrap("Normally, lending money for 10 years pays more than lending for 3 months. When it pays "
                                             "LESS (red), investors expect trouble ahead.", 110), size=13.5, weight="700"),
             pos, neg,
             f'<line x1="{cx0}" y1="{zero:.0f}" x2="{cx1}" y2="{zero:.0f}" stroke="{INK}" stroke-width="2.5"/>',
             _x_axis(cv, X2, cy1 + 18, every=1),
             f'<line x1="{X2(i_s2):.0f}" y1="{cy0}" x2="{X2(i_s2):.0f}" y2="{cy1}" stroke="{RED}" stroke-width="3" stroke-dasharray="6 4"/>',
             f'<text x="{X2(i_s2) - 6:.0f}" y="{cy0 + 16}" style="{HEAD}" font-size="17" text-anchor="end" fill="{RED}">SHARES PEAK</text>',
             f'<text x="{(X2(first_neg) + X2(i_s2)) / 2:.0f}" y="{zero + 44:.0f}" style="{HEAD}" font-size="17" text-anchor="middle" fill="{RED}">UPSIDE DOWN</text>',
             f'<path d="M{X2(first_neg):.0f},{zero + 56:.0f} H{X2(i_s2) - 4:.0f}" stroke="{INK}" stroke-width="3"/>'
             f'<path d="M{X2(i_s2) - 14:.0f},{zero + 48:.0f} L{X2(i_s2) - 4:.0f},{zero + 56:.0f} L{X2(i_s2) - 14:.0f},{zero + 64:.0f} Z" fill="{INK}"/>',
             f'<rect x="{(X2(first_neg) + X2(i_s2)) / 2 - 56:.0f}" y="{zero + 64:.0f}" width="112" height="26" fill="{YELLOW}" stroke="{INK}" stroke-width="2"/>',
             f'<text x="{(X2(first_neg) + X2(i_s2)) / 2:.0f}" y="{zero + 84:.0f}" style="{HEAD}" font-size="19" text-anchor="middle" fill="{INK}">{i_s2 - first_neg} MONTHS</text>',
             f'<text x="{cx0 + 4}" y="{cy1 - 6}" style="{BODY}" font-size="12" font-weight="700" fill="{INK}">10-year minus 3-month US rates, % points</text>']
    out.append(art.panel(x, y, w, h2, content="".join(inner)))
    y += h2 + 16
    box, bh = jargon(26, y, 560, [("Housing starts", "How many new homes builders begin each month. Builders stop when buyers disappear.", "house_down"),
                                  ("Yield curve", "Interest rates for short and long loans, side by side. Upside down = a warning.", "rate_up")],
                     cols=1, size=12.5)
    out.append(box + art.penny(760, H - 18, s=0.42, mood="shock", flip=True)
               + art.bubble(600, y, 210, "So the warning was in HOUSES, not in shares!", tail=(735, H - 140), size=14)
               + art.bear(70, H - 14, s=0.3, mood="calm")
               + art.bubble(120, y + bh + 14, 460, "Both are lights on our scoreboard. They switched on 12 and 14 months "
                                                   "before the peak.", tail=(100, y + bh + 50), size=14))
    return page("".join(out) + num_footer(pno("warning-signs")))


# ---- assemble --------------------------------------------------------------------------------

_FN = {"cover": cover, "machine": machine, "good-times": good_times, "boom-to-danger": boom_to_danger,
       "warning-signs": warning_signs, "timeline-up": lambda: kit.timeline_up(st),
       "timeline-down": lambda: kit.timeline_down(st), "what-popped": lambda: kit.what_popped(st),
       "map": lambda: kit.map_page(st), "fixing-rules": lambda: kit.fixing_rules(st),
       "lesson": lambda: kit.lights(st), "sources": lambda: kit.sources(st)}
PAGES = [(f"{i:02d}-{name}", _FN[name]) for i, name in enumerate(st.ORDER, 1)]

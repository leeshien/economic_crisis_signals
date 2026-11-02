"""Small comic icons, flags and info-graphics. Each function draws centred on (cx, cy)."""
import math
from html import escape

from comics.art import INK, YELLOW, ORANGE, RED, BLUE, TEAL, HEAD, BODY, text_block, wrap

GREEN = "#3fa34d"


def _g(cx, cy, s, body):
    return f'<g transform="translate({cx},{cy}) scale({s})" stroke-linejoin="round" stroke-linecap="round">{body}</g>'


def chart_up(cx, cy, s=1.0, color=GREEN):
    bars = "".join(f'<rect x="{-48 + i * 26}" y="{30 - h}" width="18" height="{h}" fill="{color}" stroke="{INK}" stroke-width="3"/>'
                   for i, h in enumerate((22, 38, 56, 78)))
    return _g(cx, cy, s, bars + f'<path d="M-50,10 L-20,-10 L6,-20 L44,-56" stroke="{INK}" stroke-width="5" fill="none"/>'
                               f'<path d="M30,-58 L46,-58 L46,-42" stroke="{INK}" stroke-width="5" fill="none"/>')


def worker(cx, cy, s=1.0):
    return _g(cx, cy, s, f'<circle cx="0" cy="-30" r="18" fill="#f6c7a1" stroke="{INK}" stroke-width="3"/>'
                         f'<path d="M-20,-38 Q0,-62 20,-38 Z" fill="{YELLOW}" stroke="{INK}" stroke-width="3"/>'
                         f'<path d="M-30,40 L-26,0 Q0,-12 26,0 L30,40 Z" fill="{BLUE}" stroke="{INK}" stroke-width="3"/>'
                         f'<path d="M-8,0 L0,22 L8,0" fill="#fff" stroke="{INK}" stroke-width="2"/>')


def price_tag(cx, cy, s=1.0, text="2%"):
    return _g(cx, cy, s, f'<path d="M-46,-26 L26,-26 L50,0 L26,26 L-46,26 Z" fill="#fff" stroke="{INK}" stroke-width="4"/>'
                         f'<circle cx="30" cy="0" r="6" fill="{INK}"/>'
                         f'<text x="-12" y="11" style="{HEAD}" font-size="32" text-anchor="middle" fill="{GREEN}">{escape(text)}</text>')


def piggy(cx, cy, s=1.0):
    return _g(cx, cy, s, f'<ellipse cx="0" cy="0" rx="46" ry="34" fill="#f7a8c0" stroke="{INK}" stroke-width="4"/>'
                         f'<ellipse cx="44" cy="2" rx="12" ry="10" fill="#f48fb1" stroke="{INK}" stroke-width="3"/>'
                         f'<circle cx="41" cy="0" r="2"/><circle cx="48" cy="0" r="2"/><circle cx="22" cy="-12" r="4" fill="{INK}"/>'
                         f'<path d="M10,-30 L18,-46 L26,-28" fill="#f48fb1" stroke="{INK}" stroke-width="3"/>'
                         f'<rect x="-10" y="-36" width="22" height="6" fill="{INK}"/>'
                         f'<rect x="-30" y="28" width="12" height="16" fill="#f48fb1" stroke="{INK}" stroke-width="3"/>'
                         f'<rect x="14" y="28" width="12" height="16" fill="#f48fb1" stroke="{INK}" stroke-width="3"/>'
                         f'<circle cx="2" cy="-58" r="14" fill="{YELLOW}" stroke="{INK}" stroke-width="3"/>'
                         f'<text x="2" y="-51" style="{HEAD}" font-size="20" text-anchor="middle" fill="{INK}">$</text>')


def computer(cx, cy, s=1.0, screen="www"):
    return _g(cx, cy, s, f'<rect x="-50" y="-44" width="100" height="70" rx="6" fill="#d8dde3" stroke="{INK}" stroke-width="4"/>'
                         f'<rect x="-40" y="-34" width="80" height="50" fill="{BLUE}"/>'
                         f'<text x="0" y="-1" style="{HEAD}" font-size="24" text-anchor="middle" fill="#fff">{escape(screen)}</text>'
                         f'<rect x="-10" y="26" width="20" height="12" fill="#d8dde3" stroke="{INK}" stroke-width="3"/>'
                         f'<rect x="-34" y="38" width="68" height="8" rx="3" fill="#d8dde3" stroke="{INK}" stroke-width="3"/>')


def capitol(cx, cy, s=1.0):
    cols = "".join(f'<rect x="{-40 + i * 16}" y="-6" width="8" height="34" fill="#fff" stroke="{INK}" stroke-width="2"/>' for i, _ in enumerate(range(6)))
    return _g(cx, cy, s, f'<path d="M-30,-14 Q0,-60 30,-14 Z" fill="#fff" stroke="{INK}" stroke-width="3"/>'
                         f'<rect x="-3" y="-66" width="6" height="12" fill="{INK}"/>'
                         f'<rect x="-50" y="-14" width="100" height="10" fill="#fff" stroke="{INK}" stroke-width="3"/>'
                         + cols + f'<rect x="-54" y="28" width="108" height="10" fill="#fff" stroke="{INK}" stroke-width="3"/>')


def cable(cx, cy, s=1.0):
    spool = (f'<ellipse cx="0" cy="0" rx="40" ry="40" fill="{ORANGE}" stroke="{INK}" stroke-width="4"/>'
             f'<ellipse cx="0" cy="0" rx="14" ry="14" fill="#fff" stroke="{INK}" stroke-width="3"/>')
    wire = "".join(f'<path d="M{-30 + i * 6},{-28 + i * 6} A{36 - i * 5},{36 - i * 5} 0 0 1 {30 - i * 6},{-28 + i * 6}" stroke="{YELLOW}" stroke-width="3" fill="none"/>' for i in range(4))
    return _g(cx, cy, s, spool + wire + f'<path d="M40,0 Q70,20 60,46" stroke="{YELLOW}" stroke-width="6" fill="none"/>')


def cash_fire(cx, cy, s=1.0):
    return _g(cx, cy, s, f'<path d="M-30,30 Q-40,-10 -10,-40 Q-12,-10 4,-14 Q0,-40 24,-56 Q20,-20 40,0 Q46,24 30,30 Z" fill="{ORANGE}" stroke="{INK}" stroke-width="4"/>'
                         f'<path d="M-16,30 Q-20,6 -2,-12 Q2,8 14,4 Q26,16 18,30 Z" fill="{YELLOW}" stroke="{INK}" stroke-width="3"/>'
                         f'<rect x="-44" y="26" width="88" height="26" rx="3" fill="#8bc34a" stroke="{INK}" stroke-width="4"/>'
                         f'<text x="0" y="46" style="{HEAD}" font-size="22" text-anchor="middle" fill="{INK}">$$$</text>')


def handshake(cx, cy, s=1.0, left="AOL", right="TIME WARNER"):
    return _g(cx, cy, s, f'<path d="M-70,-6 L-24,-10 L6,10 L-24,22 L-70,18 Z" fill="{BLUE}" stroke="{INK}" stroke-width="4"/>'
                         f'<path d="M70,-6 L24,-10 L-6,10 L24,22 L70,18 Z" fill="{RED}" stroke="{INK}" stroke-width="4"/>'
                         f'<ellipse cx="0" cy="6" rx="26" ry="16" fill="#f6c7a1" stroke="{INK}" stroke-width="4"/>'
                         f'<text x="-50" y="-22" style="{HEAD}" font-size="18" text-anchor="middle" fill="{INK}">{escape(left)}</text>'
                         f'<text x="50" y="-22" style="{HEAD}" font-size="18" text-anchor="middle" fill="{INK}">{escape(right)}</text>')


def rocket(cx, cy, s=1.0, label=""):
    return _g(cx, cy, s, f'<path d="M0,-70 Q34,-40 26,30 L-26,30 Q-34,-40 0,-70 Z" fill="#fff" stroke="{INK}" stroke-width="4"/>'
                         f'<circle cx="0" cy="-20" r="12" fill="{BLUE}" stroke="{INK}" stroke-width="3"/>'
                         f'<path d="M-26,8 L-46,40 L-24,30 Z M26,8 L46,40 L24,30 Z" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
                         f'<path d="M-16,30 Q0,76 16,30 Z" fill="{ORANGE}" stroke="{INK}" stroke-width="3"/>'
                         + (f'<text x="0" y="18" style="{HEAD}" font-size="16" text-anchor="middle" fill="{INK}">{escape(label)}</text>' if label else ""))


def balloon(cx, cy, r=120, label=".COM", string=True):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * 1.15}" fill="{RED}" stroke="{INK}" stroke-width="6"/>'
            f'<ellipse cx="{cx - r * 0.4}" cy="{cy - r * 0.5}" rx="{r * 0.18}" ry="{r * 0.3}" fill="#fff" opacity="0.55" transform="rotate(-25 {cx - r * 0.4} {cy - r * 0.5})"/>'
            f'<path d="M{cx - 14},{cy + r * 1.15 + 14} L{cx},{cy + r * 1.15 - 4} L{cx + 14},{cy + r * 1.15 + 14} Z" fill="{RED}" stroke="{INK}" stroke-width="4"/>'
            + (f'<path d="M{cx},{cy + r * 1.15 + 14} q-30,40 10,70" stroke="{INK}" stroke-width="3" fill="none"/>' if string else "")
            + f'<text x="{cx}" y="{cy + r * 0.2}" style="{HEAD}" font-size="{r * 0.55:.0f}" text-anchor="middle" fill="#fff" stroke="{INK}" stroke-width="3" paint-order="stroke">{escape(label)}</text>')


def pin(x0, y0, x1, y1, n):
    """A push-pin from (x0, y0) (head) toward (x1, y1) (point), with a number on its head."""
    return (f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="#9aa0a6" stroke-width="5"/>'
            f'<circle cx="{x0}" cy="{y0}" r="22" fill="{YELLOW}" stroke="{INK}" stroke-width="4"/>'
            f'<text x="{x0}" y="{y0 + 9}" style="{HEAD}" font-size="26" text-anchor="middle" fill="{INK}">{n}</text>')


# ---- flags (w x h = 72 x 48, centred) ----------------------------------------------------------

_TRICOLOURS = {"FR": (("#002395", "#fff", "#ed2939"), True), "IT": (("#009246", "#fff", "#ce2b37"), True),
               "IE": (("#169b62", "#fff", "#ff883e"), True), "NL": (("#ae1c28", "#fff", "#21468b"), False),
               "AT": (("#ed2939", "#fff", "#ed2939"), False), "RU": (("#fff", "#0039a6", "#d52b1e"), False),
               "IN": (("#ff9933", "#fff", "#138808"), False), "HU": (("#ce2939", "#fff", "#477050"), False)}


def flag(cx, cy, code, s=1.0):
    W, Hh = 72, 48
    x, y = -W / 2, -Hh / 2
    if code == "US":
        stripes = "".join(f'<rect x="{x}" y="{y + i * Hh / 13:.1f}" width="{W}" height="{Hh / 13:.1f}" fill="{"#b22234" if i % 2 == 0 else "#fff"}"/>' for i in range(13))
        stars = "".join(f'<circle cx="{x + 4 + (i % 5) * 6.2:.1f}" cy="{y + 4 + (i // 5) * 6:.1f}" r="1.3" fill="#fff"/>' for i in range(20))
        body = stripes + f'<rect x="{x}" y="{y}" width="{W * 0.42:.1f}" height="{Hh * 7 / 13:.1f}" fill="#3c3b6e"/>' + stars
    elif code == "EU":
        stars = "".join(f'<circle cx="{14 * math.cos(2 * math.pi * i / 12):.1f}" cy="{14 * math.sin(2 * math.pi * i / 12):.1f}" r="2.2" fill="#ffcc00"/>' for i in range(12))
        body = f'<rect x="{x}" y="{y}" width="{W}" height="{Hh}" fill="#003399"/>' + stars
    elif code == "DE":
        body = "".join(f'<rect x="{x}" y="{y + i * Hh / 3:.1f}" width="{W}" height="{Hh / 3:.1f}" fill="{c}"/>' for i, c in enumerate(("#000", "#dd0000", "#ffce00")))
    elif code == "UK":
        body = (f'<rect x="{x}" y="{y}" width="{W}" height="{Hh}" fill="#012169"/>'
                f'<path d="M{x},{y} L{-x},{-y} M{-x},{y} L{x},{-y}" stroke="#fff" stroke-width="9"/>'
                f'<path d="M{x},{y} L{-x},{-y} M{-x},{y} L{x},{-y}" stroke="#c8102e" stroke-width="3"/>'
                f'<path d="M0,{y} L0,{-y} M{x},0 L{-x},0" stroke="#fff" stroke-width="14"/>'
                f'<path d="M0,{y} L0,{-y} M{x},0 L{-x},0" stroke="#c8102e" stroke-width="8"/>')
    elif code == "JP":
        body = f'<rect x="{x}" y="{y}" width="{W}" height="{Hh}" fill="#fff"/><circle cx="0" cy="0" r="14" fill="#bc002d"/>'
    elif code == "CA":
        leaf = "M0,-15 L4,-7 L9,-9 L7,1 L12,-1 L10,5 L4,4 L5,12 L1,12 L0,6 L-1,12 L-5,12 L-4,4 L-10,5 L-12,-1 L-7,1 L-9,-9 L-4,-7 Z"
        body = (f'<rect x="{x}" y="{y}" width="{W}" height="{Hh}" fill="#fff"/>'
                f'<rect x="{x}" y="{y}" width="{W / 4}" height="{Hh}" fill="#d52b1e"/><rect x="{-x - W / 4}" y="{y}" width="{W / 4}" height="{Hh}" fill="#d52b1e"/>'
                f'<path d="{leaf}" fill="#d52b1e"/>')
    elif code in _TRICOLOURS:
        cols, vertical = _TRICOLOURS[code]
        body = "".join((f'<rect x="{x + i * W / 3:.1f}" y="{y}" width="{W / 3:.1f}" height="{Hh}" fill="{c}"/>' if vertical else
                        f'<rect x="{x}" y="{y + i * Hh / 3:.1f}" width="{W}" height="{Hh / 3:.1f}" fill="{c}"/>')
                       for i, c in enumerate(cols))
    else:  # a global body (G20, Basel, FSB...): blue panel with a globe and its name
        body = (f'<rect x="{x}" y="{y}" width="{W}" height="{Hh}" fill="#1f4e8c"/>'
                f'<circle cx="{x + 15}" cy="0" r="10" fill="none" stroke="#fff" stroke-width="2"/>'
                f'<ellipse cx="{x + 15}" cy="0" rx="4.5" ry="10" fill="none" stroke="#fff" stroke-width="1.5"/>'
                f'<path d="M{x + 5},0 H{x + 25}" stroke="#fff" stroke-width="1.5"/>'
                f'<text x="{x + 46}" y="7" style="{HEAD}" font-size="{20 if len(code) <= 3 else 15}" text-anchor="middle" fill="#fff">{escape(code)}</text>')
    return _g(cx, cy, s, body + f'<rect x="{x}" y="{y}" width="{W}" height="{Hh}" fill="none" stroke="{INK}" stroke-width="3"/>')


# ---- info-graphics ---------------------------------------------------------------------------

def thermometer(x, y, h, value, vmax, marks):
    """Vertical thermometer from (x, y) top; marks = [(value, label, color)] drawn as ticks."""
    w = 46
    fill_h = (h - 40) * min(value, vmax) / vmax
    out = [f'<rect x="{x - w / 2}" y="{y}" width="{w}" height="{h - 30}" rx="{w / 2}" fill="#fff" stroke="{INK}" stroke-width="5"/>',
           f'<circle cx="{x}" cy="{y + h - 20}" r="40" fill="{RED}" stroke="{INK}" stroke-width="5"/>',
           f'<rect x="{x - 12}" y="{y + h - 40 - fill_h:.0f}" width="24" height="{fill_h + 30:.0f}" fill="{RED}"/>']
    for v, label, col in marks:
        ty = y + h - 40 - (h - 40) * v / vmax
        out.append(f'<line x1="{x + w / 2}" y1="{ty:.0f}" x2="{x + w / 2 + 24}" y2="{ty:.0f}" stroke="{INK}" stroke-width="4"/>'
                   f'<text x="{x + w / 2 + 32}" y="{ty + 8:.0f}" style="{HEAD}" font-size="26" fill="{col}">{v:.1f}</text>'
                   f'<text x="{x + w / 2 + 96}" y="{ty + 7:.0f}" style="{BODY}" font-size="16" font-weight="700" fill="{INK}">{escape(label)}</text>')
    return "".join(out)


def mini_bars(x, y, w, h, items, color=GREEN, fmt="{:.1f}"):
    """Tiny bar chart: items = [(label, value)]; bars grow upward inside the box."""
    vmax = max(v for _, v in items) or 1
    bw = w / len(items)
    out = []
    for i, (label, v) in enumerate(items):
        bh = (h - 40) * v / vmax
        bx = x + i * bw + bw * 0.18
        out.append(f'<rect x="{bx:.0f}" y="{y + h - 20 - bh:.0f}" width="{bw * 0.64:.0f}" height="{bh:.0f}" fill="{color}" stroke="{INK}" stroke-width="3"/>'
                   f'<text x="{bx + bw * 0.32:.0f}" y="{y + h - 26 - bh:.0f}" style="{HEAD}" font-size="20" text-anchor="middle" fill="{INK}">{fmt.format(v)}</text>'
                   f'<text x="{bx + bw * 0.32:.0f}" y="{y + h - 3:.0f}" style="{BODY}" font-size="12.5" font-weight="700" text-anchor="middle" fill="{INK}">{escape(label)}</text>')
    return "".join(out)


def date_badge(x, y, text, fill=INK, color=YELLOW, size=20):
    w = 18 + len(text) * size * 0.5
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{size + 12}" fill="{fill}"/>'
            f'<text x="{x + 9}" y="{y + size + 3}" style="{HEAD}" font-size="{size}" fill="{color}" letter-spacing="1">{escape(text)}</text>', w)


def event_card(x, y, w, date, title, text, mood="up", size=14.5, text_w=None):
    """Timeline card: date badge, bold title, short text. mood: up (green), down (red), neutral.
    text_w narrows the text column (e.g. to leave room for a picture on the right)."""
    edge = {"up": GREEN, "down": RED, "neutral": BLUE}[mood]
    tw = text_w or w
    lines = wrap(text, int(tw / (size * 0.5)))
    tlines = wrap(title, int(tw / 11))
    h = max(46 + len(tlines) * 22 + len(lines) * size * 1.22 + 8, 96 if text_w else 0)
    badge, _ = date_badge(x + 10, y - 14, date, fill=edge, color="#fff", size=18)
    body = (f'<rect x="{x + 5}" y="{y + 5}" width="{w}" height="{h:.0f}" fill="{INK}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h:.0f}" fill="#fff" stroke="{INK}" stroke-width="3.5"/>'
            f'<rect x="{x}" y="{y}" width="8" height="{h:.0f}" fill="{edge}"/>' + badge
            + text_block(x + 18, y + 44, tlines, size=19, family=HEAD, lh=1.15)
            + text_block(x + 18, y + 44 + len(tlines) * 22 + 2, lines, size=size, weight="700"))
    return body, h

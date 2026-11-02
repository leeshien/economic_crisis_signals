"""Pictograms for the tech-revolution page. Each draws centred on (cx, cy) at roughly 100 x 100 for s=1."""
import math
from html import escape

from comics.art import INK, YELLOW, ORANGE, RED, BLUE, TEAL, HEAD, BODY

GREEN = "#3fa34d"
_sw = 'stroke="#1b1b1f" stroke-linejoin="round" stroke-linecap="round"'


def _g(cx, cy, s, body):
    return f'<g transform="translate({cx:.1f},{cy:.1f}) scale({s})">{body}</g>'


def web(cx, cy, s=1.0):
    """Globe with a 'www' band."""
    return _g(cx, cy, s, f'<circle r="40" fill="{BLUE}" {_sw} stroke-width="4"/>'
                         f'<ellipse rx="18" ry="40" fill="none" {_sw} stroke-width="3"/>'
                         f'<path d="M-40,0 H40 M-34,-20 H34 M-34,20 H34" fill="none" {_sw} stroke-width="3"/>'
                         f'<rect x="-30" y="-12" width="60" height="24" rx="5" fill="#fff" {_sw} stroke-width="3"/>'
                         f'<text y="7" style="{HEAD}" font-size="18" text-anchor="middle" fill="{INK}">www</text>')


def browser(cx, cy, s=1.0):
    """A browser window with a picture in it (Mosaic showed images in pages)."""
    return _g(cx, cy, s, f'<rect x="-44" y="-34" width="88" height="68" rx="5" fill="#fff" {_sw} stroke-width="4"/>'
                         f'<rect x="-44" y="-34" width="88" height="14" fill="#d8dde3" {_sw} stroke-width="4"/>'
                         + "".join(f'<circle cx="{-36 + i * 8}" cy="-27" r="2.6" fill="{c}"/>' for i, c in enumerate((RED, YELLOW, GREEN)))
                         + f'<rect x="-36" y="-14" width="40" height="30" fill="#cfe8f5" {_sw} stroke-width="2"/>'
                         f'<path d="M-36,16 L-22,0 L-12,10 L-4,4 L4,16 Z" fill="{GREEN}"/><circle cx="-6" cy="-6" r="4" fill="{YELLOW}"/>'
                         f'<path d="M10,-10 H36 M10,-2 H32 M10,6 H36 M10,14 H28" {_sw} stroke-width="3"/>')


def parcel(cx, cy, s=1.0):
    """Cardboard box with a smile-shaped tape (online shopping), no brand marks."""
    return _g(cx, cy, s, f'<path d="M-40,-14 L0,-32 L40,-14 L40,30 L0,46 L-40,30 Z" fill="#d9a066" {_sw} stroke-width="4"/>'
                         f'<path d="M-40,-14 L0,4 L40,-14 M0,4 V46" fill="none" {_sw} stroke-width="3"/>'
                         f'<path d="M-30,18 Q-14,30 0,24" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
                         f'<path d="M-20,-23 L20,-5" stroke="#f4e3c3" stroke-width="7"/>')


def gavel(cx, cy, s=1.0):
    """Auction hammer."""
    return _g(cx, cy, s, f'<g transform="rotate(-35)"><rect x="-30" y="-36" width="60" height="26" rx="6" fill="#a0522d" {_sw} stroke-width="4"/>'
                         f'<rect x="-6" y="-10" width="12" height="54" rx="4" fill="#c68642" {_sw} stroke-width="3"/></g>'
                         f'<rect x="-6" y="26" width="52" height="14" rx="4" fill="#8d6e63" {_sw} stroke-width="3"/>'
                         )


def magnifier(cx, cy, s=1.0):
    return _g(cx, cy, s, f'<path d="M14,14 L40,40" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
                         f'<circle cx="-6" cy="-6" r="30" fill="#e3f2fd" {_sw} stroke-width="6"/>'
                         f'<path d="M-20,-10 Q-14,-24 0,-24" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/>')


def chip(cx, cy, s=1.0, label=""):
    pins = "".join(f'<rect x="{-30 + i * 12}" y="-44" width="5" height="10" fill="#9aa0a6"/>'
                   f'<rect x="{-30 + i * 12}" y="34" width="5" height="10" fill="#9aa0a6"/>'
                   f'<rect x="-44" y="{-30 + i * 12}" width="10" height="5" fill="#9aa0a6"/>'
                   f'<rect x="34" y="{-30 + i * 12}" width="10" height="5" fill="#9aa0a6"/>' for i in range(6))
    return _g(cx, cy, s, pins + f'<rect x="-34" y="-34" width="68" height="68" rx="6" fill="#37474f" {_sw} stroke-width="4"/>'
                         f'<rect x="-20" y="-20" width="40" height="40" fill="#607d8b" stroke="{YELLOW}" stroke-width="2"/>'
                         + (f'<text y="8" style="{HEAD}" font-size="22" text-anchor="middle" fill="#fff">{escape(label)}</text>' if label else ""))


def pc(cx, cy, s=1.0):
    return _g(cx, cy, s, f'<rect x="-38" y="-36" width="76" height="54" rx="4" fill="#d8dde3" {_sw} stroke-width="4"/>'
                         f'<rect x="-30" y="-28" width="60" height="38" fill="{BLUE}"/>'
                         f'<rect x="-8" y="18" width="16" height="10" fill="#d8dde3" {_sw} stroke-width="3"/>'
                         f'<rect x="-30" y="28" width="60" height="8" rx="3" fill="#d8dde3" {_sw} stroke-width="3"/>')


def tag(cx, cy, s=1.0, text="", fill="#fff"):
    w = 20 + len(text) * 13
    return _g(cx, cy, s, f'<path d="M{-w / 2},-17 L{w / 2 - 6},-17 L{w / 2 + 10},0 L{w / 2 - 6},17 L{-w / 2},17 Z" fill="{fill}" {_sw} stroke-width="3"/>'
                         f'<circle cx="{w / 2 - 2}" cy="0" r="3.5" fill="{INK}"/>'
                         f'<text x="-4" y="9" style="{HEAD}" font-size="25" text-anchor="middle" fill="{INK}">{escape(text)}</text>')


def house(cx, cy, s=1.0, fill="#fff"):
    return _g(cx, cy, s, f'<path d="M-24,-2 L0,-26 L24,-2 L24,24 L-24,24 Z" fill="{fill}" {_sw} stroke-width="3"/>'
                         f'<rect x="-12" y="4" width="16" height="12" fill="#cfe8f5" {_sw} stroke-width="2"/>')


def mobile(cx, cy, s=1.0, fill="#fff"):
    """A 1990s 'brick' phone."""
    return _g(cx, cy, s, f'<rect x="-6" y="-38" width="5" height="14" fill="{INK}"/>'
                         f'<rect x="-13" y="-26" width="26" height="52" rx="5" fill="{fill}" {_sw} stroke-width="3"/>'
                         f'<rect x="-8" y="-20" width="16" height="12" fill="#cfe8f5" {_sw} stroke-width="2"/>'
                         + "".join(f'<circle cx="{-6 + (i % 3) * 6}" cy="{2 + (i // 3) * 6}" r="1.8" fill="{INK}"/>' for i in range(9)))


def office(cx, cy, s=1.0):
    win = "".join(f'<rect x="{-22 + c * 16}" y="{-30 + r * 16}" width="10" height="10" fill="{YELLOW}" {_sw} stroke-width="1.5"/>'
                  for r in range(4) for c in range(3))
    return _g(cx, cy, s, f'<rect x="-30" y="-40" width="60" height="80" fill="#90a4ae" {_sw} stroke-width="4"/>' + win
                         + f'<rect x="-8" y="26" width="16" height="14" fill="{INK}"/>')


def gauge(cx, cy, s=1.0):
    """Speedometer pushed toward the top: more output per hour."""
    return _g(cx, cy, s, f'<path d="M-40,14 A40,40 0 0 1 40,14 Z" fill="#fff" {_sw} stroke-width="4"/>'
                         f'<path d="M-32,14 A32,32 0 0 1 -16,-14" fill="none" stroke="{RED}" stroke-width="8"/>'
                         f'<path d="M-16,-14 A32,32 0 0 1 16,-14" fill="none" stroke="{YELLOW}" stroke-width="8"/>'
                         f'<path d="M16,-14 A32,32 0 0 1 32,14" fill="none" stroke="{GREEN}" stroke-width="8"/>'
                         f'<path d="M0,14 L26,-12" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><circle cx="0" cy="14" r="6" fill="{INK}"/>'
                         f'<text y="36" style="{HEAD}" font-size="16" text-anchor="middle" fill="{INK}">PER HOUR</text>')


def sun(cx, cy, s=1.0):
    rays = "".join(f'<path d="M{30 * math.cos(a):.1f},{30 * math.sin(a):.1f} L{44 * math.cos(a):.1f},{44 * math.sin(a):.1f}" stroke="{ORANGE}" stroke-width="6" stroke-linecap="round"/>'
                   for a in [i * math.pi / 6 for i in range(12)])
    return _g(cx, cy, s, rays + f'<circle r="24" fill="{YELLOW}" {_sw} stroke-width="4"/>'
                         f'<circle cx="-8" cy="-4" r="3" fill="{INK}"/><circle cx="8" cy="-4" r="3" fill="{INK}"/>'
                         f'<path d="M-10,6 Q0,16 10,6" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')


def pie(cx, cy, r, frac, color=BLUE, rest="#e5e7eb"):
    a = 2 * math.pi * frac - math.pi / 2
    large = 1 if frac > 0.5 else 0
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{rest}" {_sw} stroke-width="4"/>'
            f'<path d="M{cx},{cy} L{cx},{cy - r} A{r},{r} 0 {large} 1 {cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f} Z" '
            f'fill="{color}" {_sw} stroke-width="4"/>')


def pictogram_row(x, y, n, frac_filled, draw, step, color, empty="#ffffff", iw=48, s=1.0):
    """n icons in a row; the first frac_filled*n of them coloured (the last one partly, via clipping).
    iw = drawn icon width at s=1, used to clip the partly-filled icon."""
    full = frac_filled * n
    out = []
    for i in range(n):
        cx = x + i * step
        out.append(draw(cx, y, s, empty))
        part = max(0.0, min(1.0, full - i))
        if part > 0:
            cid = f"pc{int(x)}_{int(y)}_{i}"
            w = iw * s
            out.append(f'<clipPath id="{cid}"><rect x="{cx - w / 2:.1f}" y="{y - 40}" width="{w * part:.1f}" height="80"/></clipPath>'
                       f'<g clip-path="url(#{cid})">{draw(cx, y, s, color)}</g>')
    return "".join(out)

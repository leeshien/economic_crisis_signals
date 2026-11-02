"""Symbols for timeline events and crash triggers, plus the stressed balloon and fibre strands.
Each icon draws centred on (cx, cy), about 90 x 90 at s=1."""
import math
from html import escape

from comics.art import INK, YELLOW, ORANGE, RED, BLUE, HEAD

GREEN = "#3fa34d"
_sw = 'stroke="#1b1b1f" stroke-linejoin="round" stroke-linecap="round"'


def _g(cx, cy, s, body):
    return f'<g transform="translate({cx:.1f},{cy:.1f}) scale({s})">{body}</g>'


def pct_arrow(cx, cy, s=1.0, up=True):
    """Interest rates: a % sign with an arrow going up (red) or down (green)."""
    col = RED if up else GREEN
    arrow = ("M18,22 L18,-14 L8,-14 L26,-36 L44,-14 L34,-14 L34,22 Z" if up else
             "M18,-36 L18,0 L8,0 L26,22 L44,0 L34,0 L34,-36 Z")
    return _g(cx, cy, s, f'<circle cx="-14" cy="-6" r="30" fill="#fff" {_sw} stroke-width="4"/>'
                         f'<text x="-14" y="8" style="{HEAD}" font-size="40" text-anchor="middle" fill="{INK}">%</text>'
                         f'<path d="{arrow}" fill="{col}" {_sw} stroke-width="3"/>')


def rate_up(cx, cy, s=1.0):
    return pct_arrow(cx, cy, s, True)


def rate_down(cx, cy, s=1.0):
    return pct_arrow(cx, cy, s, False)


def peak_flag(cx, cy, s=1.0):
    return _g(cx, cy, s, f'<path d="M-44,34 L-6,-26 L10,-4 L20,-16 L46,34 Z" fill="#90a4ae" {_sw} stroke-width="4"/>'
                         f'<path d="M-14,-14 L-6,-26 L2,-14 Z" fill="#fff"/>'
                         f'<path d="M-6,-26 V-50" stroke="{INK}" stroke-width="3"/>'
                         f'<path d="M-6,-50 L18,-43 L-6,-36 Z" fill="{RED}" {_sw} stroke-width="2"/>')


def chart_down(cx, cy, s=1.0):
    bars = "".join(f'<rect x="{-44 + i * 24}" y="{30 - h}" width="16" height="{h}" fill="{RED}" {_sw} stroke-width="3"/>'
                   for i, h in enumerate((70, 52, 34, 16)))
    return _g(cx, cy, s, bars + f'<path d="M-46,-44 L-10,-20 L10,-10 L40,14" fill="none" stroke="{INK}" stroke-width="5"/>'
                               f'<path d="M26,16 L42,16 L42,0" fill="none" stroke="{INK}" stroke-width="5"/>')


def warning(cx, cy, s=1.0):
    return _g(cx, cy, s, f'<path d="M0,-40 L42,34 L-42,34 Z" fill="{YELLOW}" {_sw} stroke-width="5"/>'
                         f'<text y="26" style="{HEAD}" font-size="50" text-anchor="middle" fill="{INK}">!</text>')


def sock_puppet(cx, cy, s=1.0):
    """A plain sock puppet (the bust's best-known mascot was one)."""
    return _g(cx, cy, s, f'<path d="M-16,40 L-16,-6 Q-16,-38 14,-38 Q40,-38 40,-14 Q40,0 22,2 L18,40 Z" fill="#eceff1" {_sw} stroke-width="4"/>'
                         f'<path d="M-16,40 H18" stroke="{RED}" stroke-width="6"/>'
                         f'<circle cx="8" cy="-22" r="7" fill="#fff" {_sw} stroke-width="2"/><circle cx="10" cy="-21" r="3" fill="{INK}"/>'
                         f'<circle cx="26" cy="-22" r="6" fill="#fff" {_sw} stroke-width="2"/><circle cx="27" cy="-21" r="2.6" fill="{INK}"/>'
                         f'<path d="M24,-6 Q36,-2 40,-10" fill="none" stroke="{INK}" stroke-width="3"/>')


def closed_sign(cx, cy, s=1.0):
    return _g(cx, cy, s, f'<path d="M-20,-30 L0,-46 L20,-30" fill="none" stroke="{INK}" stroke-width="3"/>'
                         f'<circle cx="0" cy="-46" r="4" fill="{INK}"/>'
                         f'<rect x="-46" y="-30" width="92" height="44" rx="5" fill="{RED}" {_sw} stroke-width="4"/>'
                         f'<text y="1" style="{HEAD}" font-size="22" text-anchor="middle" fill="#fff">MARKETS</text>'
                         f'<rect x="-36" y="16" width="72" height="22" fill="#fff" {_sw} stroke-width="3"/>'
                         f'<text y="34" style="{HEAD}" font-size="19" text-anchor="middle" fill="{RED}">CLOSED</text>')


def stamped_doc(cx, cy, s=1.0, stamp="FAKE"):
    """Accounts sheet with a red rubber stamp."""
    rows = "".join(f'<path d="M-24,{-26 + i * 11} H{8 + (i % 2) * 12}" stroke="#90a4ae" stroke-width="3"/>' for i in range(6))
    return _g(cx, cy, s, f'<path d="M-34,-42 H20 L34,-28 V42 H-34 Z" fill="#fff" {_sw} stroke-width="4"/>' + rows
              + f'<g transform="rotate(-18)"><rect x="-46" y="-4" width="92" height="30" rx="4" fill="#fff" fill-opacity="0.7" stroke="{RED}" stroke-width="4"/>'
                f'<text y="19" style="{HEAD}" font-size="{22 if len(stamp) < 6 else 17}" text-anchor="middle" fill="{RED}">{escape(stamp)}</text></g>')


def fake_accounts(cx, cy, s=1.0):
    return stamped_doc(cx, cy, s, "FAKE")


def bankrupt(cx, cy, s=1.0):
    return stamped_doc(cx, cy, s, "BANKRUPT")


def floor_hit(cx, cy, s=1.0):
    return _g(cx, cy, s, f'<path d="M-46,34 H46" stroke="{INK}" stroke-width="5"/>'
                         f'<path d="M-10,-44 H10 V6 H22 L0,30 L-22,6 H-10 Z" fill="{RED}" {_sw} stroke-width="3"/>'
                         f'<path d="M-30,24 L-40,14 M30,24 L40,14 M-24,32 L-38,30 M24,32 L38,30" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')


def padlock_open(cx, cy, s=1.0):
    return _g(cx, cy, s, f'<path d="M-18,-6 V-26 Q-18,-46 2,-46 Q22,-46 22,-30" fill="none" stroke="#9aa0a6" stroke-width="9" stroke-linecap="round"/>'
                         f'<rect x="-34" y="-8" width="56" height="46" rx="6" fill="{YELLOW}" {_sw} stroke-width="4"/>'
                         f'<circle cx="-6" cy="12" r="6" fill="{INK}"/><rect x="-8" y="12" width="4" height="14" fill="{INK}"/>')


def wallet_empty(cx, cy, s=1.0):
    return _g(cx, cy, s, f'<rect x="-40" y="-26" width="80" height="54" rx="8" fill="#8d6e63" {_sw} stroke-width="4"/>'
                         f'<rect x="10" y="-6" width="34" height="18" rx="5" fill="#a1887f" {_sw} stroke-width="3"/>'
                         f'<circle cx="22" cy="3" r="3.5" fill="{INK}"/>'
                         f'<path d="M-24,-34 q6,-10 12,0 q6,-10 12,0" fill="none" stroke="{INK}" stroke-width="3"/>'
                         f'<text x="-12" y="16" style="{HEAD}" font-size="22" text-anchor="middle" fill="#fff">$0</text>')


def cart_x(cx, cy, s=1.0):
    return _g(cx, cy, s, f'<path d="M-46,-30 H-32 L-20,16 H30 L40,-16 H-28" fill="none" stroke="{INK}" stroke-width="5"/>'
                         f'<circle cx="-14" cy="28" r="7" fill="{INK}"/><circle cx="24" cy="28" r="7" fill="{INK}"/>'
                         f'<path d="M-10,-24 L22,8 M22,-24 L-10,8" stroke="{RED}" stroke-width="7" stroke-linecap="round"/>')


def broken_trust(cx, cy, s=1.0):
    return _g(cx, cy, s, f'<path d="M-48,-4 L-14,-8 L-6,6 L-14,18 L-48,16 Z" fill="{BLUE}" {_sw} stroke-width="4"/>'
                         f'<path d="M48,-4 L14,-8 L6,6 L14,18 L48,16 Z" fill="{ORANGE}" {_sw} stroke-width="4"/>'
                         f'<path d="M0,-40 L-8,-18 L6,-12 L-4,14" fill="none" stroke="{RED}" stroke-width="5"/>')


def recession(cx, cy, s=1.0):
    """A factory with a falling arrow."""
    return _g(cx, cy, s, f'<path d="M-44,36 V-6 L-24,-20 V-6 L-4,-20 V-6 L16,-20 V36 Z" fill="#90a4ae" {_sw} stroke-width="4"/>'
                         f'<rect x="20" y="-40" width="14" height="76" fill="#78909c" {_sw} stroke-width="3"/>'
                         f'<path d="M30,-40 H38 V4 H46 L34,22 L22,4 H30 Z" fill="{RED}" {_sw} stroke-width="2"/>'
                         + "".join(f'<rect x="{-36 + i * 18}" y="10" width="10" height="10" fill="{YELLOW}" {_sw} stroke-width="1.5"/>' for i in range(3)))


def fibre_bundle(x, y, w, n=20):
    """n fibre strands across a width; one glows (in use), the rest are 'dark fibre'."""
    out = []
    for i in range(n):
        yy = y + i * 7
        glow = i == n // 2
        out.append(f'<path d="M{x},{yy} C{x + w * 0.35},{yy - 10} {x + w * 0.65},{yy + 10} {x + w},{yy}" fill="none" '
                   f'stroke="{YELLOW if glow else "#4b5563"}" stroke-width="{6 if glow else 4}" stroke-linecap="round"/>')
    return "".join(out)


def needle(hx, hy, tx, ty, n):
    """A pin: round numbered head at (hx, hy), sharp steel point at (tx, ty)."""
    ang = math.atan2(ty - hy, tx - hx)
    bx, by = tx - 18 * math.cos(ang), ty - 18 * math.sin(ang)
    px, py = -math.sin(ang) * 4, math.cos(ang) * 4
    return (f'<line x1="{hx:.1f}" y1="{hy:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="#78858f" stroke-width="8" stroke-linecap="round"/>'
            f'<line x1="{hx:.1f}" y1="{hy:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="#cfd8dc" stroke-width="2.5"/>'
            f'<path d="M{bx + px:.1f},{by + py:.1f} L{tx:.1f},{ty:.1f} L{bx - px:.1f},{by - py:.1f} Z" fill="#78858f" stroke="{INK}" stroke-width="1.5"/>'
            f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="22" fill="{YELLOW}" stroke="{INK}" stroke-width="4"/>'
            f'<text x="{hx:.1f}" y="{hy + 9:.1f}" style="{HEAD}" font-size="26" text-anchor="middle" fill="{INK}">{n}</text>')


def stressed_balloon(cx, cy, r, label, pin_dirs):
    """A balloon stretched to its limit: dents where needles press, strain creases, sweat, wobble lines.
    pin_dirs = angles (radians, screen coordinates) where needles touch. Returns (svg, contact points)."""
    ry = r * 1.12
    pts = []
    for k in range(240):
        a = 2 * math.pi * k / 240
        rr = 1.0 + 0.018 * math.sin(6 * a + 0.4)  # slightly lumpy, over-inflated outline
        for d in pin_dirs:
            diff = math.atan2(math.sin(a - d), math.cos(a - d))
            rr -= 0.06 * math.exp(-(diff / 0.07) ** 2)  # pushed in where a needle presses
        pts.append((cx + r * rr * math.cos(a), cy + ry * rr * math.sin(a)))
    path = "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"
    contacts = [(cx + r * 0.94 * math.cos(d), cy + ry * 0.94 * math.sin(d)) for d in pin_dirs]
    out = [f'<path d="{path}" fill="{RED}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>']
    for (x, y), d in zip(contacts, pin_dirs):  # over-stretched rubber shows paler round each dent
        out.append(f'<ellipse cx="{x - 14 * math.cos(d):.1f}" cy="{y - 14 * math.sin(d):.1f}" rx="13" ry="26" fill="#ff8a80" '
                   f'opacity="0.75" transform="rotate({math.degrees(d):.0f} {x - 14 * math.cos(d):.1f} {y - 14 * math.sin(d):.1f})"/>')
        for k in (-1, 0, 1):  # strain creases fanning inward
            a = d + math.pi + k * 0.4
            out.append(f'<path d="M{x + 12 * math.cos(a):.1f},{y + 12 * math.sin(a):.1f} '
                       f'L{x + 40 * math.cos(a):.1f},{y + 40 * math.sin(a):.1f}" stroke="#7f1d1d" stroke-width="3" stroke-linecap="round"/>')
    out.append(f'<ellipse cx="{cx - r * 0.4}" cy="{cy - ry * 0.45}" rx="{r * 0.15}" ry="{r * 0.28}" fill="#fff" opacity="0.6" '
               f'transform="rotate(-25 {cx - r * 0.4} {cy - ry * 0.45})"/>')
    out.append(f'<path d="M{cx - 14},{cy + ry + 16} L{cx},{cy + ry - 2} L{cx + 14},{cy + ry + 16} Z" fill="{RED}" stroke="{INK}" stroke-width="4"/>')
    for sx, sy, rot in [(-0.7, -1.12, -20), (0.72, -1.1, 20), (-1.16, 0.0, -90), (1.16, 0.05, 90)]:  # sweat drops
        x, y = cx + r * sx, cy + ry * sy
        out.append(f'<path d="M{x:.0f},{y - 12:.0f} Q{x + 9:.0f},{y + 2:.0f} {x:.0f},{y + 8:.0f} Q{x - 9:.0f},{y + 2:.0f} {x:.0f},{y - 12:.0f} Z" '
                   f'fill="#90caf9" stroke="{INK}" stroke-width="2" transform="rotate({rot} {x:.0f} {y:.0f})"/>')
    for side in (-1, 1):  # wobble lines
        for k in range(3):
            x = cx + side * (r * 1.3 + k * 10)
            out.append(f'<path d="M{x:.0f},{cy - 40 + k * 4} Q{x + side * 8:.0f},{cy} {x:.0f},{cy + 40 - k * 4}" fill="none" '
                       f'stroke="{INK}" stroke-width="3" stroke-linecap="round" opacity="{0.8 - 0.25 * k:.2f}"/>')
    out.append(f'<text x="{cx}" y="{cy + r * 0.16}" style="{HEAD}" font-size="{r * 0.5:.0f}" text-anchor="middle" fill="#fff" '
               f'stroke="{INK}" stroke-width="3" paint-order="stroke">{escape(label)}</text>')
    return "".join(out), contacts

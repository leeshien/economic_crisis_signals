"""Icons for the later crisis comics (banks, housing, rescues...). Each draws centred on (cx, cy),
about 90 x 90 at s=1, in the same flat ink-outlined style as symbols.py."""
import math
from html import escape

from comics.art import INK, YELLOW, ORANGE, RED, BLUE, TEAL, HEAD

GREEN = "#3fa34d"
GREY = "#90a4ae"
_sw = 'stroke="#1b1b1f" stroke-linejoin="round" stroke-linecap="round"'


def _g(cx, cy, s, body):
    return f'<g transform="translate({cx:.1f},{cy:.1f}) scale({s})">{body}</g>'


def _house(x=0, y=0, k=1.0, fill="#fff", roof=RED):
    """Small house body in local coordinates (centre x, ground y)."""
    return (f'<g transform="translate({x},{y}) scale({k})">'
            f'<rect x="-30" y="-40" width="60" height="40" fill="{fill}" {_sw} stroke-width="4"/>'
            f'<path d="M-38,-38 L0,-70 L38,-38 Z" fill="{roof}" {_sw} stroke-width="4"/>'
            f'<rect x="-8" y="-24" width="16" height="24" fill="#8d6e63" {_sw} stroke-width="3"/>'
            f'<rect x="-24" y="-32" width="12" height="11" fill="#cfe8f5" {_sw} stroke-width="2"/>'
            f'<rect x="12" y="-32" width="12" height="11" fill="#cfe8f5" {_sw} stroke-width="2"/></g>')


def _arrow(x, y, up=True, col=None, k=1.0):
    col = col or (GREEN if up else RED)
    d = ("M-8,16 V-6 H-18 L0,-28 L18,-6 H8 V16 Z" if up else "M-8,-16 V6 H-18 L0,28 L18,6 H8 V-16 Z")
    return f'<g transform="translate({x},{y}) scale({k})"><path d="{d}" fill="{col}" {_sw} stroke-width="3"/></g>'


# ---- housing ---------------------------------------------------------------------------------

def house_up(cx, cy, s=1.0):
    return _g(cx, cy, s, _house(-10, 36) + _arrow(32, -18, True))


def house_down(cx, cy, s=1.0):
    return _g(cx, cy, s, _house(-10, 36, fill="#eceff1", roof=GREY) + _arrow(32, -14, False))


def house_record(cx, cy, s=1.0, text="69%"):
    """House with a winner's rosette (record home ownership)."""
    return _g(cx, cy, s, _house(-8, 40)
              + f'<path d="M24,-6 L18,30 L28,22 L36,32 L38,-4 Z" fill="{BLUE}" {_sw} stroke-width="3"/>'
              + f'<circle cx="30" cy="-18" r="20" fill="{YELLOW}" {_sw} stroke-width="3.5"/>'
              + f'<text x="30" y="-11" style="{HEAD}" font-size="17" text-anchor="middle" fill="{INK}">{escape(text)}</text>')


def for_sale(cx, cy, s=1.0, text="FORECLOSED"):
    """Yard sign hammered in front of a house."""
    return _g(cx, cy, s, _house(14, 30, k=0.8, fill="#eceff1", roof=GREY)
              + f'<path d="M-26,44 V-10" stroke="#6d4c41" stroke-width="6"/>'
              + f'<rect x="-50" y="-30" width="62" height="34" fill="#fff" {_sw} stroke-width="3.5"/>'
              + f'<text x="-19" y="-16" style="{HEAD}" font-size="13" text-anchor="middle" fill="{INK}">FOR SALE</text>'
              + f'<rect x="-48" y="-12" width="58" height="13" fill="{RED}"/>'
              + f'<text x="-19" y="-1.5" style="{HEAD}" font-size="{11 if len(text) > 8 else 12}" text-anchor="middle" fill="#fff">{escape(text)}</text>')


def flip_house(cx, cy, s=1.0):
    """House with circular arrows: bought to sell again quickly."""
    return _g(cx, cy, s, _house(0, 26, k=0.75)
              + f'<path d="M-44,-6 A44,44 0 0 1 30,-34" fill="none" stroke="{ORANGE}" stroke-width="7"/>'
              + f'<path d="M22,-46 L40,-30 L18,-24 Z" fill="{ORANGE}" {_sw} stroke-width="2"/>'
              + f'<path d="M44,10 A44,44 0 0 1 -30,38" fill="none" stroke="{ORANGE}" stroke-width="7"/>'
              + f'<path d="M-22,50 L-40,34 L-18,28 Z" fill="{ORANGE}" {_sw} stroke-width="2"/>')


def mortgage(cx, cy, s=1.0):
    """A loan paper with a house on it."""
    rows = "".join(f'<path d="M-22,{8 + i * 10} H{14 + (i % 2) * 8}" stroke="{GREY}" stroke-width="3"/>' for i in range(3))
    return _g(cx, cy, s, f'<path d="M-34,-44 H20 L34,-30 V44 H-34 Z" fill="#fff" {_sw} stroke-width="4"/>'
              + _house(0, -4, k=0.45) + rows
              + f'<path d="M-6,40 q6,-10 12,0 q6,-10 12,0" fill="none" stroke="{BLUE}" stroke-width="3"/>')


def liar_loan(cx, cy, s=1.0):
    from comics.symbols import stamped_doc
    return stamped_doc(cx, cy, s, "NO PROOF")


def teaser(cx, cy, s=1.0):
    """Monthly payment jumps after the cheap 'teaser' years."""
    return _g(cx, cy, s, f'<rect x="-46" y="4" width="34" height="32" fill="{GREEN}" {_sw} stroke-width="3.5"/>'
              + f'<text x="-29" y="27" style="{HEAD}" font-size="17" text-anchor="middle" fill="#fff">$</text>'
              + f'<rect x="8" y="-40" width="38" height="76" fill="{RED}" {_sw} stroke-width="3.5"/>'
              + f'<text x="27" y="6" style="{HEAD}" font-size="26" text-anchor="middle" fill="#fff">$$</text>'
              + f'<path d="M-26,-6 Q-20,-34 0,-36" fill="none" stroke="{INK}" stroke-width="4"/>'
              + f'<path d="M-4,-44 L8,-36 L-4,-28 Z" fill="{INK}"/>'
              + f'<path d="M-50,40 H50" stroke="{INK}" stroke-width="4"/>')


# ---- banks and markets -----------------------------------------------------------------------

def bank(cx, cy, s=1.0, cracked=False, label="BANK"):
    cols = "".join(f'<rect x="{-34 + i * 20}" y="-12" width="10" height="38" fill="#fff" {_sw} stroke-width="3"/>' for i in range(4))
    crack = (f'<path d="M-4,-38 L4,-22 L-6,-6 L6,10 L-2,30" fill="none" stroke="{RED}" stroke-width="5"/>' if cracked else "")
    return _g(cx, cy, s, f'<path d="M-46,-16 L0,-46 L46,-16 Z" fill="#eceff1" {_sw} stroke-width="4"/>'
              + f'<text y="-21" style="{HEAD}" font-size="14" text-anchor="middle" fill="{INK}">{escape(label)}</text>'
              + f'<rect x="-42" y="-16" width="84" height="6" fill="#eceff1" {_sw} stroke-width="3"/>' + cols
              + f'<rect x="-46" y="26" width="92" height="10" fill="#eceff1" {_sw} stroke-width="4"/>' + crack)


def bank_cracked(cx, cy, s=1.0):
    return bank(cx, cy, s, cracked=True)


def bank_run(cx, cy, s=1.0):
    """Savers queueing outside a bank."""
    people = "".join(f'<circle cx="{x}" cy="14" r="7" fill="#f6c7a1" {_sw} stroke-width="2.5"/>'
                     f'<path d="M{x - 9},44 V30 Q{x - 9},22 {x},22 Q{x + 9},22 {x + 9},30 V44 Z" fill="{c}" {_sw} stroke-width="2.5"/>'
                     for x, c in ((-34, TEAL), (-14, ORANGE), (6, BLUE), (26, RED)))
    return _g(cx, cy, s, bank(0, -18, 0.62) + people)


def aaa_stamp(cx, cy, s=1.0, text="AAA"):
    return _g(cx, cy, s, f'<g transform="rotate(-14)"><circle r="42" fill="#fff" stroke="{RED}" stroke-width="6"/>'
              + f'<circle r="33" fill="none" stroke="{RED}" stroke-width="2.5"/>'
              + f'<text y="13" style="{HEAD}" font-size="36" text-anchor="middle" fill="{RED}">{escape(text)}</text></g>')


def frozen(cx, cy, s=1.0):
    """Money frozen in an ice cube: banks stopped lending."""
    return _g(cx, cy, s, f'<rect x="-40" y="-40" width="80" height="80" rx="12" fill="#bfe6fb" {_sw} stroke-width="4"/>'
              + f'<path d="M-30,-30 L-14,-30 M-30,-30 L-30,-14" stroke="#fff" stroke-width="5"/>'
              + f'<text y="16" style="{HEAD}" font-size="50" text-anchor="middle" fill="{GREEN}" fill-opacity="0.75">$</text>'
              + "".join(f'<path d="M{x},-48 v-8 M{x - 5},-52 h10" stroke="{BLUE}" stroke-width="3"/>' for x in (-20, 0, 20)))


def lifebuoy(cx, cy, s=1.0, text="$"):
    """A rescue ring: a government or central-bank rescue."""
    segs = "".join(
        f'<path d="M{40 * math.cos(a0):.1f},{40 * math.sin(a0):.1f} A40,40 0 0 1 {40 * math.cos(a1):.1f},{40 * math.sin(a1):.1f} '
        f'L{20 * math.cos(a1):.1f},{20 * math.sin(a1):.1f} A20,20 0 0 0 {20 * math.cos(a0):.1f},{20 * math.sin(a0):.1f} Z" '
        f'fill="{RED if i % 2 == 0 else "#fff"}" {_sw} stroke-width="3"/>'
        for i, (a0, a1) in enumerate((k * math.pi / 2, (k + 1) * math.pi / 2) for k in range(4)))
    return _g(cx, cy, s, segs + f'<text y="11" style="{HEAD}" font-size="28" text-anchor="middle" fill="{INK}">{escape(text)}</text>')


def leverage(cx, cy, s=1.0):
    """See-saw: one small coin of own money against a tall stack of borrowed money."""
    stack = "".join(f'<rect x="10" y="{-18 - i * 7}" width="34" height="7" fill="{YELLOW}" {_sw} stroke-width="2"/>' for i in range(7))
    return _g(cx, cy, s, f'<path d="M-6,36 L0,22 L6,36 Z" fill="{INK}"/>'
              + f'<g transform="rotate(12)"><rect x="-50" y="16" width="100" height="6" fill="#8d6e63" {_sw} stroke-width="2.5"/>'
              + stack + f'<circle cx="-36" cy="9" r="7" fill="{GREEN}" {_sw} stroke-width="2.5"/></g>'
              + f'<text x="-34" y="-8" style="{HEAD}" font-size="15" text-anchor="middle" fill="{GREEN}">$1</text>'
              + f'<text x="26" y="-48" style="{HEAD}" font-size="15" text-anchor="middle" fill="{RED}">$30</text>')


def umbrella_holes(cx, cy, s=1.0):
    """Insurance that could not pay out: an umbrella full of holes in the rain."""
    rain = "".join(f'<path d="M{x},{-48 + (i % 2) * 6} l-4,10" stroke="{BLUE}" stroke-width="3"/>' for i, x in enumerate(range(-36, 40, 12)))
    return _g(cx, cy, s, rain + f'<path d="M-44,0 Q-44,-38 0,-38 Q44,-38 44,0 Q33,-8 22,0 Q11,-8 0,0 Q-11,-8 -22,0 Q-33,-8 -44,0 Z" fill="{RED}" {_sw} stroke-width="3.5"/>'
              + "".join(f'<circle cx="{x}" cy="{y}" r="4.5" fill="#fff" {_sw} stroke-width="1.5"/>' for x, y in ((-22, -18), (8, -26), (26, -12), (-6, -10)))
              + f'<path d="M0,0 V34 Q0,42 -8,42 Q-14,42 -14,36" fill="none" stroke="{INK}" stroke-width="4"/>')


def dominoes(cx, cy, s=1.0):
    """Toppling dominoes: one failure knocks over the next."""
    out = []
    for i, ang in enumerate((-58, -40, -18, 0)):
        x = -40 + i * 24
        out.append(f'<g transform="translate({x},36) rotate({ang})"><rect x="-8" y="-50" width="16" height="50" rx="2" fill="#fff" {_sw} stroke-width="3"/>'
                   f'<circle cx="0" cy="-38" r="2.6" fill="{INK}"/><circle cx="0" cy="-14" r="2.6" fill="{INK}"/>'
                   f'<path d="M-8,-25 H8" stroke="{INK}" stroke-width="2"/></g>')
    return _g(cx, cy, s, "".join(out) + f'<path d="M-48,36 H48" stroke="{INK}" stroke-width="4"/>')


def globe_arrows(cx, cy, s=1.0):
    """A globe with arrows flying out: sold all over the world."""
    arrows = "".join(f'<g transform="rotate({a})"><path d="M0,-34 V-48" stroke="{ORANGE}" stroke-width="5"/>'
                     f'<path d="M-7,-46 L0,-56 L7,-46 Z" fill="{ORANGE}" {_sw} stroke-width="1.5"/></g>' for a in range(0, 360, 60))
    return _g(cx, cy, s, arrows + f'<circle r="32" fill="{BLUE}" {_sw} stroke-width="4"/>'
              + f'<path d="M-20,-18 Q-6,-26 2,-14 Q-6,-4 -16,-6 Z M4,4 Q18,-2 22,12 Q12,24 4,16 Z" fill="{GREEN}" {_sw} stroke-width="2"/>'
              + f'<ellipse rx="13" ry="32" fill="none" {_sw} stroke-width="2"/>')


def vote_no(cx, cy, s=1.0):
    """Parliament dome with a big red X: a vote rejected."""
    from comics.icons import capitol
    return (capitol(cx, cy, s * 0.95)
            + _g(cx, cy, s, f'<path d="M-30,-30 L30,30 M30,-30 L-30,30" stroke="{RED}" stroke-width="12" stroke-linecap="round"/>'
                            f'<path d="M-30,-30 L30,30 M30,-30 L-30,30" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity="0.5"/>'))


def signed_law(cx, cy, s=1.0, text="LAW"):
    rows = "".join(f'<path d="M-22,{-14 + i * 10} H22" stroke="{GREY}" stroke-width="3"/>' for i in range(3))
    return _g(cx, cy, s, f'<path d="M-34,-44 H34 V44 H-34 Z" fill="#fff" {_sw} stroke-width="4"/>'
              + f'<text y="-24" style="{HEAD}" font-size="18" text-anchor="middle" fill="{INK}">{escape(text)}</text>' + rows
              + f'<path d="M-22,28 q8,-14 14,0 q6,-12 12,0 q4,-8 10,-2" fill="none" stroke="{BLUE}" stroke-width="3"/>'
              + f'<g transform="rotate(35 30 20)"><rect x="24" y="-10" width="10" height="44" rx="3" fill="{YELLOW}" {_sw} stroke-width="2.5"/>'
              + f'<path d="M24,34 L29,46 L34,34 Z" fill="{INK}"/></g>')


def rate_zero(cx, cy, s=1.0):
    """Interest rates cut to zero."""
    return _g(cx, cy, s, f'<circle r="42" fill="#fff" {_sw} stroke-width="5"/>'
              + f'<text x="-6" y="18" style="{HEAD}" font-size="52" text-anchor="middle" fill="{GREEN}">0</text>'
              + f'<text x="22" y="8" style="{HEAD}" font-size="26" text-anchor="middle" fill="{INK}">%</text>')


def net_worth(cx, cy, s=1.0):
    """A full money bag: household wealth."""
    return _g(cx, cy, s, f'<path d="M-14,-34 L14,-34 L8,-22 Q40,-8 38,20 Q36,42 0,42 Q-36,42 -38,20 Q-40,-8 -8,-22 Z" fill="#c9a227" {_sw} stroke-width="4"/>'
              + f'<path d="M-12,-24 H12" stroke="{INK}" stroke-width="4"/>'
              + f'<text y="26" style="{HEAD}" font-size="34" text-anchor="middle" fill="#fff" stroke="{INK}" stroke-width="1">$</text>')


def calm_sea(cx, cy, s=1.0):
    """A small boat on flat water: the calm 'Great Moderation'."""
    return _g(cx, cy, s, f'<circle cx="28" cy="-26" r="14" fill="{YELLOW}" {_sw} stroke-width="3"/>'
              + f'<path d="M-30,10 H30 L20,24 H-20 Z" fill="{RED}" {_sw} stroke-width="3.5"/>'
              + f'<path d="M-2,10 V-36 L-28,4 Z" fill="#fff" {_sw} stroke-width="3"/>'
              + f'<path d="M-48,32 q8,-6 16,0 t16,0 t16,0 t16,0 t16,0 t16,0" fill="none" stroke="{BLUE}" stroke-width="4"/>')


def iceland(cx, cy, s=1.0):
    """Iceland's flag on a cracked bank."""
    return _g(cx, cy, s, bank(0, 8, 0.8, cracked=True)
              + f'<path d="M30,-30 V-62" stroke="{INK}" stroke-width="3"/>'
              + f'<rect x="30" y="-62" width="30" height="20" fill="#02529c" {_sw} stroke-width="2"/>'
              + f'<path d="M30,-52 H60 M40,-62 V-42" stroke="#fff" stroke-width="6"/>'
              + f'<path d="M30,-52 H60 M40,-62 V-42" stroke="#dc1e35" stroke-width="3"/>')


def handshake2(cx, cy, s=1.0, left="BofA", right="CW"):
    from comics.icons import handshake
    return handshake(cx, cy, s * 0.75, left, right)


def countrywide(cx, cy, s=1.0):
    return handshake2(cx, cy, s, "BANK OF AMERICA", "COUNTRYWIDE")


def bear_sold(cx, cy, s=1.0):
    """A price tag reading $2 a share."""
    return _g(cx, cy, s, f'<path d="M-40,-20 H20 L42,0 L20,20 H-40 Z" fill="{YELLOW}" {_sw} stroke-width="4"/>'
              + f'<circle cx="24" cy="0" r="4" fill="{INK}"/>'
              + f'<text x="-12" y="10" style="{HEAD}" font-size="28" text-anchor="middle" fill="{RED}">$2</text>'
              + f'<text x="-12" y="40" style="{HEAD}" font-size="15" text-anchor="middle" fill="{INK}">A SHARE</text>')


def house_of_cards(cx, cy, s=1.0, labels=("LOANS", "AAA", "CDO", "BANK", "HOUSE", "DEBT")):
    """A triangle of playing cards; the top pair tips over."""
    def card(x, y, ang, lab):
        return (f'<g transform="translate({x},{y}) rotate({ang})"><rect x="-17" y="-52" width="34" height="52" rx="4" fill="#fff" {_sw} stroke-width="3"/>'
                f'<text x="0" y="-22" style="{HEAD}" font-size="11" text-anchor="middle" fill="{RED}">{escape(lab)}</text></g>')
    out, k = [], 0
    for row, n in enumerate((3, 2, 1)):
        y = 50 - row * 54
        for i in range(n):
            x = (i - (n - 1) / 2) * 44
            tilt = 22 if row < 2 else 40
            out.append(card(x - 11, y, 18 if row < 2 else 30, labels[k % len(labels)]) + card(x + 11, y, -18 if row < 2 else -6, labels[(k + 1) % len(labels)]))
            k += 2
        if row < 2:
            out.append(f'<rect x="{-(n - 1) * 22 - 26}" y="{y - 56}" width="{(n - 1) * 44 + 52}" height="5" fill="#fff" {_sw} stroke-width="2.5"/>')
    return _g(cx, cy, s, "".join(out))


def handshake_sell(cx, cy, s=1.0):
    """A loan paper passed on with an arrow: 'sell it on'."""
    return (mortgage(cx - 22 * s, cy, s * 0.62)
            + _g(cx, cy, s, f'<path d="M-2,-6 H22 V-18 L46,2 L22,22 V10 H-2 Z" fill="{ORANGE}" {_sw} stroke-width="3"/>'
                            f'<text x="18" y="7" style="{HEAD}" font-size="13" text-anchor="middle" fill="{INK}">SOLD</text>'))


def bundle(cx, cy, s=1.0):
    """Many loan papers tied into one bundle."""
    papers = "".join(f'<rect x="{-36 + i * 5}" y="{-30 + i * 6}" width="60" height="44" fill="#fff" {_sw} stroke-width="3"/>' for i in range(4))
    return _g(cx, cy, s, papers + _house(10, 26, k=0.32)
              + f'<path d="M-2,-30 V40 M-40,6 H42" stroke="{RED}" stroke-width="5"/>'
              + f'<circle cx="-2" cy="6" r="6" fill="{RED}" {_sw} stroke-width="2"/>')


def big_fish(cx, cy, s=1.0):
    """A big fish swallowing a small one: a takeover of a failing firm."""
    return _g(cx, cy, s, f'<path d="M50,0 Q16,-34 -24,-8 L-38,-26 L-34,0 L-38,26 L-24,8 Q16,34 50,0 Z" '
                         f'fill="{BLUE}" {_sw} stroke-width="3.5"/>'
                         f'<path d="M50,0 L22,-16 L22,16 Z" fill="#fff8e7" {_sw} stroke-width="3"/>'
                         f'<circle cx="6" cy="-12" r="4" fill="{INK}"/>'
                         f'<path d="M30,0 Q40,-10 50,0 Q40,10 30,0 Z M50,0 L57,-7 L57,7 Z" fill="{ORANGE}" {_sw} stroke-width="2.5"/>')


# ---- balloon art: what the bubble was made of (drawn inside the red balloon) -------------------

def bubble_subprime(cx, cy, r=118):
    """A wobbly pile of houses bought with subprime loans, a soaring price tag, and a banner."""
    k = r / 118
    roofs = [YELLOW, BLUE, ORANGE, TEAL, YELLOW, BLUE]
    rows = [(18, [-52, 0, 52]), (-24, [-26, 26]), (-66, [0])]
    body, n = [], 0
    for gy, xs in rows:
        for x in xs:
            tilt = (-4, 3, -2, 5, -3, 2)[n]
            body.append(f'<g transform="rotate({tilt} {x} {gy})">{_house(x, gy, 0.6, "#fff8e7", roofs[n])}</g>')
            n += 1
    body.append(_arrow(-58, -74, True, k=0.8))  # prices only go up...
    body.append(f'<path d="M14,-100 L38,-96" stroke="{INK}" stroke-width="2.5"/>'
                f'<path d="M38,-108 L78,-102 L76,-82 L36,-88 L30,-99 Z" fill="{YELLOW}" {_sw} stroke-width="3"/>'
                f'<text x="56" y="-89" style="{HEAD}" font-size="15" text-anchor="middle" fill="{INK}" '
                f'transform="rotate(8 56 -89)">$$$</text>')
    body.append(f'<path d="M-104,30 L96,30 L104,46 L96,62 L-96,62 L-104,46 Z" fill="{YELLOW}" {_sw} stroke-width="4"/>'
                f'<text x="0" y="56" style="{HEAD}" font-size="30" text-anchor="middle" fill="{INK}">SUBPRIME</text>'
                f'<text x="0" y="90" style="{HEAD}" font-size="19" text-anchor="middle" fill="#fff" stroke="{INK}" '
                f'stroke-width="3" paint-order="stroke">HOUSING BUBBLE</text>')
    return _g(cx, cy, k, "".join(body))


# ---- 2020: pandemic, lockdown, rescue --------------------------------------------------------

def _person(x, y, col=BLUE, k=1.0):
    return (f'<g transform="translate({x},{y}) scale({k})"><circle cx="0" cy="-30" r="9" fill="#f6c7a1" {_sw} stroke-width="2.5"/>'
            f'<path d="M-12,8 V-12 Q-12,-20 0,-20 Q12,-20 12,-12 V8 Z" fill="{col}" {_sw} stroke-width="2.5"/></g>')


def virus(cx, cy, s=1.0):
    """A coronavirus: a ball with knobbed spikes."""
    spikes = "".join(f'<path d="M{24 * math.cos(a):.1f},{24 * math.sin(a):.1f} L{38 * math.cos(a):.1f},{38 * math.sin(a):.1f}" stroke="{INK}" stroke-width="4"/>'
                     f'<circle cx="{40 * math.cos(a):.1f}" cy="{40 * math.sin(a):.1f}" r="6" fill="{RED}" {_sw} stroke-width="2.5"/>'
                     for a in (k * math.pi / 5 for k in range(10)))
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ff8a80"/>' for x, y, r in ((-8, -8, 5), (9, 4, 4), (-4, 11, 3.5), (10, -11, 3)))
    return _g(cx, cy, s, spikes + f'<circle r="27" fill="#ef5350" {_sw} stroke-width="4"/>' + dots)


def globe_virus(cx, cy, s=1.0):
    """The whole world caught it: a globe with virus particles."""
    return _g(cx, cy, s, f'<circle r="34" fill="#90caf9" {_sw} stroke-width="4"/>'
              + f'<path d="M-20,-22 q10,6 6,16 q-8,6 -2,16 q8,2 6,14 M8,-30 q-4,12 8,14 q12,0 10,14 q-6,8 4,14" fill="none" '
                f'stroke="{GREEN}" stroke-width="6" stroke-linecap="round"/>'
              + virus(-32, -30, 0.36) + virus(36, -18, 0.3) + virus(26, 34, 0.32))


def lockdown(cx, cy, s=1.0):
    """A shop front with its shutter down and a padlock."""
    slats = "".join(f'<path d="M-38,{-14 + i * 9} H38" stroke="#78909c" stroke-width="2.5"/>' for i in range(6))
    return _g(cx, cy, s, f'<rect x="-44" y="-30" width="88" height="70" fill="#cfd8dc" {_sw} stroke-width="4"/>'
              + f'<rect x="-48" y="-44" width="96" height="16" fill="{RED}" {_sw} stroke-width="3.5"/>'
              + f'<text y="-32" style="{HEAD}" font-size="13" text-anchor="middle" fill="#fff">CLOSED</text>' + slats
              + f'<path d="M-9,14 V6 A9,9 0 0 1 9,6 V14" fill="none" stroke="{INK}" stroke-width="4"/>'
              + f'<rect x="-13" y="13" width="26" height="20" rx="3" fill="{YELLOW}" {_sw} stroke-width="3"/>')


def siren(cx, cy, s=1.0):
    """An emergency light: an alarm is raised."""
    rays = "".join(f'<path d="M{30 * math.cos(a):.1f},{-6 + 30 * math.sin(a):.1f} L{44 * math.cos(a):.1f},{-6 + 44 * math.sin(a):.1f}" '
                   f'stroke="{RED}" stroke-width="5" stroke-linecap="round"/>'
                   for a in (math.radians(d) for d in (-160, -125, -90, -55, -20)))
    return _g(cx, cy, s, rays + f'<path d="M-22,24 V-4 A22,22 0 0 1 22,-4 V24 Z" fill="#ef5350" {_sw} stroke-width="4"/>'
              + f'<path d="M-10,-6 A10,10 0 0 1 0,-16" fill="none" stroke="#fff" stroke-width="4"/>'
              + f'<rect x="-32" y="24" width="64" height="14" fill="{INK}"/>')


def jobs_lost(cx, cy, s=1.0):
    """A worker carrying out a box of belongings: laid off."""
    return _g(cx, cy, s, _person(-14, 30, TEAL, 1.3)
              + f'<rect x="-6" y="0" width="40" height="30" fill="#d7ccc8" {_sw} stroke-width="3.5"/>'
              + f'<path d="M4,0 V-10 H14 V0 M22,0 L28,-12" stroke="{INK}" stroke-width="3" fill="none"/>'
              + _arrow(36, -26, False, k=0.75))


def jobless_queue(cx, cy, s=1.0):
    """People queueing for unemployment benefits."""
    sign = (f'<rect x="-48" y="-48" width="96" height="22" fill="#fff" {_sw} stroke-width="3"/>'
            f'<text y="-32" style="{HEAD}" font-size="11.5" text-anchor="middle" fill="{INK}">UNEMPLOYMENT</text>')
    return _g(cx, cy, s, sign + "".join(_person(x, 38, c, 1.15) for x, c in ((-33, TEAL), (-11, ORANGE), (11, BLUE), (33, RED))))


def oil_barrel(cx, cy, s=1.0, text=""):
    """An oil barrel with a falling-price arrow (or a price tag)."""
    tag = (f'<rect x="0" y="-46" width="50" height="24" rx="4" fill="{YELLOW}" {_sw} stroke-width="3"/>'
           f'<text x="25" y="-28" style="{HEAD}" font-size="16" text-anchor="middle" fill="{RED}">{escape(text)}</text>')
    return _g(cx, cy, s, f'<rect x="-34" y="-30" width="48" height="70" rx="6" fill="#37474f" {_sw} stroke-width="4"/>'
              + f'<path d="M-34,-8 H14 M-34,18 H14" stroke="#90a4ae" stroke-width="4"/>'
              + f'<path d="M-18,0 q8,-14 16,0 q0,10 -8,10 q-8,0 -8,-10 Z" fill="{ORANGE}"/>'
              + (tag if text else _arrow(32, 0, False, k=0.85)))


def oil_negative(cx, cy, s=1.0):
    return oil_barrel(cx, cy, s, "−$37")


def stimulus_check(cx, cy, s=1.0):
    """A government cheque in an envelope."""
    return _g(cx, cy, s, f'<rect x="-44" y="-10" width="88" height="50" fill="#fff8e1" {_sw} stroke-width="3.5"/>'
              + f'<path d="M-44,-10 L0,20 L44,-10" fill="none" stroke="{INK}" stroke-width="3"/>'
              + f'<g transform="rotate(-8)"><rect x="-40" y="-44" width="80" height="38" fill="#c8e6c9" {_sw} stroke-width="3.5"/>'
              + f'<text x="0" y="-19" style="{HEAD}" font-size="19" text-anchor="middle" fill="{GREEN}">$1,200</text></g>')


def money_printer(cx, cy, s=1.0):
    """A printer pushing out banknotes: the central bank creating money."""
    bills = "".join(f'<g transform="translate({x},{y}) rotate({a})"><rect x="-16" y="-9" width="32" height="18" fill="#a5d6a7" {_sw} stroke-width="2.5"/>'
                    f'<text y="5" style="{HEAD}" font-size="12" text-anchor="middle" fill="{GREEN}">$</text></g>'
                    for x, y, a in ((-20, 34, -14), (4, 40, 8), (26, 32, 18)))
    return _g(cx, cy, s, f'<rect x="-28" y="-44" width="56" height="22" fill="#fff" {_sw} stroke-width="3"/>'
              + f'<rect x="-44" y="-24" width="88" height="40" rx="6" fill="#90a4ae" {_sw} stroke-width="4"/>'
              + f'<circle cx="30" cy="-12" r="4" fill="{GREEN}"/><rect x="-30" y="10" width="60" height="6" fill="{INK}"/>' + bills)


def cash_dash(cx, cy, s=1.0):
    """A money bag racing away with speed lines: everyone selling to raise cash."""
    lines = "".join(f'<path d="M{-50 + k * 4},{-8 + k * 12} H{-24 + k * 4}" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>' for k in range(3))
    return _g(cx, cy, s, lines + f'<path d="M-14,40 Q-24,0 0,-14 L-8,-30 H22 L14,-14 Q38,0 28,40 Z" fill="#d7ccc8" {_sw} stroke-width="4"/>'
              + f'<path d="M-6,-14 H20" stroke="{INK}" stroke-width="4"/>'
              + f'<text x="7" y="26" style="{HEAD}" font-size="30" text-anchor="middle" fill="{GREEN}">$</text>')


def bbb_stamp(cx, cy, s=1.0):
    return aaa_stamp(cx, cy, s, "BBB")


def buyback(cx, cy, s=1.0):
    """A company buying back its own shares: an arrow from the share certificate back into the firm."""
    wins = "".join(f'<rect x="{-32 + (i % 2) * 18}" y="{-10 + (i // 2) * 16}" width="10" height="9" fill="#cfe8f5" {_sw} stroke-width="1.5"/>'
                   for i in range(6))
    return _g(cx, cy, s, f'<rect x="-40" y="-20" width="44" height="60" fill="#eceff1" {_sw} stroke-width="4"/>' + wins
              + f'<rect x="12" y="-46" width="36" height="40" fill="#fff" {_sw} stroke-width="3"/>'
              + f'<text x="30" y="-21" style="{HEAD}" font-size="12" text-anchor="middle" fill="{BLUE}">SHARE</text>'
              + f'<path d="M30,-4 Q30,26 12,26" fill="none" stroke="{ORANGE}" stroke-width="6"/>'
              + f'<path d="M16,16 L4,26 L16,36 Z" fill="{ORANGE}" {_sw} stroke-width="2"/>')


def trade_deal(cx, cy, s=1.0):
    return handshake2(cx, cy, s, left="US", right="CHINA")


def calendar(cx, cy, s=1.0, top="128", bottom="MONTHS"):
    """A calendar page."""
    rings = "".join(f'<rect x="{x}" y="-48" width="7" height="18" rx="3" fill="{INK}"/>' for x in (-24, 17))
    return _g(cx, cy, s, f'<rect x="-40" y="-40" width="80" height="80" rx="6" fill="#fff" {_sw} stroke-width="4"/>'
              + f'<rect x="-40" y="-40" width="80" height="22" rx="6" fill="{RED}" {_sw} stroke-width="4"/>' + rings
              + f'<text y="16" style="{HEAD}" font-size="32" text-anchor="middle" fill="{INK}">{escape(top)}</text>'
              + f'<text y="33" style="{HEAD}" font-size="13" text-anchor="middle" fill="{INK}">{escape(bottom)}</text>')


def plane_grounded(cx, cy, s=1.0):
    """A plane parked under a no-entry sign: travel stopped."""
    return _g(cx, cy, s, f'<path d="M-44,10 L30,10 Q46,10 46,2 Q46,-6 30,-6 L-30,-6 L-44,-24 L-50,-24 L-42,-4 Z" fill="#eceff1" {_sw} stroke-width="3.5"/>'
              + f'<path d="M-6,-6 L10,-30 H20 L14,-6 M-6,10 L8,30 H18 L14,10" fill="#b0bec5" {_sw} stroke-width="3"/>'
              + f'<circle cx="30" cy="-30" r="14" fill="{RED}" {_sw} stroke-width="3"/><rect x="22" y="-33" width="16" height="6" fill="#fff"/>'
              + f'<path d="M-50,36 H50" stroke="{INK}" stroke-width="4"/>')


def circuit_breaker(cx, cy, s=1.0):
    """A big pause button over a falling chart: trading halted."""
    return _g(cx, cy, s, f'<path d="M-44,-30 L-20,-10 L0,-20 L40,30" fill="none" stroke="{RED}" stroke-width="6"/>'
              + f'<circle cx="4" cy="2" r="26" fill="{YELLOW}" {_sw} stroke-width="4"/>'
              + f'<rect x="-8" y="-11" width="7" height="26" fill="{INK}"/><rect x="9" y="-11" width="7" height="26" fill="{INK}"/>')


def _factory(extra):
    return (f'<path d="M-44,36 V-6 L-24,-20 V-6 L-4,-20 V-6 L16,-20 V36 Z" fill="#90a4ae" {_sw} stroke-width="4"/>'
            + "".join(f'<rect x="{-36 + i * 18}" y="10" width="10" height="10" fill="{YELLOW}" {_sw} stroke-width="1.5"/>' for i in range(3))
            + extra)


def factory_hours(cx, cy, s=1.0):
    """A factory with a clock: fewer hours worked."""
    return _g(cx, cy, s, _factory(f'<circle cx="28" cy="-14" r="20" fill="#fff" {_sw} stroke-width="3.5"/>'
                                  f'<path d="M28,-14 V-28 M28,-14 L38,-10" stroke="{INK}" stroke-width="3"/>'
                                  + _arrow(32, 24, False, k=0.6)))


def factory_up(cx, cy, s=1.0):
    """A factory starting up again."""
    return _g(cx, cy, s, _factory(f'<path d="M-30,-24 q-6,-10 4,-16 q4,-8 12,-4" fill="none" stroke="#b0bec5" stroke-width="5"/>'
                                  + _arrow(34, -6, True, k=0.85)))


def wage_shield(cx, cy, s=1.0):
    """A pay packet kept dry under an umbrella: the state paying wages (furlough)."""
    return _g(cx, cy, s, f'<path d="M-44,-6 A44,36 0 0 1 44,-6 Z" fill="{BLUE}" {_sw} stroke-width="4"/>'
              + f'<path d="M0,-6 V12" stroke="{INK}" stroke-width="4"/>'
              + f'<rect x="-30" y="10" width="60" height="32" fill="#fff8e1" {_sw} stroke-width="3.5"/>'
              + f'<text y="33" style="{HEAD}" font-size="20" text-anchor="middle" fill="{GREEN}">80%</text>')


def safe_bonds_sold(cx, cy, s=1.0):
    """Even 'safe' government bonds dumped for cash."""
    return _g(cx, cy, s, f'<g transform="rotate(-10)"><rect x="-44" y="-36" width="64" height="46" fill="#fff" {_sw} stroke-width="3.5"/>'
              + f'<text x="-12" y="-16" style="{HEAD}" font-size="13" text-anchor="middle" fill="{BLUE}">US GOV</text>'
              + f'<text x="-12" y="0" style="{HEAD}" font-size="13" text-anchor="middle" fill="{BLUE}">BOND</text></g>'
              + f'<rect x="-4" y="8" width="52" height="26" fill="{RED}" {_sw} stroke-width="3"/>'
              + f'<text x="22" y="27" style="{HEAD}" font-size="17" text-anchor="middle" fill="#fff">SELL!</text>')


def bubble_boom(cx, cy, r=118):
    """Balloon art for 2020: an 11-year stock boom drawn as a climbing chart over a city."""
    k = r / 118
    towers = []
    for x, w, h in ((-92, 30, 40), (-58, 34, 70), (-20, 30, 52), (14, 36, 84), (54, 32, 48)):
        towers.append(f'<rect x="{x}" y="{30 - h}" width="{w}" height="{h}" fill="#fff8e7" {_sw} stroke-width="3"/>')
        for c in range((w - 6) // 10):
            for rr in range((h - 16) // 14):
                towers.append(f'<rect x="{x + 5 + c * 10}" y="{38 - h + rr * 14}" width="5" height="7" fill="{YELLOW}"/>')
    pts = [(-96, 10), (-70, -2), (-52, -16), (-34, -8), (-12, -34), (8, -46), (26, -40), (46, -66), (66, -76), (80, -96)]
    path = "M" + " L".join(f"{x},{y}" for x, y in pts)
    return _g(cx, cy, k, "".join(towers)
              + f'<path d="{path}" fill="none" stroke="#fff" stroke-width="12" stroke-linejoin="round"/>'
              + f'<path d="{path}" fill="none" stroke="{GREEN}" stroke-width="6" stroke-linejoin="round"/>'
              + f'<path d="M70,-104 L92,-108 L84,-86 Z" fill="{GREEN}" {_sw} stroke-width="2.5"/>'
              + f'<path d="M-104,30 L96,30 L104,46 L96,62 L-96,62 L-104,46 Z" fill="{YELLOW}" {_sw} stroke-width="4"/>'
              + f'<text x="0" y="56" style="{HEAD}" font-size="27" text-anchor="middle" fill="{INK}">11-YEAR BOOM</text>'
              + f'<text x="0" y="90" style="{HEAD}" font-size="19" text-anchor="middle" fill="#fff" stroke="{INK}" '
                f'stroke-width="3" paint-order="stroke">RECORD-HIGH STOCKS</text>')

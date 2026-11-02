"""Comic building blocks as SVG strings: panels, captions, speech bubbles, bursts, the narrators.

Page coordinates: an A4 page is 840 x 1188 units (4 units = 1 mm).
"""
import math
from html import escape

W, H = 840, 1188
INK = "#1b1b1f"
PAPER = "#fff8e7"
YELLOW, ORANGE, RED, BLUE, TEAL = "#ffd23f", "#f78c2e", "#e63b2e", "#2e86de", "#16a3a0"
HEAD = "font-family:Bangers,Impact,sans-serif"
BODY = "font-family:'Comic Neue','Comic Sans MS',sans-serif"


def defs() -> str:
    """Shared patterns: halftone dots and hatching."""
    return (f'<defs>'
            f'<pattern id="dots" width="9" height="9" patternUnits="userSpaceOnUse">'
            f'<circle cx="4.5" cy="4.5" r="1.6" fill="{INK}" fill-opacity="0.16"/></pattern>'
            f'<pattern id="dots-big" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<circle cx="7" cy="7" r="3" fill="{INK}" fill-opacity="0.10"/></pattern>'
            f'<pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<line x1="0" y1="0" x2="0" y2="7" stroke="{INK}" stroke-opacity="0.22" stroke-width="1.4"/></pattern>'
            f'</defs>')


def wrap(text: str, width: int) -> list:
    """Greedy word wrap by character count."""
    lines, cur = [], ""
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + ([cur] if cur else [])


def text_block(x, y, text, size=18, width=40, weight="400", anchor="start", fill=INK, lh=1.22, family=BODY) -> str:
    out = []
    for i, line in enumerate(text if isinstance(text, list) else wrap(text, width)):
        out.append(f'<text x="{x}" y="{y + i * size * lh:.1f}" style="{family}" font-size="{size}" '
                   f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{escape(line)}</text>')
    return "".join(out)


def panel(x, y, w, h, fill="#ffffff", content="", tilt=0) -> str:
    """A bordered comic panel; content is clipped to it."""
    cid = f"clip{int(x)}_{int(y)}_{int(w)}"
    t = f' transform="rotate({tilt} {x + w / 2} {y + h / 2})"' if tilt else ""
    return (f'<g{t}><clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'
            f'<g clip-path="url(#{cid})">{content}</g>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{INK}" stroke-width="5"/></g>')


def caption(x, y, w, text, size=17, fill=YELLOW, width=None) -> tuple:
    """Narration box (yellow, square). Returns (svg, height)."""
    lines = wrap(text, width or int(w / (size * 0.5)))
    h = 16 + len(lines) * size * 1.22
    svg = (f'<rect x="{x + 4}" y="{y + 4}" width="{w}" height="{h:.0f}" fill="{INK}"/>'
           f'<rect x="{x}" y="{y}" width="{w}" height="{h:.0f}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
           + text_block(x + 12, y + 8 + size, lines, size=size, weight="700"))
    return svg, h


def bubble(x, y, w, text, tail, size=19, shout=False, width=None) -> str:
    """Speech bubble with its top-left corner at (x, y); tail = (tx, ty) point it aims at."""
    lines = wrap(text, width or int(w / (size * 0.52)))
    h = 24 + len(lines) * size * 1.2
    cx, cy = x + w / 2, y + h / 2
    tx, ty = tail
    # tail base sits on the bubble edge nearest the speaker
    bx = min(max(tx, x + w * 0.25), x + w * 0.75)
    by = y + h if ty > cy else y
    tail_path = f'M{bx - 14:.0f},{by:.0f} L{tx:.0f},{ty:.0f} L{bx + 14:.0f},{by:.0f} Z'
    rx = h / 2 if h < 70 else 26
    stroke = 4 if shout else 3
    font = HEAD if shout else BODY
    return (f'<path d="{tail_path}" fill="#fff" stroke="{INK}" stroke-width="{stroke}" stroke-linejoin="round"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h:.0f}" rx="{rx:.0f}" fill="#fff" stroke="{INK}" stroke-width="{stroke}"/>'
            f'<path d="M{bx - 12:.0f},{by:.0f} L{bx + 12:.0f},{by:.0f}" stroke="#fff" stroke-width="{stroke + 3}"/>'
            + text_block(cx, y + 12 + size, lines, size=size + (3 if shout else 0), weight="700", anchor="middle",
                         family=font, lh=1.2))


def burst(cx, cy, r, text="POP!", points=14, fill=YELLOW, size=54, rot=-8) -> str:
    """Spiky explosion star with a sound-effect word."""
    pts = []
    for i in range(points * 2):
        rr = r if i % 2 == 0 else r * 0.62
        a = math.pi * i / points
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return (f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<text x="{cx}" y="{cy + size * 0.35:.0f}" style="{HEAD}" font-size="{size}" text-anchor="middle" '
            f'fill="{RED}" stroke="{INK}" stroke-width="2" transform="rotate({rot} {cx} {cy})">{escape(text)}</text>')


def sunburst(cx, cy, rays=28, c1=YELLOW, c2="#ffe680") -> str:
    out = [f'<rect width="{W}" height="{H}" fill="{c2}"/>']
    R = 1600
    for i in range(rays):
        if i % 2:
            continue
        a0, a1 = 2 * math.pi * i / rays, 2 * math.pi * (i + 1) / rays
        out.append(f'<polygon points="{cx},{cy} {cx + R * math.cos(a0):.0f},{cy + R * math.sin(a0):.0f} '
                   f'{cx + R * math.cos(a1):.0f},{cy + R * math.sin(a1):.0f}" fill="{c1}"/>')
    return "".join(out)


def title(x, y, text, size=120, fill=RED, shadow=YELLOW, anchor="middle", rot=0) -> str:
    t = f' transform="rotate({rot} {x} {y})"' if rot else ""
    common = f'style="{HEAD}" font-size="{size}" text-anchor="{anchor}" letter-spacing="2"'
    return (f'<g{t}><text x="{x + 7}" y="{y + 7}" {common} fill="{INK}">{escape(text)}</text>'
            f'<text x="{x}" y="{y}" {common} fill="{fill}" stroke="{INK}" stroke-width="5" paint-order="stroke">'
            f'{escape(text)}</text></g>')


# ---- the narrators -------------------------------------------------------------------------

def penny(x, y, s=1.0, mood="happy", flip=False) -> str:
    """Penny, an everyday saver. (x, y) = feet centre; about 300 units tall at s=1."""
    skin, hair, top = "#f6c7a1", "#5b3a29", TEAL
    eyes = ('<circle cx="-14" cy="-232" r="5" fill="#1b1b1f"/><circle cx="14" cy="-232" r="5" fill="#1b1b1f"/>'
            if mood != "shock" else
            '<circle cx="-14" cy="-232" r="8" fill="#fff" stroke="#1b1b1f" stroke-width="3"/><circle cx="-14" cy="-232" r="3"/>'
            '<circle cx="14" cy="-232" r="8" fill="#fff" stroke="#1b1b1f" stroke-width="3"/><circle cx="14" cy="-232" r="3"/>')
    mouth = {"happy": '<path d="M-16,-210 Q0,-192 16,-210" fill="#c0392b" stroke="#1b1b1f" stroke-width="3"/>',
             "shock": '<ellipse cx="0" cy="-204" rx="8" ry="11" fill="#7a1f1f" stroke="#1b1b1f" stroke-width="3"/>',
             "think": '<path d="M-10,-206 L12,-209" stroke="#1b1b1f" stroke-width="3.5" stroke-linecap="round"/>'}[mood]
    arms = ('<path d="M-38,-150 Q-75,-190 -62,-238" stroke="#f6c7a1" stroke-width="16" fill="none" stroke-linecap="round"/>'
            '<path d="M38,-150 Q75,-190 62,-238" stroke="#f6c7a1" stroke-width="16" fill="none" stroke-linecap="round"/>'
            if mood == "happy" else
            '<path d="M-38,-150 Q-62,-110 -50,-80" stroke="#f6c7a1" stroke-width="16" fill="none" stroke-linecap="round"/>'
            '<path d="M38,-150 Q62,-110 50,-80" stroke="#f6c7a1" stroke-width="16" fill="none" stroke-linecap="round"/>')
    flipt = " scale(-1,1)" if flip else ""
    return (f'<g transform="translate({x},{y}) scale({s}){flipt}" stroke-linejoin="round">'
            # legs + shoes
            '<rect x="-24" y="-70" width="14" height="66" fill="#3a3a4a"/><rect x="10" y="-70" width="14" height="66" fill="#3a3a4a"/>'
            '<ellipse cx="-19" cy="-4" rx="18" ry="8" fill="#1b1b1f"/><ellipse cx="19" cy="-4" rx="18" ry="8" fill="#1b1b1f"/>'
            f'{arms}'
            # body (t-shirt with @ logo)
            f'<path d="M-42,-160 Q0,-178 42,-160 L48,-66 L-48,-66 Z" fill="{top}" stroke="#1b1b1f" stroke-width="4"/>'
            '<text x="0" y="-100" font-family="Bangers,Impact" font-size="40" text-anchor="middle" fill="#fff">@</text>'
            # neck + head
            f'<rect x="-9" y="-182" width="18" height="18" fill="{skin}"/>'
            f'<circle cx="0" cy="-226" r="46" fill="{skin}" stroke="#1b1b1f" stroke-width="4"/>'
            # hair: fringe + bun
            f'<circle cx="0" cy="-286" r="20" fill="{hair}" stroke="#1b1b1f" stroke-width="4"/>'
            f'<path d="M-46,-226 Q-50,-276 0,-274 Q50,-276 46,-226 Q30,-258 0,-252 Q-28,-258 -46,-226 Z" fill="{hair}" stroke="#1b1b1f" stroke-width="4"/>'
            f'{eyes}<circle cx="-28" cy="-212" r="7" fill="#f29b9b" opacity="0.7"/><circle cx="28" cy="-212" r="7" fill="#f29b9b" opacity="0.7"/>'
            f'{mouth}</g>')


def bear(x, y, s=1.0, mood="calm", flip=False) -> str:
    """Professor Bear, the sceptic. (x, y) = feet centre; about 320 units tall at s=1."""
    fur, muzzle, coat = "#8d5a3b", "#d9b48a", "#6b6f4e"
    brow = ('<path d="M-30,-262 L-10,-256 M30,-262 L10,-256" stroke="#1b1b1f" stroke-width="4" stroke-linecap="round"/>'
            if mood == "stern" else "")
    mouth = ('<path d="M-12,-214 Q0,-206 12,-214" stroke="#1b1b1f" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
             if mood != "stern" else
             '<path d="M-12,-210 L12,-210" stroke="#1b1b1f" stroke-width="3.5" stroke-linecap="round"/>')
    flipt = " scale(-1,1)" if flip else ""
    return (f'<g transform="translate({x},{y}) scale({s}){flipt}" stroke-linejoin="round">'
            f'<rect x="-34" y="-78" width="26" height="74" rx="8" fill="{fur}" stroke="#1b1b1f" stroke-width="4"/>'
            f'<rect x="8" y="-78" width="26" height="74" rx="8" fill="{fur}" stroke="#1b1b1f" stroke-width="4"/>'
            # tweed jacket with pointer arm
            f'<path d="M-56,-176 Q0,-196 56,-176 L62,-70 L-62,-70 Z" fill="{coat}" stroke="#1b1b1f" stroke-width="4"/>'
            '<path d="M0,-186 L-14,-120 L0,-100 L14,-120 Z" fill="#f4efe1" stroke="#1b1b1f" stroke-width="3"/>'
            f'<path d="M56,-168 Q98,-176 118,-214" stroke="{coat}" stroke-width="22" fill="none" stroke-linecap="round"/>'
            f'<circle cx="120" cy="-220" r="13" fill="{fur}" stroke="#1b1b1f" stroke-width="3.5"/>'
            f'<path d="M-56,-168 Q-76,-120 -64,-92" stroke="{coat}" stroke-width="22" fill="none" stroke-linecap="round"/>'
            # bow tie
            '<path d="M0,-184 L-22,-196 L-22,-172 Z M0,-184 L22,-196 L22,-172 Z" fill="#e63b2e" stroke="#1b1b1f" stroke-width="3"/>'
            # head
            f'<circle cx="-42" cy="-282" r="20" fill="{fur}" stroke="#1b1b1f" stroke-width="4"/>'
            f'<circle cx="42" cy="-282" r="20" fill="{fur}" stroke="#1b1b1f" stroke-width="4"/>'
            '<circle cx="-42" cy="-282" r="9" fill="#5c3a26"/><circle cx="42" cy="-282" r="9" fill="#5c3a26"/>'
            f'<circle cx="0" cy="-238" r="52" fill="{fur}" stroke="#1b1b1f" stroke-width="4"/>'
            f'<ellipse cx="0" cy="-218" rx="28" ry="22" fill="{muzzle}" stroke="#1b1b1f" stroke-width="3"/>'
            '<ellipse cx="0" cy="-230" rx="10" ry="7" fill="#1b1b1f"/>'
            # round glasses
            '<circle cx="-20" cy="-250" r="14" fill="#fff" fill-opacity="0.35" stroke="#1b1b1f" stroke-width="3.5"/>'
            '<circle cx="20" cy="-250" r="14" fill="#fff" fill-opacity="0.35" stroke="#1b1b1f" stroke-width="3.5"/>'
            '<path d="M-6,-250 L6,-250" stroke="#1b1b1f" stroke-width="3"/>'
            '<circle cx="-20" cy="-250" r="4" fill="#1b1b1f"/><circle cx="20" cy="-250" r="4" fill="#1b1b1f"/>'
            f'{brow}{mouth}</g>')

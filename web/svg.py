"""Server-side SVG charts. Colours come from CSS classes so light/dark themes work."""
from html import escape

KIND_LABEL = {"early": "warning", "chronic": "long on", "after": "after the peak",
              "old": "earlier episode (not counted)"}


def _scale(v, d0, d1, r0, r1):
    return r0 if d1 == d0 else r0 + (v - d0) * (r1 - r0) / (d1 - d0)


def _cell_label(cell, ref_label):
    """Right-hand text for a timeline row, matching the scoreboard cell."""
    if not cell:
        return "", ""
    st, m = cell["state"], cell["months"]
    if "label" in cell:  # today page: label precomputed from the latest month
        return escape(cell["label"]), "lbl-early" if st == "early" else "lbl-none"
    return {
        "early": (f"{m} mo early", "lbl-early"),
        "chronic": ("long on", "lbl-chronic"),
        "late": (f"late +{m} mo", "lbl-late"),
        "none": ("did not fire", "lbl-none"),
        "na": ("no data", "lbl-none"),
    }[st]


def _month_label(rel, ref_label):
    if rel == 0:
        return ref_label
    return f"{rel:+d} mo"


def timeline_svg(tl: dict, ref_label: str = "peak", width: int = 960) -> str:
    """Warning-light timeline: S&P 500 line on top, one bar row per signal below."""
    left, right, top = 190, 130, 16
    line_h, row_h, gap = 150, 30, 26
    rows = tl["rows"]
    height = top + line_h + gap + row_h * len(rows) + 40
    x0, x1 = tl["x0"], max(tl["x1"], 1)
    X = lambda m: _scale(m, x0, x1, left, width - right)
    out = [f'<svg class="timeline" viewBox="0 0 {width} {height}" role="img" '
           f'aria-label="Warning-light timeline">']

    # recession shading spans line + rows
    for a, b in tl["recessions"]:
        xa, xb = X(max(a, x0)), X(min(b + 1, x1))
        out.append(f'<rect class="recession" x="{xa:.1f}" y="{top}" width="{max(xb - xa, 1):.1f}" '
                   f'height="{height - top - 30}"><title>Recession (NBER)</title></rect>')

    # window shading
    if tl.get("window") is not None and tl["window"] > x0:
        xw = X(tl["window"])
        out.append(f'<rect class="window" x="{xw:.1f}" y="{top + line_h + gap - 6}" width="{X(0) - xw:.1f}" '
                   f'height="{row_h * len(rows) + 6}"><title>Warning window</title></rect>')

    # S&P line
    pts = tl["sp500"]
    if pts:
        vals = [v for _, v in pts]
        lo, hi = min(vals), max(vals)
        pad = (hi - lo) * 0.08 or 1
        Y = lambda v: _scale(v, lo - pad, hi + pad, top + line_h, top)
        path = " ".join(f"{'M' if i == 0 else 'L'}{X(m):.1f},{Y(v):.1f}" for i, (m, v) in enumerate(pts))
        out.append(f'<path class="sp-line" d="{path}"/>')
        out.append(f'<text class="axis-label" x="{left - 10}" y="{top + 14}" text-anchor="end">S&amp;P 500</text>')
        out.append(f'<text class="axis-small" x="{left - 10}" y="{top + 30}" text-anchor="end">monthly average</text>')

    # rows
    for i, row in enumerate(rows):
        y = top + line_h + gap + i * row_h
        out.append(f'<text class="row-label" x="{left - 10}" y="{y + row_h / 2 + 4:.1f}" text-anchor="end">'
                   f'{escape(row["name"])}</text>')
        out.append(f'<rect class="track" x="{left}" y="{y + 6}" width="{width - right - left}" '
                   f'height="{row_h - 12}" rx="{(row_h - 12) / 2}"/>')
        for r in row["runs"]:
            xa, xb = X(r["a"]), X(r["b"] + 1)
            w = max(xb - xa, 3)
            tip = f'{row["name"]}: {KIND_LABEL[r["kind"]]}, {_month_label(r["a"], ref_label)} to {_month_label(r["b"], ref_label)}'
            out.append(f'<rect class="bar bar-{r["kind"]}" x="{xa:.1f}" y="{y + 6}" width="{w:.1f}" '
                       f'height="{row_h - 12}" rx="{(row_h - 12) / 2}"><title>{escape(tip)}</title></rect>')
        text, cls = _cell_label(row.get("cell"), ref_label)
        out.append(f'<text class="cell-label {cls}" x="{width - right + 10}" y="{y + row_h / 2 + 4:.1f}">{text}</text>')

    # reference line (peak / now)
    xp = X(0)
    out.append(f'<line class="peak-line" x1="{xp:.1f}" x2="{xp:.1f}" y1="{top}" y2="{height - 30}"/>')
    out.append(f'<text class="peak-label" x="{xp:.1f}" y="{height - 12}" text-anchor="middle">'
               f'{escape(ref_label)}</text>')

    if tl.get("sahm") is not None:
        xs = X(tl["sahm"])
        out.append(f'<line class="sahm-line" x1="{xs:.1f}" x2="{xs:.1f}" y1="{top}" y2="{height - 30}">'
                   f'<title>Recession confirmed by the Sahm rule</title></line>')
        out.append(f'<text class="sahm-label" x="{xs + 4:.1f}" y="{top + line_h + 12}">recession confirmed</text>')

    # x ticks every 12 months
    for m in range((x0 // 12) * 12, x1 + 1, 12):
        if m < x0 or m == 0:
            continue
        out.append(f'<text class="axis-small" x="{X(m):.1f}" y="{height - 12}" text-anchor="middle">{m:+d} mo</text>')
    out.append("</svg>")
    return "".join(out)


def sparkline_svg(sm: dict, width: int = 300, height: int = 120) -> str:
    """Small chart: metric line, dashed threshold, shaded where the light is ON, peak marker."""
    pts = sm["points"]
    if not pts:
        return '<p class="muted">No data for this period.</p>'
    left, right, top, bottom = 34, 8, 8, 18
    xs = [m for m, _ in pts]
    vals = [v for _, v in pts] + [sm["threshold"]]
    lo, hi = min(vals), max(vals)
    pad = (hi - lo) * 0.1 or 1
    X = lambda m: _scale(m, xs[0], xs[-1], left, width - right)
    Y = lambda v: _scale(v, lo - pad, hi + pad, height - bottom, top)
    ops = {"<": lambda v, t: v < t, "<=": lambda v, t: v <= t, ">": lambda v, t: v > t, ">=": lambda v, t: v >= t}
    is_on = ops[sm["op"]]
    out = [f'<svg class="spark" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(sm["label"])}">']
    for m, v in pts:
        if is_on(v, sm["threshold"]):
            out.append(f'<rect class="spark-on" x="{X(m) - 1:.1f}" y="{top}" width="{max(X(m + 1) - X(m), 2):.1f}" '
                       f'height="{height - top - bottom}"/>')
    ty = Y(sm["threshold"])
    out.append(f'<line class="threshold" x1="{left}" x2="{width - right}" y1="{ty:.1f}" y2="{ty:.1f}"/>')
    out.append(f'<text class="axis-small" x="{left - 4}" y="{ty + 4:.1f}" text-anchor="end">{sm["threshold"]:g}</text>')
    path = " ".join(f"{'M' if i == 0 else 'L'}{X(m):.1f},{Y(v):.1f}" for i, (m, v) in enumerate(pts))
    out.append(f'<path class="spark-line" d="{path}"/>')
    if xs[0] <= 0 <= xs[-1]:
        out.append(f'<line class="peak-line" x1="{X(0):.1f}" x2="{X(0):.1f}" y1="{top}" y2="{height - bottom}"/>')
    out.append(f'<text class="axis-small" x="{left}" y="{height - 4}">{xs[0]:+d} mo</text>')
    out.append(f'<text class="axis-small" x="{width - right}" y="{height - 4}" text-anchor="end">{xs[-1]:+d} mo</text>')
    out.append("</svg>")
    return "".join(out)


_BOARD_STYLE = """
.bg{fill:#ffffff}.t{fill:#111827}.m{fill:#6b7280}
.c-early{fill:#dc2626}.x-early{fill:#ffffff}.c-chronic{fill:#fca5a5}.x-chronic{fill:#7f1d1d}
.c-late{fill:#d1d5db}.x-late{fill:#374151}.c-none{fill:#f3f4f6}.c-na{fill:none;stroke:#d1d5db;stroke-dasharray:3 2}
@media (prefers-color-scheme: dark){
.bg{fill:#0d1117}.t{fill:#e6edf3}.m{fill:#9ca3af}
.c-early{fill:#ef4444}.c-chronic{fill:#7f1d1d}.x-chronic{fill:#fecaca}
.c-late{fill:#374151}.x-late{fill:#d1d5db}.c-none{fill:#1f2937}.c-na{stroke:#374151}}
text{font-family:system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif}
"""


def _wrap2(name: str) -> list:
    """Split a header into two lines of balanced length."""
    words = name.split()
    if len(words) < 2:
        return words
    k = min(range(1, len(words)), key=lambda i: max(len(" ".join(words[:i])), len(" ".join(words[i:]))))
    return [" ".join(words[:k]), " ".join(words[k:])]


def scoreboard_svg(report: dict, cell_text) -> str:
    """Standalone scoreboard image (crises x signals) for the README; own colours, light + dark."""
    signals, crises = report["signals"], report["crises"]
    left, col, gap, count_w = 178, 82, 4, 84
    top, head_h, row_h = 62, 44, 40
    width = left + col * len(signals) + count_w + 12
    rows_y = top + head_h
    legend_y = rows_y + row_h * (len(crises) + 1) + 26
    height = legend_y + 34
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
           f'height="{height}" role="img" aria-label="Warning-light scoreboard">',
           f"<style>{_BOARD_STYLE}</style>",
           f'<rect class="bg" width="{width}" height="{height}" rx="12"/>',
           '<text class="t" x="16" y="30" font-size="19" font-weight="800">'
           'Which warning lights came on before each crash?</text>',
           f'<text class="m" x="16" y="50" font-size="13">S&amp;P 500 fall from peak to bottom; months '
           f'= how early the light switched on before the peak. Data as of {escape(report["generated"])}.</text>']
    for j, s in enumerate(signals):
        cx = left + j * col + col / 2
        lines = _wrap2(s["name"])
        for k, line in enumerate(lines):
            y = rows_y - 8 - (len(lines) - 1 - k) * 15
            out.append(f'<text class="t" x="{cx:.0f}" y="{y}" font-size="12" font-weight="600" '
                       f'text-anchor="middle">{escape(line)}</text>')
    out.append(f'<text class="t" x="{left + col * len(signals) + count_w / 2:.0f}" y="{rows_y - 8}" '
               f'font-size="12" font-weight="600" text-anchor="middle">Warned</text>')
    for i, c in enumerate(crises):
        y = rows_y + i * row_h
        out.append(f'<text class="t" x="16" y="{y + 18}" font-size="14" font-weight="700">{escape(c["short"])}</text>')
        out.append(f'<text class="m" x="16" y="{y + 33}" font-size="12">{c["fall_pct"]}%</text>')
        for j, s in enumerate(signals):
            cell = c["cells"][s["id"]]
            st, x = cell["state"], left + j * col + gap / 2
            out.append(f'<rect class="c-{st}" x="{x}" y="{y + 2}" width="{col - gap}" height="{row_h - 4}" rx="6"/>')
            txt = cell_text(cell)
            if txt:
                cls = {"early": "x-early", "chronic": "x-chronic", "late": "x-late"}.get(st, "m")
                weight = "700" if st in ("early", "chronic") else "500"
                out.append(f'<text class="{cls}" x="{x + (col - gap) / 2:.0f}" y="{y + row_h / 2 + 5:.0f}" '
                           f'font-size="13" font-weight="{weight}" text-anchor="middle">{escape(txt)}</text>')
        out.append(f'<text class="t" x="{left + col * len(signals) + count_w / 2:.0f}" y="{y + row_h / 2 + 5:.0f}" '
                   f'font-size="14" text-anchor="middle"><tspan font-weight="800">{c["early_count"]}</tspan>'
                   f' of {len(signals)}</text>')
    y = rows_y + len(crises) * row_h
    out.append(f'<text class="m" x="16" y="{y + 18}" font-size="12">On in normal times</text>')
    out.append(f'<text class="m" x="16" y="{y + 32}" font-size="11">% of months, 1972–2019</text>')
    for j, s in enumerate(signals):
        out.append(f'<text class="m" x="{left + j * col + col / 2:.0f}" y="{y + 24}" font-size="12" '
                   f'text-anchor="middle">{round(s["false_alarm"])}%</text>')
    x = 16
    for st, label in [("early", "Warned: switched on before the peak"), ("chronic", "Long on: already on for years"),
                      ("late", "Late: fired only after the peak"), ("none", "Did not fire")]:
        out.append(f'<rect class="c-{st}" x="{x}" y="{legend_y}" width="14" height="14" rx="3"/>')
        out.append(f'<text class="m" x="{x + 20}" y="{legend_y + 12}" font-size="12">{label}</text>')
        x += 20 + len(label) * 6.4 + 22
    out.append("</svg>")
    return "".join(out)

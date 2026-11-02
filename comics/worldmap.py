"""World map in the Equal Earth projection, drawn as SVG paths (no GIS libraries needed)."""
import json
import math
from functools import lru_cache
from pathlib import Path

ASSETS = Path(__file__).resolve().parent / "assets"

_A1, _A2, _A3, _A4 = 1.340264, -0.081106, 0.000893, 0.003796
_M = math.sqrt(3) / 2


def equal_earth(lon: float, lat: float) -> tuple:
    """Lon/lat in degrees -> unscaled Equal Earth x, y (y grows north)."""
    lam, phi = math.radians(lon), math.radians(lat)
    th = math.asin(_M * math.sin(phi))
    t2, t6 = th * th, th ** 6
    x = 2 * math.sqrt(3) * lam * math.cos(th) / (3 * (_A1 + 3 * _A2 * t2 + t6 * (7 * _A3 + 9 * _A4 * t2)))
    y = th * (_A1 + _A2 * t2 + t6 * (_A3 + _A4 * t2))
    return x, y


@lru_cache(maxsize=1)
def countries() -> list:
    return json.loads((ASSETS / "world.json").read_text(encoding="utf-8"))["features"]


def _rings(feature):
    polys = [feature["coords"]] if feature["type"] == "Polygon" else feature["coords"]
    for poly in polys:
        for ring in poly:
            yield ring


class Frame:
    """Maps lon/lat into a box (x, y, w, h) on the page, fitted to a lon/lat window."""

    def __init__(self, x, y, w, h, lon=(-170, 190), lat=(-56, 80)):
        pts = [equal_earth(lo, la) for lo in (lon[0], lon[1], (lon[0] + lon[1]) / 2) for la in (lat[0], lat[1], (lat[0] + lat[1]) / 2)]
        self.x0, self.x1 = min(p[0] for p in pts), max(p[0] for p in pts)
        self.y0, self.y1 = min(p[1] for p in pts), max(p[1] for p in pts)
        self.s = min(w / (self.x1 - self.x0), h / (self.y1 - self.y0))
        self.ox = x + (w - (self.x1 - self.x0) * self.s) / 2
        self.oy = y + (h - (self.y1 - self.y0) * self.s) / 2

    def __call__(self, lon, lat):
        px, py = equal_earth(lon, lat)
        return self.ox + (px - self.x0) * self.s, self.oy + (self.y1 - py) * self.s


def country_paths(frame: Frame, style) -> str:
    """One <path> per country; style(a3) -> attribute string (fill, class, ...)."""
    out = []
    for f in countries():
        d = []
        for ring in _rings(f):
            pts = [frame(lon, lat) for lon, lat in ring]
            d.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z")
        out.append(f'<path d="{"".join(d)}" {style(f["a3"])}><title>{f["name"]}</title></path>')
    return "".join(out)

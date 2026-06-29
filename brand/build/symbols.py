import math

from brand.build.tokens import CREAM, GOLD_LIGHT

GOLD = GOLD_LIGHT
# pytest emblem bar tints (light->dark) — the one allowed non-token palette
_BAR_TINTS = ("#e6b14d", "#d99a1f", GOLD, "#9c6c00")


def _ah(tx: float, ty: float, ang: float, sz: float, fill: str = GOLD) -> str:
    """Simple isoceles arrowhead, tip at (tx,ty) pointing toward `ang` (radians)."""
    a1 = ang + math.radians(150)
    a2 = ang - math.radians(150)
    return (
        f'<polygon points="{tx:.1f},{ty:.1f} '
        f"{tx + sz * math.cos(a1):.1f},{ty + sz * math.sin(a1):.1f} "
        f'{tx + sz * math.cos(a2):.1f},{ty + sz * math.sin(a2):.1f}" fill="{fill}"/>'
    )


def _cyl(
    cx: float, cy: float, r: float, h: float = 0.78, w: float = 1.0, fill: str = GOLD
) -> str:
    """Database cylinder centred on (cx,cy)."""
    rx = 0.5 * r * w
    return (
        f'<ellipse cx="{cx}" cy="{cy - h / 2 * r:.1f}" rx="{rx:.1f}" ry="{0.16 * r:.1f}" fill="{fill}"/>'
        f'<rect x="{cx - rx:.1f}" y="{cy - h / 2 * r:.1f}" width="{2 * rx:.1f}" height="{h * r:.1f}" fill="{fill}"/>'
        f'<ellipse cx="{cx}" cy="{cy + h / 2 * r:.1f}" rx="{rx:.1f}" ry="{0.16 * r:.1f}" fill="{fill}"/>'
        f'<ellipse cx="{cx}" cy="{cy - h / 2 * r:.1f}" rx="{rx:.1f}" ry="{0.16 * r:.1f}" '
        f'fill="none" stroke="{CREAM}" stroke-width="0.8"/>'
    )


def _star5(cx: float, cy: float, radius: float, color: str, inner: float = 0.42) -> str:
    """Five-pointed star centred on (cx,cy)."""
    pts: list[tuple[float, float]] = []
    for i in range(5):
        ao = -90 + i * 72
        pts.append(
            (
                cx + radius * math.cos(math.radians(ao)),
                cy + radius * math.sin(math.radians(ao)),
            )
        )
        ai = ao + 36
        pts.append(
            (
                cx + radius * inner * math.cos(math.radians(ai)),
                cy + radius * inner * math.sin(math.radians(ai)),
            )
        )
    body = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{body}" fill="{color}"/>'


def _circ_arc(cx: float, cy: float, rad: float, a0: float, a1: float, w: float) -> str:
    """Clockwise arc a0->a1 (deg, increasing) with a leading arrowhead at a1."""
    a1s = a1 - 7  # stop the stroke short so the head caps it cleanly
    x0 = cx + rad * math.cos(math.radians(a0))
    y0 = cy + rad * math.sin(math.radians(a0))
    x1 = cx + rad * math.cos(math.radians(a1s))
    y1 = cy + rad * math.sin(math.radians(a1s))
    large = 1 if (a1s - a0) % 360 > 180 else 0
    d = (
        f'<path d="M{x0:.1f} {y0:.1f} A {rad:.1f} {rad:.1f} 0 {large} 1 {x1:.1f} {y1:.1f}" '
        f'fill="none" stroke="{GOLD}" stroke-width="{w}" stroke-linecap="butt"/>'
    )
    ex = cx + rad * math.cos(math.radians(a1))
    ey = cy + rad * math.sin(math.radians(a1))
    ang = math.radians(a1 + 90)  # forward (clockwise) tangent
    length = w * 3.0
    width = w * 1.7
    dx, dy = math.cos(ang), math.sin(ang)
    px, py = -dy, dx
    tip = (ex + 0.55 * length * dx, ey + 0.55 * length * dy)
    base = (ex - 0.45 * length * dx, ey - 0.45 * length * dy)
    d += (
        f'<polygon points="{tip[0]:.1f},{tip[1]:.1f} '
        f"{base[0] + width * px:.1f},{base[1] + width * py:.1f} "
        f'{base[0] - width * px:.1f},{base[1] - width * py:.1f}" fill="{GOLD}"/>'
    )
    return d

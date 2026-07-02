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


def _sparkle4(cx: float, cy: float, radius: float, color: str, inner: float = 0.34) -> str:
    """Four-point sparkle (concave star) centred on (cx,cy)."""
    pts: list[tuple[float, float]] = []
    for i in range(4):
        ao = -90 + i * 90
        pts.append(
            (
                cx + radius * math.cos(math.radians(ao)),
                cy + radius * math.sin(math.radians(ao)),
            )
        )
        ai = ao + 45
        pts.append(
            (
                cx + radius * inner * math.cos(math.radians(ai)),
                cy + radius * inner * math.sin(math.radians(ai)),
            )
        )
    body = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{body}" fill="{color}"/>'


def sparkle_cluster(cx: float, cy: float, r: float) -> str:
    """Starlette cue: a large four-point sparkle with a small companion
    (a "little star" — starlette)."""
    big = _sparkle4(cx - 0.174 * r, cy + 0.130 * r, r * 0.82, GOLD)
    small = _sparkle4(cx + 0.565 * r, cy - 0.522 * r, r * 0.36, GOLD)
    return big + small


def _circ_arc(
    cx: float, cy: float, rad: float, a0: float, a1: float, w: float, color: str = GOLD
) -> str:
    """Clockwise arc a0->a1 (deg, increasing) with a leading arrowhead at a1."""
    a1s = a1 - 7  # stop the stroke short so the head caps it cleanly
    x0 = cx + rad * math.cos(math.radians(a0))
    y0 = cy + rad * math.sin(math.radians(a0))
    x1 = cx + rad * math.cos(math.radians(a1s))
    y1 = cy + rad * math.sin(math.radians(a1s))
    large = 1 if (a1s - a0) % 360 > 180 else 0
    d = (
        f'<path d="M{x0:.1f} {y0:.1f} A {rad:.1f} {rad:.1f} 0 {large} 1 {x1:.1f} {y1:.1f}" '
        f'fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="butt"/>'
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
        f'{base[0] - width * px:.1f},{base[1] - width * py:.1f}" fill="{color}"/>'
    )
    return d


def async_loop(cx: float, cy: float, r: float) -> str:
    """aiohttp cue: an async event-loop cycle — two opposed curved arrows
    knocked out of a gold disc."""
    rad = r * 0.52
    w = 3.4
    loop = _circ_arc(cx, cy, rad, 25, 165, w, color=CREAM) + _circ_arc(
        cx, cy, rad, 205, 345, w, color=CREAM
    )
    return f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="{GOLD}"/>' + loop


FASTSTREAM_PATH = (
    "m499.61,356.87l-92.61-160.41-36.48-63.19-10.46,251.02c.07,2.86-.78,6.05-2.51,8.6"
    "-2.98,4.41-7.42,5.31-9.92,2.02l.02-.03-68.85-90.48-107.13,38.09v.04c-3.89,1.38-7.11"
    "-1.8-7.2-7.12-.05-3.08.97-6.22,2.6-8.57L327.1,58.07l-12.71-22.02c-25.95-44.94-90.82"
    "-44.94-116.77,0l-92.61,160.41L12.39,356.87c-25.95,44.94,6.49,101.12,58.38,101.12"
    "h370.45c51.9,0,84.33-56.18,58.38-101.12Z"
)


def bolt_disc(cx: float, cy: float, r: float) -> str:
    """FastAPI cue: lightning bolt knocked out of a gold disc."""
    norm = [
        (0.30, -0.80),
        (-0.42, 0.18),
        (0.05, 0.18),
        (-0.22, 0.82),
        (0.48, -0.22),
        (0.05, -0.22),
    ]
    pts = " ".join(
        f"{cx + dx * r * 0.82:.1f},{cy + dy * r * 0.82:.1f}" for dx, dy in norm
    )
    return f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="{GOLD}"/><polygon points="{pts}" fill="{CREAM}"/>'


def star_disc(cx: float, cy: float, r: float) -> str:
    """Litestar cue: star knocked out of a gold disc."""
    return f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="{GOLD}"/>' + _star5(
        cx, cy, r * 0.72, CREAM
    )


def faststream(cx: float, cy: float, r: float) -> str:
    """FastStream's own delta/stream mark, recoloured gold (sized ~2r tall)."""
    size = r * 2.1
    sc = size / 462.0
    return (
        f'<g transform="translate({cx - 256 * sc:.1f},{cy - 231 * sc:.1f}) scale({sc:.4f})">'
        f'<path d="{FASTSTREAM_PATH}" fill="{GOLD}"/></g>'
    )


def terminal(cx: float, cy: float, r: float) -> str:
    """Typer cue: terminal window showing a bold >T prompt (notched chevron + T),
    drawn as paths so it is font-independent."""
    screen = (
        f'<rect x="{cx - r:.1f}" y="{cy - r * 0.72:.1f}" width="{2 * r:.1f}" '
        f'height="{r * 1.44:.1f}" rx="{r * 0.2:.1f}" fill="{GOLD}"/>'
    )
    # prompt chevron "❯": constant-thickness angle with a back V-notch
    chx = cx - 0.40 * r
    reach, hgt, th = 0.30 * r, 0.34 * r, 0.20 * r
    pts = [
        (chx - reach, cy - hgt),
        (chx - reach + th, cy - hgt),
        (chx + reach, cy - th * 0.15),
        (chx + reach, cy + th * 0.15),
        (chx - reach + th, cy + hgt),
        (chx - reach, cy + hgt),
        (chx - reach + th * 1.7, cy),
    ]
    chevron = (
        '<polygon points="'
        + " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
        + f'" fill="{CREAM}"/>'
    )
    # bold T
    tx = cx + 0.42 * r
    half, hbar, stem, h = 0.32 * r, 0.16 * r, 0.16 * r, 0.62 * r
    tee = (
        f'<rect x="{tx - half:.1f}" y="{cy - 0.34 * r:.1f}" width="{2 * half:.1f}" height="{hbar:.1f}" rx="1.5" fill="{CREAM}"/>'
        f'<rect x="{tx - stem / 2:.1f}" y="{cy - 0.34 * r:.1f}" width="{stem:.1f}" height="{h:.1f}" rx="1.5" fill="{CREAM}"/>'
    )
    return screen + chevron + tee


def bars(cx: float, cy: float, r: float) -> str:
    """pytest cue: stepped bars hanging from a crossbar (gold tints), vertically centred."""
    bw = r * 0.34
    gap = r * 0.22
    x0 = cx - r
    stub = r * 0.18
    cb = r * 0.2
    maxlen = r * 1.0
    total = stub + r * 0.12 + cb + maxlen
    top = cy - total / 2
    y_stub = top
    y_cb = top + stub + r * 0.12
    y_bar = y_cb + cb
    heights = [1.0, 0.78, 0.55, 0.38]
    out = [
        f'<rect x="{x0:.1f}" y="{y_cb:.1f}" width="{2 * r:.1f}" height="{cb:.1f}" rx="{cb / 2:.1f}" fill="{GOLD}"/>'
    ]
    for i in range(4):
        x = x0 + i * (bw + gap)
        out.append(
            f'<rect x="{x:.1f}" y="{y_stub:.1f}" width="{bw:.1f}" height="{stub:.1f}" fill="{_BAR_TINTS[i]}"/>'
        )
        out.append(
            f'<rect x="{x:.1f}" y="{y_bar:.1f}" width="{bw:.1f}" height="{r * heights[i]:.1f}" rx="1" fill="{_BAR_TINTS[i]}"/>'
        )
    return "".join(out)


def chevron(cx: float, cy: float, r: float) -> str:
    """The org chevron (used by templates and as a standalone cue)."""
    return (
        f'<polyline points="{cx - r * 0.45:.1f},{cy - r:.1f} {cx + r * 0.7:.1f},{cy:.1f} '
        f'{cx - r * 0.45:.1f},{cy + r:.1f}" fill="none" stroke="{GOLD}" '
        f'stroke-width="{r * 0.5:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def graph(cx: float, cy: float, r: float, *, dashed: bool) -> str:
    """Dependency graph: 3 nodes + two edges. dashed=auto-wired (modern-di),
    solid=explicit (that-depends)."""
    top = (cx, cy - 0.62 * r)
    bl = (cx - 0.82 * r, cy + 0.6 * r)
    br = (cx + 0.82 * r, cy + 0.6 * r)
    nr = r * 0.24
    w = r * 0.15
    da = ' stroke-dasharray="4 3"' if dashed else ""
    return (
        f'<line x1="{top[0]:.1f}" y1="{top[1]:.1f}" x2="{bl[0]:.1f}" y2="{bl[1]:.1f}" stroke="{GOLD}" stroke-width="{w:.1f}"{da}/>'
        f'<line x1="{top[0]:.1f}" y1="{top[1]:.1f}" x2="{br[0]:.1f}" y2="{br[1]:.1f}" stroke="{GOLD}" stroke-width="{w:.1f}"{da}/>'
        f'<circle cx="{top[0]:.1f}" cy="{top[1]:.1f}" r="{nr:.1f}" fill="{GOLD}"/>'
        f'<circle cx="{bl[0]:.1f}" cy="{bl[1]:.1f}" r="{nr:.1f}" fill="{GOLD}"/>'
        f'<circle cx="{br[0]:.1f}" cy="{br[1]:.1f}" r="{nr:.1f}" fill="{GOLD}"/>'
    )


def rocket(cx: float, cy: float, r: float) -> str:
    """lite-bootstrap: a rocket (launch)."""
    body = (
        f'<path d="M{cx} {cy - r} Q{cx + 0.42 * r} {cy - 0.45 * r} {cx + 0.4 * r} {cy + 0.05 * r} '
        f"L{cx + 0.36 * r} {cy + 0.42 * r} L{cx - 0.36 * r} {cy + 0.42 * r} "
        f'L{cx - 0.4 * r} {cy + 0.05 * r} Q{cx - 0.42 * r} {cy - 0.45 * r} {cx} {cy - r} Z" fill="{GOLD}"/>'
    )
    fins = (
        f'<polygon points="{cx - 0.36 * r:.1f},{cy + 0.12 * r:.1f} {cx - 0.72 * r:.1f},{cy + 0.5 * r:.1f} {cx - 0.36 * r:.1f},{cy + 0.42 * r:.1f}" fill="{GOLD}"/>'
        f'<polygon points="{cx + 0.36 * r:.1f},{cy + 0.12 * r:.1f} {cx + 0.72 * r:.1f},{cy + 0.5 * r:.1f} {cx + 0.36 * r:.1f},{cy + 0.42 * r:.1f}" fill="{GOLD}"/>'
    )
    window = f'<circle cx="{cx}" cy="{cy - 0.28 * r:.1f}" r="{0.16 * r:.1f}" fill="{CREAM}"/>'
    flame = f'<polygon points="{cx - 0.18 * r:.1f},{cy + 0.42 * r:.1f} {cx + 0.18 * r:.1f},{cy + 0.42 * r:.1f} {cx:.1f},{cy + 0.8 * r:.1f}" fill="{GOLD}"/>'
    return body + fins + window + flame


def chain(cx: float, cy: float, r: float) -> str:
    """httpware: two interlocked chain links (middleware chain)."""
    sw = r * 0.2
    return (
        f'<rect x="{cx - 0.85 * r:.1f}" y="{cy - 0.3 * r:.1f}" width="{0.9 * r:.1f}" height="{0.6 * r:.1f}" rx="{0.3 * r:.1f}" fill="none" stroke="{GOLD}" stroke-width="{sw:.1f}"/>'
        f'<rect x="{cx - 0.05 * r:.1f}" y="{cy - 0.3 * r:.1f}" width="{0.9 * r:.1f}" height="{0.6 * r:.1f}" rx="{0.3 * r:.1f}" fill="none" stroke="{GOLD}" stroke-width="{sw:.1f}"/>'
    )


def stopwatch(cx: float, cy: float, r: float) -> str:
    """faststream-redis-timers: a stopwatch."""
    c = cy + 0.07 * r
    rr = r * 0.92
    face = (
        f'<circle cx="{cx}" cy="{c:.1f}" r="{0.9 * rr:.1f}" fill="none" stroke="{GOLD}" stroke-width="{rr * 0.16:.1f}"/>'
        f'<line x1="{cx}" y1="{c:.1f}" x2="{cx}" y2="{c - 0.55 * rr:.1f}" stroke="{GOLD}" stroke-width="{rr * 0.15:.1f}" stroke-linecap="round"/>'
        f'<line x1="{cx}" y1="{c:.1f}" x2="{cx + 0.42 * rr:.1f}" y2="{c + 0.18 * rr:.1f}" stroke="{GOLD}" stroke-width="{rr * 0.15:.1f}" stroke-linecap="round"/>'
    )
    btn = (
        f'<rect x="{cx - 0.13 * r:.1f}" y="{cy - 1.18 * r:.1f}" width="{0.26 * r:.1f}" height="{0.2 * r:.1f}" rx="2" fill="{GOLD}"/>'
        f'<line x1="{cx}" y1="{cy - 1.0 * r:.1f}" x2="{cx}" y2="{cy - 0.85 * r:.1f}" stroke="{GOLD}" stroke-width="{r * 0.14:.1f}"/>'
    )
    return face + btn


def lanes(cx: float, cy: float, r: float, length: float = 1.7) -> str:
    """faststream-concurrent-aiokafka: three staggered parallel arrows (middle longest)."""
    out = ""
    for i, dy in enumerate((-0.55 * r, 0.0, 0.55 * r)):
        ln = length * r * (0.72 if i != 1 else 1.0)
        x1 = cx - length * r / 2
        x2 = x1 + ln
        out += (
            f'<line x1="{x1:.1f}" y1="{cy + dy:.1f}" x2="{x2 - 0.18 * r:.1f}" y2="{cy + dy:.1f}" '
            f'stroke="{GOLD}" stroke-width="{r * 0.15:.1f}" stroke-linecap="round"/>'
        )
        out += _ah(x2, cy + dy, 0.0, r * 0.3)
    return out


def outbox(cx: float, cy: float, r: float) -> str:
    """faststream-outbox: a database cylinder publishing concentric broadcast arcs."""
    base = _cyl(cx - 0.28 * r, cy + 0.28 * r, r * 0.72, 0.72)
    bx, by = cx, cy - 0.02 * r
    out = f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{0.13 * r:.1f}" fill="{GOLD}"/>'
    for k in (0.5, 0.82, 1.14):
        kk = k * r * 0.72
        out += (
            f'<path d="M{bx + kk:.1f} {by:.1f} A {kk:.1f} {kk:.1f} 0 0 0 {bx:.1f} {by - kk:.1f}" '
            f'fill="none" stroke="{GOLD}" stroke-width="{r * 0.72 * 0.14:.1f}"/>'
        )
    return base + out


def db_retry(cx: float, cy: float, r: float) -> str:
    """db-retry: a database cylinder inside a two-head clockwise retry circle."""
    rad = 0.92 * r
    return (
        _cyl(cx, cy, r * 0.6)
        + _circ_arc(cx, cy, rad, 285, 425, 4.5)
        + _circ_arc(cx, cy, rad, 105, 245, 4.5)
    )


def eof_fixer(cx: float, cy: float, r: float) -> str:
    """eof-fixer: a document with a newline-return (down-then-left) arrow."""
    doc = (
        f'<rect x="{cx - 0.6 * r:.1f}" y="{cy - 0.8 * r:.1f}" width="{1.2 * r:.1f}" height="{1.6 * r:.1f}" '
        f'rx="3" fill="none" stroke="{GOLD}" stroke-width="{r * 0.12:.1f}"/>'
    )
    for i in range(3):
        doc += (
            f'<line x1="{cx - 0.4 * r:.1f}" y1="{cy - 0.5 * r + i * 0.32 * r:.1f}" '
            f'x2="{cx + 0.4 * r:.1f}" y2="{cy - 0.5 * r + i * 0.32 * r:.1f}" stroke="{GOLD}" stroke-width="{r * 0.1:.1f}"/>'
        )
    doc += (
        f'<line x1="{cx - 0.2 * r:.1f}" y1="{cy + 0.55 * r:.1f}" x2="{cx + 0.45 * r:.1f}" y2="{cy + 0.55 * r:.1f}" '
        f'stroke="{GOLD}" stroke-width="{r * 0.1:.1f}"/>'
    )
    doc += _ah(cx - 0.2 * r, cy + 0.55 * r, math.pi, r * 0.24)
    return doc


def tag(cx: float, cy: float, r: float) -> str:
    """semvertag: a price/version tag with a punch-hole, vertically centred."""
    return (
        f'<path d="M{cx - 0.2 * r:.1f} {cy - 0.48 * r:.1f} L{cx + 0.75 * r:.1f} {cy - 0.48 * r:.1f} '
        f"L{cx + 0.75 * r:.1f} {cy + 0.48 * r:.1f} L{cx - 0.2 * r:.1f} {cy + 0.48 * r:.1f} "
        f'L{cx - 0.75 * r:.1f} {cy:.1f} Z" fill="{GOLD}"/>'
        f'<circle cx="{cx - 0.28 * r:.1f}" cy="{cy:.1f}" r="{0.13 * r:.1f}" fill="{CREAM}"/>'
    )

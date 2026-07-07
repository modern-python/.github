from brand.build.text import outline_text

_SVG_OPEN = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Modern Python">'


def _icon_mark(struct: str, gold: str) -> str:
    """The two border-reaching snakes (block head + diagonal-cut tail) + chevron.
    Tail polygon bases overlap the stroke by 2px to avoid a seam."""
    return (
        f'<path d="M15 68 L15 15 L68 15" fill="none" stroke="{struct}" stroke-width="11" stroke-linecap="butt" stroke-linejoin="miter"/>'
        f'<rect x="61" y="8" width="14" height="14" rx="2" fill="{struct}"/>'
        f'<polygon points="9.5,66 20.5,66 20.5,68 9.5,79" fill="{struct}"/>'
        f'<path d="M85 32 L85 85 L32 85" fill="none" stroke="{gold}" stroke-width="11" stroke-linecap="butt" stroke-linejoin="miter"/>'
        f'<rect x="25" y="78" width="14" height="14" rx="2" fill="{gold}"/>'
        f'<polygon points="90.5,34 79.5,34 79.5,32 90.5,21" fill="{gold}"/>'
        f'<polyline points="45,40 57,50 45,60" fill="none" stroke="{gold}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def icon(*, bg: str, struct: str, gold: str) -> str:
    """Full-bleed square icon — favicon, apple-touch, GitHub avatar."""
    return (
        _SVG_OPEN.format(w=100, h=100)
        + f'<rect width="100" height="100" fill="{bg}"/>'
        + _icon_mark(struct, gold)
        + "</svg>"
    )


def icon_circle(*, bg: str, struct: str, gold: str, scale: float = 0.74) -> str:
    """Padded variant centered for circular crops (e.g. Telegram). The mark is
    scaled about the center so it fits inside the inscribed circle with margin."""
    return (
        _SVG_OPEN.format(w=100, h=100)
        + f'<rect width="100" height="100" fill="{bg}"/>'
        + f'<g transform="translate(50,50) scale({scale}) translate(-50,-50)">{_icon_mark(struct, gold)}</g>'
        + "</svg>"
    )


def lockup_body(*, struct: str, gold: str) -> str:
    """The MODERN/PYTHON crop-mark lockup, drawn in a 540x250 coordinate space.
    Returned as bare markup (no <svg> wrapper, no background) for embedding."""
    modern, _ = outline_text(
        "MODERN",
        50,
        x=270,
        baseline_y=126,
        anchor="middle",
        color=struct,
        fit_width=210,
    )
    python, _ = outline_text(
        "PYTHON", 50, x=270, baseline_y=166, anchor="middle", color=gold, fit_width=210
    )
    crops = (
        '<g fill="none" stroke-width="8" stroke-linecap="butt" stroke-linejoin="miter">'
        f'<path d="M138 122 L138 50 L210 50" stroke="{struct}"/>'
        f'<path d="M402 128 L402 200 L330 200" stroke="{gold}"/></g>'
        f'<rect x="202.5" y="42.5" width="15" height="15" rx="3" fill="{struct}"/>'
        f'<rect x="322.5" y="192.5" width="15" height="15" rx="3" fill="{gold}"/>'
        f'<polygon points="134,120 142,120 142,122 134,130" fill="{struct}"/>'
        f'<polygon points="406,130 398,130 398,128 406,120" fill="{gold}"/>'
    )
    return crops + modern + python


def wordmark(*, struct: str, gold: str) -> str:
    """Standalone two-color MODERN/PYTHON wordmark for the site hero. Wraps
    `lockup_body` (drawn in a 540x250 space) in a tight viewBox centered on the
    content, with no background — transparent so it sits on any page surface."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="118 32 304 184" '
        'role="img" aria-label="Modern Python">'
        + lockup_body(struct=struct, gold=gold)
        + "</svg>"
    )


def mark(*, struct: str, gold: str) -> str:
    """The chevron mark on its own (no background) for the site header logo —
    same glyph as `icon`, minus the full-bleed background rect."""
    return _SVG_OPEN.format(w=100, h=100) + _icon_mark(struct, gold) + "</svg>"


def apparel_back(*, struct: str, gold: str) -> str:
    """Back-of-shirt lockup: the MODERN/PYTHON wordmark with the full domain
    outlined beneath it, transparent, for the cream+gold-dark colorway. Extends
    the `wordmark` viewBox downward to seat the URL centered on the same axis."""
    url, _ = outline_text(
        "modern-python.org",
        18,
        x=270,
        baseline_y=240,
        anchor="middle",
        color=gold,
        letter_spacing=3,
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="118 32 304 228" '
        'role="img" aria-label="Modern Python, modern-python.org">'
        + lockup_body(struct=struct, gold=gold)
        + url
        + "</svg>"
    )


def social_card(*, bg: str, struct: str, gold: str, url_color: str) -> str:
    body = lockup_body(struct=struct, gold=gold)
    url, _ = outline_text(
        "modern-python.org",
        34,
        x=640,
        baseline_y=575,
        anchor="middle",
        color=url_color,
        letter_spacing=4,
    )
    return (
        _SVG_OPEN.format(w=1280, h=640)
        + f'<rect width="1280" height="640" fill="{bg}"/>'
        + f'<g transform="translate(235,108) scale(1.5)">{body}</g>'
        + url
        + "</svg>"
    )


def social_square(*, bg: str, struct: str, gold: str) -> str:
    body = lockup_body(struct=struct, gold=gold)
    s = 1.9
    tx = round(320 - 270 * s, 1)  # box-center horizontally (lockup box is 540 wide)
    ty = round(320 - 125 * s, 1)  # box-center vertically (lockup box is 250 tall)
    return (
        _SVG_OPEN.format(w=640, h=640)
        + f'<rect width="640" height="640" fill="{bg}"/>'
        + f'<g transform="translate({tx},{ty}) scale({s})">{body}</g>'
        + "</svg>"
    )


def boosty_cover(*, bg: str, struct: str, gold: str) -> str:
    """Boosty profile-header banner — 8:1 (1920x240), Boosty's documented header
    size. The strip is too shallow to stack, so the MODERN/PYTHON lockup and the
    outlined tagline sit side by side, centered as a pair on a full-bleed
    background. The tagline width is measured to center the whole row."""
    w, h = 1920, 240
    s = 0.9  # lockup scale; its visual box is x[134,406] (width 272), y-center 125
    lock_w = 272 * s
    tagline_text = "Open-source Python for production"
    tag_size = 40
    gap = 60  # px between lockup and tagline
    _, tag_w = outline_text(
        tagline_text,
        tag_size,
        x=0,
        baseline_y=0,
        anchor="start",
        color=gold,
        letter_spacing=4,
    )
    x0 = (w - (lock_w + gap + tag_w)) / 2  # left edge of the centered row
    tx = round(x0 - 134 * s, 1)  # seat the lockup's visual-left at x0
    ty = round(h / 2 - 125 * s, 1)  # center the lockup vertically
    body = lockup_body(struct=struct, gold=gold)
    tagline, _ = outline_text(
        tagline_text,
        tag_size,
        x=round(x0 + lock_w + gap, 1),
        baseline_y=round(h / 2 + tag_size * 0.32, 1),  # optical vertical center
        anchor="start",
        color=gold,
        letter_spacing=4,
    )
    return (
        _SVG_OPEN.format(w=w, h=h)
        + f'<rect width="{w}" height="{h}" fill="{bg}"/>'
        + f'<g transform="translate({tx},{ty}) scale({s})">{body}</g>'
        + tagline
        + "</svg>"
    )


def project_frame(
    *,
    struct: str,
    accent: str,
    w: int = 100,
    h: int = 100,
    m: int = 9,
    lx: int = 53,
    ly: int = 53,
    s: int = 11,
) -> str:
    """Two pinwheeled L-snakes in opposite corners — the constant project frame.
    Returns bare markup (no <svg> wrapper)."""
    hs = s + 3
    parts = [
        f'<path d="M{m} {m + ly} L{m} {m} L{m + lx} {m}" fill="none" stroke="{struct}" stroke-width="{s}" stroke-linejoin="miter"/>',
        f'<rect x="{m + lx - hs / 2:.1f}" y="{m - hs / 2:.1f}" width="{hs}" height="{hs}" rx="2" fill="{struct}"/>',
        f'<polygon points="{m - s / 2:.1f},{m + ly - 2:.1f} {m + s / 2:.1f},{m + ly - 2:.1f} {m + s / 2:.1f},{m + ly:.1f} {m - s / 2:.1f},{m + ly + s:.1f}" fill="{struct}"/>',
        f'<path d="M{w - m} {h - m - ly} L{w - m} {h - m} L{w - m - lx} {h - m}" fill="none" stroke="{accent}" stroke-width="{s}" stroke-linejoin="miter"/>',
        f'<rect x="{w - m - lx - hs / 2:.1f}" y="{h - m - hs / 2:.1f}" width="{hs}" height="{hs}" rx="2" fill="{accent}"/>',
        f'<polygon points="{w - m + s / 2:.1f},{h - m - ly + 2:.1f} {w - m - s / 2:.1f},{h - m - ly + 2:.1f} {w - m - s / 2:.1f},{h - m - ly:.1f} {w - m + s / 2:.1f},{h - m - ly - s:.1f}" fill="{accent}"/>',
    ]
    return "".join(parts)

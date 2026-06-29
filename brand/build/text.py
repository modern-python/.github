from functools import lru_cache
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

_FONTS = Path(__file__).parent / "fonts"
JOST = _FONTS / "Jost-Regular.ttf"


@lru_cache(maxsize=4)
def _font(path: Path) -> TTFont:
    return TTFont(path)


def _upm(path: Path) -> int:
    return _font(path)["head"].unitsPerEm  # ty: ignore[unresolved-attribute]


def outline_text(
    text: str,
    size: float,
    *,
    x: float,
    baseline_y: float,
    anchor: str = "start",
    color: str = "#000000",
    fit_width: float | None = None,
    letter_spacing: float = 0.0,
    font_path: Path = JOST,
) -> tuple[str, float]:
    """Outline `text` to SVG <path>s. Returns (group_svg, rendered_width).

    fit_width pins the rendered width (like SVG textLength): glyphs+spacing are
    scaled horizontally to exactly fit_width. letter_spacing is extra px between
    glyphs. anchor="middle" centers on x.
    """
    f = _font(font_path)
    glyphset = f.getGlyphSet()
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    upm = _upm(font_path)
    s = size / upm
    assert cmap is not None, "font has no Unicode cmap"

    ls_units = letter_spacing / s if s else 0.0
    parts: list[str] = []
    cursor = 0.0
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            raise ValueError(
                f"character {ch!r} (U+{ord(ch):04X}) not in {font_path.name} cmap"
            )
        pen = SVGPathPen(glyphset)
        glyphset[gname].draw(pen)
        d = pen.getCommands()
        if d:
            parts.append(f'<path d="{d}" transform="translate({cursor:.2f},0)"/>')
        cursor += hmtx[gname][0] + ls_units
    cursor -= ls_units  # drop trailing letter-spacing

    natural = cursor * s
    sx = s * (fit_width / natural) if (fit_width and natural) else s
    eff = fit_width if fit_width else natural
    ox = x - eff / 2 if anchor == "middle" else x
    g = (
        f'<g fill="{color}" transform="translate({ox:.3f},{baseline_y:.3f}) '
        f'scale({sx:.6f},{-s:.6f})">{"".join(parts)}</g>'
    )
    return g, eff

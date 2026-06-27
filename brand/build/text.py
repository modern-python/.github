from pathlib import Path
from functools import lru_cache
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

_FONT_PATH = Path(__file__).parent / "fonts" / "JetBrainsMono-SemiBold.ttf"


@lru_cache(maxsize=1)
def _font() -> TTFont:
    return TTFont(_FONT_PATH)


def _upm() -> int:
    return _font()["head"].unitsPerEm


def cap_height_scaled(size: float) -> float:
    f = _font()
    cap = getattr(f["OS/2"], "sCapHeight", 0) or int(0.7 * _upm())
    return cap * size / _upm()


def outline_text(
    text: str,
    size: float,
    *,
    x: float,
    baseline_y: float,
    anchor: str = "start",
    color: str = "#000000",
) -> tuple[str, float]:
    f = _font()
    glyphset = f.getGlyphSet()
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    upm = _upm()
    s = size / upm

    parts: list[str] = []
    cursor: int = 0
    for ch in text:
        gname = cmap[ord(ch)]
        pen = SVGPathPen(glyphset)
        glyphset[gname].draw(pen)
        d = pen.getCommands()
        if d:
            parts.append(f'<path d="{d}" transform="translate({cursor},0)"/>')
        cursor += hmtx[gname][0]

    width = cursor * s
    ox = x - width / 2 if anchor == "middle" else x
    inner = "".join(parts)
    # font units are y-up; scale(s,-s) flips to SVG y-down, baseline at baseline_y
    g = (
        f'<g fill="{color}" transform="translate({ox:.3f},{baseline_y:.3f}) '
        f'scale({s:.5f},{-s:.5f})">{inner}</g>'
    )
    return g, width

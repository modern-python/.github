"""Generate a transparent, vector SVG wordmark for Modern Python.

Extracts the "MODERN PYTHON" glyph outlines from Futura (present on macOS) as
real vector paths — no font dependency at render time — and frames them with the
brand's corner brackets. Fill is `currentColor` so the same file can be tinted
per theme (green on light surfaces, white on the green header) via CSS/attr.

Run locally:

    uv run --with fonttools python scripts/gen_logo_svg.py

Outputs:
    docs/assets/modern-python.svg        (two-line wordmark + brackets)
    docs/assets/modern-python-mark.svg   (compact bracket mark, for the favicon)
"""

import pathlib

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

FONT_PATH = "/System/Library/Fonts/Supplemental/Futura.ttc"
FONT_NUMBER = 0  # Futura Medium
ASSETS = pathlib.Path(__file__).resolve().parent.parent / "docs" / "assets"

LINES = ["MODERN", "PYTHON"]
TRACKING = 0.10  # fraction of em added between glyphs
LINE_GAP = 0.18  # fraction of em between the two lines
PAD = 0.34       # padding (em) inside the bracket frame
BRACKET = 0.55   # bracket arm length (em)
STROKE = 0.07    # bracket stroke width (em)


def layout_line(font, glyph_set, cmap, text, upm):
    """Return (svg_paths, width_em) for one tracked line, baseline at y=0, y-up."""
    paths, x = [], 0.0
    track = TRACKING * upm
    for ch in text:
        gname = cmap[ord(ch)]
        pen = SVGPathPen(glyph_set)
        glyph_set[gname].draw(pen)
        d = pen.getCommands()
        if d:
            paths.append(f'<path transform="translate({x:.1f},0)" d="{d}"/>')
        x += glyph_set[gname].width + track
    return paths, (x - track) / upm  # drop trailing track


def main() -> None:
    font = TTFont(FONT_PATH, fontNumber=FONT_NUMBER)
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font["head"].unitsPerEm
    cap = font["OS/2"].sCapHeight if hasattr(font["OS/2"], "sCapHeight") else int(0.7 * upm)
    cap_em = cap / upm

    # Lay out each line; track widest for centering.
    laid = [layout_line(font, glyph_set, cmap, line, upm) for line in LINES]
    text_w = max(w for _, w in laid)

    line_h = cap_em + LINE_GAP
    text_h = line_h * len(LINES) - LINE_GAP

    # Frame geometry (em units, y-down in final SVG).
    frame_w = text_w + 2 * PAD
    frame_h = text_h + 2 * PAD
    vb_w = frame_w
    vb_h = frame_h

    groups = []
    # Each line: flip y-up glyphs into y-down SVG space and position.
    for i, (paths, w) in enumerate(laid):
        if not paths:
            continue
        x0 = (frame_w - w) / 2 * upm
        baseline = (PAD + cap_em + i * line_h) * upm  # y of baseline in y-down em*upm
        # translate to (x0, baseline) then scale(1,-1) maps glyph y-up to y-down.
        groups.append(
            f'<g transform="scale({1/upm:.6f}) translate({x0:.1f},{baseline:.1f}) '
            f'scale(1,-1)">{"".join(paths)}</g>'
        )

    # Corner brackets: top-left and bottom-right, stroked (no fill).
    sw, arm = STROKE, BRACKET

    def wordmark(color: str) -> str:
        tl = (
            f'<path fill="none" stroke="{color}" stroke-width="{sw}" '
            f'd="M {sw/2:.3f} {arm:.3f} L {sw/2:.3f} {sw/2:.3f} L {arm:.3f} {sw/2:.3f}"/>'
        )
        br = (
            f'<path fill="none" stroke="{color}" stroke-width="{sw}" '
            f'd="M {frame_w-sw/2:.3f} {frame_h-arm:.3f} L {frame_w-sw/2:.3f} {frame_h-sw/2:.3f} '
            f'L {frame_w-arm:.3f} {frame_h-sw/2:.3f}"/>'
        )
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w:.3f} {vb_h:.3f}" '
            f'fill="{color}" role="img" aria-label="Modern Python">'
            f'{"".join(groups)}{tl}{br}</svg>\n'
        )

    # currentColor variant — inlined in the homepage hero, themed via CSS.
    (ASSETS / "modern-python.svg").write_text(wordmark("currentColor"))
    # White variant — used as the header logo (the header sits on brand green).
    (ASSETS / "modern-python-white.svg").write_text(wordmark("#ffffff"))
    print(f"wrote modern-python.svg + modern-python-white.svg (viewBox 0 0 {vb_w:.2f} {vb_h:.2f})")

    # Compact favicon mark: the two corner brackets only, in a tight square.
    # Adapts to the browser/OS theme: brand green on light tabs, white on dark.
    m_sw, m_arm = 0.12, 0.62
    paths = (
        f'<path d="M {m_sw/2:.3f} {m_arm:.3f} L {m_sw/2:.3f} {m_sw/2:.3f} L {m_arm:.3f} {m_sw/2:.3f}"/>'
        f'<path d="M {1-m_sw/2:.3f} {1-m_arm:.3f} L {1-m_sw/2:.3f} {1-m_sw/2:.3f} '
        f'L {1-m_arm:.3f} {1-m_sw/2:.3f}"/>'
    )
    style = (
        "<style>:root{--mp:#356852}"
        "@media(prefers-color-scheme:dark){:root{--mp:#ffffff}}</style>"
    )
    mark = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1" '
        f'fill="none" stroke="var(--mp)" stroke-width="{m_sw}" '
        f'stroke-linecap="square" role="img" aria-label="Modern Python">'
        f'{style}{paths}</svg>\n'
    )
    (ASSETS / "modern-python-mark.svg").write_text(mark)
    print("wrote modern-python-mark.svg")


if __name__ == "__main__":
    main()

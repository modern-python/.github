import shutil
from pathlib import Path

import pytest

from brand.build.raster import export_png

pytestmark = pytest.mark.skipif(
    shutil.which("rsvg-convert") is None, reason="rsvg-convert not installed"
)

_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10" fill="{fill}"/></svg>'


def _write_svg(path: Path, fill: str = "#c98a00") -> Path:
    path.write_text(_SVG.format(fill=fill), encoding="utf-8")
    return path


def test_unchanged_source_leaves_png_untouched(tmp_path: Path) -> None:
    """INVARIANT: re-rendering an unchanged SVG does not rewrite its PNG.

    rsvg-convert builds differ byte-wise from machine to machine, so a render that
    always rewrites turns every brand PR into a diff of every committed PNG.
    """
    svg = _write_svg(tmp_path / "a.svg")
    png = tmp_path / "a.png"
    assert export_png(svg, png, width=32, height=32)
    before = png.read_bytes()
    stamp = png.stat().st_mtime_ns

    assert export_png(svg, png, width=32, height=32)
    assert png.stat().st_mtime_ns == stamp
    assert png.read_bytes() == before


def test_changed_svg_rerenders(tmp_path: Path) -> None:
    svg = _write_svg(tmp_path / "a.svg")
    png = tmp_path / "a.png"
    assert export_png(svg, png, width=32, height=32)
    before = png.read_bytes()

    _write_svg(svg, fill="#1f4d3a")
    assert export_png(svg, png, width=32, height=32)
    assert png.read_bytes() != before


def test_changed_size_rerenders(tmp_path: Path) -> None:
    svg = _write_svg(tmp_path / "a.svg")
    png = tmp_path / "a.png"
    assert export_png(svg, png, width=32, height=32)
    before = png.read_bytes()

    assert export_png(svg, png, width=64, height=64)
    assert png.read_bytes() != before

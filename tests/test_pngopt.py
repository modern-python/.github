import shutil
from pathlib import Path

import pytest
from PIL import Image

from brand.build import projects as p

pytestmark = pytest.mark.skipif(
    shutil.which("rsvg-convert") is None, reason="rsvg-convert not installed"
)


def _render(tmp: Path) -> None:
    p.render_projects(out_dir=tmp)


def test_social_card_png_is_quantized_and_small(tmp_path: Path) -> None:
    _render(tmp_path)
    card = tmp_path / "modern-di" / "social-card.png"
    im = Image.open(card)
    assert im.mode == "P", f"expected indexed palette, got {im.mode}"
    assert im.size == (1280, 640)
    assert card.stat().st_size < 20_000, card.stat().st_size


def test_transparent_mark_png_keeps_alpha_and_is_small(tmp_path: Path) -> None:
    """INVARIANT: palette quantization preserves the transparent marks' alpha.

    Every generated PNG is indexed-colour so the committed binaries stay small, and a
    quantizer chosen for the opaque social cards can flatten alpha to a matte without
    erroring — the mark then ships with a white box behind it on every dark surface.
    """
    _render(tmp_path)
    mark = tmp_path / "modern-di" / "mark-1024.png"
    im = Image.open(mark)
    assert im.mode == "P", f"expected indexed palette, got {im.mode}"
    assert im.size == (1024, 1024)
    assert "transparency" in im.info, "transparent mark lost its alpha"
    assert mark.stat().st_size < 15_000, mark.stat().st_size


def test_card_palette_is_actually_reduced(tmp_path: Path) -> None:
    _render(tmp_path)
    card = tmp_path / "modern-di" / "social-card.png"
    colors = Image.open(card).convert("RGBA").getcolors(maxcolors=100_000)
    assert colors is not None and len(colors) <= 40, (
        f"card should be palette-reduced; found {None if colors is None else len(colors)} colours"
    )

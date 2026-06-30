import re

from brand.build import tokens


def test_palette_values():
    assert tokens.GREEN_INK == "#356852"
    assert tokens.GREEN_SURFACE == "#2f5e4a"
    assert tokens.GOLD_LIGHT == "#c98a00"
    assert tokens.GOLD_DARK == "#f0b528"
    assert tokens.CREAM == "#f4f1e8"


def test_all_tokens_are_hex():
    hexre = re.compile(r"^#[0-9a-f]{6}$")
    for name in ("GREEN_INK", "GREEN_SURFACE", "GOLD_LIGHT", "GOLD_DARK", "CREAM"):
        assert hexre.match(getattr(tokens, name)), name


def test_green_muted_present() -> None:
    assert tokens.GREEN_MUTED == "#5b6f63"

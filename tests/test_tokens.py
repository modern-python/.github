from brand.build import tokens


def test_palette_values():
    assert tokens.GREEN == "#356852"
    assert tokens.GOLD == "#c98a00"
    assert tokens.GREEN_DARK == "#3f8064"
    assert tokens.GOLD_DARK == "#e0a300"
    assert tokens.TEAL == "#2a9d8f"
    assert tokens.AMBER == "#c2722b"


def test_framework_has_fastapi():
    assert "fastapi" in tokens.FRAMEWORK
    assert tokens.FRAMEWORK["fastapi"].startswith("#")

from brand.build.text import outline_text, cap_height_scaled


def test_outline_returns_group_and_width(parse_svg):
    g, width = outline_text("di", 30, x=50, baseline_y=58, anchor="middle", color="#c98a00")
    el = parse_svg(g)
    assert el.tag.endswith("g")
    assert el.attrib["fill"] == "#c98a00"
    assert width > 0
    # at least one outlined glyph path with real data
    paths = [c for c in el if c.tag.endswith("path")]
    assert paths and paths[0].attrib["d"].startswith("M")


def test_monospace_width_scales_with_length():
    _, w2 = outline_text("di", 30, x=0, baseline_y=0)
    _, w3 = outline_text("did", 30, x=0, baseline_y=0)
    assert round(w3 / w2, 2) == round(3 / 2, 2)  # uniform advance


def test_cap_height_positive():
    assert cap_height_scaled(30) > 0

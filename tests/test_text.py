from brand.build.text import outline_text


def test_outline_returns_group_and_paths(parse_svg):
    g, width = outline_text("MODERN", 50, x=270, baseline_y=126,
                            anchor="middle", color="#356852")
    el = parse_svg(g)
    assert el.tag.endswith("g")
    assert el.attrib["fill"] == "#356852"
    assert width > 0
    paths = [c for c in el if c.tag.endswith("path")]
    assert paths and paths[0].attrib["d"].startswith("M")


def test_width_grows_with_length():
    _, w2 = outline_text("MO", 50, x=0, baseline_y=0)
    _, w4 = outline_text("MODE", 50, x=0, baseline_y=0)
    assert w4 > w2


def test_fit_width_pins_rendered_width():
    _, w = outline_text("MODERN", 50, x=270, baseline_y=126,
                        anchor="middle", fit_width=210)
    assert abs(w - 210.0) < 1e-6



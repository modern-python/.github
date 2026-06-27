from brand.build import geometry as g


def test_org_icon_structure(parse_svg):
    el = parse_svg(g.org_icon())
    assert el.attrib["viewBox"] == "0 0 100 100"
    assert el.attrib["role"] == "img"
    assert "Modern Python" in el.attrib["aria-label"]
    svg = g.org_icon()
    assert g.OUTER_SNAKE in svg and g.MIDDLE_SNAKE in svg
    assert "prefers-color-scheme: dark" in svg
    assert "#356852" in svg and "#c98a00" in svg
    assert "#3f8064" in svg and "#e0a300" in svg
    assert 'cx="50" cy="50" r="5"' in svg  # core present


def test_favicon_drops_core(parse_svg):
    svg = g.org_favicon()
    parse_svg(svg)  # well-formed
    assert g.OUTER_SNAKE in svg and g.MIDDLE_SNAKE in svg
    assert 'cx="50" cy="50" r="5"' not in svg  # core dropped (two-band)

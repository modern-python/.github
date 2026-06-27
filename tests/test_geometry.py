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


def test_monogram_frame_and_letters(parse_svg):
    svg = g.project_monogram("di", frame_color="#356852", ink="#c98a00",
                             label="modern-di")
    el = parse_svg(svg)
    assert el.attrib["aria-label"] == "modern-di"
    assert g.OUTER_SNAKE in svg          # frame present
    assert g.MIDDLE_SNAKE not in svg     # no inner snake on project marks
    assert "#c98a00" in svg              # ink
    # outlined letters, not <text>
    assert "<text" not in svg


def test_template_has_three_bars(parse_svg):
    svg = g.project_template(frame_color="#356852", ink="#009688",
                             label="fastapi-sqlalchemy-template")
    parse_svg(svg)
    assert svg.count("<rect") == 3
    assert 'width="26" height="6"' in svg

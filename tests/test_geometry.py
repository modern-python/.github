import xml.etree.ElementTree as ET

from brand.build import geometry as g


def test_icon_structure(parse_svg):
    svg = g.icon(bg="#2f5e4a", struct="#f4f1e8", gold="#f0b528")
    el = parse_svg(svg)
    assert el.attrib["viewBox"] == "0 0 100 100"
    assert 'fill="#2f5e4a"' in svg
    assert "M15 68 L15 15 L68 15" in svg
    assert "M85 32 L85 85 L32 85" in svg
    assert 'points="9.5,66 9.5,79 20.5,66"' in svg
    assert 'points="90.5,34 90.5,21 79.5,34"' in svg
    assert 'points="45,40 57,50 45,60"' in svg
    assert "#f4f1e8" in svg and "#f0b528" in svg
    assert "var(" not in svg


def test_lockup_body_has_outlined_wordmark_and_crops(parse_svg):
    body = g.lockup_body(struct="#356852", gold="#c98a00")
    # wrap so it is parseable on its own
    parse_svg(f'<svg xmlns="http://www.w3.org/2000/svg">{body}</svg>')
    assert "M138 122 L138 50 L210 50" in body   # TL crop
    assert "M402 128 L402 200 L330 200" in body  # BR crop
    assert "#356852" in body and "#c98a00" in body
    assert "<text" not in body                   # outlined, not live text
    assert body.count("<path") >= 4              # 2 crops + >=2 glyph paths
    assert 'points="134,120 134,130 142,120"' in body   # TL snake tail
    assert 'points="406,130 406,120 398,130"' in body   # BR snake tail


def test_social_card_cream(parse_svg):
    svg = g.social_card(bg="#f4f1e8", struct="#356852", gold="#c98a00", url_color="#c98a00")
    el = parse_svg(svg)
    assert el.attrib["viewBox"] == "0 0 1280 640"
    assert 'fill="#f4f1e8"' in svg               # cream bg
    assert "translate(235,108) scale(1.5)" in svg
    assert "var(" not in svg and "<text" not in svg


def test_social_square(parse_svg):
    svg = g.social_square(bg="#2f5e4a", struct="#f4f1e8", gold="#f0b528")
    el = parse_svg(svg)
    assert el.attrib["viewBox"] == "0 0 640 640"
    assert "translate(-193.0,82.5) scale(1.9)" in svg


def test_icon_circle(parse_svg):
    svg = g.icon_circle(bg="#2f5e4a", struct="#f4f1e8", gold="#f0b528")
    el = parse_svg(svg)
    assert el.attrib["viewBox"] == "0 0 100 100"
    assert "scale(0.74)" in svg

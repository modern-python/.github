from xml.dom import minidom
from brand.build import geometry as g
from brand.build import tokens as t

def test_project_frame_parses_and_uses_tokens() -> None:
    frame = g.project_frame(struct=t.GREEN_INK, accent=t.GOLD_LIGHT)
    minidom.parseString(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{frame}</svg>')
    assert t.GREEN_INK in frame and t.GOLD_LIGHT in frame

from pathlib import Path
from xml.dom import minidom

from PIL import Image

from brand.build import projects as p
from brand.build import tokens as t


def test_light_and_dark_lockup_colourways() -> None:
    light = p.project_lockup("modern-di")
    dark = p.project_lockup("modern-di", dark=True)
    minidom.parseString(light)
    minidom.parseString(dark)
    assert t.GREEN_INK in light and t.GOLD_LIGHT in light
    # dark uses the on-dark colourway: cream + gold-dark, never the dark-green ink
    assert t.CREAM in dark and t.GOLD_DARK in dark
    assert t.GREEN_INK not in dark


def test_render_writes_three_lockup_assets(tmp_path: Path) -> None:
    p.render_projects(out_dir=tmp_path)
    d = tmp_path / "modern-di"
    assert (d / "lockup-light.svg").is_file()
    assert (d / "lockup-dark.svg").is_file()
    png = d / "lockup.png"
    assert png.is_file()
    assert Image.open(png).mode == "P"  # quantized via export_png

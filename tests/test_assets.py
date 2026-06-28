import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from brand.build import geometry as g
from brand.build.render import bake

ORG = Path("brand/org")


def test_render_writes_valid_org_assets():
    subprocess.run([sys.executable, "-m", "brand.build.render"], check=True)
    for name in ("icon", "favicon", "horizontal", "stacked", "social"):
        p = ORG / f"{name}.svg"
        assert p.exists(), p
        ET.parse(p)  # well-formed


def test_bake_light_concrete_colors():
    light = bake(g.org_icon(), "light")
    assert "#356852" in light and "#c98a00" in light
    assert "var(--" not in light
    assert "<style" not in light


def test_bake_dark_concrete_colors():
    dark = bake(g.org_icon(), "dark")
    assert "#3f8064" in dark and "#e0a300" in dark
    assert "var(--" not in dark


def test_render_writes_baked_and_pngs():
    subprocess.run([sys.executable, "-m", "brand.build.render"], check=True)
    for name in ("icon-light", "icon-dark"):
        p = ORG / f"{name}.svg"
        assert p.exists()
        ET.parse(p)
        assert b"var(--" not in p.read_bytes()
    # PNGs only when rsvg-convert is available
    if shutil.which("rsvg-convert"):
        for name in ("favicon", "social"):
            png = ORG / f"{name}.png"
            assert png.exists()
            assert png.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_modern_di_assets():
    subprocess.run([sys.executable, "-m", "brand.build.render"], check=True)
    base = Path("brand/projects/modern-di")
    icon = (base / "icon.svg").read_text()
    assert 'aria-label="modern-di"' in icon
    assert "#c98a00" in icon            # gold monogram
    assert "<text" not in icon          # outlined
    for name in ("icon", "horizontal", "stacked"):
        ET.parse(base / f"{name}.svg")
    # dark variant: frame color remapped to dark green
    icon_dark = (base / "icon-dark.svg").read_text()
    assert (base / "icon-dark.svg").exists()
    ET.parse(base / "icon-dark.svg")
    assert "#3f8064" in icon_dark       # dark green frame

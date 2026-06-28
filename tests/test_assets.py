import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ORG = Path("brand/org")


def _render():
    subprocess.run([sys.executable, "-m", "brand.build.render"], check=True)


def test_render_writes_favicon():
    _render()
    p = ORG / "favicon.svg"
    assert p.exists()
    ET.parse(p)
    text = p.read_text()
    assert "#2f5e4a" in text and "#f4f1e8" in text and "#f0b528" in text
    assert "var(" not in text
    if shutil.which("rsvg-convert"):
        for sz in (16, 32, 48):
            png = ORG / f"favicon-{sz}.png"
            assert png.exists()
            assert png.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_render_writes_avatar_and_apple_touch():
    _render()
    assert (ORG / "avatar.svg").exists()
    ET.parse(ORG / "avatar.svg")
    apple = (ORG / "apple-touch-icon.svg")
    assert apple.exists()
    assert 'points="45,40 57,50 45,60"' in apple.read_text()
    assert 'points="45,40 57,50 45,60"' in (ORG / "avatar.svg").read_text()
    if shutil.which("rsvg-convert"):
        assert (ORG / "avatar-1024.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
        assert (ORG / "apple-touch-icon-180.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_render_writes_avatar_circle():
    _render()
    assert (ORG / "avatar-circle.svg").exists()
    ET.parse(ORG / "avatar-circle.svg")
    if shutil.which("rsvg-convert"):
        assert (ORG / "avatar-circle-1024.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_render_writes_social_cards():
    _render()
    cream = (ORG / "social-card.svg").read_text()
    assert ET.parse(ORG / "social-card.svg") is not None
    assert 'fill="#f4f1e8"' in cream and "#356852" in cream and "#c98a00" in cream
    green = (ORG / "social-card-green.svg").read_text()
    assert 'fill="#2f5e4a"' in green and "#f4f1e8" in green and "#f0b528" in green
    for name in ("social-card", "social-card-green", "social-square", "social-square-green"):
        ET.parse(ORG / f"{name}.svg")
    if shutil.which("rsvg-convert"):
        for name in ("social-card", "social-card-green", "social-square", "social-square-green"):
            assert (ORG / f"{name}.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"

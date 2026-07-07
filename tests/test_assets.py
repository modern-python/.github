import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ORG = Path("brand/org")
APPAREL = Path("brand/apparel")


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
    apple = ORG / "apple-touch-icon.svg"
    assert apple.exists()
    assert 'points="45,40 57,50 45,60"' in apple.read_text()
    assert 'points="45,40 57,50 45,60"' in (ORG / "avatar.svg").read_text()
    if shutil.which("rsvg-convert"):
        assert (ORG / "avatar-1024.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
        assert (ORG / "apple-touch-icon-180.png").read_bytes()[
            :8
        ] == b"\x89PNG\r\n\x1a\n"


def test_render_writes_avatar_circle():
    _render()
    assert (ORG / "avatar-circle.svg").exists()
    ET.parse(ORG / "avatar-circle.svg")
    if shutil.which("rsvg-convert"):
        assert (ORG / "avatar-circle-1024.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_render_writes_site_wordmark_and_mark():
    _render()
    light = (ORG / "wordmark.svg").read_text()
    assert ET.parse(ORG / "wordmark.svg") is not None
    assert "#356852" in light and "#c98a00" in light  # green ink + gold-light
    dark = (ORG / "wordmark-dark.svg").read_text()
    assert "#f4f1e8" in dark and "#f0b528" in dark  # cream + gold-dark
    for wm in ("wordmark.svg", "wordmark-dark.svg"):
        assert "<rect width=" not in (ORG / wm).read_text()  # no background fill
    mark = (ORG / "mark.svg").read_text()
    assert ET.parse(ORG / "mark.svg") is not None
    assert 'width="100" height="100"' not in mark  # transparent, no bg rect
    assert 'points="45,40 57,50 45,60"' in mark  # chevron
    assert "#f4f1e8" in mark and "#f0b528" in mark


def test_render_writes_social_cards():
    _render()
    cream = (ORG / "social-card.svg").read_text()
    assert ET.parse(ORG / "social-card.svg") is not None
    assert 'fill="#f4f1e8"' in cream and "#356852" in cream and "#c98a00" in cream
    green = (ORG / "social-card-green.svg").read_text()
    assert 'fill="#2f5e4a"' in green and "#f4f1e8" in green and "#f0b528" in green
    for name in (
        "social-card",
        "social-card-green",
        "social-square",
        "social-square-green",
    ):
        ET.parse(ORG / f"{name}.svg")
    if shutil.which("rsvg-convert"):
        for name in (
            "social-card",
            "social-card-green",
            "social-square",
            "social-square-green",
        ):
            assert (ORG / f"{name}.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_render_writes_boosty_cover():
    _render()
    cover = ORG / "boosty-cover.svg"
    assert cover.exists()
    ET.parse(cover)
    text = cover.read_text()
    assert 'viewBox="0 0 1920 480"' in text
    assert 'fill="#2f5e4a"' in text and "#f4f1e8" in text and "#f0b528" in text
    assert "<text" not in text and "var(" not in text
    if shutil.which("rsvg-convert"):
        assert (ORG / "boosty-cover.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_render_writes_apparel():
    _render()
    chest = APPAREL / "chest-mark.svg"
    back = APPAREL / "back-lockup.svg"
    assert chest.exists() and back.exists()
    ET.parse(chest)
    ET.parse(back)
    ctext = chest.read_text()
    assert 'points="45,40 57,50 45,60"' in ctext  # chevron
    assert 'width="100" height="100"' not in ctext  # transparent, no bg rect
    assert "#f4f1e8" in ctext and "#f0b528" in ctext
    btext = back.read_text()
    assert 'aria-label="Modern Python, modern-python.org"' in btext
    assert "<text" not in btext  # outlined URL
    assert "<rect width=" not in btext  # transparent
    assert "#f4f1e8" in btext and "#f0b528" in btext
    if shutil.which("rsvg-convert"):
        for name in ("chest-mark-1050.png", "back-lockup-2400.png"):
            assert (APPAREL / name).read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"

"""Generate the Open Graph / social-card image for modern-python.org.

Layout C: centered wordmark, thin divider, domain — white on brand green.
Run locally (needs the Futura font, present on macOS):

    uv run --with pillow python scripts/gen_social_card.py

Output: docs/assets/social-card.png (1200x630).
"""

import math
import pathlib

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 630
GREEN = (53, 104, 82)  # #356852, the brand color sampled from the logo
WHITE = (255, 255, 255)

FONT_PATH = "/System/Library/Fonts/Supplemental/Futura.ttc"
FONT_INDEX = 0  # Futura Medium

WORDMARK = "MODERN PYTHON"
DOMAIN = "MODERN-PYTHON.ORG"
OUT = pathlib.Path(__file__).resolve().parent.parent / "docs" / "assets" / "social-card.png"


def render_tracked(text: str, font: ImageFont.FreeTypeFont, tracking: float, alpha: int) -> Image.Image:
    """Render `text` with manual letter-spacing into a tight RGBA image."""
    advances = [font.getlength(ch) for ch in text]
    total_w = sum(advances) + tracking * (len(text) - 1)
    bbox = font.getbbox(text)
    top, height = bbox[1], bbox[3] - bbox[1]
    img = Image.new("RGBA", (math.ceil(total_w), height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    x = 0.0
    for ch, adv in zip(text, advances):
        draw.text((x, -top), ch, font=font, fill=(*WHITE, alpha))
        x += adv + tracking
    return img


def fit_wordmark(max_width: int) -> Image.Image:
    """Pick the largest Futura size whose tracked wordmark fits max_width."""
    for size in range(140, 40, -2):
        font = ImageFont.truetype(FONT_PATH, size, index=FONT_INDEX)
        img = render_tracked(WORDMARK, font, tracking=size * 0.14, alpha=255)
        if img.width <= max_width:
            return img
    raise RuntimeError("wordmark never fit")


def main() -> None:
    base = Image.new("RGBA", (WIDTH, HEIGHT), (*GREEN, 255))

    wordmark = fit_wordmark(max_width=1000)
    domain_font = ImageFont.truetype(FONT_PATH, 30, index=FONT_INDEX)
    domain = render_tracked(DOMAIN, domain_font, tracking=30 * 0.16, alpha=217)  # ~85%

    divider_w, divider_h = 360, 3
    gap1, gap2 = 48, 42
    group_h = wordmark.height + gap1 + divider_h + gap2 + domain.height
    y = (HEIGHT - group_h) // 2

    base.alpha_composite(wordmark, ((WIDTH - wordmark.width) // 2, y))
    y += wordmark.height + gap1

    divider = Image.new("RGBA", (divider_w, divider_h), (*WHITE, 128))  # ~50%
    base.alpha_composite(divider, ((WIDTH - divider_w) // 2, y))
    y += divider_h + gap2

    base.alpha_composite(domain, ((WIDTH - domain.width) // 2, y))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(OUT, "PNG")
    print(f"wrote {OUT} ({base.width}x{base.height})")


if __name__ == "__main__":
    main()

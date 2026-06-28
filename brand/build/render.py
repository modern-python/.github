import shutil
import subprocess
from pathlib import Path

from brand.build import geometry as g
from brand.build import tokens as t

ROOT = Path(__file__).resolve().parents[2]
ORG = ROOT / "brand" / "org"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")


def export_png(
    svg_path: Path,
    png_path: Path,
    *,
    width: int | None = None,
    height: int | None = None,
) -> bool:
    exe = shutil.which("rsvg-convert")
    if exe is None:
        return False
    args = [exe]
    if width is not None:
        args += ["-w", str(width)]
    if height is not None:
        args += ["-h", str(height)]
    args += [str(svg_path), "-o", str(png_path)]
    subprocess.run(args, check=True)
    return True


def render() -> None:
    ORG.mkdir(parents=True, exist_ok=True)
    ic = dict(bg=t.GREEN_SURFACE, struct=t.CREAM, gold=t.GOLD_DARK)
    # favicon
    _write(ORG / "favicon.svg", g.icon(**ic))
    for sz in (16, 32, 48):
        export_png(ORG / "favicon.svg", ORG / f"favicon-{sz}.png", width=sz, height=sz)
    # apple-touch (same mark, already full-bleed/square)
    _write(ORG / "apple-touch-icon.svg", g.icon(**ic))
    export_png(ORG / "apple-touch-icon.svg", ORG / "apple-touch-icon-180.png", width=180, height=180)
    # avatar (same mark, large raster)
    _write(ORG / "avatar.svg", g.icon(**ic))
    export_png(ORG / "avatar.svg", ORG / "avatar-1024.png", width=1024, height=1024)
    _write(ORG / "avatar-circle.svg",
           g.icon_circle(bg=t.GREEN_SURFACE, struct=t.CREAM, gold=t.GOLD_DARK))
    export_png(ORG / "avatar-circle.svg", ORG / "avatar-circle-1024.png", width=1024, height=1024)

    # Site logos — transparent, no background.
    #   wordmark (hero): two-color lockup, light + dark variants
    #   mark (header): chevron mark in cream/gold-dark for the green header bar
    _write(ORG / "wordmark.svg", g.wordmark(struct=t.GREEN_INK, gold=t.GOLD_LIGHT))
    _write(ORG / "wordmark-dark.svg", g.wordmark(struct=t.CREAM, gold=t.GOLD_DARK))
    _write(ORG / "mark.svg", g.mark(struct=t.CREAM, gold=t.GOLD_DARK))

    # Social cards — cream (primary) + green (alternate).
    _write(ORG / "social-card.svg",
           g.social_card(bg=t.CREAM, struct=t.GREEN_INK, gold=t.GOLD_LIGHT, url_color=t.GOLD_LIGHT))
    export_png(ORG / "social-card.svg", ORG / "social-card.png", width=1280, height=640)
    _write(ORG / "social-card-green.svg",
           g.social_card(bg=t.GREEN_SURFACE, struct=t.CREAM, gold=t.GOLD_DARK, url_color=t.GOLD_DARK))
    export_png(ORG / "social-card-green.svg", ORG / "social-card-green.png", width=1280, height=640)

    # Square (Telegram / square social) — cream + green.
    _write(ORG / "social-square.svg",
           g.social_square(bg=t.CREAM, struct=t.GREEN_INK, gold=t.GOLD_LIGHT))
    export_png(ORG / "social-square.svg", ORG / "social-square.png", width=640, height=640)
    _write(ORG / "social-square-green.svg",
           g.social_square(bg=t.GREEN_SURFACE, struct=t.CREAM, gold=t.GOLD_DARK))
    export_png(ORG / "social-square-green.svg", ORG / "social-square-green.png", width=640, height=640)


def main() -> None:
    render()


if __name__ == "__main__":
    main()

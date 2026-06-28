import re
import shutil
import subprocess
from pathlib import Path

from brand.build import geometry as g
from brand.build import tokens as t

ROOT = Path(__file__).resolve().parents[2]
ORG = ROOT / "brand" / "org"

MANIFEST: list[tuple[Path, object]] = []

_STYLE_RE = re.compile(r"<style>.*?</style>", re.DOTALL)

_BAKE: dict[str, dict[str, str]] = {
    "light": {"--struct": t.GREEN, "--accent": t.GOLD, "--ink": t.GREEN},
    "dark": {"--struct": t.GREEN_DARK, "--accent": t.GOLD_DARK, "--ink": t.GREEN_DARK},
}


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")


def bake(svg: str, mode: str) -> str:
    out = _STYLE_RE.sub("", svg, count=1)
    for var_name, color in _BAKE[mode].items():
        out = out.replace(f"var({var_name})", color)
    return out


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


def render_org() -> None:
    inner = g.icon_inner("org")
    _write(ORG / "icon.svg", g.org_icon())
    _write(ORG / "favicon.svg", g.org_favicon())
    _write(ORG / "horizontal.svg", g.lockup_horizontal(inner, "modern-python", label="Modern Python"))
    _write(ORG / "stacked.svg", g.lockup_stacked(inner, "modern-python", label="Modern Python"))
    _write(ORG / "social.svg", g.social_card(inner, "modern-python", label="Modern Python"))
    _write(ORG / "icon-light.svg", bake(g.org_icon(), "light"))
    _write(ORG / "icon-dark.svg", bake(g.org_icon(), "dark"))
    # PNG exports from baked-light sources (favicon for tabs, social for og:image)
    _write(ORG / "_favicon-light.svg", bake(g.org_favicon(), "light"))
    export_png(ORG / "_favicon-light.svg", ORG / "favicon.png", width=64, height=64)
    _write(ORG / "_social-light.svg", bake(g.social_card(inner, "modern-python", label="Modern Python"), "light"))
    export_png(ORG / "_social-light.svg", ORG / "social.png", width=1280, height=640)
    (ORG / "_favicon-light.svg").unlink(missing_ok=True)
    (ORG / "_social-light.svg").unlink(missing_ok=True)


def main() -> None:
    render_org()
    # project rendering added in later tasks


if __name__ == "__main__":
    main()

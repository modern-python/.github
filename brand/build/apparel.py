from pathlib import Path

from brand.build import geometry as g
from brand.build import tokens as t
from brand.build.raster import export_png

ROOT = Path(__file__).resolve().parents[2]
APPAREL = ROOT / "brand" / "apparel"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")


def render_apparel() -> None:
    """Print-ready artwork for the black org t-shirt: a transparent left-chest
    chevron mark and a back wordmark+URL lockup, both cream + gold-dark. SVG is
    the master; PNGs are 300 DPI print fallbacks (chest 3.5 in, back 8 in)."""
    APPAREL.mkdir(parents=True, exist_ok=True)
    ink = dict(struct=t.CREAM, gold=t.GOLD_DARK)
    _write(APPAREL / "chest-mark.svg", g.mark(**ink))
    export_png(APPAREL / "chest-mark.svg", APPAREL / "chest-mark-1050.png", width=1050)
    _write(APPAREL / "back-lockup.svg", g.apparel_back(**ink))
    export_png(APPAREL / "back-lockup.svg", APPAREL / "back-lockup-2400.png", width=2400)

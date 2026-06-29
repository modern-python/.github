from collections.abc import Callable
from pathlib import Path

from brand.build import geometry as g
from brand.build import symbols as sym
from brand.build import tokens as t
from brand.build.raster import export_png

R = 23
_CX = _CY = 50

ALLOWED_COLORS: frozenset[str] = frozenset(
    c.lower() for c in (t.GREEN_INK, t.GOLD_LIGHT, t.CREAM, *sym._BAR_TINTS)
)

MANIFEST: dict[str, Callable[[], str]] = {
    # dependency injection
    "modern-di": lambda: sym.graph(_CX, _CY, R, dashed=True),
    "that-depends": lambda: sym.graph(_CX, _CY, R, dashed=False),
    "modern-di-fastapi": lambda: sym.bolt_disc(_CX, _CY, R),
    "modern-di-litestar": lambda: sym.star_disc(_CX, _CY, R),
    "modern-di-faststream": lambda: sym.faststream(_CX, _CY, R),
    "modern-di-typer": lambda: sym.terminal(_CX, _CY, R),
    "modern-di-pytest": lambda: sym.bars(_CX, _CY, R),
    # templates — reuse the org chevron
    "fastapi-sqlalchemy-template": lambda: sym.chevron(_CX, _CY, R - 1),
    "litestar-sqlalchemy-template": lambda: sym.chevron(_CX, _CY, R - 1),
    # microservices, http & messaging
    "lite-bootstrap": lambda: sym.rocket(_CX, _CY, R),
    "httpware": lambda: sym.chain(_CX, _CY, R),
    "faststream-redis-timers": lambda: sym.stopwatch(_CX, _CY, R),
    "faststream-concurrent-aiokafka": lambda: sym.lanes(_CX, _CY, R),
    "faststream-outbox": lambda: sym.outbox(_CX, _CY, R),
    # utilities
    "db-retry": lambda: sym.db_retry(_CX, _CY, R),
    "eof-fixer": lambda: sym.eof_fixer(_CX, _CY, R),
    "semvertag": lambda: sym.tag(_CX, _CY, R),
}


ROOT = Path(__file__).resolve().parents[2]
PROJECTS = ROOT / "brand" / "projects"
_PNG_SIZES = (512, 1024)


def project_mark(repo: str) -> str:
    """Full <svg> for a repo: constant frame + its gold inner symbol."""
    frame = g.project_frame(struct=t.GREEN_INK, accent=t.GOLD_LIGHT)
    inner = MANIFEST[repo]()
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" '
        f'role="img" aria-label="{repo}">{frame}{inner}</svg>'
    )


def render_projects(out_dir: Path | None = None) -> list[Path]:
    """Write mark.svg (+ PNGs) for every repo under out_dir/<repo>/."""
    base = out_dir if out_dir is not None else PROJECTS
    written: list[Path] = []
    for repo in MANIFEST:
        d = base / repo
        d.mkdir(parents=True, exist_ok=True)
        svg = d / "mark.svg"
        svg.write_text(project_mark(repo) + "\n", encoding="utf-8")
        for sz in _PNG_SIZES:
            export_png(svg, d / f"mark-{sz}.png", width=sz, height=sz)
        written.append(svg)
    return written

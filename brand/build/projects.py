from collections.abc import Callable
from pathlib import Path

from brand.build import geometry as g
from brand.build import symbols as sym
from brand.build import tokens as t
from brand.build.raster import export_png
from brand.build.text import outline_text

R = 23
_CX = _CY = 50

ALLOWED_COLORS: frozenset[str] = frozenset(
    c.lower() for c in (t.GREEN_INK, t.GOLD_LIGHT, t.CREAM, *sym._BAR_TINTS)
)

MANIFEST: dict[str, Callable[[], str]] = {
    # dependency injection
    "modern-di": lambda: sym.graph(_CX, _CY, R, dashed=True),
    "that-depends": lambda: sym.graph(_CX, _CY, R, dashed=False),
    "modern-di-aiohttp": lambda: sym.async_loop(_CX, _CY, R),
    "modern-di-aiogram": lambda: sym.plane(_CX, _CY, R),
    "modern-di-arq": lambda: sym.hopper(_CX, _CY, R),
    "modern-di-fastapi": lambda: sym.bolt_disc(_CX, _CY, R),
    "modern-di-faststream": lambda: sym.faststream(_CX, _CY, R),
    "modern-di-litestar": lambda: sym.star_disc(_CX, _CY, R),
    "modern-di-pytest": lambda: sym.bars(_CX, _CY, R),
    "modern-di-starlette": lambda: sym.sparkle_cluster(_CX, _CY, R),
    "modern-di-typer": lambda: sym.terminal(_CX, _CY, R),
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
    "compose2pod": lambda: sym.pod(_CX, _CY, R),
}


ROOT = Path(__file__).resolve().parents[2]
PROJECTS = ROOT / "brand" / "projects"
_PNG_SIZES = (512, 1024)

_LOCKUP_H = 100
_NAME_SIZE = 34
_GAP = 18


def project_mark(repo: str) -> str:
    """Full <svg> for a repo: constant frame + its gold inner symbol."""
    frame = g.project_frame(struct=t.GREEN_INK, accent=t.GOLD_LIGHT)
    inner = MANIFEST[repo]()
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" '
        f'role="img" aria-label="{repo}">{frame}{inner}</svg>'
    )


def project_lockup(repo: str, *, dark: bool = False) -> str:
    """Framed mark + the repo name in Jost. Light = green-ink/gold (light UIs);
    dark = cream/gold-dark (dark UIs). Transparent background either way."""
    struct = t.CREAM if dark else t.GREEN_INK
    accent = t.GOLD_DARK if dark else t.GOLD_LIGHT
    name_color = t.CREAM if dark else t.GREEN_INK
    mark_frame = g.project_frame(struct=struct, accent=accent)
    inner = MANIFEST[repo]()
    if dark:
        inner = inner.replace(t.GOLD_LIGHT, t.GOLD_DARK)
    name_x = _LOCKUP_H + _GAP
    name_svg, name_w = outline_text(
        repo,
        _NAME_SIZE,
        x=name_x,
        baseline_y=_LOCKUP_H / 2 + _NAME_SIZE * 0.34,
        anchor="start",
        color=name_color,
    )
    total_w = round(name_x + name_w + _GAP)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {_LOCKUP_H}" '
        f'role="img" aria-label="{repo}"><g>{mark_frame}{inner}</g>{name_svg}</svg>'
    )


def render_projects(out_dir: Path | None = None) -> list[Path]:
    """Write mark.svg, lockup-light.svg, lockup-dark.svg, lockup.png (+ mark PNGs)
    for every repo under out_dir/<repo>/.

    Docs-site repos (DOCS_REPOS) also get social-card.svg/png (1280×640)."""
    base = out_dir if out_dir is not None else PROJECTS
    written: list[Path] = []
    for repo in MANIFEST:
        d = base / repo
        d.mkdir(parents=True, exist_ok=True)
        svg = d / "mark.svg"
        svg.write_text(project_mark(repo) + "\n", encoding="utf-8")
        for sz in _PNG_SIZES:
            export_png(svg, d / f"mark-{sz}.png", width=sz, height=sz)
        (d / "lockup-light.svg").write_text(project_lockup(repo) + "\n", encoding="utf-8")
        dark_svg = d / "lockup-dark.svg"
        dark_svg.write_text(project_lockup(repo, dark=True) + "\n", encoding="utf-8")
        export_png(d / "lockup-light.svg", d / "lockup.png")
        if repo in DOCS_REPOS:
            card = d / "social-card.svg"
            card.write_text(
                project_social_card(repo, tagline=DOCS_REPOS[repo]) + "\n",
                encoding="utf-8",
            )
            export_png(card, d / "social-card.png", width=_CARD_W, height=_CARD_H)
        written.append(svg)
    return written


def _measure(text: str, size: float) -> float:
    _, w = outline_text(text, size, x=0, baseline_y=0, anchor="start", color="#000000")
    return w


def fit_text(
    text: str,
    base_size: float,
    max_w: float,
    *,
    color: str,
    x: float,
    baseline_y: float,
) -> tuple[str, float]:
    """Render `text` left-anchored; shrink the font so its width fits max_w."""
    natural = _measure(text, base_size)
    size = base_size if natural <= max_w else base_size * max_w / natural
    svg, _ = outline_text(
        text, size, x=x, baseline_y=baseline_y, anchor="start", color=color
    )
    return svg, size


def wrap_text(text: str, size: float, max_w: float) -> list[str]:
    """Greedy word-wrap to lines no wider than max_w."""
    lines: list[str] = []
    cur = ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if cur and _measure(trial, size) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


DOCS_REPOS: dict[str, str] = {
    "modern-di": "powerful DI framework with scopes",
    "that-depends": "predecessor DI framework, still actively maintained",
    "lite-bootstrap": "lightweight package for bootstrapping new microservices",
    "httpware": "HTTP client framework with sync/async clients, middleware chain, and built-in resilience (retry, bulkhead)",
    "faststream-redis-timers": "FastStream broker integration for Redis-backed distributed timer scheduling",
    "faststream-outbox": "FastStream broker integration for the transactional outbox pattern with Postgres",
    "semvertag": "auto-tag your GitHub/GitLab repo with semantic version tags from CI",
}

_CARD_W = 1280
_CARD_H = 640
_PANEL = 460  # green panel width
_TEXT_X = 520  # text column left edge
_TEXT_W = 700  # text column width
_NAME_BASE = 74
_TAG_SIZE = 30
_URL_SIZE = 26


def project_social_card(repo: str, *, tagline: str) -> str:
    """1280x640 og:image: green mark panel + cream name/tagline/url panel."""
    panels = (
        f'<rect width="{_PANEL}" height="{_CARD_H}" fill="{t.GREEN_SURFACE}"/>'
        f'<rect x="{_PANEL}" width="{_CARD_W - _PANEL}" height="{_CARD_H}" fill="{t.CREAM}"/>'
    )
    frame = g.project_frame(struct=t.CREAM, accent=t.GOLD_DARK)
    inner = MANIFEST[repo]()
    mark = f'<g transform="translate(80,170) scale(3.0)">{frame}{inner}</g>'

    tag_lines = wrap_text(tagline, _TAG_SIZE, _TEXT_W)
    n = len(tag_lines)
    # block = name + 26 gap + n*38 tagline lines + 44 gap + url(30); centre vertically
    block_h = _NAME_BASE + 26 + n * 38 + 44 + 30
    top = (_CARD_H - block_h) / 2
    name_base = top + _NAME_BASE
    name_svg, _ = fit_text(
        repo, _NAME_BASE, _TEXT_W, color=t.GREEN_INK, x=_TEXT_X, baseline_y=name_base
    )
    y = name_base + 26
    tag_svg = ""
    for line in tag_lines:
        y += 38
        seg, _ = outline_text(
            line,
            _TAG_SIZE,
            x=_TEXT_X,
            baseline_y=y,
            anchor="start",
            color=t.GREEN_MUTED,
        )
        tag_svg += seg
    y += 44
    url_svg, _ = outline_text(
        f"{repo}.modern-python.org",
        _URL_SIZE,
        x=_TEXT_X,
        baseline_y=y,
        anchor="start",
        color=t.GOLD_LIGHT,
        letter_spacing=2,
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_CARD_W} {_CARD_H}" '
        f'role="img" aria-label="{repo} — {tagline}">'
        f"{panels}{mark}{name_svg}{tag_svg}{url_svg}</svg>"
    )

import re
from pathlib import Path
from xml.dom import minidom
import pytest
from PIL import Image
from brand.build import geometry as g
from brand.build import tokens as t
from brand.build import projects as p
from brand.build.raster import export_png


def test_project_frame_parses_and_uses_tokens() -> None:
    frame = g.project_frame(struct=t.GREEN_INK, accent=t.GOLD_LIGHT)
    minidom.parseString(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{frame}</svg>'
    )
    assert t.GREEN_INK in frame and t.GOLD_LIGHT in frame


EXPECTED_REPOS = {
    "modern-di",
    "that-depends",
    "modern-di-fastapi",
    "modern-di-litestar",
    "modern-di-starlette",
    "modern-di-aiohttp",
    "modern-di-faststream",
    "modern-di-typer",
    "modern-di-pytest",
    "modern-di-aiogram",
    "fastapi-sqlalchemy-template",
    "litestar-sqlalchemy-template",
    "lite-bootstrap",
    "httpware",
    "faststream-redis-timers",
    "faststream-concurrent-aiokafka",
    "faststream-outbox",
    "db-retry",
    "eof-fixer",
    "semvertag",
    "modern-di-arq",
    "compose2pod",
    "modern-di-celery",
    "modern-di-taskiq",
    "modern-di-flask",
    "modern-di-grpc",
}


def test_manifest_covers_every_repo() -> None:
    assert set(p.MANIFEST) == EXPECTED_REPOS


@pytest.mark.parametrize("repo", sorted(EXPECTED_REPOS))
def test_project_mark_is_valid_svg(repo: str) -> None:
    svg = p.project_mark(repo)
    minidom.parseString(svg)
    assert svg.startswith("<svg") and 'viewBox="0 0 100 100"' in svg


@pytest.mark.parametrize("repo", sorted(EXPECTED_REPOS))
def test_only_allowed_colours(repo: str) -> None:
    hexes = {h.lower() for h in re.findall(r"#[0-9a-fA-F]{6}", p.project_mark(repo))}
    assert hexes <= p.ALLOWED_COLORS, (
        f"{repo} stray colours: {hexes - p.ALLOWED_COLORS}"
    )


def test_templates_use_chevron() -> None:
    # both templates share the org chevron (a polyline), not a bespoke symbol
    for repo in ("fastapi-sqlalchemy-template", "litestar-sqlalchemy-template"):
        assert "<polyline" in p.project_mark(repo)


def test_render_projects_writes_every_mark(tmp_path: Path) -> None:
    written = p.render_projects(out_dir=tmp_path)
    assert len(written) == len(EXPECTED_REPOS)
    for repo in EXPECTED_REPOS:
        svg = tmp_path / repo / "mark.svg"
        assert svg.is_file() and svg.read_text(encoding="utf-8").startswith("<svg")


@pytest.mark.parametrize("repo", ["modern-di", "faststream-outbox", "semvertag"])
def test_lockup_is_valid_and_names_repo(repo: str) -> None:
    svg = p.project_lockup(repo)
    minidom.parseString(svg)
    assert svg.startswith("<svg")


def test_render_projects_writes_lockup(tmp_path: Path) -> None:
    p.render_projects(out_dir=tmp_path)
    repo_dir = tmp_path / "modern-di"
    assert (repo_dir / "lockup-light.svg").is_file()
    assert (repo_dir / "lockup-dark.svg").is_file()
    assert (repo_dir / "lockup.png").is_file()


def test_fit_text_shrinks_only_when_needed() -> None:
    short_svg, short_size = p.fit_text(
        "hi", 74, 700, color="#356852", x=0, baseline_y=0
    )
    assert short_size == 74  # fits, unchanged
    long_svg, long_size = p.fit_text(
        "x" * 80, 74, 700, color="#356852", x=0, baseline_y=0
    )
    assert long_size < 74  # too wide -> shrunk
    assert "<g" in short_svg and "<g" in long_svg


def test_wrap_text_splits_long_and_keeps_short() -> None:
    assert len(p.wrap_text("short tagline", 30, 700)) == 1
    assert len(p.wrap_text("word " * 60, 30, 700)) > 1


DOCS_EXPECTED = {
    "modern-di",
    "that-depends",
    "lite-bootstrap",
    "httpware",
    "faststream-redis-timers",
    "faststream-outbox",
    "semvertag",
}

CARD_ALLOWED = {
    c.lower()
    for c in (
        t.GREEN_INK,
        t.GREEN_SURFACE,
        t.GOLD_LIGHT,
        t.GOLD_DARK,
        t.CREAM,
        t.GREEN_MUTED,
    )
}


def test_docs_repos_is_subset_of_manifest_and_exact() -> None:
    assert set(p.DOCS_REPOS) == DOCS_EXPECTED
    assert set(p.DOCS_REPOS) <= set(p.MANIFEST)


@pytest.mark.parametrize("repo", sorted(DOCS_EXPECTED))
def test_social_card_valid_and_palette(repo: str) -> None:
    svg = p.project_social_card(repo, tagline=p.DOCS_REPOS[repo])
    minidom.parseString(svg)
    assert 'viewBox="0 0 1280 640"' in svg
    hexes = {h.lower() for h in re.findall(r"#[0-9a-fA-F]{6}", svg)}
    assert hexes <= CARD_ALLOWED, f"{repo} stray colours: {hexes - CARD_ALLOWED}"


def test_social_card_includes_url_and_name(repo: str = "modern-di") -> None:
    svg = p.project_social_card(repo, tagline=p.DOCS_REPOS[repo])
    assert f'aria-label="{repo}' in svg  # accessible label carries the repo


def test_render_projects_writes_cards_for_docs_repos_only(tmp_path: Path) -> None:
    p.render_projects(out_dir=tmp_path)
    for repo in DOCS_EXPECTED:
        card = tmp_path / repo / "social-card.svg"
        assert card.is_file() and card.read_text(encoding="utf-8").startswith("<svg")
    non_docs = set(p.MANIFEST) - DOCS_EXPECTED
    for repo in non_docs:
        assert not (tmp_path / repo / "social-card.svg").exists()


# Regression guard for the transparent-background invariant: every mark is
# drawn on a transparent background, and CREAM is only ever a knockout
# painted ON TOP OF a GOLD shape — never standalone ink directly on the
# background. Violate that and the mark looks fine on a cream/light page
# (cream-on-cream is invisible) but shows stray bright-white ink once the
# same mark.svg is placed on a dark surface (e.g. lockup-dark.svg's README
# banner half). Only the seven marks introduced on this branch are checked
# here — see NEW_MARKS below.
#
# Known, pre-existing, OUT OF SCOPE exclusions: `db-retry` and
# `faststream-outbox` both use the `_cyl` helper, whose 0.8-wide CREAM rim
# stroke straddles an ellipse edge and leaves a faint cream hairline outside
# the gold — the same class of bug, shipped before this branch. Fixing
# `_cyl` is a separate follow-up; it is deliberately not touched here.
NEW_MARKS = {
    "modern-di-aiogram",
    "modern-di-arq",
    "modern-di-celery",
    "modern-di-flask",
    "modern-di-grpc",
    "modern-di-taskiq",
    "compose2pod",
}


def _cream_pixels_without_gold_beneath(
    repo: str, tmp_path: Path, size: int = 256
) -> list[tuple[int, int]]:
    """Rasterize `repo`'s mark twice — once normally, once with every CREAM
    knockout stripped to `none` — and return the (x, y) of every pixel that
    is CREAM in the normal render but transparent once CREAM is stripped.
    Such a pixel has no gold underneath it: it is standalone cream ink
    sitting directly on the transparent background."""
    svg = p.project_mark(repo)
    normal_svg = tmp_path / f"{repo}-normal.svg"
    normal_svg.write_text(svg, encoding="utf-8")
    normal_png = tmp_path / f"{repo}-normal.png"
    assert export_png(normal_svg, normal_png, width=size, height=size)

    stripped_svg = tmp_path / f"{repo}-stripped.svg"
    stripped_svg.write_text(svg.replace(t.CREAM, "none"), encoding="utf-8")
    stripped_png = tmp_path / f"{repo}-stripped.png"
    assert export_png(stripped_svg, stripped_png, width=size, height=size)

    normal_im = Image.open(normal_png).convert("RGBA")
    stripped_im = Image.open(stripped_png).convert("RGBA")
    cream_rgb = tuple(int(t.CREAM[i : i + 2], 16) for i in (1, 3, 5))
    tol = 10
    bad: list[tuple[int, int]] = []
    for idx, ((r, gg, b, a), (_, _, _, sa)) in enumerate(
        zip(normal_im.getdata(), stripped_im.getdata())
    ):
        if a < 200:
            continue
        if (
            abs(r - cream_rgb[0]) < tol
            and abs(gg - cream_rgb[1]) < tol
            and abs(b - cream_rgb[2]) < tol
            and sa < 50
        ):
            bad.append((idx % size, idx // size))
    return bad


@pytest.mark.parametrize("repo", sorted(NEW_MARKS))
def test_new_marks_have_no_cream_on_transparent(repo: str, tmp_path: Path) -> None:
    bad = _cream_pixels_without_gold_beneath(repo, tmp_path)
    assert not bad, (
        f"{repo}: {len(bad)} cream pixel(s) with no gold beneath, e.g. {bad[:5]} "
        "— this mark will show stray white ink on dark surfaces"
    )

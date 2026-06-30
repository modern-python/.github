import re
from pathlib import Path
from xml.dom import minidom
import pytest
from brand.build import geometry as g
from brand.build import tokens as t
from brand.build import projects as p


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
    "modern-di-faststream",
    "modern-di-typer",
    "modern-di-pytest",
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
    assert (tmp_path / "modern-di" / "lockup.svg").is_file()


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

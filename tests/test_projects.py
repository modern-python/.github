import re
from xml.dom import minidom
import pytest
from brand.build import geometry as g
from brand.build import tokens as t
from brand.build import projects as p

def test_project_frame_parses_and_uses_tokens() -> None:
    frame = g.project_frame(struct=t.GREEN_INK, accent=t.GOLD_LIGHT)
    minidom.parseString(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{frame}</svg>')
    assert t.GREEN_INK in frame and t.GOLD_LIGHT in frame

EXPECTED_REPOS = {
    "modern-di", "that-depends", "modern-di-fastapi", "modern-di-litestar",
    "modern-di-faststream", "modern-di-typer", "modern-di-pytest",
    "fastapi-sqlalchemy-template", "litestar-sqlalchemy-template",
    "lite-bootstrap", "httpware", "faststream-redis-timers",
    "faststream-concurrent-aiokafka", "faststream-outbox",
    "db-retry", "eof-fixer", "semvertag",
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
    assert hexes <= p.ALLOWED_COLORS, f"{repo} stray colours: {hexes - p.ALLOWED_COLORS}"

def test_templates_use_chevron() -> None:
    # both templates share the org chevron (a polyline), not a bespoke symbol
    for repo in ("fastapi-sqlalchemy-template", "litestar-sqlalchemy-template"):
        assert "<polyline" in p.project_mark(repo)

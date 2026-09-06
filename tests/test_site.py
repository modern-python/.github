from pathlib import Path

_INDEX = Path(__file__).parent.parent / "docs" / "index.md"


def test_home_page_supplies_its_own_h1() -> None:
    """INVARIANT: the org home page's content carries an `<h1>` of its own.

    Material injects a fallback `<h1>{{ page.title }}</h1>` only when the rendered
    content has none, so the wordmark hero has to be wrapped in one. Swap that `<h1>`
    for a `<div>` — the natural move, since the hero is an image and reads as
    decoration — and the site quietly grows a "Modern Python" heading above it.
    """
    assert "<h1" in _INDEX.read_text(encoding="utf-8")

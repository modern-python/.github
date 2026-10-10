import re
from pathlib import Path

from brand.build import projects as p

_INDEX = Path(__file__).parent.parent / "docs" / "index.md"


def test_home_page_supplies_its_own_h1() -> None:
    """INVARIANT: the org home page's content carries an `<h1>` of its own.

    Material injects a fallback `<h1>{{ page.title }}</h1>` only when the rendered
    content has none, so the wordmark hero has to be wrapped in one. Swap that `<h1>`
    for a `<div>` — the natural move, since the hero is an image and reads as
    decoration — and the site quietly grows a "Modern Python" heading above it.
    """
    assert "<h1" in _INDEX.read_text(encoding="utf-8")


def test_every_listed_project_mark_has_a_site_entry() -> None:
    """INVARIANT: the repos in the org site's project lists are exactly the repos in
    `projects.py::MANIFEST` minus the `modern-di-*` integrations.

    It is the site's half of the profile-row invariant. A hand-kept list of expected
    repos drifts the same way the page does, so a repo added to the org and the profile
    can still be missing here without anything failing.
    """
    listed = set(
        re.findall(
            r"^- \[`([^`]+)`\]\(https://github\.com/modern-python/\1\)",
            _INDEX.read_text(encoding="utf-8"),
            flags=re.M,
        )
    )
    assert listed == {repo for repo in p.MANIFEST if not repo.startswith("modern-di-")}

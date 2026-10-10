import re
from pathlib import Path

from brand.build import projects as p

_PROFILE = Path(__file__).parent.parent / "profile" / "README.md"
_INDEX = Path(__file__).parent.parent / "docs" / "index.md"


def _sections() -> dict[str, str]:
    parts = re.split(r"^### ", _PROFILE.read_text(encoding="utf-8"), flags=re.M)[1:]
    return {part.splitlines()[0].strip(): part for part in parts}


def _repos(section: str) -> list[str]:
    return re.findall(r"^\| \[`([^`]+)`\]", section, flags=re.M)


def test_every_listed_project_mark_has_a_profile_row() -> None:
    """INVARIANT: the repos listed in `profile/README.md` are exactly the repos in
    `projects.py::MANIFEST` minus the `modern-di-*` integrations.

    They are the two halves of one act — a repo joins the org by getting a mark and a
    profile row — but nothing links them, so adding, renaming, or unpublishing a repo
    updates one and silently leaves the other behind. The failure is invisible: a mark
    nobody links to, or a row whose banner 404s. Integrations keep their marks, because
    their READMEs load the lockups from this repo, but are listed only on the modern-di
    docs site.
    """
    listed = {repo for section in _sections().values() for repo in _repos(section)}
    assert listed == {repo for repo in p.MANIFEST if not repo.startswith("modern-di-")}


def test_di_table_lists_only_the_two_frameworks() -> None:
    """INVARIANT: the Dependency injection table lists `modern-di` then `that-depends`.

    The order carries meaning: the core users should start from, then the earlier
    framework that stays maintained.
    """
    assert _repos(_sections()["Dependency injection"]) == ["modern-di", "that-depends"]


def test_no_modern_di_integration_on_the_org_profile_or_site() -> None:
    """INVARIANT: neither the org profile nor the org site homepage links a
    `modern-di-*` integration repo.

    Integrations are listed on the modern-di docs site. Re-adding one here is the
    natural move when a new integration ships, and it brings the clutter back.
    """
    for page in (_PROFILE, _INDEX):
        assert re.findall(r"github\.com/modern-python/(modern-di-[\w-]+)", page.read_text(encoding="utf-8")) == []


def test_templates_carry_stars_only() -> None:
    """INVARIANT: the Project templates table has no Downloads column.

    Templates are not published to PyPI, so a Downloads badge would 404 forever rather
    than self-heal the way a not-yet-published library's does. Copying a library row as
    the starting point for a new template row is how the dead badge gets in.
    """
    section = _sections()["Project templates"]
    headers = [line for line in section.splitlines() if line.startswith("| Project")]
    assert len(headers) == 1, "the templates table lost its header row"
    assert "Downloads" not in headers[0]
    assert "pepy" not in section


def test_every_download_badge_is_pepy_and_names_its_repo() -> None:
    """INVARIANT: a Downloads badge is a `static.pepy.tech` baked SVG for a package
    named exactly after its repo.

    Two ways this breaks, both invisible from here. The shields `pypi/dm` endpoint is
    the obvious equivalent and is flaky enough to make the whole strip look
    unmaintained. And a badge naming a package that is not the repo — the one case
    where distribution name and repo name are allowed to drift apart — renders as a
    permanent 404 that looks exactly like a package not yet published.
    """
    text = _PROFILE.read_text(encoding="utf-8")
    assert "pypi/dm" not in text

    badges = re.findall(r"static\.pepy\.tech/badge/([^/]+)/month", text)
    assert badges, "no Downloads badges found; the row shape must have changed"

    rows = re.findall(
        r"^\| \[`([^`]+)`\].*?static\.pepy\.tech/badge/([^/]+)/month",
        text,
        flags=re.M,
    )
    assert len(rows) == len(badges)
    assert [repo for repo, package in rows if repo != package] == []


def test_every_social_card_tagline_is_its_profile_description() -> None:
    """INVARIANT: a docs repo's social-card tagline is the description in its profile row.

    The profile row already mirrors the GitHub description and the pyproject
    `description`. The card tagline is a fourth copy that lives in Python, so a
    description rewrite updates the other three and leaves the card telling link
    previews something the repo no longer says.
    """
    text = _PROFILE.read_text(encoding="utf-8")
    descriptions = dict(re.findall(r"^\| \[`([^`]+)`\]\([^)]*\) \| ([^|]+?) \|", text, flags=re.M))
    assert p.DOCS_REPOS == {repo: descriptions[repo] for repo in p.DOCS_REPOS}

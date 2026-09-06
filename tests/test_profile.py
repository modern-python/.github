import re
from pathlib import Path

from brand.build import projects as p

_PROFILE = Path(__file__).parent.parent / "profile" / "README.md"


def _sections() -> dict[str, str]:
    parts = re.split(r"^### ", _PROFILE.read_text(encoding="utf-8"), flags=re.M)[1:]
    return {part.splitlines()[0].strip(): part for part in parts}


def _repos(section: str) -> list[str]:
    return re.findall(r"^\| \[`([^`]+)`\]", section, flags=re.M)


def test_every_project_mark_has_a_profile_row() -> None:
    """INVARIANT: the repos in `projects.py::MANIFEST` and the repos listed in
    `profile/README.md` are the same set.

    They are the two halves of one act — a repo joins the org by getting a mark and a
    profile row — but nothing links them, so adding, renaming, or unpublishing a repo
    updates one and silently leaves the other behind. The failure is invisible: a mark
    nobody links to, or a row whose banner 404s.
    """
    listed = {repo for section in _sections().values() for repo in _repos(section)}
    assert listed == set(p.MANIFEST)


def test_di_table_lists_core_first_then_alphabetical_then_that_depends() -> None:
    """INVARIANT: the Dependency injection table opens with `modern-di`, ends with
    `that-depends`, and sorts every integration between them alphabetically.

    The two anchors carry meaning — the core users should start from, and the earlier
    framework that stays maintained — and alphabetical order in between is what makes a
    new integration slot in with no insertion-point decision to make. Appending the
    newest integration to the bottom is the natural move, and it lands past the anchor.
    """
    rows = _repos(_sections()["Dependency injection"])
    assert rows[0] == "modern-di"
    assert rows[-1] == "that-depends"
    assert rows[1:-1] == sorted(rows[1:-1])


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

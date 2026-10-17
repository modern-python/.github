import os
import pathlib
import re
import typing

import pytest


EM_DASH: typing.Final = "em dash (U+2014)"
EN_DASH: typing.Final = "en dash (U+2013)"
EMOJI_HEADING: typing.Final = "emoji in a heading"
READMES: typing.Final = ("README.md", "readme.md")
ROOT_FILES: typing.Final = (*READMES, "CONTEXT.md", "AGENTS.md")
DOCS_DIR: typing.Final = "docs"
UNSCANNED_DOCS_DIR: typing.Final = "agents"

_FENCE: typing.Final = re.compile(r"(`{3,}|~{3,})(.*)$")
_INLINE_CODE: typing.Final = re.compile(r"(?<!`)(`+)(?!`).+?(?<!`)\1(?!`)")
_LONE_DASH_CELL: typing.Final = re.compile(r"(?<=\|)[ \t]*[\u2013\u2014][ \t]*(?=\||$)")
_RANGE: typing.Final = re.compile(r"(?<=\d)\u2013(?=\d)")
_HEADING: typing.Final = re.compile(r" {0,3}#{1,6}(?:[ \t]|$)")
_EMOJI: typing.Final = re.compile(
    "[\U0001f000-\U0001faff\u2600-\u27bf\u2b00-\u2bff\u231a\u231b\u2328\u23cf\u23e9-\u23f3\u23f8-\u23fa"
    "\u3030\u303d\u3297\u3299\ufe0f]"
)


def _scanned_files(root: pathlib.Path) -> list[pathlib.Path]:
    # Listed rather than probed: on a case-insensitive filesystem `readme.md` "exists" beside `README.md`.
    found = [root / name for name in sorted(os.listdir(root)) if name in ROOT_FILES and (root / name).is_file()]
    docs = root / DOCS_DIR
    for dirpath, dirnames, filenames in os.walk(docs):
        dirnames[:] = sorted(
            name
            for name in dirnames
            if not name.startswith(".") and not (pathlib.Path(dirpath) == docs and name == UNSCANNED_DOCS_DIR)
        )
        found.extend(pathlib.Path(dirpath, name) for name in sorted(filenames) if name.endswith(".md"))
    return found


def _prose_lines(source: str) -> typing.Iterator[tuple[int, str]]:
    fence = ""
    for number, line in enumerate(source.splitlines(), start=1):
        stripped = line.strip()
        if fence:
            if stripped.startswith(fence) and not stripped.lstrip(fence[0]):
                fence = ""
            continue
        opening = _FENCE.match(stripped)
        if opening and not (opening[1][0] == "`" and "`" in opening[2]):
            fence = opening[1]
            continue
        yield number, _INLINE_CODE.sub("", line)


def _line_violations(line: str, *, is_readme: bool) -> list[str]:
    found = []
    if is_readme and _HEADING.match(line) and _EMOJI.search(line):
        found.append(EMOJI_HEADING)
    prose = _RANGE.sub("", _LONE_DASH_CELL.sub("", line) if "|" in line else line)
    found.extend(name for dash, name in (("\u2014", EM_DASH), ("\u2013", EN_DASH)) if dash in prose)
    return found


def prose_violations(root: pathlib.Path) -> list[tuple[str, int, str]]:
    return sorted(
        (file.relative_to(root).as_posix(), number, found)
        for file in _scanned_files(root)
        for number, line in _prose_lines(file.read_text(encoding="utf-8"))
        for found in _line_violations(line, is_readme=file.name in READMES and file.parent == root)
    )


def test_prose_has_no_long_dashes_and_readme_headings_have_no_emoji(pytestconfig: pytest.Config) -> None:
    """INVARIANT: the repo's prose Markdown has no em or en dash, and no README heading carries emoji.

    Every org repo fetches this file from `main` and runs it against its own tree (CI10), so a change
    here reaches all of them on their next run.

    Broken by pasting prose that uses either dash, or by restoring the emoji link headings that RM3
    replaced with a plain `## Links` list.

    Scanned: the root `README.md` (or `readme.md`), `CONTEXT.md` and `AGENTS.md`, and every `.md`
    under `docs/` except `docs/agents/`. Skipped: fenced code, inline code, a table cell that holds
    only a dash (an empty default), and an en dash between two digits (a range, such as `3\u20135`).
    """
    violations = prose_violations(pytestconfig.rootpath)

    assert violations == [], "\n".join(f"{file}:{number}: {found}" for file, number, found in violations)

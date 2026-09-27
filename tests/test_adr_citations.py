import ast
import os
import pathlib
import re
import typing

import pytest


ADR_DIR: typing.Final = "docs/adr/"
_CITATION: typing.Final = re.compile(r"docs/adr/\d{4}(?:-[a-z0-9-]+\.md)?")
NUMBER_PREFIX: typing.Final = "ADR-"
_NUMBER_CITATION: typing.Final = re.compile(NUMBER_PREFIX + r"\d{4}")
UNWALKED_DIR: typing.Final = "node_modules"
# mkdocs build output: a second copy of docs/, whose citations are the originals'.
_GENERATED_DIR: typing.Final = "site"
_SCANNED_SUFFIXES: typing.Final = (".py", ".md", ".toml")


def _scanned_files(root: pathlib.Path) -> list[pathlib.Path]:
    found: list[pathlib.Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            name for name in dirnames if not name.startswith(".") and name not in (UNWALKED_DIR, _GENERATED_DIR)
        )
        found.extend(pathlib.Path(dirpath, name) for name in sorted(filenames) if name.endswith(_SCANNED_SUFFIXES))
    return found


def _citations(file: pathlib.Path, source: str) -> set[str]:
    texts = [source]
    if file.suffix == ".py":
        # Adjacent literals are joined at parse time, so a path split across them is one string
        # in the AST and two fragments in the raw text.
        texts.extend(
            node.value
            for node in ast.walk(ast.parse(source))
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        )
    return {cited for text in texts for pattern in (_CITATION, _NUMBER_CITATION) for cited in pattern.findall(text)}


def _resolves(root: pathlib.Path, cited: str) -> bool:
    if cited.startswith(ADR_DIR):
        return (root / cited).is_file()
    return any((root / ADR_DIR).glob(f"{cited.removeprefix(NUMBER_PREFIX)}-*.md"))


def unresolved_citations(root: pathlib.Path) -> list[tuple[str, str]]:
    return sorted(
        (file.relative_to(root).as_posix(), cited)
        for file in _scanned_files(root)
        for cited in _citations(file, file.read_text(encoding="utf-8"))
        if not _resolves(root, cited)
    )


def test_every_adr_citation_in_the_repo_resolves(pytestconfig: pytest.Config) -> None:
    """INVARIANT: every ADR named in this repo resolves, by full path or by bare `ADR-NNNN` number.

    Every org repo fetches this file from `main` and runs it against its own tree (CI9), so a change
    here reaches all of them on their next run.

    Broken by renaming, renumbering or pruning an ADR without following its citations. The offline
    link gate reads Markdown links only, so a path in a docstring, a comment, a guard message or a
    `pyproject.toml` dependency rationale is otherwise checked by nothing, and neither is the bare
    number form, which is how most of them are written. A user who trips a guard is handed a link
    to follow.

    The number form is checked for existence only: a citation renumbered onto a *different* live
    ADR still resolves, and nothing here can know it now names the wrong decision.
    A bare `docs/adr/NNNN` path is reported outright: it names no file, so it would survive a
    rename or a drop unnoticed and point at whatever record holds that number next.
    """
    unresolved = unresolved_citations(pytestconfig.rootpath)

    assert unresolved == [], "\n".join(f"{file} cites {cited}" for file, cited in unresolved)

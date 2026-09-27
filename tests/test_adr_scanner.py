import pathlib

from test_adr_citations import ADR_DIR, NUMBER_PREFIX, UNWALKED_DIR, unresolved_citations


def test_a_citation_of_a_missing_adr_is_reported_with_its_citing_file(tmp_path: pathlib.Path) -> None:
    """The scanner is exercised against a known result, so an empty scan cannot pass as a green one."""
    (tmp_path / ADR_DIR).mkdir(parents=True)
    (tmp_path / ADR_DIR / "0001-kept.md").write_text("# kept\n", encoding="utf-8")
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "mod.py").write_text(
        f'"""Explained in {ADR_DIR}0001-kept.md and {ADR_DIR}9999-missing.md."""\n',
        encoding="utf-8",
    )

    assert unresolved_citations(tmp_path) == [("pkg/mod.py", f"{ADR_DIR}9999-missing.md")]


def test_a_citation_split_across_adjacent_string_literals_is_found(tmp_path: pathlib.Path) -> None:
    """Python joins adjacent literals at parse time, which is what the `nack` guard message relies on."""
    (tmp_path / "guard.py").write_text(
        f'MESSAGE = (\n    "See https://example.invalid/blob/main/{ADR_DIR}"\n    "0003-split.md."\n)\n',
        encoding="utf-8",
    )

    assert unresolved_citations(tmp_path) == [("guard.py", f"{ADR_DIR}0003-split.md")]


def test_a_citation_inside_a_hash_comment_is_found(tmp_path: pathlib.Path) -> None:
    """Comments never reach the AST, so the raw text is scanned as well."""
    (tmp_path / "graph.py").write_text(f"# The rule is one-way, see {ADR_DIR}0009-comment.md\n", encoding="utf-8")

    assert unresolved_citations(tmp_path) == [("graph.py", f"{ADR_DIR}0009-comment.md")]


def test_a_bare_adr_number_naming_no_file_is_reported(tmp_path: pathlib.Path) -> None:
    """A renumber leaves `ADR-NNNN` prose behind; only the path form was ever checked."""
    (tmp_path / ADR_DIR).mkdir(parents=True)
    (tmp_path / ADR_DIR / "0001-kept.md").write_text("# kept\n", encoding="utf-8")
    (tmp_path / "smoke.py").write_text(
        f"# the constraint {NUMBER_PREFIX}0001 records, unlike {NUMBER_PREFIX}9999\n", encoding="utf-8"
    )

    assert unresolved_citations(tmp_path) == [("smoke.py", f"{NUMBER_PREFIX}9999")]


def test_a_bare_adr_path_is_reported_even_when_the_adr_exists(tmp_path: pathlib.Path) -> None:
    """`docs/adr/NNNN` with no slug names nothing on disk, so a rename or a drop never breaks it."""
    (tmp_path / ADR_DIR).mkdir(parents=True)
    (tmp_path / ADR_DIR / "0002-kept.md").write_text("# kept\n", encoding="utf-8")
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "mod.py").write_text(
        f'"""Argued in {ADR_DIR}0002 and {ADR_DIR}0002-kept.md."""\n', encoding="utf-8"
    )

    assert unresolved_citations(tmp_path) == [("pkg/mod.py", f"{ADR_DIR}0002")]


def test_a_citation_outside_python_is_found(tmp_path: pathlib.Path) -> None:
    """`pyproject.toml` explains dependency floors by citing ADRs, and Markdown cites them in prose."""
    (tmp_path / ADR_DIR).mkdir(parents=True)
    (tmp_path / "pyproject.toml").write_text(f"# see {ADR_DIR}0002-floor.md\ndeps = []\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text(f"Read {NUMBER_PREFIX}0004 before editing.\n", encoding="utf-8")

    assert unresolved_citations(tmp_path) == [
        ("AGENTS.md", f"{NUMBER_PREFIX}0004"),
        ("pyproject.toml", f"{ADR_DIR}0002-floor.md"),
    ]


def test_a_tree_with_no_citations_and_no_adr_directory_reports_nothing(tmp_path: pathlib.Path) -> None:
    (tmp_path / "plain.py").write_text("X = 1\n", encoding="utf-8")

    assert unresolved_citations(tmp_path) == []


def test_files_under_dot_directories_are_not_scanned(tmp_path: pathlib.Path) -> None:
    """A virtualenv or a cache is not this repo's citations."""
    (tmp_path / ".venv" / "lib").mkdir(parents=True)
    (tmp_path / ".venv" / "lib" / "vendored.py").write_text(f"# {ADR_DIR}0001-elsewhere.md\n", encoding="utf-8")
    (tmp_path / UNWALKED_DIR).mkdir()
    (tmp_path / UNWALKED_DIR / "dep.py").write_text(f"# {ADR_DIR}0002-elsewhere.md\n", encoding="utf-8")

    assert unresolved_citations(tmp_path) == []

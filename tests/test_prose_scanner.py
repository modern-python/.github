import pathlib

from test_prose import DOCS_DIR, EM_DASH, EMOJI_HEADING, EN_DASH, prose_violations


def _write(root: pathlib.Path, relative: str, text: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_dashes_in_every_prose_file_are_reported_with_their_line(tmp_path: pathlib.Path) -> None:
    """The scanner is exercised against a known result, so an empty scan cannot pass as a green one."""
    _write(tmp_path, "README.md", "# pkg\n\nFast \u2014 and small.\n")
    _write(tmp_path, "CONTEXT.md", "A term \u2013 its meaning.\n")
    _write(tmp_path, "AGENTS.md", "ok\nRead this \u2014 first.\n")
    _write(tmp_path, "docs/guide/usage.md", "Use it \u2014 well.\n")
    _write(tmp_path, f"{DOCS_DIR}/adr/0001-choice.md", "We chose \u2014 this.\n")

    assert prose_violations(tmp_path) == [
        ("AGENTS.md", 2, EM_DASH),
        ("CONTEXT.md", 1, EN_DASH),
        ("README.md", 3, EM_DASH),
        (f"{DOCS_DIR}/adr/0001-choice.md", 1, EM_DASH),
        ("docs/guide/usage.md", 1, EM_DASH),
    ]


def test_a_lowercase_readme_is_scanned(tmp_path: pathlib.Path) -> None:
    _write(tmp_path, "readme.md", "## \U0001f4e6 PyPI\n")

    assert prose_violations(tmp_path) == [("readme.md", 1, EMOJI_HEADING)]


def test_an_emoji_in_a_readme_heading_is_reported(tmp_path: pathlib.Path) -> None:
    _write(tmp_path, "README.md", "# pkg\n\n## \U0001f4e6 [PyPI](https://pypi.org/project/pkg/)\n\n## \u2b50 Stars\n")

    assert prose_violations(tmp_path) == [("README.md", 3, EMOJI_HEADING), ("README.md", 5, EMOJI_HEADING)]


def test_an_emoji_outside_a_heading_or_outside_the_readme_is_allowed(tmp_path: pathlib.Path) -> None:
    """RM3 is about the README outline that GitHub and PyPI show, not emoji in general."""
    _write(tmp_path, "README.md", "# pkg\n\nShips fast \U0001f680\n")
    _write(tmp_path, "docs/index.md", "## \U0001f680 Fast\n")

    assert prose_violations(tmp_path) == []


def test_fenced_code_is_skipped(tmp_path: pathlib.Path) -> None:
    _write(
        tmp_path,
        "README.md",
        "```python\nx = 1  # a \u2014 b\n```\n\n~~~~\n```\n# \U0001f4e6 not a heading\n~~~~\nAfter \u2014 fence.\n",
    )

    assert prose_violations(tmp_path) == [("README.md", 9, EM_DASH)]


def test_a_fence_indented_inside_a_list_item_is_skipped(tmp_path: pathlib.Path) -> None:
    _write(tmp_path, "docs/index.md", "- step\n\n    ```bash\n    echo a \u2014 b\n    ```\n")

    assert prose_violations(tmp_path) == []


def test_inline_code_is_skipped(tmp_path: pathlib.Path) -> None:
    _write(tmp_path, "AGENTS.md", "Run `a \u2014 b` and ``c ` \u2013 d`` then \u2014 stop.\n")

    assert prose_violations(tmp_path) == [("AGENTS.md", 1, EM_DASH)]


def test_a_table_cell_holding_only_a_dash_is_allowed(tmp_path: pathlib.Path) -> None:
    """A lone dash marks an empty default; a dash inside a cell's prose is still reported."""
    _write(
        tmp_path,
        "docs/config.md",
        "| Name | Default |\n|---|---|\n| `a` | \u2014 |\n| `b` |\u2013|\n| `c` | none \u2014 unset |\n",
    )

    assert prose_violations(tmp_path) == [("docs/config.md", 5, EM_DASH)]


def test_an_en_dash_between_digits_is_a_range_and_allowed(tmp_path: pathlib.Path) -> None:
    """A range is the en dash's own job; the em dash has no such use, and a spaced en dash is a pause."""
    _write(tmp_path, "docs/index.md", "Retries 3\u20135 times on 3.11\u20133.14.\nSee 3 \u2013 5.\nSee 3\u20145.\n")

    assert prose_violations(tmp_path) == [("docs/index.md", 2, EN_DASH), ("docs/index.md", 3, EM_DASH)]


def test_agent_skill_docs_generated_site_and_other_files_are_not_scanned(tmp_path: pathlib.Path) -> None:
    """Only the root prose files and docs/ are scanned, and docs/agents/ is left out."""
    _write(tmp_path, "docs/agents/domain.md", "a \u2014 b\n")
    _write(tmp_path, "site/index.md", "a \u2014 b\n")
    _write(tmp_path, "CHANGELOG.md", "a \u2014 b\n")
    _write(tmp_path, "pkg/notes.md", "a \u2014 b\n")
    _write(tmp_path, "docs/notes.txt", "a \u2014 b\n")

    assert prose_violations(tmp_path) == []


def test_a_tree_with_no_prose_files_reports_nothing(tmp_path: pathlib.Path) -> None:
    _write(tmp_path, "pkg/mod.py", "X = '\u2014'\n")

    assert prose_violations(tmp_path) == []

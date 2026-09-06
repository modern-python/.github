"""Census of the invariant tests themselves, and of what the repo's prose cites.

An `INVARIANT:` docstring states the claim on line 1 and what breaks it in the second
paragraph; the claim alone is a label. Citations are the only pointers left now that
there is no capability page, so they have to resolve — and `mkdocs build --strict`
sees none of them, because they are inline code, not links, and the Markdown that
carries most of them sits outside `docs/`.
"""

import ast
import io
import pathlib
import re
import tokenize

_REPO_ROOT = pathlib.Path(__file__).parent.parent
_SOURCE_DIRS = ("tests", "brand")
_SKIPPED = (".venv", "site", "node_modules")

_INVARIANT = "INVARIANT:"
_MIN_PARAGRAPHS = 2

# A bare test-name citation: not part of a module path, and not an identifier fragment.
_TEST_NAME = re.compile(r"(?<![\w/])test_[a-z0-9_]+(?!\.py)\b")
_TEST_PATH = re.compile(r"\btests/[a-z0-9_]+\.py\b")
_ADR_PATH = re.compile(r"\bdocs/adr/[0-9]{4}-[a-z0-9-]+\.md\b")


def _source_files() -> list[pathlib.Path]:
    return sorted(
        path
        for directory in _SOURCE_DIRS
        for path in (_REPO_ROOT / directory).rglob("*.py")
    )


def _markdown_files() -> list[pathlib.Path]:
    return sorted(
        path
        for path in _REPO_ROOT.rglob("*.md")
        if not any(part in _SKIPPED for part in path.parts)
    )


def _test_functions() -> list[tuple[pathlib.Path, ast.FunctionDef | ast.AsyncFunctionDef]]:
    found = []
    for path in _source_files():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        found.extend(
            (path, node)
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        )
    return found


def _prose(path: pathlib.Path) -> str:
    """Everything in a file that is prose rather than code.

    For Python that means docstrings, string literals, and comments — never the
    ``def`` lines, or every definition would trivially satisfy its own citation.
    """
    source = path.read_text(encoding="utf-8")
    if path.suffix != ".py":
        return source
    tree = ast.parse(source)
    strings = [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    ]
    comments = [
        token.string
        for token in tokenize.generate_tokens(io.StringIO(source).readline)
        if token.type == tokenize.COMMENT
    ]
    return "\n".join([*strings, *comments])


def test_every_invariant_states_what_breaks_it() -> None:
    marked = [
        (path, node)
        for path, node in _test_functions()
        if (ast.get_docstring(node) or "").startswith(_INVARIANT)
    ]
    assert marked, "no test carries an INVARIANT: docstring; the convention is not in use"

    bare = sorted(
        f"{path.relative_to(_REPO_ROOT)}::{node.name}"
        for path, node in marked
        if len(
            [
                part
                for part in (ast.get_docstring(node) or "").split("\n\n")
                if part.strip()
            ]
        )
        < _MIN_PARAGRAPHS
    )
    assert not bare, f"INVARIANT tests with no 'what breaks it' paragraph: {bare}"


def test_cited_tests_and_adrs_resolve() -> None:
    names = {node.name for _, node in _test_functions()}
    cited, dangling = 0, []

    for path in [*_source_files(), *_markdown_files()]:
        prose = _prose(path)
        relative = path.relative_to(_REPO_ROOT)
        for name in _TEST_NAME.findall(prose):
            cited += 1
            if name not in names:
                dangling.append(f"{relative}: {name}")
        for cited_path in [*_TEST_PATH.findall(prose), *_ADR_PATH.findall(prose)]:
            cited += 1
            if not (_REPO_ROOT / cited_path).is_file():
                dangling.append(f"{relative}: {cited_path}")

    assert cited, "nothing cites a test or an ADR; this census would pass vacuously"
    assert not dangling, f"citations that do not resolve: {sorted(dangling)}"

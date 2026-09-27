import datetime
import pathlib
import typing

import pytest

from conformance.__main__ import PROFILE, profile_rows, published_from, render, with_release_consistency
from conformance.checks import AGENTS_PARAGRAPHS, REGISTRY, TS6_BECOMES_MUST, Metadata, Repo, Status, evaluate
from conformance.standard import STANDARD, Exemption, exemptions, requirement_ids


_NAME: typing.Final = "sample-lib"
_BEFORE_MUST: typing.Final = TS6_BECOMES_MUST - datetime.timedelta(days=1)
_MATRIX: typing.Final = '["3.11", "3.12", "3.13", "3.14", "3.14t"]'

_PYPROJECT: typing.Final = f"""\
[project]
name = "{_NAME}"
description = "Sample library for the conformance tests"
requires-python = ">=3.11,<4"
license = "MIT"
keywords = ["python", "di"]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    "Programming Language :: Python :: Free Threading :: 2 - Beta",
    "Typing :: Typed",
]
dependencies = ["anyio>=4"]
version = "0"

[project.urls]
Homepage = "https://modern-python.org"
Repository = "https://github.com/modern-python/{_NAME}"
Issues = "https://github.com/modern-python/{_NAME}/issues"
Changelog = "https://github.com/modern-python/{_NAME}/releases"

[dependency-groups]
dev = ["pytest", "pytest-cov"]
lint = ["ruff", "ty", "eof-fixer"]

[build-system]
requires = ["uv_build"]
build-backend = "uv_build"

[tool.ruff]
fix = true
unsafe-fixes = true
line-length = 120

[tool.ruff.lint]
select = ["ALL"]
ignore = [
    "D1",     # reason
    "D203",   # reason
    "D213",   # reason
    "COM812", # reason
    "ISC001", # reason
    "CPY001", # reason
    "FBT",    # reason
    "TCH",    # reason
]
isort.lines-after-imports = 2
isort.no-lines-before = ["standard-library", "local-folder"]

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.coverage.report]
fail_under = 100
exclude_also = ["if typing.TYPE_CHECKING:"]
"""

_JUSTFILE: typing.Final = """\
install:
    uv lock --upgrade
    uv sync --all-extras --frozen --group lint

lint:
    uv run eof-fixer .
    uv run ruff format
    uv run ruff check --fix
    uv run ty check

lint-ci:
    uv run eof-fixer . --check
    uv run ruff format --check
    uv run ruff check --no-fix
    uv run ty check

test *args:
    uv run --no-sync pytest {{ args }}

test-ci:
    uv run --no-sync pytest --cov=. --cov-report xml

publish:
    uv version $GITHUB_REF_NAME
    uv build
    uv publish
"""

_CHECKS: typing.Final = f"""\
on:
  workflow_call: {{}}
jobs:
  lint:
    steps:
      - run: uv python pin 3.11
      - run: just install lint-ci
  pytest:
    strategy:
      fail-fast: false
      matrix:
        python-version: {_MATRIX}
    steps:
      - run: just install
      - run: just test-ci
  floors:
    if: github.event_name != 'schedule'
    strategy:
      matrix:
        python-version: {_MATRIX}
    steps:
      - run: uv sync --resolution lowest-direct --no-build
  links:
    steps:
      - uses: lycheeverse/lychee-action@v2
        with:
          args: --offline --remap x
"""

_CI: typing.Final = """\
on:
  push:
    branches:
      - main
  pull_request: {}
concurrency:
  group: x
  cancel-in-progress: true
jobs:
  checks:
    uses: ./.github/workflows/_checks.yml
"""

_SCHEDULED: typing.Final = """\
on:
  schedule:
    - cron: "28 6 * * *"
  workflow_dispatch: {}
jobs:
  checks:
    uses: ./.github/workflows/_checks.yml
  report-failure:
    steps:
      - run: echo open or update tracking issue
"""

_RELEASE: typing.Final = """\
on:
  push:
    tags:
      - '[0-9]+.[0-9]+.[0-9]+'
      - '[0-9]+.[0-9]+.[0-9]+[a-z]+[0-9]+'
permissions:
  contents: write
  id-token: write
jobs:
  release:
    environment: pypi
    steps:
      - uses: astral-sh/setup-uv@v7
      - run: just publish
      - uses: softprops/action-gh-release@v3
        with:
          generate_release_notes: true
"""


def _write_repo(root: pathlib.Path) -> pathlib.Path:
    files = {
        "pyproject.toml": _PYPROJECT,
        "justfile": _JUSTFILE,
        ".github/workflows/_checks.yml": _CHECKS,
        ".github/workflows/ci.yml": _CI,
        ".github/workflows/scheduled.yml": _SCHEDULED,
        ".github/workflows/release.yml": _RELEASE,
        "CLAUDE.md": "@AGENTS.md\n",
        "AGENTS.md": "\n\n".join(AGENTS_PARAGRAPHS) + "\n",
        "LICENSE": "MIT License\n",
        "README.md": "Sample library. [Docs](https://modern-python.org)\n",
        "sample_lib/__init__.py": "",
    }
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return root


def _metadata(**overrides: typing.Any) -> Metadata:
    values = {
        "description": "Sample library for the conformance tests",
        "homepage": "https://modern-python.org",
        "topics": ("python", "di"),
        "profile_row": "Sample library for the conformance tests",
        "pr_titles": ("feat: add a thing",),
    }
    return Metadata(**{**values, **overrides})


def _repo(
    root: pathlib.Path,
    *,
    metadata: Metadata | None = None,
    exemption: Exemption | None = None,
    today: datetime.date = _BEFORE_MUST,
    name: str = _NAME,
) -> Repo:
    return Repo(name=name, root=root, metadata=metadata or _metadata(), exemption=exemption, today=today)


def _status(repo: Repo, requirement: str) -> Status:
    return next(finding.status for finding in evaluate(repo) if finding.requirement == requirement)


def _replace(path: pathlib.Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old, new), encoding="utf-8")


@pytest.fixture
def sample(tmp_path: pathlib.Path) -> pathlib.Path:
    return _write_repo(tmp_path / _NAME)


def test_a_conforming_repo_passes_every_check(sample: pathlib.Path) -> None:
    failures = [finding for finding in evaluate(_repo(sample)) if finding.status is not Status.PASS]
    assert failures == []


def test_every_check_names_a_requirement_of_the_standard() -> None:
    ids = set(requirement_ids(STANDARD.read_text(encoding="utf-8")))
    assert set(REGISTRY) | {"CI6", "TS6", "RL5", "RL6"} <= ids


@pytest.mark.parametrize(
    ("path", "old", "new", "requirement"),
    [
        ("pyproject.toml", 'testpaths = ["tests"]', "", "TS1"),
        ("pyproject.toml", '"tests/**" = ["S101"]', '"tests/*.py" = ["S101"]', "RF1"),
        ("pyproject.toml", '    "TCH",    # reason\n', '    "TCH",    # reason\n    "ANN",\n', "RF2"),
        ("pyproject.toml", 'exclude_also = ["if typing.TYPE_CHECKING:"]', 'exclude_also = ["except ImportError:"]', "TS5"),
        ("pyproject.toml", '"Typing :: Typed",\n', '"Typing :: Typed",\n    "License :: OSI Approved",\n', "MD4"),
        ("justfile", "uv run ruff check --no-fix", "uv run ruff check", "JF1"),
        (".github/workflows/_checks.yml", "uv python pin 3.11", "uv python pin 3.13", "CI4"),
        (".github/workflows/_checks.yml", "--no-build", "", "CI6"),
        ("AGENTS.md", "`just --list`, or read it.", "Run `just --list`.", "FL2"),
        ("README.md", "https://modern-python.org", "docs/index.md", "RM1"),
    ],
)
def test_a_broken_requirement_fails(
    sample: pathlib.Path, path: str, old: str, new: str, requirement: str
) -> None:
    _replace(sample / path, old, new)
    assert _status(_repo(sample), requirement) is Status.FAIL


def test_topics_that_differ_from_keywords_fail(sample: pathlib.Path) -> None:
    assert _status(_repo(sample, metadata=_metadata(topics=("python", "ioc"))), "MD3") is Status.FAIL


def test_a_misspelt_shared_topic_fails(sample: pathlib.Path) -> None:
    _replace(sample / "pyproject.toml", 'keywords = ["python", "di"]', 'keywords = ["python", "async"]')
    assert _status(_repo(sample, metadata=_metadata(topics=("python", "async"))), "MD2") is Status.FAIL


def test_a_bare_pragma_warns_until_the_date_and_fails_after(sample: pathlib.Path) -> None:
    (sample / "sample_lib" / "__init__.py").write_text("x = 1  # pragma: no cover\n", encoding="utf-8")
    assert _status(_repo(sample), "TS6") is Status.WARN
    assert _status(_repo(sample, today=TS6_BECOMES_MUST), "TS6") is Status.FAIL


def test_a_reasoned_pragma_passes(sample: pathlib.Path) -> None:
    (sample / "sample_lib" / "__init__.py").write_text("x = 1  # pragma: no cover - never imported\n", encoding="utf-8")
    assert _status(_repo(sample, today=TS6_BECOMES_MUST), "TS6") is Status.PASS


def test_a_floors_matrix_that_drops_an_entry_warns(sample: pathlib.Path) -> None:
    checks = sample / ".github" / "workflows" / "_checks.yml"
    head, floors = checks.read_text(encoding="utf-8").split("  floors:")
    checks.write_text(head + "  floors:" + floors.replace(_MATRIX, '["3.11", "3.12", "3.13", "3.14"]'), encoding="utf-8")
    assert _status(_repo(sample), "CI6") is Status.WARN


def test_a_repo_without_runtime_dependencies_needs_no_floors_job(sample: pathlib.Path) -> None:
    _replace(sample / "pyproject.toml", 'dependencies = ["anyio>=4"]\n', "")
    checks = sample / ".github" / "workflows" / "_checks.yml"
    text = checks.read_text(encoding="utf-8")
    checks.write_text(text.split("  floors:")[0] + "  links:" + text.split("  links:")[1], encoding="utf-8")
    assert _status(_repo(sample), "CI6") is Status.PASS


def test_an_exemption_turns_a_failure_into_exempt(sample: pathlib.Path) -> None:
    _replace(sample / "pyproject.toml", 'testpaths = ["tests"]', "")
    whole_core = Exemption(ids=frozenset({"TS2"}), whole_core=True)
    assert _status(_repo(sample, exemption=whole_core), "TS1") is Status.EXEMPT


def test_a_free_threading_exemption_drops_the_t_entry_from_the_expectations(sample: pathlib.Path) -> None:
    _replace(sample / ".github" / "workflows" / "_checks.yml", _MATRIX, '["3.11", "3.12", "3.13", "3.14"]')
    _replace(sample / "pyproject.toml", '    "Programming Language :: Python :: Free Threading :: 2 - Beta",\n', "")
    repo = _repo(sample, exemption=Exemption(ids=frozenset({"PV1"}), whole_core=False))
    assert {_status(repo, requirement) for requirement in ("PV1", "PV2", "MD4")} == {Status.PASS}


def test_release_yml_drift_fails_but_action_pins_do_not(tmp_path: pathlib.Path) -> None:
    same = _repo(_write_repo(tmp_path / "a"), name="a")
    bumped_root = _write_repo(tmp_path / "b")
    _replace(bumped_root / ".github" / "workflows" / "release.yml", "setup-uv@v7", "setup-uv@v8.2.0")
    drifted_root = _write_repo(tmp_path / "c")
    _replace(drifted_root / ".github" / "workflows" / "release.yml", "      - run: just publish\n", "      - run: just test\n      - run: just publish\n")
    repos = [same, _repo(bumped_root, name="b"), _repo(drifted_root, name="c")]
    results: dict[str, list] = {repo.name: [] for repo in repos}
    with_release_consistency(repos, results)
    assert [results[name][0].status for name in ("a", "b", "c")] == [Status.PASS, Status.PASS, Status.FAIL]


def test_the_exemptions_table_parses() -> None:
    table = exemptions(STANDARD.read_text(encoding="utf-8"))
    assert table["that-depends"].covers("TS1")
    assert not table["that-depends"].covers("TS2")
    assert table["modern-di-arq"].covers("PV1")
    assert not table["modern-di-arq"].covers("TS1")
    assert table["semvertag"].covers("RL5")


def test_the_profile_lists_a_row_per_repo() -> None:
    rows = profile_rows(PROFILE.read_text(encoding="utf-8"))
    assert rows["modern-di"] == "Powerful dependency-injection framework with IoC container and scopes"


def test_the_report_lists_only_problems(sample: pathlib.Path) -> None:
    _replace(sample / "pyproject.toml", 'testpaths = ["tests"]', "")
    report = render(_NAME, evaluate(_repo(sample)))
    assert "[TS1](https://modern-python.org/standard/#TS1) | FAIL" in report
    assert "TL1" not in report
    assert report.startswith(f"## `{_NAME}`")


def test_a_pypi_name_clash_is_not_a_core_repo() -> None:
    assert published_from({"project_urls": {"Repository": "https://github.com/modern-python/modern-di"}}, "modern-di")
    assert not published_from({"home_page": "https://github.com/someone-else/chat-app", "project_urls": None}, "chat-app")


def test_a_pragma_mentioned_in_a_comment_line_is_not_a_pragma(sample: pathlib.Path) -> None:
    (sample / "sample_lib" / "__init__.py").write_text("# body that would need # pragma: no cover.\n", encoding="utf-8")
    assert _status(_repo(sample, today=TS6_BECOMES_MUST), "TS6") is Status.PASS

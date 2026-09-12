import datetime
import pathlib

import pytest

from census import python_releases, registry, report, rules
from census.snapshot import RepoSnapshot


_PYPROJECT = """
[project]
name = "demo-lib"
version = "0"
description = "Does one thing well"
license = "MIT"
requires-python = ">=3.12,<4"
keywords = ["python", "demo"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    "Typing :: Typed",
]

[project.urls]
Homepage = "https://modern-python.org"
Repository = "https://github.com/modern-python/demo-lib"
Issues = "https://github.com/modern-python/demo-lib/issues"
Changelog = "https://github.com/modern-python/demo-lib/releases"

[build-system]
requires = ["uv_build>=0.11,<1.0"]
build-backend = "uv_build"

[dependency-groups]
dev = ["pytest", "pytest-cov"]
lint = ["ruff", "ty", "eof-fixer"]

[tool.ruff]
fix = true
unsafe-fixes = true
line-length = 120

[tool.ruff.lint]
select = ["ALL"]
ignore = ["D1", "D203", "D213", "COM812", "ISC001", "CPY001", "FBT", "TCH"]
isort.lines-after-imports = 2
isort.no-lines-before = ["standard-library", "local-folder"]

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101"]
"""

_JUSTFILE = """default: install lint test

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
    uv run --no-sync pytest --cov=. --cov-report term-missing --cov-report xml --cov-fail-under=100

# Auth via PyPI Trusted Publishing (OIDC).
publish:
    rm -rf dist
    uv version $GITHUB_REF_NAME
    uv build
    uv publish
"""

_CI = """name: main
on:
  push:
    branches: [main]
  pull_request: {}
concurrency:
  group: ${{ github.head_ref || github.run_id }}
  cancel-in-progress: true
jobs:
  checks:
    uses: ./.github/workflows/_checks.yml
"""

_CHECKS = """name: checks
on:
  workflow_call: {}
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: []
  pytest:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13", "3.14", "3.14t"]
    steps: []
  links:
    runs-on: ubuntu-latest
    steps: []
"""

_SCHEDULED = """name: scheduled
on:
  schedule:
    - cron: "0 6 * * 1"
  workflow_dispatch: {}
jobs:
  checks:
    uses: ./.github/workflows/_checks.yml
"""

_RELEASE = """name: Release
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
    runs-on: ubuntu-latest
    environment: pypi
    steps:
      - run: just publish
"""

_AGENTS = """# AGENTS.md

`just` (task runner) and `uv` (package manager). The [`justfile`](justfile) is the source of
truth — `just --list`, or read it. The one thing it does not say: nothing.

Every link in `README.md` must be absolute: `https://github.com/modern-python/<repo>/blob/main/<path>`,
or `.../tree/main/<path>` for a directory. Never a relative path: `README.md` is also the PyPI long
description, and PyPI does not rewrite relative links, so a relative one 404s on the package page.
"""

_COMPLIANT_FILES = {
    "pyproject.toml": _PYPROJECT,
    "justfile": _JUSTFILE,
    "CLAUDE.md": "@AGENTS.md\n",
    "AGENTS.md": _AGENTS,
    "CONTEXT.md": "# demo-lib\n\nDoes one thing well.\n",
    "LICENSE": "MIT License\n\nCopyright (c) 2026\n",
    "README.md": "# demo-lib\n\nSee [docs](https://github.com/modern-python/demo-lib/blob/main/docs/index.md).\n",
    ".github/workflows/ci.yml": _CI,
    ".github/workflows/_checks.yml": _CHECKS,
    ".github/workflows/scheduled.yml": _SCHEDULED,
    ".github/workflows/release.yml": _RELEASE,
}

_CONTEXT = rules.Context(newest_python="3.14", profile_descriptions={"demo-lib": "Does one thing well"})


def _snapshot(**overrides: str | None) -> RepoSnapshot:
    files = {path: text for path, text in {**_COMPLIANT_FILES, **overrides}.items() if text is not None}
    return RepoSnapshot(
        name="demo-lib",
        files=files,
        description="Does one thing well",
        topics=("python", "demo"),
        homepage="https://modern-python.org",
    )


def test_compliant_repo_has_no_findings() -> None:
    assert report.run_census([_snapshot()], _CONTEXT) == []


@pytest.mark.parametrize(
    ("path", "content", "item", "fragment"),
    [
        ("CLAUDE.md", "# Notes\n", "claude-md", "exactly"),
        ("CLAUDE.md", None, "claude-md", "missing"),
        ("AGENTS.md", "# AGENTS.md\n\nnothing canonical here\n", "agents-paragraphs", "canonical paragraph"),
        ("CONTEXT.md", None, "context-md", "missing"),
        ("LICENSE", "Apache License\n", "license", "MIT"),
        ("README.md", '[guide](docs/guide.md) and <img src="logo.svg">', "readme-links", "relative link"),
        (".github/workflows/scheduled.yml", None, "ci-workflows", "scheduled.yml"),
        (".github/workflows/publish.yml", "on: release\njobs: {}\n", "ci-workflows", "publish.yml"),
        (
            ".github/workflows/release.yml",
            _RELEASE.replace("environment: pypi", "environment: prod"),
            "release-workflow",
            "pypi",
        ),
        (".github/workflows/_checks.yml", _CHECKS.replace(', "3.14t"', ""), "python-matrix", "free-threaded"),
        (".github/workflows/_checks.yml", _CHECKS.replace('"3.13", ', ""), "python-matrix", "lacks 3.13"),
        (".github/workflows/_checks.yml", _CHECKS.replace('"3.12"', "3.12"), "python-matrix", "quoted"),
    ],
)
def test_single_file_deviation_is_reported(path: str, content: str | None, item: str, fragment: str) -> None:
    findings = report.run_census([_snapshot(**{path: content})], _CONTEXT)
    assert {f.item for f in findings} == {item}
    assert any(fragment in f.message for f in findings)


@pytest.mark.parametrize(
    ("old", "new", "item", "fragment"),
    [
        ('"TCH"]', '"TCH", "G004"]', "ruff-config", "G004"),
        ('"TCH"]', '"TCH", "S101"]', "ruff-config", "S101 must be"),
        ('"D1", ', "", "ruff-config", "lacks D1"),
        ("line-length = 120", "line-length = 100", "ruff-config", "line-length"),
        ("line-length = 120", 'line-length = 120\ntarget-version = "py312"', "ruff-config", "target-version"),
        ('lint = ["ruff", "ty", "eof-fixer"]', 'lint = ["ruff", "ty"]', "lint-group", "eof-fixer"),
        ('version = "0"', 'version = "1.2.3"', "pyproject-metadata", "version"),
        (
            '"Typing :: Typed",',
            '"Typing :: Typed",\n    "License :: OSI Approved :: MIT License",',
            "pyproject-metadata",
            "License ::",
        ),
        ('license = "MIT"', 'license = "Apache-2.0"', "pyproject-metadata", "SPDX"),
        ('Changelog = "https://github.com/modern-python/demo-lib/releases"', "", "pyproject-metadata", "Changelog"),
        ('    "Programming Language :: Python :: 3.12",\n', "", "python-matrix", "classifiers"),
    ],
)
def test_pyproject_deviation_is_reported(old: str, new: str, item: str, fragment: str) -> None:
    assert old in _PYPROJECT
    findings = report.run_census([_snapshot(**{"pyproject.toml": _PYPROJECT.replace(old, new)})], _CONTEXT)
    assert {f.item for f in findings} == {item}
    assert any(fragment in f.message for f in findings)


def test_trailing_period_in_description_is_reported_on_both_surfaces() -> None:
    pyproject = _PYPROJECT.replace('description = "Does one thing well"', 'description = "Does one thing well."')
    findings = report.run_census([_snapshot(**{"pyproject.toml": pyproject})], _CONTEXT)
    assert {f.item for f in findings} == {"pyproject-metadata", "description-surfaces"}
    assert any("trailing period" in f.message for f in findings)


def test_coverage_gate_in_pyproject_is_the_wrong_home() -> None:
    pyproject = _PYPROJECT + "\n[tool.coverage.report]\nfail_under = 100\n"
    justfile = _JUSTFILE.replace(" --cov-fail-under=100", "")
    findings = report.run_census([_snapshot(**{"pyproject.toml": pyproject, "justfile": justfile})], _CONTEXT)
    assert {f.item for f in findings} == {"coverage-gate-home"}
    assert len(findings) == 2  # noqa: PLR2004


def test_missing_gate_everywhere_is_two_findings() -> None:
    justfile = _JUSTFILE.replace(" --cov-fail-under=100", "")
    findings = report.run_census([_snapshot(justfile=justfile)], _CONTEXT)
    assert {f.item for f in findings} == {"coverage-gate", "coverage-gate-home"}


def test_justfile_recipe_contracts() -> None:
    justfile = _JUSTFILE.replace("uv run ruff check --no-fix\n", "").replace(
        "uv publish", "uv publish --token $PYPI_TOKEN"
    )
    findings = report.run_census([_snapshot(justfile=justfile)], _CONTEXT)
    messages = [f.message for f in findings if f.item == "justfile-recipes"]
    assert any("lint-ci" in m and "ruff check --no-fix" in m for m in messages)
    assert any("token" in m for m in messages)


def test_justfile_parser_handles_dependencies_and_comments() -> None:
    recipes = rules.parse_justfile(
        "# comment\n"
        "test *args: down && down\n"
        "    docker compose run app uv run pytest {{ args }}\n"
        "\n"
        "build:\n"
        "    docker compose build\n",
    )
    assert set(recipes) == {"test", "build"}
    assert "pytest {{ args }}" in recipes["test"].text


def test_exempted_extra_ignore_is_allowed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(registry.EXTRA_IGNORES, "demo-lib", frozenset({"ANN401"}))
    pyproject = _PYPROJECT.replace('"TCH"]', '"TCH", "ANN401"]')
    assert report.run_census([_snapshot(**{"pyproject.toml": pyproject})], _CONTEXT) == []


def test_subset_repo_skips_library_only_items(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(registry, "SUBSET_REPOS", frozenset({"demo-lib"}))
    justfile = _JUSTFILE.split("# Auth via", maxsplit=1)[0]
    files = {
        "pyproject.toml": _PYPROJECT,
        "justfile": justfile,
        ".github/workflows/release.yml": None,
        ".github/workflows/scheduled.yml": None,
    }
    assert report.run_census([_snapshot(**files)], _CONTEXT) == []


def test_whole_repo_exemption_keeps_only_the_coverage_gate(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(registry.EXEMPTIONS, "demo-lib", registry.CORE_ITEMS - {"coverage-gate"})
    files = {path: None for path in _COMPLIANT_FILES if path != "pyproject.toml"}
    findings = report.run_census([_snapshot(**files)], _CONTEXT)
    assert [f.item for f in findings] == ["coverage-gate"]


def test_description_surfaces_compare_three_places() -> None:
    context = rules.Context(newest_python="3.14", profile_descriptions={"demo-lib": "Something else"})
    findings = report.run_census([_snapshot()], context)
    assert [f.item for f in findings] == ["description-surfaces"]
    assert "profile row" in findings[0].message


def test_local_snapshot_without_github_metadata_skips_metadata_rules() -> None:
    snapshot = RepoSnapshot(name="demo-lib", files=_COMPLIANT_FILES)
    assert report.run_census([snapshot], rules.Context(newest_python="3.14")) == []


def test_shared_checks_workflow_satisfies_ci_and_matrix() -> None:
    ci = _CI.replace("./.github/workflows/_checks.yml", "modern-python/.github/.github/workflows/checks.yml@main")
    files = {".github/workflows/ci.yml": ci, ".github/workflows/_checks.yml": None}
    assert report.run_census([_snapshot(**files)], _CONTEXT) == []


def test_newest_cycle_ignores_unreleased_cycles() -> None:
    payload = [
        {"cycle": "3.15", "releaseDate": "2026-10-01"},
        {"cycle": "3.14", "releaseDate": "2025-10-07"},
        {"cycle": "3.9", "releaseDate": "2020-10-05"},
    ]
    assert python_releases.newest_cycle_from_payload(payload, datetime.date(2026, 9, 12)) == "3.14"
    assert python_releases.newest_cycle_from_payload(payload, datetime.date(2026, 10, 1)) == "3.15"


def test_profile_descriptions_parse_real_profile() -> None:
    descriptions = report.profile_descriptions(pathlib.Path(__file__).parent.parent / "profile" / "README.md")
    assert descriptions["modern-di"] == "Powerful dependency-injection framework with IoC container and scopes"


def test_render_markdown_groups_by_repo() -> None:
    findings = [report.Finding(repo="b", item="x", message="m1"), report.Finding(repo="a", item="y", message="m2")]
    text = report.render_markdown(findings, 3)
    assert text.startswith("2 findings across 2 of 3 repos.")
    assert text.index("### a") < text.index("### b")


def test_gate_in_pytest_addopts_counts_as_a_gate_in_the_wrong_home() -> None:
    pyproject = _PYPROJECT + '\n[tool.pytest.ini_options]\naddopts = "--cov=. --cov-fail-under=100"\n'
    justfile = _JUSTFILE.replace(" --cov-fail-under=100", "")
    findings = report.run_census([_snapshot(**{"pyproject.toml": pyproject, "justfile": justfile})], _CONTEXT)
    assert {f.item for f in findings} == {"coverage-gate-home"}
    assert any("addopts" in f.message for f in findings)


def test_lowercase_readme_is_found() -> None:
    files = {"README.md": None, "readme.md": "# demo\n\n[guide](docs/guide.md)\n"}
    findings = report.run_census([_snapshot(**files)], _CONTEXT)
    assert [f.item for f in findings] == ["readme-links"]
    assert "relative link" in findings[0].message

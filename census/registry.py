import typing


ORG: typing.Final = "modern-python"

EXCLUDED_REPOS: typing.Final = frozenset({".github"})

SUBSET_REPOS: typing.Final = frozenset(
    {"fastapi-sqlalchemy-template", "litestar-sqlalchemy-template", "chat-app"},
)

SUBSET_ITEMS: typing.Final = frozenset(
    {
        "claude-md",
        "agents-paragraphs",
        "context-md",
        "license",
        "ruff-config",
        "lint-group",
        "justfile-recipes",
        "readme-links",
    },
)

CORE_ITEMS: typing.Final = SUBSET_ITEMS | frozenset(
    {
        "pyproject-metadata",
        "coverage-gate",
        "coverage-gate-home",
        "ci-workflows",
        "release-workflow",
        "python-matrix",
        "description-surfaces",
        "topics-keywords",
        "shared-pytest-job",
    },
)

EXEMPTIONS: typing.Final[dict[str, frozenset[str]]] = {
    "that-depends": CORE_ITEMS - {"coverage-gate"},
    "db-retry": frozenset({"shared-pytest-job"}),
    "faststream-redis-timers": frozenset({"shared-pytest-job"}),
    "faststream-concurrent-aiokafka": frozenset({"shared-pytest-job"}),
    "modern-di-arq": frozenset({"shared-pytest-job"}),
}

EXTRA_IGNORES: typing.Final[dict[str, frozenset[str]]] = {
    "faststream-outbox": frozenset({"ANN401"}),
    "faststream-redis-timers": frozenset({"ANN401"}),
    "fastapi-sqlalchemy-template": frozenset({"INP", "B008", "S105"}),
    "litestar-sqlalchemy-template": frozenset({"INP", "B008", "S105"}),
    "chat-app": frozenset({"INP", "B008", "S105"}),
}

CANONICAL_IGNORES: typing.Final = frozenset({"D1", "D203", "D213", "COM812", "ISC001", "CPY001", "FBT", "TCH"})

LINT_GROUP_TOOLS: typing.Final = frozenset({"ruff", "ty", "eof-fixer"})

RECIPES: typing.Final = ("install", "lint", "lint-ci", "test", "test-ci", "publish")

CANONICAL_PARAGRAPHS: typing.Final = (
    (
        "`just` (task runner) and `uv` (package manager). The [`justfile`](justfile) is the source of truth — "
        "`just --list`, or read it."
    ),
    (
        "Every link in `README.md` must be absolute: `https://github.com/modern-python/<repo>/blob/main/<path>`, "
        "or `.../tree/main/<path>` for a directory. Never a relative path: `README.md` is also the PyPI long "
        "description, and PyPI does not rewrite relative links, so a relative one 404s on the package page."
    ),
)

RELEASE_TAG_PATTERNS: typing.Final = frozenset({"[0-9]+.[0-9]+.[0-9]+", "[0-9]+.[0-9]+.[0-9]+[a-z]+[0-9]+"})

SHARED_CHECKS_WORKFLOW: typing.Final = "modern-python/.github/.github/workflows/checks.yml"

DESCRIPTION_MAX_LENGTH: typing.Final = 120
TOPICS_MAX: typing.Final = 12


def exempted_repos() -> frozenset[str]:
    return frozenset(EXEMPTIONS) | frozenset(EXTRA_IGNORES)


def applicable_items(repo: str) -> frozenset[str]:
    items = SUBSET_ITEMS if repo in SUBSET_REPOS else CORE_ITEMS
    return items - EXEMPTIONS.get(repo, frozenset())

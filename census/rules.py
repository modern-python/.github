import dataclasses
import re
import typing

import tomllib
import yaml

from census import registry
from census.snapshot import RepoSnapshot


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class Context:
    newest_python: str
    profile_descriptions: typing.Mapping[str, str] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class Recipe:
    name: str
    body: tuple[str, ...]

    @property
    def text(self) -> str:
        return "\n".join(self.body)


_RECIPE_HEADER: typing.Final = re.compile(r"^(?P<name>[A-Za-z0-9_-]+)(?P<params>[^:=]*):(?P<deps>.*)$")
_MARKDOWN_LINK: typing.Final = re.compile(r"\]\((?P<target>[^)\s]+)")
_HTML_SRC: typing.Final = re.compile(r'(?:src|href)="(?P<target>[^"]+)"')
_ABSOLUTE: typing.Final = re.compile(r"^(https?://|mailto:|#)")
_REQUIRES_FLOOR: typing.Final = re.compile(r">=\s*3\.(?P<minor>\d+)")
_PYTHON_CLASSIFIER: typing.Final = re.compile(r"^Programming Language :: Python :: 3\.(?P<minor>\d+)$")
_TOPIC: typing.Final = re.compile(r"^[a-z0-9][a-z0-9-]{0,49}$")
_DEP_NAME: typing.Final = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*")


def parse_justfile(text: str) -> dict[str, Recipe]:
    recipes: dict[str, Recipe] = {}
    current: str | None = None
    body: list[str] = []
    for line in text.splitlines():
        if line.startswith((" ", "\t")):
            if current is not None:
                body.append(line.strip())
            continue
        if current is not None:
            recipes[current] = Recipe(name=current, body=tuple(body))
            current, body = None, []
        if line.startswith("#") or not line.strip():
            continue
        if match := _RECIPE_HEADER.match(line):
            current = match.group("name")
    if current is not None:
        recipes[current] = Recipe(name=current, body=tuple(body))
    return recipes


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def _pyproject(snapshot: RepoSnapshot) -> dict[str, typing.Any] | None:
    text = snapshot.read("pyproject.toml")
    return None if text is None else tomllib.loads(text)


def _workflow(snapshot: RepoSnapshot, name: str) -> dict[str, typing.Any] | None:
    text = snapshot.read(f".github/workflows/{name}")
    if text is None:
        return None
    loaded = yaml.safe_load(text)
    return loaded if isinstance(loaded, dict) else None


def _triggers(workflow: dict[str, typing.Any]) -> typing.Any:  # noqa: ANN401
    return workflow.get("on", workflow.get(True))


def _dep_name(spec: str) -> str:
    match = _DEP_NAME.match(spec.strip())
    return match.group(0).lower().replace("_", "-") if match else spec


def uses_shared_checks(snapshot: RepoSnapshot) -> bool:
    workflow = _workflow(snapshot, "ci.yml")
    if workflow is None:
        return False
    return any(
        str(job.get("uses", "")).startswith(registry.SHARED_CHECKS_WORKFLOW)
        for job in workflow.get("jobs", {}).values()
        if isinstance(job, dict)
    )


def check_claude_md(snapshot: RepoSnapshot, _: Context) -> list[str]:
    text = snapshot.read("CLAUDE.md")
    if text is None:
        return ["CLAUDE.md is missing"]
    if text.strip() != "@AGENTS.md":
        return ["CLAUDE.md must contain exactly `@AGENTS.md`"]
    return []


def check_agents_paragraphs(snapshot: RepoSnapshot, _: Context) -> list[str]:
    text = snapshot.read("AGENTS.md")
    if text is None:
        return ["AGENTS.md is missing"]
    normalized = normalize_whitespace(text)
    return [
        f"AGENTS.md lacks the canonical paragraph starting `{paragraph[:40]}…`"
        for paragraph in registry.CANONICAL_PARAGRAPHS
        if normalize_whitespace(paragraph) not in normalized
    ]


def check_context_md(snapshot: RepoSnapshot, _: Context) -> list[str]:
    text = snapshot.read("CONTEXT.md")
    if text is None:
        return ["CONTEXT.md is missing"]
    if not text.lstrip().startswith("# "):
        return ["CONTEXT.md must open with a `# <name>` heading"]
    return []


def check_license(snapshot: RepoSnapshot, _: Context) -> list[str]:
    text = snapshot.read("LICENSE")
    if text is None:
        return ["LICENSE is missing"]
    if "MIT License" not in text:
        return ["LICENSE is not the MIT License"]
    return []


def check_lint_group(snapshot: RepoSnapshot, _: Context) -> list[str]:
    project = _pyproject(snapshot)
    if project is None:
        return ["pyproject.toml is missing"]
    group = project.get("dependency-groups", {}).get("lint")
    if not isinstance(group, list):
        return ["pyproject.toml has no `lint` dependency group"]
    present = {_dep_name(spec) for spec in group if isinstance(spec, str)}
    return [f"`lint` dependency group lacks {tool}" for tool in sorted(registry.LINT_GROUP_TOOLS - present)]


def _ignore_findings(snapshot: RepoSnapshot, lint: dict[str, typing.Any]) -> list[str]:
    findings = []
    actual = frozenset(lint.get("ignore", []))
    allowed_extra = registry.EXTRA_IGNORES.get(snapshot.name, frozenset())
    if missing := registry.CANONICAL_IGNORES - actual:
        findings.append(f"ruff ignore list lacks {', '.join(sorted(missing))}")
    if "S101" in actual:
        findings.append("S101 must be a `tests/**` per-file ignore, not a global one")
    if extra := actual - registry.CANONICAL_IGNORES - allowed_extra - {"S101"}:
        findings.append(f"ruff ignore list carries {', '.join(sorted(extra))} without an exemption")
    per_file = lint.get("per-file-ignores", {}) | lint.get("extend-per-file-ignores", {})
    if not any(key.startswith("tests/") and "S101" in rules for key, rules in per_file.items()):
        findings.append('per-file-ignores lacks `"tests/**" = ["S101"]`')
    return findings


def check_ruff_config(snapshot: RepoSnapshot, _: Context) -> list[str]:
    project = _pyproject(snapshot)
    if project is None:
        return ["pyproject.toml is missing"]
    ruff = project.get("tool", {}).get("ruff")
    if ruff is None:
        return ["pyproject.toml has no [tool.ruff] section"]
    findings = []
    expected_top = {"fix": True, "unsafe-fixes": True, "line-length": 120}
    findings.extend(
        f"[tool.ruff] {key} must be {value!r}" for key, value in expected_top.items() if ruff.get(key) != value
    )
    if "target-version" in ruff:
        findings.append("[tool.ruff] target-version must be omitted; ruff derives it from requires-python")
    lint = ruff.get("lint", {})
    if lint.get("select") != ["ALL"]:
        findings.append('[tool.ruff.lint] select must be ["ALL"]')
    findings.extend(_ignore_findings(snapshot, lint))
    isort = lint.get("isort", {})
    if isort.get("lines-after-imports") != 2:  # noqa: PLR2004
        findings.append("[tool.ruff.lint.isort] lines-after-imports must be 2")
    if isort.get("no-lines-before") != ["standard-library", "local-folder"]:
        findings.append('[tool.ruff.lint.isort] no-lines-before must be ["standard-library", "local-folder"]')
    return findings


_LINT_STEPS: typing.Final = ("eof-fixer .", "ruff format", "ruff check --fix", "ty check")
_LINT_CI_STEPS: typing.Final = ("eof-fixer . --check", "ruff format --check", "ruff check --no-fix", "ty check")
_PUBLISH_STEPS: typing.Final = ("uv version $GITHUB_REF_NAME", "uv build", "uv publish")


def _recipe_findings(recipes: dict[str, Recipe], name: str, steps: tuple[str, ...]) -> list[str]:
    recipe = recipes.get(name)
    if recipe is None:
        return []
    return [f"justfile `{name}` lacks `{step}`" for step in steps if step not in recipe.text]


def check_justfile_recipes(snapshot: RepoSnapshot, _: Context) -> list[str]:
    text = snapshot.read("justfile")
    if text is None:
        return ["justfile is missing (lowercase name)"]
    recipes = parse_justfile(text)
    required = (
        registry.RECIPES
        if snapshot.name not in registry.SUBSET_REPOS
        else tuple(r for r in registry.RECIPES if r != "publish")
    )
    findings = [f"justfile lacks recipe `{name}`" for name in required if name not in recipes]
    findings.extend(_recipe_findings(recipes, "lint", _LINT_STEPS))
    findings.extend(_recipe_findings(recipes, "lint-ci", _LINT_CI_STEPS))
    findings.extend(_recipe_findings(recipes, "publish", _PUBLISH_STEPS))
    if (publish := recipes.get("publish")) and "--token" in publish.text:
        findings.append("justfile `publish` must not pass a token; auth is Trusted Publishing")
    if (test := recipes.get("test")) and (
        "pytest" not in test.text or "{{ args }}" not in test.text.replace("{{args}}", "{{ args }}")
    ):
        findings.append("justfile `test` must run pytest and pass `{{ args }}` through")
    return findings


def _coverage_fail_under(project: dict[str, typing.Any]) -> object:
    coverage = project.get("tool", {}).get("coverage", {})
    return coverage.get("report", {}).get("fail_under")


def _pytest_addopts_gate(project: dict[str, typing.Any]) -> bool:
    addopts = project.get("tool", {}).get("pytest", {}).get("ini_options", {}).get("addopts", "")
    return "--cov-fail-under=100" in (addopts if isinstance(addopts, str) else " ".join(addopts))


def check_coverage_gate(snapshot: RepoSnapshot, _: Context) -> list[str]:
    project = _pyproject(snapshot) or {}
    recipes = parse_justfile(snapshot.read("justfile") or "")
    in_justfile = any("--cov-fail-under=100" in recipe.text for recipe in recipes.values())
    in_pyproject = _coverage_fail_under(project) == 100 or _pytest_addopts_gate(project)  # noqa: PLR2004
    return [] if in_justfile or in_pyproject else ["no 100% coverage gate anywhere"]


def check_coverage_gate_home(snapshot: RepoSnapshot, _: Context) -> list[str]:
    findings = []
    project = _pyproject(snapshot) or {}
    if _coverage_fail_under(project) is not None:
        findings.append("[tool.coverage.report] fail_under is set; the gate lives in `just test-ci` only")
    if _pytest_addopts_gate(project):
        findings.append("pytest addopts gate coverage on every run; the gate lives in `just test-ci` only")
    recipes = parse_justfile(snapshot.read("justfile") or "")
    if (test := recipes.get("test")) and "cov-fail-under" in test.text:
        findings.append("justfile `test` must not gate coverage")
    if (test_ci := recipes.get("test-ci")) and "--cov-fail-under=100" not in test_ci.text:
        findings.append("justfile `test-ci` must pass `--cov-fail-under=100`")
    return findings


def _metadata_project_findings(snapshot: RepoSnapshot, project: dict[str, typing.Any]) -> list[str]:
    findings = []
    meta = project.get("project", {})
    if meta.get("name") != snapshot.name:
        findings.append(f"[project] name must equal the repo name `{snapshot.name}`")
    if meta.get("version") != "0":
        findings.append('[project] version must be "0"; the tag sets the real one')
    if meta.get("license") != "MIT":
        findings.append('[project] license must be the SPDX string "MIT"')
    if project.get("build-system", {}).get("build-backend") != "uv_build":
        findings.append("[build-system] build-backend must be uv_build")
    description = meta.get("description", "")
    if not description:
        findings.append("[project] description is missing")
    elif len(description) > registry.DESCRIPTION_MAX_LENGTH or description.endswith("."):
        findings.append("[project] description must be at most 120 characters with no trailing period")
    if not meta.get("keywords"):
        findings.append("[project] keywords are missing")
    return findings


def check_pyproject_metadata(snapshot: RepoSnapshot, _: Context) -> list[str]:
    project = _pyproject(snapshot)
    if project is None:
        return ["pyproject.toml is missing"]
    findings = _metadata_project_findings(snapshot, project)
    meta = project.get("project", {})
    classifiers = meta.get("classifiers", [])
    for needle in ("Intended Audience :: Developers", "Typing :: Typed"):
        if needle not in classifiers:
            findings.append(f"classifiers lack `{needle}`")
    if not any(item.startswith("Development Status ::") for item in classifiers):
        findings.append("classifiers lack a `Development Status ::` entry")
    if any(item.startswith("License ::") for item in classifiers):
        findings.append("classifiers must not carry a `License ::` entry (PEP 639)")
    urls = meta.get("urls", {})
    expected_urls = {
        "Homepage": None,
        "Repository": f"https://github.com/{registry.ORG}/{snapshot.name}",
        "Issues": f"https://github.com/{registry.ORG}/{snapshot.name}/issues",
        "Changelog": f"https://github.com/{registry.ORG}/{snapshot.name}/releases",
    }
    for label, expected in expected_urls.items():
        if label not in urls:
            findings.append(f"[project.urls] lacks `{label}`")
        elif expected is not None and urls[label] != expected:
            findings.append(f"[project.urls] {label} must be {expected}")
    return findings


def check_ci_workflows(snapshot: RepoSnapshot, _: Context) -> list[str]:
    findings = []
    ci = _workflow(snapshot, "ci.yml")
    if ci is None:
        findings.append("ci.yml is missing")
    else:
        triggers = _triggers(ci) or {}
        if not isinstance(triggers, dict) or "pull_request" not in triggers or "push" not in triggers:
            findings.append("ci.yml must trigger on pull_request and push")
        if "concurrency" not in ci:
            findings.append("ci.yml must declare `concurrency` to cancel superseded runs")
    scheduled = _workflow(snapshot, "scheduled.yml")
    if scheduled is None:
        findings.append("scheduled.yml is missing")
    elif not isinstance(triggers := _triggers(scheduled), dict) or "schedule" not in triggers:
        findings.append("scheduled.yml must trigger on a schedule")
    if "publish.yml" in snapshot.workflow_names():
        findings.append("publish.yml is the retired release-published trigger; release.yml replaces it")
    if not uses_shared_checks(snapshot):
        checks = _workflow(snapshot, "_checks.yml")
        if checks is None:
            findings.append("neither the shared checks workflow nor a local _checks.yml is used")
        else:
            jobs = set(checks.get("jobs", {}))
            findings.extend(
                f"_checks.yml lacks the `{job}` job" for job in ("lint", "pytest", "links") if job not in jobs
            )
    return findings


def check_release_workflow(snapshot: RepoSnapshot, _: Context) -> list[str]:
    release = _workflow(snapshot, "release.yml")
    if release is None:
        return ["release.yml is missing"]
    findings = []
    triggers = _triggers(release) or {}
    tags = frozenset((triggers.get("push") or {}).get("tags") or []) if isinstance(triggers, dict) else frozenset()
    if tags != registry.RELEASE_TAG_PATTERNS:
        findings.append("release.yml must trigger on exactly the stable and pre-release tag patterns")
    permissions = release.get("permissions", {})
    if permissions.get("id-token") != "write" or permissions.get("contents") != "write":
        findings.append("release.yml must grant `id-token: write` and `contents: write`")
    jobs = [job for job in release.get("jobs", {}).values() if isinstance(job, dict)]
    if not any(job.get("environment") == "pypi" for job in jobs):
        findings.append("release.yml must run in the `pypi` environment")
    steps = [step for job in jobs for step in job.get("steps", []) if isinstance(step, dict)]
    if not any("just publish" in str(step.get("run", "")) for step in steps):
        findings.append("release.yml must run `just publish`")
    return findings


def _matrix_versions(checks: dict[str, typing.Any]) -> tuple[set[str], list[str]]:
    versions: set[str] = set()
    unquoted: list[str] = []
    for job in checks.get("jobs", {}).values():
        if not isinstance(job, dict):
            continue
        matrix = job.get("strategy", {}).get("matrix", {})
        candidates = list(matrix.get("python-version", []) or [])
        candidates.extend(entry.get("python-version") for entry in matrix.get("include", []) if isinstance(entry, dict))
        for candidate in candidates:
            if isinstance(candidate, float):
                unquoted.append(str(candidate))
            elif candidate is not None:
                versions.add(str(candidate))
    return versions, unquoted


def check_python_matrix(snapshot: RepoSnapshot, context: Context) -> list[str]:
    project = _pyproject(snapshot)
    if project is None:
        return ["pyproject.toml is missing"]
    requires = project.get("project", {}).get("requires-python", "")
    floor_match = _REQUIRES_FLOOR.search(requires)
    if floor_match is None:
        return ["requires-python must declare a `>=3.X` floor"]
    newest_minor = int(context.newest_python.split(".")[1])
    expected = {f"3.{minor}" for minor in range(int(floor_match.group("minor")), newest_minor + 1)}
    findings = []
    classifiers = {
        f"3.{match.group('minor')}"
        for item in project.get("project", {}).get("classifiers", [])
        if (match := _PYTHON_CLASSIFIER.match(item))
    }
    if classifiers != expected:
        findings.append(f"Python classifiers must list exactly {', '.join(sorted(expected))}")
    if uses_shared_checks(snapshot):
        return findings
    checks = _workflow(snapshot, "_checks.yml")
    if checks is None:
        return [*findings, "_checks.yml is missing; the matrix cannot be checked"]
    versions, unquoted = _matrix_versions(checks)
    if unquoted:
        findings.append(f"matrix python-version entries must be quoted strings; found {', '.join(unquoted)}")
    if missing := expected - versions:
        findings.append(f"pytest matrix lacks {', '.join(sorted(missing))}")
    if f"{context.newest_python}t" not in versions:
        findings.append(f"pytest matrix lacks the free-threaded build {context.newest_python}t")
    return findings


def _readme(snapshot: RepoSnapshot) -> str | None:
    return next((text for path, text in snapshot.files.items() if path.lower() == "readme.md"), None)


def check_readme_links(snapshot: RepoSnapshot, _: Context) -> list[str]:
    text = _readme(snapshot)
    if text is None:
        return ["README.md is missing"]
    targets = [match.group("target") for match in _MARKDOWN_LINK.finditer(text)]
    targets.extend(match.group("target") for match in _HTML_SRC.finditer(text))
    relative = sorted({target for target in targets if not _ABSOLUTE.match(target)})
    return [f"README.md has a relative link: {target}" for target in relative]


def check_description_surfaces(snapshot: RepoSnapshot, context: Context) -> list[str]:
    if snapshot.description is None:
        return []
    project = _pyproject(snapshot) or {}
    findings = []
    pyproject_description = project.get("project", {}).get("description")
    if pyproject_description != snapshot.description:
        findings.append("GitHub description and pyproject description differ")
    profile_description = context.profile_descriptions.get(snapshot.name)
    if profile_description is None:
        findings.append("repo has no row in the org profile")
    elif profile_description != snapshot.description:
        findings.append("GitHub description and org profile row differ")
    return findings


def check_topics_keywords(snapshot: RepoSnapshot, _: Context) -> list[str]:
    if snapshot.topics is None:
        return []
    findings = []
    if not snapshot.topics:
        findings.append("repo has no GitHub topics")
    if len(snapshot.topics) > registry.TOPICS_MAX:
        findings.append(f"repo has more than {registry.TOPICS_MAX} topics")
    findings.extend(
        f"topic `{topic}` is not lowercase-hyphenated" for topic in snapshot.topics if not _TOPIC.match(topic)
    )
    project = _pyproject(snapshot) or {}
    keywords = frozenset(project.get("project", {}).get("keywords", []))
    if keywords != frozenset(snapshot.topics):
        findings.append("pyproject keywords and GitHub topics differ")
    if not snapshot.homepage:
        findings.append("repo website field is empty; set the docs site or modern-python.org")
    return findings


RULES: typing.Final[dict[str, typing.Callable[[RepoSnapshot, Context], list[str]]]] = {
    "claude-md": check_claude_md,
    "agents-paragraphs": check_agents_paragraphs,
    "context-md": check_context_md,
    "license": check_license,
    "lint-group": check_lint_group,
    "ruff-config": check_ruff_config,
    "justfile-recipes": check_justfile_recipes,
    "coverage-gate": check_coverage_gate,
    "coverage-gate-home": check_coverage_gate_home,
    "pyproject-metadata": check_pyproject_metadata,
    "ci-workflows": check_ci_workflows,
    "release-workflow": check_release_workflow,
    "python-matrix": check_python_matrix,
    "readme-links": check_readme_links,
    "description-surfaces": check_description_surfaces,
    "topics-keywords": check_topics_keywords,
}

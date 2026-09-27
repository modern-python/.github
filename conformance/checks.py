import collections.abc
import dataclasses
import datetime
import enum
import pathlib
import re
import tomllib
import typing

import yaml
from trove_classifiers import classifiers as valid_classifiers

from conformance.standard import Exemption


NEWEST: typing.Final = "3.14"
TS6_BECOMES_MUST: typing.Final = datetime.date(2026, 11, 1)
VOCABULARY_SPELLINGS: typing.Final = {
    "ioc": "ioc-container",
    "async": "asyncio",
    "postgres": "postgresql",
    "dependency-injector": "dependency-injection",
    "command-line": "cli",
}
CANONICAL_IGNORES: typing.Final = ("D1", "D203", "D213", "COM812", "ISC001", "CPY001", "FBT", "TCH")
TAG_PATTERNS: typing.Final = frozenset({"[0-9]+.[0-9]+.[0-9]+", "[0-9]+.[0-9]+.[0-9]+[a-z]+[0-9]+"})
FIXED_RECIPES: typing.Final = ("install", "lint", "lint-ci", "test", "test-ci", "publish")
AGENTS_PARAGRAPHS: typing.Final = (
    "`just` (task runner) and `uv` (package manager). The [`justfile`](justfile) is the source of truth — "
    "`just --list`, or read it.",
    "Every link in `README.md` must be absolute: `https://github.com/modern-python/<repo>/blob/main/<path>`, "
    "or `.../tree/main/<path>` for a directory. Never a relative path: `README.md` is also the PyPI long "
    "description, and PyPI does not rewrite relative links, so a relative one 404s on the package page.",
)
UNCHECKED: typing.Final = ("JF3", "PV3", "FL3", "FL6", "RM2")
_CONVENTIONAL: typing.Final = re.compile(
    r"^(feat|fix|docs|chore|refactor|test|ci|build|perf|style|revert)(\([^)]+\))?!?: "
)
_PRAGMA: typing.Final = re.compile(r"#\s*pragma:\s*no\s*cover(.*)$")


class Status(enum.StrEnum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    EXEMPT = "exempt"


@dataclasses.dataclass(frozen=True, kw_only=True)
class Finding:
    requirement: str
    status: Status
    detail: str = ""


@dataclasses.dataclass(frozen=True, kw_only=True)
class Metadata:
    description: str
    homepage: str
    topics: tuple[str, ...]
    profile_row: str | None
    pr_titles: tuple[str, ...]


def _recipes(justfile: str) -> dict[str, str]:
    found: dict[str, str] = {}
    current = None
    for line in justfile.splitlines():
        header = re.match(r"^([a-z][\w-]*)(\s[^:]*)?:(?!=)", line)
        if header:
            current = header.group(1)
            found[current] = ""
        elif current and line.startswith((" ", "\t")):
            found[current] += line.strip() + "\n"
        elif line.strip() and not line.startswith("#"):
            current = None
    return found


def _load_workflow(path: pathlib.Path) -> dict[str, typing.Any]:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if True in data:
        data["on"] = data.pop(True)
    return data


def _names(requirements: collections.abc.Iterable[str]) -> set[str]:
    return {re.split(r"[\s\[<>=!~;]", item, maxsplit=1)[0].lower() for item in requirements}


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


class Repo:
    def __init__(
        self, *, name: str, root: pathlib.Path, metadata: Metadata, exemption: Exemption | None, today: datetime.date
    ) -> None:
        self.name = name
        self.root = root
        self.metadata = metadata
        self.exemption = exemption
        self.today = today
        self.pyproject_text = self.read("pyproject.toml")
        self.pyproject = tomllib.loads(self.pyproject_text)
        self.project = self.pyproject.get("project", {})
        self.tool = self.pyproject.get("tool", {})
        self.groups = self.pyproject.get("dependency-groups", {})
        self.recipes = _recipes(self.read("justfile"))
        workflows = root / ".github" / "workflows"
        self.checks = _load_workflow(workflows / "_checks.yml")
        self.ci = _load_workflow(workflows / "ci.yml")
        self.scheduled = _load_workflow(workflows / "scheduled.yml")
        self.release = _load_workflow(workflows / "release.yml")
        self.jobs = self.checks.get("jobs", {})

    def read(self, relative: str) -> str:
        path = self.root / relative
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def exempt_from(self, requirement: str) -> bool:
        return self.exemption is not None and self.exemption.covers(requirement)

    @property
    def free_threaded_expected(self) -> bool:
        return not self.exempt_from("PV1")

    @property
    def floor(self) -> str | None:
        match = re.search(r">=\s*3\.(\d+)", self.project.get("requires-python", ""))
        return f"3.{match.group(1)}" if match else None

    def matrix(self, job: str) -> list[str]:
        versions = self.jobs.get(job, {}).get("strategy", {}).get("matrix", {}).get("python-version", [])
        return [str(version) for version in versions]

    def steps(self, job: str) -> str:
        return "\n".join(
            str(step.get("run", "")) + str(step.get("with", "")) for step in self.jobs.get(job, {}).get("steps", [])
        )

    @property
    def has_runtime_dependencies(self) -> bool:
        return bool(self.project.get("dependencies") or self.project.get("optional-dependencies"))


Check = collections.abc.Callable[[Repo], tuple[bool, str]]
REGISTRY: dict[str, Check] = {}


def check(requirement: str) -> collections.abc.Callable[[Check], Check]:
    def register(function: Check) -> Check:
        REGISTRY[requirement] = function
        return function

    return register


@check("TL1")
def _tl1(repo: Repo) -> tuple[bool, str]:
    backend = repo.pyproject.get("build-system", {}).get("build-backend")
    return backend == "uv_build", f"build-backend is {backend!r}"


@check("TL2")
def _tl2(repo: Repo) -> tuple[bool, str]:
    lint = _names(repo.groups.get("lint", []))
    missing = sorted({"ruff", "ty", "eof-fixer"} - lint)
    return not missing and bool(repo.recipes), f"lint group lacks {missing}" if missing else "no justfile"


@check("TL3")
def _tl3(repo: Repo) -> tuple[bool, str]:
    leaked = sorted(_names(repo.project.get("dependencies", [])) & _names(repo.groups.get("lint", [])))
    has_pytest = "pytest" in _names(repo.groups.get("dev", []))
    return has_pytest and not leaked, f"runtime deps include lint tools {leaked}" if leaked else "dev lacks pytest"


@check("JF1")
def _jf1(repo: Repo) -> tuple[bool, str]:
    problems = [f"missing recipe {name}" for name in FIXED_RECIPES if name not in repo.recipes]
    install = repo.recipes.get("install", "")
    if "uv lock --upgrade" not in install or "--all-extras" not in install or not (
        "--group lint" in install or "--all-groups" in install
    ):
        problems.append("install does not upgrade the lock and sync every extra plus lint")
    if any("uv lock" in body for name, body in repo.recipes.items() if name != "install"):
        problems.append("a recipe other than install touches uv.lock")
    lint_ci = repo.recipes.get("lint-ci", "")
    if (
        re.search(r"ruff check(?!.*--no-fix)", lint_ci)
        or re.search(r"ruff format(?!.*--check)", lint_ci)
        or re.search(r"eof-fixer(?!.*--check)", lint_ci)
    ):
        problems.append("lint-ci rewrites files")
    if "--cov" in repo.recipes.get("test", ""):
        problems.append("test measures coverage")
    test_ci = repo.recipes.get("test-ci", "")
    if "--cov" not in test_ci or "xml" not in test_ci:
        problems.append("test-ci does not measure coverage and write XML")
    publish = repo.recipes.get("publish", "")
    if "GITHUB_REF_NAME" not in publish or "uv publish" not in publish or re.search("token", publish, re.IGNORECASE):
        problems.append("publish does not take the tag and publish with Trusted Publishing")
    return not problems, "; ".join(problems)


@check("RF1")
def _rf1(repo: Repo) -> tuple[bool, str]:
    ruff = repo.tool.get("ruff", {})
    lint = ruff.get("lint", {})
    isort = lint.get("isort", {})
    per_file = {**lint.get("per-file-ignores", {}), **lint.get("extend-per-file-ignores", {})}
    problems = []
    if ruff.get("fix") is not True or ruff.get("unsafe-fixes") is not True or ruff.get("line-length") != 120:
        problems.append("fix, unsafe-fixes or line-length differ")
    if lint.get("select") != ["ALL"]:
        problems.append("select is not ALL")
    removed = [code for code in CANONICAL_IGNORES if code not in lint.get("ignore", [])]
    if removed:
        problems.append(f"canonical ignores removed: {removed}")
    if isort.get("lines-after-imports") != 2 or isort.get("no-lines-before") != ["standard-library", "local-folder"]:
        problems.append("isort settings differ")
    if not any(glob in ("tests/**", "tests/**/*.py") and "S101" in codes for glob, codes in per_file.items()):
        problems.append("S101 is not ignored for tests/**")
    if "S101" in lint.get("ignore", []):
        problems.append("S101 is ignored everywhere")
    return not problems, "; ".join(problems)


@check("RF2")
def _rf2(repo: Repo) -> tuple[bool, str]:
    block = re.search(r"\[tool\.ruff\.lint\].*?\nignore\s*=\s*\[(.*?)\]", repo.pyproject_text, re.DOTALL)
    unreasoned = []
    for line in (block.group(1) if block else "").splitlines():
        entry = re.match(r'\s*"([A-Z]+\d*)"\s*,?\s*(#.*)?$', line)
        if entry and entry.group(1) not in CANONICAL_IGNORES and not entry.group(2):
            unreasoned.append(entry.group(1))
    return not unreasoned, f"ignores without a reason: {unreasoned}"


@check("RF3")
def _rf3(repo: Repo) -> tuple[bool, str]:
    return "target-version" not in repo.tool.get("ruff", {}), "target-version is set"


@check("RF4")
def _rf4(repo: Repo) -> tuple[bool, str]:
    stale = [code for code in ("G004", "TRY003", "EM102") if code in repo.tool.get("ruff", {}).get("lint", {}).get("ignore", [])]
    return not stale, f"stale ignores: {stale}"


@check("TY1")
def _ty1(repo: Repo) -> tuple[bool, str]:
    lint, lint_ci = repo.recipes.get("lint", ""), repo.recipes.get("lint-ci", "")
    arguments = [found.strip() for found in re.findall(r"ty check([^\n]*)", lint + lint_ci)]
    return "ty check" in lint and "ty check" in lint_ci and not any(arguments), f"ty check args: {arguments}"


@check("TY2")
def _ty2(repo: Repo) -> tuple[bool, str]:
    ty = repo.tool.get("ty", {})
    extra = sorted(set(ty) - {"src"}) + sorted(set(ty.get("src", {})) - {"exclude"})
    return not extra, f"[tool.ty] also sets {extra}"


@check("TS1")
def _ts1(repo: Repo) -> tuple[bool, str]:
    pytest = repo.tool.get("pytest", {}).get("ini_options", {})
    problems = []
    if pytest.get("testpaths") != ["tests"]:
        problems.append(f"testpaths is {pytest.get('testpaths')}")
    if "pytest-asyncio" in _names(repo.groups.get("dev", [])) and pytest.get("asyncio_mode") != "auto":
        problems.append("asyncio_mode is not auto")
    return not problems, "; ".join(problems)


def _coverage(repo: Repo) -> dict[str, typing.Any]:
    return repo.tool.get("coverage", {})


def _addopts(repo: Repo) -> str:
    addopts = repo.tool.get("pytest", {}).get("ini_options", {}).get("addopts", "")
    return " ".join(addopts) if isinstance(addopts, list) else addopts


@check("TS2")
def _ts2(repo: Repo) -> tuple[bool, str]:
    fail_under = _coverage(repo).get("report", {}).get("fail_under")
    duplicated = "cov-fail-under" in _addopts(repo) + "".join(repo.recipes.values())
    return fail_under == 100 and not duplicated, f"fail_under is {fail_under}, duplicated={duplicated}"


@check("TS3")
def _ts3(repo: Repo) -> tuple[bool, str]:
    return "--cov" not in _addopts(repo), "--cov is in addopts"


@check("TS4")
def _ts4(repo: Repo) -> tuple[bool, str]:
    gated = _coverage(repo).get("run", {}).get("branch") is True or "--cov-branch" in repo.recipes.get("test-ci", "")
    return not gated, "branch coverage is measured in the gated run"


@check("TS5")
def _ts5(repo: Repo) -> tuple[bool, str]:
    coverage = _coverage(repo)
    report = coverage.get("report", {})
    package = repo.tool.get("uv", {}).get("build-backend", {}).get("module-name") or repo.project.get(
        "name", ""
    ).replace("-", "_")
    omitted = coverage.get("run", {}).get("omit", []) + report.get("omit", [])
    package_omits = [
        entry for entry in omitted if entry.split("/")[0] in (package, "src") or entry.endswith("__main__.py")
    ]
    exact = report.get("exclude_also") == ["if typing.TYPE_CHECKING:"] and "exclude_lines" not in report
    return exact and not package_omits, f"exclude_also={report.get('exclude_also')} package omits={package_omits}"


@check("PV1")
def _pv1(repo: Repo) -> tuple[bool, str]:
    matrix = repo.matrix("pytest")
    wanted = [NEWEST] + ([f"{NEWEST}t"] if repo.free_threaded_expected else [])
    return all(version in matrix for version in wanted), f"pytest matrix {matrix} lacks one of {wanted}"


def expected_matrix(repo: Repo) -> list[str]:
    if repo.floor is None:
        return []
    low, high = int(repo.floor.split(".")[1]), int(NEWEST.split(".")[1])
    return [f"3.{minor}" for minor in range(low, high + 1)] + ([f"{NEWEST}t"] if repo.free_threaded_expected else [])


@check("PV2")
def _pv2(repo: Repo) -> tuple[bool, str]:
    return repo.matrix("pytest") == expected_matrix(repo), f"pytest matrix {repo.matrix('pytest')} != {expected_matrix(repo)}"


@check("CI1")
def _ci1(repo: Repo) -> tuple[bool, str]:
    on = repo.ci.get("on") or {}
    branches = (on.get("push") or {}).get("branches")
    cancels = repo.ci.get("concurrency", {}).get("cancel-in-progress") is True
    return branches == ["main"] and "pull_request" in on and cancels, "triggers or concurrency differ"


def _floors_skipped_on_schedule(repo: Repo) -> bool:
    return "github.event_name != 'schedule'" in str(repo.jobs.get("floors", {}).get("if", ""))


@check("CI2")
def _ci2(repo: Repo) -> tuple[bool, str]:
    on = repo.scheduled.get("on") or {}
    daily = any(re.fullmatch(r"\S+ \S+ \* \* \*", entry.get("cron", "").strip()) for entry in on.get("schedule", []))
    opens_issue = "issue" in repo.read(".github/workflows/scheduled.yml").lower()
    floors_ok = _floors_skipped_on_schedule(repo) or "floors" not in repo.jobs
    return daily and "workflow_dispatch" in on and opens_issue and floors_ok, (
        f"daily={daily} dispatch={'workflow_dispatch' in on} issue={opens_issue} floors-skipped={floors_ok}"
    )


@check("CI3")
def _ci3(repo: Repo) -> tuple[bool, str]:
    def calls(workflow: dict[str, typing.Any]) -> bool:
        return any(str(job.get("uses", "")).endswith("_checks.yml") for job in workflow.get("jobs", {}).values())

    return calls(repo.ci) and calls(repo.scheduled), "ci.yml or scheduled.yml does not call _checks.yml"


@check("CI4")
def _ci4(repo: Repo) -> tuple[bool, str]:
    steps = repo.steps("lint")
    pinned = re.findall(r"uv python pin (\S+)", steps)
    return "just install lint-ci" in steps and pinned == [repo.floor], f"lint job pins {pinned}, floor is {repo.floor}"


@check("CI5")
def _ci5(repo: Repo) -> tuple[bool, str]:
    steps = repo.steps("pytest")
    fail_fast = repo.jobs.get("pytest", {}).get("strategy", {}).get("fail-fast")
    return "just install" in steps and "just test-ci" in steps and fail_fast is False, f"fail-fast={fail_fast}"


def floors_finding(repo: Repo) -> Finding:
    if "floors" not in repo.jobs:
        if repo.has_runtime_dependencies:
            return Finding(requirement="CI6", status=Status.FAIL, detail="no floors job")
        return Finding(requirement="CI6", status=Status.PASS, detail="no runtime dependencies")
    steps = repo.steps("floors")
    problems = []
    if "lowest" not in steps:
        problems.append("does not resolve the lowest versions")
    if "--no-build" not in steps and "--only-binary" not in steps:
        problems.append("not wheel-only")
    if not _floors_skipped_on_schedule(repo):
        problems.append("not skipped on the schedule")
    if problems:
        return Finding(requirement="CI6", status=Status.FAIL, detail="; ".join(problems))
    missing = [version for version in repo.matrix("pytest") if version not in repo.matrix("floors")]
    if missing:
        return Finding(
            requirement="CI6", status=Status.WARN, detail=f"floors skip {missing}; allowed only where no wheel exists"
        )
    return Finding(requirement="CI6", status=Status.PASS)


@check("CI7")
def _ci7(repo: Repo) -> tuple[bool, str]:
    links = str(repo.jobs.get("links", {}))
    return "lychee" in links and "--offline" in links and "--remap" in links, "links job differs"


@check("CI8")
def _ci8(repo: Repo) -> tuple[bool, str]:
    if not (repo.root / "mkdocs.yml").is_file():
        return True, ""
    strict = "mkdocs build --strict" in repo.recipes.get("docs-build", "")
    return "just docs-build" in repo.steps("docs") and strict, f"docs job or strict docs-build missing, strict={strict}"


@check("RL1")
def _rl1(repo: Repo) -> tuple[bool, str]:
    tags = set(((repo.release.get("on") or {}).get("push") or {}).get("tags", []))
    return tags == TAG_PATTERNS, f"tag patterns {sorted(tags)}"


@check("RL2")
def _rl2(repo: Repo) -> tuple[bool, str]:
    version = repo.project.get("version")
    return version == "0" and "GITHUB_REF_NAME" in repo.recipes.get("publish", ""), f"version is {version!r}"


@check("RL3")
def _rl3(repo: Repo) -> tuple[bool, str]:
    steps = [step for job in repo.release.get("jobs", {}).values() for step in job.get("steps", [])]
    publish = [index for index, step in enumerate(steps) if "just publish" in str(step.get("run", ""))]
    release = [index for index, step in enumerate(steps) if "gh-release" in str(step.get("uses", ""))]
    checks = [step.get("run") for step in steps if re.search(r"just (test|lint)|pytest|ruff", str(step.get("run", "")))]
    ordered = bool(publish) and bool(release) and publish[0] < release[0]
    notes = "generate_release_notes" in str(steps)
    return ordered and notes and not checks, f"publish-first={ordered} notes={notes} checks={checks}"


@check("RL4")
def _rl4(repo: Repo) -> tuple[bool, str]:
    environments = [job.get("environment") for job in repo.release.get("jobs", {}).values()]
    id_token = "id-token: write" in repo.read(".github/workflows/release.yml")
    workflows = " ".join(path.read_text(encoding="utf-8") for path in (repo.root / ".github" / "workflows").glob("*.yml"))
    tokens = re.findall(r"secrets\.(\w*PYPI\w*)", workflows)
    return "pypi" in environments and id_token and not tokens, f"env={environments} id-token={id_token} tokens={tokens}"


def release_fingerprint(repo: Repo) -> str:
    lines = []
    for line in repo.read(".github/workflows/release.yml").splitlines():
        stripped = re.sub(r"\s+#.*", "", line).rstrip()
        if stripped.strip() and not stripped.strip().startswith("#"):
            lines.append(re.sub(r"(uses: [\w./-]+)@\S+", r"\1", stripped))
    return "\n".join(lines)


@check("FL1")
def _fl1(repo: Repo) -> tuple[bool, str]:
    return repo.read("CLAUDE.md").strip() == "@AGENTS.md", "CLAUDE.md is not exactly @AGENTS.md"


@check("FL2")
def _fl2(repo: Repo) -> tuple[bool, str]:
    agents = _norm(repo.read("AGENTS.md"))
    missing = [index + 1 for index, paragraph in enumerate(AGENTS_PARAGRAPHS) if _norm(paragraph) not in agents]
    return not missing, f"canonical paragraph(s) {missing} missing or reworded"


@check("FL4")
def _fl4(repo: Repo) -> tuple[bool, str]:
    adr = repo.root / "docs" / "adr"
    misnamed = [path.name for path in adr.glob("*.md") if not re.fullmatch(r"\d{4}-[a-z0-9-]+\.md", path.name)]
    return not misnamed, f"misnamed records: {misnamed}"


@check("FL5")
def _fl5(repo: Repo) -> tuple[bool, str]:
    return "MIT License" in repo.read("LICENSE"), "LICENSE is not MIT"


@check("RM1")
def _rm1(repo: Repo) -> tuple[bool, str]:
    readme = repo.read("README.md")
    links = re.findall(r"\]\(([^)\s]+)", readme) + re.findall(r'(?:href|src|srcset)="([^"\s]+)', readme)
    relative = [link for link in links if not re.match(r"(https?:|mailto:|#)", link)]
    return not relative, f"relative links: {relative[:5]}"


@check("MD1")
def _md1(repo: Repo) -> tuple[bool, str]:
    description = repo.project.get("description", "")
    problems = []
    if repo.metadata.description != description:
        problems.append(f"GitHub description {repo.metadata.description!r} != pyproject {description!r}")
    if repo.metadata.profile_row is None:
        problems.append("no row in the org profile")
    elif repo.metadata.profile_row != description:
        problems.append(f"profile row {repo.metadata.profile_row!r} differs")
    if len(description) > 120 or description.endswith("."):
        problems.append("longer than 120 characters or ends with a period")
    return not problems, "; ".join(problems)


@check("MD2")
def _md2(repo: Repo) -> tuple[bool, str]:
    topics = repo.metadata.topics
    misspelt = [f"{topic} -> {VOCABULARY_SPELLINGS[topic]}" for topic in topics if topic in VOCABULARY_SPELLINGS]
    malformed = [topic for topic in topics if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", topic)]
    homepage = bool(re.match(r"https://([a-z0-9-]+\.)?modern-python\.org", repo.metadata.homepage))
    ok = 0 < len(topics) <= 12 and not misspelt and not malformed and homepage
    return ok, f"{len(topics)} topics, misspelt={misspelt}, malformed={malformed}, homepage={repo.metadata.homepage!r}"


@check("MD3")
def _md3(repo: Repo) -> tuple[bool, str]:
    keywords = set(repo.project.get("keywords", []))
    topics = set(repo.metadata.topics)
    forbidden = any("dependency injector" in keyword.lower() for keyword in keywords)
    return keywords == topics and not forbidden, (
        f"only in keywords {sorted(keywords - topics)}, only in topics {sorted(topics - keywords)}"
    )


@check("MD4")
def _md4(repo: Repo) -> tuple[bool, str]:
    classifiers = repo.project.get("classifiers", [])
    listed = sorted(
        entry.rsplit(":: ", 1)[1]
        for entry in classifiers
        if re.fullmatch(r"Programming Language :: Python :: 3\.\d+", entry)
    )
    tested = sorted(version for version in expected_matrix(repo) if not version.endswith("t"))
    free_threading = "Programming Language :: Python :: Free Threading :: 2 - Beta" in classifiers
    problems = []
    if not any(entry.startswith("Development Status") for entry in classifiers):
        problems.append("no Development Status")
    if "Intended Audience :: Developers" not in classifiers or "Typing :: Typed" not in classifiers:
        problems.append("no Intended Audience :: Developers or Typing :: Typed")
    if listed != tested:
        problems.append(f"Python classifiers {listed} != tested {tested}")
    if free_threading != repo.free_threaded_expected:
        problems.append(f"free-threading classifier present={free_threading}")
    if any(entry.startswith("License ::") for entry in classifiers):
        problems.append("License classifier")
    invalid = [entry for entry in classifiers if entry not in valid_classifiers]
    if invalid:
        problems.append(f"invalid: {invalid}")
    return not problems, "; ".join(problems)


@check("MD5")
def _md5(repo: Repo) -> tuple[bool, str]:
    urls = repo.project.get("urls", {})
    wanted = {"Homepage", "Repository", "Issues", "Changelog"}
    if repo.metadata.homepage.rstrip("/") != "https://modern-python.org":
        wanted.add("Documentation")
    changelog = str(urls.get("Changelog", "")).endswith("/releases")
    return set(urls) == wanted and changelog, f"labels {sorted(urls)}, expected {sorted(wanted)}"


@check("MD6")
def _md6(repo: Repo) -> tuple[bool, str]:
    return repo.project.get("name") == repo.name, f"distribution name is {repo.project.get('name')!r}"


def _pragmas(repo: Repo) -> tuple[int, int]:
    bare = reasoned = 0
    for path in repo.root.rglob("*.py"):
        if {".git", ".venv"} & set(path.relative_to(repo.root).parts):
            continue
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            found = None if line.lstrip().startswith("#") else _PRAGMA.search(line)
            if found and re.search(r"\w", found.group(1)):
                reasoned += 1
            elif found:
                bare += 1
    return bare, reasoned


def pragma_finding(repo: Repo) -> Finding:
    bare, _ = _pragmas(repo)
    if not bare:
        return Finding(requirement="TS6", status=Status.PASS)
    status = Status.FAIL if repo.today >= TS6_BECOMES_MUST else Status.WARN
    return Finding(requirement="TS6", status=status, detail=f"{bare} pragma(s) without a reason")


def pr_title_finding(repo: Repo) -> Finding:
    unconventional = [title for title in repo.metadata.pr_titles if not _CONVENTIONAL.match(title)]
    if not unconventional:
        return Finding(requirement="RL6", status=Status.PASS)
    return Finding(requirement="RL6", status=Status.WARN, detail=f"recent titles not conventional: {unconventional[:3]}")


def evaluate(repo: Repo) -> list[Finding]:
    findings = [
        Finding(requirement=requirement, status=Status.PASS if ok else Status.FAIL, detail="" if ok else detail)
        for requirement, (ok, detail) in ((requirement, function(repo)) for requirement, function in REGISTRY.items())
    ]
    findings += [floors_finding(repo), pragma_finding(repo), pr_title_finding(repo)]
    return [
        dataclasses.replace(finding, status=Status.EXEMPT)
        if finding.status in (Status.FAIL, Status.WARN) and repo.exempt_from(finding.requirement)
        else finding
        for finding in findings
    ]

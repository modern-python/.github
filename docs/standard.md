# The standard

What makes a repository a modern-python repository. It is written for the maintainer,
contributors, and the coding agents that work across the org's repositories. It is not a guide to
writing Python; it is the shape every repo shares so that tooling, CI, and agents can rely on it.

## Scope

The standard applies to every repo that publishes a package to PyPI under the org.

## Reading a requirement

Each requirement has a stable ID (`CI6`) and an anchor of the same name
(`https://modern-python.org/standard/#CI6`). Cite the ID, not a heading.

The key words "MUST", "MUST NOT", "SHOULD", "SHOULD NOT", and "MAY" are to be interpreted as
described in [BCP 14](https://www.rfc-editor.org/info/bcp14) ([RFC 2119], [RFC 8174]) when, and
only when, they appear in all capitals.

- **MUST** and **MUST NOT** form the **core**. A repo meets every core requirement, or carries an
  [exemption](#exemptions) for it.
- **SHOULD** and **SHOULD NOT** are recommendations. A pull request that departs from one says why.
- **MAY** is a permission.

A *Why* line under a requirement is its rationale, not part of the requirement.

[RFC 2119]: https://www.rfc-editor.org/rfc/rfc2119
[RFC 8174]: https://www.rfc-editor.org/rfc/rfc8174

## Toolchain

### TL1 · uv { #TL1 }

A repo MUST use [uv](https://github.com/astral-sh/uv) for Python versions, dependencies, the
lockfile, build, and publish, with the `uv_build` build backend.

### TL2 · Lint, types, and tasks { #TL2 }

A repo MUST use [ruff](https://github.com/astral-sh/ruff) to lint and format,
[ty](https://github.com/astral-sh/ty) to type-check,
[eof-fixer](https://github.com/modern-python/eof-fixer) so that every text file ends with exactly
one newline, and [just](https://github.com/casey/just) as the task runner.

### TL3 · Dependency groups { #TL3 }

The `dev` group MUST hold the test dependencies. The `lint` group MUST hold `ruff`, `ty`,
`eof-fixer`, and any typing stubs. A library's runtime dependencies MUST NOT include either group's
packages.

## justfile

### JF1 · Fixed recipes { #JF1 }

The `justfile` MUST provide these recipes, each meeting its contract:

| Recipe | Contract |
|---|---|
| `install` | Upgrades the lockfile and syncs every extra plus the `lint` group. The only recipe that touches `uv.lock`. |
| `lint` | **Rewrites files.** Autofix, then type-check. |
| `lint-ci` | The read-only twin of `lint`, same checks. |
| `test` | pytest with arguments passed through and **no coverage measured**. |
| `test-ci` | The full run with coverage measured and the XML report written. |
| `publish` | Builds and publishes the version named by the tag ([RL2](#RL2)), authenticating with Trusted Publishing ([RL4](#RL4)). |

*Why:* CI and contributors call only these names, so every repo can be driven the same way.
`lint-ci` answers without mutating; `test` stays free of the coverage gate so a targeted run never
meets it ([TS3](#TS3)).

### JF2 · Recipe names are fixed { #JF2 }

A repo MAY add recipes. It MUST NOT rename or repurpose the recipes in [JF1](#JF1).

### JF3 · Tests that need a service { #JF3 }

A repo whose tests need a service (PostgreSQL, Redis, a broker) MAY run `test` through Docker
Compose. The recipe name and the pass-through of arguments stay as [JF1](#JF1) defines them.

## Ruff

### RF1 · Canonical configuration { #RF1 }

`pyproject.toml` MUST contain the [canonical ruff block](#appendix-a-ruff-block).

### RF2 · Ignores { #RF2 }

A repo MAY add ignores to the canonical block, each with a one-line reason. It MUST NOT remove an
ignore the canonical block lists.

*Why:* the canonical `ignore` list is the minimum the org agrees on.

### RF3 · No target version { #RF3 }

The ruff configuration SHOULD NOT set `target-version`.

*Why:* ruff derives it from `requires-python`, so a second declaration can only drift.

### RF4 · Stale ignores { #RF4 }

A repo that still ignores `G004`, `TRY003`, or `EM102` SHOULD drop them the next time it touches
the ruff block.

*Why:* across the org they suppress nothing.

## Type checking

### TY1 · Where ty runs { #TY1 }

`ty check` MUST run in `lint` and `lint-ci`, over the whole repo.

### TY2 · ty configuration { #TY2 }

`[tool.ty]` MUST NOT hold configuration other than `src.exclude`, and `src.exclude` MUST list only
directories that are not the package (benchmarks with their own environment, generated code).

## Tests and coverage

### TS1 · pytest { #TS1 }

Tests MUST run under pytest with `testpaths = ["tests"]`, and with `asyncio_mode = "auto"` where
asyncio is involved.

### TS2 · 100 % line coverage { #TS2 }

Line coverage MUST be 100 %, declared once as `[tool.coverage.report] fail_under = 100`.

### TS3 · Coverage is measured only in CI recipes { #TS3 }

`--cov` MUST NOT appear in pytest `addopts`.

*Why:* pytest-cov applies `fail_under` whenever coverage is measured, so the gate applies exactly
where `--cov` is passed: `test-ci` (and `test-branch`, where present), never `test`. Measuring on
every run would gate every run.

### TS4 · Branch coverage { #TS4 }

A repo MAY measure branch coverage. Branch coverage MUST NOT be the gate.

### TS5 · Exclusions { #TS5 }

`[tool.coverage.report] exclude_also` MUST be `["if typing.TYPE_CHECKING:"]`. A repo MUST NOT
exclude a file to reach the number; it deletes or tests the code instead.

## Python versions

### PV1 · Newest Python { #PV1 }

The test matrix MUST include the newest stable CPython minor and that minor's free-threaded build
(`3.14` and `3.14t` today).

### PV2 · Matrix shape { #PV2 }

The matrix MUST be every minor from the repo's `requires-python` floor to the newest, plus the
free-threaded newest, written as a hand-maintained list in the repo's `_checks.yml`.

*Why:* a new Python is then a one-line change in every repo, made in one sweep.

### PV3 · Python floor { #PV3 }

A repo MAY set `requires-python` to what its code needs, and MAY raise it without a recorded
reason. Dependency floors are a separate obligation ([CI6](#CI6)).

## CI

### CI1 · `ci.yml` { #CI1 }

`ci.yml` MUST run on `push` to `main` and on `pull_request`, with `concurrency` cancelling
superseded runs.

### CI2 · `scheduled.yml` { #CI2 }

`scheduled.yml` MUST run weekly and on `workflow_dispatch`, running the same checks as `ci.yml`. On
a scheduled failure it MUST open or update a tracking issue in the repo.

*Why:* a dependency release or a new Python that breaks the build becomes a ticket without anyone
watching.

### CI3 · Per-repo `_checks.yml` { #CI3 }

`ci.yml` and `scheduled.yml` MUST both call the repo's own reusable `_checks.yml`, which holds the
jobs [CI4](#CI4) to [CI8](#CI8).

*Why:* a shared workflow in `modern-python/.github` was built and rejected
([#95](https://github.com/modern-python/.github/issues/95)): a `workflow_call` input is a scalar,
so a service container or an env map has to be flattened into a string, and image knowledge ends
up in the org repo. A change to the jobs is a sweep across the repos instead.

### CI4 · `lint` job { #CI4 }

The `lint` job MUST run `just install lint-ci` on the repo's floor Python.

### CI5 · `pytest` job { #CI5 }

The `pytest` job MUST run `just install` then `just test-ci` on every matrix entry, with
`fail-fast: false`.

### CI6 · `floors` job { #CI6 }

The `floors` job MUST resolve every direct dependency at its declared floor, wheel-only
(`--no-build`, or `--only-binary` naming the dependency that needs it), on every matrix entry, then
run the suite or an import.

A repo MAY run an import smoke test instead of the suite where the floors cannot carry it, and MAY
drop a matrix entry that no upstream wheel covers at the floor (`compose2pod` drops `3.14t` for
PyYAML).

*Why:* `pytest` resolves every dependency at its newest, so without this job the bottom of each
declared range ships untested. It has rotted there before
([compose2pod#126](https://github.com/modern-python/compose2pod/issues/126),
[faststream-outbox#190](https://github.com/modern-python/faststream-outbox/pull/190)).
Wheel-only, because a floor reachable only by compiling an sdist is not one a user installing a
wheel can reach, and without the flag the resolver builds one and reports success. Every matrix
entry, because wheel coverage is per interpreter.

### CI7 · `links` job { #CI7 }

The `links` job MUST run [lychee](https://github.com/lycheeverse/lychee-action) with `--offline`,
remapping this repo's `blob/main` URLs to the checkout.

*Why:* it then fails only on a relative link or file path the diff broke.

### CI8 · `docs` job { #CI8 }

A repo with a docs site MUST have a `docs` job running `just docs-build` (`mkdocs build --strict`).

## Release

### RL1 · Tags { #RL1 }

A release MUST be a tag pushed off green `main`. The tag name MUST be bare semver (`3.4.0`) or a
PEP 440 pre-release (`2.0.0rc1`, `4.0.0a2`). The tag object MAY be annotated or signed.

```bash
git tag -m "<repo> 3.4.0" 3.4.0 && git push origin 3.4.0
```

### RL2 · Version from the tag { #RL2 }

`pyproject.toml` MUST keep `version = "0"` and MUST NOT be bumped. `just publish` takes the version
from the tag (`$GITHUB_REF_NAME`).

### RL3 · `release.yml` { #RL3 }

`release.yml` MUST trigger on the tag patterns of [RL1](#RL1), run `just publish`, and only then
create the GitHub Release with generated notes, flagging a tag that contains a letter as a
pre-release. It MUST NOT run checks of its own.

*Why:* PyPI is irreversible, so a failed publish must create no Release. The tag is the commitment
point, which is why the workflow does not gate on CI.

### RL4 · Trusted Publishing { #RL4 }

Publishing MUST authenticate with PyPI Trusted Publishing through the `pypi` environment. A repo
MUST NOT hold a PyPI token.

### RL5 · One `release.yml` { #RL5 }

`release.yml` MUST be identical across repos apart from the comment naming the PyPI project.

*Why:* PyPI does not accept a reusable workflow as a Trusted Publisher, so the file cannot be
shared and is copied instead.

### RL6 · PR titles { #RL6 }

Pull request titles SHOULD follow [Conventional Commits](https://www.conventionalcommits.org/).
Release prose MAY be added afterwards with `gh release edit`.

*Why:* the Release body is GitHub's generated notes from squashed PR titles, so the title is the
changelog entry.

## Repository files

### FL1 · `CLAUDE.md` { #FL1 }

`CLAUDE.md` MUST be exactly one line: `@AGENTS.md`.

### FL2 · `AGENTS.md` { #FL2 }

`AGENTS.md` MUST contain the [canonical paragraphs](#appendix-b-agentsmd-paragraphs) word for word
(line wrapping is free). A repo MAY append sentences after each. Beyond them, `AGENTS.md` MUST hold
only what an agent cannot infer from the tree.

*Why:* the canonical paragraphs are the facts an agent gets wrong on first contact and cannot learn
from the tree.

### FL3 · `CONTEXT.md` { #FL3 }

`CONTEXT.md` MUST be the glossary: what the repo is in one or two sentences, then terms that have a
synonym to reject. It MUST NOT hold implementation details.

### FL4 · Decision records { #FL4 }

Decision records MUST live in `docs/adr/` as `NNNN-slug.md`, one paragraph each, and only for
decisions that are hard to reverse, surprising later, and the result of a real trade-off.

### FL5 · License { #FL5 }

`LICENSE` MUST be MIT.

### FL6 · Community health files { #FL6 }

A repo MUST NOT carry its own `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, or
`SUPPORT.md` except to override the one it inherits from `modern-python/.github`.

## README

### RM1 · Absolute links { #RM1 }

Every link in `README.md` MUST be absolute:
`https://github.com/modern-python/<repo>/blob/main/<path>`, or `.../tree/main/<path>` for a
directory.

*Why:* `README.md` is also the PyPI long description, and PyPI does not rewrite relative links, so
a relative one 404s on the package page.

### RM2 · Opening { #RM2 }

`README.md` MUST open with the repo's one-liner ([MD1](#MD1)), then what the package does, then a
minimal example.

## Metadata

### MD1 · One-liner { #MD1 }

The GitHub description, the pyproject `description`, and the repo's row in the org profile MUST be
the same one-liner: purpose-first, about 120 characters at most, no trailing period.

### MD2 · GitHub topics and website { #MD2 }

GitHub topics MUST be lowercase and hyphenated, at most 12, drawn from the shared vocabulary:
`python`, `dependency-injection`, `di`, `ioc-container`, `modern-di`, `fastapi`, `litestar`,
`faststream`, `sqlalchemy`, `postgresql`, `asyncio`, `docker`, `cli`, `messaging`. The website
field MUST be the docs site, or `modern-python.org`.

### MD3 · Keywords { #MD3 }

`keywords` MUST mirror the topics, and MUST NOT include `dependency injector`.

*Why:* that is another package's name (`dependency-injector`).

### MD4 · Classifiers { #MD4 }

`classifiers` MUST include `Development Status`, `Intended Audience :: Developers`, one
`Programming Language :: Python :: 3.X` per minor in the matrix ([PV2](#PV2)), and
`Typing :: Typed`. They MUST include `Programming Language :: Python :: Free Threading :: 2 - Beta`
when the matrix's free-threaded entry is green, and a repo exempt from that entry omits it. They
SHOULD include a `Topic` where apt. Every string MUST validate against
<https://pypi.org/classifiers/>. They MUST NOT include a `License ::` classifier.

*Why:* the SPDX `license = "MIT"` key is the declaration, and PEP 639 deprecates pairing it with a
classifier.

### MD5 · Project URLs { #MD5 }

`[project.urls]` MUST use the PyPI labels `Homepage`, `Documentation` (only if a docs site exists),
`Repository`, `Issues`, and `Changelog` (the Releases page).

### MD6 · Distribution name { #MD6 }

The PyPI distribution name MUST equal the repo name.

## Exemptions

| Repo | Exempt from | Why |
|---|---|---|
| `that-depends` | the core as a whole, except [TS2](#TS2) | The org's most-used package and the only repo with steady external contributor traffic; it keeps its own tooling rather than converging. |
| `modern-di-arq` | [PV1](#PV1), the `3.14t` entry | Every `arq` release requires `redis[hiredis]<6`, and importing `hiredis` re-enables the GIL ([hiredis-py#229](https://github.com/redis/hiredis-py/issues/229)). Lift when a `hiredis` release declares free-threading support. |
| `modern-di-grpc` | [PV1](#PV1), the `3.14t` entry | `grpcio` ships no free-threaded wheel and importing `cygrpc` re-enables the GIL ([grpc/grpc#38762](https://github.com/grpc/grpc/issues/38762)). Lift when a `grpcio` release declares free-threading support. |

An exemption is granted by a pull request to this repo that adds the row. Drift that nobody
recorded is not an exemption.

## Changing the standard

A change lands as one pull request to `modern-python/.github` that updates this page and the
exemptions table together. Repos then converge. The standard carries no version number: the page on
`main` is the standard.

- An ID is never reused. A removed requirement leaves its ID retired; a reworded one keeps its ID
  only if its meaning is unchanged.
- A new MUST lands as a SHOULD marked "becomes MUST on <date>", giving repos time to converge before
  it joins the core.

## Appendix A: ruff block { #appendix-a-ruff-block }

The canonical block for [RF1](#RF1).

```toml
[tool.ruff]
fix = true
unsafe-fixes = true
line-length = 120

[tool.ruff.lint]
select = ["ALL"]
ignore = [
    "D1",     # docstrings are not forced; a docstring exists when it says something
    "D203",   # conflicts with D211
    "D213",   # conflicts with D212
    "COM812", # conflicts with the formatter
    "ISC001", # conflicts with the formatter
    "CPY001", # no per-file copyright header
    "FBT",    # boolean positional arguments are fine
    "TCH",    # imports stay real; TYPE_CHECKING-only imports break runtime introspection
]
isort.lines-after-imports = 2
isort.no-lines-before = ["standard-library", "local-folder"]

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101"]  # assert is the test idiom; in library code it is a finding
```

## Appendix B: AGENTS.md paragraphs { #appendix-b-agentsmd-paragraphs }

The canonical paragraphs for [FL2](#FL2).

```markdown
`just` (task runner) and `uv` (package manager). The [`justfile`](justfile) is the source of truth —
`just --list`, or read it.
```

```markdown
Every link in `README.md` must be absolute: `https://github.com/modern-python/<repo>/blob/main/<path>`,
or `.../tree/main/<path>` for a directory. Never a relative path: `README.md` is also the PyPI long
description, and PyPI does not rewrite relative links, so a relative one 404s on the package page.
```

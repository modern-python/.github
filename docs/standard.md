# The standard

What makes a repository a modern-python repository. It is normative: a repo either meets the
**core** below, or carries an **exemption** listed at the end of this page. Everything the page
describes outside the core is a recommendation.

The audience is the maintainer, contributors, and the coding agents that work across the org's
repositories. It is not a guide to writing Python; it is the shape every repo shares so that
tooling, CI, and agents can rely on it.

## Scope

**Core repositories** are the libraries: every repo that publishes a package to PyPI under the
org. The core applies to them in full.

`that-depends` is exempt from the core as a whole; see [Exemptions](#exemptions).

## 1. Toolchain

| Tool | Role |
|---|---|
| [uv](https://github.com/astral-sh/uv) | Python versions, dependencies, lockfile, build (`uv_build` backend), publish |
| [ruff](https://github.com/astral-sh/ruff) | lint and format, `select = ["ALL"]` |
| [ty](https://github.com/astral-sh/ty) | type checking |
| [eof-fixer](https://github.com/modern-python/eof-fixer) | every text file ends with exactly one newline |
| [just](https://github.com/casey/just) | task runner; the `justfile` is the only entry point CI and contributors use |

Dependency groups: `dev` holds test dependencies, `lint` holds `ruff`, `ty`, `eof-fixer` and any
typing stubs. CI installs both; a library's runtime dependencies never include either.

## 2. The justfile

Recipe names and their contracts are fixed. CI calls only these names, so a repo may add recipes
freely but may not rename or repurpose these.


| Recipe | Contract |
|---|---|
| `install` | Upgrades the lockfile and syncs every extra plus the `lint` group. The only recipe that touches `uv.lock`. |
| `lint` | **Rewrites files.** Autofix, then type-check. |
| `lint-ci` | The read-only twin of `lint`, same checks. What CI runs. Use it locally when you want an answer, not a mutation. |
| `test` | pytest with arguments passed through and **no coverage measured**, so a targeted run never meets the gate. |
| `test-ci` | The full run with coverage measured and the XML report written; the gate in `[tool.coverage.report]` applies here. What CI runs. |
| `publish` | Version comes from the git tag (`$GITHUB_REF_NAME`); `pyproject.toml` keeps `version = "0"` and is never bumped. Auth is PyPI Trusted Publishing; there is no token. |

A repo whose tests need a service (PostgreSQL, Redis, a broker) may run `test` through Docker
Compose; the recipe name and the pass-through of arguments stay the same.

## 3. Ruff

The canonical block. Its `ignore` list is the minimum: a repo may add ignores it needs, each with
a one-line reason, and may not remove one.

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

`target-version` is omitted: ruff derives it from `requires-python`.

Three ignores that appear in older copies of this block suppress nothing measured across the org:
`G004`, `TRY003`, `EM102`. Drop them when you touch a repo.

## 4. Type checking

`ty check` runs in `lint` and `lint-ci`, over the whole repo, with no `[tool.ty]` configuration
beyond `src.exclude` for directories that are not the package (benchmarks with their own
environment, generated code).

## 5. Tests and coverage

- pytest, `testpaths = ["tests"]`, `asyncio_mode = "auto"` where asyncio is involved.
- **100 % line coverage**, declared once as `[tool.coverage.report] fail_under = 100`. pytest-cov
  reads it whenever coverage is measured, so the gate applies exactly where `--cov` is passed:
  `test-ci` (and `test-branch`, where present), never `test`. `--cov` never appears in pytest
  `addopts`; measuring on every run would gate every run. Branch coverage is diagnostic, never the
  gate.
- `[tool.coverage.report] exclude_also = ["if typing.TYPE_CHECKING:"]` is the one standing
  exclusion. Do not exclude a file to reach the number; delete or test it.

## 6. Python versions

There is no floor policy. A repo sets `requires-python` to what its code needs and may raise it
without a recorded reason.

The obligation is at the other end: **the test matrix always includes the newest stable CPython
minor and that minor's free-threaded build** (`3.14` and `3.14t` today). The matrix is every minor
from the repo's floor to the newest, plus the free-threaded newest. The `Programming Language ::
Python :: 3.X` classifiers list every minor in the matrix.

In the shared checks workflow (section 7) the matrix is derived at run time from `requires-python`
and the newest released cycle, so no repo edits a matrix when a Python ships; a repo still on its
own `_checks.yml` maintains the list by hand.

## 7. CI

Two workflows per repo, both thin:

- `ci.yml` on `push` to `main` and on `pull_request`, with `concurrency` cancelling superseded runs.
- `scheduled.yml` weekly and on `workflow_dispatch`, running the same checks and, on a scheduled
  failure, opening or updating a tracking issue in the repo. This is how a dependency release or a
  new Python that breaks the build becomes a ticket without anyone watching.

Both call one reusable `checks.yml` with these jobs:

| Job | What it does |
|---|---|
| `lint` | `just install lint-ci` on the repo's floor Python |
| `pytest` | `just install` then `just test-ci` on every matrix entry, `fail-fast: false` |
| `links` | [lychee](https://github.com/lycheeverse/lychee-action) with `--offline`, remapping this repo's `blob/main` URLs to the checkout, so it fails only on a relative link or file path the diff broke |
| `docs` | `just docs-build` (`mkdocs build --strict`), only for repos with a docs site |

The shared `checks.yml` will live in `modern-python/.github` and be referenced at `main`, so a
change to it reaches every repo on merge; such a change is first exercised from a branch ref in
one repo. Until it exists, each repo carries the same jobs in a local `_checks.yml`.

## 8. Release

Tag-driven. A maintainer pushes a tag off green `main`:

```bash
git tag -m "<repo> 3.4.0" 3.4.0 && git push origin 3.4.0
```

- The tag **name** is bare semver (`3.4.0`) or a PEP 440 pre-release (`2.0.0rc1`, `4.0.0a2`); the
  tag object may be annotated or signed.
- `release.yml` matches those two patterns, runs `just publish` first (PyPI is irreversible, so a
  failed publish creates no Release), then creates the GitHub Release with generated notes; a tag
  containing a letter is flagged pre-release.
- Auth is PyPI Trusted Publishing through the `pypi` environment. Nothing is registered but the
  workflow filename and the environment; there is no CI gate in the workflow because the tag is the
  commitment point.
- The Release body is GitHub's generated notes from squashed PR titles, so a conventional-commit
  PR title is the changelog entry. Prose goes in afterwards with `gh release edit`.

`release.yml` stays a per-repo file: PyPI does not accept a reusable workflow as a Trusted
Publisher. It is identical across repos apart from the comment naming the PyPI project.

## 9. Repository files

| File | Rule |
|---|---|
| `CLAUDE.md` | Exactly one line: `@AGENTS.md`. |
| `AGENTS.md` | Agent guidance for this repo. Contains the two canonical paragraphs below verbatim, then only what an agent cannot infer from the tree. |
| `CONTEXT.md` | The glossary: what the repo is in one or two sentences, then terms that have a synonym to reject. No implementation details. |
| `docs/adr/` | Decision records, `NNNN-slug.md`, one paragraph each, only for decisions that are hard to reverse, surprising later, and the result of a real trade-off. |
| `LICENSE` | MIT. |
| `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md` | Inherited from `modern-python/.github`; a repo adds its own only to override. |

The two canonical `AGENTS.md` paragraphs. They are the facts an agent gets wrong on first contact
and cannot learn from the tree; a repo may append sentences after each, but the text itself is
kept word for word (line wrapping is free):

```markdown
`just` (task runner) and `uv` (package manager). The [`justfile`](justfile) is the source of truth —
`just --list`, or read it.
```

```markdown
Every link in `README.md` must be absolute: `https://github.com/modern-python/<repo>/blob/main/<path>`,
or `.../tree/main/<path>` for a directory. Never a relative path: `README.md` is also the PyPI long
description, and PyPI does not rewrite relative links, so a relative one 404s on the package page.
```

## 10. README

`README.md` is the PyPI long description. Every link in it is absolute, per the paragraph above.
It opens with the repo's one-line description (section 11), then what the package does, then a
minimal example.

## 11. Metadata

A repo's summary appears in three places and they say the same thing: the GitHub description, the
pyproject `description`, and the repo's row in the org profile. One canonical one-liner per repo,
purpose-first, about 120 characters at most, no trailing period.

- **GitHub topics**: lowercase, hyphenated, at most 12, drawn from the shared vocabulary (`python`,
  `dependency-injection`, `di`, `ioc-container`, `modern-di`, `fastapi`, `litestar`, `faststream`,
  `sqlalchemy`, `postgresql`, `asyncio`, `docker`, `cli`, `messaging`). The website field is the
  docs site, or `modern-python.org`.
- **`keywords`** mirror the topics.
- **`classifiers`**: `Development Status`, `Intended Audience :: Developers`, one
  `Programming Language :: Python :: 3.X` per tested minor, `Typing :: Typed`, a `Topic` where apt.
  **No `License ::` classifier**: the SPDX `license = "MIT"` key is the declaration, and PEP 639
  deprecates pairing it with a classifier.
- **`[project.urls]`** uses the PyPI labels `Homepage`, `Documentation` (only if a docs site
  exists), `Repository`, `Issues`, `Changelog` (the Releases page).
- The PyPI distribution name equals the repo name.

## Exemptions

| Repo | Exempt from | Why |
|---|---|---|
| `that-depends` | the core as a whole | The org's most-used package and the only repo with steady external contributor traffic; it keeps its own tooling rather than converging. It does adopt the 100 % coverage gate. |
| `modern-di-arq` | section 6, the `3.14t` matrix entry | Every `arq` release requires `redis[hiredis]<6`, and importing `hiredis` re-enables the GIL ([hiredis-py#229](https://github.com/redis/hiredis-py/issues/229)). Lift when a `hiredis` release declares free-threading support. |
| `modern-di-grpc` | section 6, the `3.14t` matrix entry | `grpcio` ships no free-threaded wheel and importing `cygrpc` re-enables the GIL ([grpc/grpc#38762](https://github.com/grpc/grpc/issues/38762)). Lift when a `grpcio` release declares free-threading support. |

An exemption is granted by a pull request to this repo that adds the row. Drift that nobody
recorded is not an exemption.

## Changing the standard

A change to the core lands as one pull request to `modern-python/.github` that updates this page
and the exemptions table together. Repos then converge. The standard carries no version number:
the page on `main` is the standard.

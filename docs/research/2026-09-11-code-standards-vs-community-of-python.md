# Code standards: what community-of-python has, what modern-python has, what to build

Research note, 2026-09-11. Internal to the repo; `mkdocs.yml` excludes `docs/research/` from the
public site.

**Question.** community-of-python publishes code style and standards (guidelines, a lint plugin,
shared CI). What would "the same thing" be for modern-python, and which parts are worth building?

**Method.** Primary sources only: shallow clones of the four community-of-python repos at today's
`main` (`pylines@6a521b8`, `flake8-plugin@7ad1c09`, `community-workflow@d89d285`, `.github`), plus
`microbootstrap` and `stompman` as consumers; the 28 modern-python checkouts under
`~/src/modern-python` as of today; `ruff 0.16.4` and `ty 0.0.74` CLIs from the `modern-di` venv;
the ruff FAQ, PyPI Trusted Publishers docs and tracker, GitHub reusable-workflow docs, copier docs.

## 1. What community-of-python has

Four repos, four layers:

| Layer | Repo | Mechanism | State (2026-09-11) |
|---|---|---|---|
| Prose guidelines | [pylines](https://github.com/community-of-python/pylines) | Markdown: `code-style.md` (Russian), `tests.md`, `rest.md`, `solid.md`, `our-stack.md`, `frontend*.md`, plus a reference `pyproject.toml` | 43 stars, pushed 2026-09-07, one active author |
| Agent skill | `pylines/pylines-skill/` | `SKILL.md` + `sync.sh`: shallow-clones the repo into a cache (1 h TTL), regenerates a heading index, tells the agent to read guides whole; installed with `npx skills add … -g`. Guides are not bundled, so the skill never goes stale | same repo |
| Custom lint rules | [flake8-plugin](https://github.com/community-of-python/flake8-plugin) | 17 `COP0xx` flake8 checks for rules ruff cannot express: names ≥ 8 chars, verb function names, no `get_` on async, `@typing.final` on every class, `MappingProxyType` for module dicts, `dataclass(kw_only, slots, frozen)`, `one_` loop-variable prefix, `*`/`/` after two positional args, reassignment forbidden unless annotated `Mutable[T]` (shipped as a zero-dep `cop_extensions` package) | 4 stars, pushed 2026-07-10 |
| Shared CI | [community-workflow](https://github.com/community-of-python/community-workflow) | Four `workflow_call` files: `preset.yml` fans out to `lint.yml`, `test.yml` (3-OS × Python matrix, codecov upload), `publish.yml` (`PYPI_TOKEN` secret on `release: published`). Consumers call `preset.yml@main` with a JSON list of Python versions | 1 star, pushed 2025-08-15 |
| Org profile | `.github` | README says "This repository is not important" | profile only |

Two design points carry over:

- **The rule and its rationale live together.** `code-style.md` opens with the ruff config and
  explains every ignored rule in one line each. The same ignore list is byte-identical in
  `pylines/pyproject.toml`, `flake8-plugin/pyproject.toml` and `microbootstrap/pyproject.toml`
  (`EM FBT TRY003 D1 D203 D213 G004 FA COM812 ISC001`).
- **The CI contract is the justfile.** `community-workflow` never runs a tool directly; it runs
  `just install lint-ci`, `just test …`, `just publish`. A repo opts in by exposing those recipe
  names. Of the two consumers checked, `microbootstrap` uses `preset.yml`; `stompman` has its own
  workflows and a different recipe set (`check-types`, `test-fast`), so adoption is partial even
  upstream.

Why flake8 rather than ruff for the custom rules: the ruff FAQ states "Ruff does not yet support
third-party plugins" and "Ruff's primary limitation vis-à-vis Flake8 is that it does not support
custom lint rules" ([docs.astral.sh/ruff/faq](https://docs.astral.sh/ruff/faq/)).

## 2. What modern-python already has

More than it looks like from the outside; the problem is form, not content.

**Org level** (`modern-python/.github`, this repo): `AGENTS.md` fixes the metadata rules (one
description on three surfaces, topic vocabulary, keyword/classifier rules, no License classifier,
PyPI URL labels), the tooling line (uv, ruff, ty, uv_build), the CI stale-merge-ref gotcha, and the
`INVARIANT:` docstring convention. `CONTRIBUTING.md` applies org-wide "unless a repository overrides
it". Issue and PR templates, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md` are inherited by every
repo. `tests/test_profile.py` already enforces cross-repo invariants (every repo in the brand
manifest has a profile row, DI table ordering).

**Per repo**, measured over the 28 checkouts:

| Convention | Coverage |
|---|---|
| `CLAUDE.md` is exactly `@AGENTS.md` | 28/28 |
| `AGENTS.md` present | 28/28 |
| `CONTEXT.md` glossary (single-context, "_Avoid_" synonyms) | 25/28 (missing: both templates, `that-depends`) |
| `docs/adr/` with at least one record | 25/28 (same three missing) |
| `docs/agents/` (`domain.md`, `issue-tracker.md`, `triage-labels.md`) | 7/28 |
| `justfile` with `install / lint / lint-ci / test / publish` | 28/28 (`that-depends` adds `hook`, `docs`) |
| ruff `line-length = 120`, `select = ["ALL"]` | 27/27 repos with a ruff config |
| Type checker `ty` | 27/28 (`that-depends`: mypy strict + pyrefly, deliberately) |
| `uv_build` backend | 24/28 (templates, `chat-app`, this repo are not packages) |
| `eof-fixer` in `lint` recipe | 26/28 (`that-depends`, this repo) |
| 100 % coverage gate somewhere | 26/28 (`that-depends` and this repo have none) |
| Tag-driven `release.yml` with PyPI Trusted Publishing (OIDC) | 22/28 (`that-depends` still `publish.yml` on release-published; non-packages have none) |
| Weekly `scheduled.yml` re-running `_checks.yml` | 24/28 |
| lychee `--offline` local-link job | present in most `_checks.yml` |

**Drift, measured:**

- **ruff ignore lists: seven distinct sets.** Base (`D1 S101 TCH FBT D203 D213 COM812 ISC001 CPY001`):
  `modern-di`, `compose2pod`, `eof-fixer`, `httpware`. Base + `G004`: all 13 `modern-di-*`, `db-retry`,
  `lite-bootstrap`. FastStream flavour (`TRY003 EM102 G004`, no `S101`/`TCH`):
  `faststream-concurrent-aiokafka`; plus `ANN` in `faststream-outbox`, `faststream-redis-timers`.
  `semvertag` (`TRY003 EM102 S105`). Templates (`INP B008 ANN204 RUF001 S105`, `chat-app` adds
  `TC001-3`). `that-depends` (`B008 D100 D105 S311 PT028`). Nothing records which of these is policy
  and which is accident.
- **Python floor:** `>=3.10` in 18 repos, `>=3.11` in 7, `>=3.14` in 3.
- **`justfile`:** 11 byte-identical (the `modern-di-*` integrations except `arq` and `grpc`), 17 other
  variants. The variation is real (docker-compose test runners, docs recipes, benchmarks) but the
  shared core is copied, not referenced.
- **`_checks.yml`:** 24 copies, 12 byte-identical. The other 12 vary in: service containers (redis,
  postgres, redpanda), an added `docs` job, the lint-job Python pin (3.10 / 3.11 / 3.13), and how
  tests are invoked (`just test-ci` vs `just test --cov-report xml` vs raw `uv run pytest`).
- **`release.yml`:** 22 copies; 20 are identical apart from one comment naming the PyPI project.
  `compose2pod` and `semvertag` differ substantively.
- **Coverage gate location:** 15 repos gate in the `justfile` (`test-ci`), 11 in
  `[tool.coverage] fail_under`, so "does this repo gate coverage" has no single place to look.
- **Duplicated `AGENTS.md` prose**, verbatim across repos: "Real work not scheduled becomes a GitHub
  issue" (26), the `INVARIANT:` paragraph (25), the absolute-README-links rule (25), "the justfile is
  the source of truth" (23), the `# ty: ignore` note (18). These are org standards written 25 times.

**One inaccuracy found.** `AGENTS.md` here says the profile's static `coverage 100%` badge holds
"because every repo's CI enforces a 100%-coverage guard". `that-depends` has no such guard: its
`_checks.yml` uploads to codecov without `--cov-fail-under`, and neither its `justfile` nor its
`pyproject.toml` sets one.

## 3. The actual gap

community-of-python's standard is one written thing that other repos *reference* (a URL in a
workflow, a skill that clones the guide). modern-python's standard is real and stricter (100 %
coverage, `ty`, `eof-fixer`, ADRs, glossaries, invariant tests) but exists only as 28 copies with no
canonical text, so nobody can point to it, and drift has no reference to be measured against.

"Similar thing" therefore means two deliverables, not one: **(a)** a written standard, and **(b)** a
reference mechanism to replace copy-paste where a mechanism exists. Section 4 is what mechanisms
actually exist; section 5 is what to do.

## 4. Mechanisms, verified against their sources

- **Shared ruff config: not possible by reference.** `ruff config extend` (ruff 0.16.4): "A path to a
  local `pyproject.toml` or `ruff.toml` file to merge into this configuration." No URL, no package.
  The shared config has to be copied (template) and checked (census), as pylines does by hand.
- **Custom lint rules: only via flake8.** Ruff FAQ, quoted above. modern-python's own cross-cutting
  rules are already pytest invariants (`tests/test_docs_slug_census.py` in `modern-di`,
  `tests/test_profile.py` here), which is a better fit for repo-specific rules than a linter plugin.
- **Reusable workflows for checks: possible.** `_checks.yml` is already `on: workflow_call`; moving it
  to an org repo changes the caller to `uses: modern-python/<repo>/.github/workflows/checks.yml@<ref>`.
  GitHub docs: same-org callers may pass `secrets: inherit`; permissions "can only be maintained or
  reduced—not elevated—throughout the chain"; a called job may declare `environment:` and it resolves
  in the caller's repo
  ([docs.github.com reuse-workflows](https://docs.github.com/en/actions/how-tos/sharing-automations/reuse-workflows)).
  The hard part is the five repos whose `pytest` job needs a service container; those either keep a
  local file or the shared workflow grows a second entry point.
- **Reusable workflow for release: not possible today.** PyPI: "Reusable workflows cannot currently
  be used as the workflow in a Trusted Publisher. This is a practical limitation, and is being
  tracked in warehouse#11096"
  ([docs.pypi.org troubleshooting](https://docs.pypi.org/trusted-publishers/troubleshooting/)).
  [pypi/warehouse#11096](https://github.com/pypi/warehouse/issues/11096) was opened 2022-04-01 and is
  still open; the maintainers' 2025-05-20 comment is pseudocode for a *possible* future migration.
  community-workflow sidesteps this because it publishes with a `PYPI_TOKEN`, which the org moved
  away from. A commenter (ekohl, 2025-05-12) reports a composite action works because "a composite
  action doesn't create a new context", so the release steps could be shared as an action while each
  repo keeps a thin `release.yml`. Given that 20 of 22 copies differ by one comment, leaving
  `release.yml` per repo is also defensible.
- **Template with updates: copier.** `copier update` needs `.copier-answers.yml` in the generated
  project and git tags on the template; it regenerates from the new template version, diffs, and
  writes conflicts inline or as `.rej` files, "you should review those manually before committing"
  ([copier docs](https://copier.readthedocs.io/en/stable/updating/)). The 11 byte-identical
  `modern-di-*` repos are the obvious first tenants.
- **Agent skill: the pylines pattern applies unchanged.** `SKILL.md` + a `sync.sh` that clones the
  standard. modern-python already routes agents through `AGENTS.md → docs/agents/`; an org-level
  `docs/agents/` in this repo plus a one-line pointer in each `AGENTS.md` removes the 25× duplication
  without a skill at all, at the cost that agents only see it when they follow the link.

## 5. Options and assessment

1. **Write the standard, in this repo.** `docs/standards/` (or one page), published on
   modern-python.org next to the catalog. Content is what section 2 measured, not a pylines clone:
   the toolchain and pinned recipe names; the canonical ruff ignore list with one-line rationale per
   entry (pylines' best idea); the coverage gate and where it lives; `CONTEXT.md` / `docs/adr/` /
   `docs/agents/` layout; the `INVARIANT:` convention; README absolute links; tag-driven release
   and PEP 440 pre-release form; metadata rules already in `AGENTS.md`. Skip pylines' identifier
   rules (8-char names, verb-only functions, `one_` prefixes): nothing in the org enforces them and
   the libraries are not written that way. English, because the audience is external contributors.
   Cost: low. This is the prerequisite for everything below, because the other options need a
   reference to converge on.
2. **Shared `checks.yml` and `scheduled.yml` as reusable workflows.** Replaces 12 identical copies
   outright and 7 near-identical ones with a caller of ~5 lines. Pin callers to a tag, not `main`,
   or a workflow change becomes a 24-repo incident. Exempt: `that-depends` (its `AGENTS.md` says it
   diverges deliberately), the two templates and `chat-app` (docker-compose runners). Cost: medium;
   payoff grows with every new integration.
3. **A copier template for a library repo.** Solves `justfile`, `pyproject` ruff/coverage blocks,
   `release.yml`, `AGENTS.md` skeleton, `docs/agents/` in one place, with `copier update` for drift.
   Cost: medium-high up front. Do after 1 and 2, when the canonical shapes are settled.
4. **A drift census in this repo.** A test in the style of `test_profile.py` that reads each repo's
   `pyproject.toml`, `justfile` and `_checks.yml` (via `gh api` contents or local checkouts) and
   asserts the standard: ignore list ⊆ canonical, coverage gate present, recipe names present.
   Cheap once 1 exists; turns the standard from prose into an invariant, which is how this org
   already treats what must stay true.
5. **A custom lint plugin.** Not recommended. The org's rules that ruff cannot express are
   repo-specific and already pytest invariants; a flake8 dependency for zero rules is cost only.

**Suggested order:** 1 → 4 → 2 → 3. Skip 5.

## 6. Decisions only the maintainer can make

- Which ruff ignore set is canonical. Concretely: is `G004` (f-strings in logging) allowed org-wide?
  Are `TRY003`/`EM102` (exception messages) allowed, as the FastStream repos assume? Is `ANN` off in
  `faststream-outbox` and `faststream-redis-timers` on purpose? Is `S101` (assert) allowed
  everywhere, as the base set does, or only in `tests/`, as pylines does?
- Python floor policy: `>=3.10` for libraries and `>=3.11` only where a dependency forces it, or a
  single org floor.
- Coverage gate home: `justfile test-ci` (15 repos) or `[tool.coverage] fail_under` (11 repos).
- Whether `that-depends` is exempt from the standard or should gain the coverage gate the profile
  already claims for it.
- Whether templates and `chat-app` are in scope, or the standard covers libraries only.
- Whether the standard is a public site page or repo-internal docs.

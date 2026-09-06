# modern-python org conventions

The conventions below apply across **all** repos in the `modern-python` org, not
just this one. [`CONTEXT.md`](CONTEXT.md) says what this repo is and owns the
vocabulary — read it before naming a mark, a colourway, or a surface.

## Naming & branding

- Brand/framework casing — use exactly: `modern-di`, `that-depends`, `Litestar`
  (not "LiteStar"), `FastStream`, `FastAPI`, `Typer`, `SQLAlchemy`, `PostgreSQL`.
- Per-project docs sites live at `<name>.modern-python.org` (only some repos have one).

## Repository metadata (three surfaces kept consistent)

Every repo's summary appears in up to three places — keep them saying the same thing:
the **GitHub description**, the pyproject **`description`**, and the repo's blurb in
`profile/README.md`. Write one canonical one-liner per repo: purpose-first,
≤ ~120 chars, **no trailing period** (GitHub convention).

### GitHub topics
- Lowercase letters/numbers/hyphens only, ≤50 chars each, ≤12 per repo.
- Draw from the shared org vocabulary so `/topics/*` pages cluster: `python`,
  `dependency-injection`, `di`, `ioc-container`, `modern-di`, `fastapi`, `litestar`,
  `faststream`, `sqlalchemy`, `postgresql`, `asyncio`, `docker`, `cli`, `messaging`.
- `modern-di-*` integrations share a base set
  (`python, dependency-injection, di, ioc-container, modern-di`) plus their framework.
- Also set the repo **website field** to its docs site, or `modern-python.org` if none.

### pyproject `[project]`
- **`keywords`** mirror the GitHub topics (lowercase/hyphenated). Never use
  `"dependency injector"` — that is another package's name (`dependency-injector`).
- **`classifiers`**: include `Development Status :: <level>`,
  `Intended Audience :: Developers`, the relevant `Programming Language :: Python ::`
  versions, `Typing :: Typed`, and a `Topic ::` where apt. Validate every string
  against <https://pypi.org/classifiers/> before committing.
- **Do NOT add a `License :: OSI Approved :: ...` classifier.** All repos are MIT and
  declare the SPDX `license = "MIT"` key; PEP 639 deprecates pairing that with a
  License classifier, and `uv_build` warns on it.
- **`[project.urls]`** uses PyPI well-known labels (capitalized):
  `Homepage`, `Documentation` (only if a docs site exists), `Repository`,
  `Issues` (`…/issues`), `Changelog` (`…/releases`).

The PyPI distribution name equals the repo name, for every package. The org
profile's `coverage 100%` badge is static and deliberately unlinked — the claim holds
because every repo's CI enforces a 100%-coverage guard, and there is no org-level
coverage URL to point at.

A repo may be listed on the org profile **before** its package reaches PyPI. Its
Downloads badge 404s until pepy indexes it; the Stars badge and repo link resolve
meanwhile. That lag is self-healing — note it, never block the listing on it.

## Brand surfaces

A repo's brand assets are generated here, in `brand/projects/<repo>/`. Which of them a
repo hotlinks and which it vendors is settled in
[`docs/adr/0003-docs-vendor-assets-readmes-hotlink.md`](docs/adr/0003-docs-vendor-assets-readmes-hotlink.md).

A docs site's `docs/index.md` replaces its `# <Title>` heading with a `.mp-hero` block
holding both lockup variants. Add no `title:` front matter there: Material titles the
home page from `site_name`, so `title:` renders as `<repo> - <repo>`.

## Tooling

Projects use **uv** (packaging), **ruff** (lint/format), **ty** (type check), and
the build backend is **uv_build**. `that-depends` additionally runs `mypy` and
`pyrefly` in its `lint-ci` recipe. Lint/test live behind a `justfile` in most repos.

## CI gotcha

GitHub occasionally type-checks a **stale `refs/pull/<n>/merge`** after a push, so a
PR can show an old lint/test failure that no longer matches the branch. Confirm by
running the failing check locally at the branch HEAD (with the pinned tool version);
if it's clean, push a fresh commit to force GitHub to recompute the merge ref.

## Workflow

**The spec for a change is its PR body**, not a committed file: why, design,
non-goals, verification, reviewed with the diff. There is no change file, no lane to
choose, and no `planning/` tree. A trivial PR (typo, dep bump, formatter, CI tweak)
ships a conventional-commit title with no body ceremony.

> This repo's `.github/PULL_REQUEST_TEMPLATE.md` is the **org default**, inherited by
> every repo without a local one, and most of them still run the older `planning/`
> convention — so it still carries the generic form. Replacing it is tracked
> separately; write PR bodies in the shape above regardless.

Two things outlive the PR, and there are exactly two places to put them: an
alternative **rejected** with reasoning becomes an ADR in [`docs/adr/`](docs/adr/)
(`NNNN-slug.md`, sequential, with a revisit trigger), and real work **not scheduled**
becomes a GitHub issue. There is no third state and no truth-home directory — a
change to a mark, a badge, or a page is reviewed with the diff, not promoted to a page.

## Where a fact goes

Four homes, one owner each:

| Home | Holds |
|---|---|
| `brand/`, `profile/`, `mkdocs.yml` | anything readable from the source — the default |
| a named test | an **invariant**: must stay true, and a change could silently break it |
| `docs/adr/` | a rejected alternative, with the reasoning that would otherwise be re-litigated |
| `docs/`, `profile/README.md` | anything a user needs |

Before writing a line anywhere:

> Can an agent get this by reading the source? → **don't write it.**
> Would a wrong change here fail a test? → it belongs **in the test**, not in prose.
> Does a user need it? → **`docs/`**.
> Otherwise it does not get written.

**Prose about mechanism has no home. There is no file to add a paragraph to.** This
file included: it is always loaded, so a line restating a docstring, a justfile
comment, or `mkdocs.yml` costs every turn and rots in two places at once.

An invariant is a test whose name is the claim, with a docstring opening `INVARIANT:`
and a second paragraph naming **what breaks it** — design rationale, not a report of
what this one test catches. `tests/test_invariant_census.py` enforces that shape, and
checks that every test name and ADR path cited from the source or from the Markdown
outside `docs/` resolves. Both ADRs and
`INVARIANT:` docstrings ratchet: nothing prunes a record once its call is settled.
Keeping them lean is a standing habit.

## Agent skills

- **Issues and specs** — GitHub Issues on `modern-python/.github`, via `gh`:
  [`docs/agents/issue-tracker.md`](docs/agents/issue-tracker.md)
- **Triage labels** — the five canonical roles: [`docs/agents/triage-labels.md`](docs/agents/triage-labels.md)
- **Domain docs** — single-context, `CONTEXT.md` + `docs/adr/`:
  [`docs/agents/domain.md`](docs/agents/domain.md)

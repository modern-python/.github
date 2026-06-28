# modern-python org conventions

This repo (`modern-python/.github`) builds the org site at **modern-python.org**
(MkDocs Material, in `docs/`) and hosts the org profile shown on the GitHub org page
(`profile/README.md`). The conventions below apply across **all** repos in the
`modern-python` org, not just this one.

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

Planning follows the convention in [`planning/README.md`](planning/README.md) —
its **Quick path** is authoritative. Pick a lane (Full = `design.md` + `plan.md`,
Lightweight = `change.md`, Tiny = conventional commit), create a bundle under
`planning/changes/YYYY-MM-DD.NN-<slug>/` from `planning/_templates/`, and run
`just check-planning` before pushing. The applied convention version is in
`planning/.convention-version`; update it via the canonical repo's `APPLY.md`.

## Architecture

`architecture/` (repo root) is the living truth about what this repo does now —
one file per capability plus `glossary.md`, no frontmatter, authored lazily.
**When a change alters a capability's behavior, update the matching
`architecture/<capability>.md` in the same PR.** The change bundle in
`planning/changes/` stays as the *why*.

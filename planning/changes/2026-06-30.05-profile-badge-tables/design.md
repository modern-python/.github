---
summary: Rework profile/README.md into a metrics-forward layout — org-standards badge strip plus per-category project tables with live per-repo badges.
---

# Design: Profile README badge tables

## Summary

Replace the prose bullet lists in `profile/README.md` with a metrics-forward
layout: an org-standards badge strip (uv · Ruff · ty · coverage 100%) directly
under the wordmark banner, then the same four category groupings rendered as
three-column tables (`Project | What it is | Badges`). Each published-package row
carries live badges — GitHub stars, PyPI version, monthly downloads, and a
Context7 docs link where one exists. The two project templates get their own
PyPI-column-free table so no empty/ragged cells appear. The prose tooling footer
is dropped (now redundant with the top strip).

## Motivation

The current profile is a clean grouped bullet list, but it surfaces zero signal
about project health or adoption — no versions, no downloads, no stars. The
maintainer wants the org landing page to read as metrics-forward, matching the
badge strips already present in every repo README (`modern-di`'s README even
carries a project table already, so the pattern has internal precedent).

Two research sweeps (saved findings in this bundle's history) established the
guardrails:
- No surveyed org (astral-sh, pydantic, encode, prisma, grafana, langchain,
  vercel, supabase, …) puts a per-repo badge **table** in its org profile; the
  common pattern is a grouped link list with at most headline badges. Adopting a
  table is a deliberate, distinctive choice.
- The dominant failure mode of metrics in profiles is **staleness** — hand-typed
  star/repo counts rot (github's "4357 repositories", n8n's `~70k~ 80k`). This
  design uses **only live shields** for every number, so nothing rots.
- Per-repo badge tables concentrate maintenance/breakage on the highest-traffic
  page. Mitigated by: per-category tables, a separate template table (no empty
  cells), flat badge style for row alignment, and `static.pepy.tech` (baked SVG)
  instead of the flaky shields `pypi/dm` downloads endpoint.

## Non-goals

- Not changing the wordmark `<picture>` banner or the tagline.
- Not adding badges to the per-repo READMEs (they already have them).
- Not adding a Python-versions badge (cut for noise reduction).
- Not adding coverage as a per-row column — coverage is a single org-wide top
  badge, justified by every repo's CI 100%-coverage guard.
- Not adding CI / license / social / Discord badges to the profile.

## Design

### 1. Page structure (top to bottom)

1. Wordmark `<picture>` banner — unchanged.
2. Tagline paragraph — unchanged.
3. **Org-standards badge strip** (new) — a single line of four badges:
   `uv` · `Ruff` · `ty` · `coverage 100%`.
4. Four category sections, each a markdown table (order unchanged):
   **Project templates**, **Dependency injection**,
   **Microservices, HTTP & messaging**, **Utilities**.
5. Footer prose ("Projects … built with uv, ruff, ty") — **removed**.

### 2. Org-standards badge strip

Represents what is true of every repo. Tooling badges reuse the exact Astral
endpoint snippets already in the repo READMEs; coverage is a static badge
justified by the org-wide CI 100% guard (no org-level coverage URL exists, so it
renders unlinked).

```markdown
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
```

### 3. Published-package tables (DI, Microservices, Utilities)

Three columns. The blurb column reuses the canonical ≤120-char one-liner already
in the profile (preserving the description metadata surface). The badge cell is a
flat-style strip in a fixed order: **stars · version · downloads · Context7**.

| Column | Content |
|--------|---------|
| `Project` | repo name as inline code, linked to the GitHub repo |
| `What it is` | canonical one-liner (reused from the old profile, sentence-cased with trailing punctuation stripped) |
| `Badges` | stars · PyPI version · downloads/mo · Context7 (if a page exists) |

Per-badge templates (`REPO` = GitHub repo name, `PKG` = PyPI distribution name):

```markdown
[![Stars](https://img.shields.io/github/stars/modern-python/REPO)](https://github.com/modern-python/REPO/stargazers)
[![PyPI](https://img.shields.io/pypi/v/PKG)](https://pypi.org/project/PKG/)
[![Downloads](https://static.pepy.tech/badge/PKG/month)](https://pepy.tech/projects/PKG)
[![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/REPO)
```

All badges use flat (default) style — never `style=social` — so badge heights
match and rows align.

Category membership (from the current profile):
- **Dependency injection:** `modern-di`, `modern-di-fastapi`,
  `modern-di-litestar`, `modern-di-faststream`, `modern-di-typer`,
  `modern-di-pytest`, `that-depends`.
- **Microservices, HTTP & messaging:** `lite-bootstrap`, `httpware`,
  `faststream-redis-timers`, `faststream-concurrent-aiokafka`,
  `faststream-outbox`.
- **Utilities:** `db-retry`, `eof-fixer`, `semvertag`.

### 4. Templates table (PyPI-column-free)

`fastapi-sqlalchemy-template` and `litestar-sqlalchemy-template` are not
published to PyPI (verified: PyPI returns 404), so they get a separate table
whose badge cell is **stars + Context7 + a static `type: template` chip** — no
version/downloads columns, so no empty cells. Both templates have a Context7
page (verified 200), so the Context7 badge applies under the "include where a
page exists" rule.

```markdown
[![Stars](https://img.shields.io/github/stars/modern-python/REPO)](https://github.com/modern-python/REPO/stargazers)
[![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/REPO)
![Template](https://img.shields.io/badge/type-template-blue)
```

### 5. Per-repo verification (done at design time, re-confirm at ship)

Verified on 2026-06-30 (PyPI `…/pypi/<pkg>/json`, Context7
`context7.com/modern-python/<repo>`):
- **PyPI distribution name == repo name** for every package (read from each
  `pyproject.toml` `[project].name`).
- **All 15 library repos** return PyPI 200 and Context7 200 → full strip
  (stars · version · downloads · Context7).
- **Both templates** return PyPI 404 (stars-only, no version/downloads) and
  Context7 200 (Context7 badge applies).

Re-confirm badge/link liveness at ship (a package could be yanked between
design and merge); any repo that has become unpublished drops to stars-only.

## Operations

None out-of-repo. All badges are third-party hosted (shields.io, pepy.tech,
context7.com); no assets are added to this repo.

## Testing

- Render-check the rewritten `profile/README.md` on a GitHub branch (the org
  profile renders in a narrow column — confirm tables do not force a horizontal
  scrollbar and badge rows align).
- Verify every badge image returns HTTP 200 `image/svg+xml` and every link
  target resolves (stars → stargazers, version/downloads → PyPI/pepy,
  Context7 → an existing page).
- Promote into architecture: add a new `architecture/org-profile.md` capturing
  the profile's structure (banner → tagline → standards strip → per-category
  tables → templates table), edited in the same PR per the promotion rule.
- `just check-planning` passes before pushing.

## Risk

- **Badge breakage on the highest-traffic page** (likely × moderate). A renamed
  repo, yanked package, or upstream badge-host outage shows a broken image on the
  org landing page. Mitigated by all-live shields with stable hosts
  (`static.pepy.tech` baked SVG, Astral endpoint JSON) and per-repo verification
  before ship; residual risk accepted as the cost of a metrics-forward profile.
- **Width overflow** (moderate × low). Three columns + a multi-badge strip could
  scroll on the narrow profile column. Mitigated by cutting pyversions/coverage
  from rows and keeping the strip to four badges max; confirmed in the render
  check.
- **Wrong PKG name → 404 badge** (low, gated by verification). The implementation
  verification step catches mismatches before commit.

# profile-badge-tables — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rework `profile/README.md` into an org-standards badge strip plus
per-category project tables with live per-repo badges.

**Spec:** [`design.md`](./design.md)

**Branch:** `profile-badge-tables` (already created; the design spec is committed there)

**Commit strategy:** Per-task commits.

## Global Constraints

- Brand casing exactly: `modern-di`, `that-depends`, `Litestar`, `FastStream`,
  `FastAPI`, `Typer`, `pytest`, `SQLAlchemy`, `PostgreSQL`, `aiokafka`.
- Blurbs: purpose-first, no trailing period (GitHub convention).
- All badges use shields/pepy **flat (default) style** — never `?style=social`
  (keeps badge heights equal so table rows align).
- Downloads badge uses `static.pepy.tech/...badge/<pkg>/month` (baked SVG), never
  shields `pypi/dm` (flaky).
- Verified 2026-06-30: every library repo is on PyPI (dist name == repo name) and
  has a Context7 page; both templates are 404 on PyPI but have Context7 pages.
- Do not touch the wordmark `<picture>` banner or the tagline paragraph.

---

### Task 1: Rewrite `profile/README.md`

**Files:**
- Modify: `profile/README.md` (full replacement of body below the tagline; banner
  + tagline kept verbatim)

**Interfaces:**
- Consumes: nothing.
- Produces: the rewritten profile page consumed by Task 2 (link/badge
  verification) and described by Task 3 (`architecture/org-profile.md`).

Replace the entire file with the content in Step 1. Banner and tagline are
unchanged; everything after the tagline is the new badge strip + four tables.

- [ ] **Step 1: Write the new `profile/README.md`**

Write `profile/README.md` with exactly this content:

```markdown
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/modern-python/.github/main/brand/org/wordmark-dark.svg">
    <img alt="Modern Python" src="https://raw.githubusercontent.com/modern-python/.github/main/brand/org/wordmark.svg" width="360">
  </picture>
</p>

Open-source templates and libraries for building production-ready Python applications — web services, microservices, and the dependency injection that wires them together.

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

### Project templates

| Project | What it is | Badges |
|---|---|---|
| [`fastapi-sqlalchemy-template`](https://github.com/modern-python/fastapi-sqlalchemy-template) | Dockerized web application with DI on FastAPI, SQLAlchemy 2, PostgreSQL | [![Stars](https://img.shields.io/github/stars/modern-python/fastapi-sqlalchemy-template)](https://github.com/modern-python/fastapi-sqlalchemy-template/stargazers) [![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/fastapi-sqlalchemy-template) ![Template](https://img.shields.io/badge/type-template-blue) |
| [`litestar-sqlalchemy-template`](https://github.com/modern-python/litestar-sqlalchemy-template) | Dockerized web application on Litestar, SQLAlchemy 2, PostgreSQL | [![Stars](https://img.shields.io/github/stars/modern-python/litestar-sqlalchemy-template)](https://github.com/modern-python/litestar-sqlalchemy-template/stargazers) [![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/litestar-sqlalchemy-template) ![Template](https://img.shields.io/badge/type-template-blue) |

### Dependency injection

| Project | What it is | Badges |
|---|---|---|
| [`modern-di`](https://github.com/modern-python/modern-di) | Powerful DI framework with scopes | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di)](https://github.com/modern-python/modern-di/stargazers) [![PyPI](https://img.shields.io/pypi/v/modern-di)](https://pypi.org/project/modern-di/) [![Downloads](https://static.pepy.tech/badge/modern-di/month)](https://pepy.tech/projects/modern-di) [![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/modern-di) |
| [`modern-di-fastapi`](https://github.com/modern-python/modern-di-fastapi) | modern-di integration for FastAPI | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-fastapi)](https://github.com/modern-python/modern-di-fastapi/stargazers) [![PyPI](https://img.shields.io/pypi/v/modern-di-fastapi)](https://pypi.org/project/modern-di-fastapi/) [![Downloads](https://static.pepy.tech/badge/modern-di-fastapi/month)](https://pepy.tech/projects/modern-di-fastapi) [![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/modern-di-fastapi) |
| [`modern-di-litestar`](https://github.com/modern-python/modern-di-litestar) | modern-di integration for Litestar | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-litestar)](https://github.com/modern-python/modern-di-litestar/stargazers) [![PyPI](https://img.shields.io/pypi/v/modern-di-litestar)](https://pypi.org/project/modern-di-litestar/) [![Downloads](https://static.pepy.tech/badge/modern-di-litestar/month)](https://pepy.tech/projects/modern-di-litestar) [![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/modern-di-litestar) |
| [`modern-di-faststream`](https://github.com/modern-python/modern-di-faststream) | modern-di integration for FastStream | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-faststream)](https://github.com/modern-python/modern-di-faststream/stargazers) [![PyPI](https://img.shields.io/pypi/v/modern-di-faststream)](https://pypi.org/project/modern-di-faststream/) [![Downloads](https://static.pepy.tech/badge/modern-di-faststream/month)](https://pepy.tech/projects/modern-di-faststream) [![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/modern-di-faststream) |
| [`modern-di-typer`](https://github.com/modern-python/modern-di-typer) | modern-di integration for Typer | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-typer)](https://github.com/modern-python/modern-di-typer/stargazers) [![PyPI](https://img.shields.io/pypi/v/modern-di-typer)](https://pypi.org/project/modern-di-typer/) [![Downloads](https://static.pepy.tech/badge/modern-di-typer/month)](https://pepy.tech/projects/modern-di-typer) [![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/modern-di-typer) |
| [`modern-di-pytest`](https://github.com/modern-python/modern-di-pytest) | modern-di integration for pytest | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-pytest)](https://github.com/modern-python/modern-di-pytest/stargazers) [![PyPI](https://img.shields.io/pypi/v/modern-di-pytest)](https://pypi.org/project/modern-di-pytest/) [![Downloads](https://static.pepy.tech/badge/modern-di-pytest/month)](https://pepy.tech/projects/modern-di-pytest) [![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/modern-di-pytest) |
| [`that-depends`](https://github.com/modern-python/that-depends) | Predecessor DI framework, still actively maintained | [![Stars](https://img.shields.io/github/stars/modern-python/that-depends)](https://github.com/modern-python/that-depends/stargazers) [![PyPI](https://img.shields.io/pypi/v/that-depends)](https://pypi.org/project/that-depends/) [![Downloads](https://static.pepy.tech/badge/that-depends/month)](https://pepy.tech/projects/that-depends) [![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/that-depends) |

### Microservices, HTTP & messaging

| Project | What it is | Badges |
|---|---|---|
| [`lite-bootstrap`](https://github.com/modern-python/lite-bootstrap) | Lightweight package for bootstrapping new microservices | [![Stars](https://img.shields.io/github/stars/modern-python/lite-bootstrap)](https://github.com/modern-python/lite-bootstrap/stargazers) [![PyPI](https://img.shields.io/pypi/v/lite-bootstrap)](https://pypi.org/project/lite-bootstrap/) [![Downloads](https://static.pepy.tech/badge/lite-bootstrap/month)](https://pepy.tech/projects/lite-bootstrap) [![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/lite-bootstrap) |
| [`httpware`](https://github.com/modern-python/httpware) | HTTP client framework with sync/async clients, middleware chain, and built-in resilience (retry, bulkhead) | [![Stars](https://img.shields.io/github/stars/modern-python/httpware)](https://github.com/modern-python/httpware/stargazers) [![PyPI](https://img.shields.io/pypi/v/httpware)](https://pypi.org/project/httpware/) [![Downloads](https://static.pepy.tech/badge/httpware/month)](https://pepy.tech/projects/httpware) [![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/httpware) |
| [`faststream-redis-timers`](https://github.com/modern-python/faststream-redis-timers) | FastStream broker integration for Redis-backed distributed timer scheduling | [![Stars](https://img.shields.io/github/stars/modern-python/faststream-redis-timers)](https://github.com/modern-python/faststream-redis-timers/stargazers) [![PyPI](https://img.shields.io/pypi/v/faststream-redis-timers)](https://pypi.org/project/faststream-redis-timers/) [![Downloads](https://static.pepy.tech/badge/faststream-redis-timers/month)](https://pepy.tech/projects/faststream-redis-timers) [![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/faststream-redis-timers) |
| [`faststream-concurrent-aiokafka`](https://github.com/modern-python/faststream-concurrent-aiokafka) | Concurrent message processing middleware for FastStream with aiokafka | [![Stars](https://img.shields.io/github/stars/modern-python/faststream-concurrent-aiokafka)](https://github.com/modern-python/faststream-concurrent-aiokafka/stargazers) [![PyPI](https://img.shields.io/pypi/v/faststream-concurrent-aiokafka)](https://pypi.org/project/faststream-concurrent-aiokafka/) [![Downloads](https://static.pepy.tech/badge/faststream-concurrent-aiokafka/month)](https://pepy.tech/projects/faststream-concurrent-aiokafka) [![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/faststream-concurrent-aiokafka) |
| [`faststream-outbox`](https://github.com/modern-python/faststream-outbox) | FastStream broker integration for the transactional outbox pattern with Postgres | [![Stars](https://img.shields.io/github/stars/modern-python/faststream-outbox)](https://github.com/modern-python/faststream-outbox/stargazers) [![PyPI](https://img.shields.io/pypi/v/faststream-outbox)](https://pypi.org/project/faststream-outbox/) [![Downloads](https://static.pepy.tech/badge/faststream-outbox/month)](https://pepy.tech/projects/faststream-outbox) [![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/faststream-outbox) |

### Utilities

| Project | What it is | Badges |
|---|---|---|
| [`db-retry`](https://github.com/modern-python/db-retry) | Retry helpers for PostgreSQL / SQLAlchemy database operations | [![Stars](https://img.shields.io/github/stars/modern-python/db-retry)](https://github.com/modern-python/db-retry/stargazers) [![PyPI](https://img.shields.io/pypi/v/db-retry)](https://pypi.org/project/db-retry/) [![Downloads](https://static.pepy.tech/badge/db-retry/month)](https://pepy.tech/projects/db-retry) [![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/db-retry) |
| [`eof-fixer`](https://github.com/modern-python/eof-fixer) | Automatically fix newlines at the end of files | [![Stars](https://img.shields.io/github/stars/modern-python/eof-fixer)](https://github.com/modern-python/eof-fixer/stargazers) [![PyPI](https://img.shields.io/pypi/v/eof-fixer)](https://pypi.org/project/eof-fixer/) [![Downloads](https://static.pepy.tech/badge/eof-fixer/month)](https://pepy.tech/projects/eof-fixer) [![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/eof-fixer) |
| [`semvertag`](https://github.com/modern-python/semvertag) | Auto-tag your GitHub/GitLab repo with semantic version tags from CI | [![Stars](https://img.shields.io/github/stars/modern-python/semvertag)](https://github.com/modern-python/semvertag/stargazers) [![PyPI](https://img.shields.io/pypi/v/semvertag)](https://pypi.org/project/semvertag/) [![Downloads](https://static.pepy.tech/badge/semvertag/month)](https://pepy.tech/projects/semvertag) [![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/semvertag) |
```

- [ ] **Step 2: Verify structure locally**

  Run:
  ```bash
  cd /Users/kevinsmith/src/pypi/modern-python
  grep -c '^| \[' profile/README.md
  ```
  Expected: `17` (one linked-project row per repo: 2 templates + 7 DI + 5
  microservices + 3 utilities).

- [ ] **Step 3: Confirm no leftover prose footer / old bullets**

  Run:
  ```bash
  grep -n 'Projects in this organization are built with' profile/README.md || echo "footer removed (ok)"
  ```
  Expected: `footer removed (ok)`.

- [ ] **Step 4: Commit**

  ```bash
  git add profile/README.md
  git commit -m "docs(profile): badge tables per category + org-standards strip"
  ```

---

### Task 2: Verify every badge image and link target is live

**Files:**
- None modified unless a check fails (then fix `profile/README.md`).

**Interfaces:**
- Consumes: `profile/README.md` from Task 1.
- Produces: confidence that no badge renders broken on the org landing page.

- [ ] **Step 1: Check every badge image URL returns 200**

  Run:
  ```bash
  cd /Users/kevinsmith/src/pypi/modern-python
  grep -oE 'https://[^)]*\.json|https://img\.shields\.io[^)]*|https://static\.pepy\.tech[^)]*' profile/README.md \
    | sort -u \
    | while read -r u; do printf "%s %s\n" "$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$u")" "$u"; done
  ```
  Expected: every line starts with `200`. (shields version/downloads/stars
  endpoints answer 200 even for brand-new packages.)

- [ ] **Step 2: Check every link target resolves**

  Run:
  ```bash
  cd /Users/kevinsmith/src/pypi/modern-python
  grep -oE '\]\(https://(github\.com|pypi\.org|pepy\.tech|context7\.com)[^)]*\)' profile/README.md \
    | sed -E 's/^\]\(//; s/\)$//' | sort -u \
    | while read -r u; do printf "%s %s\n" "$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 -L "$u")" "$u"; done
  ```
  Expected: `200` for every GitHub, PyPI, pepy, and Context7 link. If any PyPI
  link is 404, that package is unpublished — drop its version/downloads badges
  and move the repo to a stars+Context7 row, then re-run.

- [ ] **Step 3: Commit only if a fix was needed**

  ```bash
  git add profile/README.md
  git commit -m "docs(profile): drop badges for unpublished repo"
  ```
  (Skip if Steps 1-2 were all 200.)

---

### Task 3: Promote into `architecture/org-profile.md`

**Files:**
- Create: `architecture/org-profile.md`

**Interfaces:**
- Consumes: the shipped `profile/README.md` structure.
- Produces: the living-truth capability page (no frontmatter, per the
  architecture convention).

- [ ] **Step 1: Write `architecture/org-profile.md`**

  Write this content:

```markdown
# Org profile README

`profile/README.md` is the org landing page shown on
[github.com/modern-python](https://github.com/modern-python). Living prose, no
frontmatter; dated by git.

## Structure (top to bottom)

1. **Wordmark banner** — centered `<picture>` (light/dark) referencing
   `brand/org/wordmark[-dark].svg` by absolute `raw.githubusercontent.com` URL.
2. **Tagline** — one paragraph: what the org builds.
3. **Org-standards badge strip** — `uv`, `Ruff`, `ty` (Astral endpoint badges,
   live) and a static `coverage 100%` badge. The coverage claim holds org-wide
   because every repo's CI enforces a 100%-coverage guard; it renders unlinked
   (there is no org-level coverage URL).
4. **Four category tables** — `Project | What it is | Badges`, in order:
   Project templates, Dependency injection, Microservices/HTTP & messaging,
   Utilities. The `What it is` column carries the canonical ≤120-char one-liner
   (one of the three metadata surfaces kept consistent across GitHub
   description, pyproject `description`, and this blurb).

## Badge rules

- **Published libraries** get a four-badge strip: GitHub stars → stargazers,
  PyPI version, monthly downloads (`static.pepy.tech/badge/<pkg>/month`), and a
  Context7 docs badge → `context7.com/modern-python/<repo>`.
- **Templates** (`*-sqlalchemy-template`, not on PyPI) get stars + Context7 + a
  static `Template` chip — no version/downloads columns, so no empty cells.
- All badges use flat (default) style so row heights align. Downloads use the
  pepy baked SVG, not the flaky shields `pypi/dm` endpoint. Every number is a
  live shield (no hand-typed stats that could go stale).
- PyPI distribution name equals the repo name for every package.

When a repo is added, removed, renamed, or unpublished, update the matching
table row here and in `profile/README.md` in the same PR.
```

- [ ] **Step 2: Commit**

  ```bash
  git add architecture/org-profile.md
  git commit -m "docs(architecture): add org-profile capability page"
  ```

---

### Task 4: Finalize planning bundle and open the PR

**Files:**
- Modify: `planning/changes/2026-06-30.05-profile-badge-tables/design.md`
  (finalize `summary:` only if the realized result differs)

**Interfaces:**
- Consumes: Tasks 1-3.
- Produces: a green `just check-planning` and an open PR.

- [ ] **Step 1: Run the planning check**

  Run:
  ```bash
  cd /Users/kevinsmith/src/pypi/modern-python
  just check-planning
  ```
  Expected: passes (exit 0). Fix any reported issue and re-run.

- [ ] **Step 2: Push the branch**

  ```bash
  git push -u origin profile-badge-tables
  ```

- [ ] **Step 3: Open the PR**

  ```bash
  gh pr create --base main --title "Profile README: badge tables per category" \
    --body "Reworks profile/README.md into an org-standards badge strip (uv/ruff/ty/coverage) plus per-category project tables with live per-repo badges (stars, version, downloads, Context7). Templates get a stars+Context7+chip row (not on PyPI). Spec + plan in planning/changes/2026-06-30.05-profile-badge-tables/.

🤖 Generated with [Claude Code](https://claude.com/claude-code)"
  ```

- [ ] **Step 4: Visual render-check**

  Open the rendered file on the branch:
  `https://github.com/modern-python/.github/blob/profile-badge-tables/profile/README.md`
  Confirm: all four tables render, badge rows align (equal heights), no broken
  image icons, and the badge strip wraps rather than forcing a wide horizontal
  scrollbar. If a row is too wide, the badge cell wraps naturally — only act if
  an image is broken or a column visibly overflows.

- [ ] **Step 5: Watch CI**

  ```bash
  gh pr checks --watch
  ```
  Expected: all checks green. If `check-planning` flakes on a stale merge ref,
  re-confirm locally at branch HEAD and push an empty commit to recompute.

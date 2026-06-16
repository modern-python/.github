# modern-python.org Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a green-branded GitHub Pages landing page for the `modern-python` org at the custom apex domain `modern-python.org`, built with MkDocs + Material and deployed via GitHub Actions, all living in this `.github` repo without touching `profile/README.md`.

**Architecture:** A MkDocs + Material project rooted in this repo. `docs/index.md` is a single landing page (layout C: centered intro → topic tiles → category sections) listing every org project. Dependencies are managed with `uv`. A GitHub Actions workflow builds with `mkdocs build --strict` and publishes via `actions/deploy-pages`. A `docs/CNAME` binds the apex domain. DNS and Pages-settings toggles are manual owner steps documented at the end.

**Tech Stack:** MkDocs, `mkdocs-material`, `uv`, GitHub Actions Pages, Markdown.

**Note on testing:** This is a static-site project — there is no unit-test runner. The TDD loop here is: define the expected build output / content, run `uv run mkdocs build --strict`, then assert on the generated `site/` files with `grep`. `--strict` fails the build on broken links, bad nav, or unresolved anchors, so it is the primary correctness gate.

---

## File structure

| File | Responsibility |
|------|----------------|
| `pyproject.toml` | uv project: declares `mkdocs-material` dependency, `requires-python`. |
| `mkdocs.yml` | Site config: name, theme, custom palette, logo/favicon, markdown extensions, `extra_css`. |
| `docs/index.md` | The homepage (intro + topic tiles + category sections). |
| `docs/stylesheets/extra.css` | Brand-green CSS variables + hero centering + tile tweaks. |
| `docs/assets/modern-python.png` | Org logo (moved from repo root); header logo + favicon source. |
| `docs/CNAME` | `modern-python.org` — copied to site root on every build. |
| `.github/workflows/deploy.yml` | Build with uv + deploy to Pages. |
| `profile/README.md` | UNCHANGED — GitHub org profile. |

---

## Task 1: Scaffold uv project + minimal buildable MkDocs site

**Files:**
- Create: `pyproject.toml`
- Create: `mkdocs.yml`
- Create: `docs/index.md` (stub, replaced in Task 4)

- [ ] **Step 1: Write `pyproject.toml`**

```toml
[project]
name = "modern-python-org"
version = "0.1.0"
description = "modern-python.org organization homepage"
requires-python = ">=3.11"
dependencies = [
    "mkdocs-material>=9.5",
]
```

- [ ] **Step 2: Write a minimal `mkdocs.yml`**

```yaml
site_name: Modern Python
site_url: https://modern-python.org/
site_description: Open-source templates and libraries for building production-ready Python applications.
repo_url: https://github.com/modern-python
repo_name: modern-python

theme:
  name: material
  features:
    - navigation.instant
    - navigation.top
    - search.suggest
    - content.action.edit
  palette:
    - scheme: default
      primary: custom
      accent: custom
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: custom
      accent: custom
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
```

- [ ] **Step 3: Write a stub `docs/index.md`**

```markdown
# Modern Python

Site under construction.
```

- [ ] **Step 4: Build and verify it succeeds**

Run: `uv run mkdocs build --strict`
Expected: exits 0, prints `Documentation built in ...`, creates `site/index.html`.

- [ ] **Step 5: Verify output exists**

Run: `test -f site/index.html && echo OK`
Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml uv.lock mkdocs.yml docs/index.md
git commit -m "feat: scaffold mkdocs-material site for modern-python.org"
```

(`uv.lock` is created by the first `uv run`; include it if present.)

---

## Task 2: Brand the site — move logo, custom green palette, favicon

**Files:**
- Move: `modern-python.png` → `docs/assets/modern-python.png`
- Create: `docs/stylesheets/extra.css`
- Modify: `mkdocs.yml` (add `logo`, `favicon`, `extra_css`, markdown extensions)

- [ ] **Step 1: Move the logo into the docs tree**

Run:
```bash
git mv modern-python.png docs/assets/modern-python.png
```
Expected: file relocated; `git status` shows a rename.

- [ ] **Step 2: Write `docs/stylesheets/extra.css`**

```css
/* Brand palette — forest green sampled from the org logo (#356852) */
:root > * {
  --md-primary-fg-color:        #356852;
  --md-primary-fg-color--light: #4a8a6e;
  --md-primary-fg-color--dark:  #234738;
  --md-accent-fg-color:         #c98a00;
}

/* Dark scheme keeps the same brand hue for links/accents */
[data-md-color-scheme="slate"] {
  --md-primary-fg-color:        #356852;
  --md-accent-fg-color:         #e0a300;
}

/* Centered hero intro on the homepage */
.mp-hero {
  text-align: center;
  margin: 2rem 0 3rem;
}
.mp-hero .mp-logo {
  max-width: 420px;
  width: 70%;
  height: auto;
}
.mp-hero .mp-tagline {
  color: var(--md-default-fg-color--light);
  font-size: 1.05rem;
  margin-top: 0.5rem;
}

/* Topic tiles inherit Material's .grid.cards; nudge the brand color */
.md-typeset .grid.cards > ul > li:hover {
  border-color: var(--md-primary-fg-color);
}
```

- [ ] **Step 3: Add logo, favicon, extensions, and `extra_css` to `mkdocs.yml`**

Add `logo` and `favicon` under the existing `theme:` block (same indentation level as `name:`):

```yaml
theme:
  name: material
  logo: assets/modern-python.png
  favicon: assets/modern-python.png
  # ... (features and palette from Task 1 remain unchanged below) ...
```

Then append these top-level blocks to the end of `mkdocs.yml`:

```yaml
extra_css:
  - stylesheets/extra.css

markdown_extensions:
  - attr_list
  - md_in_html
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
```

- [ ] **Step 4: Build and verify it succeeds**

Run: `uv run mkdocs build --strict`
Expected: exits 0.

- [ ] **Step 5: Verify the logo and brand color reached the output**

Run:
```bash
test -f site/assets/modern-python.png && echo LOGO_OK
grep -rq "356852" site/assets/stylesheets/ && echo COLOR_OK
```
Expected: `LOGO_OK` and `COLOR_OK`.

- [ ] **Step 6: Commit**

```bash
git add mkdocs.yml docs/stylesheets/extra.css docs/assets/modern-python.png
git commit -m "feat: brand site with org logo and forest-green palette"
```

---

## Task 3: Define the expected homepage content as a verification script

This task writes the assertion we will satisfy in Task 4. Listing every repo up front prevents omissions.

**Files:**
- Create: `scripts/check_site_content.sh`

- [ ] **Step 1: Write `scripts/check_site_content.sh`**

```bash
#!/usr/bin/env bash
# Verifies the built homepage links to every modern-python project.
set -euo pipefail

HTML="site/index.html"
test -f "$HTML" || { echo "MISSING $HTML — run 'uv run mkdocs build' first"; exit 1; }

REPOS=(
  fastapi-sqlalchemy-template litestar-sqlalchemy-template
  modern-di modern-di-fastapi modern-di-litestar modern-di-faststream
  modern-di-typer modern-di-pytest that-depends
  lite-bootstrap httpware faststream-redis-timers
  faststream-concurrent-aiokafka faststream-outbox
  db-retry eof-fixer semvertag
)

missing=0
for r in "${REPOS[@]}"; do
  if ! grep -q "github.com/modern-python/${r}\"" "$HTML"; then
    echo "MISSING LINK: $r"
    missing=1
  fi
done

if [ "$missing" -eq 0 ]; then
  echo "ALL ${#REPOS[@]} PROJECT LINKS PRESENT"
else
  exit 1
fi
```

- [ ] **Step 2: Make it executable**

Run: `chmod +x scripts/check_site_content.sh`

- [ ] **Step 3: Run it against the current (stub) build to confirm it FAILS**

Run: `uv run mkdocs build --strict && ./scripts/check_site_content.sh`
Expected: FAIL — prints `MISSING LINK:` lines (the stub homepage has no project links yet).

- [ ] **Step 4: Commit**

```bash
git add scripts/check_site_content.sh
git commit -m "test: add homepage project-link verification script"
```

---

## Task 4: Write the homepage (layout C)

**Files:**
- Modify: `docs/index.md` (replace stub with full content)

- [ ] **Step 1: Replace `docs/index.md` with the full homepage**

````markdown
---
hide:
  - navigation
  - toc
---

<div class="mp-hero" markdown>

![Modern Python](assets/modern-python.png){ .mp-logo }

Open-source templates and libraries for building production-ready Python
applications — web services, microservices, and the dependency injection that
wires them together.

<p class="mp-tagline">Built with <a href="https://github.com/astral-sh/uv">uv</a>,
<a href="https://github.com/astral-sh/ruff">ruff</a>, and
<a href="https://github.com/astral-sh/ty">ty</a>.</p>

</div>

<div class="grid cards" markdown>

-   :material-package-variant-closed:{ .lg .middle } __Project templates__

    ---

    Dockerized, batteries-included starting points for new web apps.

    [:octicons-arrow-right-24: Browse templates](#templates)

-   :material-needle:{ .lg .middle } __Dependency injection__

    ---

    The `modern-di` family of DI frameworks and integrations.

    [:octicons-arrow-right-24: Browse DI](#di)

-   :material-server-network:{ .lg .middle } __Microservices, HTTP & messaging__

    ---

    Bootstrapping, HTTP clients, and FastStream broker tooling.

    [:octicons-arrow-right-24: Browse services](#services)

-   :material-tools:{ .lg .middle } __Utilities__

    ---

    Small, focused helpers for everyday Python projects.

    [:octicons-arrow-right-24: Browse utilities](#utilities)

</div>

## Project templates { #templates }

- [`fastapi-sqlalchemy-template`](https://github.com/modern-python/fastapi-sqlalchemy-template) — dockerized web application with DI on FastAPI, SQLAlchemy 2, PostgreSQL.
- [`litestar-sqlalchemy-template`](https://github.com/modern-python/litestar-sqlalchemy-template) — dockerized web application on LiteStar, SQLAlchemy 2, PostgreSQL.

## Dependency injection { #di }

- [`modern-di`](https://github.com/modern-python/modern-di) — powerful DI framework with scopes.
- [`modern-di-fastapi`](https://github.com/modern-python/modern-di-fastapi) — `modern-di` integration for FastAPI.
- [`modern-di-litestar`](https://github.com/modern-python/modern-di-litestar) — `modern-di` integration for LiteStar.
- [`modern-di-faststream`](https://github.com/modern-python/modern-di-faststream) — `modern-di` integration for FastStream.
- [`modern-di-typer`](https://github.com/modern-python/modern-di-typer) — `modern-di` integration for Typer.
- [`modern-di-pytest`](https://github.com/modern-python/modern-di-pytest) — `modern-di` integration for pytest.
- [`that-depends`](https://github.com/modern-python/that-depends) — predecessor DI framework, still actively maintained.

## Microservices, HTTP & messaging { #services }

- [`lite-bootstrap`](https://github.com/modern-python/lite-bootstrap) — lightweight package for bootstrapping new microservices.
- [`httpware`](https://github.com/modern-python/httpware) — HTTP client framework with sync/async clients, middleware chain, and built-in resilience (retry, bulkhead).
- [`faststream-redis-timers`](https://github.com/modern-python/faststream-redis-timers) — FastStream broker integration for Redis-backed distributed timer scheduling.
- [`faststream-concurrent-aiokafka`](https://github.com/modern-python/faststream-concurrent-aiokafka) — concurrent message processing middleware for FastStream with `aiokafka`.
- [`faststream-outbox`](https://github.com/modern-python/faststream-outbox) — FastStream broker integration for the transactional outbox pattern with Postgres.

## Utilities { #utilities }

- [`db-retry`](https://github.com/modern-python/db-retry) — retry helpers for database operations.
- [`eof-fixer`](https://github.com/modern-python/eof-fixer) — automatically fix newlines at the end of files.
- [`semvertag`](https://github.com/modern-python/semvertag) — auto-tag your GitHub/GitLab repo with semantic version tags from CI.
````

- [ ] **Step 2: Build with strict mode (verifies the four tile anchors resolve)**

Run: `uv run mkdocs build --strict`
Expected: exits 0. (Strict mode fails if any `#anchor` tile link has no matching heading.)

- [ ] **Step 3: Verify every project link is present**

Run: `./scripts/check_site_content.sh`
Expected: `ALL 17 PROJECT LINKS PRESENT`

- [ ] **Step 4: Preview locally (optional, manual)**

Run: `uv run mkdocs serve`
Open http://127.0.0.1:8000 — confirm green hero with logo, four tiles jumping to their sections, light/dark toggle. Stop with Ctrl-C.

- [ ] **Step 5: Commit**

```bash
git add docs/index.md
git commit -m "feat: build modern-python.org homepage (intro, tiles, project list)"
```

---

## Task 5: Bind the custom domain

**Files:**
- Create: `docs/CNAME`

- [ ] **Step 1: Write `docs/CNAME`** (exactly one line, no scheme, no trailing path)

```
modern-python.org
```

- [ ] **Step 2: Build and verify CNAME lands at the site root**

Run:
```bash
uv run mkdocs build --strict
cat site/CNAME
```
Expected: prints `modern-python.org`.

- [ ] **Step 3: Commit**

```bash
git add docs/CNAME
git commit -m "feat: add CNAME for modern-python.org custom domain"
```

---

## Task 6: GitHub Actions deploy workflow

**Files:**
- Create: `.github/workflows/deploy.yml`

- [ ] **Step 1: Write `.github/workflows/deploy.yml`**

```yaml
name: Deploy site

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        uses: astral-sh/setup-uv@v6
      - name: Build site
        run: uv run mkdocs build --strict
      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: site

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: Validate the workflow YAML parses**

Run: `uv run python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/deploy.yml')); print('YAML OK')"`
Expected: `YAML OK`

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/deploy.yml
git commit -m "ci: build and deploy site to GitHub Pages via Actions"
```

---

## Task 7: Document the manual owner-only steps

**Files:**
- Create: `docs/DEPLOYMENT.md`

These steps need registrar access and the GitHub web UI and cannot be done from this repo. Capture them so the owner has an exact runbook.

- [ ] **Step 1: Write `docs/DEPLOYMENT.md`**

````markdown
# Deployment & domain setup (owner-only)

The site builds and deploys automatically via `.github/workflows/deploy.yml` on
every push to `main`. The following one-time steps require registrar access and
the GitHub web UI.

## 1. Enable Pages from Actions

Repo → **Settings → Pages → Build and deployment → Source = GitHub Actions**.

## 2. DNS records at the `modern-python.org` registrar

Apex `A` records:

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

Apex `AAAA` records:

```
2606:50c0:8000::153
2606:50c0:8001::153
2606:50c0:8002::153
2606:50c0:8003::153
```

`www` subdomain `CNAME` → `modern-python.github.io`

## 3. Enforce HTTPS

After the first successful deploy and DNS propagation:
Repo → **Settings → Pages → tick "Enforce HTTPS"**.

## Notes

- Only one Pages site per org can claim the apex `modern-python.org`. This
  `.github` repo owns it — no other repo should set the same custom domain.
- The published custom domain is held by `docs/CNAME`; do not remove it.
````

- [ ] **Step 2: Build to confirm the new page doesn't break strict mode**

Run: `uv run mkdocs build --strict`
Expected: exits 0.

- [ ] **Step 3: Commit**

```bash
git add docs/DEPLOYMENT.md
git commit -m "docs: add owner runbook for Pages and DNS setup"
```

---

## Final verification

- [ ] **Full clean build passes strict mode**

Run: `rm -rf site && uv run mkdocs build --strict`
Expected: exits 0.

- [ ] **All project links present**

Run: `./scripts/check_site_content.sh`
Expected: `ALL 17 PROJECT LINKS PRESENT`

- [ ] **Custom domain file shipped**

Run: `cat site/CNAME`
Expected: `modern-python.org`

- [ ] **Org profile untouched**

Run: `git status --short profile/`
Expected: no output (no changes to `profile/`).

- [ ] **Push to trigger first deploy**

```bash
git push origin main
```
Then watch the **Deploy site** workflow in the Actions tab. After it succeeds and
the owner completes the manual steps in `docs/DEPLOYMENT.md`, https://modern-python.org
serves the homepage.

---

## Self-review notes

- **Spec coverage:** scope (single landing page, room to grow) → Task 4 tiles use in-page anchors that promote to pages later; generator MkDocs+Material → Tasks 1–2; layout C → Task 4; deploy via Actions → Task 6; branding green `#356852` + logo → Task 2; CNAME + DNS → Tasks 5 & 7; `profile/README.md` untouched → final verification; independence of profile vs index → no sync task added (by design).
- **Project-link count:** 17 repos across 4 categories, enforced by `scripts/check_site_content.sh`.
- **Type/name consistency:** tile links use explicit heading ids (`#templates`, `#di`, `#services`, `#utilities`) set via `attr_list` `{ #id }` syntax, avoiding fragile auto-slug guessing for the `&`/comma in "Microservices, HTTP & messaging". `--strict` verifies each resolves.

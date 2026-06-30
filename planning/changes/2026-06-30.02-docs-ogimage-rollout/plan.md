# docs-site og:image rollout — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Each of the 7 docs-site repos emits `og:image`/`twitter:image` pointing
at its self-hosted social card, via a MkDocs Material `custom_dir` + `main.html`
override — shipped as one PR per repo.

**Spec:** [`design.md`](./design.md)

**Branch (this `.github` bundle):** `docs-ogimage`. **Per docs-repo branch:** `docs-ogimage`.

**Commit strategy:** one PR per docs repo; a final PR lands this planning bundle in `.github`.

## Global constraints

- **The 7 repos and their sites** (all default branch `main`):
  | repo | site_url | custom_dir |
  |------|----------|-----------|
  | `modern-di` | `https://modern-di.modern-python.org` | none (add `overrides`) |
  | `lite-bootstrap` | `https://lite-bootstrap.modern-python.org` | none (add `overrides`) |
  | `httpware` | `https://httpware.modern-python.org` | none (add `overrides`) |
  | `faststream-redis-timers` | `https://faststream-redis-timers.modern-python.org` | none (add `overrides`) |
  | `faststream-outbox` | `https://faststream-outbox.modern-python.org` | none (add `overrides`) |
  | `semvertag` | `https://semvertag.modern-python.org` | none (add `overrides`) |
  | `that-depends` | `https://that-depends.modern-python.org` | **existing** `docs/overrides` |

- **Card source** (this `.github` checkout, already on disk):
  `/Users/kevinsmith/src/pypi/modern-python/brand/projects/<repo>/social-card.png`
- **Clone work dir:** `/Users/kevinsmith/src/pypi/.ogimage-clones/<repo>` (create the
  parent once; it is outside the `.github` repo).
- **The override file is byte-identical for all 7 repos** — this exact content
  (it reads everything from `mkdocs.yml`, so nothing is per-repo):

  ```jinja
  {% extends "base.html" %}
  {% block extrahead %}
    {{ super() }}
    {% set base = config.site_url if config.site_url.endswith('/') else config.site_url ~ '/' %}
    {% set card = base ~ 'assets/social-card.png' %}
    {% set title = (page.title ~ ' · ' ~ config.site_name) if (page.title and not page.is_homepage) else config.site_name %}
    {% set description = page.meta.description if page.meta and page.meta.description else config.site_description %}
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="{{ config.site_name }}">
    <meta property="og:title" content="{{ title }}">
    <meta property="og:description" content="{{ description }}">
    <meta property="og:url" content="{{ page.canonical_url }}">
    <meta property="og:image" content="{{ card }}">
    <meta property="og:image:type" content="image/png">
    <meta property="og:image:width" content="1280">
    <meta property="og:image:height" content="640">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{{ title }}">
    <meta name="twitter:description" content="{{ description }}">
    <meta name="twitter:image" content="{{ card }}">
  {% endblock %}
  ```

- **Per-repo procedure** (Tasks 1–6 follow it exactly with their `<repo>` /
  `<site>` / `<override-dir>` = `overrides`; Task 7 differs — see it):

  1. `mkdir -p /Users/kevinsmith/src/pypi/.ogimage-clones`
  2. `gh repo clone modern-python/<repo> /Users/kevinsmith/src/pypi/.ogimage-clones/<repo>` (skip if dir exists; then `git -C … pull --ff-only`)
  3. `cd` into it; `git checkout -b docs-ogimage`
  4. `mkdir -p docs/assets <override-dir>`
  5. Copy the card: `cp /Users/kevinsmith/src/pypi/modern-python/brand/projects/<repo>/social-card.png docs/assets/social-card.png`
  6. Write `<override-dir>/main.html` with the exact override content above.
  7. Add `custom_dir: <override-dir>` under `theme:` in `mkdocs.yml` **only if absent** (Tasks 1–6 add `custom_dir: overrides`; Task 7 already has it).
  8. **Verify** (see "Verification" below).
  9. `git add -A && git commit -m "docs: add social card og:image meta"`
  10. `git push -u origin docs-ogimage`
  11. `gh pr create --base main --head docs-ogimage --title "Add social card og:image" --body "<body>"` (body: one line on what + that the card is self-hosted at `<site>/assets/social-card.png`, plus the 🤖 line).
  12. Watch CI: `gh pr checks <n>` until non-pending.

- **Verification (the task's "test"):** from the repo clone:
  - Build the docs. Try, in order: (a) `uv sync` then `uv run mkdocs build -d /tmp/ogbuild-<repo>`; (b) if that repo isn't uv-managed or deps fail, `uvx --with 'mkdocs-material[imaging]' --with mkdocs mkdocs build -d /tmp/ogbuild-<repo>` (add `--with` for any plugin the build complains is missing). If the docs toolchain genuinely cannot be assembled, STOP and report — do not open the PR on an unverified build.
  - Assert the built homepage carries the card:
    `grep -F '<meta property="og:image" content="<site>/assets/social-card.png">' /tmp/ogbuild-<repo>/index.html`
    must match exactly one line.
  - Assert the asset shipped: `test -f /tmp/ogbuild-<repo>/assets/social-card.png`.
  - Spot-check one interior page's built HTML contains the same `og:image` line.

- Do not touch anything else in the docs repos. No README changes here (separate spec).

---

### Task 1: modern-di (pilot)

**Repo:** `modern-python/modern-di` · **site:** `https://modern-di.modern-python.org` · **override-dir:** `overrides` (new) · **custom_dir:** add `overrides`.

This is the pilot — execute the per-repo procedure end to end and confirm the
pattern before the rest.

- [ ] **Step 1: Clone + branch**

  ```bash
  mkdir -p /Users/kevinsmith/src/pypi/.ogimage-clones
  gh repo clone modern-python/modern-di /Users/kevinsmith/src/pypi/.ogimage-clones/modern-di
  cd /Users/kevinsmith/src/pypi/.ogimage-clones/modern-di && git checkout -b docs-ogimage
  ```

- [ ] **Step 2: Add card + override + custom_dir**

  ```bash
  mkdir -p docs/assets overrides
  cp /Users/kevinsmith/src/pypi/modern-python/brand/projects/modern-di/social-card.png docs/assets/social-card.png
  ```
  Write `overrides/main.html` with the exact override content from Global
  Constraints. Then add `custom_dir: overrides` under `theme:` in `mkdocs.yml`
  (it currently has none). Example (match the file's existing indentation):

  ```yaml
  theme:
    name: material
    custom_dir: overrides
    # …existing theme keys unchanged…
  ```

- [ ] **Step 3: Build + verify (the test)**

  ```bash
  uv sync && uv run mkdocs build -d /tmp/ogbuild-modern-di
  grep -F '<meta property="og:image" content="https://modern-di.modern-python.org/assets/social-card.png">' /tmp/ogbuild-modern-di/index.html
  test -f /tmp/ogbuild-modern-di/assets/social-card.png && echo CARD_OK
  ```
  Expected: the grep prints exactly one line; `CARD_OK`. If `uv sync`/`uv run`
  fails, use the `uvx --with …` fallback from Global Constraints. If the build
  cannot be assembled at all, STOP and report BLOCKED.

- [ ] **Step 4: Commit + push + PR**

  ```bash
  git add -A && git commit -m "docs: add social card og:image meta"
  git push -u origin docs-ogimage
  gh pr create --base main --head docs-ogimage \
    --title "Add social card og:image" \
    --body $'Adds a self-hosted social card and the og:image/twitter:image meta (Material custom_dir override). Card served at https://modern-di.modern-python.org/assets/social-card.png.\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)'
  ```

- [ ] **Step 5: Watch CI**

  `gh pr checks <n>` until non-pending; report the result.

---

### Task 2: lite-bootstrap

**Repo:** `modern-python/lite-bootstrap` · **site:** `https://lite-bootstrap.modern-python.org` · **override-dir:** `overrides` (new) · **custom_dir:** add `overrides`.

Follow the Global Constraints per-repo procedure with these values. Card source:
`…/brand/projects/lite-bootstrap/social-card.png`.

- [ ] **Step 1: Clone + branch** — `gh repo clone modern-python/lite-bootstrap …/.ogimage-clones/lite-bootstrap`; `git checkout -b docs-ogimage`.
- [ ] **Step 2: Add card + override + custom_dir** — copy `lite-bootstrap` card to `docs/assets/social-card.png`; write `overrides/main.html` (exact Global-Constraints content); add `custom_dir: overrides` under `theme:` in `mkdocs.yml`.
- [ ] **Step 3: Build + verify** — build to `/tmp/ogbuild-lite-bootstrap`; assert one match of
  `grep -F '<meta property="og:image" content="https://lite-bootstrap.modern-python.org/assets/social-card.png">' /tmp/ogbuild-lite-bootstrap/index.html` and `test -f /tmp/ogbuild-lite-bootstrap/assets/social-card.png`.
- [ ] **Step 4: Commit + push + PR** — commit `docs: add social card og:image meta`; PR `--base main` with body naming `https://lite-bootstrap.modern-python.org/assets/social-card.png` + the 🤖 line.
- [ ] **Step 5: Watch CI** — `gh pr checks <n>` to completion.

---

### Task 3: httpware

**Repo:** `modern-python/httpware` · **site:** `https://httpware.modern-python.org` · **override-dir:** `overrides` (new) · **custom_dir:** add `overrides`.

- [ ] **Step 1: Clone + branch** — clone to `…/.ogimage-clones/httpware`; `git checkout -b docs-ogimage`.
- [ ] **Step 2: Add card + override + custom_dir** — copy `httpware` card to `docs/assets/social-card.png`; write `overrides/main.html` (exact content); add `custom_dir: overrides` under `theme:`.
- [ ] **Step 3: Build + verify** — build to `/tmp/ogbuild-httpware`; assert one match of
  `grep -F '<meta property="og:image" content="https://httpware.modern-python.org/assets/social-card.png">' /tmp/ogbuild-httpware/index.html` and the card file exists.
- [ ] **Step 4: Commit + push + PR** — `docs: add social card og:image meta`; PR body names `https://httpware.modern-python.org/assets/social-card.png` + 🤖 line.
- [ ] **Step 5: Watch CI.**

---

### Task 4: faststream-redis-timers

**Repo:** `modern-python/faststream-redis-timers` · **site:** `https://faststream-redis-timers.modern-python.org` · **override-dir:** `overrides` (new) · **custom_dir:** add `overrides`.

- [ ] **Step 1: Clone + branch** — clone to `…/.ogimage-clones/faststream-redis-timers`; `git checkout -b docs-ogimage`.
- [ ] **Step 2: Add card + override + custom_dir** — copy `faststream-redis-timers` card; write `overrides/main.html`; add `custom_dir: overrides`.
- [ ] **Step 3: Build + verify** — build to `/tmp/ogbuild-faststream-redis-timers`; assert one match of
  `grep -F '<meta property="og:image" content="https://faststream-redis-timers.modern-python.org/assets/social-card.png">' /tmp/ogbuild-faststream-redis-timers/index.html` and the card exists.
- [ ] **Step 4: Commit + push + PR** — `docs: add social card og:image meta`; PR body names the redis-timers card URL + 🤖 line.
- [ ] **Step 5: Watch CI.**

---

### Task 5: faststream-outbox

**Repo:** `modern-python/faststream-outbox` · **site:** `https://faststream-outbox.modern-python.org` · **override-dir:** `overrides` (new) · **custom_dir:** add `overrides`.

- [ ] **Step 1: Clone + branch** — clone to `…/.ogimage-clones/faststream-outbox`; `git checkout -b docs-ogimage`.
- [ ] **Step 2: Add card + override + custom_dir** — copy `faststream-outbox` card; write `overrides/main.html`; add `custom_dir: overrides`.
- [ ] **Step 3: Build + verify** — build to `/tmp/ogbuild-faststream-outbox`; assert one match of
  `grep -F '<meta property="og:image" content="https://faststream-outbox.modern-python.org/assets/social-card.png">' /tmp/ogbuild-faststream-outbox/index.html` and the card exists.
- [ ] **Step 4: Commit + push + PR** — `docs: add social card og:image meta`; PR body names the outbox card URL + 🤖 line.
- [ ] **Step 5: Watch CI.**

---

### Task 6: semvertag

**Repo:** `modern-python/semvertag` · **site:** `https://semvertag.modern-python.org` · **override-dir:** `overrides` (new) · **custom_dir:** add `overrides`.

- [ ] **Step 1: Clone + branch** — clone to `…/.ogimage-clones/semvertag`; `git checkout -b docs-ogimage`.
- [ ] **Step 2: Add card + override + custom_dir** — copy `semvertag` card; write `overrides/main.html`; add `custom_dir: overrides`.
- [ ] **Step 3: Build + verify** — build to `/tmp/ogbuild-semvertag`; assert one match of
  `grep -F '<meta property="og:image" content="https://semvertag.modern-python.org/assets/social-card.png">' /tmp/ogbuild-semvertag/index.html` and the card exists.
- [ ] **Step 4: Commit + push + PR** — `docs: add social card og:image meta`; PR body names the semvertag card URL + 🤖 line.
- [ ] **Step 5: Watch CI.**

---

### Task 7: that-depends (special — existing `docs/overrides`)

**Repo:** `modern-python/that-depends` · **site:** `https://that-depends.modern-python.org` · **override-dir:** `docs/overrides` (**exists**; `custom_dir: docs/overrides` already set — do NOT add `custom_dir`).

- [ ] **Step 1: Clone + branch** — clone to `…/.ogimage-clones/that-depends`; `git checkout -b docs-ogimage`.

- [ ] **Step 2: Inspect existing overrides**

  ```bash
  ls -la docs/overrides
  cat docs/overrides/main.html 2>/dev/null || echo "no main.html"
  ```
  - **If `docs/overrides/main.html` does NOT exist:** create it with the exact
    override content from Global Constraints.
  - **If it EXISTS:** merge — keep its `{% extends … %}` and existing blocks, and
    ensure an `extrahead` block contains the OG/Twitter `<meta>` lines from the
    Global Constraints template (with `{{ super() }}` first). If it already has an
    `extrahead` block, append the meta lines inside it; if not, add the
    `{% block extrahead %}{{ super() }} … {% endblock %}` block. Do not remove
    anything it already does.

- [ ] **Step 3: Add card (no mkdocs change)**

  ```bash
  mkdir -p docs/assets
  cp /Users/kevinsmith/src/pypi/modern-python/brand/projects/that-depends/social-card.png docs/assets/social-card.png
  ```
  Do not edit `mkdocs.yml` — `custom_dir: docs/overrides` is already set.

- [ ] **Step 4: Build + verify**

  Build to `/tmp/ogbuild-that-depends` (uv first, else the `uvx --with` fallback).
  Assert exactly one match of
  `grep -F '<meta property="og:image" content="https://that-depends.modern-python.org/assets/social-card.png">' /tmp/ogbuild-that-depends/index.html`
  and `test -f /tmp/ogbuild-that-depends/assets/social-card.png`. Spot-check one
  interior page. If a pre-existing override already emitted an `og:image`, confirm
  there is now exactly ONE `og:image` line (grep count) — if two, the merge
  duplicated it; fix so only our line remains.

- [ ] **Step 5: Commit + push + PR** — `docs: add social card og:image meta`; PR `--base main`, body names `https://that-depends.modern-python.org/assets/social-card.png` + 🤖 line.

- [ ] **Step 6: Watch CI.**

---

### Task 8: finalize the `.github` planning bundle

**Files (in `.github`, branch `docs-ogimage`):**
- Modify: `planning/changes/2026-06-30.02-docs-ogimage-rollout/design.md` (summary)

- [ ] **Step 1: Finalize the summary**

  In `design.md`, set `summary:` to the realized result, e.g.:
  `summary: docs-site og:image shipped — all 7 docs repos serve a self-hosted social card via a Material override; one PR per repo.`

- [ ] **Step 2: Verify planning**

  ```bash
  cd /Users/kevinsmith/src/pypi/modern-python && just check-planning
  ```
  Expected: `planning: OK`.

- [ ] **Step 3: Commit + open the bundle PR**

  ```bash
  git add planning/changes/2026-06-30.02-docs-ogimage-rollout/design.md
  git commit -m "docs: finalize og:image rollout bundle summary"
  git push -u origin docs-ogimage
  gh pr create --base main --head docs-ogimage \
    --title "Plan + record: docs-site og:image rollout" \
    --body $'Planning bundle (design + plan) for wiring og:image into the 7 docs repos. The implementation shipped as one PR per docs repo (linked).\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)'
  ```

---

## Notes for the executor

- Each docs-repo task is a self-contained PR; verify the build (or STOP) before
  opening it. The 7 repo PRs are independent — order does not matter, but do the
  `modern-di` pilot first to shake out the docs-build command.
- These tasks run in cloned repos under `/Users/kevinsmith/src/pypi/.ogimage-clones/`,
  NOT in the `.github` repo. Only Task 8 touches `.github`.
- If a repo's docs build needs a plugin the fallback `uvx` line doesn't include,
  add another `--with <plugin>` rather than skipping verification.

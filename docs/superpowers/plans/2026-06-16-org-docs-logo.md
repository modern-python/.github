# Org Logo + Brand Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make all 7 checked-out modern-python docs sites show the org white wordmark logo in the top-left corner, the org mark as favicon, and the org green brand palette.

**Architecture:** Each target repo is an independent git repository. The change is the same byte-identical pattern per repo: copy two SVG assets into `docs/assets/`, add `logo`/`favicon` keys and switch the palette to `custom` in `mkdocs.yml`, and add a `docs/css/brand.css` defining the green Material custom-property variables. Verified per repo with a strict MkDocs build plus a visual spot-check.

**Tech Stack:** MkDocs + Material theme, `uv`/`uvx`, `just`.

---

## Shared artifacts (used by every task)

### Source SVGs (copy from the org `.github` repo)

- `/Users/kevinsmith/src/pypi/.github/docs/assets/modern-python-white.svg` → repo `docs/assets/modern-python-white.svg`
- `/Users/kevinsmith/src/pypi/.github/docs/assets/modern-python-mark.svg` → repo `docs/assets/modern-python-mark.svg`

### `docs/css/brand.css` — exact content (identical in every repo)

```css
/* Brand palette — forest green sampled from the org logo (#356852) */
:root > * {
  --md-primary-fg-color:        #356852;
  --md-primary-fg-color--light: #4a8a6e;
  --md-primary-fg-color--dark:  #234738;
  --md-accent-fg-color:         #c98a00;
}

/* Dark scheme keeps the same brand hue; lighter green for body links so they
   stay AA-readable on the dark background. */
[data-md-color-scheme="slate"] {
  --md-primary-fg-color:        #356852;
  --md-primary-fg-color--light: #4a8a6e;
  --md-primary-fg-color--dark:  #234738;
  --md-accent-fg-color:         #e0a300;
  --md-typeset-a-color:         #7fb79f;
}
```

### `mkdocs.yml` edits (same three edits in every repo)

1. **Add logo + favicon** — directly after the `  name: material` line inside `theme:`:
   ```yaml
     logo: assets/modern-python-white.svg
     favicon: assets/modern-python-mark.svg
   ```
2. **Switch palette to custom** — replace **all** occurrences (there are two of each, one per scheme):
   - `primary: black` → `primary: custom`
   - `accent: pink` → `accent: custom`
3. **Register the stylesheet** in the top-level `extra_css:` list:
   - add `  - css/brand.css`

### Verification command (run from the repo root)

```bash
uvx --with-requirements docs/requirements.txt mkdocs build --strict
```
Expected: build succeeds, ends with `INFO - Documentation built in ...`, **no** WARNING lines (`--strict` turns warnings into a non-zero exit — a missing `assets/…svg` path fails here). 5 repos also expose `just docs-build` (same command); that-depends does not, so use the command above directly.

### Per-repo commit message

```
docs: adopt org logo, favicon, and brand palette

Match modern-python.org: white wordmark logo top-left, mark favicon,
forest-green Material palette.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

---

## Tasks

> The 7 repos split into two shapes:
> - **Group A — already has `extra_css: - css/code.css`** (just append `brand.css`): modern-di, faststream-outbox, that-depends, lite-bootstrap, faststream-redis-timers.
> - **Group B — no `extra_css` and no `docs/css/` dir** (create both): autosemver, httpware.
>
> Each task is independent and commits in its own repository. **Branch first in each repo** (all are on `main` except faststream-outbox — see Task 2).

### Task 1: modern-di (Group A)

**Files:**
- Repo root: `/Users/kevinsmith/src/pypi/modern-di`
- Create: `docs/assets/modern-python-white.svg`, `docs/assets/modern-python-mark.svg`, `docs/css/brand.css`
- Modify: `mkdocs.yml` (palette lines 69,70,76,77; theme block after line ~66 `name: material`; `extra_css` at line 102-103)

- [ ] **Step 1: Branch**
```bash
cd /Users/kevinsmith/src/pypi/modern-di && git checkout -b docs/org-logo-brand
```

- [ ] **Step 2: Copy assets**
```bash
mkdir -p docs/assets
cp /Users/kevinsmith/src/pypi/.github/docs/assets/modern-python-white.svg docs/assets/
cp /Users/kevinsmith/src/pypi/.github/docs/assets/modern-python-mark.svg docs/assets/
```

- [ ] **Step 3: Create `docs/css/brand.css`** with the exact content from §Shared artifacts.

- [ ] **Step 4: Edit `mkdocs.yml`** — apply the three edits from §Shared artifacts:
  - after `  name: material`, add the `logo:` and `favicon:` lines;
  - replace both `primary: black`→`primary: custom` and both `accent: pink`→`accent: custom`;
  - under `extra_css:` (after `- css/code.css`), add `  - css/brand.css`.

- [ ] **Step 5: Strict build**
```bash
just docs-build
```
Expected: PASS, no warnings.

- [ ] **Step 6: Visual spot-check** — `uvx --with-requirements docs/requirements.txt mkdocs serve`, open http://127.0.0.1:8000, confirm: white wordmark top-left, favicon (mark) in the tab, green header; toggle to dark mode and confirm green accents + readable links. Ctrl-C.

- [ ] **Step 7: Commit**
```bash
git add docs/assets/modern-python-white.svg docs/assets/modern-python-mark.svg docs/css/brand.css mkdocs.yml
git commit -m "docs: adopt org logo, favicon, and brand palette" -m "Match modern-python.org: white wordmark logo top-left, mark favicon, forest-green Material palette." -m "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

### Task 2: faststream-outbox (Group A) — ⚠️ currently on an unrelated branch

**Files:**
- Repo root: `/Users/kevinsmith/src/pypi/faststream-outbox`
- Create: `docs/assets/modern-python-white.svg`, `docs/assets/modern-python-mark.svg`, `docs/css/brand.css`
- Modify: `mkdocs.yml` (palette lines 55,56,62,63; theme block after `name: material`; `extra_css` at line 87-88)

- [ ] **Step 1: Branch off main (do NOT branch off the current `fix/actionable-schema-drift-error` branch)**
```bash
cd /Users/kevinsmith/src/pypi/faststream-outbox
git stash -u 2>/dev/null; git checkout main && git checkout -b docs/org-logo-brand
```
If `git checkout main` fails due to uncommitted work, stop and report — do not mix this change into the unrelated feature branch.

- [ ] **Step 2: Copy assets**
```bash
mkdir -p docs/assets
cp /Users/kevinsmith/src/pypi/.github/docs/assets/modern-python-white.svg docs/assets/
cp /Users/kevinsmith/src/pypi/.github/docs/assets/modern-python-mark.svg docs/assets/
```

- [ ] **Step 3: Create `docs/css/brand.css`** with the exact content from §Shared artifacts.

- [ ] **Step 4: Edit `mkdocs.yml`** — the three edits from §Shared artifacts (logo/favicon after `name: material`; palette black→custom / pink→custom ×2 each; append `- css/brand.css` under `extra_css`).

- [ ] **Step 5: Strict build**
```bash
just docs-build
```
Expected: PASS, no warnings.

- [ ] **Step 6: Visual spot-check** — `uvx --with-requirements docs/requirements.txt mkdocs serve`, confirm logo/favicon/green header (light + dark). Ctrl-C.

- [ ] **Step 7: Commit** (same message as Task 1 Step 7, staging the same 4 paths).

### Task 3: that-depends (Group A) — keeps its `custom_dir: docs/overrides`

**Files:**
- Repo root: `/Users/kevinsmith/src/pypi/that-depends`
- Create: `docs/assets/modern-python-white.svg`, `docs/assets/modern-python-mark.svg`, `docs/css/brand.css`
- Modify: `mkdocs.yml` (palette lines 68,69,75,76; theme block after `name: material`; `extra_css` at line 101-102, which is immediately followed by `plugins:` — insert `- css/brand.css` between `- css/code.css` and `plugins:`)

- [ ] **Step 1: Branch**
```bash
cd /Users/kevinsmith/src/pypi/that-depends && git checkout -b docs/org-logo-brand
```

- [ ] **Step 2: Copy assets**
```bash
mkdir -p docs/assets
cp /Users/kevinsmith/src/pypi/.github/docs/assets/modern-python-white.svg docs/assets/
cp /Users/kevinsmith/src/pypi/.github/docs/assets/modern-python-mark.svg docs/assets/
```

- [ ] **Step 3: Create `docs/css/brand.css`** with the exact content from §Shared artifacts.

- [ ] **Step 4: Edit `mkdocs.yml`** — the three edits from §Shared artifacts. Do **not** touch `custom_dir: docs/overrides`. The `extra_css:` list is followed directly by `plugins:`; insert `  - css/brand.css` after the `- css/code.css` line.

- [ ] **Step 5: Strict build**
```bash
uvx --with-requirements docs/requirements.txt mkdocs build --strict
```
Expected: PASS, no warnings. (that-depends uses the `llmstxt` plugin — `docs/requirements.txt` includes it; if the build errors on a missing plugin, that's a pre-existing repo issue, report it.)

- [ ] **Step 6: Visual spot-check** — `uv run mkdocs serve` (or `uvx --with-requirements docs/requirements.txt mkdocs serve`), confirm logo/favicon/green header (light + dark). Ctrl-C.

- [ ] **Step 7: Commit** (same message as Task 1 Step 7, staging the same 4 paths).

### Task 4: lite-bootstrap (Group A)

**Files:**
- Repo root: `/Users/kevinsmith/src/pypi/lite-bootstrap`
- Create: `docs/assets/modern-python-white.svg`, `docs/assets/modern-python-mark.svg`, `docs/css/brand.css`
- Modify: `mkdocs.yml` (palette lines 36,37,43,44; theme block after `name: material`; `extra_css` at line 67-68)

- [ ] **Step 1: Branch**
```bash
cd /Users/kevinsmith/src/pypi/lite-bootstrap && git checkout -b docs/org-logo-brand
```
- [ ] **Step 2: Copy assets**
```bash
mkdir -p docs/assets
cp /Users/kevinsmith/src/pypi/.github/docs/assets/modern-python-white.svg docs/assets/
cp /Users/kevinsmith/src/pypi/.github/docs/assets/modern-python-mark.svg docs/assets/
```
- [ ] **Step 3: Create `docs/css/brand.css`** with the exact content from §Shared artifacts.
- [ ] **Step 4: Edit `mkdocs.yml`** — the three edits from §Shared artifacts.
- [ ] **Step 5: Strict build** — `just docs-build` (expected PASS, no warnings).
- [ ] **Step 6: Visual spot-check** — `uvx --with-requirements docs/requirements.txt mkdocs serve`; confirm logo/favicon/green header (light + dark). Ctrl-C.
- [ ] **Step 7: Commit** (same message as Task 1 Step 7, staging the same 4 paths).

### Task 5: faststream-redis-timers (Group A)

**Files:**
- Repo root: `/Users/kevinsmith/src/pypi/faststream-redis-timers`
- Create: `docs/assets/modern-python-white.svg`, `docs/assets/modern-python-mark.svg`, `docs/css/brand.css`
- Modify: `mkdocs.yml` (palette lines 36,37,43,44; theme block after `name: material`; `extra_css` at line 68-69)

- [ ] **Step 1: Branch**
```bash
cd /Users/kevinsmith/src/pypi/faststream-redis-timers && git checkout -b docs/org-logo-brand
```
- [ ] **Step 2: Copy assets**
```bash
mkdir -p docs/assets
cp /Users/kevinsmith/src/pypi/.github/docs/assets/modern-python-white.svg docs/assets/
cp /Users/kevinsmith/src/pypi/.github/docs/assets/modern-python-mark.svg docs/assets/
```
- [ ] **Step 3: Create `docs/css/brand.css`** with the exact content from §Shared artifacts.
- [ ] **Step 4: Edit `mkdocs.yml`** — the three edits from §Shared artifacts. (Note: this repo has no `site_url`; that does not affect logo/favicon/palette and is out of scope.)
- [ ] **Step 5: Strict build** — `just docs-build` (expected PASS, no warnings).
- [ ] **Step 6: Visual spot-check** — `uvx --with-requirements docs/requirements.txt mkdocs serve`; confirm logo/favicon/green header (light + dark). Ctrl-C.
- [ ] **Step 7: Commit** (same message as Task 1 Step 7, staging the same 4 paths).

### Task 6: autosemver (Group B — create `docs/css/` + `extra_css`)

**Files:**
- Repo root: `/Users/kevinsmith/src/pypi/autosemver`
- Create: `docs/assets/modern-python-white.svg`, `docs/assets/modern-python-mark.svg`, `docs/css/brand.css`
- Modify: `mkdocs.yml` (palette lines 38,39,45,46; theme block after `name: material`; **add a new top-level `extra_css:` key**)

- [ ] **Step 1: Branch**
```bash
cd /Users/kevinsmith/src/pypi/autosemver && git checkout -b docs/org-logo-brand
```
- [ ] **Step 2: Copy assets**
```bash
mkdir -p docs/assets docs/css
cp /Users/kevinsmith/src/pypi/.github/docs/assets/modern-python-white.svg docs/assets/
cp /Users/kevinsmith/src/pypi/.github/docs/assets/modern-python-mark.svg docs/assets/
```
- [ ] **Step 3: Create `docs/css/brand.css`** with the exact content from §Shared artifacts.
- [ ] **Step 4: Edit `mkdocs.yml`:**
  - after `  name: material`, add the `logo:` and `favicon:` lines;
  - replace both `primary: black`→`primary: custom` and both `accent: pink`→`accent: custom`;
  - add a new top-level key (place it just before `markdown_extensions:`):
    ```yaml
    extra_css:
      - css/brand.css
    ```
- [ ] **Step 5: Confirm `docs/requirements.txt` exists** (the verification command needs it):
```bash
test -f docs/requirements.txt && cat docs/requirements.txt || echo "MISSING — report before building"
```
If missing, report — the repo's docs build is configured differently; check `just docs-build` and use whatever it invokes.
- [ ] **Step 6: Strict build** — `just docs-build` (expected PASS, no warnings).
- [ ] **Step 7: Visual spot-check** — `uvx --with-requirements docs/requirements.txt mkdocs serve`; confirm logo/favicon/green header (light + dark). Ctrl-C.
- [ ] **Step 8: Commit** (same message as Task 1 Step 7, staging the 4 paths).

### Task 7: httpware (Group B — create `docs/css/` + `extra_css`)

**Files:**
- Repo root: `/Users/kevinsmith/src/pypi/httpware`
- Create: `docs/assets/modern-python-white.svg`, `docs/assets/modern-python-mark.svg`, `docs/css/brand.css`
- Modify: `mkdocs.yml` (palette lines 33,34,40,41; theme block after `name: material`; **add a new top-level `extra_css:` key**)

- [ ] **Step 1: Branch**
```bash
cd /Users/kevinsmith/src/pypi/httpware && git checkout -b docs/org-logo-brand
```
- [ ] **Step 2: Copy assets**
```bash
mkdir -p docs/assets docs/css
cp /Users/kevinsmith/src/pypi/.github/docs/assets/modern-python-white.svg docs/assets/
cp /Users/kevinsmith/src/pypi/.github/docs/assets/modern-python-mark.svg docs/assets/
```
- [ ] **Step 3: Create `docs/css/brand.css`** with the exact content from §Shared artifacts.
- [ ] **Step 4: Edit `mkdocs.yml`** — same as Task 6 Step 4 (logo/favicon after `name: material`; palette black→custom / pink→custom ×2 each; add a new top-level `extra_css:` key with `  - css/brand.css`, placed just before `markdown_extensions:`).
- [ ] **Step 5: Confirm `docs/requirements.txt` exists** (as in Task 6 Step 5).
- [ ] **Step 6: Strict build** — `just docs-build` (expected PASS, no warnings).
- [ ] **Step 7: Visual spot-check** — `uvx --with-requirements docs/requirements.txt mkdocs serve`; confirm logo/favicon/green header (light + dark). Ctrl-C.
- [ ] **Step 8: Commit** (same message as Task 1 Step 7, staging the 4 paths).

---

## Final verification (after all 7 tasks)

- [ ] Each of the 7 repos has a clean `docs/org-logo-brand` branch with exactly one commit touching only `mkdocs.yml`, `docs/css/brand.css`, and the two `docs/assets/*.svg` files.
- [ ] Every `just docs-build` (or the direct `uvx … mkdocs build --strict`) passed with no warnings.
- [ ] Logo, favicon, and green palette confirmed visually in at least modern-di (light + dark), with one Group B repo (autosemver or httpware) also spot-checked to prove the created `extra_css` wiring works.

## Out of scope (do not implement here)

- OG social cards / `overrides/main.html` / `social-card.png`.
- Backfilling `site_url` in faststream-redis-timers.
- Opening PRs / pushing — left to the maintainer unless asked.

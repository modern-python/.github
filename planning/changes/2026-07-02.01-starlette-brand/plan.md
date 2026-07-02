# starlette-brand — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Onboard `modern-di-starlette` into the org brand kit and every surface
its siblings appear on (mark, profile README, docs site, GitHub repo settings).

**Spec:** [`design.md`](./design.md)

**Branch:** `starlette-brand` (already created)

**Commit strategy:** Per-task commits.

## Global Constraints

- Canonical one-liner, used verbatim on every surface: `modern-di integration for Starlette`.
- Brand marks may use only the allowed palette; the Starlette mark uses only `GOLD` (`GOLD_LIGHT = #c98a00`). `test_only_allowed_colours` is the guardrail.
- Ordering everywhere: web-framework integrations run fastapi -> litestar -> starlette (starlette inserted immediately after litestar) in the manifest, the profile table, the docs list, and the stack sentence.
- All Python edits: imports at module level, annotate every argument (repo house style + ruff `ALL`).
- Run from repo root `/Users/kevinsmith/src/pypi/modern-python`. Commands use `uv run` / `just` as the repo does.

---

### Task 1: Mint the Starlette mark (symbol + manifest + test)

**Files:**
- Modify: `tests/test_projects.py` (add repo to `EXPECTED_REPOS`)
- Modify: `brand/build/symbols.py` (add `_sparkle4` + `sparkle_cluster`)
- Modify: `brand/build/projects.py` (add `MANIFEST` entry)

**Interfaces:**
- Produces: `sparkle_cluster(cx: float, cy: float, r: float) -> str` in `brand.build.symbols`, returning bare SVG markup (no `<svg>` wrapper), consumed by `MANIFEST["modern-di-starlette"]` in `brand.build.projects`.

- [ ] **Step 1: Write the failing test**

  In `tests/test_projects.py`, add `"modern-di-starlette"` to the `EXPECTED_REPOS` set, immediately after the `"modern-di-litestar"` line:

  ```python
      "modern-di-litestar",
      "modern-di-starlette",
      "modern-di-faststream",
  ```

- [ ] **Step 2: Run the test to verify it fails**

  Run: `uv run pytest tests/test_projects.py -q`
  Expected: FAIL — `test_manifest_covers_every_repo` asserts `set(p.MANIFEST) == EXPECTED_REPOS` and the manifest is missing `modern-di-starlette`; the `project_mark`/`only_allowed_colours` params for that repo also error with `KeyError: 'modern-di-starlette'`.

- [ ] **Step 3: Add the sparkle symbols**

  In `brand/build/symbols.py`, add these two functions next to `_star5` (which ends just before `_circ_arc`). `_sparkle4` is a private helper; `sparkle_cluster` is the public mark. Colours: `GOLD` only.

  ```python
  def _sparkle4(cx: float, cy: float, radius: float, color: str, inner: float = 0.34) -> str:
      """Four-point sparkle (concave star) centred on (cx,cy)."""
      pts: list[tuple[float, float]] = []
      for i in range(4):
          ao = -90 + i * 90
          pts.append(
              (
                  cx + radius * math.cos(math.radians(ao)),
                  cy + radius * math.sin(math.radians(ao)),
              )
          )
          ai = ao + 45
          pts.append(
              (
                  cx + radius * inner * math.cos(math.radians(ai)),
                  cy + radius * inner * math.sin(math.radians(ai)),
              )
          )
      body = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
      return f'<polygon points="{body}" fill="{color}"/>'


  def sparkle_cluster(cx: float, cy: float, r: float) -> str:
      """Starlette cue: a large four-point sparkle with a small companion
      (a "little star" — starlette)."""
      big = _sparkle4(cx - 0.174 * r, cy + 0.130 * r, r * 0.82, GOLD)
      small = _sparkle4(cx + 0.565 * r, cy - 0.522 * r, r * 0.36, GOLD)
      return big + small
  ```

- [ ] **Step 4: Add the manifest entry**

  In `brand/build/projects.py`, inside `MANIFEST`, add the Starlette line immediately after `modern-di-litestar`:

  ```python
      "modern-di-litestar": lambda: sym.star_disc(_CX, _CY, R),
      "modern-di-starlette": lambda: sym.sparkle_cluster(_CX, _CY, R),
      "modern-di-faststream": lambda: sym.faststream(_CX, _CY, R),
  ```

- [ ] **Step 5: Run the tests to verify they pass**

  Run: `uv run pytest tests/test_projects.py -q`
  Expected: PASS — manifest now equals `EXPECTED_REPOS`; the new repo's mark parses as valid SVG and uses only allowed colours.

- [ ] **Step 6: Commit**

  ```bash
  git add tests/test_projects.py brand/build/symbols.py brand/build/projects.py
  git commit -m "feat(brand): add sparkle-cluster mark for modern-di-starlette"
  ```

---

### Task 2: Regenerate and commit the brand assets

**Files:**
- Create: `brand/projects/modern-di-starlette/{mark.svg,mark-512.png,mark-1024.png,lockup-light.svg,lockup-dark.svg,lockup.png}`

Regenerate the kit so the integration repo's README image links resolve.

- [ ] **Step 1: Regenerate**

  Run: `just sync-assets`
  (Runs `uv run python -m brand.build.render`, then copies the org subset into `docs/assets/`.)

- [ ] **Step 2: Verify only the new files changed**

  Run: `git status --short`
  Expected: six new untracked files under `brand/projects/modern-di-starlette/` and nothing else. The render is deterministic, so existing project/org/docs assets must show no diff. If any other file changed, STOP and investigate (likely a tool/font version drift) before committing — do not blanket-commit unexpected diffs.

- [ ] **Step 3: Visually inspect the mark and lockups**

  Confirm the four-point sparkle cluster renders inside the green/gold frame, and that light/dark lockups carry the `modern-di-starlette` name:

  ```bash
  ls -1 brand/projects/modern-di-starlette/
  open brand/projects/modern-di-starlette/mark.svg brand/projects/modern-di-starlette/lockup-light.svg brand/projects/modern-di-starlette/lockup-dark.svg
  ```
  Expected: `lockup-dark.svg  lockup-light.svg  lockup.png  mark-1024.png  mark-512.png  mark.svg`; the dark lockup uses the darker gold (`#f0b528`).

- [ ] **Step 4: Commit**

  ```bash
  git add brand/projects/modern-di-starlette
  git commit -m "chore(brand): generate modern-di-starlette assets"
  ```

---

### Task 3: List Starlette on the profile README and docs site

**Files:**
- Modify: `profile/README.md` (Dependency injection table)
- Modify: `docs/index.md` (DI list + stack sentence)

Add the integration to both public catalogs, using the canonical one-liner.

- [ ] **Step 1: Add the profile README table row**

  In `profile/README.md`, in the `### Dependency injection` table, insert this row immediately after the `modern-di-litestar` row (mirrors the sibling row exactly, name swapped):

  ```markdown
  | [`modern-di-starlette`](https://github.com/modern-python/modern-di-starlette) | modern-di integration for Starlette | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-starlette)](https://github.com/modern-python/modern-di-starlette/stargazers) [![PyPI](https://img.shields.io/pypi/v/modern-di-starlette)](https://pypi.org/project/modern-di-starlette/) [![Downloads](https://static.pepy.tech/badge/modern-di-starlette/month)](https://pepy.tech/projects/modern-di-starlette) [![Context7](https://img.shields.io/badge/Context7-docs-blue)](https://context7.com/modern-python/modern-di-starlette) |
  ```

- [ ] **Step 2: Add the docs DI list bullet**

  In `docs/index.md`, in the `## Dependency injection { #di }` list, insert this bullet immediately after the `modern-di-litestar` line:

  ```markdown
  - [`modern-di-starlette`](https://github.com/modern-python/modern-di-starlette) — `modern-di` integration for Starlette.
  ```

- [ ] **Step 3: Extend the stack sentence**

  In `docs/index.md`, in the `## The stack` section, update the `modern-di` bullet. Replace:

  ```
  dependency injection with one wiring shared across FastAPI, Litestar,
  FastStream, and Typer.
  ```

  with:

  ```
  dependency injection with one wiring shared across FastAPI, Litestar,
  Starlette, FastStream, and Typer.
  ```

- [ ] **Step 4: Verify surfaces and run the full suite**

  ```bash
  grep -n "modern-di-starlette" profile/README.md docs/index.md
  uv run just check-planning
  uv run just test
  ```
  Expected: the slug `modern-di-starlette` appears once in `profile/README.md` and once in `docs/index.md` (the DI bullet). The stack sentence names "Starlette" (not the slug), so it does not add a grep hit. `check-planning` prints `planning: OK`; the pytest suite is green.

- [ ] **Step 5: Commit**

  ```bash
  git add profile/README.md docs/index.md
  git commit -m "docs: list modern-di-starlette on profile README and docs site"
  ```

---

### Task 4: Align the GitHub repo settings

**Files:** none (out-of-repo; GitHub settings via `gh`). No commit.

Bring `modern-python/modern-di-starlette` description, website, and topics in line with org conventions. Apply only the diff from current state.

- [ ] **Step 1: Read current settings**

  ```bash
  gh repo view modern-python/modern-di-starlette --json description,homepageUrl,repositoryTopics
  ```
  Note which of the three fields already match the intended values below; skip any that already match.

- [ ] **Step 2: Set description and website**

  ```bash
  gh repo edit modern-python/modern-di-starlette \
    --description "modern-di integration for Starlette" \
    --homepage "https://modern-di.modern-python.org"
  ```

- [ ] **Step 3: Set topics**

  Intended set (integration base set + framework):
  `python, dependency-injection, di, ioc-container, modern-di, starlette`.

  ```bash
  gh repo edit modern-python/modern-di-starlette \
    --add-topic python \
    --add-topic dependency-injection \
    --add-topic di \
    --add-topic ioc-container \
    --add-topic modern-di \
    --add-topic starlette
  ```
  If Step 1 showed stray topics not in the intended set, remove each with `--remove-topic <name>`.

- [ ] **Step 4: Verify**

  ```bash
  gh repo view modern-python/modern-di-starlette --json description,homepageUrl,repositoryTopics
  ```
  Expected: description `modern-di integration for Starlette`, homepage `https://modern-di.modern-python.org`, topics exactly the six above.

---

### Task 5: Open the PR

**Files:** none.

- [ ] **Step 1: Push the branch**

  ```bash
  git push -u origin starlette-brand
  ```

- [ ] **Step 2: Open the PR**

  ```bash
  gh pr create --fill --title "Onboard modern-di-starlette: brand mark + surfaces"
  ```

- [ ] **Step 3: Watch CI**

  ```bash
  gh pr checks --watch
  ```
  Expected: all checks green. (If a stale `refs/pull/<n>/merge` lint failure appears that doesn't reproduce locally at branch HEAD, push a fresh commit to force GitHub to recompute the merge ref — see CLAUDE.md "CI gotcha".)

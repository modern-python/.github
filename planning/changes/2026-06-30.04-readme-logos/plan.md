# README logos — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A centered, theme-aware brand banner atop all 17 repo READMEs —
generated as light/dark/PNG lockups in `.github` and embedded via `<picture>`.

**Spec:** [`design.md`](./design.md)

**Branch (this `.github` bundle + assets):** `brand-readme-logos`. **Per docs/repo branch:** `readme-logo`.

**Commit strategy:** Tasks 1–2 = the `.github` PR; Tasks 3+ = one PR per repo.

## Global constraints

- **Two phases, ordered:** Phase 1 = the `.github` PR (lockup assets + docs;
  Tasks 1–2). It must be **merged to `main` first** so the
  `raw.githubusercontent.com/.../main/...` URLs resolve. Phase 2 = the 17
  README PRs (Task 3 pilot + Task 4 the rest), opened after Phase 1 is on `main`.
- **Assets are central** in `.github` `brand/projects/<repo>/`; the 17 repo PRs
  are **README-only** (no asset copies).
- **Lockup colourways:** light = `struct=GREEN_INK`, `accent=GOLD_LIGHT`, name
  `GREEN_INK`; dark = `struct=CREAM`, `accent=GOLD_DARK`, name `CREAM`, inner gold
  `GOLD_LIGHT`→`GOLD_DARK` (cream negatives stay). Tokens: `GREEN_INK #356852`,
  `GOLD_LIGHT #c98a00`, `GOLD_DARK #f0b528`, `CREAM #f4f1e8`.
- **Per-repo assets:** `lockup-light.svg`, `lockup-dark.svg`, `lockup.png` (the
  light lockup rasterized via `export_png`, hence auto-quantized).
- **The 17 repos:** modern-di, that-depends, modern-di-fastapi, modern-di-litestar,
  modern-di-faststream, modern-di-typer, modern-di-pytest,
  fastapi-sqlalchemy-template, litestar-sqlalchemy-template, lite-bootstrap,
  httpware, faststream-redis-timers, faststream-concurrent-aiokafka,
  faststream-outbox, db-retry, eof-fixer, semvertag.
- **The README banner** (exact; substitute `<repo>` — its README filename is
  `README.md` except `fastapi-sqlalchemy-template`, which uses `readme.md`):

  ```html
  <p align="center">
    <picture>
      <source media="(prefers-color-scheme: dark)"  srcset="https://raw.githubusercontent.com/modern-python/.github/main/brand/projects/<repo>/lockup-dark.svg">
      <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/modern-python/.github/main/brand/projects/<repo>/lockup-light.svg">
      <img alt="<repo>" src="https://raw.githubusercontent.com/modern-python/.github/main/brand/projects/<repo>/lockup.png" width="420">
    </picture>
  </p>
  ```

- **Per-repo README procedure** (Task 3 and each repo in Task 4):
  1. `gh repo clone modern-python/<repo> /Users/kevinsmith/src/pypi/.readme-clones/<repo>` (mkdir the parent once; `git -C … pull --ff-only` if it exists).
  2. `cd` in; `git checkout -b readme-logo`.
  3. In the README (`README.md`, or `readme.md` for the template), **replace the
     leading H1** — the first line matching `^# <repo>\s*$` — with the banner
     block above (repo substituted). If there is no leading `# <repo>` line,
     insert the banner as the first line instead (and report it). Leave the badge
     row and all other content untouched.
  4. Verify (below).
  5. `git add -A && git commit -m "docs: add brand logo banner to README"`;
     `git push -u origin readme-logo`; `gh pr create --base main` (body: one line
     + the 🤖 line).
  6. `gh pr checks <n>` to completion.

- **Per-repo verification:** (a) the README's first non-blank line is
  `<p align="center">` and the file no longer contains a leading `# <repo>`
  heading; (b) all three URLs contain `/brand/projects/<repo>/` and the filenames
  `lockup-dark.svg` / `lockup-light.svg` / `lockup.png`; (c) if the repo builds a
  distribution, `uv build` then `uvx twine check dist/*` reports PASS (this
  validates the long_description renders for PyPI); if it isn't a package (the two
  templates), skip twine and just confirm (a)+(b).
- Imports at module level; annotate args; `# ty: ignore` not `# type: ignore`.
  CI gate is `just` (= check-planning + pytest); ruff not a gate.

---

### Task 1: Light/dark/PNG lockups in `brand/build`

**Files:**
- Modify: `brand/build/projects.py`
- Test: `tests/test_lockups.py` (new)
- Regenerate: `brand/projects/**/lockup-*.svg`, `brand/projects/**/lockup.png`

**Interfaces:**
- Produces: `project_lockup(repo: str, *, dark: bool = False) -> str`;
  `render_projects` writes `lockup-light.svg`, `lockup-dark.svg`, `lockup.png` per
  repo (replacing the old single `lockup.svg`).

- [ ] **Step 1: Write the failing test**

  ```python
  # tests/test_lockups.py
  from pathlib import Path
  from xml.dom import minidom

  from PIL import Image

  from brand.build import projects as p
  from brand.build import tokens as t


  def test_light_and_dark_lockup_colourways() -> None:
      light = p.project_lockup("modern-di")
      dark = p.project_lockup("modern-di", dark=True)
      minidom.parseString(light)
      minidom.parseString(dark)
      assert t.GREEN_INK in light and t.GOLD_LIGHT in light
      # dark uses the on-dark colourway: cream + gold-dark, never the dark-green ink
      assert t.CREAM in dark and t.GOLD_DARK in dark
      assert t.GREEN_INK not in dark


  def test_render_writes_three_lockup_assets(tmp_path: Path) -> None:
      p.render_projects(out_dir=tmp_path)
      d = tmp_path / "modern-di"
      assert (d / "lockup-light.svg").is_file()
      assert (d / "lockup-dark.svg").is_file()
      png = d / "lockup.png"
      assert png.is_file()
      assert Image.open(png).mode == "P"  # quantized via export_png
  ```

- [ ] **Step 2: Run to verify it fails**

  Run: `uv run pytest tests/test_lockups.py -q`
  Expected: FAIL — `project_lockup` has no `dark` kwarg / `lockup-light.svg` not written.

- [ ] **Step 3: Generalize `project_lockup` + emit three assets**

  Replace `project_lockup` in `brand/build/projects.py` with:

  ```python
  def project_lockup(repo: str, *, dark: bool = False) -> str:
      """Framed mark + the repo name in Jost. Light = green-ink/gold (light UIs);
      dark = cream/gold-dark (dark UIs). Transparent background either way."""
      struct = t.CREAM if dark else t.GREEN_INK
      accent = t.GOLD_DARK if dark else t.GOLD_LIGHT
      name_color = t.CREAM if dark else t.GREEN_INK
      mark_frame = g.project_frame(struct=struct, accent=accent)
      inner = MANIFEST[repo]()
      if dark:
          inner = inner.replace(t.GOLD_LIGHT, t.GOLD_DARK)
      name_x = _LOCKUP_H + _GAP
      name_svg, name_w = outline_text(
          repo,
          _NAME_SIZE,
          x=name_x,
          baseline_y=_LOCKUP_H / 2 + _NAME_SIZE * 0.34,
          anchor="start",
          color=name_color,
      )
      total_w = round(name_x + name_w + _GAP)
      return (
          f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {_LOCKUP_H}" '
          f'role="img" aria-label="{repo}"><g>{mark_frame}{inner}</g>{name_svg}</svg>'
      )
  ```

  In `render_projects`, replace the single `lockup.svg` write line with:

  ```python
          (d / "lockup-light.svg").write_text(project_lockup(repo) + "\n", encoding="utf-8")
          dark_svg = d / "lockup-dark.svg"
          dark_svg.write_text(project_lockup(repo, dark=True) + "\n", encoding="utf-8")
          export_png(d / "lockup-light.svg", d / "lockup.png")
  ```

  (`export_png(svg, png)` with no width/height rasterizes at the SVG's natural size
  and quantizes; that's the light PNG fallback.) Update the `render_projects`
  docstring's "lockup.svg" mention to the three new names.

- [ ] **Step 4: Run to verify it passes**

  Run: `uv run pytest tests/test_lockups.py -q`
  Expected: PASS (2 tests).

- [ ] **Step 5: Regenerate + sanity-render a dark lockup, then commit**

  ```bash
  uv run python -m brand.build.render
  rsvg-convert -w 480 brand/projects/modern-di/lockup-dark.svg -o /tmp/lockup-dark.png  # eyeball: cream+gold-dark on transparent
  git add brand/build/projects.py tests/test_lockups.py brand/projects
  git status --short | grep -E "lockup\.svg" && echo "NOTE: old lockup.svg files are now untracked/removed — git rm them" || true
  git rm brand/projects/*/lockup.svg 2>/dev/null || true
  git add brand/projects
  git commit -m "feat(brand): light/dark/png lockups for README banners"
  ```
  The `git rm` removes the superseded single `lockup.svg` per repo (render no
  longer writes it). Confirm `git status` is clean after.

---

### Task 2: `.github` docs + finalize bundle

**Files:**
- Modify: `brand/README.md`, `architecture/brand-marks.md`
- Modify: `planning/changes/2026-06-30.04-readme-logos/design.md` (summary)

- [ ] **Step 1: `brand/README.md`** — note the lockup outputs changed to
  `lockup-light.svg` / `lockup-dark.svg` / `lockup.png` (light + dark colourways +
  PyPI PNG fallback), used as README banners across the org.

- [ ] **Step 2: `architecture/brand-marks.md`** — append: each repo has
  `lockup-{light,dark}.svg` + `lockup.png`; the dark colourway is cream + gold-dark
  (mirrors `wordmark-dark`); READMEs embed them via `<picture>` from the `.github`
  raw path.

- [ ] **Step 3: Finalize the bundle summary** in `design.md`, e.g.:
  `summary: README logos shipped — light/dark/png lockups generated in .github; centered <picture> banner replaces the H1 in all 17 repo READMEs.`

- [ ] **Step 4: Verify + commit**

  ```bash
  uv run pytest -q        # all green
  just check-planning     # planning: OK
  uv run python -m brand.build.render   # clean; git status shows no asset churn
  git add brand/README.md architecture/brand-marks.md planning/changes/2026-06-30.04-readme-logos/design.md
  git commit -m "docs(brand): document README lockups"
  ```
  Then push `brand-readme-logos` and open the `.github` PR (Tasks 1–2). **This PR
  must merge before Phase 2.**

---

### Task 3: README banner — pilot (`modern-di`)

> Phase 2. Do this only after the Task 1–2 `.github` PR is merged to `main`
> (otherwise the raw URLs 404). Pilot to confirm the H1 replacement + render.

**Repo:** `modern-python/modern-di` (`README.md`, leading line `# modern-di`).

- [ ] **Step 1: Clone + branch** — per the Global per-repo procedure, into `…/.readme-clones/modern-di`, branch `readme-logo`.
- [ ] **Step 2: Replace the leading H1** — swap the first `# modern-di` line for the banner block (Global Constraints), `<repo>`=`modern-di`. Confirm the badge row immediately below is untouched.
- [ ] **Step 3: Verify** — first non-blank line is `<p align="center">`; no `# modern-di` heading remains; the 3 URLs contain `/brand/projects/modern-di/`; `uv build` then `uvx twine check dist/*` → PASS.
- [ ] **Step 4: Commit + push + PR** — `docs: add brand logo banner to README`; `gh pr create --base main`, body names the banner + 🤖 line.
- [ ] **Step 5: Watch CI** — `gh pr checks <n>` to completion.

---

### Task 4: README banner — remaining 16 repos

> Phase 2, after the `.github` PR is merged. Apply the **Global per-repo
> procedure** to each repo below; each is its own `readme-logo` branch + PR +
> verification (treat each as an independent unit). README filename is `README.md`
> except `fastapi-sqlalchemy-template` (`readme.md`). For each, verify the 3 URLs
> contain `/brand/projects/<repo>/`, the leading `# <repo>` H1 is replaced, and
> (packages only) `uvx twine check dist/*` passes after `uv build`.

- [ ] `that-depends`
- [ ] `modern-di-fastapi`
- [ ] `modern-di-litestar`
- [ ] `modern-di-faststream`
- [ ] `modern-di-typer`
- [ ] `modern-di-pytest`
- [ ] `fastapi-sqlalchemy-template`  *(readme.md; not a PyPI package — skip twine, confirm URLs + banner placement; its leading heading may differ, replace the first H1 or insert at top and report)*
- [ ] `litestar-sqlalchemy-template`  *(not a PyPI package — skip twine)*
- [ ] `lite-bootstrap`
- [ ] `httpware`
- [ ] `faststream-redis-timers`
- [ ] `faststream-concurrent-aiokafka`
- [ ] `faststream-outbox`
- [ ] `db-retry`
- [ ] `eof-fixer`
- [ ] `semvertag`

---

## Notes for the executor

- **Hard gate:** open no Phase-2 README PR until the Task 1–2 `.github` PR is on
  `main` — the banner URLs resolve only then.
- The 17 README edits are independent and mechanically identical (replace the
  leading H1 with the banner, substitute `<repo>`); they can be dispatched in
  parallel, each its own PR and review.
- Work in `/Users/kevinsmith/src/pypi/.readme-clones/<repo>`, never in `.github`.
- Do not touch anything but the leading H1 in each README.
- Some packages may need build deps for `uv build`; if a repo can't build a dist,
  fall back to confirming the banner block + URLs and rely on the repo's CI /
  `twine check` in its release flow — and say so in the report.

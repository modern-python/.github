# brand PNG optimization — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every generated brand PNG is committed palette-quantized (~70–80%
smaller, visually lossless), via a Pillow step in `raster.py`.

**Spec:** [`design.md`](./design.md)

**Branch:** `brand-png-optimize` (already created)

**Commit strategy:** per-task commits.

## Global constraints

- **Pillow** is the only new dependency, added to the `dev` dependency group in
  `pyproject.toml` (beside `fonttools`). No Node, no required system binary.
  `uv.lock` is git-ignored — don't commit it.
- Quantize uses `Image.Quantize.FASTOCTREE` (preserves alpha for transparent
  marks AND works for opaque cards), `colors = 32` (constant `_PNG_COLORS`).
- Only `brand/build/raster.py` changes in the pipeline; **no** changes to
  `render.py`, `geometry.py`, `symbols.py`, `projects.py`, or any SVG output.
- The quantize step degrades gracefully (no-op) if Pillow is import-unavailable,
  mirroring the existing `rsvg-convert`-optional pattern.
- Regenerate and commit all PNGs (`uv run python -m brand.build.render`); the
  committed artifact is always the optimized one.
- CI gate is `just` (= `check-planning` + `pytest`); ruff is not a CI gate.
- Imports at module level (the one allowed exception is the in-function
  `from PIL import Image` guarded by `try/except ModuleNotFoundError`, which is
  the graceful-skip mechanism — keep it local so a missing Pillow can't break
  module import); annotate function args; `# ty: ignore` not `# type: ignore`.

---

### Task 1: Palette-quantize PNGs in the build

**Files:**
- Modify: `pyproject.toml` (add `pillow` to the `dev` group)
- Modify: `brand/build/raster.py`
- Create: `tests/test_pngopt.py`
- Regenerate: `brand/org/**.png`, `brand/projects/**/*.png`

**Interfaces:**
- Consumes: `projects.render_projects(out_dir: Path | None = None) -> list[Path]`
  (writes `mark.svg`, `mark-512.png`, `mark-1024.png`, `lockup.svg`, and — for
  `DOCS_REPOS` — `social-card.svg/png` per repo).
- Produces: `raster._quantize_png(path: Path, colors: int = _PNG_COLORS) -> None`;
  `export_png` now writes a palette-quantized PNG.

- [ ] **Step 1: Add Pillow to the dev dependency group**

  In `pyproject.toml`, under `[dependency-groups]` `dev`, add `pillow`:

  ```toml
  [dependency-groups]
  dev = [
      "fonttools>=4.63.0",
      "pillow>=11.0.0",
      "pytest>=9.1.1",
  ]
  ```

  Then sync: `uv sync`. Expected: Pillow installed (no lock file is committed —
  `uv.lock` is git-ignored).

- [ ] **Step 2: Write the failing test**

  ```python
  # tests/test_pngopt.py
  from pathlib import Path

  from PIL import Image

  from brand.build import projects as p


  def _render(tmp: Path) -> None:
      p.render_projects(out_dir=tmp)


  def test_social_card_png_is_quantized_and_small(tmp_path: Path) -> None:
      _render(tmp_path)
      card = tmp_path / "modern-di" / "social-card.png"
      im = Image.open(card)
      assert im.mode == "P", f"expected indexed palette, got {im.mode}"
      assert im.size == (1280, 640)
      assert card.stat().st_size < 20_000, card.stat().st_size


  def test_transparent_mark_png_keeps_alpha_and_is_small(tmp_path: Path) -> None:
      _render(tmp_path)
      mark = tmp_path / "modern-di" / "mark-1024.png"
      im = Image.open(mark)
      assert im.mode == "P", f"expected indexed palette, got {im.mode}"
      assert im.size == (1024, 1024)
      assert "transparency" in im.info, "transparent mark lost its alpha"
      assert mark.stat().st_size < 15_000, mark.stat().st_size


  def test_card_palette_is_actually_reduced(tmp_path: Path) -> None:
      _render(tmp_path)
      card = tmp_path / "modern-di" / "social-card.png"
      colors = Image.open(card).convert("RGB").getcolors(maxcolors=100_000)
      assert colors is not None and len(colors) <= 40, (
          f"card should be palette-reduced; found {None if colors is None else len(colors)} colours"
      )
  ```

- [ ] **Step 3: Run the test to verify it fails**

  Run: `uv run pytest tests/test_pngopt.py -q`
  Expected: FAIL — the PNGs are currently RGBA (`im.mode == "RGBA"`, not `"P"`)
  and far larger than the ceilings (`rsvg-convert` output ~25–55 KB).

- [ ] **Step 4: Implement the quantize step in `raster.py`**

  Read `brand/build/raster.py` first. Add the constant + helper near the top
  (after the imports) and call the helper at the end of `export_png` after a
  successful `rsvg-convert`:

  ```python
  _PNG_COLORS = 32  # palette size; flat art needs few (8 already looked clean; 32 = headroom)


  def _quantize_png(path: Path, colors: int = _PNG_COLORS) -> None:
      """Re-save a PNG as an indexed-palette image — visually lossless for flat
      art. FASTOCTREE preserves alpha, so it is correct for both the opaque
      social cards and the transparent marks. No-op if Pillow is unavailable."""
      try:
          from PIL import Image
      except ModuleNotFoundError:
          return
      im = Image.open(path).convert("RGBA")
      q = im.quantize(colors=colors, method=Image.Quantize.FASTOCTREE)
      q.save(path, format="PNG", optimize=True)
  ```

  `export_png`'s signature is
  `export_png(svg_path, png_path, *, width=None, height=None) -> bool`, so the
  output path is `png_path`. After the `subprocess.run([...], check=True)` that
  writes the PNG and immediately before `return True`, add:

  ```python
      _quantize_png(png_path)
  ```

- [ ] **Step 5: Run the test to verify it passes**

  Run: `uv run pytest tests/test_pngopt.py -q`
  Expected: PASS (3 tests) — PNGs are mode `P`, transparent mark keeps
  `transparency`, sizes under the ceilings.

- [ ] **Step 6: Regenerate the committed PNGs and commit**

  ```bash
  uv run python -m brand.build.render
  git add pyproject.toml brand/build/raster.py tests/test_pngopt.py brand/org brand/projects
  ```
  Sanity-check the shrinkage before committing:
  ```bash
  du -sh brand/projects/*/social-card.png | sort -h | tail -3   # each should be ~10-15 KB now
  ```
  Then commit:
  ```bash
  git commit -m "feat(brand): palette-quantize generated PNGs (Pillow FASTOCTREE)"
  ```

---

### Task 2: Docs + finalize

**Files:**
- Modify: `brand/README.md`
- Modify: `architecture/brand-marks.md`
- Modify: `planning/changes/2026-06-30.03-png-optimization/design.md` (summary)

- [ ] **Step 1: Note it in `brand/README.md`**

  In the `## Per-project marks (brand/projects/)` subsection (or the Outputs
  area), add a sentence:

  ```markdown
  PNGs are palette-quantized at build time (`brand/build/raster.py`, Pillow
  FASTOCTREE) — indexed-colour and ~70–80% smaller than raw `rsvg-convert`
  output, with no visible change (the art is flat-colour). Regenerate with
  `uv run python -m brand.build.render`.
  ```

- [ ] **Step 2: Note it in `architecture/brand-marks.md`**

  Append to the per-project/marks section:

  ```markdown
  All generated PNGs are palette-quantized in `raster.py` (`_quantize_png`,
  Pillow FASTOCTREE, `_PNG_COLORS` palette) so the committed binaries are
  indexed-colour and compact; alpha is preserved for the transparent marks.
  SVGs are left as generated.
  ```

- [ ] **Step 3: Finalize the bundle summary**

  Set the `summary:` in this bundle's `design.md` to the realized result, e.g.:
  `summary: Brand PNGs palette-quantized in the build (Pillow FASTOCTREE) — committed indexed-colour, ~70-80% smaller, visually lossless.`

- [ ] **Step 4: Verify**

  Run: `uv run pytest -q` → all green.
  Run: `just check-planning` → `planning: OK`.
  Run: `uv run python -m brand.build.render` → clean; `git status` shows no
  unexpected changes (PNGs already committed in Task 1 reproduce identically —
  FASTOCTREE is deterministic).

- [ ] **Step 5: Commit**

  ```bash
  git add brand/README.md architecture/brand-marks.md planning/changes/2026-06-30.03-png-optimization/design.md
  git commit -m "docs(brand): document PNG quantization"
  ```

---

## Notes for the executor

- After both tasks: push the branch and open a PR (do not local-merge); watch CI.
- Do not touch SVGs or add `pngquant`/`oxipng`/`svgo` — out of scope.
- If `git status` after the final `render` shows PNG churn, FASTOCTREE
  non-determinism is the suspect — investigate before merging (the design expects
  byte-identical reproduction).
- The 7 open docs-repo PRs still carry the large cards; refreshing them is a
  separate follow-up (noted in the spec's Operations), not part of this branch.

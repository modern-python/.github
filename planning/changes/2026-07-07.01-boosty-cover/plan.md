# boosty-cover — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Boosty profile-cover target to the brand generator that emits an
8:1 1920×240 green-colorway header banner (MODERN/PYTHON lockup + tagline, side
by side) as SVG + PNG in `brand/org/`.

**Spec:** [`design.md`](./design.md)

**Branch:** `boosty-profile-cover`

**Commit strategy:** Per-task commits.

## Global Constraints

- Green colorway only: `bg = #2f5e4a` (`tokens.GREEN_SURFACE`), `struct = #f4f1e8`
  (`tokens.CREAM`), `gold = #f0b528` (`tokens.GOLD_DARK`). No other colors.
- Cover SVG viewBox is exactly `0 0 1920 240` (8:1, Boosty's header slot); the
  lockup is `scale(0.9)`; the tagline `Open-source Python for production` is
  outlined at `tag_size=40`, `letter_spacing=4`, set to the lockup's right with a
  60 px gap, and the pair is centered on x=960 using the measured tagline width.
- PNG size: `width=1920, height=240`.
- All imports at module level; annotate all function arguments; `ty: ignore`
  never `type: ignore`.
- Brand casing in prose: `modern-python`, `modern-di`. Tagline has no trailing
  period.
- Generated SVG **and** PNG under `brand/org/` are committed.
- No dependency changes, so `uv.lock` must not change (leave it alone).
- Commit only on the `boosty-profile-cover` branch, never `main`. End commit
  messages with the `Co-Authored-By: Claude Opus 4.8 (1M context)
  <noreply@anthropic.com>` trailer. Do not mention Claude Code in the body.
- Run `just check-planning` and `just test` before pushing. Finish via PR.

---

### Task 1: Cover geometry (`geometry.boosty_cover`)

**Files:**
- Modify: `brand/build/geometry.py` (add function after `social_square()`)
- Test: `tests/test_geometry.py` (add one test)

- [ ] **Step 1: Write the failing test** in `tests/test_geometry.py`:

```python
def test_boosty_cover(parse_svg):
    svg = g.boosty_cover(bg="#2f5e4a", struct="#f4f1e8", gold="#f0b528")
    el = parse_svg(svg)
    assert el.attrib["viewBox"] == "0 0 1920 240"  # 8:1 Boosty header
    assert 'fill="#2f5e4a"' in svg  # full-bleed green bg
    assert 'width="1920" height="240"' in svg  # full-bleed rect
    assert "scale(0.9)" in svg  # lockup scaled into the short strip
    assert "M138 122 L138 50 L210 50" in svg  # carries the lockup crops
    assert "<text" not in svg  # tagline outlined, not live text
    assert "#f4f1e8" in svg and "#f0b528" in svg
    assert "var(" not in svg
    # the tagline adds outlined glyph paths beyond the bare wordmark
    assert svg.count("<path") > g.wordmark(struct="#f4f1e8", gold="#f0b528").count("<path")
```

- [ ] **Step 2: Run test, verify it fails** —
  `uv run pytest tests/test_geometry.py::test_boosty_cover -v`
  Expected: `AttributeError: ... has no attribute 'boosty_cover'`.

- [ ] **Step 3: Implement** `boosty_cover` in `brand/build/geometry.py` per the
  spec's §1 code block.

- [ ] **Step 4: Run test, verify it passes.**

- [ ] **Step 5: Commit**

```bash
git add brand/build/geometry.py tests/test_geometry.py
git commit -m "feat(brand): boosty_cover wide banner geometry"
```

---

### Task 2: Render target + regenerate assets

**Files:**
- Modify: `brand/build/render.py` (write SVG + export PNG after the green card)
- Test: `tests/test_assets.py` (add a boosty-cover render test)

- [ ] **Step 1: Write the failing test** in `tests/test_assets.py`:

```python
def test_render_writes_boosty_cover():
    _render()
    cover = ORG / "boosty-cover.svg"
    assert cover.exists()
    ET.parse(cover)
    text = cover.read_text()
    assert 'viewBox="0 0 1920 240"' in text
    assert 'fill="#2f5e4a"' in text and "#f4f1e8" in text and "#f0b528" in text
    assert "<text" not in text and "var(" not in text
    if shutil.which("rsvg-convert"):
        assert (ORG / "boosty-cover.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
```

- [ ] **Step 2: Run test, verify it fails** —
  `uv run pytest tests/test_assets.py::test_render_writes_boosty_cover -v`
  Expected: `assert cover.exists()` is False.

- [ ] **Step 3: Wire render.py.** After the `social-card-green` block in
  `render()`, add:

```python
    # Boosty profile cover (green colorway) — brand/org/boosty-cover.*
    _write(
        ORG / "boosty-cover.svg",
        g.boosty_cover(bg=t.GREEN_SURFACE, struct=t.CREAM, gold=t.GOLD_DARK),
    )
    export_png(
        ORG / "boosty-cover.svg", ORG / "boosty-cover.png", width=1920, height=240
    )
```

- [ ] **Step 4: Run test, verify it passes.**

- [ ] **Step 5: Regenerate and commit**

```bash
uv run python -m brand.build.render
git add brand/build/render.py tests/test_assets.py brand/org/boosty-cover.svg brand/org/boosty-cover.png
git commit -m "feat(brand): boosty profile cover render target"
```

  Expected: `git status` shows only the two new `brand/org/boosty-cover.*` files
  plus the edited sources — no other asset churn.

---

### Task 3: Architecture promotion

**Files:**
- Modify: `architecture/brand-marks.md` (note the Boosty cover under Org marks)

- [ ] **Step 1: Promote the capability** — add to the Org marks description that
  `brand/org/boosty-cover.svg|png` is a 1920×480 green-colorway profile-header
  banner for `boosty.to/lesnik512`, generated by `geometry.boosty_cover`
  (centered `lockup_body` + outlined tagline).

- [ ] **Step 2: Verify** — `just test` (all pass) and `just check-planning`
  (`planning: OK`).

- [ ] **Step 3: Commit**

```bash
git add architecture/brand-marks.md
git commit -m "docs(brand): promote boosty cover to architecture"
```

---

## Notes for the executor

- Follow the existing one-function-per-asset pattern; do not restructure
  `geometry.py` or `render.py` beyond the additions above.
- The cover is **not** added to `just sync-assets` — the site does not serve it.
- If Boosty's uploader wants a different size, change only the `export_png`
  width/height in `render.py` and re-render.
- Finish via PR (push `boosty-profile-cover`, open a PR); do not local-merge.
  Watch CI after pushing.

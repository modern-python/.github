# Org T-Shirt Artwork Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an apparel target to the brand generator that emits print-ready artwork (transparent left-chest chevron mark + back wordmark/URL lockup) for a black org t-shirt.

**Architecture:** A new pure geometry function `geometry.apparel_back()` composes the existing `lockup_body()` wordmark over an outlined `modern-python.org` line in one transparent SVG. A new `brand/build/apparel.py` render module writes both artworks (chest reuses the existing `mark()`) as SVG + 300 DPI PNG into `brand/apparel/`, wired into `render.py`. Docs and the architecture capability file are updated in the same branch.

**Tech Stack:** Python 3, `uv` (packaging), `pytest`, `ruff`, `ty`; SVG generated as strings; `rsvg-convert` (librsvg) for PNG rasterization; `fontTools` for text outlining (already used).

## Global Constraints

- Colorway is exactly two inks: cream `struct = #f4f1e8` (`tokens.CREAM`) and gold-dark `gold = #f0b528` (`tokens.GOLD_DARK`). No other colors; no background rect (transparent art).
- Back-lockup SVG viewBox is exactly `118 32 304 228`; URL is `outline_text("modern-python.org", 18, x=270, baseline_y=240, anchor="middle", color=gold, letter_spacing=3)`.
- PNG print sizes at 300 DPI: chest `width=1050` (3.5 in), back `width=2400` (8 in).
- All imports at module level, never inside function bodies. Annotate all function arguments.
- For type-checker suppressions use `ty: ignore`, never `type: ignore`.
- Brand casing in prose: `modern-python`, `modern-di`. Domain rendered as `modern-python.org`. No trailing period on the canonical one-liner.
- Generated SVG **and** PNG assets under `brand/apparel/` are committed, same as `brand/org/` and `brand/projects/`.
- This change touches no dependencies, so `uv.lock` must not change (it is tracked in this repo; leave it alone).
- Commit only on a feature branch (e.g. `org-tshirt-apparel`), never on `main`. End commit messages with the `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` trailer. Do not mention Claude Code in the body.
- Run `just check-planning` and `just test` (or `uv run pytest`) before pushing.

---

### Task 1: Back-lockup geometry (`geometry.apparel_back`)

**Files:**
- Modify: `brand/build/geometry.py` (add function after `mark()`, before `social_card()`)
- Test: `tests/test_geometry.py` (add one test)

**Interfaces:**
- Consumes: existing `geometry.lockup_body(*, struct: str, gold: str) -> str`, `text.outline_text(...)`, `geometry.wordmark(*, struct: str, gold: str) -> str`.
- Produces: `geometry.apparel_back(*, struct: str, gold: str) -> str` — a complete transparent `<svg>` string (viewBox `118 32 304 228`) with the wordmark lockup plus the outlined `modern-python.org` line beneath it. Consumed by Task 2's `apparel.py`.

- [ ] **Step 1: Write the failing test**

Add to `tests/test_geometry.py`:

```python
def test_apparel_back_wordmark_plus_url(parse_svg):
    svg = g.apparel_back(struct="#f4f1e8", gold="#f0b528")
    el = parse_svg(svg)
    assert el.attrib["viewBox"] == "118 32 304 228"  # wordmark viewBox extended for the URL
    assert el.attrib["aria-label"] == "Modern Python, modern-python.org"
    assert "<rect width=" not in svg  # transparent — no background fill
    assert "M138 122 L138 50 L210 50" in svg  # carries the lockup crops
    assert "<text" not in svg  # URL is outlined to paths, not live text
    assert "#f4f1e8" in svg and "#f0b528" in svg
    assert "var(" not in svg
    # the URL adds outlined glyph paths beyond the bare wordmark
    assert svg.count("<path") > g.wordmark(struct="#f4f1e8", gold="#f0b528").count("<path")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_geometry.py::test_apparel_back_wordmark_plus_url -v`
Expected: FAIL with `AttributeError: module 'brand.build.geometry' has no attribute 'apparel_back'`

- [ ] **Step 3: Write minimal implementation**

In `brand/build/geometry.py`, add after the `mark()` function:

```python
def apparel_back(*, struct: str, gold: str) -> str:
    """Back-of-shirt lockup: the MODERN/PYTHON wordmark with the full domain
    outlined beneath it, transparent, for the cream+gold-dark colorway. Extends
    the `wordmark` viewBox downward to seat the URL centered on the same axis."""
    url, _ = outline_text(
        "modern-python.org",
        18,
        x=270,
        baseline_y=240,
        anchor="middle",
        color=gold,
        letter_spacing=3,
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="118 32 304 228" '
        'role="img" aria-label="Modern Python, modern-python.org">'
        + lockup_body(struct=struct, gold=gold)
        + url
        + "</svg>"
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_geometry.py::test_apparel_back_wordmark_plus_url -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add brand/build/geometry.py tests/test_geometry.py
git commit -m "feat(brand): apparel_back wordmark+URL lockup geometry"
```

---

### Task 2: Apparel render target (`brand/build/apparel.py` + render wiring)

**Files:**
- Create: `brand/build/apparel.py`
- Modify: `brand/build/render.py` (import + call after `render_projects()`)
- Test: `tests/test_assets.py` (add `APPAREL` path + one render test)

**Interfaces:**
- Consumes: `geometry.mark(*, struct, gold)`, `geometry.apparel_back(*, struct, gold)` (Task 1), `tokens.CREAM`, `tokens.GOLD_DARK`, `raster.export_png(svg_path, png_path, *, width)`.
- Produces: `apparel.render_apparel() -> None`, writing `brand/apparel/{chest-mark.svg, chest-mark-1050.png, back-lockup.svg, back-lockup-2400.png}`.

- [ ] **Step 1: Write the failing test**

In `tests/test_assets.py`, add the apparel path next to `ORG` (top of file, after `ORG = Path("brand/org")`):

```python
APPAREL = Path("brand/apparel")
```

Then add this test:

```python
def test_render_writes_apparel():
    _render()
    chest = APPAREL / "chest-mark.svg"
    back = APPAREL / "back-lockup.svg"
    assert chest.exists() and back.exists()
    ET.parse(chest)
    ET.parse(back)
    ctext = chest.read_text()
    assert 'points="45,40 57,50 45,60"' in ctext  # chevron
    assert 'width="100" height="100"' not in ctext  # transparent, no bg rect
    assert "#f4f1e8" in ctext and "#f0b528" in ctext
    btext = back.read_text()
    assert 'aria-label="Modern Python, modern-python.org"' in btext
    assert "<text" not in btext  # outlined URL
    assert "<rect width=" not in btext  # transparent
    assert "#f4f1e8" in btext and "#f0b528" in btext
    if shutil.which("rsvg-convert"):
        for name in ("chest-mark-1050.png", "back-lockup-2400.png"):
            assert (APPAREL / name).read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_assets.py::test_render_writes_apparel -v`
Expected: FAIL — `assert chest.exists()` is False (render does not produce apparel yet).

- [ ] **Step 3: Create the apparel render module**

Create `brand/build/apparel.py`:

```python
from pathlib import Path

from brand.build import geometry as g
from brand.build import tokens as t
from brand.build.raster import export_png

ROOT = Path(__file__).resolve().parents[2]
APPAREL = ROOT / "brand" / "apparel"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")


def render_apparel() -> None:
    """Print-ready artwork for the black org t-shirt: a transparent left-chest
    chevron mark and a back wordmark+URL lockup, both cream + gold-dark. SVG is
    the master; PNGs are 300 DPI print fallbacks (chest 3.5 in, back 8 in)."""
    APPAREL.mkdir(parents=True, exist_ok=True)
    ink = dict(struct=t.CREAM, gold=t.GOLD_DARK)
    _write(APPAREL / "chest-mark.svg", g.mark(**ink))
    export_png(APPAREL / "chest-mark.svg", APPAREL / "chest-mark-1050.png", width=1050)
    _write(APPAREL / "back-lockup.svg", g.apparel_back(**ink))
    export_png(APPAREL / "back-lockup.svg", APPAREL / "back-lockup-2400.png", width=2400)
```

- [ ] **Step 4: Wire it into `render.py`**

In `brand/build/render.py`, add the import beside the existing `render_projects` import:

```python
from brand.build.apparel import render_apparel
```

Then, at the end of `render()`, immediately after the `render_projects()` call, add:

```python
    # Apparel artwork (brand/apparel/).
    render_apparel()
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/test_assets.py::test_render_writes_apparel -v`
Expected: PASS (PNG assertions run only if `rsvg-convert` is installed).

- [ ] **Step 6: Regenerate assets and commit**

```bash
uv run python -m brand.build.render
git add brand/build/apparel.py brand/build/render.py tests/test_assets.py brand/apparel/
git commit -m "feat(brand): apparel render target for the org t-shirt"
```

Expected: `git status` shows the four new `brand/apparel/` files (two SVG, two PNG) staged. If `rsvg-convert` is not installed, the two PNGs will be absent — install librsvg (`brew install librsvg`) and re-run `render` before committing so the print fallbacks are included.

---

### Task 3: Print spec + architecture promotion

**Files:**
- Create: `brand/apparel/README.md`
- Modify: `architecture/brand-marks.md` (add an Apparel section)

**Interfaces:**
- Consumes: the files produced by Task 2. No code.
- Produces: documentation only.

- [ ] **Step 1: Write the print spec**

Create `brand/apparel/README.md`:

```markdown
# Apparel artwork

Print-ready artwork for the **black** modern-python org t-shirt, generated by
`brand/build/apparel.py`. Regenerate with:

```bash
uv run python -m brand.build.render
```

## Colorway

Two-ink spot print, cream + gold-dark (the on-dark org treatment):

| Token | Hex | Role |
|-------|-----|------|
| Cream | `#f4f1e8` | MODERN, top crop, chevron snake |
| Gold-dark | `#f0b528` | PYTHON, bottom crop, chevron, URL |

## Files

| File | Placement | Print size |
|------|-----------|-----------|
| `chest-mark.svg` / `chest-mark-1050.png` | Left chest, standard placement | ~3.5 in wide |
| `back-lockup.svg` / `back-lockup-2400.png` | Back, centered, ~4-5 in below collar | ~8 in wide |

The transparent chevron mark is `geometry.mark`; the back lockup (wordmark +
`modern-python.org`) is `geometry.apparel_back`. PNGs are 300 DPI fallbacks;
prefer the SVGs (vector) for print. Send the vendor a black garment with a
2-color print in the two hexes above.
```

- [ ] **Step 2: Promote the capability into `architecture/brand-marks.md`**

Append a new section to `architecture/brand-marks.md`:

```markdown
## Apparel (`brand/apparel/`)

Print-ready artwork for the black org t-shirt, generated by
`brand/build/apparel.py::render_apparel` from the same primitives as the org
marks, in the cream + gold-dark colorway (a 2-ink spot print). Two artworks:
`chest-mark.svg` (the transparent chevron `geometry.mark`, left chest) and
`back-lockup.svg` (`geometry.apparel_back` — the MODERN/PYTHON wordmark with
`modern-python.org` outlined beneath it, viewBox `118 32 304 228`, back print).
Each ships a 300 DPI PNG fallback (`chest-mark-1050.png` 3.5 in,
`back-lockup-2400.png` 8 in). Regenerate via `uv run python -m brand.build.render`;
placement and vendor notes live in `brand/apparel/README.md`.
```

- [ ] **Step 3: Verify the full suite and planning**

Run: `just test`
Expected: all tests PASS, including `test_apparel_back_wordmark_plus_url` and `test_render_writes_apparel`.

Run: `just check-planning`
Expected: `planning: OK`

- [ ] **Step 4: Commit**

```bash
git add brand/apparel/README.md architecture/brand-marks.md
git commit -m "docs(brand): apparel print spec + architecture promotion"
```

---

## Notes for the executor

- The `design.md` in this bundle is the *why*; its `summary` is already written
  as the realized result and needs no edit at ship.
- Do not restructure `geometry.py` or `render.py` beyond the additions above —
  follow the existing one-function-per-asset pattern.
- If the rendered URL sits too close to or too far from PYTHON, adjust only
  `baseline_y` (currently 240) in `apparel_back` and re-render; the viewBox
  height (228) has ~16u of margin below a 240 baseline.
- Finish via PR (push the `org-tshirt-apparel` branch, open a PR); do not
  local-merge. Watch CI after pushing.

---
summary: Brand PNGs palette-quantized in the build (Pillow FASTOCTREE) — committed indexed-colour, ~70-80% smaller, visually lossless.
---

# Design: Brand PNG optimization

## Summary

Fold a palette-quantization pass into the brand build so every generated PNG is
committed in a compact indexed form. The art is flat 2–3 colour, so quantizing
`rsvg-convert`'s 32-bit RGBA output to a small palette is **visually lossless**
and cuts each PNG ~70–80% (social cards ~55 KB → ~13 KB, `mark-1024` ~25 KB →
~8 KB; total committed PNGs ~1.0 MB → ~0.3 MB). Done with **Pillow** (a pip/uv
dependency — no Node, no required system binary), inside `raster.py` so the
committed artifact is always the optimized one. SVGs are deliberately left alone.

## Motivation

The brand kit commits 52 PNGs (~1.0 MB). `rsvg-convert` emits 32-bit RGBA with
default zlib — uncompressed for flat art. Research and a measured test showed
palette quantization is the one meaningful win: a flat-colour 1280×640 card drops
from 55 KB to ~10–15 KB with no visible change (palette-8 was already
indistinguishable by eye; transparent marks quantized with FASTOCTREE preserve
alpha with no edge fringing — both verified on cream and dark backgrounds).

This is **repo-hygiene, not performance**: the assets already clear every social
scraper limit (Facebook 8 MB, X 5 MB) by 12×+ and gzip well over the wire. The
value is a smaller repo and smaller cards copied into the 7 docs repos
(~50 KB → ~13 KB each).

## Non-goals

- **SVG optimization.** Our SVGs are machine-generated with no editor cruft and
  glyph paths are integer font-units; the served SVGs (favicon/mark/wordmark/
  lockup) are 0.7–12 KB and gzip well, and the big `social-card.svg` is a build
  source, not served. Not worth adding `svgo` (Node) or `scour` for a few hundred
  bytes.
- **External optimizers.** No `pngquant`/`oxipng` dependency; Pillow already
  captures the dominant win uv-natively. (A future change could use them
  optionally for a few extra percent — out of scope.)
- **og:image aspect ratio.** Cards are 1280×640 (2:1) vs the canonical
  1200×630; that's a separate design question, not compression. Untouched.
- **Re-copying optimized cards into the 7 docs repos.** A follow-up (see
  Operations); not done in this change.

## Design

### 1. Quantization in `raster.py`

`export_png` currently shells out to `rsvg-convert` and returns `bool`. Add a
post-write step that re-saves the PNG palette-quantized:

```python
_PNG_COLORS = 32  # palette size; flat art needs few. 8 already looked clean; 32 = headroom.


def _quantize_png(path: Path, colors: int = _PNG_COLORS) -> None:
    """Re-save a PNG as an indexed-palette image (visually lossless for flat art).
    FASTOCTREE preserves alpha, so it is correct for both the opaque social cards
    and the transparent marks. No-op (leaves the RGBA file) if Pillow is absent."""
    try:
        from PIL import Image
    except ModuleNotFoundError:
        return
    im = Image.open(path).convert("RGBA")
    q = im.quantize(colors=colors, method=Image.Quantize.FASTOCTREE)
    q.save(path, format="PNG", optimize=True)
```

`export_png` calls `_quantize_png(png_path)` after a successful `rsvg-convert`.
If `rsvg-convert` is absent there's no PNG and nothing to quantize (unchanged
behaviour). Pillow is a committed dependency, so in normal builds/CI every PNG is
quantized; the `try/except` keeps the build working if it's ever missing.

This is the only code change to the pipeline — `render.py`, `geometry.py`,
`symbols.py`, `projects.py`, and all SVG output are untouched. Because `export_png`
is the single chokepoint for every PNG (org marks, project marks, lockups PNGs,
social cards), one edit covers them all.

### 2. Dependency

Add `pillow` to the `dev` dependency group in `pyproject.toml` (beside
`fonttools`, which the brand build already needs). This repo **tracks** `uv.lock`
(it's the site app, not a distributed package, and `uv.lock` is not in
`.gitignore`), so the lock update is committed alongside.

### 3. Regenerate & commit

Run `uv run python -m brand.build.render` to rewrite every PNG under `brand/org/`
and `brand/projects/` in quantized form, and commit the smaller binaries.

## Operations

After this merges, the optimized cards differ from the ~50 KB copies currently in
the **7 open docs-repo PRs** (`modern-di#248`, `that-depends#219`,
`lite-bootstrap#141`, `httpware#86`, `faststream-redis-timers#54`,
`faststream-outbox#120`, `semvertag#43`). Recommended follow-up (separate, per
repo): re-copy `brand/projects/<repo>/social-card.png` into each branch so the
docs sites ship the small card. Not part of this change.

## Out of scope

- SVG optimization; external PNG optimizers; the og:image aspect ratio; the docs-repo card refresh (above).

## Testing

Render into a tmp dir and assert, with Pillow:

- A social card (`brand/projects/modern-di/social-card.png`) opens in mode `"P"`
  (indexed), is 1280×640, and is below a ceiling (e.g. `< 20_000` bytes).
- A transparent mark (`brand/projects/modern-di/mark-1024.png`) opens in mode
  `"P"`, is 1024×1024, **still carries transparency** (`"transparency" in info`),
  and is below a ceiling (e.g. `< 15_000` bytes).
- Guard against fidelity regressions cheaply: assert the quantized card's colour
  count is small (`len(Image.open(card).convert("RGB").getcolors(maxcolors=100000)) <= _PNG_COLORS + small slack`) — i.e. it really is palette-reduced, not silently left RGBA.

Plus: full `uv run pytest` green; `uv run python -m brand.build.render` runs
clean; `just check-planning` OK.

## Risk

- **Alpha handling on transparent marks.** Naïve MEDIANCUT drops alpha; the
  design uses `FASTOCTREE`, verified to preserve per-index alpha with no edge
  fringing on light and dark backgrounds. Likelihood low, impact medium if wrong;
  the test asserts transparency is retained.
- **Over-aggressive palette banding.** 32 colours is conservative for ≤5-colour
  art; verified visually lossless. If a future richer mark ever bands, raise
  `_PNG_COLORS`. Likelihood low.
- **Determinism.** FASTOCTREE is deterministic for a given input, so re-running
  the build reproduces identical bytes — no spurious diffs. Likelihood low.

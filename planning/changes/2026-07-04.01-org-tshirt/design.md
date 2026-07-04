---
summary: Add an apparel target to the brand generator — a transparent left-chest chevron mark and a back wordmark+URL lockup, in the cream/gold-dark colorway, as print-ready SVG + 300 DPI PNG for a black org t-shirt.
---

# Design: modern-python org t-shirt artwork

## Summary

Add a new **apparel** output to the brand kit (`brand/build/`) that renders the
two print-ready artworks for a black org t-shirt: a small **left-chest chevron
mark** and a large **back lockup** (the MODERN/PYTHON wordmark with
`modern-python.org` beneath it). Both print in the two-ink cream + gold-dark
colorway (`#f4f1e8` + `#f0b528`) — the same treatment as the org avatar and site
header — so the whole garment is a 2-color spot print. Everything is drawn from
existing `geometry.py` primitives; the only new geometry is a back-lockup
composition that stacks the existing wordmark over an outlined URL line. Outputs
land in `brand/apparel/` as vector SVG plus 300 DPI PNG, regenerable via
`uv run python -m brand.build.render`.

## Motivation

The org has a full generated brand kit but no apparel artwork. A physical
t-shirt (org swag) needs files a print shop can use: vector art in the correct
colorway for a dark garment, at real print sizes. Producing these by hand would
drift from the repo's "every asset is generated from `brand/build/`" convention;
wiring them into the generator keeps them reproducible and on-palette.

The visual was settled interactively (front/back mockups): black garment,
transparent chevron mark on the left chest, and a ~8 in back lockup with the
full domain set small beneath the wordmark.

## Non-goals

- No physical/print ordering, vendor choice, or garment sourcing — files only.
- No proof/mockup asset committed (reviewed via the live mockups; skipped).
- No new colorways or garment colors — black only, one colorway.
- No changes to org marks, project marks, social cards, or site wiring.
- No new palette tokens — reuses `CREAM` and `GOLD_DARK`.

## Design

### 1. Back-lockup geometry — `brand/build/geometry.py`

Add `apparel_back(*, struct, gold)`: the transparent wordmark lockup with the
full domain outlined beneath it, in one SVG. It reuses `lockup_body()` (the
MODERN/PYTHON crop-mark lockup, drawn in the 540×250 space) and `outline_text()`
(the same font-outlining path the social card URL uses, so nothing depends on a
font at serve time). The viewBox extends the wordmark's `118 32 304 184` down to
fit the URL line, keeping the same horizontal center (x=270).

```python
def apparel_back(*, struct: str, gold: str) -> str:
    """Back-of-shirt lockup: the MODERN/PYTHON wordmark with the full domain
    outlined beneath it, transparent, for the cream+gold-dark colorway."""
    url, _ = outline_text(
        "modern-python.org", 18, x=270, baseline_y=240,
        anchor="middle", color=gold, letter_spacing=3,
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="118 32 304 228" '
        'role="img" aria-label="Modern Python — modern-python.org">'
        + lockup_body(struct=struct, gold=gold)
        + url
        + "</svg>"
    )
```

The URL is set in `gold` (gold-dark) — the wordmark supplies `struct` (cream) for
MODERN and gold for PYTHON, so the graphic stays within the two allowed inks. The
size (18u) and baseline (240u, ~40u below the crop bottom) reproduce the
signed-off "S2" mockup: clearly secondary to the wordmark, still legible.

The chest art needs no new geometry — it is the existing
`mark(struct=CREAM, gold=GOLD_DARK)` (transparent chevron, viewBox `0 0 100 100`).

### 2. Apparel render module — `brand/build/apparel.py`

New module mirroring `projects.py`'s shape, exposing `render_apparel()`. Writes
to `brand/apparel/`:

```python
def render_apparel() -> None:
    APPAREL.mkdir(parents=True, exist_ok=True)
    ink = dict(struct=t.CREAM, gold=t.GOLD_DARK)
    _write(APPAREL / "chest-mark.svg", g.mark(**ink))
    export_png(APPAREL / "chest-mark.svg", APPAREL / "chest-mark-1050.png", width=1050)
    _write(APPAREL / "back-lockup.svg", g.apparel_back(**ink))
    export_png(APPAREL / "back-lockup.svg", APPAREL / "back-lockup-2400.png", width=2400)
```

PNG widths are the print sizes at 300 DPI: chest 3.5 in → 1050 px (→ 1050×1050);
back 8 in → 2400 px (→ 2400×1800, aspect preserved by `rsvg-convert -w`). PNGs
go through the existing `export_png` → `_quantize_png` path (indexed color, alpha
preserved). Without `rsvg-convert` the SVGs still write and PNGs are skipped, as
elsewhere.

### 3. Render wiring — `brand/build/render.py`

Import `render_apparel` and call it after `render_projects()` at the end of
`render()`. No other change.

### 4. Print spec — `brand/apparel/README.md`

Short prose the print shop reads: black garment; 2-color spot print (cream
`#f4f1e8` + gold-dark `#f0b528`); left-chest mark ~3.5 in wide at standard
left-chest placement; back lockup ~8 in wide, centered, ~4–5 in below the
collar; prefer the SVGs (vector), PNGs are 300 DPI fallbacks. Regenerate with
`uv run python -m brand.build.render`.

### 5. Architecture promotion — `architecture/brand-marks.md`

Add an **Apparel** section documenting the new capability: what
`brand/apparel/` holds, the colorway, and that it is generated by
`apparel.py` / `geometry.apparel_back` from the same primitives as the org
marks.

## Out of scope

Other garment colors (would need the light green-ink/gold-light colorway),
long-sleeve/sleeve prints, stickers, and any non-shirt merch. Each is a clean
follow-up reusing the same primitives if wanted later.

## Testing

- New `tests/test_geometry.py::test_apparel_back`: viewBox is
  `118 32 304 228`; carries the lockup crops (`M138 122 L138 50 L210 50`);
  contains the outlined domain (glyph `<path>`s, **no** `<text>`); is transparent
  (no full-bleed background rect); uses only `#f4f1e8` and `#f0b528`; no `var(`.
- Extend the asset test (`tests/test_assets.py`) to assert the four
  `brand/apparel/` files parse as valid SVG / exist after render, mirroring how
  org and project assets are checked.
- `just test` green; `just sync-assets` (or `python -m brand.build.render`) is a
  deterministic no-op diff apart from the new apparel files.
- Visual check of `chest-mark.svg` and `back-lockup.svg` (and the PNGs) on a dark
  background before committing.
- `just check-planning` passes before pushing.

## Risk

- **Low: URL baseline/size looks off against the wordmark** once rendered with
  the real Jost outline (mockup used a fallback font). Mitigated — `baseline_y`
  and `size` are single constants in `apparel_back`; adjust and re-render if the
  vertical gap reads wrong. The visual target is the approved S2 mockup.
- **Low: PNGs absent in CI** if `rsvg-convert` is unavailable. Same behavior as
  existing targets — SVGs still generate; PNGs are the machine-produced
  fallback, committed from a dev machine that has librsvg.
- **Low: back graphic exceeds the shirt print area at 8 in.** Mitigated — 8 in
  is a conservative standard back-print width; the size lives in one place and is
  trivially changed.

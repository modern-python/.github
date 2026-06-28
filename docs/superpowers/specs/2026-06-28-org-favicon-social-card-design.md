# modern-python org favicon + social card — design spec

**Status:** approved design (brainstorming output)
**Scope:** the org-level **favicon** and **social card** only. Everything else
(per-project marks, the subfamily/family system, inner glyphs, framework
integrations) is explicitly **deferred** to a later task.

This supersedes the snake-based mark in open PR #16 for the org identity. The
two deliverables here use a new mark co-designed visually; PR #16's generator
and assets are replaced by the toolchain described below.

---

## The mark (org identity)

A **pinwheel of two interlocked "snakes"** — two corner brackets with square
heads, rotated opposite each other (top-left + bottom-right), reading as the
two Python snakes abstracted. Two forms:

1. **Icon** — the two snakes reaching the borders (square **block head** at one
   end, **diagonal-cut tail** at the other) around a **gold chevron**, on a
   square full-bleed tile. One mark at every size — favicon, apple-touch, and the
   GitHub avatar — plus a padded `icon_circle` variant for circular crops (Telegram).
2. **Wordmark lockup** — the same two snakes as **crop marks** (block head +
   diagonal-cut tail) framing the stacked wordmark `MODERN` / `PYTHON`. Used for
   the social card and square.

### Palette (concrete)

| Token | Hex | Role |
|-------|-----|------|
| Green (ink, on light) | `#356852` | snakes/text on cream |
| Green (surface) | `#2f5e4a` | green-background fills |
| Gold (on light) | `#c98a00` | accent on cream |
| Gold (on dark) | `#f0b528` | accent on green |
| Cream | `#f4f1e8` | light surface; **and** the light "ink" on green (not pure white) |

Two-color pairing: the **top-left** snake + `MODERN` use the green/cream
"structure" color; the **bottom-right** snake + `PYTHON` use gold. On cream the
structure color is green `#356852`; on green it is cream `#f4f1e8`.

### Typeface

**Jost** (SIL OFL — free for commercial use, embedding, and outlining), weight
400. Wordmark glyphs are **outlined to SVG paths** at build time so assets
render without the font installed (same approach the repo already uses for
JetBrains Mono). Jost + its OFL license are vendored under `brand/build/fonts/`.

---

## Geometry (authoritative coordinates)

### Icon (100×100 viewBox) — favicon / apple-touch / avatar

One mark (`_icon_mark`), used full-bleed by `icon()` and padded by `icon_circle()`.
Snakes reach the borders; each has a square **block head** at one end and a
**diagonal-cut tail** (outer edge straight, inner edge sliced) at the other. Tail
polygon bases overlap the stroke by ~2px so tail and body render as one shape.
```
bg:       rect 0 0 100 100  fill BG  (square, no rx)
snake TL: path "M15 68 L15 15 L68 15"  stroke STRUCT  width 11  (butt, miter)
head TL:  rect x61 y8 w14 h14 rx2      fill STRUCT
tail TL:  polygon "9.5,66 9.5,79 20.5,66"   fill STRUCT
snake BR: path "M85 32 L85 85 L32 85"  stroke GOLD    width 11
head BR:  rect x25 y78 w14 h14 rx2     fill GOLD
tail BR:  polygon "90.5,34 90.5,21 79.5,34"  fill GOLD
chevron:  polyline "45,40 57,50 45,60"  stroke GOLD  width 6  (round)
```
`icon_circle` wraps the mark in `translate(50,50) scale(0.74) translate(-50,-50)`
so it fits inside the inscribed circle with margin.
On green: BG `#2f5e4a`, STRUCT (top-left snake) cream `#f4f1e8`, GOLD (bottom-right
snake + chevron) `#f0b528`.

### Wordmark lockup (540×250 viewBox — the unit scaled into cards)

```
snake TL: path "M138 122 L138 50 L210 50"  stroke STRUCT  width 8  (butt, miter)
snake BR: path "M402 128 L402 200 L330 200" stroke GOLD   width 8
head TL:  rect x202.5 y42.5 w15 h15 rx3  fill STRUCT
head BR:  rect x322.5 y192.5 w15 h15 rx3  fill GOLD
tail TL:  polygon "134,120 134,130 142,120"  fill STRUCT
tail BR:  polygon "406,130 406,120 398,130"  fill GOLD
MODERN:   x270 y126  Jost 400  size 50  fill STRUCT  text-anchor middle  textLength 210
PYTHON:   x270 y166  Jost 400  size 50  fill GOLD    text-anchor middle  textLength 210
```
`textLength 210` + `lengthAdjust="spacingAndGlyphs"` pins each line's width so
the crop marks frame the text exactly regardless of renderer. Baselines 126/166
= **gap 40**.

---

## Deliverables

### Icon set (one mark, every size)
- `favicon.svg` + `favicon-16/32/48.png` — browser favicon.
- `apple-touch-icon.svg` + `apple-touch-icon-180.png` — iOS (square, full-bleed).
- `avatar.svg` + `avatar-1024.png` — GitHub org picture (square).
- `avatar-circle.svg` + `avatar-circle-1024.png` — **padded** variant for
  platforms that crop avatars to a circle (e.g. Telegram).

### Social card
- `social-card.svg` / `social-card.png` — **1280×640**, **cream** (primary):
  bg `#f4f1e8`, lockup green `#356852` + gold `#c98a00`, URL `#c98a00`.
- `social-card-green.svg` / `.png` — 1280×640 **green** alternate: bg `#2f5e4a`,
  lockup cream `#f4f1e8` + gold `#f0b528`, URL `#f0b528`.
- `social-square.svg` / `.png` — **640×640** (Telegram / square social), cream
  and green variants, wordmark centered (no URL).

Card composition (1280×640): the 540×250 lockup is embedded **uniformly scaled**
`translate(235,108) scale(1.5)` (no internal reproportioning); URL `modern-python.org`
centered at `x640 y575`, size 34, letter-spacing 4, gold. No tagline.

Square (640×640): lockup `translate(-193.0,82.5) scale(1.9)` (enlarged, box-centered), no URL.

---

## Build toolchain

Extend/replace `brand/build/` (Python):
- `tokens.py` — the five colors above.
- `text.py` — outline Jost glyphs to SVG paths (fonttools), as today.
- `geometry.py` — emit the icon, favicon, wordmark lockup, and card
  compositions from the coordinates above.
- `render.py` — write every SVG, bake concrete colors, and rasterize PNGs via
  `rsvg-convert` (guarded by `shutil.which`, skip PNGs if absent — as today).

Regenerate with `uv run python -m brand.build.render`. Tests assert each asset
exists, parses, contains the right baked colors (no `var()`), and that PNGs
carry the PNG magic when `rsvg-convert` is present.

All Python follows house rules: imports at module level, annotated args,
`ty: ignore` not `type: ignore`.

---

## Out of scope (deferred)

- Per-project / per-repo marks and README logos.
- The subfamily/family system (Scheme B) and any inner glyphs.
- Framework integration colors and lockups.
- Site (`mkdocs.yml`) wiring beyond dropping in the new favicon + og:image
  (a thin follow-up, not this task's design).

---

## Open question for review

- **URL on the card** is fixed copy `modern-python.org`. Confirm that is the
  canonical domain to print.

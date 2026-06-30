# modern-python brand kit

Source of truth for the org's **favicon** and **social card**. Generated assets
live in `brand/org/`. Regenerate with:

```bash
uv run python -m brand.build.render
```

PNGs require `rsvg-convert` (`brew install librsvg` / `apt install librsvg2-bin`).
Without it the SVGs are still written and PNGs are skipped.

## Palette

| Token | Hex | Role |
|-------|-----|------|
| Green ink | `#356852` | snakes/text on cream |
| Green surface | `#2f5e4a` | green backgrounds |
| Gold (light) | `#c98a00` | accent on cream |
| Gold (dark) | `#f0b528` | accent on green |
| Cream | `#f4f1e8` | light surface; light ink on green |

## Mark

Two interlocked "snakes" (corner brackets with square heads) as a pinwheel. The
**icon** wraps them around a gold core dot (favicon + avatar). The **wordmark
lockup** pulls them into crop marks framing `MODERN` / `PYTHON` set in **Jost**
(SIL OFL, outlined to paths at build time — see `brand/build/fonts/Jost-OFL.txt`).

## Outputs (`brand/org/`)

| File | What |
|------|------|
| `favicon.svg`, `favicon-16/32/48.png` | browser favicon (bold reduction, green) |
| `apple-touch-icon.svg`, `apple-touch-icon-180.png` | iOS home-screen (full-bleed) |
| `avatar.svg`, `avatar-1024.png` | GitHub org picture |
| `social-card.svg` / `.png` | 1280×640 og:image, **cream** (primary) |
| `social-card-green.svg` / `.png` | 1280×640, green alternate |
| `social-square.svg` / `.png`, `social-square-green.*` | 640×640 (Telegram) |

## Per-project marks (`brand/projects/`)

Each repo gets a large-format mark: the constant green+gold snake-frame with
one gold inner symbol (see `brand/build/projects.py::MANIFEST`). Regenerate
with `uv run python -m brand.build.render`; outputs land in
`brand/projects/<repo>/` as `mark.svg`, three lockup files (see below), and
PNGs. These are large-format only — every repo's favicon/avatar stays the org mark.

### Lockup outputs

Each repo gets three lockup files:

| File | Colourway | Use |
|------|-----------|-----|
| `lockup-light.svg` | green-ink + gold on transparent | GitHub light theme |
| `lockup-dark.svg` | cream + gold-dark on transparent | GitHub dark theme |
| `lockup.png` | light lockup rasterized + quantized | PyPI fallback (`<img>`) |

The dark colourway (cream + `#f0b528` gold-dark) mirrors the org `wordmark-dark`.
These are used as README banners across the org via a `<picture>` element that
references the assets at their `raw.githubusercontent.com` URL in `.github`.
Repos with a docs site also get a `social-card.svg` + `social-card.png`
(1280×640 og:image): the repo mark on a green panel beside its name, tagline,
and docs URL on cream. The docs-site repos are listed in
`brand/build/projects.py::DOCS_REPOS`.

PNGs are palette-quantized at build time (`brand/build/raster.py`, Pillow
FASTOCTREE) — indexed-colour, with no visible change (the art is flat-colour).
The large assets (social cards, 1024px marks) shrink ~70–80% vs raw
`rsvg-convert` output; the tiny favicons less. Regenerate with
`uv run python -m brand.build.render`.

## Deferred (not in this kit)

The header nav logo redesign is a follow-up.

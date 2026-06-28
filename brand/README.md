# modern-python brand kit

Source of truth for all visual assets across the modern-python org.
Generated files live in `brand/org/` and `brand/projects/<slug>/`.

---

## Palette

### Org colors

| Role        | Light       | Dark        |
|-------------|-------------|-------------|
| Green (struct / frame / ink) | `#356852` | `#3f8064` |
| Gold (accent / monogram) | `#c98a00` | `#e0a300` |
| Teal (messaging frame) | `#2a9d8f` | — |
| Amber (utilities frame) | `#c2722b` | — |

Green is the primary brand color: frame strokes, org mark bands, wordmark ink.
Gold is the accent: inner snake band and gold-ink monograms.
Teal and amber are category frame colors for messaging and utility repos respectively.

### Framework ink colors

These are starting approximations, harmonized per spec §5.3 against each
upstream framework's own brand palette. Verify against the upstream brand
before using them in non-generated contexts.

| Framework   | Light ink   | Dark ink    |
|-------------|-------------|-------------|
| FastAPI     | `#009688`   | `#2dd4bf`   |
| Litestar    | `#5b8def`   | `#93b4ff`   |
| FastStream  | `#c2569b`   | `#e879c0`   |
| Typer       | `#1f9ed1`   | `#5bc0f0`   |
| pytest      | `#3aae6b`   | `#5fd99a`   |

---

## Org mark

The org icon is two nested rounded-square snake glyphs:

- **Outer snake** — green stroke, head dot at top-left.
- **Middle snake** — gold stroke, head dot at bottom-right (counter-rotated).
- **Core dot** — green filled circle at center.

The favicon is the two-band reduction (outer + middle snake, core dot dropped).

Both icons adapt to dark mode via `prefers-color-scheme`.

---

## Project icon system

Every project icon is a **rounded-square frame** (outer snake only, no middle band
or core dot) in the category frame color, plus an inner device:

| Category              | Frame color | Inner device              | Ink         |
|-----------------------|-------------|---------------------------|-------------|
| DI core (`modern-di`) | Green       | Gold monogram ("di")      | Gold        |
| DI integrations       | Green       | Framework-colored letters (2-char initials) | Framework color |
| Templates             | Green       | Framework-colored stack glyph (three stacked bars) | Framework color |
| Messaging             | Teal        | Gold monogram             | Gold        |
| Utilities             | Amber       | Gold monogram             | Gold        |

**Integration vs. template distinction**: integration icons use **letter monograms**
(e.g. "fa" for FastAPI). Template icons use a **stack glyph** (three horizontal
rounded bars), representing a layered scaffold rather than a framework abbreviation.

---

## Light/dark file matrix

| Asset | Auto-adapts? | Files |
|-------|-------------|-------|
| `brand/org/icon.svg` | Yes — `prefers-color-scheme` CSS | single file |
| `brand/org/icon-light.svg` | No — colors baked in | explicit light |
| `brand/org/icon-dark.svg` | No — colors baked in | explicit dark |
| `brand/org/favicon.svg` | Yes — `prefers-color-scheme` CSS | single file |
| `brand/org/horizontal.svg` | Yes | single file |
| `brand/org/stacked.svg` | Yes | single file |
| `brand/org/social.svg` / `.png` | Light only (og:image) | baked light |
| `brand/projects/<slug>/icon.svg` | No | light only |
| `brand/projects/<slug>/icon-dark.svg` | No | dark only |
| `brand/projects/<slug>/horizontal.svg` | No | light only |
| `brand/projects/<slug>/horizontal-dark.svg` | No | dark only |
| `brand/projects/<slug>/stacked.svg` | No | light only |
| `brand/projects/<slug>/stacked-dark.svg` | No | dark only |

Use a `<picture>` element to serve the right variant in GitHub READMEs and
other contexts that don't execute inline CSS:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="icon-dark.svg">
  <img src="icon.svg" alt="modern-di" width="48">
</picture>
```

For browsers (e.g. inline SVG on the org site) the auto-adapting single-file
variants work directly without `<picture>`.

---

## Regenerating assets

```bash
uv run python -m brand.build.render
```

PNGs (`favicon.png`, `social.png`) require `rsvg-convert` (part of
`librsvg`). Install with `brew install librsvg` on macOS or
`apt install librsvg2-bin` on Debian/Ubuntu. If `rsvg-convert` is absent the
script still writes all SVG files; PNGs are skipped silently.

---

## Adding a new repo

Open `brand/build/render.py` and add a call to `render_project()` inside
`main()`:

```python
render_project(
    "my-new-repo",          # slug — matches brand/projects/<slug>/
    "monogram",             # "monogram" for DI/messaging/utility, "template" for scaffolds
    "my-new-repo",          # wordmark text (used in horizontal + stacked lockups)
    "my-new-repo",          # aria-label
    initials="mn",          # 2-char initials (monogram only)
    frame_color=t.GREEN,    # GREEN / TEAL / AMBER per category table above
    ink=t.GOLD,             # GOLD or a FRAMEWORK color
)
```

For a template repo, omit `initials` and pass `"template"` as the second arg:

```python
render_project(
    "my-template",
    "template",
    "my-template",
    "my-template",
    frame_color=t.GREEN,
    ink=t.FRAMEWORK["fastapi"],
)
```

Then run `uv run python -m brand.build.render` to produce the six SVG files
under `brand/projects/my-new-repo/`.

---

## Font license

Wordmarks use **JetBrains Mono SemiBold**, licensed under the SIL Open Font
License 1.1 (`brand/build/fonts/OFL.txt`). The OFL covers the font files only;
SVG paths produced by outlining glyphs are unencumbered — they are not
themselves "font software" under the OFL's terms.

---

## Follow-ups (out of scope here)

- White nav-icon variant for the MkDocs Material header (`theme.logo`).
- `render_project()` calls for the remaining ~13 repos (one PR per batch).

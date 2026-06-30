---
summary: Per-repo social cards (1280×640 og:image) for the 7 docs-site repos — two-panel green/cream, built on the project marks.
---

# Design: Per-repo social cards

## Summary

Generate a **social card** (1280×640 `og:image`) for each org repo that has a
live docs site. The card is a two-panel composition: a green panel holding the
repo's project **mark** (the snake-frame + its gold inner symbol, shipped in the
previous change) and a cream panel with the repo **name**, its one-line
**tagline**, and its **docs URL**. Cards are produced by the existing
`brand/build/` pipeline into `brand/projects/<repo>/social-card.svg` +
`social-card.png`, for the seven docs-site repos only.

## Motivation

The per-project marks shipped (`brand/projects/<repo>/mark.svg|lockup.svg`), but
a repo's docs site still has no branded `og:image` — link unfurls on
GitHub/Slack/X fall back to a generic screenshot or nothing. The org site already
ships a social card (`brand/build/geometry.py::social_card`); this extends that
to each docs-site repo, reusing the marks we just built so the family reads
consistently when shared.

The seven repos with live docs sites were determined by probing
`https://<repo>.modern-python.org/` (HTTP 200): `modern-di`, `that-depends`,
`lite-bootstrap`, `httpware`, `faststream-redis-timers`, `faststream-outbox`,
`semvertag`. The other ten repos do not resolve and get no card.

## Non-goals

- Cards for repos without a docs site (the other ten) — `og:image` is only
  valuable where a docs site exists.
- Wiring each card into its repo's docs `og:image` / `twitter:image` meta — that
  edits each downstream repo and is per-repo follow-up, tracked separately.
- A square / Telegram variant per repo — only the 1280×640 card for now (YAGNI).
- Changing the org card or the project marks — unchanged.

## Design

### 1. Layout (two-panel)

1280×640, two panels:

- **Green panel** — `x ∈ [0, 460)`, fill `GREEN_SURFACE #2f5e4a`. The repo's
  mark (its `project_frame` + inner symbol) drawn in **`CREAM`** struct +
  **`GOLD_DARK`** accent (the on-green colourway), ~300px, vertically centred
  (`translate(80,170) scale(3.0)`).
- **Cream panel** — `x ∈ [460, 1280]`, fill `CREAM`. A vertically-centred text
  block at left edge `x = 520`, column width `≈ 700px`:
  - **name** — Jost, `GREEN_INK`, base 74px, **auto-shrunk** to the column width
    if its natural width exceeds it (size scaled, aspect preserved).
  - **tagline** — Jost, `GREEN_MUTED` (new token), 30px, **word-wrapped** to the
    column width (1–3 lines in practice).
  - **url** — `<repo>.modern-python.org`, Jost, `GOLD_LIGHT`, 26px,
    `letter_spacing=2`.

  The block (name + N tagline lines + url) is centred vertically by computing its
  height from the line count and offsetting from the card centre, so 1-line and
  3-line taglines both sit balanced. Validated visually for a short
  (`modern-di`), medium (`faststream-outbox`, 2 lines) and long (`httpware`,
  3 lines) tagline.

### 2. Data

- **Mark + inner symbol:** reuse `projects.py::MANIFEST[repo]`.
- **Tagline:** the **canonical one-liner** from `profile/README.md` — the same
  text kept in sync with each repo's GitHub description and pyproject
  `description` (per CLAUDE.md's "three surfaces" rule). Captured as a
  `DOCS_REPOS: dict[str, str]` (repo → tagline) in `projects.py`. Verbatim, so
  there is no new copy to maintain — if the canonical blurb changes, update this
  one table.
- **URL:** derived as `f"{repo}.modern-python.org"`.

`DOCS_REPOS` keys are a strict subset of `MANIFEST`; a test asserts that.

### 3. Build pipeline

- Two text helpers (in `projects.py`, used only by the card):
  - `fit_text(text, base_size, max_w, *, color, x, baseline_y) -> str` — renders
    via `text.outline_text`; if the natural width exceeds `max_w`, re-renders at
    `base_size * max_w / natural` so it fits without horizontal squishing.
  - `wrap_text(text, size, max_w) -> list[str]` — greedy word-wrap using
    `outline_text`'s measured width per trial line.
- `project_social_card(repo: str, *, tagline: str) -> str` — composes the two
  panels + mark + name/tagline/url into a 1280×640 `<svg>`.
- `render_projects` gains a pass: for each `repo, tagline` in `DOCS_REPOS`, write
  `brand/projects/<repo>/social-card.svg` and rasterise `social-card.png`
  (1280×640) via the existing `raster.export_png`.
- Add `GREEN_MUTED` to `brand/build/tokens.py` (the tagline colour) so the card
  uses only named tokens.

### 4. Outputs

`brand/projects/<repo>/social-card.svg` + `social-card.png` for the seven docs
repos. `brand/README.md` and `architecture/brand-marks.md` note the new output.

## Operations

None in-repo. Pointing each docs site's `og:image` at its card (copying the PNG
into the repo and setting the meta) is per-repo follow-up.

## Out of scope

- Downstream `og:image` wiring (per repo).
- Square/alternate sizes; light/dark variants of the card.

## Testing

- Each of the seven cards parses as XML, is `viewBox="0 0 1280 640"`, and uses
  only palette colours (`tokens` + `GREEN_MUTED`).
- `fit_text`: a string wider than `max_w` yields a smaller font size than base; a
  string that fits stays at base. `wrap_text`: a long tagline returns >1 line; a
  short one returns exactly 1.
- `render_projects(out_dir=tmp)` writes `social-card.svg` for exactly the seven
  `DOCS_REPOS` and for none of the other ten repos.
- `DOCS_REPOS` ⊆ `MANIFEST` (no orphan/typo repo key).

## Risk

- **Tagline length / overflow.** The longest canonical blurb (`httpware`, ~105
  chars) wraps to three lines; anything longer could crowd the card. Likelihood
  low (blurbs are capped ~120 chars by convention), impact low (it stays
  centred). *Mitigation:* `wrap_text` handles arbitrary length; if a future blurb
  is too long for the card, shorten that one `DOCS_REPOS` value.
- **Docs-site set drift.** A repo could gain/lose a docs site later. *Mitigation:*
  `DOCS_REPOS` is one explicit table; re-probe and edit it. Cheap.
- **Tagline duplication vs. profile/README.** The blurb now lives in two files.
  *Mitigation:* both are governed by the same CLAUDE.md "three surfaces" rule;
  the test set is small and the canonical text rarely changes.

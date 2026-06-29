---
summary: Per-project marks shipped — 17 repos, constant snake-frame + gold inner symbol, generated into brand/projects/.
---

# Design: Per-project and per-family brand marks

## Summary

Extend the org brand kit (currently only the org favicon/social card) with a
**per-repository logo system**. Every repo gets a large-format mark built from
the **same green+gold "snake" frame** with a single **gold inner symbol** that
says what the project does. It is a strict two-colour system (forest green +
ochre gold on cream), differentiated by *symbol shape*, not colour. Marks are
generated programmatically in `brand/build/` (the same pipeline that draws the
org mark) and emitted under `brand/projects/<repo>/`. The org favicon/avatar and
the small-size identity are unchanged — these new marks are **large-format only**
(docs hero, README banner).

## Motivation

The org mark shipped in `brand/org/` (favicon, avatar, social cards) and the
backstage story (`brand/STORY.md`, "Act 2 — the family that never shipped")
explicitly deferred the per-project system: *"the frame stays constant and an
inner glyph marks each sub-family."* `brand/projects/` exists but is empty, and
`brand/README.md` lists "per-project / per-repo marks, the subfamily system" as
a later task. This change delivers that system across all ~17 repos so each
project's docs site and README can carry a recognisable, on-brand mark.

Research into comparable systems informed the approach: Astral (uv/ruff/ty) and
the JetBrains/Adobe families show that a **constant frame + a per-product inner
mark** reads as a family while staying individually identifiable, and that
leaning on *two* discriminators is only needed when marks must survive tiny
sizes. Because these marks are large-format only (favicons stay the org mark),
shape alone is a sufficient discriminator and a single accent colour (gold)
keeps the system tight.

## Non-goals

- Small-size / favicon use — every repo keeps the **org** mark as its favicon
  and avatar. These project marks are for large contexts only.
- Per-family accent colours — explored (a "Heritage" palette: terracotta /
  slate / plum / teal) and **deliberately dropped**; three colours read as busy
  against the green+gold frame. See
  `planning/decisions/2026-06-29-project-marks-single-gold-inner.md`.
- Redesigning the org mark, header logo, or wordmark — unchanged.
- Separate marks for the two project templates — they reuse the org chevron mark.
- The horizontal name lockup typography is specified at a high level only; exact
  kerning/wordmark rendering is an implementation detail for `plan.md`.

## Design

### 1. The constant frame

The two interlocked pinwheel "snakes" from the org mark, drawn parametrically on
a 100×100 viewBox with the snakes pushed to the edges so a large inner symbol
gets clearance:

- **Geometry:** `margin = 9`, arm length `Lx = Ly = 53`, stroke `s = 11`.
  Snake 1 (top-left corner) `struct` colour; snake 2 (bottom-right) `accent`
  colour — same pinwheel construction as `geometry.py::_icon_mark`, but
  parameterised by `(W, H, margin, Lx, Ly, stroke)` so the corners can be moved
  and the canvas can be non-square if ever needed.
- **Colours (from `brand/build/tokens.py`):** `struct = GREEN_INK #356852`,
  `accent = GOLD_LIGHT #c98a00`. The frame is identical on every mark.
- **Heads & tails:** square block-head at each arm's outer end; diagonal-cut
  tail at the inner end — carried over from the org mark.

This frame is a new function alongside the existing `icon()`/`mark()`; it does
not replace them. The org favicon/avatar keep the original tighter geometry.

### 2. The inner symbol

One gold symbol, centred at (50,50), nominal radius **r ≈ 23**, in
`GOLD_LIGHT #c98a00` with `CREAM #f4f1e8` for negative space / cut-outs (e.g. the
bolt inside a filled disc). Two-colour total (green + gold); no third hue.

Filled "disc" marks (a gold disc with a cream symbol knocked out) are used where
the partner's own logo is a filled badge; line/figure marks are used elsewhere.
Every symbol is **redrawn in our geometry** — we evoke a partner, we do not paste
their logo (see Risk for the one exception).

### 3. The per-repo symbols (17 repos, 4 families)

**Dependency injection** (7):
| Repo | Inner symbol |
|------|--------------|
| `modern-di` | **dashed** dependency graph (3 nodes, dashed edges = "auto-wired by annotations") |
| `that-depends` | **solid** dependency graph (same 3 nodes, solid edges = the explicit predecessor) |
| `modern-di-fastapi` | lightning **bolt knocked out of a gold disc** (evokes FastAPI's teal disc+bolt) |
| `modern-di-litestar` | 5-point **star knocked out of a gold disc** (evokes Litestar's star) |
| `modern-di-faststream` | the **FastStream delta/stream** shape, recoloured gold |
| `modern-di-typer` | terminal window showing **`T>`** prompt (evokes Typer) |
| `modern-di-pytest` | **stepped bars** hanging from a crossbar, gold tints (evokes pytest's bar emblem) |

**Templates** (2) — reuse the **org chevron mark** (no bespoke symbol):
`fastapi-sqlalchemy-template`, `litestar-sqlalchemy-template`.

**Microservices, HTTP & messaging** (5):
| Repo | Inner symbol |
|------|--------------|
| `lite-bootstrap` | **rocket** (launch / bootstrap) |
| `httpware` | two interlocked **chain links** (middleware chain) |
| `faststream-redis-timers` | **stopwatch** (distributed timers) |
| `faststream-concurrent-aiokafka` | three **parallel lane arrows**, middle longest (staggered, concurrency) |
| `faststream-outbox` | **database cylinder publishing broadcast arcs** (DB emits events; transactional outbox) |

**Utilities** (3):
| Repo | Inner symbol |
|------|--------------|
| `db-retry` | database **cylinder inside a two-head clockwise retry circle** |
| `eof-fixer` | **document with a newline-return (↵)** arrow |
| `semvertag` | a **price/version tag** with punch-hole |

The three `faststream-*` messaging repos use their own concept symbols (timer /
lanes / outbox), *not* the FastStream delta — only the DI integration
`modern-di-faststream` co-brands with FastStream, per the "evoke the integrated
partner" rule that applies to the `modern-di-*` family.

### 4. Build pipeline & outputs

- Add symbol/frame functions to `brand/build/geometry.py` (parametric
  `project_frame(...)` + one function per inner symbol). Reuse
  `tokens.py` colours and `text.py` outlining for any text glyphs (`T>`).
- `brand/build/render.py` gains a pass that, for each repo in a manifest
  (repo → symbol), writes `brand/projects/<repo>/mark.svg` and rasterises
  `mark-<size>.png` (sizes TBD in plan; large-format, e.g. 512/1024) via the
  existing `export_png` (`rsvg-convert`).
- A **horizontal lockup** (`lockup.svg`: the framed mark + the repo name set in
  Jost, green/gold) is produced per repo for README banners. Name typography
  reuses `text.py::outline_text`.
- `brand/README.md` table of "Deferred" items is updated to mark the per-project
  system as shipped, and a short generation note is added.

### 5. Prototype (validated)

The full system was prototyped as standalone SVG generators and rendered with
`rsvg-convert` to verify every mark visually (centering checked against a
crosshair for `faststream-outbox` and `semvertag`; the `db-retry` circular-arrow
arrowheads were corrected to lead the arc with a butt cap). The implementation
ports that validated geometry into `brand/build/`.

## Operations

None out-of-repo for generation. Rolling each mark out to its repo's docs
site / README (copying `mark.svg` into each downstream repo, wiring MkDocs
`theme.logo`) is **per-repo follow-up work**, tracked separately — this change
produces the assets in this repo only.

## Out of scope

- Wiring the marks into each downstream repo's site/README (follow-up per repo).
- PNG size matrix and any `@2x` social-card variants per project.
- Animations or dark-mode inversions of the project marks.

## Testing

- `uv run python -m brand.build.render` produces a `mark.svg` (+ PNGs) for every
  manifest repo with no errors; `brand/projects/<repo>/` is populated.
- A contact-sheet render (all marks on one sheet) is eyeballed for consistency
  and centering — the prototype workflow, retained as a dev check.
- SVGs are well-formed (parse) and use only `tokens.py` colours (a small test
  asserting no stray hex values outside the token set is feasible).
- `just check-planning` passes; `architecture/` updated (see below).

## Risk

- **Trademark / partner-logo use (most likely concern).** `modern-di-faststream`
  uses the *actual* FastStream delta path recoloured; the fastapi/litestar/typer/
  pytest cues are redrawn evocations, not copies. Likelihood medium, impact low
  (these are clearly our snake-frame marks indicating an integration, fair-use
  nominative). *Mitigation:* keep the FastStream path as the only literal partner
  asset, recoloured into our palette; reconsider if any project objects.
- **Symbol legibility / taste.** Some glyphs (rocket, outbox arcs) are detailed;
  at large format this is fine but a few may need a second pass. *Mitigation:*
  the generator makes iteration cheap; review the contact sheet before shipping.
- **Architecture doc drift.** This adds a capability; `architecture/` must gain a
  `brand-marks.md` (or extend `site-branding.md`) in the implementing PR per the
  planning convention.

# modern-python logo system — design

**Date:** 2026-06-27
**Status:** design approved (visual exploration done via the brainstorming companion); pending spec review.
**Scope:** Establish a reusable org + project logo system and produce full kits for the org mark plus 3 exemplar projects. The remaining ~14 repos follow the documented rules in a later pass.

## 1. Goal

Give the `modern-python` org a distinctive, ownable identity and a system that gives every repo its own mark while staying visibly one family. Output is a **full kit** (icon, horizontal + stacked lockups, social card, favicon) for the org and 3 exemplars, plus written rules so any repo can be generated later.

The system replaces the current corner-bracket org mark (`docs/assets/modern-python*.svg`).

## 2. Brand foundation (unchanged)

- **Primary green** `#356852` (light). **Gold accent** `#c98a00` (light).
- **Dark mode:** green lifts to `#3f8064`, gold brightens to `#e0a300`.
- Marks are hand-authored SVG on a `0 0 100 100` viewBox, stroke-based, `stroke-linecap`/`linejoin` round, role="img" + aria-label.

## 3. The org mark (parent)

Two nested, lightly-squared "snakes" (rounded-square open loops with a head) woven concentrically around a small core. Reads as: Python (two snakes, echoing the python.org interlock without copying it), a container/scope, and a dependency at the core.

**Geometry (viewBox `0 0 100 100`), all strokes width 8, round caps/joins:**

- **Outer snake** (green `#356852`):
  - path: `M20 35 L20 65 Q20 80 35 80 L65 80 Q80 80 80 65 L80 35 Q80 20 65 20 L35 20`
  - head: filled circle `cx=35 cy=20 r=5.5` (same color), at the open top-left corner.
- **Middle snake** (gold `#c98a00`), concentric, head at the opposite (bottom-right) corner:
  - path: `M65 57 L65 43 Q65 35 57 35 L43 35 Q35 35 35 43 L35 57 Q35 65 43 65 L57 65`
  - head: filled circle `cx=65 cy=57 r=5.5` (same color).
- **Core** (green `#356852`): filled circle `cx=50 cy=50 r=5`.

Both snakes share the stroke weight (8) so the three concentric bands read as a harmonic set. Even radial spacing (outer band ≈ r30, middle ≈ r15, core ≈ r0).

**Dark mode:** outer + core → `#3f8064`, middle → `#e0a300`. Implement as a single SVG that adapts via an embedded `<style>` with `@media (prefers-color-scheme: dark)` (same technique as the existing `modern-python-mark.svg`).

**Favicon (≤24px):** at 16–24px the three bands merge. Ship a simplified favicon variant — outer snake + core only (drop the middle snake), or a 2-band reduction — as a separate asset. Decision recorded in the plan.

## 4. The wordmark / lockups

Recommended default (flagged for confirmation in §8): **monospace** wordmark to match the code/terminal theme and the project monograms.

- **Primary (horizontal):** icon + `modern-python` set in JetBrains Mono, reading like a command line.
- **Secondary (stacked):** icon above two-line `Modern / Python` (or spaced caps) for square/social/avatar contexts.
- Lockup rules (from research): clear space = one icon-height around the whole lockup; wordmark optically balanced to the icon height; type weight harmonized to stroke weight; shared baseline/center. Icon must work standalone (it does).
- Final wordmark text is converted to outlined paths (font-independent).

## 5. The project-mark system

One shared **foundation** with a single controlled **variable** per project (the industry pattern: Adobe CC / JetBrains / Material).

### 5.1 Construction (constant for every project)

- **Frame:** the single outer snake (the org mark's outer snake), stroke 8, head top-left. This is the family signature.
- **Inner content:** a 2-letter monogram OR a glyph, optically centered. Monogram is **JetBrains Mono bold**, lowercase, centered with a slight optical lift (≈ `y=48.5` on the 100 viewBox, `dominant-baseline=central`, `text-anchor=middle`); size ~30 for narrow pairs, ~26 for wide pairs. Converted to outlined paths in final art.
- Same grid, stroke weight, corner radius, and round caps as the org mark.

### 5.2 The variable, by category

| Group | Frame color | Inner content | Inner color |
|---|---|---|---|
| **DI core** (`modern-di`, `that-depends`) | green `#356852` | monogram (`di`, `td`) | gold `#c98a00` |
| **modern-di integrations** (`-fastapi`, `-litestar`, `-faststream`, `-typer`, `-pytest`) | green `#356852` | monogram (`fa`, `ls`, `fs`, `ty`, `pt`) | **framework color** |
| **Templates** (`fastapi-sqlalchemy-template`, `litestar-sqlalchemy-template`) | green `#356852` | **stack glyph** (3 stacked rounded bars) | **framework color** |
| **Microservices / HTTP / messaging** (`httpware`, `lite-bootstrap`, `faststream-outbox`, `faststream-redis-timers`, `faststream-concurrent-aiokafka`) | teal `#2a9d8f` | monogram | gold `#c98a00` |
| **Utilities** (`db-retry`, `eof-fixer`, `semvertag`) | amber `#c2722b` | monogram | gold `#c98a00` |

**Why this resolves the integration-vs-template clash:** `modern-di-fastapi` and `fastapi-sqlalchemy-template` share the FastAPI color but differ by device — integration = framework-colored **letters** (`fa`); template = framework-colored **stack glyph**. Same family, clearly different role.

**Stack glyph** (template marker), centered in the frame, filled in the framework color:
`rect x=37 y=39 w=26 h=6 rx=3` · `rect x=37 y=48 w=26 h=6 rx=3` · `rect x=37 y=57 w=26 h=6 rx=3`.

### 5.3 Framework colors (PLACEHOLDERS — verify before shipping)

Approximate, must be confirmed against each project's actual brand:
FastAPI `#009688`, Litestar `#5b8def`, FastStream `#c2569b`, Typer `#1f9ed1`, pytest `#3aae6b`.
(See §8 — do not ship until each is verified against the upstream brand.)

### 5.4 Monogram assignments (initial)

`di`, `td`, `fa`, `ls`, `fs`, `ty`, `pt`, `hw`, `lb`, `fo`, `db`, `ef`, `sv`. Collisions across categories are acceptable because the frame color differs; revisit any within-category collision when rolling out the full set.

## 6. Deliverables

### 6.1 Exemplars to produce now (exercise every rule)

1. **Org mark** — full nested-snakes mark.
2. **`modern-di`** — DI core, gold `di` monogram, green frame.
3. **`modern-di-fastapi`** — integration, FastAPI-colored `fa`, green frame.
4. **`fastapi-sqlalchemy-template`** — template, FastAPI-colored stack glyph, green frame.

### 6.2 Per mark, produce

- Icon SVG (single file, light/dark via `prefers-color-scheme`).
- Horizontal lockup (icon + monospace wordmark).
- Stacked lockup.
- Simplified favicon (16/24px).
- Social-preview card (1280×640) — centered stacked lockup on brand background.

### 6.3 Storage

Canonical source lives in this repo (the org-site repo). Proposed: `brand/` at the repo root with one folder per mark and a shared `tokens` reference; the org-site favicon/logo in `docs/assets/` is regenerated from it. Per-repo usage: each repo's `README.md` header gets its horizontal lockup; repos with a docs site get the favicon. Exact path confirmed in the plan.

## 7. Conventions to honor

- Keep the three metadata surfaces consistent (GitHub description, pyproject `description`, `profile/README.md`) — unaffected by logos but adjacent.
- SVGs: `role="img"`, `aria-label`, no raster fallback needed.
- Brand casing in any text: `modern-di`, `that-depends`, `Litestar`, `FastStream`, `FastAPI`, `Typer`.

## 8. Open decisions (please rule during spec review)

1. **Wordmark typeface/lockup** — adopt the monospace command-line default (§4), or prefer a geometric sans / the existing wordmark? (Earlier companion options L1 vs L3 vs L5.)
2. **Framework hex values** (§5.3) — confirm sourcing: pull each from the upstream project's brand, or pick our own harmonized set?
3. **Storage location** (§6.3) — `brand/` at repo root vs `docs/assets/brand/`.
4. **Favicon reduction** — outer+core only, or a 2-band version?
5. **Rollout** — produce all 17 now, or the 4 exemplars first then the rest in a follow-up (current scope assumes the latter).

## 9. Explicitly out of scope

- Rebranding the docs-site theme colors (palette is unchanged).
- Animation / motion versions.
- Producing all 17 marks in this pass (only the 4 exemplars).

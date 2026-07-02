---
summary: Add modern-di-starlette to the org brand kit (sparkle-cluster mark) and list it on the profile README, docs site, and its GitHub repo settings.
---

# Design: Onboard modern-di-starlette into the org brand and surfaces

## Summary

`modern-di-starlette` is a new DI integration. Its repo already ships a README
that references central brand assets under
`brand/projects/modern-di-starlette/` — assets that do not exist yet, so those
image links are currently broken. This change mints the project's mark (a
four-point **sparkle cluster**), regenerates its brand assets, adds it to the
`profile/README.md` DI table and the `docs/index.md` DI list, and brings its
GitHub repo metadata (description, topics, website) in line with org
conventions. All code changes live in this repo (`.github`); the integration
repo itself is already complete.

## Motivation

The `modern-di-starlette` README (in its own repo) points at
`https://raw.githubusercontent.com/modern-python/.github/main/brand/projects/modern-di-starlette/lockup-{light,dark}.svg`
and `lockup.png`. None of those files exist, so the README renders with a broken
image. Every sibling integration (`modern-di-fastapi`, `modern-di-litestar`,
`modern-di-faststream`, `modern-di-typer`, `modern-di-pytest`) has a mark, a
profile-README row, and a docs-site entry; Starlette must match to keep the
three metadata surfaces (GitHub description, pyproject `description`, profile
blurb) consistent.

## Non-goals

- No changes to the `modern-di-starlette` repo contents (README, CI, planning,
  architecture already present and correct).
- No social card: integrations are not in `DOCS_REPOS`, matching the other
  `modern-di-*` integrations, which have no per-project docs site.
- No new symbol vocabulary beyond the one Starlette mark.

## Design

### 1. Sparkle-cluster symbol — `brand/build/symbols.py`

Add a `sparkle_cluster(cx, cy, r)` function: a large four-point sparkle with a
small secondary sparkle at upper-right, both filled in `GOLD` (no disc). The
four-point sparkle is a concave 8-vertex polygon (outer points at N/E/S/W,
inner points at the 45-degree diagonals). Uses only `GOLD`, so it satisfies the
`test_only_allowed_colours` palette check. It follows the same contract as the
existing `star_disc` / `bolt_disc` (takes `cx, cy, r`, returns bare SVG markup).

The exact geometry is the approved candidate B, verified in the visual
companion: large sparkle centred slightly down-left, `r*0.82`, `inner=0.34`;
small sparkle up-right, `r*0.36`. The `project_lockup` dark-mode path already
swaps `GOLD_LIGHT` -> `GOLD_DARK` globally, so the dark lockup needs no special
handling.

### 2. Manifest entry — `brand/build/projects.py`

Add `"modern-di-starlette": lambda: sym.sparkle_cluster(_CX, _CY, R)` to
`MANIFEST`, in the dependency-injection block, immediately after
`modern-di-litestar` (keeps the web-framework integrations fastapi -> litestar ->
starlette adjacent).

### 3. Test — `tests/test_projects.py`

Add `"modern-di-starlette"` to `EXPECTED_REPOS`. That set is asserted equal to
`MANIFEST`, and the valid-SVG / allowed-colours / render tests are parametrized
off it, so no other test edits are required. `DOCS_EXPECTED` is unchanged
(Starlette gets no social card).

### 4. Regenerate assets — `just sync-assets`

Runs `python -m brand.build.render`, producing
`brand/projects/modern-di-starlette/{mark.svg, mark-512.png, mark-1024.png,
lockup-light.svg, lockup-dark.svg, lockup.png}`. Commit the generated files.
This resolves the integration repo's broken README image links.

### 5. Profile README — `profile/README.md`

Add one row to the **Dependency injection** table, immediately after the
`modern-di-litestar` row, blurb `modern-di integration for Starlette`, carrying
the same badge set as its siblings (Stars, PyPI, Downloads, Context7).

### 6. Docs site — `docs/index.md`

Add one bullet to the `Dependency injection { #di }` list after the Litestar
line: `` `modern-di-starlette` — `modern-di` integration for Starlette.`` Also
extend the "The stack" sentence to read "...shared across FastAPI, Starlette,
Litestar, FastStream, and Typer" so the narrative names the new integration.

## Operations

GitHub repo settings for `modern-python/modern-di-starlette`, set via `gh` to
match org conventions:

- **Description:** `modern-di integration for Starlette` (the canonical
  one-liner, matching pyproject and the profile blurb).
- **Website:** `https://modern-di.modern-python.org` (integrations have no own
  docs site; they point at the modern-di docs).
- **Topics:** the `modern-di-*` integration base set plus the framework —
  `python, dependency-injection, di, ioc-container, modern-di, starlette`.

These are verified against the live repo before/after: read current values,
compare to the intended set, apply only the diff.

## Testing

- `just test` green, in particular `tests/test_projects.py`:
  `test_manifest_covers_every_repo` (MANIFEST == EXPECTED_REPOS),
  `test_only_allowed_colours`, `test_project_mark_is_valid_svg`, and the
  render tests.
- Visually inspect the regenerated `mark.svg` and `lockup-light/dark.svg` /
  `lockup.png` for the Starlette entry.
- Confirm the integration repo's README image links now resolve to real files
  at the referenced paths.
- `just check-planning` passes before pushing.
- `gh repo view modern-python/modern-di-starlette` reflects the intended
  description, homepage, and topics.

## Risk

- **Low: mark reads too close to Litestar.** Mitigated — the sparkle cluster is
  four-point and disc-less, visibly distinct from Litestar's 5-point star-in-
  disc; confirmed against the sibling marks in the visual companion.
- **Low: stray colour fails the palette test.** Mitigated — the symbol uses only
  `GOLD`; `test_only_allowed_colours` is the guardrail.
- **Low: GitHub settings drift from pyproject/profile.** Mitigated — all three
  use the single canonical one-liner `modern-di integration for Starlette`.

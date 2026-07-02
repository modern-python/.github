---
summary: Mint the modern-di-aiohttp brand mark (async event-loop in a gold disc) and generate its assets; public surfaces deferred until the repo ships.
---

# Design: modern-di-aiohttp brand mark

## Summary

`modern-di-aiohttp` is a new DI integration, still in development — its GitHub
repo is not public and the package is not on PyPI yet. This change mints its
brand mark (an **async event-loop cycle knocked out of a gold disc**) and
generates the six per-project asset files in this repo (`.github`), so they are
ready when the repo goes public. The public-facing surfaces (profile README row,
docs-site bullet, GitHub repo settings) are deliberately **deferred** — they
show PyPI/Downloads badges and link to a public repo that does not exist yet.

## Motivation

Every mainstream web-framework integration in the org has a brand mark
(`modern-di-fastapi` bolt-in-disc, `modern-di-litestar` star-in-disc,
`modern-di-starlette` sparkle). Preparing aiohttp's mark now means the asset
URLs resolve the moment its repo publishes its README, with no scramble.

We reviewed aiohttp's real logo (a node/network graph inside a ring). We
deliberately did **not** adapt it: the node-graph motif is already how
`modern-di` and `that-depends` read in this same lineup, so a faithful copy
would collide. The chosen mark keeps the async meaning and joins the
disc-family (FastAPI/Litestar), which is visually distinct from the DI
graph marks.

## Non-goals

- No changes to the (not-yet-public) `modern-di-aiohttp` repo.
- **No** profile README row, docs-site bullet, or GitHub repo settings — these
  wait until the repo is public (tracked under "Deferred follow-ups" below).
- No social card: integrations are not in `DOCS_REPOS`.

## Design

### 1. Async-loop symbol — `brand/build/symbols.py`

Add `async_loop(cx, cy, r)`: two cream arrows chasing each other in a circular
loop (the universal "async / event-loop" cycle), knocked out of a gold disc.
It reuses the existing `_circ_arc` arc-with-arrowhead helper.

`_circ_arc` currently hardcodes `GOLD` for both its stroke and its arrowhead
fill. Extend its signature with a trailing optional `color: str = GOLD` and
substitute `{color}` for the two `{GOLD}` occurrences. This is backward
compatible — the only existing caller (`db_retry`) omits the argument and keeps
`GOLD`.

```python
def _circ_arc(cx: float, cy: float, rad: float, a0: float, a1: float, w: float,
              color: str = GOLD) -> str:
    ...  # stroke and arrowhead now use {color} instead of {GOLD}


def async_loop(cx: float, cy: float, r: float) -> str:
    """aiohttp cue: an async event-loop cycle (two chasing arrows) knocked out
    of a gold disc."""
    rad = r * 0.52
    w = 3.4
    loop = (
        _circ_arc(cx, cy, rad, 25, 165, w, color=CREAM)
        + _circ_arc(cx, cy, rad, 205, 345, w, color=CREAM)
    )
    return f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="{GOLD}"/>' + loop
```

`CREAM` is already imported in `symbols.py`. The mark uses only `GOLD` and
`CREAM`, both in the allowed palette, so `test_only_allowed_colours` passes.

### 2. Manifest entry — `brand/build/projects.py`

Add `"modern-di-aiohttp": lambda: sym.async_loop(_CX, _CY, R)` to `MANIFEST`,
in the dependency-injection block, immediately after `modern-di-starlette`
(keeps the web-framework integrations fastapi -> litestar -> starlette ->
aiohttp adjacent).

### 3. Test — `tests/test_projects.py`

Add `"modern-di-aiohttp"` to `EXPECTED_REPOS`. That set is asserted equal to
`MANIFEST`, and the valid-SVG / allowed-colours / render tests are parametrized
off it, so no other test edits are required. `DOCS_EXPECTED` is unchanged.

### 4. Regenerate assets — `just sync-assets`

Produces `brand/projects/modern-di-aiohttp/{mark.svg, mark-512.png,
mark-1024.png, lockup-light.svg, lockup-dark.svg, lockup.png}`. Commit the
generated files.

## Deferred follow-ups (when the repo is public)

Ship these in a later change once `github.com/modern-python/modern-di-aiohttp`
exists and the package is on PyPI:

- Profile README row in the Dependency injection table.
- Docs-site bullet in the DI list (+ mention in the stack sentence).
- GitHub repo settings: description `modern-di integration for aiohttp`,
  homepage `https://modern-di.modern-python.org`, topics
  `python, dependency-injection, di, ioc-container, modern-di, aiohttp`.

The canonical one-liner for all of the above will be
`modern-di integration for aiohttp`.

## Testing

- `just test` green, in particular `tests/test_projects.py`:
  `test_manifest_covers_every_repo`, `test_only_allowed_colours`,
  `test_project_mark_is_valid_svg`, and the render tests.
- Visually inspect the regenerated `mark.svg` and light/dark lockups for the
  aiohttp entry.
- `just sync-assets` re-run is a no-op diff apart from the six new files
  (deterministic render).
- `just check-planning` passes before pushing.

## Risk

- **Low: async_loop reads too close to db-retry's retry arcs** (both are
  arced arrows). Mitigated — db-retry is a single retry arc around a database
  cylinder; async_loop is two symmetric arrows forming a closed cycle on a
  plain disc. Different enough; confirmed against the rendered marks.
- **Low: extending `_circ_arc` breaks db-retry.** Mitigated — the new param is
  optional and defaults to `GOLD`; the existing call is unchanged and the
  palette test covers db-retry.

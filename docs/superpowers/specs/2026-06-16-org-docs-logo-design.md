# Org logo + brand alignment across project docs

**Date**: 2026-06-16
**Status**: approved
**Scope**: 7 modern-python org documentation sites

## Context

The org docs site (modern-python.org, built from the `.github` repo) shows the
"Modern Python" white wordmark in the top-left corner, the org mark as favicon,
and a forest-green brand palette. Individual project docs sites use the Material
theme but configure **no logo** and a generic `primary: black, accent: pink`
palette, so they read as unrelated sites. The goal is to make every org project's
docs visibly part of one family by adopting the org logo, favicon, and palette.

OG social cards are explicitly **out of scope** for this change (deferred to a
separate follow-up) because they require per-repo `overrides/` templates, a card
image, and a `site_url` that one target repo currently lacks.

## Source assets

From `.github/docs/assets/`:

- `modern-python-white.svg` (white wordmark, 2.5K) → top-left corner logo
- `modern-python-mark.svg` (mark icon, 372B) → favicon

The white wordmark is correct because Material colors the top app bar with the
primary color; with `primary: custom` (green) the white logo sits on a green
header, exactly matching the org site.

## Target repos (7)

All checked-out org projects with a Material docs site:

`modern-di`, `faststream-outbox`, `that-depends`, `autosemver`, `httpware`,
`lite-bootstrap`, `faststream-redis-timers`.

All use `docs_dir: docs`. None currently configure a logo or favicon. This change
intentionally applies the "Modern Python" org wordmark to independently-named libs
(`that-depends`, `autosemver`, `httpware`) as well — confirmed desired ("all 7").

## Per-repo changes (identical pattern)

### 1. Copy assets

Copy both SVGs into the repo:

- `docs/assets/modern-python-white.svg`
- `docs/assets/modern-python-mark.svg`

(Self-contained — committed per repo, no cross-repo runtime dependency.)

### 2. `mkdocs.yml` `theme:` block

Add the logo and favicon keys:

```yaml
theme:
  name: material
  logo: assets/modern-python-white.svg
  favicon: assets/modern-python-mark.svg
  ...
```

Change **both** palette entries (light and dark scheme):

- `primary: black` → `primary: custom`
- `accent: pink` → `accent: custom`

### 3. Brand palette CSS

Add `docs/css/brand.css` containing only the palette custom properties ported from
the org's `docs/stylesheets/extra.css` (the `:root` + `slate` color vars — **not**
the org homepage-specific `.mp-hero` / `.grid.cards` rules):

```css
/* Brand palette — forest green sampled from the org logo (#356852) */
:root > * {
  --md-primary-fg-color:        #356852;
  --md-primary-fg-color--light: #4a8a6e;
  --md-primary-fg-color--dark:  #234738;
  --md-accent-fg-color:         #c98a00;
}

[data-md-color-scheme="slate"] {
  --md-primary-fg-color:        #356852;
  --md-primary-fg-color--light: #4a8a6e;
  --md-primary-fg-color--dark:  #234738;
  --md-accent-fg-color:         #e0a300;
  /* Lighter green for body links so they stay AA-readable on the dark bg */
  --md-typeset-a-color:         #7fb79f;
}
```

Reference it in `extra_css`. Two repo states:

- **Has `extra_css` already** (`modern-di`, `faststream-outbox`, `that-depends`,
  `lite-bootstrap`, `faststream-redis-timers`, each with `- css/code.css`): append
  `- css/brand.css`.
- **No `extra_css` / no `docs/css/`** (`autosemver`, `httpware`): create
  `docs/css/`, add the new `extra_css:` key with `- css/brand.css`.

`that-depends` keeps its existing `custom_dir: docs/overrides` untouched.

## Verification

For each repo, build the docs and spot-check the rendered output:

```bash
uv run mkdocs build --strict   # or the repo's documented build command
```

Confirm in the rendered `site/`:

- white wordmark logo in the top-left corner
- favicon present (mark icon)
- green header / green primary palette in both light and dark schemes

At minimum, confirm `modern-di` renders correctly end-to-end before declaring done;
build all 7 to catch `--strict` failures (e.g. a missing asset path).

## Out of scope

- OG social cards (`overrides/main.html` + `social-card.png` + `site_url`
  backfill for `faststream-redis-timers`) — separate follow-up.
- Org repos not checked out locally (templates, integration repos without their
  own docs site) — the pattern above transfers directly if/when needed.

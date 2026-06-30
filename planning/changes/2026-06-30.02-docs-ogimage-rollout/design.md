---
summary: Wire each of the 7 docs-site repos to serve its social card as og:image, via a Material template override + self-hosted card.
---

# Design: docs-site og:image rollout

## Summary

Make each of the seven `modern-python` docs sites emit a proper
`og:image`/`twitter:image` pointing at its own social card, so link unfurls on
GitHub/Slack/X/etc. show the branded card instead of nothing. Each docs repo
self-hosts its card (`docs/assets/social-card.png`, copied from this repo's
`brand/projects/<repo>/social-card.png`) and gains a small MkDocs Material
template override that emits the Open Graph + Twitter meta. Shipped as **seven
PRs**, one per docs repo. This planning bundle lives in `.github` (the org/brand
home where the cards are generated); no code changes land in `.github`.

## Motivation

The cards shipped in `brand/projects/<repo>/social-card.png` (PR #23) but nothing
consumes them yet — the docs sites have no `og:image`, so shared links are bare.
Probing confirmed all 7 sites are live MkDocs Material with their subdomain
`site_url` set, none use Material's `social` plugin (no auto-card to conflict
with), and only `that-depends` has a `custom_dir` (`docs/overrides`).

The 7 docs repos: `modern-di`, `that-depends`, `lite-bootstrap`, `httpware`,
`faststream-redis-timers`, `faststream-outbox`, `semvertag`.

## Non-goals

- README logos — a separate, later spec (this is the og:image piece only).
- Cards for non-docs repos — they have no docs site.
- Auto-generating cards with Material's `social` plugin — we use the bespoke
  cards already generated in this repo.
- Changing the card design or this repo's own og:image.

## Design

### 1. Per-repo change set (identical shape across all 7)

Each docs repo PR adds:

1. **`docs/assets/social-card.png`** — the repo's card, copied verbatim from
   `modern-python/.github`'s `brand/projects/<repo>/social-card.png` (current
   `main`).
2. **`overrides/main.html`** — a Material override (template below). For
   `that-depends`, this goes in its existing `docs/overrides/` instead of a new
   `overrides/`.
3. **`mkdocs.yml`** — add `theme.custom_dir: overrides` for the six repos that
   lack it. `that-depends` already sets `custom_dir: docs/overrides` — no change.

### 2. The override template

One file, identical for every repo (it reads values from `mkdocs.yml`, so nothing
is hard-coded per repo):

```jinja
{% extends "base.html" %}
{% block extrahead %}
  {{ super() }}
  {% set base = config.site_url if config.site_url.endswith('/') else config.site_url ~ '/' %}
  {% set card = base ~ 'assets/social-card.png' %}
  {% set title = (page.title ~ ' · ' ~ config.site_name) if (page.title and not page.is_homepage) else config.site_name %}
  {% set description = page.meta.description if page.meta and page.meta.description else config.site_description %}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{{ config.site_name }}">
  <meta property="og:title" content="{{ title }}">
  <meta property="og:description" content="{{ description }}">
  <meta property="og:url" content="{{ page.canonical_url }}">
  <meta property="og:image" content="{{ card }}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1280">
  <meta property="og:image:height" content="640">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{{ title }}">
  <meta name="twitter:description" content="{{ description }}">
  <meta name="twitter:image" content="{{ card }}">
{% endblock %}
```

**Trailing-slash guard is load-bearing:** these repos' `site_url` has no trailing
slash (e.g. `https://modern-di.modern-python.org`), unlike this repo's
(`https://modern-python.org/`); the `base` computation normalises it so the card
URL is `https://<repo>.modern-python.org/assets/social-card.png`, never
`…orgassets/…`.

It extends `base.html` and only appends to `extrahead` via `{{ super() }}`, so it
adds meta without overriding anything Material already renders.

### 3. Asset sourcing

The card is copied from this `.github` checkout:
`brand/projects/<repo>/social-card.png` → `<docs-repo>/docs/assets/social-card.png`.
It is committed into the docs repo (self-hosted), so the docs site serves it
same-origin and there is no cross-repo runtime dependency. If a card is later
regenerated here, re-copy it into the repo (rare; noted as a maintenance step).

### 4. Execution: seven PRs

One PR per repo, done sequentially and verified before the next:
clone → branch → add card + override (+ `custom_dir` where missing) → verify
(below) → push → PR → watch CI. Branch name per repo: `docs-ogimage`.
`that-depends` is the one special case (existing `docs/overrides/`,
`custom_dir` already set).

## Operations

After each PR merges and the site redeploys, the card is live at
`https://<repo>.modern-python.org/assets/social-card.png`. Optionally validate the
unfurl with a debugger (e.g. opengraph.xyz) — manual, out of band.

## Out of scope

- README logos (separate spec).
- Any change to this `.github` repo's site or to the card design.

## Testing

Per repo, before opening the PR:

- Build the docs the way the repo builds them (e.g. `uv run mkdocs build` or the
  repo's documented command). The build must succeed.
- Assert the generated `site/index.html` contains
  `<meta property="og:image" content="https://<repo>.modern-python.org/assets/social-card.png">`
  and `site/assets/social-card.png` exists.
- Spot-check one interior page's built HTML carries the same `og:image`.

## Risk

- **Docs build needs Material + plugins installed.** Cloning a repo and running
  `mkdocs build` may require its docs dependencies. Likelihood medium, impact
  low. *Mitigation:* install via the repo's own dev/docs extra
  (`uv sync`/`uv run`), or `uvx --with mkdocs-material[imaging] mkdocs build`; if
  a repo's plugin set is heavy and unavailable, fall back to verifying the
  override is valid Jinja and the card file is present, and rely on the repo's CI
  to build.
- **`that-depends` already has a `main.html` in `docs/overrides/`.** Then it must
  be *merged* (append the `extrahead` block), not overwritten. *Mitigation:* the
  plan inspects `docs/overrides/` first and merges if a `main.html` exists.
- **Per-repo `mkdocs.yml` drift.** A repo might key the theme differently.
  *Mitigation:* the plan reads each `mkdocs.yml` before editing; the override
  template itself is config-driven and unaffected.
- **Card staleness.** The committed card can drift from a regenerated one in
  `.github`. Likelihood low (cards rarely change), impact low. *Mitigation:* the
  later README spec or a follow-up can document a re-copy step; out of scope here.

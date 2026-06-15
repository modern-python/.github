# modern-python.org — org homepage site

**Date:** 2026-06-15
**Status:** Approved design, ready for implementation plan

## Goal

Publish a GitHub Pages site at the custom apex domain **modern-python.org** for the
`modern-python` GitHub organization. The site is a single landing page that introduces
the org and lists its projects, built with a static site generator and structured so
additional pages can be added later without rework.

The site lives in this `.github` org-profile repo. The existing `profile/README.md`
(which renders the GitHub org profile) is **not** touched and continues to work as-is.

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Scope | Landing page + room to grow | One page now; structure allows adding pages (per-category, about) later. |
| Generator | MkDocs + Material | Python-native, the de-facto standard in the Python ecosystem; easiest for the org to maintain. |
| Deployment | GitHub Actions → Pages | Builds on push to `main`, deploys via `actions/deploy-pages`. No build artifacts committed. |
| Homepage layout | Layout C — minimal hub + topic tiles | Centered intro, topic tiles, then category sections. Leans into "room to grow". |
| Content sync | `profile/README.md` and `docs/index.md` kept independent | Both small; different audiences/formats. No generator to sync them. |
| Branding | Forest green `#356852`, org wordmark logo | From the provided `modern-python.png` logo. |

## Repository layout

```
.github/
├── profile/README.md            # UNCHANGED — GitHub org profile
├── README.md                    # existing root readme (unchanged)
├── mkdocs.yml                   # site config: theme, nav, palette, domain
├── pyproject.toml               # mkdocs + material deps, managed with uv
├── docs/
│   ├── index.md                 # the homepage (layout C)
│   ├── CNAME                     # "modern-python.org" — copied to site root on build
│   ├── assets/
│   │   ├── modern-python.png    # org logo (header logo + favicon source)
│   │   └── custom.css           # tile grid + green accents
│   └── superpowers/specs/       # design docs (this file)
├── .github/workflows/
│   └── deploy.yml               # build + deploy to Pages
└── .gitignore                   # + site/ , .superpowers/
```

Single source of truth for the project list is `docs/index.md`.

## Homepage structure (`docs/index.md`)

Rendered with Material for MkDocs. Sections top to bottom:

1. **Centered intro** — "Modern Python" heading + the tagline from the current README
   opening line ("Open-source templates and libraries for building production-ready
   Python applications…"), and the "built with uv, ruff, ty" note.
2. **Topic tiles** — a responsive grid of cards, one per category. In v1 each tile is an
   anchor link that jumps to its section lower on the same page (one page, no dead links).
   The same markup promotes cleanly to dedicated pages later — only the tile `href`
   changes. Categories:
   - Project templates
   - Dependency injection
   - Microservices, HTTP & messaging
   - Utilities
3. **Category sections** — one section per category, each listing its projects with the
   one-line description and a link to the GitHub repo. Content mirrors the current
   `profile/README.md` project list.

## Theme & branding

- **Theme:** `material` with features: light/dark mode toggle, navigation, built-in
  search, repo link + "edit" in the header.
- **Palette:** custom primary keyed to brand green `#356852` for both light and dark
  schemes (sampled from `modern-python.png`); a warm complementary accent for
  links/buttons. White text on green for the hero/header band.
- **Logo / favicon:** `docs/assets/modern-python.png` set as `theme.logo` and
  `theme.favicon` source. The hero/header background uses the same green so the wordmark
  (which has a solid green background, not transparent) blends seamlessly.
  - Future improvement (out of scope): a transparent-background or SVG variant of the
    logo for use on light surfaces.
- **`custom.css`:** styles the topic-tile grid and applies the green to section
  headings / card borders.

## Deployment (`.github/workflows/deploy.yml`)

- **Trigger:** push to `main` (plus `workflow_dispatch` for manual runs).
- **Build:** check out repo, set up `uv`, install MkDocs + Material from `pyproject.toml`,
  run `mkdocs build --strict` (strict mode fails the build on broken links / nav).
- **Deploy:** upload the built `site/` as a Pages artifact and publish via the official
  `actions/deploy-pages` action.
- **Permissions:** `pages: write`, `id-token: write`, `contents: read`.
- **Concurrency:** single in-flight Pages deployment.
- Pages source in repo settings must be set to **GitHub Actions** (manual, see below).

## Custom domain — modern-python.org

- `docs/CNAME` contains exactly `modern-python.org`, so it lands at the published site
  root every deploy and GitHub keeps the custom domain bound.
- Apex-domain caveat: only one Pages site per org can claim `modern-python.org`. This
  `.github` repo owns it; no other repo in the org should set the same custom domain.
- After DNS propagates, enable **Enforce HTTPS** in the repo's Pages settings.

## Manual steps (owner-only, cannot be automated here)

These require registrar access and the GitHub web UI:

1. **DNS at the domain registrar** for `modern-python.org`:
   - Apex `A` records → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`,
     `185.199.111.153`
   - Apex `AAAA` records → `2606:50c0:8000::153`, `2606:50c0:8001::153`,
     `2606:50c0:8002::153`, `2606:50c0:8003::153`
   - `www` `CNAME` → `modern-python.github.io`
2. **Repo → Settings → Pages:** set **Source = GitHub Actions**.
3. After the first successful deploy and DNS propagation: tick **Enforce HTTPS**.

## Out of scope (YAGNI)

- Per-category or "about" pages (structure supports them; not built now).
- Blog, docs aggregation across projects, search beyond Material's built-in.
- Automated sync between `profile/README.md` and `docs/index.md`.
- Transparent/SVG logo variant.

## Success criteria

- `mkdocs build --strict` succeeds locally and in CI.
- Pushing to `main` deploys the site via GitHub Actions with no committed build artifacts.
- Once DNS + Pages settings are configured by the owner, https://modern-python.org serves
  the green-branded homepage (layout C) with all project links resolving to the correct
  GitHub repos.
- `profile/README.md` and the GitHub org profile are unchanged.

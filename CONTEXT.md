# modern-python/.github

The org's shared repo: it generates the brand kit under `brand/`, builds the org
site at **modern-python.org** from `docs/` (MkDocs Material), and hosts the org
profile shown on the GitHub org page (`profile/README.md`) plus the community
health files every other repo inherits.

The conventions in [`AGENTS.md`](AGENTS.md) apply across **all** repos in the org,
not just this one.

## Language

A term is listed only when there is a synonym to reject, or a meaning subtle enough that code, the
profile, and the site must agree on it. General design vocabulary does not belong here, however
heavily this repo uses it.

**Mark**:
A square logo drawn from vector geometry, with no type. The *org mark* is the interlocked-snakes
pinwheel with a chevron; a *project mark* is the green+gold snake frame around one repo's inner
symbol.
_Avoid_: logo, icon

**Inner symbol**:
The gold shape inside a project mark's frame, one per repo, chosen in `projects.py::MANIFEST`. It
is the only thing that distinguishes one project mark from another.
_Avoid_: glyph, badge

**Wordmark**:
The `MODERN`/`PYTHON` crop-mark type, outlined to paths. Type only, no mark.
_Avoid_: logotype, title

**Lockup**:
A mark and a name composed into one fixed arrangement — the org wordmark, or a project's
mark-plus-repo-name banner.
_Avoid_: header, combo mark

**Colourway**:
One named ink pair an asset renders in: *light* is green-ink + gold-light, *dark* is cream +
gold-dark. Every asset ships both, and which one a surface loads is a `prefers-color-scheme` or
`data-md-color-scheme` swap, never a separate design.
_Avoid_: theme, variant, colour scheme

**Knockout**:
Cream painted **on top of** a gold shape to cut a hole in it. Cream is never ink in its own right:
on a transparent background it is invisible on light surfaces and stray white on dark ones.
_Avoid_: highlight, cutout

**Brand kit**:
The generated tree under `brand/` — the whole output of `brand.build.render`, and the source of
truth every other surface copies or hotlinks from.

**Social card**:
The 1280×640 `og:image` for a repo with a docs site: mark panel plus name, tagline, and URL.
_Avoid_: banner, preview image

**Org profile**:
`profile/README.md`, the landing page GitHub renders at github.com/modern-python. Distinct from the
**org site**, `modern-python.org`, built from `docs/`.

**The three metadata surfaces**:
A repo's one-liner, written once and kept identical in the GitHub description, the pyproject
`description`, and its org-profile row. Naming fewer than three of them is the usual way they drift.

# modern-python/.github

The org's shared repo: it generates the brand kit under `brand/`, builds the org
site at **modern-python.org** from `docs/` (MkDocs Material), and hosts the org
profile shown on the GitHub org page (`profile/README.md`) plus the community
health files every other repo inherits.

## Language

A term is listed only when there is a synonym to reject, or a meaning subtle enough that code, the
profile, and the site must agree on it. General design vocabulary does not belong here, however
heavily this repo uses it.

**Mark**:
A square logo drawn from vector geometry, with no type. The *org mark* is the interlocked-snakes
pinwheel with a chevron; a *project mark* is the green+gold snake frame around one repo's inner
symbol.
_Avoid_: logo — for our own assets. A third party's logo is a logo (`symbols.py` draws from
Flask's and FastStream's), and `icon` is the right word for a favicon or the `icon()` full-bleed
square.

**Inner symbol**:
The gold shape inside a project mark's frame, one per repo, chosen in `projects.py::MANIFEST`. It
is the only thing that distinguishes one project mark from another.
_Avoid_: glyph — which `text.py` needs for its real meaning, an outlined character from the font.

**Wordmark**:
The `MODERN`/`PYTHON` crop-mark type, outlined to paths. Type only, no mark.

**Lockup**:
A mark and a name composed into one fixed arrangement — the org wordmark, or a project's
mark-plus-repo-name banner. Named in the files themselves: `lockup-light.svg`, `lockup-dark.svg`.

**Colourway**:
One named ink pair an asset renders in: *light* is green-ink + gold-light, *dark* is cream +
gold-dark. Every asset ships both, and which one a surface loads is a `prefers-color-scheme` or
`data-md-color-scheme` swap, never a separate design.
_Avoid_: colorway — the repo has spelled it both ways; British spelling wins for this one word,
because the assets and the docs that describe them already read `colour`.

**Knockout**:
Cream painted **on top of** a gold shape to cut a hole in it. Cream is never ink in its own right:
on a transparent background it is invisible on light surfaces and stray white on dark ones.

**Org profile**:
`profile/README.md`, the landing page GitHub renders at github.com/modern-python. Distinct from the
**org site**, `modern-python.org`, built from `docs/` — the two carry different content and drift
apart if the names are used loosely.

**Owned channel**:
A community surface the org runs, moderates, and is accountable for. GitHub Discussions is the only
one today, per `docs/adr/0002-discussions-is-the-only-owned-channel.md`.
_Avoid_: channel, bare. On its own it reads as either kind, and both kinds are linked from the
profile and the site.

**Borrowed audience**:
A venue someone else runs, where the org participates as a guest and never moderates: the Python
Discord, the framework community channels, Stack Overflow, the newsletters.
_Avoid_: channel — a borrowed audience is never one of ours, and calling it one invites the
assumption that we moderate it.

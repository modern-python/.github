# modern-python/.github

[`CONTEXT.md`](CONTEXT.md) says what this repo is and owns the vocabulary — read it
before naming a mark, a colourway, or a surface.

## Naming & branding

- Brand/framework casing — use exactly: `modern-di`, `that-depends`, `Litestar`
  (not "LiteStar"), `FastStream`, `FastAPI`, `Typer`, `SQLAlchemy`, `PostgreSQL`.
- Per-project docs sites live at `<name>.modern-python.org` (only some repos have one).

## Repository metadata

A repo's description, topics, keywords, classifiers and `[project.urls]` follow
[section 11 of the standard](https://modern-python.org/standard/#11-metadata).

The org profile's `coverage 100%` badge is static and deliberately unlinked: there is no
org-level coverage URL to point at, and the gate in section 5 of the standard is what
makes the claim true.

A repo may be listed on the org profile **before** its package reaches PyPI. Its
Downloads badge 404s until pepy indexes it; the Stars badge and repo link resolve
meanwhile. That lag is self-healing — note it, never block the listing on it.

## Brand surfaces

A repo's brand assets are generated here, in `brand/projects/<repo>/`.

A docs site's `docs/index.md` replaces its `# <Title>` heading with a `.mp-hero` block
holding both lockup variants. Add no `title:` front matter there: Material titles the
home page from `site_name`, so `title:` renders as `<repo> - <repo>`.

## CI gotcha

GitHub occasionally type-checks a **stale `refs/pull/<n>/merge`** after a push, so a
PR can show an old lint/test failure that no longer matches the branch. Confirm by
running the failing check locally at the branch HEAD (with the pinned tool version);
if it's clean, push a fresh commit to force GitHub to recompute the merge ref.

## Agent skills

### Issue tracker

GitHub issues on `modern-python/.github`, via `gh`. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical roles, each label string equal to its name. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

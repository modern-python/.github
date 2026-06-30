---
summary: Add a centered light/dark logo banner to all 17 repo READMEs, served from .github; generate light/dark/png lockups in brand/build.
---

# Design: README logos

## Summary

Give every org repo (all 17) a centered brand banner at the top of its README:
the project's framed lockup (mark + name), theme-aware on GitHub (light/dark) and
rendering on PyPI. Two parts: **(1)** extend `brand/build` to emit three lockup
assets per repo — `lockup-light.svg`, `lockup-dark.svg`, `lockup.png` — committed
in `.github` under `brand/projects/<repo>/`; **(2)** a 17-repo rollout that
replaces each README's leading `# <name>` heading with a `<picture>` banner
pointing at those assets via absolute `raw.githubusercontent.com` URLs.

## Motivation

The brand kit shipped marks, social cards, and og:image, but the most-seen
surface — each repo's README (which, for every published package, is also the
PyPI `long_description`) — still opens with a bare `# <name>`. A logo banner
completes the rollout and gives the family a consistent first impression on both
GitHub and PyPI.

## Background: dual-surface rendering (researched)

- **GitHub** renders absolute `raw.githubusercontent.com/*.svg` URLs (served
  `image/svg+xml`) and supports light/dark via `<picture>` +
  `prefers-color-scheme`. SVGs are sandboxed (no JS/external refs) — fine for
  static logos.
- **PyPI** (`readme_renderer`) strips inline `<svg>` and `<source>`/`srcset`, so a
  `<picture>` collapses to its `<img>` fallback, which must be a **PNG at an
  absolute https URL** (relative paths don't resolve on PyPI). `<p align="center">`,
  `<img>`, `width`, `alt` are allowed.
- All sampled package repos set `readme = "README.md"`, so the banner must satisfy
  both surfaces. The `<picture>`+PNG-fallback pattern does.

## Non-goals

- The org **profile README** (`profile/README.md`) — it's the org landing page,
  not a per-repo banner target.
- A tagline under the logo (decided: replace the H1 with just the centered logo).
- Per-repo committed assets — assets live centrally in `.github` (decided),
  referenced by raw URL. No asset files added to the 17 repos.
- Any change to marks, social cards, or og:image.

## Design

### 1. Lockup assets in `brand/build` (`.github`)

`project_lockup` currently produces one light lockup. Generalize it to a colourway
and emit a dark sibling:

```python
def project_lockup(repo: str, *, dark: bool = False) -> str:
    """Framed mark + the repo name in Jost. Light = green-ink/gold on transparent
    (for light UIs); dark = cream/gold-dark on transparent (for dark UIs)."""
    struct = t.CREAM if dark else t.GREEN_INK
    accent = t.GOLD_DARK if dark else t.GOLD_LIGHT
    name_color = t.CREAM if dark else t.GREEN_INK
    mark_frame = g.project_frame(struct=struct, accent=accent)
    inner = MANIFEST[repo]()
    if dark:
        inner = inner.replace(t.GOLD_LIGHT, t.GOLD_DARK)  # inner gold reads on dark; cream negatives stay
    name_x = _LOCKUP_H + _GAP
    name_svg, name_w = outline_text(
        repo, _NAME_SIZE, x=name_x, baseline_y=_LOCKUP_H / 2 + _NAME_SIZE * 0.34,
        anchor="start", color=name_color,
    )
    total_w = round(name_x + name_w + _GAP)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {_LOCKUP_H}" '
        f'role="img" aria-label="{repo}"><g>{mark_frame}{inner}</g>{name_svg}</svg>'
    )
```

The dark colourway mirrors the org `wordmark-dark` and the on-green mark
colourway. The `inner.replace(GOLD_LIGHT, GOLD_DARK)` recolor is reliable because
the symbols emit exact token hex strings; `CREAM` negative-space stays cream
(visible on dark). (The `pytest` bar-tint literals aren't swapped — they're gold
shades that read fine on dark.)

`render_projects` writes, per repo, in place of today's single `lockup.svg`:
`lockup-light.svg` (= `project_lockup(repo)`), `lockup-dark.svg`
(= `project_lockup(repo, dark=True)`), and `lockup.png` — the **light** lockup
rasterized via the existing `export_png` (so it's auto-quantized; PyPI bg is
white, so the light lockup is the right fallback).

### 2. README banner (each of the 17 repos)

Replace the leading `# <repo>` line with:

```html
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)"  srcset="https://raw.githubusercontent.com/modern-python/.github/main/brand/projects/<repo>/lockup-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/modern-python/.github/main/brand/projects/<repo>/lockup-light.svg">
    <img alt="<repo>" src="https://raw.githubusercontent.com/modern-python/.github/main/brand/projects/<repo>/lockup.png" width="420">
  </picture>
</p>
```

Everything else in each README (the badges row, all content) is unchanged. The
`<repo>` placeholders are the repo name; `width="420"` is tunable.

### 3. Rollout & sequencing

1. **`.github` PR** — generate + commit the three lockups per repo. Must merge to
   `main` **first**, so the `…/main/…` raw URLs resolve.
2. **17 README PRs** — one per repo, README-only (no asset copies), replacing the
   H1 with the banner. Independent of each other; open after step 1 merges.

The 17 repos: modern-di, that-depends, modern-di-fastapi, modern-di-litestar,
modern-di-faststream, modern-di-typer, modern-di-pytest, fastapi-sqlalchemy-template,
litestar-sqlalchemy-template, lite-bootstrap, httpware, faststream-redis-timers,
faststream-concurrent-aiokafka, faststream-outbox, db-retry, eof-fixer, semvertag.
(`fastapi-sqlalchemy-template` uses `readme.md`, lowercase — handle per repo.)

## Operations

After step 1 merges, the assets are live at
`https://raw.githubusercontent.com/modern-python/.github/main/brand/projects/<repo>/lockup-*.{svg,png}`.
Each README PR renders its banner once both that PR and step 1 are on `main`.

## Out of scope

- profile README; taglines; per-repo asset hosting; non-README brand assets.

## Testing

**`.github` (`brand/build`):** render to a tmp dir and assert, for a sample repo,
that `lockup-light.svg`, `lockup-dark.svg`, `lockup.png` are written; the dark SVG
contains `CREAM`/`GOLD_DARK` and **not** `GREEN_INK`; the light SVG contains
`GREEN_INK`; both parse as XML; `lockup.png` opens mode `"P"` (quantized). Full
`pytest` + `just check-planning` green; `render` clean and deterministic (no PNG
churn).

**Per repo:** the README's first non-blank line is the `<p align="center">`
banner; there is no leading `# <repo>` heading; the three `srcset`/`src` URLs name
that repo and the correct asset filenames; the package still builds where
applicable (`uvx twine check` on a built sdist/wheel, or the repo's CI).

## Risk

- **Raw-URL availability / path stability.** READMEs depend on the `.github`
  `main` raw path. Likelihood low (path is stable; `.github` is canonical), impact
  medium (broken image if moved). *Mitigation:* keep `brand/projects/<repo>/`
  paths stable; they're already the established layout.
- **Dark recolor correctness.** The `GOLD_LIGHT→GOLD_DARK` swap + cream name could
  in principle misrender a symbol on dark. Likelihood low (verified colourway
  matches the marks' on-green treatment), impact low. *Mitigation:* the test
  asserts the dark SVG's palette; spot-render one dark lockup during the `.github`
  task.
- **PyPI sanitization variance.** If a renderer drops `<picture>` AND the `<img>`,
  no logo shows. Likelihood low (the `<img>`+`<p align>` are in readme_renderer's
  allowlist). *Mitigation:* `twine check` in the per-repo verification.
- **Heading removal churn.** The exact `# <name>` line varies slightly per repo
  (and one uses `readme.md`). *Mitigation:* the rollout reads each README first
  and replaces only the leading H1.

# Deferred

Real-but-unscheduled items, each with a revisit trigger. Add entries lazily.

## Zensical cutover for the docs sites

**What:** Replace Material for MkDocs with [Zensical](https://zensical.org)
(same team) as the builder for the org site and per-project docs sites.
Validated feasible against Zensical 0.0.46 on 2026-07-05: a `zensical.toml`
mirror of `mkdocs.yml` plus a one-block `overrides/main.html` tweak (dedupe the
homepage `<title>` by title text) builds the current site cleanly under both
builders. The spike branch was not kept — redo the port from `mkdocs.yml` when
revisiting.

**Why deferred:** Zensical is still pre-1.0 alpha (0.0.46 as of 2026-07-05, the
latest release) with known gaps versus our current setup.

**Revisit trigger — when Zensical reaches beta/1.0, re-check:**

1. **`page.is_homepage`** (and siblings) exposed to custom templates. Today it
   is undefined/falsy under Zensical; the spike works around it by deduping the
   homepage `<title>` by title text.
2. **`validation` parity** for the docs-heavy repos (e.g. `faststream-outbox`,
   which runs `mkdocs build --strict`): `omitted_files` / orphaned-page
   detection and `absolute_links` have **no** documented Zensical equivalent,
   and several Zensical validation keys are still marked deprecated. `--strict`
   itself and `invalid_links` / `invalid_link_anchors` do map.
3. **`classic` variant fidelity** — that the traditional Material look still
   matches the live site after the theme rewrite stabilizes.

# Docs sites vendor brand assets; READMEs hotlink them

**Decision:** A repo's `README.md` embeds its lockup by absolute
`raw.githubusercontent.com/modern-python/.github/main/brand/projects/<repo>/` URL, so no asset file
is committed to that repo. A repo's **docs site** does the opposite: it copies `lockup-light.svg`
and `lockup-dark.svg` into its own `docs/assets/`.

Hotlinking everywhere was the tidier option — one copy of every asset, in the repo that generates
them, and a regenerated mark propagates without touching 26 repos. It is right for READMEs, which
GitHub renders directly and which have no build step to break.

It is wrong for docs sites. `mkdocs build --strict` does not check external URLs, so a moved or
renamed asset fails silently at serve time instead of at build time; the build also becomes subject
to CDN caching lag, to a site's CSP, and to network access, which breaks offline builds. Docs sites
already vendor every other brand asset (`mark.svg`, `favicon.svg`, `social-card.png` are committed
copies today), so vendoring the lockup is the consistent choice as well as the robust one.

The cost is accepted and real: a lockup change means re-copying into each docs repo. That is the
same manual step those repos already take for their other assets.

**Revisit trigger:** MkDocs gains external-link validation under `--strict`, or the number of docs
repos makes the re-copy step the thing that actually breaks.

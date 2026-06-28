# Architecture — the truth home

This directory holds the **living truth** about what `modern-python/.github` does
*now*: one file per capability, plus a single `glossary.md` (the ubiquitous
language). These files carry **no frontmatter** and are dated by git.

**Promotion rule:** when a change alters a capability's behavior, hand-edit the
matching `architecture/<capability>.md` in the **same PR** as the code — the edit
rides in the same diff and is reviewed with it. The change bundle in
`planning/changes/` stays as the *why*; this directory stays *true*.

Capability files and `glossary.md` are authored **lazily** — each appears when the
first capability or term is worth pinning down.

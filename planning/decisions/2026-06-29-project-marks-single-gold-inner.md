---
status: accepted
summary: Project marks use a single gold inner symbol; per-family accent colours rejected as too busy.
supersedes: null
superseded_by: null
---

# Project marks are two-colour (green+gold), differentiated by symbol not colour

**Decision:** Every per-project mark uses the constant green+gold snake-frame
with a single **gold** inner symbol. Projects are told apart by the *shape* of
the inner symbol, not by colour. No per-family accent hue.

## Context

While designing the per-project system we evaluated giving each of the four
families its own accent colour for the inner symbol — a "Heritage" palette
(dependency-injection = terracotta, templates = slate blue, microservices =
plum, utilities = teal) and a brighter "Vivid" alternative. The research on
comparable systems (JetBrains, Adobe, Astral) recommends two discriminators
(shape **and** colour) — but only because those marks must survive favicon
sizes. Our project marks are **large-format only**; the org mark remains every
repo's favicon.

Options on the table:
1. Green+gold frame + gold inner (one colour) — chosen.
2. Green+gold frame + per-family accent inner (three colours on the mark).
3. All-green frame + per-family accent inner.

## Decision & rationale

Rendered side by side, the per-family accent made each mark a **three-colour**
object (green frame + gold frame + accent inner), which read as busy and diluted
the org identity. Since favicon-size legibility is explicitly a non-goal, the
second discriminator (colour) buys little. A single gold inner keeps every mark
unmistakably part of one family, matches the existing brand palette exactly, and
means a new repo only needs a new *shape*, not a new colour to keep harmonious.
Templates don't even get a symbol — they reuse the org chevron mark.

## Revisit trigger

If the org ever needs these marks at favicon scale (shape alone insufficient to
disambiguate), or if a family grows large enough that a colour band materially
helps wayfinding on the org site, reopen and reconsider per-family accents.

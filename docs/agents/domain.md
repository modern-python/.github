# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring
the codebase.

This repo does **not** use the stock `CONTEXT.md` + `docs/adr/` layout. It follows the
two-axis planning convention (applied version in `planning/.convention-version`), which
already has a home for each role. Use the repo's own files — do not create `CONTEXT.md`,
`CONTEXT-MAP.md`, or `docs/adr/`.

## Layout: single-context

| Stock skill concept                | This repo                                      |
| ---------------------------------- | ---------------------------------------------- |
| `CONTEXT.md` (ubiquitous language) | `architecture/glossary.md`                     |
| what the system does now           | `architecture/<capability>.md`, one per capability |
| `docs/adr/` (durable decisions)    | `planning/decisions/<YYYY-MM-DD>-<slug>.md`    |
| the *why* behind a shipped change  | `planning/changes/<YYYY-MM-DD>.NN-<slug>.md`   |

## Before exploring, read these

- `architecture/README.md`, then the `architecture/<capability>.md` files touching your
  area. This is the living truth about what the repo does now.
- `architecture/glossary.md` — the ubiquitous language.
- `planning/decisions/*.md` whose subject touches your area. Each carries
  `status: accepted | superseded`; a superseded decision is history, follow
  `superseded_by`.
- `planning/changes/*.md` for the rationale behind a specific past change.
  `just index` prints the change/decision listing.

If any of these don't exist, **proceed silently**. Don't flag their absence; don't suggest
creating them upfront. `architecture/glossary.md` in particular is authored lazily — it
appears when the first term is worth pinning down.

## Use the glossary's vocabulary

When your output names a domain concept (an issue title, a refactor proposal, a
hypothesis, a test name), use the term as defined in `architecture/glossary.md`, and
honor its `_Avoid_:` lines — those synonyms are rejected on purpose.

If the concept you need isn't in the glossary yet, that's a signal: either you're
inventing language the project doesn't use (reconsider) or there's a real gap (note it
for `/domain-modeling`).

## Writing back

Domain docs here are written under the planning convention, not freehand:

- **A new or sharpened term** → edit `architecture/glossary.md` in the same PR as the
  change. No frontmatter; each entry is a term, a one-or-two-sentence definition of what
  it *is*, and an optional `_Avoid_:` line. Seed a new file from
  `planning/_templates/glossary.md`.
- **A behavior change** → hand-edit the affected `architecture/<capability>.md` in the
  implementing PR, alongside the code. Never as a separate post-merge step.
- **A design decision, especially a rejected option** → a new
  `planning/decisions/<YYYY-MM-DD>-<slug>.md` from `planning/_templates/decision.md`,
  including its **Revisit trigger**.
- Run `just check-planning` before pushing.

## Flag conflicts

If your output contradicts an accepted decision or a capability page, surface it
explicitly rather than silently overriding:

> _Contradicts `planning/decisions/2026-06-29-project-marks-single-gold-inner.md`, but
> worth reopening because…_

A decision's **Revisit trigger** names the concrete signal that should reopen it. If that
signal has fired, say so.

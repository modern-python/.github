# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the
codebase. This repo is **single-context**.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root: what this repo is, and the glossary.
- **`docs/adr/`**: read the decision records that touch the area you're about to work in.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest
creating them upfront. The `/domain-modeling` skill creates them lazily when terms or decisions
actually get resolved.

## File structure

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-….md
│   └── 0002-….md
├── brand/          ← the brand kit and its generator
├── profile/        ← the org profile README
└── tests/
```

There is no `CONTEXT-MAP.md` and no per-package `CONTEXT.md`: one repo, one context. There is also
no `architecture/` and no `planning/` — the present is the source, and what must stay true is a test
whose docstring opens `INVARIANT:`.

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a proposal, a hypothesis, a test name),
use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids:
write `mark` and not `logo`, `colourway` and not `colorway`, `inner symbol` and not `glyph`.

If the concept you need isn't in the glossary yet, that's a signal: either you're inventing language
the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Where a new fact goes

Run the admission check in `AGENTS.md` before writing anything down. In short: derivable from the
source → don't write it; enforceable → a named test with an `INVARIANT:` docstring; a user needs it
→ `docs/` or `profile/README.md`; a rejected alternative → an ADR; real work you are not doing now →
a GitHub issue. Nothing else gets written.

## Link style inside `docs/`

`docs/` is the MkDocs `docs_dir`, and the same files are read on GitHub. Two rules keep a link
working in both renderings:

- **Between files inside `docs/`, use a plain relative `.md` link.** MkDocs rewrites it to a site
  URL and GitHub follows it as a file. From one ADR to another, that is `[ADR-NNNN](NNNN-slug.md)`.
- **Never link from a file inside `docs/` to a path outside it.** It cannot resolve in both
  renderings: MkDocs ships the link verbatim, so it 404s on the site. Cite `brand/...`, `tests/...`,
  and root files as inline code, never as links.

## Flag ADR conflicts

If your output contradicts an existing decision record, surface it explicitly rather than silently
overriding:

> _Contradicts ADR-NNNN (its title), but worth reopening because…_

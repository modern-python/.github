---
summary: Adopt lesnik512/planning-convention v1.1.1 at the repo root and migrate docs/superpowers/ into planning/ change bundles plus a lazy architecture/ truth home.
---

# Design: Adopt the planning convention and migrate docs/superpowers/

## Summary

Apply the portable two-axis planning convention from
[`lesnik512/planning-convention`](https://github.com/lesnik512/planning-convention)
(v1.1.1) to this repo via its `APPLY.md` flow, as a **fresh adoption**, and
migrate the existing planning material under `docs/superpowers/` into the
convention's `planning/changes/` bundles. The convention's `architecture/` and
`planning/` trees live at the **repo root**, where the convention's prose,
`index.py` path resolution, and `APPLY.md` §5 all assume they live.

This spec is itself written into the new tree it describes
(`planning/changes/2026-06-28.02-adopt-planning-convention/`), dogfooding the
convention from the first artifact.

## Motivation

Planning material currently lives ad hoc under `docs/superpowers/{specs,plans}/`
with a `**Date:**/**Status:**/**Owner:**/**Scope:**` heading block per file and
no validator, index, or shared lane discipline. Specs and plans are loosely
paired by date/slug and are not machine-checkable. Adopting the canonical
convention gives the org a single, portable, agent-friendly planning model
(shared across every `modern-python` repo): lean frontmatter, a `check-planning`
validator, a generated index, a Quick-path lane decision, and a living
`architecture/` truth home.

## Decisions (ruled by the maintainer during brainstorming)

1. **Location: repo root.** Create `/planning/` and `/architecture/`; migrate and
   delete `docs/superpowers/`. Matches the convention verbatim with no prose
   rewrites. Nothing lands under `docs/`, so MkDocs never publishes it and the
   `exclude_docs: superpowers/` rule is retired.
2. **community-health bundle: `change.md`.** The `org-community-health-defaults`
   plan (06-24) has no design doc; the bundle is given a condensed `change.md` as
   its spec. The substantial shipped `plan.md` is **kept alongside** it (the
   validator allows `change.md` + `plan.md` in one bundle) so the detailed
   shipped record is preserved in-repo rather than only in git history.
   *(Open for confirmation at the review gate: keep both, or fold the plan into
   change.md and drop plan.md.)*
3. **Tooling: Justfile + CI check.** Add a `Justfile` (the repo has none) with
   `index` / `check-planning` recipes and run the check in CI on pull requests.
   The new task runner is the `APPLY.md` §3 deviation noted in the PR.
4. **architecture/: lazy.** Create only `architecture/README.md` (the promotion
   rule) per `APPLY.md` §5. Capability files and `glossary.md` are authored
   lazily, when the first capability or term is worth pinning down.

## Design

### 1. Target tree (repo root)

```
planning/
  README.md                 # repo intro + merged convention prose (Quick path + Conventions) + Index + Other
  .convention-version       # 1.1.1
  index.py                  # verbatim from canonical
  _templates/{change,design,plan,decision,release,glossary}.md   # verbatim
  deferred.md               # header only (lazy)
  launch-playbook.md        # moved from docs/superpowers/launch-playbook.md
  changes/
    2026-06-24.01-promotion-strategy/             design.md
    2026-06-24.02-org-community-health-defaults/  change.md + plan.md
    2026-06-27.01-community-channels/             design.md
    2026-06-28.01-org-favicon-social-card/        design.md + plan.md
    2026-06-28.02-adopt-planning-convention/      design.md (this spec) + plan.md
  decisions/   (.gitkeep — lazy)
  releases/    (.gitkeep — lazy)
architecture/
  README.md                 # promotion rule only
```

`index.py` resolves `changes/` and `decisions/` relative to its own parent, so
`planning/index.py` validates the `planning/` tree correctly.

### 2. Content migration

Each migrated artifact is moved (`git mv` where 1:1) and reshaped to convention
frontmatter. Migration is **structural only**: each document's existing body and
headings are preserved (the templates are starting points, not mandatory section
names; the validator enforces only `summary:` on specs).

| Bundle | Lane | Source | Frontmatter change |
|---|---|---|---|
| `2026-06-24.01-promotion-strategy` | design-only (pending) | `specs/2026-06-24-promotion-strategy-design.md` → `design.md` | add `summary:`; drop the `**Date/Status/Owner/Scope**` block (date derived from dir; `status`/`owner` are not convention fields); keep Scope as a prose line |
| `2026-06-24.02-org-community-health-defaults` | `change.md` + `plan.md` | `plans/2026-06-24-org-community-health-defaults.md` → `plan.md`; new `change.md` from the plan intro | plan.md: none; change.md: `summary:` |
| `2026-06-27.01-community-channels` | design-only (pending) | `specs/2026-06-27-community-channels-design.md` → `design.md` | same as promotion-strategy |
| `2026-06-28.01-org-favicon-social-card` | Full | `specs/2026-06-28-org-favicon-social-card-design.md` → `design.md`; `plans/2026-06-28-org-favicon-social-card.md` → `plan.md` | design.md: `summary:`, drop Status; plan.md: none |

The `.NN` counter on 06-24 places the strategic umbrella (`promotion-strategy`)
at `.01` and its implementation (`community-health-defaults`) at `.02`.

`launch-playbook.md` moves to `planning/launch-playbook.md` as a loose
operational asset — it cannot live inside a bundle (the validator rejects any
file other than `design.md`/`plan.md`/`change.md` there). Its "excluded via
`exclude_docs`" note is updated, since it now sits at the repo root and is never
published. After migration, `docs/superpowers/` is deleted.

### 3. Tooling, CI, and instructions

- **`Justfile`** (new): `index` (`uv run python planning/index.py`),
  `check-planning` (`uv run python planning/index.py --check`), a `lint-ci` that
  runs the check, and `test` (`uv run pytest`) since the repo already has tests.
- **CI** (new `.github/workflows/planning.yml`): on `pull_request` and `push`,
  run `uv run python planning/index.py --check` (expect `planning: OK`).
  `deploy.yml` is untouched.
- **`CLAUDE.md`**: add a `## Workflow` pointer naming `planning/README.md`'s
  Quick path as the authoritative convention, and the promotion reminder ("When a
  change alters a capability's behavior, update the matching
  `architecture/<capability>.md` in the same PR"). All existing org-conventions
  content is preserved.
- **`planning/README.md`**: repo-specific title/intro, then the body of the
  canonical `convention.md` (Quick path + Conventions) below its title, plus an
  `## Index` note (`just index`) and `## Other` pointers (launch-playbook).
- **`mkdocs.yml`**: remove the now-stale `superpowers/` entry from `exclude_docs`
  (and the block if it empties).
- **`.convention-version`**: `1.1.1`.

### 4. Verbatim-copied artifacts

Per `APPLY.md` §1, copied exactly from the canonical repo into `planning/`:
`index.py` and `_templates/{change,design,plan,decision,release,glossary}.md`.
Local edits to these are intentionally not made — they are owned upstream.

## Non-goals

- Authoring `architecture/` capability files or `glossary.md` now — deferred to
  lazy authoring per the chosen decision.
- Rewriting the bodies of the migrated specs/plans — migration is structural.
- Extracting `decisions/` entries from the existing specs — authored lazily.
- Changing what the published MkDocs site contains (other than dropping the
  retired `superpowers/` exclude line).

## Testing

- `just check-planning` → must print `planning: OK`.
- `uv run mkdocs build --strict` → still succeeds (no `docs/superpowers/`
  references remain).
- `git grep -n "docs/superpowers"` → returns nothing stale.
- New `planning.yml` CI run is green on the PR.

## Risk

- **Plan-without-design bundle fails validation** (community-health). Mitigated by
  decision 2 (write a `change.md`).
- **Stale references** to `docs/superpowers/` elsewhere in the repo (e.g.
  `mkdocs.yml`, CLAUDE.md, launch-playbook prose). Mitigated by the `git grep`
  verification step.
- **CI gotcha** (per repo CLAUDE.md): GitHub may type-check a stale
  `refs/pull/<n>/merge`. If the new check fails spuriously, confirm clean locally
  at branch HEAD and push a fresh commit.
- **Convention drift**: future `APPLY.md` updates re-copy `index.py`/templates;
  any local edits to them would be discarded. Mitigated by not editing them.

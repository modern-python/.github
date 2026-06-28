# Adopt the planning convention Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adopt `lesnik512/planning-convention` v1.1.1 at this repo's root and migrate the existing `docs/superpowers/` planning material into convention-shaped `planning/changes/` bundles plus a lazy `architecture/` truth home.

**Architecture:** Fresh adoption per the canonical repo's `APPLY.md`. The convention's two axes — `planning/` (bundles, validator, templates) and `architecture/` (living truth) — land at the repo root. Upstream-owned files (`index.py`, `_templates/*`) are copied verbatim from a clone; the existing specs/plans are `git mv`d into dated bundles and reshaped to lean `summary:` frontmatter; tooling (`Justfile`, CI) gates `check-planning`.

**Tech Stack:** Python 3.11+ stdlib (the `index.py` validator has no third-party deps), `uv` (task/env runner), `just` (new task runner), GitHub Actions, MkDocs Material (existing site build).

**Spec:** [`design.md`](./design.md)

**Branch:** `chore/adopt-planning-convention` (already created; the spec is committed on it).

**Commit strategy:** One commit per task.

## Global Constraints

- **Convention version:** v1.1.1 (latest CHANGELOG entry in the canonical repo). Record it verbatim in `planning/.convention-version`.
- **Canonical source:** `https://github.com/lesnik512/planning-convention`. `index.py` and `_templates/*` are **owned upstream — copy verbatim, never hand-edit**.
- **Lean frontmatter (validator-enforced):** `date`/`slug` are derived from the directory/file name, never written. `design.md`/`change.md` carry `summary:` only; `plan.md` carries **none**; `decisions/*.md` carry `status` + `summary` (+ optional `supersedes`/`superseded_by`); `architecture/` files carry none.
- **Bundle dir name:** `YYYY-MM-DD.NN-slug` (zero-padded intra-day counter). Bundle may contain only `design.md`, `plan.md`, `change.md`.
- **Repo layout:** `planning/` and `architecture/` live at the **repo root**, never under `docs/` (MkDocs publishes only `docs/`).
- **Verification baseline:** `uv run python planning/index.py --check` must print `planning: OK`; `uv run mkdocs build --strict` must succeed.
- **Commit trailer:** end every commit message body with `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`. Do not mention Claude Code in the body.

---

### Task 1: Scaffold the convention skeleton (verbatim copies + dirs + version)

Copy the upstream-owned files and create the fresh-adopt scaffolding. After this task, `changes/` already contains the committed `2026-06-28.02-adopt-planning-convention/` bundle (design.md + plan.md), so the validator has a real bundle to check.

**Files:**
- Create: `planning/index.py` (verbatim copy)
- Create: `planning/_templates/{change,design,plan,decision,release,glossary}.md` (verbatim copies)
- Create: `planning/.convention-version`
- Create: `planning/deferred.md`
- Create: `planning/decisions/.gitkeep`
- Create: `planning/releases/.gitkeep`
- Create: `architecture/README.md`

**Interfaces:**
- Produces: `planning/index.py` runnable as `uv run python planning/index.py [--check]`; the `planning/_templates/` set later tasks copy from; the `changes/` directory the migration tasks populate.

- [ ] **Step 1: Clone the canonical repo to a temp dir**

```bash
CONV=$(mktemp -d)/planning-convention
git clone --depth 1 https://github.com/lesnik512/planning-convention "$CONV"
echo "$CONV"
```

Expected: clone succeeds. Keep `$CONV` for the next steps (re-export if your shell resets between steps: `CONV=<path printed above>`).

- [ ] **Step 2: Copy the verbatim-owned files**

```bash
mkdir -p planning/_templates planning/decisions planning/releases architecture
cp "$CONV/index.py" planning/index.py
cp "$CONV/_templates/"*.md planning/_templates/
```

- [ ] **Step 3: Verify the copies are byte-identical to upstream**

```bash
diff "$CONV/index.py" planning/index.py && \
for f in change design plan decision release glossary; do \
  diff "$CONV/_templates/$f.md" "planning/_templates/$f.md" || echo "MISMATCH: $f"; \
done && echo "all verbatim copies OK"
```

Expected: no diff output, ends with `all verbatim copies OK`.

- [ ] **Step 4: Write the version file, deferred stub, gitkeeps, and architecture README**

```bash
printf '1.1.1\n' > planning/.convention-version
printf '# Deferred\n\nReal-but-unscheduled items, each with a revisit trigger. Add entries lazily.\n' > planning/deferred.md
: > planning/decisions/.gitkeep
: > planning/releases/.gitkeep
```

Then create `architecture/README.md` with exactly this content:

```markdown
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
```

- [ ] **Step 5: Run the validator to confirm a clean baseline**

```bash
uv run python planning/index.py --check
```

Expected: `planning: OK` (the committed `2026-06-28.02-adopt-planning-convention/` bundle has a valid `design.md`; `decisions/`/`releases/` hold only `.gitkeep`, which the validator ignores).

- [ ] **Step 6: Confirm the index generator runs**

```bash
uv run python planning/index.py
```

Expected: a `# Planning index` listing showing the `adopt-planning-convention` change under `## Changes` and `_None._` under `## Decisions`.

- [ ] **Step 7: Commit**

```bash
git add planning/index.py planning/_templates planning/.convention-version \
  planning/deferred.md planning/decisions/.gitkeep planning/releases/.gitkeep \
  architecture/README.md
git commit -m "chore: scaffold planning convention skeleton (v1.1.1)"
```

---

### Task 2: Write `planning/README.md` (merged convention prose)

Create the consumer README: a repo-specific intro, then the canonical `convention.md` body (Quick path + Conventions) pasted verbatim, then repo-local `## Index` and `## Other` sections.

**Files:**
- Create: `planning/README.md`

**Interfaces:**
- Consumes: the cloned `$CONV/convention.md` from Task 1 (re-clone if the temp dir is gone: `CONV=$(mktemp -d)/pc && git clone --depth 1 https://github.com/lesnik512/planning-convention "$CONV"`).
- Produces: `planning/README.md` — the authoritative convention prose `CLAUDE.md` will point at in Task 7.

- [ ] **Step 1: Write the repo intro + section scaffold**

Create `planning/README.md` with exactly this content:

```markdown
# Planning — modern-python/.github

This repo's planning home, following the portable two-axis convention from
[`lesnik512/planning-convention`](https://github.com/lesnik512/planning-convention)
(applied version in [`.convention-version`](.convention-version)). `architecture/`
(repo root) holds the living truth about what the system does now; the bundles in
[`changes/`](changes/) record how it got there. To update the convention itself,
re-run that repo's `APPLY.md` flow.

<!-- CONVENTION-BODY: paste convention.md's Quick path + Conventions below -->

## Index

Run `just index` to print the change/decision listing — a query over the files,
never a committed artifact.

## Other

- [`launch-playbook.md`](launch-playbook.md) — internal Phase 4 launch asset (not published).
- [`deferred.md`](deferred.md) — real-but-unscheduled items, each with a revisit trigger.
```

- [ ] **Step 2: Splice in the canonical convention prose**

Replace the `<!-- CONVENTION-BODY: ... -->` marker line with everything in `$CONV/convention.md` from the `## Quick path (start here)` heading through the end of the file (the Quick path + Conventions sections — i.e. the canonical body below its `# Planning convention` title and intro):

```bash
# Extract the Quick path → EOF block from the canonical convention.md
awk '/^## Quick path/{p=1} p' "$CONV/convention.md" > /tmp/conv-body.md
# Replace the marker line with that block
python3 - <<'PY'
import pathlib
readme = pathlib.Path("planning/README.md")
body = pathlib.Path("/tmp/conv-body.md").read_text(encoding="utf-8").rstrip() + "\n"
text = readme.read_text(encoding="utf-8")
marker = "<!-- CONVENTION-BODY: paste convention.md's Quick path + Conventions below -->\n"
assert marker in text, "marker not found"
readme.write_text(text.replace(marker, body), encoding="utf-8")
print("spliced")
PY
```

Expected: prints `spliced`.

- [ ] **Step 3: Verify the prose landed**

```bash
grep -q "^## Quick path" planning/README.md && \
grep -q "^### Frontmatter" planning/README.md && \
grep -q "^## Index" planning/README.md && \
grep -q "^## Other" planning/README.md && echo "README OK"
```

Expected: `README OK` (Quick path + Conventions body present, repo-local sections preserved).

- [ ] **Step 4: Commit**

```bash
git add planning/README.md
git commit -m "docs: add planning/README with merged convention prose"
```

---

### Task 3: Migrate the design-only bundles (promotion-strategy, community-channels)

`git mv` two specs into dated bundles and reshape their headers to `summary:` frontmatter. Both are approved-but-unimplemented designs, so they are valid design-only bundles (no `plan.md`).

**Files:**
- Create: `planning/changes/2026-06-24.01-promotion-strategy/design.md` (moved from `docs/superpowers/specs/2026-06-24-promotion-strategy-design.md`)
- Create: `planning/changes/2026-06-27.01-community-channels/design.md` (moved from `docs/superpowers/specs/2026-06-27-community-channels-design.md`)

- [ ] **Step 1: Move the two specs into bundles**

```bash
mkdir -p planning/changes/2026-06-24.01-promotion-strategy \
         planning/changes/2026-06-27.01-community-channels
git mv docs/superpowers/specs/2026-06-24-promotion-strategy-design.md \
       planning/changes/2026-06-24.01-promotion-strategy/design.md
git mv docs/superpowers/specs/2026-06-27-community-channels-design.md \
       planning/changes/2026-06-27.01-community-channels/design.md
```

- [ ] **Step 2: Reshape the promotion-strategy header**

In `planning/changes/2026-06-24.01-promotion-strategy/design.md`, replace the top block. The current top is:

```markdown
# Modern Python — Promotion Strategy

**Date:** 2026-06-24
**Status:** Approved design, ready for planning
**Owner:** modern-python maintainers
**Scope:** Org-wide growth strategy for the `modern-python` GitHub org
```

Replace it with (add frontmatter; drop `**Date:**`/`**Status:**`/`**Owner:**`; keep `**Scope:**` as prose):

```markdown
---
summary: Org-wide, users-first staged growth strategy for the modern-python GitHub org along three axes (reach, retain, contribute).
---

# Modern Python — Promotion Strategy

**Scope:** Org-wide growth strategy for the `modern-python` GitHub org
```

Leave the rest of the document (from `## Goal` onward) unchanged.

- [ ] **Step 3: Reshape the community-channels header**

In `planning/changes/2026-06-27.01-community-channels/design.md`, the current top is:

```markdown
# Modern Python — Community & Channels

**Date:** 2026-06-27
**Status:** Approved design, ready for planning
**Owner:** modern-python maintainers
**Scope:** Which channels the `modern-python` org uses to reach, support, and
retain users — and how they fit together. Extends the
```

Replace **only** the title-and-metadata lines (the `# Modern Python — Community & Channels` heading and the four `**Date/Status/Owner/Scope**` lines, keeping `**Scope:**` as prose) with:

```markdown
---
summary: Which channels the modern-python org uses to reach, support, and retain users, and how they fit together.
---

# Modern Python — Community & Channels

**Scope:** Which channels the `modern-python` org uses to reach, support, and
retain users — and how they fit together. Extends the
```

Keep everything after the `**Scope:**` sentence unchanged (the Scope sentence continues into the existing body — do not truncate it).

- [ ] **Step 4: Validate**

```bash
uv run python planning/index.py --check
```

Expected: `planning: OK`.

- [ ] **Step 5: Commit**

```bash
git add planning/changes/2026-06-24.01-promotion-strategy \
        planning/changes/2026-06-27.01-community-channels
git commit -m "docs: migrate promotion-strategy and community-channels into bundles"
```

---

### Task 4: Migrate the org-favicon-social-card Full bundle

`git mv` the paired spec + plan into one Full bundle; reshape the spec header, leave the plan frontmatter-free.

**Files:**
- Create: `planning/changes/2026-06-28.01-org-favicon-social-card/design.md` (moved from `docs/superpowers/specs/2026-06-28-org-favicon-social-card-design.md`)
- Create: `planning/changes/2026-06-28.01-org-favicon-social-card/plan.md` (moved from `docs/superpowers/plans/2026-06-28-org-favicon-social-card.md`)

- [ ] **Step 1: Move the spec and plan into one bundle**

```bash
mkdir -p planning/changes/2026-06-28.01-org-favicon-social-card
git mv docs/superpowers/specs/2026-06-28-org-favicon-social-card-design.md \
       planning/changes/2026-06-28.01-org-favicon-social-card/design.md
git mv docs/superpowers/plans/2026-06-28-org-favicon-social-card.md \
       planning/changes/2026-06-28.01-org-favicon-social-card/plan.md
```

- [ ] **Step 2: Reshape the design header**

In `planning/changes/2026-06-28.01-org-favicon-social-card/design.md`, the current top is:

```markdown
# modern-python org favicon + social card — design spec

**Status:** approved design (brainstorming output)
**Scope:** the org-level **favicon** and **social card** only. Everything else
```

Replace the title and the `**Status:**` line (drop `**Status:**`; keep `**Scope:**` as prose) with:

```markdown
---
summary: Replaced the snake brand mark with the pinwheel favicon/avatar and Jost wordmark social card, generated by the brand/build/ toolchain.
---

# modern-python org favicon + social card — design spec

**Scope:** the org-level **favicon** and **social card** only. Everything else
```

Leave the `**Scope:**` sentence and everything after it unchanged.

- [ ] **Step 3: Confirm the plan carries no frontmatter**

```bash
head -1 planning/changes/2026-06-28.01-org-favicon-social-card/plan.md
```

Expected: the plan's first line is its `#` title (the "For agentic workers" plan), **not** `---`. Plans carry no frontmatter — make no change.

- [ ] **Step 4: Validate**

```bash
uv run python planning/index.py --check
```

Expected: `planning: OK`.

- [ ] **Step 5: Commit**

```bash
git add planning/changes/2026-06-28.01-org-favicon-social-card
git commit -m "docs: migrate org-favicon-social-card into a Full bundle"
```

---

### Task 5: Migrate the community-health bundle (plan.md + new change.md)

`git mv` the existing detailed plan, then author a condensed `change.md` as the bundle's required spec. Per the spec's decision, **both** files are kept: `change.md` is the condensed why; `plan.md` is the shipped detail.

**Files:**
- Create: `planning/changes/2026-06-24.02-org-community-health-defaults/plan.md` (moved from `docs/superpowers/plans/2026-06-24-org-community-health-defaults.md`)
- Create: `planning/changes/2026-06-24.02-org-community-health-defaults/change.md` (new)

- [ ] **Step 1: Move the plan into the bundle**

```bash
mkdir -p planning/changes/2026-06-24.02-org-community-health-defaults
git mv docs/superpowers/plans/2026-06-24-org-community-health-defaults.md \
       planning/changes/2026-06-24.02-org-community-health-defaults/plan.md
```

- [ ] **Step 2: Write the condensed `change.md`**

Create `planning/changes/2026-06-24.02-org-community-health-defaults/change.md` with exactly this content:

```markdown
---
summary: Added org-wide default community-health files so every modern-python repo lacking its own inherits a CONTRIBUTING guide, Code of Conduct, security policy, support routing, issue/PR templates, and funding config — lifting coverage from ~25% to ~90% in one PR.
---

# Change: Org-wide community-health defaults

**Lane:** condensed spec for an already-shipped, multi-file org-wide change.
The full task-by-task record lives in [`plan.md`](./plan.md); this page is the
why.

## Goal

Every repo in the `modern-python` org that does not define its own
community-health files should inherit sensible org defaults, so contributors get
a consistent CONTRIBUTING guide, Code of Conduct, security policy, support
routing, issue/PR templates, and funding config without per-repo upkeep.

## Approach

GitHub serves *default* community-health files from the special `modern-python/.github`
repo: files at the repo **root** or under **`.github/`** apply to every org repo
that lacks its own. This repo also builds the public site from `docs/`, so the
community-health files go at the root or under `.github/` — **never under
`docs/`**, which would publish them. See [`plan.md`](./plan.md) for the per-file
task breakdown and verifications.

## Files

- Root community-health files (`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`,
  `SECURITY.md`, `SUPPORT.md`) and `.github/` issue/PR templates + funding config.
- [`plan.md`](./plan.md) — the detailed implementation plan (shipped).

## Verification

- [x] Each YAML form/config parses.
- [x] `mkdocs build --strict` still succeeds (no community-health file leaks into the site).
- [x] Each file lands at a path GitHub recognizes as an org default.
```

- [ ] **Step 3: Validate (the bundle now has change.md + plan.md)**

```bash
uv run python planning/index.py --check
```

Expected: `planning: OK` (the bundle has `change.md` for its spec; `plan.md` carries no frontmatter; both are allowed bundle files).

- [ ] **Step 4: Confirm the bundle appears in the index with its summary**

```bash
uv run python planning/index.py | grep "org-community-health-defaults"
```

Expected: a `- **[org-community-health-defaults](...)** (2026-06-24) — Added org-wide default community-health files…` line.

- [ ] **Step 5: Commit**

```bash
git add planning/changes/2026-06-24.02-org-community-health-defaults
git commit -m "docs: migrate community-health defaults into a bundle"
```

---

### Task 6: Move the launch playbook and delete `docs/superpowers/`

Relocate the loose internal asset to `planning/`, refresh its now-stale publishing note, and remove the emptied directory.

**Files:**
- Create: `planning/launch-playbook.md` (moved from `docs/superpowers/launch-playbook.md`)
- Delete: `docs/superpowers/` (now empty of tracked files)

- [ ] **Step 1: Move the launch playbook**

```bash
git mv docs/superpowers/launch-playbook.md planning/launch-playbook.md
```

- [ ] **Step 2: Refresh its publishing note**

In `planning/launch-playbook.md`, the second line currently reads:

```markdown
Internal asset — **not published** (excluded from the site via `exclude_docs`).
```

Replace it with (it now lives at the repo root, outside `docs/`, so it is never seen by MkDocs):

```markdown
Internal asset — **not published** (lives at the repo root, outside the MkDocs `docs/` tree).
```

- [ ] **Step 3: Confirm `docs/superpowers/` has no tracked files left, then remove it**

```bash
git ls-files docs/superpowers
```

Expected: **no output** (every tracked file was moved). Then:

```bash
rm -rf docs/superpowers
```

- [ ] **Step 4: Verify no stale references remain**

```bash
git grep -n "docs/superpowers" -- . ':!planning/changes/2026-06-28.02-adopt-planning-convention/*' || echo "no stale references"
```

Expected: `no stale references`. (The adopt-convention spec/plan describe the migration and legitimately name the old paths; they are excluded from this check.)

- [ ] **Step 5: Commit**

```bash
git add planning/launch-playbook.md
git add -A docs/superpowers 2>/dev/null || true
git commit -m "docs: move launch playbook to planning/, retire docs/superpowers"
```

---

### Task 7: Add the `Justfile`, CI check, and `CLAUDE.md` wiring

Introduce the task runner (the repo has none), gate `check-planning` in CI, and point the repo's `CLAUDE.md` at the convention. This is the `APPLY.md` §3 deviation (new `just`) to note in the PR.

**Files:**
- Create: `Justfile`
- Create: `.github/workflows/planning.yml`
- Modify: `CLAUDE.md`
- Modify: `mkdocs.yml` (remove the `superpowers/` exclude line)

- [ ] **Step 1: Create the `Justfile`**

Create `Justfile` at the repo root with exactly this content:

```make
default: check-planning test

index:
    uv run python planning/index.py

check-planning:
    uv run python planning/index.py --check

lint-ci: check-planning

test:
    uv run pytest
```

- [ ] **Step 2: Verify the recipes run**

```bash
just check-planning
```

Expected: `planning: OK`. (If `just` is not installed: `uv run python planning/index.py --check` directly, but the recipe is what CI and contributors use.)

- [ ] **Step 3: Create the CI workflow**

Create `.github/workflows/planning.yml` with exactly this content:

```yaml
name: Planning

on:
  pull_request:
  push:
    branches: [main]

jobs:
  check-planning:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Install uv
        uses: astral-sh/setup-uv@v7
        with:
          python-version: "3.11"
      - name: Validate planning bundles
        run: uv run python planning/index.py --check
```

- [ ] **Step 4: Remove the stale `superpowers/` exclude from `mkdocs.yml`**

In `mkdocs.yml`, the `exclude_docs` block currently reads:

```yaml
exclude_docs: |
  DEPLOYMENT.md
  superpowers/
```

Remove only the `superpowers/` line (keep `DEPLOYMENT.md`):

```yaml
exclude_docs: |
  DEPLOYMENT.md
```

- [ ] **Step 5: Add the `## Workflow` and `## Architecture` sections to `CLAUDE.md`**

Append the following two sections to the end of `CLAUDE.md` (preserve all existing content above):

```markdown
## Workflow

Planning follows the convention in [`planning/README.md`](planning/README.md) —
its **Quick path** is authoritative. Pick a lane (Full = `design.md` + `plan.md`,
Lightweight = `change.md`, Tiny = conventional commit), create a bundle under
`planning/changes/YYYY-MM-DD.NN-<slug>/` from `planning/_templates/`, and run
`just check-planning` before pushing. The applied convention version is in
`planning/.convention-version`; update it via the canonical repo's `APPLY.md`.

## Architecture

`architecture/` (repo root) is the living truth about what this repo does now —
one file per capability plus `glossary.md`, no frontmatter, authored lazily.
**When a change alters a capability's behavior, update the matching
`architecture/<capability>.md` in the same PR.** The change bundle in
`planning/changes/` stays as the *why*.
```

- [ ] **Step 6: Verify the site still builds and planning still validates**

```bash
uv run mkdocs build --strict && just check-planning
```

Expected: MkDocs build succeeds; `planning: OK`.

- [ ] **Step 7: Commit**

```bash
git add Justfile .github/workflows/planning.yml CLAUDE.md mkdocs.yml
git commit -m "chore: wire just + CI check-planning, point CLAUDE.md at the convention"
```

---

### Task 8: Final full verification and open the PR

Confirm the end state matches the spec, then push and open the PR (per the maintainer's PR-only workflow).

**Files:** none (verification + PR).

- [ ] **Step 1: Run the full verification suite**

```bash
just check-planning && \
uv run mkdocs build --strict && \
git grep -n "docs/superpowers" -- . ':!planning/changes/2026-06-28.02-adopt-planning-convention/*' || echo "no stale docs/superpowers references"
```

Expected: `planning: OK`, MkDocs build succeeds, and `no stale docs/superpowers references`.

- [ ] **Step 2: Confirm the end-state tree**

```bash
test -f planning/.convention-version && \
test -f planning/index.py && \
test -d architecture && \
ls planning/changes
```

Expected: the four migrated bundles plus `2026-06-28.02-adopt-planning-convention/` are listed; `.convention-version` and `index.py` exist; `architecture/` exists.

- [ ] **Step 3: Push the branch**

```bash
git push -u origin chore/adopt-planning-convention
```

- [ ] **Step 4: Open the PR**

```bash
gh pr create --title "Adopt planning-convention v1.1.1 and migrate docs/superpowers" --body "$(cat <<'EOF'
Fresh adoption of `lesnik512/planning-convention` **v1.1.1** at the repo root, and migration of the old `docs/superpowers/` planning material into convention bundles.

## What changed
- `planning/` (root): verbatim `index.py` + `_templates/`, merged `README.md`, `.convention-version` (1.1.1), `deferred.md`, lazy `decisions/`/`releases/`.
- `architecture/README.md`: promotion rule only (capability files + glossary authored lazily).
- Migrated bundles: `2026-06-24.01-promotion-strategy` (design-only), `2026-06-24.02-org-community-health-defaults` (change.md + plan.md), `2026-06-27.01-community-channels` (design-only), `2026-06-28.01-org-favicon-social-card` (Full).
- `launch-playbook.md` → `planning/`; `docs/superpowers/` removed; stale `superpowers/` exclude dropped from `mkdocs.yml`.
- Tooling: new `Justfile` (`index`/`check-planning`/`lint-ci`/`test`) and `.github/workflows/planning.yml`; `CLAUDE.md` points at the convention.

## APPLY.md §3 deviation
The repo had **no task runner**; this PR introduces `just` for the convention recipes.

## Verification
- `just check-planning` → `planning: OK`
- `uv run mkdocs build --strict` → succeeds
EOF
)"
```

- [ ] **Step 5: Watch CI**

```bash
gh pr checks --watch
```

Expected: the `Planning` and `Deploy site` workflows pass. (Per the repo's CLAUDE.md CI gotcha: if a check fails on a stale `refs/pull/<n>/merge`, confirm clean locally at HEAD and push a fresh commit to force a recompute.)

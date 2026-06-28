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

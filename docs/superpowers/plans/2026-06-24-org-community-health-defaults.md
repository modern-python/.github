# Org Community-Health Defaults Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add org-wide default community-health files to the `modern-python/.github` repo so every repo in the org that lacks its own gets a CONTRIBUTING guide, Code of Conduct, security policy, support routing, issue/PR templates, and funding config — lifting community-health coverage from ~25% to ~90% org-wide in one PR.

**Architecture:** GitHub serves *default* community-health files from a special `.github` repo in the org. Files placed at the **root** or in **`.github/`** of `modern-python/.github` apply to every repo in the org that does not define its own. This repo also builds the public website from `docs/` via MkDocs, so community-health files must go at the repo root or under `.github/` — **never under `docs/`**, which would publish them to the site. No code, no tests in the traditional sense; each task ends with a concrete verification (YAML parses, MkDocs still builds, file lands at a path GitHub recognizes).

**Tech Stack:** GitHub community-health defaults, GitHub issue *forms* (YAML schema), Markdown, MkDocs Material (existing site build), `uv` (runs the build).

## Global Constraints

- **Repo:** this is `modern-python/.github`. Default community-health files here apply org-wide. Place them at the repo **root** or in **`.github/`** only — never in `docs/` (that directory is the published MkDocs site).
- **Branch:** do this work on a dedicated branch `chore/org-community-health`, cut from `main` (NOT stacked on `docs/promotion-strategy`). One PR.
- **Brand casing (verbatim):** `modern-di`, `that-depends`, `Litestar` (never "LiteStar"), `FastStream`, `FastAPI`, `Typer`, `SQLAlchemy`, `PostgreSQL`.
- **Tooling vocabulary:** projects use `uv` (packaging), `ruff` (lint/format), `ty` (type check), `uv_build` (build backend); most repos expose tasks behind a `justfile`.
- **Security & CoC contact:** use GitHub **private vulnerability reporting** (repo/org → Security → "Report a vulnerability"). Do **not** invent or publish a personal email address.
- **Org Discussions URL:** `https://github.com/orgs/modern-python/discussions` (org-level Discussions must be enabled — see Task 8 manual step).
- **Docs site:** `https://modern-python.org`.
- **Commit footer (every commit):**
  ```
  Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
  ```
- **No "Generated with Claude Code" lines in commits** (org convention).

---

## File Structure

Files created (all in `modern-python/.github`):

```
.github/
  ISSUE_TEMPLATE/
    bug_report.yml          # bug issue form
    feature_request.yml     # feature issue form
    config.yml              # disable blank issues; route questions to Discussions/docs
  PULL_REQUEST_TEMPLATE.md  # default PR template
  FUNDING.yml               # sponsor button config (optional input)
CONTRIBUTING.md             # org-wide contributor guide (root)
CODE_OF_CONDUCT.md          # Contributor Covenant 2.1 (root)
SECURITY.md                 # vulnerability reporting policy (root)
SUPPORT.md                  # where to get help (root)
```

Modified:

```
docs/index.md               # fix "LiteStar" -> "Litestar" casing (lines ~60, ~66)
```

---

## Task 1: Issue forms + PR template

**Files:**
- Create: `.github/ISSUE_TEMPLATE/bug_report.yml`
- Create: `.github/ISSUE_TEMPLATE/feature_request.yml`
- Create: `.github/ISSUE_TEMPLATE/config.yml`
- Create: `.github/PULL_REQUEST_TEMPLATE.md`

**Interfaces:**
- Produces: org-default issue chooser (Bug / Feature) plus two contact links (Discussions, Docs); a default PR template. Consumed by GitHub's new-issue and new-PR UI on every org repo without its own templates.

- [ ] **Step 1: Create the bug report form**

Create `.github/ISSUE_TEMPLATE/bug_report.yml`:

```yaml
name: Bug report
description: Report a defect in a modern-python project
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for filing a bug. Fill in the sections below so we can reproduce it quickly.
  - type: input
    id: project
    attributes:
      label: Affected project
      description: Which repository / package is this about?
      placeholder: e.g. modern-di, that-depends, httpware
    validations:
      required: true
  - type: input
    id: version
    attributes:
      label: Versions
      description: Package version, Python version, and OS.
      placeholder: e.g. modern-di 1.2.0, Python 3.12, macOS 14
    validations:
      required: true
  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: A clear description of the bug and what you expected instead.
    validations:
      required: true
  - type: textarea
    id: repro
    attributes:
      label: Minimal reproduction
      description: The smallest snippet or steps that reproduce the problem.
      render: python
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Logs / traceback
      description: Paste any relevant traceback. Automatically formatted as code.
      render: shell
    validations:
      required: false
```

- [ ] **Step 2: Create the feature request form**

Create `.github/ISSUE_TEMPLATE/feature_request.yml`:

```yaml
name: Feature request
description: Suggest an idea or improvement for a modern-python project
labels: ["enhancement"]
body:
  - type: input
    id: project
    attributes:
      label: Target project
      description: Which repository / package would this affect?
      placeholder: e.g. modern-di, lite-bootstrap
    validations:
      required: true
  - type: textarea
    id: problem
    attributes:
      label: Problem
      description: What problem are you trying to solve? What's the use case?
    validations:
      required: true
  - type: textarea
    id: proposal
    attributes:
      label: Proposed solution
      description: What would you like to happen? Include API sketches if relevant.
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives considered
      description: Other approaches you've weighed, if any.
    validations:
      required: false
```

- [ ] **Step 3: Create the issue chooser config**

Create `.github/ISSUE_TEMPLATE/config.yml`:

```yaml
blank_issues_enabled: false
contact_links:
  - name: Question / usage help
    url: https://github.com/orgs/modern-python/discussions
    about: Ask questions and get help in GitHub Discussions.
  - name: Documentation
    url: https://modern-python.org
    about: Browse the docs — your question may already be answered.
```

- [ ] **Step 4: Create the PR template**

Create `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Summary

<!-- What does this change and why? Link any related issue: Closes #123 -->

## Changes

<!-- Bullet the notable changes. -->
-

## Checklist

- [ ] Lint and format pass (`ruff`)
- [ ] Type check passes (`ty`)
- [ ] Tests pass and new behavior is covered
- [ ] Docs updated if behavior or public API changed
- [ ] Repo metadata stays consistent across the three surfaces (GitHub description, pyproject `description`, profile blurb) if this touches packaging
```

- [ ] **Step 5: Verify the YAML parses**

Run:
```bash
python -c "import yaml; [yaml.safe_load(open(f)) for f in ['.github/ISSUE_TEMPLATE/bug_report.yml','.github/ISSUE_TEMPLATE/feature_request.yml','.github/ISSUE_TEMPLATE/config.yml']]; print('YAML OK')"
```
Expected: `YAML OK` (no traceback).

- [ ] **Step 6: Commit**

```bash
git add .github/ISSUE_TEMPLATE .github/PULL_REQUEST_TEMPLATE.md
git commit -m "chore: add org-default issue forms and PR template

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: CONTRIBUTING.md

**Files:**
- Create: `CONTRIBUTING.md` (repo root)

**Interfaces:**
- Produces: the "Contributing" link GitHub surfaces on every org repo's new-issue/new-PR pages and the repo sidebar.

- [ ] **Step 1: Create CONTRIBUTING.md**

Create `CONTRIBUTING.md`:

```markdown
# Contributing to Modern Python

Thanks for your interest in contributing! These guidelines apply across all
repositories in the [`modern-python`](https://github.com/modern-python) org
unless a repository overrides them with its own `CONTRIBUTING.md`.

## Ways to contribute

- **Report bugs** and **request features** via the issue templates.
- **Ask questions** in [GitHub Discussions](https://github.com/orgs/modern-python/discussions).
- **Improve docs** — typo fixes and clarifications are very welcome.
- **Send pull requests** — see the workflow below.

## Development setup

Projects use [`uv`](https://github.com/astral-sh/uv) for packaging,
[`ruff`](https://github.com/astral-sh/ruff) for lint/format,
[`ty`](https://github.com/astral-sh/ty) for type checking, and `uv_build` as the
build backend. Most repos expose tasks behind a `justfile`.

```bash
# Clone your fork, then from the repo root:
uv sync                 # install dependencies into a local venv
just --list             # see available tasks (lint, test, etc.) where a justfile exists
```

## Pull request workflow

1. Fork the repository and create a topic branch from `main`.
2. Make your change. Keep it focused — one logical change per PR.
3. Run lint, type check, and tests locally before pushing:
   ```bash
   uv run ruff check . && uv run ruff format --check .
   uv run ty check
   # run the project's test command (often `just test` or `uv run pytest`)
   ```
4. Update docs if you changed behavior or public API.
5. Open the PR using the template. Link the issue it resolves.

## CI note

GitHub occasionally type-checks a stale `refs/pull/<n>/merge` after a push, so a
PR can show an old lint/test failure that no longer matches the branch. Confirm
by running the failing check locally at the branch HEAD with the pinned tool
version; if it's clean, push a fresh commit to force GitHub to recompute the
merge ref.

## Code of Conduct

By participating you agree to abide by our
[Code of Conduct](CODE_OF_CONDUCT.md).
```

- [ ] **Step 2: Verify brand casing**

Run:
```bash
grep -n "LiteStar" CONTRIBUTING.md || echo "casing OK"
```
Expected: `casing OK`.

- [ ] **Step 3: Commit**

```bash
git add CONTRIBUTING.md
git commit -m "docs: add org-wide CONTRIBUTING guide

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: CODE_OF_CONDUCT.md

**Files:**
- Create: `CODE_OF_CONDUCT.md` (repo root)

**Interfaces:**
- Produces: the Code of Conduct GitHub links from every org repo; referenced by `CONTRIBUTING.md` and `SECURITY.md`.

- [ ] **Step 1: Create CODE_OF_CONDUCT.md (Contributor Covenant 2.1)**

Create `CODE_OF_CONDUCT.md` with the Contributor Covenant 2.1 text below. The
enforcement-contact paragraph is customized to use GitHub's private reporting
(no email is published).

```markdown
# Contributor Covenant Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone, regardless of age, body
size, visible or invisible disability, ethnicity, sex characteristics, gender
identity and expression, level of experience, education, socio-economic status,
nationality, personal appearance, race, caste, color, religion, or sexual
identity and orientation.

We pledge to act and interact in ways that contribute to an open, welcoming,
diverse, inclusive, and healthy community.

## Our Standards

Examples of behavior that contributes to a positive environment for our
community include:

* Demonstrating empathy and kindness toward other people
* Being respectful of differing opinions, viewpoints, and experiences
* Giving and gracefully accepting constructive feedback
* Accepting responsibility and apologizing to those affected by our mistakes,
  and learning from the experience
* Focusing on what is best not just for us as individuals, but for the overall
  community

Examples of unacceptable behavior include:

* The use of sexualized language or imagery, and sexual attention or advances of
  any kind
* Trolling, insulting or derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or email address,
  without their explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

## Enforcement Responsibilities

Community leaders are responsible for clarifying and enforcing our standards of
acceptable behavior and will take appropriate and fair corrective action in
response to any behavior that they deem inappropriate, threatening, offensive,
or harmful.

Community leaders have the right and responsibility to remove, edit, or reject
comments, commits, code, wiki edits, issues, and other contributions that are
not aligned to this Code of Conduct, and will communicate reasons for moderation
decisions when appropriate.

## Scope

This Code of Conduct applies within all community spaces, and also applies when
an individual is officially representing the community in public spaces.
Examples of representing our community include using an official email address,
posting via an official social media account, or acting as an appointed
representative at an online or offline event.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to the community leaders responsible for enforcement through GitHub's
private reporting (open the relevant repository's **Security** tab and choose
**Report a vulnerability**, which routes confidentially to the maintainers) or
by privately contacting a maintainer. All complaints will be reviewed and
investigated promptly and fairly.

All community leaders are obligated to respect the privacy and security of the
reporter of any incident.

## Enforcement Guidelines

Community leaders will follow these Community Impact Guidelines in determining
the consequences for any action they deem in violation of this Code of Conduct:

### 1. Correction

**Community Impact**: Use of inappropriate language or other behavior deemed
unprofessional or unwelcome in the community.

**Consequence**: A private, written warning from community leaders, providing
clarity around the nature of the violation and an explanation of why the
behavior was inappropriate. A public apology may be requested.

### 2. Warning

**Community Impact**: A violation through a single incident or series of
actions.

**Consequence**: A warning with consequences for continued behavior. No
interaction with the people involved, including unsolicited interaction with
those enforcing the Code of Conduct, for a specified period of time. This
includes avoiding interactions in community spaces as well as external channels
like social media. Violating these terms may lead to a temporary or permanent
ban.

### 3. Temporary Ban

**Community Impact**: A serious violation of community standards, including
sustained inappropriate behavior.

**Consequence**: A temporary ban from any sort of interaction or public
communication with the community for a specified period of time. No public or
private interaction with the people involved, including unsolicited interaction
with those enforcing the Code of Conduct, is allowed during this period.
Violating these terms may lead to a permanent ban.

### 4. Permanent Ban

**Community Impact**: Demonstrating a pattern of violation of community
standards, including sustained inappropriate behavior, harassment of an
individual, or aggression toward or disparagement of classes of individuals.

**Consequence**: A permanent ban from any sort of public interaction within the
community.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage],
version 2.1, available at
[https://www.contributor-covenant.org/version/2/1/code_of_conduct.html][v2.1].

Community Impact Guidelines were inspired by
[Mozilla's code of conduct enforcement ladder][Mozilla CoC].

For answers to common questions about this code of conduct, see the FAQ at
[https://www.contributor-covenant.org/faq][FAQ]. Translations are available at
[https://www.contributor-covenant.org/translations][translations].

[homepage]: https://www.contributor-covenant.org
[v2.1]: https://www.contributor-covenant.org/version/2/1/code_of_conduct.html
[Mozilla CoC]: https://github.com/mozilla/diversity
[FAQ]: https://www.contributor-covenant.org/faq
[translations]: https://www.contributor-covenant.org/translations
```

- [ ] **Step 2: Commit**

```bash
git add CODE_OF_CONDUCT.md
git commit -m "docs: add Contributor Covenant Code of Conduct

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: SECURITY.md + SUPPORT.md

**Files:**
- Create: `SECURITY.md` (repo root)
- Create: `SUPPORT.md` (repo root)

**Interfaces:**
- Produces: the "Security policy" and "Support" links GitHub surfaces org-wide. SECURITY.md is referenced by the CoC enforcement channel.

- [ ] **Step 1: Create SECURITY.md**

Create `SECURITY.md`:

```markdown
# Security Policy

## Reporting a vulnerability

Please **do not** open a public issue for security problems.

Report vulnerabilities privately using GitHub's built-in private reporting:
open the affected repository's **Security** tab and choose
**"Report a vulnerability"**. This routes confidentially to the maintainers.

Please include:

- the affected project and version,
- a description of the vulnerability and its impact,
- steps to reproduce or a proof of concept, if available.

We aim to acknowledge reports within a few days and will keep you informed as we
investigate and prepare a fix. Once a fix is released, we're happy to credit you
in the release notes unless you prefer to remain anonymous.

## Supported versions

Unless a repository states otherwise, security fixes target the **latest
released version** on PyPI. Upgrading to the latest release is the recommended
way to receive fixes.
```

- [ ] **Step 2: Create SUPPORT.md**

Create `SUPPORT.md`:

```markdown
# Support

Need help with a `modern-python` project? Here's where to go:

- **Documentation:** start at [modern-python.org](https://modern-python.org) and
  the project's own docs site (linked from each repo).
- **Questions & usage help:** ask in
  [GitHub Discussions](https://github.com/orgs/modern-python/discussions).
- **Bugs & feature requests:** open an issue in the relevant repository using the
  provided templates.
- **Security issues:** see [SECURITY.md](SECURITY.md) — please report privately,
  not in a public issue.

Please search existing issues and discussions before opening a new one — your
question may already be answered.
```

- [ ] **Step 3: Verify casing across both files**

Run:
```bash
grep -n "LiteStar" SECURITY.md SUPPORT.md || echo "casing OK"
```
Expected: `casing OK`.

- [ ] **Step 4: Commit**

```bash
git add SECURITY.md SUPPORT.md
git commit -m "docs: add org-wide security policy and support routing

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: FUNDING.yml (optional — needs one input)

**Files:**
- Create: `.github/FUNDING.yml`

**Interfaces:**
- Produces: the org-wide "Sponsor" button. **Requires one human input:** the GitHub Sponsors handle (or other funding platform). If the maintainer does not want a sponsor button, **skip this task entirely** and note the skip.

- [ ] **Step 1: Decide**

If the maintainer wants a sponsor button, get the GitHub Sponsors username (e.g. `lesnik512`) or other platform handle. If not, skip to "Commit (skip)" below and do not create the file.

- [ ] **Step 2: Create FUNDING.yml (only if a handle was provided)**

Create `.github/FUNDING.yml`, replacing `<github-sponsors-handle>` with the real handle:

```yaml
# Org-wide funding sources. Uncomment and fill the platforms you use.
github: [<github-sponsors-handle>]
# ko_fi: <ko-fi-handle>
# custom: ["https://modern-python.org"]
```

- [ ] **Step 3: Verify YAML parses (only if created)**

Run:
```bash
python -c "import yaml; yaml.safe_load(open('.github/FUNDING.yml')); print('YAML OK')"
```
Expected: `YAML OK`.

- [ ] **Step 4: Commit (or record skip)**

If created:
```bash
git add .github/FUNDING.yml
git commit -m "chore: add org-wide funding config

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```
If skipped: no commit; note "FUNDING.yml skipped — no sponsor handle" in the PR description.

---

## Task 6: Fix Litestar casing in docs/index.md

**Files:**
- Modify: `docs/index.md` (the two `LiteStar` occurrences, ~lines 60 and 66)

**Interfaces:**
- Produces: brand-consistent docs landing page. Independent of the community-health files; rides along in this PR as Phase 0 hygiene.

- [ ] **Step 1: Confirm the occurrences**

Run:
```bash
grep -n "LiteStar" docs/index.md
```
Expected: two lines (the `litestar-sqlalchemy-template` description and the `modern-di-litestar` line).

- [ ] **Step 2: Fix the casing**

Replace both `LiteStar` with `Litestar` in `docs/index.md`. After editing, run:
```bash
grep -n "LiteStar" docs/index.md || echo "casing OK"
```
Expected: `casing OK`.

- [ ] **Step 3: Commit**

```bash
git add docs/index.md
git commit -m "docs: fix Litestar casing on the landing page

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 7: Verify the site still builds

**Files:** none (verification only)

**Interfaces:**
- Consumes: all files added above. Confirms the root/`.github` community-health files do not leak into or break the published MkDocs site (which builds only from `docs/`).

- [ ] **Step 1: Build the docs site**

Run:
```bash
uv run mkdocs build --strict
```
Expected: build succeeds; output in `site/`. No errors. (Root-level `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, etc. are outside `docs/` and must NOT appear in `site/`.)

- [ ] **Step 2: Confirm community files did not get published**

Run:
```bash
ls site/CONTRIBUTING* site/CODE_OF_CONDUCT* 2>/dev/null && echo "LEAK — investigate" || echo "no leak"
```
Expected: `no leak`.

---

## Task 8: Open the PR (+ manual org settings)

**Files:** none (integration + PR)

**Interfaces:**
- Consumes: the full branch. Produces the PR that ships org-wide defaults.

- [ ] **Step 1: Push the branch**

```bash
git push -u origin chore/org-community-health
```

- [ ] **Step 2: Open the PR**

```bash
gh pr create --title "chore: add org-wide community-health defaults" --body "$(cat <<'EOF'
Adds default community-health files to the org \`.github\` repo so every repo
without its own inherits them: CONTRIBUTING, Code of Conduct (Contributor
Covenant 2.1), SECURITY (private vulnerability reporting), SUPPORT, issue forms
(bug/feature) + chooser, PR template, and FUNDING. Also fixes \`Litestar\`
casing on the docs landing page.

Implements Phase 0 (foundation hygiene) of the promotion strategy
(\`docs/superpowers/specs/2026-06-24-promotion-strategy-design.md\`).

Note: org-level Discussions must be enabled for the issue-chooser "Question"
contact link to resolve (see manual step).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 3: Manual org settings (maintainer action — record in PR)**

These are GitHub UI actions the maintainer performs; note them in the PR as a checklist:
- Enable **org-level Discussions**: Org → Settings → Discussions (so the issue-chooser "Question" link resolves). Pick a source repo if prompted.
- Confirm the new defaults appear on a repo that has none (e.g. open the new-issue page on `db-retry` — it should show the Bug/Feature chooser).

- [ ] **Step 4: Verify defaults propagate**

After merge, run:
```bash
gh api repos/modern-python/db-retry/community/profile --jq '.health_percentage'
```
Expected: a value well above the pre-change ~25% (the inherited CoC/Contributing/Security/templates count toward the score).

---

## Self-Review

**Spec coverage (Phase 0 portion):**
- Org-wide `.github` defaults — Tasks 1–5 (CONTRIBUTING, CoC, SECURITY, SUPPORT, ISSUE_TEMPLATE, PR template, FUNDING). ✅
- `LiteStar`→`Litestar` casing in `docs/index.md` — Task 6. ✅
- Enable Discussions — Task 8 manual step. ✅
- **Deferred to later plans (not in this plan, by design):** cross-repo PyPI metadata fixes (`that-depends`, `db-retry`, `eof-fixer`, `faststream-redis-timers`), the `faststream-outbox` readthedocs link, and all Phase 1/2 positioning + README content (those repos aren't in this workspace, and positioning is gated on Phase 1 research + maintainer sign-off). These become **Plan 2 (metadata hygiene sweep)** and **Plan 3 (positioning + READMEs)**.

**Placeholder scan:** The only intentional human input is the FUNDING.yml handle (Task 5), explicitly gated with a skip path — not a silent placeholder. No "TBD"/"handle edge cases"/"similar to" anywhere; every file's full content is inline.

**Type/name consistency:** File paths are consistent throughout (`.github/ISSUE_TEMPLATE/`, root-level docs). Cross-references resolve: `CONTRIBUTING.md`→`CODE_OF_CONDUCT.md`; `SUPPORT.md`→`SECURITY.md`; CoC enforcement→private reporting (matches `SECURITY.md`). Org Discussions URL identical in config.yml, CONTRIBUTING, SUPPORT.

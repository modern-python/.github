# docs-lockup-hero — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give each of the seven docs-site repos a centered, theme-aware
project-lockup hero on its docs home page, replacing the plain `# Title` H1.

**Spec:** [`design.md`](./design.md)

**Branch (per repo):** `feat/docs-lockup-hero`

**Commit strategy:** One commit per repo → one PR per repo. Pilot
(`that-depends`) is pushed, CI-green, and maintainer-merged **before** any
replication task starts.

## Global constraints

- Assets are **vendored** (copied into each repo's `docs/assets/`), never
  hotlinked — `mkdocs build --strict` must stay self-contained.
- All seven repos load `css/brand.css` as their last `extra_css` entry; the
  hero CSS is appended there.
- `alt` text uses the **kebab package name** (`that-depends`, not "That Depends")
  to match the lockup art. Do **not** add `title:` front matter — Material titles
  the home page from `site_name`, and adding `title:` duplicates it in the tab
  (`that-depends - that-depends`).
- The dark `<img>` is `aria-hidden="true"` with empty `alt`; only the light
  `<img>` carries the repo name, so the H1 has exactly one accessible name.
- Do not hide nav/toc; do not touch the header `logo`/`favicon`.
- Source lockups are already generated in this repo at
  `brand/projects/<repo>/lockup-light.svg` and `lockup-dark.svg` — do **not**
  regenerate.
- Every commit message ends with the trailer:
  `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`
- Working dir is `/Users/kevinsmith/src/pypi/modern-python`; sibling repos are
  at `../<repo>`. `gh` is authed.

---

## Shared snippets (referenced by every repo task)

### SNIPPET A — hero CSS (append verbatim to the repo's `docs/css/brand.css`)

```css

/* Centered project lockup hero on the docs home page */
.mp-hero {
  text-align: center;
  margin: 1.5rem 0 2.5rem;
}
.mp-hero .mp-lockup {
  margin: 0;
  font-size: 0;   /* collapse whitespace between the stacked <img> variants */
  line-height: 0;
}
.mp-hero .mp-logo {
  max-width: 420px;
  width: 70%;
  height: auto;
}
/* Light lockup by default; cream lockup in dark (slate) mode. */
.mp-hero .mp-logo--dark { display: none; }
[data-md-color-scheme="slate"] .mp-hero .mp-logo--light { display: none; }
[data-md-color-scheme="slate"] .mp-hero .mp-logo--dark  { display: inline; }
```

### SNIPPET B — hero block (top of `docs/index.md`, `<repo>` = kebab name)

```markdown
<div class="mp-hero" markdown>

<h1 class="mp-lockup">
<img class="mp-logo mp-logo--light" src="assets/lockup-light.svg" alt="<repo>">
<img class="mp-logo mp-logo--dark" src="assets/lockup-dark.svg" alt="" aria-hidden="true">
</h1>

</div>
```

### PROCEDURE P — standard per-repo rollout

Every repo task runs these steps. Only the three per-task **values** differ
(repo name; the `# <Title>` line to delete; whether a "Welcome to the `<repo>`
documentation!" line + its blank line are also deleted). Each task below states
those values and shows the exact resulting top of `index.md`.

- **P1** — branch: `cd ../<repo> && git switch -c feat/docs-lockup-hero`
  (verify clean tree first with `git -C ../<repo> status --porcelain`).
- **P2** — copy the two lockups:
  `cp brand/projects/<repo>/lockup-light.svg ../<repo>/docs/assets/lockup-light.svg`
  and `...lockup-dark.svg ../<repo>/docs/assets/lockup-dark.svg`.
- **P3** — edit `../<repo>/docs/index.md`: delete the `# <Title>` heading (and
  the "Welcome…" line where the task says so), and prepend SNIPPET B with
  `<repo>` substituted. Result must match the task's "resulting top".
- **P4** — append SNIPPET A to `../<repo>/docs/css/brand.css`.
- **P5** — build strict:
  `cd ../<repo> && uv pip install -r docs/requirements.txt && uv run mkdocs build --strict`.
  Expected: `Documentation built` with **no** warnings (strict fails on any).
- **P6** — visual check: `uv run mkdocs serve`, open `http://127.0.0.1:8000/`,
  confirm the lockup renders centered, the light variant shows by default and
  the cream variant after toggling to dark, the browser tab reads `<repo>`, and
  no project name is duplicated in the body. Stop the server.
- **P7** — commit, push, open PR, watch CI:
  ```bash
  cd ../<repo>
  git add docs/assets/lockup-light.svg docs/assets/lockup-dark.svg docs/index.md docs/css/brand.css
  git commit -m "docs: add project lockup hero to home page

  Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
  git push -u origin feat/docs-lockup-hero
  gh pr create --repo modern-python/<repo> --title "docs: add project lockup hero to home page" \
    --body "Replaces the plain \`# Title\` H1 on the docs home page with the centered, theme-aware project lockup. Assets vendored into docs/assets. See modern-python/.github planning bundle 2026-07-05.01-docs-lockup-hero.

  🤖 Generated with [Claude Code](https://claude.com/claude-code)"
  gh pr checks --repo modern-python/<repo> --watch
  ```
  Then **stop for maintainer review/merge** — do not merge.

---

### Task 1: Pilot — that-depends

**Files:**
- Create: `../that-depends/docs/assets/lockup-light.svg`, `../that-depends/docs/assets/lockup-dark.svg`
- Modify: `../that-depends/docs/index.md` (delete lines 1-4), `../that-depends/docs/css/brand.css` (append)

Establishes the exact pattern; every later repo task copies it.

**Per-task values:** repo=`that-depends`; delete `# That Depends`; delete the
`Welcome to the \`that-depends\` documentation!` line too.

**Resulting top of `docs/index.md`:**

```markdown
<div class="mp-hero" markdown>

<h1 class="mp-lockup">
<img class="mp-logo mp-logo--light" src="assets/lockup-light.svg" alt="that-depends">
<img class="mp-logo mp-logo--dark" src="assets/lockup-dark.svg" alt="" aria-hidden="true">
</h1>

</div>

`that-depends` is a python dependency injection framework which, among other things,
supports the following:
```

- [ ] **Step 1:** Run **P1** for `that-depends`.
- [ ] **Step 2:** Run **P2** for `that-depends`.
- [ ] **Step 3:** Run **P3** — apply the resulting top above.
- [ ] **Step 4:** Run **P4** (append SNIPPET A).
- [ ] **Step 5:** Run **P5** — `mkdocs build --strict`, expect no warnings.
- [ ] **Step 6:** Run **P6** — visual light/dark check.
- [ ] **Step 7:** Run **P7** — commit, push, open PR, `gh pr checks --watch`.
- [ ] **Step 8:** **GATE** — stop. Wait for maintainer review, CI green, and
      merge of the that-depends PR before starting any replication task.

---

### Task 2: Document the convention in this repo (.github)

**Files:**
- Modify: `architecture/brand-marks.md` (add a "Docs home page hero" subsection)
- Modify: `brand/README.md` (add one pointer sentence in the per-project marks section)
- Commit: the planning bundle `planning/changes/2026-07-05.01-docs-lockup-hero/`

Records the realized pattern in this repo. Do **after** Task 1 merges so the
prose describes what actually shipped.

- [ ] **Step 1:** Branch: `git switch -c feat/docs-lockup-hero` (on the
      `modern-python/.github` repo, current dir).

- [ ] **Step 2:** Append this subsection to `architecture/brand-marks.md`,
      immediately after the "### Lockup colourways and README banners" section:

  ```markdown

  ### Docs home page hero

  Repos with a live docs site also use the lockup as the home-page hero. The two
  `lockup-{light,dark}.svg` files are **vendored** into the repo's `docs/assets/`
  (unlike the README `<picture>`, which hotlinks `raw.githubusercontent.com`), and
  the leading `# <Title>` heading in `docs/index.md` is replaced by a centered
  `.mp-hero` block whose `<h1>` holds both `<img>` variants — light by default,
  cream under `[data-md-color-scheme="slate"]` — the same swap the org home page
  uses for its wordmark. Vendoring keeps `mkdocs build --strict` self-contained.
  The `.mp-hero` CSS lives in each repo's `docs/css/brand.css`.
  ```

- [ ] **Step 3:** In `brand/README.md`, in the "Per-project marks" section, after
      the paragraph describing README `<picture>` banners, add:

  ```markdown
  Docs-site repos also use these lockups as a centered hero on their
  `docs/index.md`, vendored into the repo's `docs/assets/` (see
  `architecture/brand-marks.md`).
  ```

- [ ] **Step 4:** Finalize the bundle `summary:` in `design.md` if the shipped
      pilot changed anything (it should not), then run `just check-planning`.
      Expected: `planning: OK`.

- [ ] **Step 5:** Commit, push, open PR:

  ```bash
  git add planning/changes/2026-07-05.01-docs-lockup-hero architecture/brand-marks.md brand/README.md
  git commit -m "docs(brand): docs home-page lockup hero convention + plan

  Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
  git push -u origin feat/docs-lockup-hero
  gh pr create --repo modern-python/.github --title "docs(brand): docs home-page lockup hero convention" \
    --body "Design + plan bundle for the per-project docs lockup hero rollout, plus the architecture/brand-README note recording the vendored-hero convention.

  🤖 Generated with [Claude Code](https://claude.com/claude-code)"
  gh pr checks --repo modern-python/.github --watch
  ```

---

### Task 3: lite-bootstrap

**Files:** Create `../lite-bootstrap/docs/assets/lockup-{light,dark}.svg`;
modify `../lite-bootstrap/docs/index.md`, `../lite-bootstrap/docs/css/brand.css`.

**Per-task values:** repo=`lite-bootstrap`; delete `# Lite Bootstrap`; delete the
`Welcome to the \`lite-bootstrap\` documentation!` line too.

**Resulting top of `docs/index.md`:**

```markdown
<div class="mp-hero" markdown>

<h1 class="mp-lockup">
<img class="mp-logo mp-logo--light" src="assets/lockup-light.svg" alt="lite-bootstrap">
<img class="mp-logo mp-logo--dark" src="assets/lockup-dark.svg" alt="" aria-hidden="true">
</h1>

</div>

`lite-bootstrap` assists you in creating applications with all the necessary instruments already set up.
```

- [ ] **Step 1:** Run **P1–P7** for `lite-bootstrap` with the values above.
- [ ] **Step 2:** Stop for maintainer review after PR CI is green.

---

### Task 4: httpware

**Files:** Create `../httpware/docs/assets/lockup-{light,dark}.svg`;
modify `../httpware/docs/index.md`, `../httpware/docs/css/brand.css`.

**Per-task values:** repo=`httpware`; delete `# httpware`. **No "Welcome" line
exists** — delete only the H1 and its blank line.

**Resulting top of `docs/index.md`:**

```markdown
<div class="mp-hero" markdown>

<h1 class="mp-lockup">
<img class="mp-logo mp-logo--light" src="assets/lockup-light.svg" alt="httpware">
<img class="mp-logo mp-logo--dark" src="assets/lockup-dark.svg" alt="" aria-hidden="true">
</h1>

</div>

A Python HTTP client framework with sync and async clients for building resilient service clients. `httpware` is a thin opinionated wrapper around `httpx2` — it re-exports `httpx2.Request`/`httpx2.Response` as the public request/response surface, adds a middleware chain (with a built-in resilience suite: `AsyncRetry`/`Retry` + `RetryBudget`, `AsyncBulkhead`/`Bulkhead`), opt-in typed response decoding, and a status-keyed exception tree raised automatically on 4xx/5xx.
```

- [ ] **Step 1:** Run **P1–P7** for `httpware` with the values above.
- [ ] **Step 2:** Stop for maintainer review after PR CI is green.

---

### Task 5: faststream-redis-timers

**Files:** Create `../faststream-redis-timers/docs/assets/lockup-{light,dark}.svg`;
modify `../faststream-redis-timers/docs/index.md`, `.../docs/css/brand.css`.

**Per-task values:** repo=`faststream-redis-timers`; delete
`# faststream-redis-timers`; delete the
`Welcome to the \`faststream-redis-timers\` documentation!` line too.

**Resulting top of `docs/index.md`:**

```markdown
<div class="mp-hero" markdown>

<h1 class="mp-lockup">
<img class="mp-logo mp-logo--light" src="assets/lockup-light.svg" alt="faststream-redis-timers">
<img class="mp-logo mp-logo--dark" src="assets/lockup-dark.svg" alt="" aria-hidden="true">
</h1>

</div>

`faststream-redis-timers` is a [FastStream](https://faststream.airt.ai) broker integration for Redis-backed distributed timer scheduling.
```

- [ ] **Step 1:** Run **P1–P7** for `faststream-redis-timers` with the values above.
- [ ] **Step 2:** Stop for maintainer review after PR CI is green.

---

### Task 6: faststream-outbox

**Files:** Create `../faststream-outbox/docs/assets/lockup-{light,dark}.svg`;
modify `../faststream-outbox/docs/index.md`, `.../docs/css/brand.css`.

**Per-task values:** repo=`faststream-outbox`; delete `# faststream-outbox`.
**No "Welcome" line exists** — delete only the H1 and its blank line. The first
paragraph is multi-line; keep it verbatim.

**Resulting top of `docs/index.md`:**

```markdown
<div class="mp-hero" markdown>

<h1 class="mp-lockup">
<img class="mp-logo mp-logo--light" src="assets/lockup-light.svg" alt="faststream-outbox">
<img class="mp-logo mp-logo--dark" src="assets/lockup-dark.svg" alt="" aria-hidden="true">
</h1>

</div>

`faststream-outbox` is a [FastStream](https://faststream.airt.ai) broker
integration for the **transactional outbox pattern** — a Postgres table is
the message queue. A producer writes a domain entity and an outbox row in
```
(…rest of the existing first paragraph unchanged.)

- [ ] **Step 1:** Run **P1–P7** for `faststream-outbox` with the values above.
- [ ] **Step 2:** Stop for maintainer review after PR CI is green.

---

### Task 7: semvertag

**Files:** Create `../semvertag/docs/assets/lockup-{light,dark}.svg`;
modify `../semvertag/docs/index.md`, `../semvertag/docs/css/brand.css`.

**Per-task values:** repo=`semvertag`; delete `# semvertag`. **No "Welcome" line
exists** — delete only the H1 and its blank line.

**Resulting top of `docs/index.md`:**

```markdown
<div class="mp-hero" markdown>

<h1 class="mp-lockup">
<img class="mp-logo mp-logo--light" src="assets/lockup-light.svg" alt="semvertag">
<img class="mp-logo mp-logo--dark" src="assets/lockup-dark.svg" alt="" aria-hidden="true">
</h1>

</div>

Auto-tag your GitLab repository with semantic version tags from CI —
one tool, two strategies.
```

- [ ] **Step 1:** Run **P1–P7** for `semvertag` with the values above.
- [ ] **Step 2:** Stop for maintainer review after PR CI is green.

---

### Task 8: modern-di (last — only once its branch is free)

**Files:** Create `../modern-di/docs/assets/lockup-{light,dark}.svg`;
modify `../modern-di/docs/index.md`, `../modern-di/docs/css/brand.css`.

**Per-task values:** repo=`modern-di`; delete `# Modern DI`; delete the
`Welcome to the \`modern-di\` documentation!` line too.

**Resulting top of `docs/index.md`:**

```markdown
<div class="mp-hero" markdown>

<h1 class="mp-lockup">
<img class="mp-logo mp-logo--light" src="assets/lockup-light.svg" alt="modern-di">
<img class="mp-logo mp-logo--dark" src="assets/lockup-dark.svg" alt="" aria-hidden="true">
</h1>

</div>

`modern-di` is a Python dependency injection framework which supports the following:
```

- [ ] **Step 1:** Confirm modern-di has no conflicting in-flight branch, then run
      **P1–P7** for `modern-di` with the values above.
- [ ] **Step 2:** Stop for maintainer review after PR CI is green.

---

## Self-review notes

- **Spec coverage:** design §1 (vendor assets) → P2; §2 (index hero, drop
  Welcome) → P3 + per-task resulting tops; §3 (CSS) → P4/SNIPPET A; §4 (docs
  in this repo) → Task 2; rollout order → Task 1 gate + Tasks 3-8 with modern-di
  last; testing → P5/P6; hotlink-vs-vendor risk → Global constraints.
- **Per-repo verified:** all seven load `css/brand.css`; "Welcome" line present
  in that-depends, lite-bootstrap, faststream-redis-timers, modern-di and
  absent in httpware, faststream-outbox, semvertag — matches each task.
- **No placeholders:** every task shows its exact resulting `index.md` top and
  exact commands.

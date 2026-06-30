# per-repo-social-cards — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate a 1280×640 social card (`og:image`) for each of the 7
docs-site repos — green mark panel + cream text panel — from `brand/build/`
into `brand/projects/<repo>/social-card.svg|png`.

**Spec:** [`design.md`](./design.md)

**Branch:** `brand-social-cards` (already created)

**Commit strategy:** Per-task commits.

## Global constraints

- **Card is 1280×640**, `viewBox="0 0 1280 640"`. Green panel `x ∈ [0,460)`
  (`GREEN_SURFACE`), cream panel `x ∈ [460,1280]` (`CREAM`).
- **Colours only from `brand/build/tokens.py`** — `GREEN_INK #356852`,
  `GREEN_SURFACE #2f5e4a`, `GOLD_LIGHT #c98a00`, `GOLD_DARK #f0b528`,
  `CREAM #f4f1e8`, plus a new `GREEN_MUTED` (tagline). No stray hex.
- Mark on the green panel uses the on-green colourway: `struct=CREAM`,
  `accent=GOLD_DARK`.
- **Taglines are the canonical `profile/README.md` one-liners**, verbatim, held
  in `projects.py::DOCS_REPOS`. `DOCS_REPOS` keys ⊆ `MANIFEST` keys.
- The 7 docs repos: `modern-di`, `that-depends`, `lite-bootstrap`, `httpware`,
  `faststream-redis-timers`, `faststream-outbox`, `semvertag`. No card for the
  other 10.
- All imports at module level; annotate function args; `# ty: ignore` not
  `# type: ignore`. CI gate is `just` (= `check-planning` + `pytest`); ruff is
  not a CI gate.
- Regenerate everything with `uv run python -m brand.build.render`.

---

### Task 1: GREEN_MUTED token

**Files:**
- Modify: `brand/build/tokens.py`
- Test: `tests/test_text.py` (or wherever token presence is asserted — if no such
  test exists, create `tests/test_tokens.py`)

**Interfaces:**
- Produces: `tokens.GREEN_MUTED = "#5b6f63"` (a desaturated green for tagline text
  on cream).

- [ ] **Step 1: Write the failing test**

  ```python
  # tests/test_tokens.py
  from brand.build import tokens as t

  def test_green_muted_present() -> None:
      assert t.GREEN_MUTED == "#5b6f63"
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `uv run pytest tests/test_tokens.py -q`
  Expected: FAIL — `AttributeError: module 'brand.build.tokens' has no attribute 'GREEN_MUTED'`.

- [ ] **Step 3: Add the token**

  Append to `brand/build/tokens.py`:

  ```python
  GREEN_MUTED = "#5b6f63"    # desaturated green for tagline text on cream
  ```

- [ ] **Step 4: Run test to verify it passes**

  Run: `uv run pytest tests/test_tokens.py -q`
  Expected: PASS.

- [ ] **Step 5: Commit**

  ```bash
  git add brand/build/tokens.py tests/test_tokens.py
  git commit -m "feat(brand): add GREEN_MUTED token for card taglines"
  ```

---

### Task 2: text fit + wrap helpers

**Files:**
- Modify: `brand/build/projects.py`
- Test: `tests/test_projects.py`

**Interfaces:**
- Consumes: `text.outline_text(text, size, *, x, baseline_y, anchor, color, letter_spacing) -> tuple[str, float]`
  (already exists; the float is the rendered width).
- Produces:
  - `_measure(text: str, size: float) -> float`
  - `fit_text(text: str, base_size: float, max_w: float, *, color: str, x: float, baseline_y: float) -> tuple[str, float]`
    — returns `(svg, used_size)`; `used_size < base_size` only when the text is
    wider than `max_w` at base.
  - `wrap_text(text: str, size: float, max_w: float) -> list[str]` — greedy
    word-wrap; a string that fits returns exactly one line.

- [ ] **Step 1: Write the failing test**

  ```python
  # append to tests/test_projects.py
  def test_fit_text_shrinks_only_when_needed() -> None:
      short_svg, short_size = p.fit_text("hi", 74, 700, color="#356852", x=0, baseline_y=0)
      assert short_size == 74  # fits, unchanged
      long_svg, long_size = p.fit_text("x" * 80, 74, 700, color="#356852", x=0, baseline_y=0)
      assert long_size < 74    # too wide -> shrunk
      assert "<g" in short_svg and "<g" in long_svg

  def test_wrap_text_splits_long_and_keeps_short() -> None:
      assert len(p.wrap_text("short tagline", 30, 700)) == 1
      assert len(p.wrap_text("word " * 60, 30, 700)) > 1
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `uv run pytest tests/test_projects.py -q -k "fit_text or wrap_text"`
  Expected: FAIL — `AttributeError` on `p.fit_text` / `p.wrap_text`.

- [ ] **Step 3: Implement the helpers**

  Add `from brand.build.text import outline_text` to the module-level imports of
  `brand/build/projects.py` if not already present (Task 8 of the marks change
  added it for lockups — confirm it's there; if so, do not duplicate). Then add:

  ```python
  def _measure(text: str, size: float) -> float:
      _, w = outline_text(text, size, x=0, baseline_y=0, anchor="start", color="#000000")
      return w


  def fit_text(
      text: str, base_size: float, max_w: float, *, color: str, x: float, baseline_y: float
  ) -> tuple[str, float]:
      """Render `text` left-anchored; shrink the font so its width fits max_w."""
      natural = _measure(text, base_size)
      size = base_size if natural <= max_w else base_size * max_w / natural
      svg, _ = outline_text(text, size, x=x, baseline_y=baseline_y, anchor="start", color=color)
      return svg, size


  def wrap_text(text: str, size: float, max_w: float) -> list[str]:
      """Greedy word-wrap to lines no wider than max_w."""
      lines: list[str] = []
      cur = ""
      for word in text.split():
          trial = (cur + " " + word).strip()
          if cur and _measure(trial, size) > max_w:
              lines.append(cur)
              cur = word
          else:
              cur = trial
      if cur:
          lines.append(cur)
      return lines
  ```

- [ ] **Step 4: Run tests to verify they pass**

  Run: `uv run pytest tests/test_projects.py -q -k "fit_text or wrap_text"`
  Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

  ```bash
  git add brand/build/projects.py tests/test_projects.py
  git commit -m "feat(brand): text fit + wrap helpers for cards"
  ```

---

### Task 3: DOCS_REPOS table + project_social_card

**Files:**
- Modify: `brand/build/projects.py`
- Test: `tests/test_projects.py`

**Interfaces:**
- Consumes: `geometry.project_frame`, `symbols.*` via `MANIFEST`, `tokens.*`,
  `fit_text`, `wrap_text` (Task 2), `GREEN_MUTED` (Task 1).
- Produces:
  - `DOCS_REPOS: dict[str, str]` — the 7 docs repos → canonical taglines.
  - `project_social_card(repo: str, *, tagline: str) -> str` — full 1280×640 `<svg>`.

- [ ] **Step 1: Write the failing test**

  ```python
  # append to tests/test_projects.py
  # (this file already imports: `re`, `pytest`, `minidom`, `Path`,
  #  `projects as p`, `tokens as t` — reuse them, do not re-import)

  DOCS_EXPECTED = {
      "modern-di", "that-depends", "lite-bootstrap", "httpware",
      "faststream-redis-timers", "faststream-outbox", "semvertag",
  }

  CARD_ALLOWED = {
      c.lower() for c in (
          t.GREEN_INK, t.GREEN_SURFACE, t.GOLD_LIGHT, t.GOLD_DARK, t.CREAM, t.GREEN_MUTED,
      )
  }

  def test_docs_repos_is_subset_of_manifest_and_exact() -> None:
      assert set(p.DOCS_REPOS) == DOCS_EXPECTED
      assert set(p.DOCS_REPOS) <= set(p.MANIFEST)

  @pytest.mark.parametrize("repo", sorted(DOCS_EXPECTED))
  def test_social_card_valid_and_palette(repo: str) -> None:
      svg = p.project_social_card(repo, tagline=p.DOCS_REPOS[repo])
      minidom.parseString(svg)
      assert 'viewBox="0 0 1280 640"' in svg
      hexes = {h.lower() for h in re.findall(r"#[0-9a-fA-F]{6}", svg)}
      assert hexes <= CARD_ALLOWED, f"{repo} stray colours: {hexes - CARD_ALLOWED}"

  def test_social_card_includes_url_and_name(repo: str = "modern-di") -> None:
      svg = p.project_social_card(repo, tagline=p.DOCS_REPOS[repo])
      assert f'aria-label="{repo}' in svg  # accessible label carries the repo
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `uv run pytest tests/test_projects.py -q -k "docs_repos or social_card"`
  Expected: FAIL — `AttributeError` on `p.DOCS_REPOS` / `p.project_social_card`.

- [ ] **Step 3: Implement DOCS_REPOS + project_social_card**

  Add to `brand/build/projects.py` (taglines are verbatim from
  `profile/README.md`):

  ```python
  DOCS_REPOS: dict[str, str] = {
      "modern-di": "powerful DI framework with scopes",
      "that-depends": "predecessor DI framework, still actively maintained",
      "lite-bootstrap": "lightweight package for bootstrapping new microservices",
      "httpware": "HTTP client framework with sync/async clients, middleware chain, and built-in resilience (retry, bulkhead)",
      "faststream-redis-timers": "FastStream broker integration for Redis-backed distributed timer scheduling",
      "faststream-outbox": "FastStream broker integration for the transactional outbox pattern with Postgres",
      "semvertag": "auto-tag your GitHub/GitLab repo with semantic version tags from CI",
  }

  _CARD_W = 1280
  _CARD_H = 640
  _PANEL = 460          # green panel width
  _TEXT_X = 520         # text column left edge
  _TEXT_W = 700         # text column width
  _NAME_BASE = 74
  _TAG_SIZE = 30
  _URL_SIZE = 26


  def project_social_card(repo: str, *, tagline: str) -> str:
      """1280x640 og:image: green mark panel + cream name/tagline/url panel."""
      panels = (
          f'<rect width="{_PANEL}" height="{_CARD_H}" fill="{t.GREEN_SURFACE}"/>'
          f'<rect x="{_PANEL}" width="{_CARD_W - _PANEL}" height="{_CARD_H}" fill="{t.CREAM}"/>'
      )
      frame = g.project_frame(struct=t.CREAM, accent=t.GOLD_DARK)
      inner = MANIFEST[repo]()
      mark = f'<g transform="translate(80,170) scale(3.0)">{frame}{inner}</g>'

      tag_lines = wrap_text(tagline, _TAG_SIZE, _TEXT_W)
      n = len(tag_lines)
      # block = name + 26 gap + n*38 tagline lines + 44 gap + url(30); centre vertically
      block_h = _NAME_BASE + 26 + n * 38 + 44 + 30
      top = (_CARD_H - block_h) / 2
      name_base = top + _NAME_BASE
      name_svg, _ = fit_text(repo, _NAME_BASE, _TEXT_W, color=t.GREEN_INK, x=_TEXT_X, baseline_y=name_base)
      y = name_base + 26
      tag_svg = ""
      for line in tag_lines:
          y += 38
          seg, _ = outline_text(line, _TAG_SIZE, x=_TEXT_X, baseline_y=y, anchor="start", color=t.GREEN_MUTED)
          tag_svg += seg
      y += 44
      url_svg, _ = outline_text(
          f"{repo}.modern-python.org", _URL_SIZE, x=_TEXT_X, baseline_y=y,
          anchor="start", color=t.GOLD_LIGHT, letter_spacing=2,
      )
      return (
          f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_CARD_W} {_CARD_H}" '
          f'role="img" aria-label="{repo} — {tagline}">'
          f"{panels}{mark}{name_svg}{tag_svg}{url_svg}</svg>"
      )
  ```

- [ ] **Step 4: Run tests to verify they pass**

  Run: `uv run pytest tests/test_projects.py -q -k "docs_repos or social_card"`
  Expected: PASS (subset check + 7 parametrized valid/palette + url/name).

- [ ] **Step 5: Commit**

  ```bash
  git add brand/build/projects.py tests/test_projects.py
  git commit -m "feat(brand): DOCS_REPOS + project_social_card composition"
  ```

---

### Task 4: render cards + wire into render_projects

**Files:**
- Modify: `brand/build/projects.py`
- Test: `tests/test_projects.py`

**Interfaces:**
- Consumes: `project_social_card`, `DOCS_REPOS`, `raster.export_png`,
  `render_projects` (existing).
- Produces: `render_projects` additionally writes
  `brand/projects/<repo>/social-card.svg` + `social-card.png` (1280×640) for the
  7 `DOCS_REPOS`, and for no other repo.

- [ ] **Step 1: Write the failing test**

  ```python
  # append to tests/test_projects.py
  def test_render_projects_writes_cards_for_docs_repos_only(tmp_path: Path) -> None:
      p.render_projects(out_dir=tmp_path)
      for repo in DOCS_EXPECTED:
          card = tmp_path / repo / "social-card.svg"
          assert card.is_file() and card.read_text(encoding="utf-8").startswith("<svg")
      non_docs = set(p.MANIFEST) - DOCS_EXPECTED
      for repo in non_docs:
          assert not (tmp_path / repo / "social-card.svg").exists()
  ```

- [ ] **Step 2: Run test to verify it fails**

  Run: `uv run pytest tests/test_projects.py -q -k cards_for_docs`
  Expected: FAIL — `social-card.svg` not written (no card pass yet).

- [ ] **Step 3: Add the card pass to `render_projects`**

  In `brand/build/projects.py`, inside `render_projects`'s `for repo in MANIFEST:`
  loop, after the existing `lockup.svg` write, add:

  ```python
          if repo in DOCS_REPOS:
              card = d / "social-card.svg"
              card.write_text(project_social_card(repo, tagline=DOCS_REPOS[repo]) + "\n", encoding="utf-8")
              export_png(card, d / "social-card.png", width=_CARD_W, height=_CARD_H)
  ```

- [ ] **Step 4: Run tests + full render**

  Run: `uv run pytest tests/test_projects.py -q`
  Expected: PASS.
  Run: `uv run python -m brand.build.render`
  Expected: no error. Verify:
  `ls brand/projects/modern-di/social-card.svg` exists;
  `ls brand/projects/modern-di-fastapi/social-card.svg` does NOT exist (non-docs).

- [ ] **Step 5: Commit**

  ```bash
  git add brand/build/projects.py tests/test_projects.py brand/projects
  git commit -m "feat(brand): render social cards for docs-site repos"
  ```

---

### Task 5: docs + finalize

**Files:**
- Modify: `brand/README.md`
- Modify: `architecture/brand-marks.md`
- Modify: `planning/changes/2026-06-30.01-per-repo-social-cards/design.md` (summary)

One sentence: document the new output and promote it into `architecture/`.

- [ ] **Step 1: Update `brand/README.md`**

  In the `## Per-project marks (brand/projects/)` subsection, add a sentence after
  the outputs line:

  ```markdown
  Repos with a docs site also get a `social-card.svg` + `social-card.png`
  (1280×640 og:image): the repo mark on a green panel beside its name, tagline,
  and docs URL on cream. The docs-site repos are listed in
  `brand/build/projects.py::DOCS_REPOS`.
  ```

- [ ] **Step 2: Update `architecture/brand-marks.md`**

  In the "Per-project marks" section, append:

  ```markdown
  Repos with a live docs site (`projects.py::DOCS_REPOS`, a subset of `MANIFEST`)
  additionally get a 1280×640 `social-card.svg|png` — a two-panel og:image
  (green mark panel + cream name/tagline/url), built with the same frame +
  symbols and the `fit_text`/`wrap_text` helpers. Taglines are the canonical
  `profile/README.md` one-liners.
  ```

- [ ] **Step 3: Finalize the bundle summary**

  Set the `summary:` in this bundle's `design.md` to the realized result, e.g.:
  `summary: Per-repo social cards shipped — 1280×640 two-panel og:image for the 7 docs-site repos, generated into brand/projects/<repo>/social-card.*`

- [ ] **Step 4: Normalize formatting + verify**

  Run: `uvx ruff format brand/build/ tests/` then `uvx ruff check brand/build/ tests/` (clean).
  Run: `uv run pytest -q` → all green.
  Run: `just check-planning` → `planning: OK`.
  Run: `uv run python -m brand.build.render` → no error.

- [ ] **Step 5: Commit**

  ```bash
  git add brand/README.md architecture/brand-marks.md planning/changes/2026-06-30.01-per-repo-social-cards/design.md brand/build tests
  git commit -m "docs(brand): document per-repo social cards"
  ```

---

## Notes for the executor

- After all tasks: push the branch and open a PR (do not local-merge); watch CI.
- This change only adds a card pass; do not alter the org marks, the existing
  per-project marks, or the lockups.
- Validate visually if unsure: `rsvg-convert brand/projects/<repo>/social-card.svg`
  to a PNG and eyeball — the geometry here is the version that passed visual
  review (short `modern-di`, medium `faststream-outbox`, long `httpware`).

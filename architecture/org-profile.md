# Org profile README

`profile/README.md` is the org landing page shown on
[github.com/modern-python](https://github.com/modern-python). Living prose, no
frontmatter; dated by git.

## Structure (top to bottom)

1. **Wordmark banner** — centered `<picture>` (light/dark) referencing
   `brand/org/wordmark[-dark].svg` by absolute `raw.githubusercontent.com` URL.
2. **Tagline** — one paragraph: what the org builds.
3. **Org-standards badge strip** — `uv`, `Ruff`, `ty` (Astral endpoint badges,
   live) and a static `coverage 100%` badge. The coverage claim holds org-wide
   because every repo's CI enforces a 100%-coverage guard; it renders unlinked
   (there is no org-level coverage URL).
4. **Four category tables** — `Project | What it is | Badges`, in order:
   **Project templates**, **Dependency injection**, **Microservices, HTTP & messaging**,
   **Utilities**. The `What it is` column carries the canonical ≤120-char one-liner
   (one of the three metadata surfaces kept consistent across GitHub
   description, pyproject `description`, and this blurb).

## Badge rules

- **Published libraries** get a four-badge strip: GitHub stars → stargazers,
  PyPI version, monthly downloads (`static.pepy.tech/badge/<pkg>/month`), and a
  Context7 docs badge → `context7.com/modern-python/<repo>`.
- **Templates** (`*-sqlalchemy-template`, not on PyPI) get stars + Context7 + a
  static `type: template` chip — no version/downloads columns, so no empty cells.
- All badges use flat (default) style so row heights align. Downloads use the
  pepy baked SVG, not the flaky shields `pypi/dm` endpoint. Every number is a
  live shield (no hand-typed stats that could go stale).
- PyPI distribution name equals the repo name for every package.

When a repo is added, removed, renamed, or unpublished, update the matching
table row here and in `profile/README.md` in the same PR.

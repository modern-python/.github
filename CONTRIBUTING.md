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

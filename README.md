# .github

Organization-level configuration and the public website for the
[Modern Python](https://github.com/modern-python) GitHub organization.

- **Website:** [modern-python.org](https://modern-python.org) — built from `docs/`
  with MkDocs + Material and deployed to GitHub Pages via
  [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) on every push to `main`.
- **Org profile:** [`profile/README.md`](profile/README.md) renders on the
  organization's GitHub landing page.
- **Deployment & domain setup:** see [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

## Local development

```bash
uv run mkdocs serve
```

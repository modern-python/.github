# .github

Organization-level configuration and the public website for the
[Modern Python](https://github.com/modern-python) GitHub organization.

The website, [modern-python.org](https://modern-python.org), is built from `docs/`
with MkDocs + Material and deployed to GitHub Pages via
[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) on every push to `main`.
The org profile, [`profile/README.md`](profile/README.md), renders on the
organization's GitHub landing page. Deployment and domain setup are covered in
[`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

## Local development

```bash
uv run mkdocs serve
```

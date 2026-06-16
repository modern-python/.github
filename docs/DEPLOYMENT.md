# Deployment & domain setup (owner-only)

The site builds and deploys automatically via `.github/workflows/deploy.yml` on
every push to `main`. The following one-time steps require registrar access and
the GitHub web UI.

## 1. Enable Pages from Actions

Repo → **Settings → Pages → Build and deployment → Source = GitHub Actions**.

## 2. DNS records at the `modern-python.org` registrar

Apex `A` records:

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

Apex `AAAA` records:

```
2606:50c0:8000::153
2606:50c0:8001::153
2606:50c0:8002::153
2606:50c0:8003::153
```

`www` subdomain `CNAME` → `modern-python.github.io`

## 3. Enforce HTTPS

After the first successful deploy and DNS propagation:
Repo → **Settings → Pages → tick "Enforce HTTPS"**.

## Notes

- Only one Pages site per org can claim the apex `modern-python.org`. This
  `.github` repo owns it — no other repo should set the same custom domain.
- The published custom domain is held by `docs/CNAME`; do not remove it.

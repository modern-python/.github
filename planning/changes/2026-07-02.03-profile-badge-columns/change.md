---
summary: Give the profile README tables a dedicated Stars column and drop the PyPI-version and Context7 badges, keeping Downloads.
---

# Change: profile README — Stars column, drop version + Context7 badges

## What & why

All four tables in `profile/README.md` currently use three columns —
`| Project | What it is | Badges |` — where the Badges cell packs several
shields together (Stars, PyPI version, Downloads, Context7; templates instead
carry Stars, Context7, and a Template chip). Pull **Stars** into its own column
and **remove the PyPI-version and Context7 badges**. The DI/services/utilities
tables become `| Project | What it is | Stars | Downloads |` (the fourth column,
now holding only the Downloads badge, is renamed from "Badges" to "Downloads").
The templates table becomes `| Project | What it is | Stars | Badges |`, its
Badges cell holding just the **Template chip** (templates have no Downloads
badge, so its fourth column keeps the "Badges" label). Requested to make the
star counts scannable in their own column and to declutter the badge cell.

## Scope

- One file: `profile/README.md`.
- Four tables: **Project templates**, **Dependency injection**,
  **Microservices, HTTP & messaging**, **Utilities**.
- All four tables: add a `Stars` third column (divider `|---|---|---|---|`) and
  move each row's `[![Stars]…]` badge into it; delete each row's `[![Context7]…]`
  badge.
- DI / services / utilities tables: header becomes
  `| Project | What it is | Stars | Downloads |`; also delete each row's
  `[![PyPI]…]` version badge, leaving the fourth cell holding only Downloads.
- Templates table: header becomes `| Project | What it is | Stars | Badges |`;
  its fourth cell holds only the Template chip (no PyPI badge existed).
- Leave every other badge, link, blurb, and row order untouched.

## Verification

- `just check-planning` prints `planning: OK`.
- `grep -c 'pypi/v/' profile/README.md` returns `0` (no version badges remain).
- `grep -ci context7 profile/README.md` returns `0` (no Context7 badges remain).
- Header lines: three read `| Project | What it is | Stars | Downloads |`
  (DI/services/utilities) and one reads `| Project | What it is | Stars | Badges |`
  (templates). All four dividers are `|---|---|---|---|`.
- Spot-check the rendered table columns are aligned and Downloads is still
  present in the Badges cell of the DI/services/utilities tables.
- No unrelated lines changed (`git diff` touches only `profile/README.md`).

## Notes

Pure Markdown/table formatting; no code, no tests, no brand assets. Independent
of the aiohttp brand change (2026-07-02.02) — ships as its own PR.

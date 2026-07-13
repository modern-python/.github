# Deferred

Real-but-unscheduled items, each with a revisit trigger. Add entries lazily.

## Coordinated launch (promotion strategy, Phase 4)

**What:** Fire the staggered launch — `modern-di` (Show HN + r/Python) → the
org-story announcement → `faststream-outbox` → `httpware`, roughly one per week.
The ready-to-post copy, the per-platform formats, and the timing/etiquette rules
are already written and kept in [`launch-playbook.md`](launch-playbook.md); the
rationale is in [`changes/2026-06-24.01-promotion-strategy.md`](changes/2026-06-24.01-promotion-strategy.md).

**Why deferred:** Phase 4 fires only once Phases 0–2 (foundation hygiene,
positioning backbone, conversion polish) are complete. Much of that has since
shipped — community-health defaults, the brand kit, the profile tables, the docs
sites — so this is close to ready.

**Revisit trigger:** when the maintainer judges the positioning surfaces done and
picks a launch window. Launching is a one-shot per project (greenfield: no prior
HN/Reddit/Lobsters threads exist for these projects), so it is worth not wasting.

## Community chat rooms (Telegram + Discord)

**What:** Open one org-wide Telegram group (Russian-speaking Python community)
and one Discord server (English/global), each with a mod/anti-spam bot, pinned
rules, and a pinned honest-status message. Link both from every README, docs
site, and the org profile, with a standing reflex to redirect *answerable*
questions to Discussions. Rationale and the two-room justification (a language/geo
split, the only rationale that keeps two rooms coherent rather than fragmenting a
small community) are in
[`changes/2026-06-27.01-community-channels.md`](changes/2026-06-27.01-community-channels.md).
Present-day truth — Discussions only, no rooms — is in `architecture/community.md`.

**Why deferred:** deliberately timed. The rooms open **during launch week, not
before**: an empty room opened months ahead actively hurts, because at the
highest-traffic moment every visitor sees "3 members, last message 2 weeks ago".
Launch traffic is what seeds them past the empty-room threshold.

**Revisit trigger:** the launch window above. Open the rooms as it starts. If a
room stays inactive 30 days post-launch, fold it back into Discussions rather
than keeping a dead room linked.

## Borrowed-audience channel program

**What:** Ongoing, no rooms to run: participate in the official Python Discord and
the FastAPI/Litestar/FastStream community channels; submit to **PyCoder's Weekly**
and **Python Weekly**; pitch **Talk Python to Me** / **Python Bytes** once docs are
polished; cross-post the org-story piece to dev.to / Hashnode with a canonical
link back; answer real DI/outbox questions on Stack Overflow. Ranked by ROI in
[`changes/2026-06-27.01-community-channels.md`](changes/2026-06-27.01-community-channels.md).

**Why deferred:** highest-ROI gap for a young project, but unscheduled — it is a
standing program rather than a task, and the newsletter/podcast pitches land best
alongside the launch.

**Revisit trigger:** newsletters and cross-posts at launch; podcasts once the docs
are polished enough to withstand the traffic.

## Zensical cutover for the docs sites

**What:** Replace Material for MkDocs with [Zensical](https://zensical.org)
(same team) as the builder for the org site and per-project docs sites.
Validated feasible against Zensical 0.0.46 on 2026-07-05: a `zensical.toml`
mirror of `mkdocs.yml` plus a one-block `overrides/main.html` tweak (dedupe the
homepage `<title>` by title text) builds the current site cleanly under both
builders. The spike branch was not kept — redo the port from `mkdocs.yml` when
revisiting.

**Why deferred:** Zensical is still pre-1.0 alpha (0.0.46 as of 2026-07-05, the
latest release) with known gaps versus our current setup.

**Revisit trigger — when Zensical reaches beta/1.0, re-check:**

1. **`page.is_homepage`** (and siblings) exposed to custom templates. Today it
   is undefined/falsy under Zensical; the spike works around it by deduping the
   homepage `<title>` by title text.
2. **`validation` parity** for the docs-heavy repos (e.g. `faststream-outbox`,
   which runs `mkdocs build --strict`): `omitted_files` / orphaned-page
   detection and `absolute_links` have **no** documented Zensical equivalent,
   and several Zensical validation keys are still marked deprecated. `--strict`
   itself and `invalid_links` / `invalid_link_anchors` do map.
3. **`classic` variant fidelity** — that the traditional Material look still
   matches the live site after the theme rewrite stabilizes.

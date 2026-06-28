---
summary: Which channels the modern-python org uses to reach, support, and retain users, and how they fit together.
---

# Modern Python — Community & Channels

**Scope:** Which channels the `modern-python` org uses to reach, support, and
retain users — and how they fit together. Extends the
[promotion strategy](../2026-06-24.01-promotion-strategy/design.md); **amends its Phase 5
deferral of Discord/Telegram.**

## Why this doc exists

The promotion strategy and launch playbook already specify the **broadcast**
channels (Show HN, r/Python, Lobsters, awesome-lists, the org-story post,
X/Mastodon/Bluesky one-liners). What they do *not* cover is **ongoing community
channels** and the broader channel landscape. The strategy deliberately deferred
real-time chat:

> Phase 5 — *"Deferred decision: Discord / Telegram only if Discussions demand
> justifies it — start GitHub-native."*
> Out of scope — *"Standing up Discord/Telegram up front."*

This doc revisits that decision on purpose, with a concrete plan and a stated
justification, and fills in the missing channel map.

## The mental model: three kinds of channel

The three categories have completely different cost/payoff profiles, and conflating
them is what leads to wasted effort.

1. **Broadcast (one-shot spikes).** HN, Reddit, Lobsters, awesome-lists, the
   org-story post. High impact, low ongoing cost, effectively single-use per
   project. **Already fully specified** in the launch playbook — out of scope here.
2. **Owned community (ongoing rooms we run).** GitHub Discussions, Telegram,
   Discord. High ongoing cost (presence + moderation); only pays off at critical
   mass.
3. **Borrowed audience (show up where users already are).** Existing Python chat
   communities, newsletters, podcasts, cross-post platforms, Q&A sites. Highest ROI
   for a small project, and **not yet in the strategy.**

**Strategic principle:** a 57★ project's scarcest resource is the attention needed
to seed a room. So **borrow audiences before building our own**, and make the one
*owned async* asset (GitHub Discussions) the durable, search-indexed backbone.

## Owned community channels

### GitHub Discussions — the backbone (start now)

Discussions is the primary support and feedback surface. It is searchable,
Google-indexed, async (a good fit for a solo maintainer in one timezone), and needs
no infrastructure. Every chat answer is ephemeral; every Discussion answer
compounds — it helps everyone who later searches the same error.

This elevates Discussions from the strategy's "seed it" framing to **primary support
surface**. Concrete actions (already partly in Phase 5): enable org-wide, seed Q&A /
Ideas categories, pin a "what should we build next?" roadmap thread, and route
launch-comment feedback here.

### Telegram + Discord — open at launch week, not before

We will run **both**, justified by a **language/geo split** — the only rationale
that keeps two rooms coherent rather than fragmenting a small community:

- **Telegram** — Russian-speaking Python community.
- **Discord** — English / global audience.

**Timing: open them during launch week, not earlier.** An empty room opened months
ahead actively hurts: during the highest-traffic moment (the Show HN spike), every
visitor sees "3 members, last message 2 weeks ago" — a worse signal than a clean
Discussions tab. Launch week is the one moment of concentrated attention; people who
arrive via HN/Reddit are the most likely to join, so that is when to seed the rooms
past the empty-room threshold. Opening cold afterward rarely catches up.

**Routing rule:** link both rooms from every README, docs site, and the org profile,
but push *answerable* questions to Discussions ("ask in Discussions so the next
person finds it; chat for everything else"). This keeps the durable, indexed record
growing and keeps chat low-stakes.

### Why both, and the cost we are accepting

Running two rooms doubles moderation/presence burden and is normally a trap for a
small project. We accept it **only** because the two rooms serve distinct
language communities that would not share one room anyway. If, in practice, one room
stays inactive, fold it back into Discussions rather than keeping a dead room linked.

## Borrowed-audience channels (the highest-ROI gap)

Ranked by ROI for a young Python OSS project. None of these require running a room.

1. **Existing Python chat communities.** Participate (tastefully, not drive-by
   self-promo) in the official **Python Discord** and the FastAPI / Litestar /
   FastStream community channels. Thousands of exact-fit users, zero maintenance.
2. **Newsletters — submit.** **PyCoder's Weekly** and **Python Weekly** both accept
   submissions; a single inclusion can out-perform a Show HN, and they suit the
   honest "when *not* to use this" framing already written for launch.
3. **Podcasts — pitch once docs are polished.** **Talk Python to Me** and
   **Python Bytes** cover new libraries; the "one DI wiring across FastAPI /
   FastStream / Typer" story is a natural fit.
4. **Cross-post platforms.** Republish the org-story post to **dev.to** / **Hashnode**
   with a canonical link back to the source, for a second SEO-friendly audience.
5. **Q&A sites.** Answer real DI / outbox questions on **Stack Overflow** and
   reference the docs where genuinely relevant.
6. **Conference lightning talks / PyCon.** Highest effort, optional, later.

## Low-grind upkeep model (solo maintainer)

To keep the owned rooms from becoming the "ongoing grind" the strategy warns
against:

- **One org-wide server each**, not per-repo: a single Discord with per-project
  channels, one Telegram group. The whole stack shares one community.
- **Spam control via a single mod bot** on Discord; an anti-spam bot on Telegram.
  Pinned **rules** + a pinned **"read first"** message on Discord.
- **A standing redirect reflex:** an answerable question → "let's move this to
  Discussions," so the durable record gets built and chat stays low-stakes.
- **Honest status pin:** these are young, actively-developed projects — matching the
  calibrated launch voice.

## How this fits the existing strategy

| Strategy phase | This doc's effect |
|---|---|
| Phase 4 — Coordinated launch | Telegram + Discord open in the **launch window**, seeded by launch traffic; rooms linked from launch assets. |
| Phase 5 — Sustain + feedback | **Amends** the Discord/Telegram deferral: both rooms ship (geo-split justified). Discussions elevated from "seed" to **primary support surface**. Adds the borrowed-audience channel program as ongoing work. |

## Success metrics

- **Discussions:** thread volume, answered-question rate, Ideas submissions.
- **Chat rooms:** members joined in launch week, weekly active posters, ratio of
  answerable questions redirected to Discussions. A room that stays inactive 30 days
  post-launch is a candidate to retire.
- **Borrowed audiences:** newsletter inclusions landed, podcast appearances, referral
  traffic from cross-posts / existing communities.

## Out of scope

- The broadcast channels and their copy — owned by the launch playbook.
- Per-repo chat servers (one org-wide server each instead).
- Paid promotion / ads.
- Standing up the rooms *before* launch week.

## Open questions (resolve during planning)

- Exact launch-week sequencing of room creation vs. the Show HN spike (maintainer's
  call on the window).
- Which mod/anti-spam bots to use for Discord and Telegram.
- Whether to retire one room if it stays inactive, and the threshold for that call.
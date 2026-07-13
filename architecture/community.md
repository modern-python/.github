# Community channels

How the org reaches, supports, and retains users. Living prose, no frontmatter;
dated by git.

## What exists today

**GitHub Discussions is the org's only owned channel**, and its primary support
and feedback surface. It exists at two levels:

- **Org-level** — [`/orgs/modern-python/discussions`](https://github.com/orgs/modern-python/discussions),
  backed by this `.github` repo. This is the catch-all forum, and the one
  [`SUPPORT.md`](../SUPPORT.md) routes every project's users to.
- **Per-repo** — enabled on `modern-di`, `that-depends`, and the three repos the
  launch promotes: `httpware`, `faststream-outbox`, `lite-bootstrap`. Deliberately
  **not** enabled org-wide: 20-odd empty Discussion tabs would read as a dead
  project, the same empty-room failure described below. A repo gets its own tab
  when it has traffic to fill it.

Only `that-depends` has real activity today; the other surfaces are seeded but
empty, and launch traffic is what is expected to fill them.

There is deliberately **no Discord and no Telegram room**: see
`planning/deferred.md`, which holds the plan to open them and the reason they are
not open yet.

## Why Discussions, and why nothing else yet

Discussions is searchable, Google-indexed, and async, which suits a solo
maintainer in one timezone. The durable-record argument is the load-bearing one: a
chat answer is ephemeral, while a Discussions answer compounds — it also serves
everyone who later searches the same error.

The standing principle is **borrow audiences before building our own**. A young
project's scarcest resource is the attention needed to seed a room, so the org
participates where Python users already are rather than standing up rooms it
cannot fill. An empty room is worse than no room: a visitor who arrives at a
"3 members, last message 2 weeks ago" tab gets a worse signal than from a clean
Discussions tab.

## Routing rule

When chat rooms do exist, *answerable* questions get pushed to Discussions
("ask in Discussions so the next person finds it; chat for everything else"), so
the indexed record keeps growing and chat stays low-stakes. The same reflex
applies to any question that arrives by another route today.

## Scope

One org-wide room per platform if and when rooms open — never per-repo. The whole
stack shares one community.

# GitHub Discussions is the org's only owned channel

**Decision:** Discussions is the org's sole owned support and feedback surface — org-level at
`/orgs/modern-python/discussions` (backed by this repo, and where `SUPPORT.md` routes every
project's users), plus per-repo tabs on the handful of repos with traffic to fill them. No Discord
server, no Telegram group, and no per-repo tab enabled org-wide. When an *answerable* question
arrives by any other route, it gets pushed to Discussions — "ask there so the next person finds it".

Chat rooms were the obvious alternative and are the one most often asked for. The durable-record
argument is the load-bearing reason against opening them now: a chat answer is ephemeral, while a
Discussions answer is searchable and Google-indexed, so it compounds — it also serves everyone who
later hits the same error. Async also suits a solo maintainer in one timezone.

The stronger reason is the empty-room threshold. A young project's scarcest resource is the
attention needed to seed a room, and an empty room is worse than no room: a visitor who lands on
"3 members, last message 2 weeks ago" gets a worse signal than from a clean Discussions tab. The same
arithmetic rejects enabling Discussions per-repo across all 28 repos — 20-odd empty tabs read as a
dead org. The standing principle is to **borrow audiences before building our own**: participate
where Python users already are rather than standing up rooms we cannot fill.

If rooms ever open, the scope is one org-wide room per platform, never per-repo. The whole stack
shares one community, and the only rationale that keeps two rooms coherent rather than fragmenting a
small one is a language/geo split (Russian-speaking Telegram, English/global Discord).

**Borrowing in practice:** a link back to our own pages is conditional, not standing. Link only
where the linked page actually answers the question at hand (a docs page, or an existing Discussion),
and never as a bare repo drop. The rejected alternative was a mandatory backlink on every reply: that
turns participation into the drive-by self-promotion HN, Lobsters and r/Python each punish, and costs
more standing than the referrals are worth. The obligation that *is* standing runs the other way,
when a question answered in someone else's venue exposes a gap in our docs, that gap becomes an issue
here.

**Revisit trigger:** launch week (the work is tracked in modern-python/.github#58). Rooms open *during* it, not before — launch traffic is what seeds
them past the empty-room threshold. If a room is still inactive 30 days post-launch, fold it back
into Discussions rather than keeping a dead room linked.

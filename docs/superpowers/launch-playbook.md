# Launch playbook (Phase 4)

Internal asset — **not published** (excluded from the site via `exclude_docs`).
Ready-to-post copy for the coordinated launch, plus timing and etiquette.

**Design principles**
- **Single-focus posts** on link aggregators (HN/Reddit/Lobsters) outperform one
  sprawling "look at my org" post. Stagger one project per week.
- **Greenfield:** research found no prior HN/Reddit/Lobsters threads for these
  projects, so each post gets a clean first thread.
- **Honest, calibrated voice:** "new but sharp," first-person (maintainer). The
  "when *not* to use this" framing is the credibility play — keep it.
- One equal-billing **announcement** carries the whole-stack story.

Suggested order: **modern-di (HN+Reddit)** → **stack announcement** →
**faststream-outbox** → **httpware**, ~one per week.

---

## 1. Show HN — modern-di (lead)

**Title:** `Show HN: modern-di – Typed dependency injection for Python, with scopes`

**Body:**

> Hi HN. I'm the author of modern-di, a dependency-injection framework for Python.
>
> I kept building a FastAPI API, a FastStream worker, and a Typer CLI that all shared the same business logic — and rewiring the same dependencies three times, once per entrypoint. modern-di is my attempt at *one* typed wiring shared across all of them.
>
> What it does:
> - **Type-based autowiring** — your constructor type hints *are* the graph; no `Provide[...]` markers or string keys.
> - **Explicit scopes** (APP → REQUEST → …) with **build-time** cycle- and scope-violation checks.
> - **Sync resolution by design** — async setup/teardown lives in the framework lifespan, not in resolution. This is deliberate and permanent, not a missing feature.
> - **Official integrations** for FastAPI, Litestar, FastStream, and Typer, plus a first-party pytest plugin that turns any dependency into a fixture.
> - Zero-dependency core, MIT, 100+ releases.
>
> Where it honestly stands:
> - If you're building a single FastAPI service and everything is request-scoped, FastAPI's `Depends` is enough — you don't need this.
> - The closest library is **Dishka**, which is more established, has many more integrations, and supports async resolution + custom scopes. If you need those, use Dishka. modern-di's bets are a simpler sync-only model, the first-party pytest plugin, and being one consistent small stack.
> - It's young but actively developed.
>
> Docs include a full comparison and a "do you even need a DI container?" page: https://modern-di.modern-python.org
> Repo: https://github.com/modern-python/modern-di
>
> Happy to dig into the design — especially the sync-only decision.

Etiquette: post Tue–Thu ~8–10am ET; never ask for upvotes; reply to every
comment; the honest "when not to use it" is what earns goodwill.

---

## 2. r/Python (Showcase format — three required sections)

**Title:** `modern-di – typed dependency injection with scopes and one wiring across FastAPI, Litestar, FastStream, and Typer`

**Body:**

> **What My Project Does**
> modern-di is a dependency-injection framework. You declare providers once (type-based autowiring from constructor hints), and resolve them with explicit scopes (APP → REQUEST → …) and build-time cycle/scope checks. The same container wires your FastAPI app, your FastStream workers, your Typer CLI, and your tests — via official integrations and a first-party pytest plugin that turns any dependency into a fixture. Sync resolution by design; async lives in the framework lifespan.
>
> **Target Audience**
> Python teams whose business logic runs behind *more than one entrypoint* (an API plus workers/CLIs) and who want one wiring instead of three. It's production-intended but young — early adopters welcome. If you have a single web service where everything is request-scoped, framework-native `Depends`/`Provide` is enough and modern-di is overkill.
>
> **Comparison**
> - **vs FastAPI `Depends` / Litestar `Provide`:** great inside one app, but don't span workers/CLIs or give typed app-scoped singletons; modern-di shares one wiring across all entrypoints.
> - **vs `dependency-injector`:** type-based autowiring instead of `Provide[...]` markers; nested request scopes; first-party pytest plugin.
> - **vs Dishka** (the closest library): Dishka is more established, has more integrations, and supports async resolution + custom scopes — pick it if you need those. modern-di bets on a simpler sync-only model and a first-party pytest plugin.
> - **vs `that-depends`** (my earlier framework): modern-di adds explicit scopes and drops global state; that-depends stays maintained for async resolution.
>
> Docs + comparison: https://modern-di.modern-python.org

---

## 3. Lobsters

Submit the link **https://modern-di.modern-python.org** (the docs, not the bare
repo), tag `python`. Authored comment:

> Typed DI for Python with explicit scopes, built so one container wires a FastAPI app, FastStream workers, and a Typer CLI together. Sync-only by design. The docs include an honest comparison vs dependency-injector/Dishka and a "do you even need DI?" section. Author here — happy to discuss the sync-only call.

Only post if you have a Lobsters account with karma; it's allergic to drive-by
self-promo.

---

## 4. Org-story announcement (equal billing)

For a blog / dev.to / GitHub Discussion "Announcements" post — the one place the
whole stack shares billing. Full ~580-word draft:

---

### The modern-python stack: production Python services without the boilerplate

Every production Python service I build needs roughly the same scaffolding. A
sensible project structure. A way to wire dependencies that doesn't turn into a
tangle. Resilient calls to other services. Reliable event publishing when a
database write and a message have to happen together. And observability, so I can
actually see what's happening in production.

None of that is the interesting part of the product — but all of it has to be
there, and getting it right repeatedly is tedious. Over the last couple of years
I've been factoring these concerns into a small family of MIT-licensed libraries,
each independently usable, built with the same tooling
([uv](https://github.com/astral-sh/uv), [ruff](https://github.com/astral-sh/ruff),
[ty](https://github.com/astral-sh/ty)). Collectively they're the *modern-python*
stack. Here's how the pieces fit.

**Start from a template.**
[`fastapi-sqlalchemy-template`](https://github.com/modern-python/fastapi-sqlalchemy-template)
and [`litestar-sqlalchemy-template`](https://github.com/modern-python/litestar-sqlalchemy-template)
are dockerized, batteries-included starting points: FastAPI or Litestar,
SQLAlchemy 2, PostgreSQL, dependency injection already wired, with linting,
typing, and tests configured. Clone, rename, and you have a service that runs —
instead of spending the first day assembling boilerplate.

**Wire your dependencies with [`modern-di`](https://modern-di.modern-python.org).**
The thing that tends to rot first in a growing service is dependency wiring.
modern-di is a typed DI container built around one idea: *one wiring shared across
every entrypoint.* The same container resolves dependencies in your FastAPI
handlers, your FastStream workers, and your Typer CLI — instead of three parallel
copies that drift apart. It uses type-based autowiring (your constructor hints are
the graph), explicit scopes with build-time validation, and a first-party pytest
plugin that turns any dependency into a fixture. It's deliberately sync-only:
async setup and teardown belong in the framework lifespan, not in resolution. If
you only have a single web service, your framework's own `Depends` is enough —
modern-di earns its place when you have a second entrypoint. (The docs include an
honest comparison with dependency-injector and Dishka, and a "do you even need
DI?" page.)

**Call other services with [`httpware`](https://httpware.modern-python.org).**
As soon as a service talks to other services, you need more than a bare HTTP
client. httpware wraps httpx with the things you'd otherwise assemble yourself:
typed errors (4xx/5xx become a status-keyed exception tree, no more
`raise_for_status`), typed response bodies (decode straight to your pydantic or
msgspec model), and resilience as composable middleware — retry with budget,
bulkhead, and circuit breaker, ordered explicitly.

**Publish events reliably with
[`faststream-outbox`](https://faststream-outbox.modern-python.org).**
If your service writes to a database and publishes an event, you have a dual-write
problem: a crash between the two leaves them inconsistent. faststream-outbox
solves it with the transactional outbox pattern for FastStream and Postgres —
write your domain row and an outbox row in the same transaction, and a relay
forwards each row to your broker (Kafka, RabbitMQ, NATS, Redis) with a single
decorator. At-least-once delivery, with a dead-letter option.

**Instrument everything with
[`lite-bootstrap`](https://lite-bootstrap.modern-python.org).**
Finally, observability. lite-bootstrap wires OpenTelemetry, Prometheus, Sentry,
and structlog into a FastAPI, Litestar, or FastStream service in a few lines —
each instrument opt-in, each skipped automatically if you don't configure it.
Consistent instrumentation across a fleet of services, without copy-pasting 150
lines of setup into every repo.

**Use one, or all of them.** The point isn't to adopt everything. Each library
stands alone — use httpware without modern-di, or lite-bootstrap with a framework
of your own. But together they cover the unglamorous 20% of a service that you'd
otherwise rebuild every time. [modern-python.org](https://modern-python.org) ties
it together, and everything is open to issues, ideas, and contributions. These are
young, actively-developed projects — I'd genuinely like your feedback on what's
missing.

---

## 5. Staggered follow-up posts (own thread each, later weeks)

- **Show HN: faststream-outbox** — "the transactional outbox pattern for
  FastStream + Postgres." Outbox is a respected, technical topic. Honest framing:
  the pattern is battle-tested, the library is ~weeks old.
- **Show HN / r/Python: httpware** — "httpx clients with typed errors + composable
  resilience (retry/bulkhead/circuit-breaker)." Resilience patterns draw
  discussion. Beta; pin versions.

(Reuse the modern-di structures above: HN = honest "what/where-it-stands";
r/Python = What-it-does / Target-audience / Comparison.)

## 6. awesome-list submissions (one-liners)

- **awesome-python** (DI section): `modern-di — typed dependency injection with scopes and framework integrations.`
- **awesome-fastapi**: `modern-di-fastapi — dependency injection for FastAPI via modern-di.`
- **awesome-asyncio / FastStream lists**: `faststream-outbox — transactional outbox for FastStream + Postgres.`

## 7. Social one-liners (X / Mastodon / Bluesky)

- "One typed DI wiring for your FastAPI app, FastStream workers, and Typer CLI — not three. modern-di, sync-by-design: https://modern-di.modern-python.org"
- "Dual-write problem in your event-driven service? faststream-outbox does the transactional outbox for FastStream + Postgres in one decorator."
- "httpx, but your 404s are typed exceptions and retry/bulkhead/circuit-breaker are composable middleware. httpware."

---

## Posting playbook (timing & etiquette)

- **Stagger** one launch item per week (modern-di → announcement →
  faststream-outbox → httpware). Greenfield, so each gets a clean first thread.
- **Don't** simultaneously cross-post the same project to HN + Reddit; space by a
  day or more.
- **Engage** every comment — that feedback is your Phase 5 roadmap input; route it
  to the modern-di **Ideas Discussion**.
- **HN/Reddit:** never solicit votes; lead with the honest "when *not* to use
  this." That candor is the credibility play.
- **Reddit r/Python:** follow the Showcase rules (the three required sections);
  post and engage, don't drop-and-run.

# Launch playbook (Phase 4)

Internal asset — **not published** (lives at the repo root, outside the MkDocs `docs/` tree).
Ready-to-post copy for the coordinated launch, plus timing and etiquette.

> **Facts checked 2026-07-13.** Every number and claim below was verified against
> PyPI, the GitHub API, and each repo's README on that date. Re-check before
> posting — HN and r/Python punish stale specifics, and these threads are
> one-shot. Current: `modern-di` 2.28.0 / 116 releases / 58★ / zero runtime deps /
> 13 integrations; `that-depends` 4.0.2 / 251★; `httpware` 0.15.1 (wraps
> **httpx2**, not httpx); `faststream-outbox` 0.10.5; `lite-bootstrap` 1.2.3.

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
> - **Type-based autowiring** — your constructor type hints *are* the graph, and providers are plain class attributes on a `Group`. There is no `@provide` decorator and no string keys. In the FastAPI, Litestar, FastStream and taskiq integrations your handlers need no DI decorator either — just the framework's own route decorator.
> - **Explicit scopes** (APP → REQUEST → …) with **build-time** cycle- and scope-violation checks.
> - **Async apps are first-class; the *resolve path* is synchronous.** `container.resolve(X)` never awaits — but the container is an async context manager, async finalizers are supported, and genuinely async resources (an `aiohttp` session, an `asyncpg` pool) are constructed in the framework lifespan and injected by type. Most of the integrations are async frameworks. Keeping `await` out of resolution is deliberate and permanent, not a missing feature.
> - **Official integrations** for FastAPI, Litestar, Starlette, Flask, aiohttp, FastStream, Celery, arq, taskiq, aiogram, gRPC, and Typer — plus a first-party pytest plugin that turns any dependency into a fixture.
> - Zero-dependency core, MIT, 116 releases.
>
> Where it honestly stands:
> - If you're building a single FastAPI service and everything is request-scoped, FastAPI's `Depends` is enough — you don't need this.
> - The closest library is **Dishka** — considerably more established (~1.2k stars to my ~60), with custom scopes and `await` inside resolution. modern-di deliberately takes the other road: an async resource (an `aiohttp` session, an `asyncpg` pool) is constructed in the framework lifespan and injected by type via a `ContextProvider`, so the resolve path stays synchronous. There's a recipe for exactly this: https://modern-di.modern-python.org/recipes/async-lifespan/
> - Integration coverage between the two is now roughly comparable. modern-di's bets are a lighter declaration model, a smaller core, the first-party pytest plugin, and being one consistent small stack.
>
> On the declaration model, precisely — because I'd rather state the limits than have them found: providers are plain class attributes, so there's no `@provide` anywhere, and in the FastAPI/Litestar/FastStream/taskiq integrations handlers need no DI decorator. But seven of the other integrations (Starlette, Flask, aiohttp, Celery, arq, aiogram, Typer) *do* need an `@inject`, and at the FastAPI boundary you still name the provider (`FromDI(Dependencies.user_service)`), because that's how FastAPI's own DI hooks in. So: lighter than Dishka on declarations, not "decorator-free."
> - It's young but actively developed, and deliberately conservative — the docs have a "design decisions" page for what it leaves out on purpose (auto-binding, in-package integrations, graph rendering).
>
> Docs include a full comparison and a "do you even need a DI container?" page: https://modern-di.modern-python.org
> Repo: https://github.com/modern-python/modern-di
>
> Happy to dig into the design — especially the decision to keep `await` out of the resolve path.

Etiquette: post Tue–Thu ~8–10am ET; never ask for upvotes; reply to every
comment; the honest "when not to use it" is what earns goodwill.

---

## 2. r/Python (Showcase format — three required sections)

**Title:** `modern-di – typed dependency injection with scopes and one wiring across FastAPI, Litestar, FastStream, Celery, and Typer`

**Body:**

> **What My Project Does**
> modern-di is a dependency-injection framework. You declare providers once (type-based autowiring from constructor hints), and resolve them with explicit scopes (APP → REQUEST → …) and build-time cycle/scope checks. The same container wires your FastAPI app, your FastStream workers, your Celery/arq/taskiq tasks, your Typer CLI, and your tests — via 13 official integrations and a first-party pytest plugin that turns any dependency into a fixture. Async apps are first-class — most of the integrations are async frameworks; what's synchronous is the *resolve path* itself, with async construction and teardown handled in the framework lifespan.
>
> **Target Audience**
> Python teams whose business logic runs behind *more than one entrypoint* (an API plus workers/CLIs) and who want one wiring instead of three. It's production-intended but young — early adopters welcome. If you have a single web service where everything is request-scoped, framework-native `Depends`/`Provide` is enough and modern-di is overkill.
>
> **Comparison**
> - **vs FastAPI `Depends` / Litestar `Provide`:** great inside one app, but don't span workers/CLIs or give typed app-scoped singletons; modern-di shares one wiring across all entrypoints.
> - **vs `dependency-injector`:** type-based autowiring instead of `Provide[...]` markers; nested request scopes; first-party pytest plugin.
> - **vs Dishka** (the closest library): Dishka is considerably more established (~1.2k stars), has custom scopes, and awaits inside resolution. modern-di takes the other road — async resources are built in the lifespan and injected by type through a `ContextProvider` ([recipe](https://modern-di.modern-python.org/recipes/async-lifespan/)), so resolution stays sync. Integration coverage is now roughly comparable. modern-di bets on a lighter declaration model (providers are plain class attributes — no `@provide`; and no `@inject` in the FastAPI/Litestar/FastStream/taskiq integrations, though seven others do need one), a smaller core, and a first-party pytest plugin.
> - **vs `that-depends`** (my earlier framework): modern-di adds explicit scopes and drops global state; that-depends remains the async-first sibling and stays maintained.
>
> Docs + comparison: https://modern-di.modern-python.org

---

## 3. Lobsters

Submit the link **https://modern-di.modern-python.org** (the docs, not the bare
repo), tag `python`. Authored comment:

> Typed DI for Python with explicit scopes, built so one container wires a FastAPI app, FastStream workers, and a Typer CLI together. Async apps are first-class; the resolve path itself never awaits, by design. The docs include an honest comparison vs dependency-injector/Dishka and a "do you even need DI?" section. Author here — happy to discuss the no-await-in-resolve call.

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
handlers, your FastStream workers, your Celery tasks, and your Typer CLI — instead
of four parallel copies that drift apart. Thirteen official integrations cover the
web frameworks (FastAPI, Litestar, Starlette, Flask, aiohttp), the task queues
(Celery, arq, taskiq), messaging, gRPC, and the CLI. It uses type-based autowiring
(your constructor hints are the graph), explicit scopes with build-time validation,
and a first-party pytest plugin that turns any dependency into a fixture. Async
applications are first-class — most of those integrations are async frameworks.
What is deliberately synchronous is the *resolve path*: a resource that genuinely
needs to `await` (an `aiohttp` session, an `asyncpg` pool) is constructed in the
framework lifespan and injected by type through a `ContextProvider`, so resolution
itself never awaits. If
you only have a single web service, your framework's own `Depends` is enough —
modern-di earns its place when you have a second entrypoint. (The docs include an
honest comparison with dependency-injector and Dishka, and a "do you even need
DI?" page.)

**Call other services with [`httpware`](https://httpware.modern-python.org).**
As soon as a service talks to other services, you need more than a bare HTTP
client. httpware is an HTTP client framework, with sync and async clients, built
on [httpx2](https://pypi.org/project/httpx2/). It supplies what you'd otherwise
assemble yourself: typed errors (4xx/5xx become a status-keyed exception tree, no
more `raise_for_status`), typed response bodies (decode straight to your pydantic
or msgspec model), and resilience as composable middleware — retry with budget,
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
Pyroscope, and structlog into a FastAPI, Litestar, FastStream, or FastMCP service
in a few lines — each instrument opt-in, each skipped automatically if you don't
configure it.
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
  the pattern is battle-tested, the library is young (first commit 2026-05-07,
  now 0.10.5 across 29 releases).
- **Show HN / r/Python: httpware** — "a Python HTTP client framework: sync + async
  clients on httpx2, with typed errors and composable resilience
  (retry/bulkhead/circuit-breaker)." Resilience patterns draw discussion. Still
  0.x — say so, and tell people to pin.

(Reuse the modern-di structures above: HN = honest "what/where-it-stands";
r/Python = What-it-does / Target-audience / Comparison.)

## 6. awesome-list submissions (one-liners)

- **awesome-python** (DI section): `modern-di — typed dependency injection with scopes and framework integrations.`
- **awesome-fastapi**: `modern-di-fastapi — dependency injection for FastAPI via modern-di.`
- **awesome-asyncio / FastStream lists**: `faststream-outbox — transactional outbox for FastStream + Postgres.`

## 7. Social one-liners (X / Mastodon / Bluesky)

- "One typed DI wiring for your FastAPI app, FastStream workers, Celery tasks, and Typer CLI — not four. modern-di, sync-by-design: https://modern-di.modern-python.org"
- "Dual-write problem in your event-driven service? faststream-outbox does the transactional outbox for FastStream + Postgres in one decorator."
- "An HTTP client framework where your 404s are typed exceptions and retry/bulkhead/circuit-breaker are composable middleware. Sync and async. httpware."

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

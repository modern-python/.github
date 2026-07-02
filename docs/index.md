---
title: Modern Python
hide:
  - navigation
  - toc
---

<div class="mp-hero" markdown>

<h1 class="mp-wordmark">
<img class="mp-logo mp-logo--light" src="assets/wordmark.svg" alt="Modern Python">
<img class="mp-logo mp-logo--dark" src="assets/wordmark-dark.svg" alt="" aria-hidden="true">
</h1>

Open-source templates and libraries for building production-ready Python
applications — web services, microservices, and the dependency injection that
wires them together.

</div>

<div class="grid cards" markdown>

-   :material-package-variant-closed:{ .lg .middle } __Project templates__

    ---

    Dockerized, batteries-included starting points for new web apps.

    [:octicons-arrow-right-24: Browse templates](#templates)

-   :material-needle:{ .lg .middle } __Dependency injection__

    ---

    The `modern-di` family of DI frameworks and integrations.

    [:octicons-arrow-right-24: Browse DI](#di)

-   :material-server-network:{ .lg .middle } __Microservices, HTTP & messaging__

    ---

    Bootstrapping, HTTP clients, and FastStream broker tooling.

    [:octicons-arrow-right-24: Browse services](#services)

-   :material-tools:{ .lg .middle } __Utilities__

    ---

    Small, focused helpers for everyday Python projects.

    [:octicons-arrow-right-24: Browse utilities](#utilities)

</div>

## The stack { #stack }

The modern-python projects fit together into one coherent stack for building
production Python services. Use one piece or all of them — each is independent.

- **Start from a template.**
  [`fastapi-sqlalchemy-template`](https://github.com/modern-python/fastapi-sqlalchemy-template)
  and [`litestar-sqlalchemy-template`](https://github.com/modern-python/litestar-sqlalchemy-template)
  give you a dockerized, batteries-included app — FastAPI or Litestar,
  SQLAlchemy 2, PostgreSQL, with dependency injection already wired.
- **Wire your dependencies** with
  [`modern-di`](https://github.com/modern-python/modern-di) — typed, scoped
  dependency injection with one wiring shared across FastAPI, Litestar,
  Starlette, aiohttp, FastStream, and Typer.
  ([`that-depends`](https://github.com/modern-python/that-depends), its
  production-proven predecessor, is still maintained.)
- **Call other services reliably** with
  [`httpware`](https://github.com/modern-python/httpware) — an httpx-based client
  with typed errors, typed response bodies, and a composable resilience chain
  (retry, bulkhead, circuit breaker).
- **Publish events reliably** with
  [`faststream-outbox`](https://github.com/modern-python/faststream-outbox) — the
  transactional outbox pattern for FastStream + PostgreSQL: write your domain row
  and outbox row in one transaction, relay to any broker with one decorator.
- **Instrument everything** with
  [`lite-bootstrap`](https://github.com/modern-python/lite-bootstrap) —
  OpenTelemetry, Prometheus, Sentry, and structlog wired into FastAPI, Litestar,
  or FastStream in a few lines.

Every project is built with the same tooling
([`uv`](https://github.com/astral-sh/uv), [`ruff`](https://github.com/astral-sh/ruff),
[`ty`](https://github.com/astral-sh/ty)) under the MIT license. Browse the full
catalog below.

## Project templates { #templates }

- [`fastapi-sqlalchemy-template`](https://github.com/modern-python/fastapi-sqlalchemy-template) — dockerized web application with DI on FastAPI, SQLAlchemy 2, PostgreSQL.
- [`litestar-sqlalchemy-template`](https://github.com/modern-python/litestar-sqlalchemy-template) — dockerized web application on Litestar, SQLAlchemy 2, PostgreSQL.

## Dependency injection { #di }

- [`modern-di`](https://github.com/modern-python/modern-di) — powerful DI framework with scopes.
- [`modern-di-aiohttp`](https://github.com/modern-python/modern-di-aiohttp) — `modern-di` integration for aiohttp.
- [`modern-di-fastapi`](https://github.com/modern-python/modern-di-fastapi) — `modern-di` integration for FastAPI.
- [`modern-di-faststream`](https://github.com/modern-python/modern-di-faststream) — `modern-di` integration for FastStream.
- [`modern-di-litestar`](https://github.com/modern-python/modern-di-litestar) — `modern-di` integration for Litestar.
- [`modern-di-pytest`](https://github.com/modern-python/modern-di-pytest) — `modern-di` integration for pytest.
- [`modern-di-starlette`](https://github.com/modern-python/modern-di-starlette) — `modern-di` integration for Starlette.
- [`modern-di-typer`](https://github.com/modern-python/modern-di-typer) — `modern-di` integration for Typer.
- [`that-depends`](https://github.com/modern-python/that-depends) — predecessor DI framework, still actively maintained.

## Microservices, HTTP & messaging { #services }

- [`lite-bootstrap`](https://github.com/modern-python/lite-bootstrap) — lightweight package for bootstrapping new microservices.
- [`httpware`](https://github.com/modern-python/httpware) — HTTP client framework with sync/async clients, middleware chain, and built-in resilience (retry, bulkhead).
- [`faststream-redis-timers`](https://github.com/modern-python/faststream-redis-timers) — FastStream broker integration for Redis-backed distributed timer scheduling.
- [`faststream-concurrent-aiokafka`](https://github.com/modern-python/faststream-concurrent-aiokafka) — concurrent message processing middleware for FastStream with `aiokafka`.
- [`faststream-outbox`](https://github.com/modern-python/faststream-outbox) — FastStream broker integration for the transactional outbox pattern with Postgres.

## Utilities { #utilities }

- [`db-retry`](https://github.com/modern-python/db-retry) — retry helpers for database operations.
- [`eof-fixer`](https://github.com/modern-python/eof-fixer) — automatically fix newlines at the end of files.
- [`semvertag`](https://github.com/modern-python/semvertag) — auto-tag your GitHub/GitLab repo with semantic version tags from CI.

<p class="mp-tagline">Built with <a href="https://github.com/astral-sh/uv">uv</a>,
<a href="https://github.com/astral-sh/ruff">ruff</a>, and
<a href="https://github.com/astral-sh/ty">ty</a>.</p>

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
  dependency injection with one wiring shared across web frameworks (FastAPI,
  Litestar, Starlette, Flask, aiohttp), task queues (Celery, arq, taskiq), RPC
  and messaging (gRPC, FastStream, aiogram), and CLIs (Typer).
  ([`that-depends`](https://github.com/modern-python/that-depends), the older
  DI framework, is still maintained.)
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
[`ty`](https://github.com/astral-sh/ty)) under the MIT license, to one shared
[standard](standard.md). Browse the full catalog below.

## Project templates { #templates }

- [`fastapi-sqlalchemy-template`](https://github.com/modern-python/fastapi-sqlalchemy-template): Dockerized FastAPI + SQLAlchemy 2 + PostgreSQL app template with DI
- [`litestar-sqlalchemy-template`](https://github.com/modern-python/litestar-sqlalchemy-template): Dockerized Litestar + SQLAlchemy 2 + PostgreSQL app template with DI
- [`chat-app`](https://github.com/modern-python/chat-app): Reference chat application for the modern-python organisation

## Dependency injection { #di }

!!! tip "Which one should I use?"

    Start new projects on [`modern-di`](https://github.com/modern-python/modern-di)
    — a minimal core plus the integrations listed below.

    [`that-depends`](https://github.com/modern-python/that-depends) is the earlier,
    async-first sibling and stays maintained. `modern-di` has migration guides
    [from `that-depends`](https://modern-di.modern-python.org/migration/from-that-depends/)
    and
    [from `dependency-injector`](https://modern-di.modern-python.org/migration/from-dependency-injector/).

- [`modern-di`](https://github.com/modern-python/modern-di): Powerful dependency-injection framework with IoC container and scopes
- [`modern-di-aiogram`](https://github.com/modern-python/modern-di-aiogram): modern-di integration for aiogram
- [`modern-di-aiohttp`](https://github.com/modern-python/modern-di-aiohttp): modern-di integration for aiohttp
- [`modern-di-arq`](https://github.com/modern-python/modern-di-arq): modern-di integration for arq
- [`modern-di-celery`](https://github.com/modern-python/modern-di-celery): modern-di integration for Celery
- [`modern-di-fastapi`](https://github.com/modern-python/modern-di-fastapi): modern-di integration for FastAPI
- [`modern-di-faststream`](https://github.com/modern-python/modern-di-faststream): modern-di integration for FastStream
- [`modern-di-flask`](https://github.com/modern-python/modern-di-flask): modern-di integration for Flask
- [`modern-di-grpc`](https://github.com/modern-python/modern-di-grpc): modern-di integration for gRPC
- [`modern-di-litestar`](https://github.com/modern-python/modern-di-litestar): modern-di integration for Litestar
- [`modern-di-pytest`](https://github.com/modern-python/modern-di-pytest): Pytest integration for modern-di that turns DI dependencies into fixtures
- [`modern-di-starlette`](https://github.com/modern-python/modern-di-starlette): modern-di integration for Starlette
- [`modern-di-taskiq`](https://github.com/modern-python/modern-di-taskiq): modern-di integration for taskiq
- [`modern-di-typer`](https://github.com/modern-python/modern-di-typer): modern-di integration for Typer
- [`that-depends`](https://github.com/modern-python/that-depends): Simple, typed dependency-injection framework for Python

## Microservices, HTTP & messaging { #services }

- [`lite-bootstrap`](https://github.com/modern-python/lite-bootstrap): Lightweight bootstrap for production-ready Python microservices
- [`httpware`](https://github.com/modern-python/httpware): Typed, resilient HTTP clients for Python, sync and async
- [`jwks-client`](https://github.com/modern-python/jwks-client): Async JWKS client for verifying JWTs, with key caching, resilient fetching, and Litestar and FastAPI integrations
- [`faststream-redis-timers`](https://github.com/modern-python/faststream-redis-timers): FastStream integration for Redis-backed distributed timer scheduling
- [`faststream-concurrent-aiokafka`](https://github.com/modern-python/faststream-concurrent-aiokafka): Concurrent message-processing middleware for FastStream + aiokafka
- [`faststream-outbox`](https://github.com/modern-python/faststream-outbox): FastStream transactional-outbox integration backed by a Postgres table

## Utilities { #utilities }

- [`compose2pod`](https://github.com/modern-python/compose2pod): Convert a Docker Compose file into a script that runs its services as a single Podman pod
- [`db-retry`](https://github.com/modern-python/db-retry): Retry helpers for PostgreSQL / SQLAlchemy database operations
- [`eof-fixer`](https://github.com/modern-python/eof-fixer): CLI tool that ensures text files end with exactly one newline
- [`release-scope`](https://github.com/modern-python/release-scope): Collect what sits between production and the default branch across GitLab services: tags, MRs, Jira keys, failed jobs
- [`semvertag`](https://github.com/modern-python/semvertag): Auto-tag GitHub & GitLab repos with semantic version tags from CI

<p class="mp-tagline">Built with <a href="https://github.com/astral-sh/uv">uv</a>,
<a href="https://github.com/astral-sh/ruff">ruff</a>, and
<a href="https://github.com/astral-sh/ty">ty</a>.</p>

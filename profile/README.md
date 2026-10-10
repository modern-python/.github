<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/modern-python/.github/main/brand/org/wordmark-dark.svg">
    <img alt="Modern Python" src="https://raw.githubusercontent.com/modern-python/.github/main/brand/org/wordmark.svg" width="360">
  </picture>
</p>

Open-source templates and libraries for building production-ready Python applications — web services, microservices, and the dependency injection that wires them together.

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

### Project templates

| Project | What it is | Stars |
|---|---|---|
| [`fastapi-sqlalchemy-template`](https://github.com/modern-python/fastapi-sqlalchemy-template) | Dockerized FastAPI + SQLAlchemy 2 + PostgreSQL app template with DI | [![Stars](https://img.shields.io/github/stars/modern-python/fastapi-sqlalchemy-template)](https://github.com/modern-python/fastapi-sqlalchemy-template/stargazers) |
| [`litestar-sqlalchemy-template`](https://github.com/modern-python/litestar-sqlalchemy-template) | Dockerized Litestar + SQLAlchemy 2 + PostgreSQL app template with DI | [![Stars](https://img.shields.io/github/stars/modern-python/litestar-sqlalchemy-template)](https://github.com/modern-python/litestar-sqlalchemy-template/stargazers) |
| [`chat-app`](https://github.com/modern-python/chat-app) | Reference chat application for the modern-python organisation | [![Stars](https://img.shields.io/github/stars/modern-python/chat-app)](https://github.com/modern-python/chat-app/stargazers) |

### Dependency injection

**Which one?** Start new projects on [`modern-di`](https://github.com/modern-python/modern-di) — a minimal core plus framework integrations, listed in [its docs](https://modern-di.modern-python.org/).

[`that-depends`](https://github.com/modern-python/that-depends) is the earlier, async-first sibling and stays maintained. `modern-di` has migration guides [from `that-depends`](https://modern-di.modern-python.org/migration/from-that-depends/) and [from `dependency-injector`](https://modern-di.modern-python.org/migration/from-dependency-injector/).

| Project | What it is | Stars | Downloads |
|---|---|---|---|
| [`modern-di`](https://github.com/modern-python/modern-di) | Powerful dependency-injection framework with IoC container and scopes | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di)](https://github.com/modern-python/modern-di/stargazers) | [![Downloads](https://static.pepy.tech/badge/modern-di/month)](https://pepy.tech/projects/modern-di) |
| [`that-depends`](https://github.com/modern-python/that-depends) | Simple, typed dependency-injection framework for Python | [![Stars](https://img.shields.io/github/stars/modern-python/that-depends)](https://github.com/modern-python/that-depends/stargazers) | [![Downloads](https://static.pepy.tech/badge/that-depends/month)](https://pepy.tech/projects/that-depends) |

### Microservices, HTTP & messaging

| Project | What it is | Stars | Downloads |
|---|---|---|---|
| [`lite-bootstrap`](https://github.com/modern-python/lite-bootstrap) | Lightweight bootstrap for production-ready Python microservices | [![Stars](https://img.shields.io/github/stars/modern-python/lite-bootstrap)](https://github.com/modern-python/lite-bootstrap/stargazers) | [![Downloads](https://static.pepy.tech/badge/lite-bootstrap/month)](https://pepy.tech/projects/lite-bootstrap) |
| [`httpware`](https://github.com/modern-python/httpware) | Typed, resilient HTTP clients for Python, sync and async | [![Stars](https://img.shields.io/github/stars/modern-python/httpware)](https://github.com/modern-python/httpware/stargazers) | [![Downloads](https://static.pepy.tech/badge/httpware/month)](https://pepy.tech/projects/httpware) |
| [`jwks-client`](https://github.com/modern-python/jwks-client) | Async JWKS client for verifying JWTs, with key caching, resilient fetching, and Litestar and FastAPI integrations | [![Stars](https://img.shields.io/github/stars/modern-python/jwks-client)](https://github.com/modern-python/jwks-client/stargazers) | [![Downloads](https://static.pepy.tech/badge/jwks-client/month)](https://pepy.tech/projects/jwks-client) |
| [`faststream-redis-timers`](https://github.com/modern-python/faststream-redis-timers) | FastStream integration for Redis-backed distributed timer scheduling | [![Stars](https://img.shields.io/github/stars/modern-python/faststream-redis-timers)](https://github.com/modern-python/faststream-redis-timers/stargazers) | [![Downloads](https://static.pepy.tech/badge/faststream-redis-timers/month)](https://pepy.tech/projects/faststream-redis-timers) |
| [`faststream-concurrent-aiokafka`](https://github.com/modern-python/faststream-concurrent-aiokafka) | Concurrent message-processing middleware for FastStream + aiokafka | [![Stars](https://img.shields.io/github/stars/modern-python/faststream-concurrent-aiokafka)](https://github.com/modern-python/faststream-concurrent-aiokafka/stargazers) | [![Downloads](https://static.pepy.tech/badge/faststream-concurrent-aiokafka/month)](https://pepy.tech/projects/faststream-concurrent-aiokafka) |
| [`faststream-outbox`](https://github.com/modern-python/faststream-outbox) | FastStream transactional-outbox integration backed by a Postgres table | [![Stars](https://img.shields.io/github/stars/modern-python/faststream-outbox)](https://github.com/modern-python/faststream-outbox/stargazers) | [![Downloads](https://static.pepy.tech/badge/faststream-outbox/month)](https://pepy.tech/projects/faststream-outbox) |

### Utilities

| Project | What it is | Stars | Downloads |
|---|---|---|---|
| [`compose2pod`](https://github.com/modern-python/compose2pod) | Convert a Docker Compose file into a script that runs its services as a single Podman pod | [![Stars](https://img.shields.io/github/stars/modern-python/compose2pod)](https://github.com/modern-python/compose2pod/stargazers) | [![Downloads](https://static.pepy.tech/badge/compose2pod/month)](https://pepy.tech/projects/compose2pod) |
| [`db-retry`](https://github.com/modern-python/db-retry) | Retry helpers for PostgreSQL / SQLAlchemy database operations | [![Stars](https://img.shields.io/github/stars/modern-python/db-retry)](https://github.com/modern-python/db-retry/stargazers) | [![Downloads](https://static.pepy.tech/badge/db-retry/month)](https://pepy.tech/projects/db-retry) |
| [`eof-fixer`](https://github.com/modern-python/eof-fixer) | CLI tool that ensures text files end with exactly one newline | [![Stars](https://img.shields.io/github/stars/modern-python/eof-fixer)](https://github.com/modern-python/eof-fixer/stargazers) | [![Downloads](https://static.pepy.tech/badge/eof-fixer/month)](https://pepy.tech/projects/eof-fixer) |
| [`release-scope`](https://github.com/modern-python/release-scope) | Collect what sits between production and the default branch across GitLab services: tags, MRs, Jira keys, failed jobs | [![Stars](https://img.shields.io/github/stars/modern-python/release-scope)](https://github.com/modern-python/release-scope/stargazers) | [![Downloads](https://static.pepy.tech/badge/release-scope/month)](https://pepy.tech/projects/release-scope) |
| [`semvertag`](https://github.com/modern-python/semvertag) | Auto-tag GitHub & GitLab repos with semantic version tags from CI | [![Stars](https://img.shields.io/github/stars/modern-python/semvertag)](https://github.com/modern-python/semvertag/stargazers) | [![Downloads](https://static.pepy.tech/badge/semvertag/month)](https://pepy.tech/projects/semvertag) |

### Support

If these projects save you time, consider supporting development on [Boosty](https://boosty.to/lesnik512).

[![Boosty](https://img.shields.io/badge/Boosty-support-f15f2c?logo=boosty&logoColor=white)](https://boosty.to/lesnik512)

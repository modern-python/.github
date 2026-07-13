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

### Dependency injection

**Which one?** Start new projects on [`modern-di`](https://github.com/modern-python/modern-di) — a minimal core plus the integrations below.

[`that-depends`](https://github.com/modern-python/that-depends) is the earlier, async-first sibling and stays maintained. Coming from it? `modern-di` ships a [migration guide](https://modern-di.modern-python.org/migration/from-that-depends/) — and one [from `dependency-injector`](https://modern-di.modern-python.org/migration/from-dependency-injector/).

| Project | What it is | Stars | Downloads |
|---|---|---|---|
| [`modern-di`](https://github.com/modern-python/modern-di) | Powerful dependency-injection framework with IoC container and scopes | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di)](https://github.com/modern-python/modern-di/stargazers) | [![Downloads](https://static.pepy.tech/badge/modern-di/month)](https://pepy.tech/projects/modern-di) |
| [`modern-di-aiogram`](https://github.com/modern-python/modern-di-aiogram) | modern-di integration for aiogram | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-aiogram)](https://github.com/modern-python/modern-di-aiogram/stargazers) | [![Downloads](https://static.pepy.tech/badge/modern-di-aiogram/month)](https://pepy.tech/projects/modern-di-aiogram) |
| [`modern-di-aiohttp`](https://github.com/modern-python/modern-di-aiohttp) | modern-di integration for aiohttp | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-aiohttp)](https://github.com/modern-python/modern-di-aiohttp/stargazers) | [![Downloads](https://static.pepy.tech/badge/modern-di-aiohttp/month)](https://pepy.tech/projects/modern-di-aiohttp) |
| [`modern-di-arq`](https://github.com/modern-python/modern-di-arq) | modern-di integration for arq | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-arq)](https://github.com/modern-python/modern-di-arq/stargazers) | [![Downloads](https://static.pepy.tech/badge/modern-di-arq/month)](https://pepy.tech/projects/modern-di-arq) |
| [`modern-di-celery`](https://github.com/modern-python/modern-di-celery) | modern-di integration for Celery | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-celery)](https://github.com/modern-python/modern-di-celery/stargazers) | [![Downloads](https://static.pepy.tech/badge/modern-di-celery/month)](https://pepy.tech/projects/modern-di-celery) |
| [`modern-di-fastapi`](https://github.com/modern-python/modern-di-fastapi) | modern-di integration for FastAPI | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-fastapi)](https://github.com/modern-python/modern-di-fastapi/stargazers) | [![Downloads](https://static.pepy.tech/badge/modern-di-fastapi/month)](https://pepy.tech/projects/modern-di-fastapi) |
| [`modern-di-faststream`](https://github.com/modern-python/modern-di-faststream) | modern-di integration for FastStream | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-faststream)](https://github.com/modern-python/modern-di-faststream/stargazers) | [![Downloads](https://static.pepy.tech/badge/modern-di-faststream/month)](https://pepy.tech/projects/modern-di-faststream) |
| [`modern-di-flask`](https://github.com/modern-python/modern-di-flask) | modern-di integration for Flask | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-flask)](https://github.com/modern-python/modern-di-flask/stargazers) | [![Downloads](https://static.pepy.tech/badge/modern-di-flask/month)](https://pepy.tech/projects/modern-di-flask) |
| [`modern-di-grpc`](https://github.com/modern-python/modern-di-grpc) | modern-di integration for gRPC | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-grpc)](https://github.com/modern-python/modern-di-grpc/stargazers) | [![Downloads](https://static.pepy.tech/badge/modern-di-grpc/month)](https://pepy.tech/projects/modern-di-grpc) |
| [`modern-di-litestar`](https://github.com/modern-python/modern-di-litestar) | modern-di integration for Litestar | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-litestar)](https://github.com/modern-python/modern-di-litestar/stargazers) | [![Downloads](https://static.pepy.tech/badge/modern-di-litestar/month)](https://pepy.tech/projects/modern-di-litestar) |
| [`modern-di-pytest`](https://github.com/modern-python/modern-di-pytest) | Pytest integration for modern-di — turn DI dependencies into fixtures | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-pytest)](https://github.com/modern-python/modern-di-pytest/stargazers) | [![Downloads](https://static.pepy.tech/badge/modern-di-pytest/month)](https://pepy.tech/projects/modern-di-pytest) |
| [`modern-di-starlette`](https://github.com/modern-python/modern-di-starlette) | modern-di integration for Starlette | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-starlette)](https://github.com/modern-python/modern-di-starlette/stargazers) | [![Downloads](https://static.pepy.tech/badge/modern-di-starlette/month)](https://pepy.tech/projects/modern-di-starlette) |
| [`modern-di-taskiq`](https://github.com/modern-python/modern-di-taskiq) | modern-di integration for taskiq | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-taskiq)](https://github.com/modern-python/modern-di-taskiq/stargazers) | [![Downloads](https://static.pepy.tech/badge/modern-di-taskiq/month)](https://pepy.tech/projects/modern-di-taskiq) |
| [`modern-di-typer`](https://github.com/modern-python/modern-di-typer) | modern-di integration for Typer | [![Stars](https://img.shields.io/github/stars/modern-python/modern-di-typer)](https://github.com/modern-python/modern-di-typer/stargazers) | [![Downloads](https://static.pepy.tech/badge/modern-di-typer/month)](https://pepy.tech/projects/modern-di-typer) |
| [`that-depends`](https://github.com/modern-python/that-depends) | Simple, typed dependency-injection framework for Python | [![Stars](https://img.shields.io/github/stars/modern-python/that-depends)](https://github.com/modern-python/that-depends/stargazers) | [![Downloads](https://static.pepy.tech/badge/that-depends/month)](https://pepy.tech/projects/that-depends) |

### Microservices, HTTP & messaging

| Project | What it is | Stars | Downloads |
|---|---|---|---|
| [`lite-bootstrap`](https://github.com/modern-python/lite-bootstrap) | Lightweight bootstrap for production-ready Python microservices | [![Stars](https://img.shields.io/github/stars/modern-python/lite-bootstrap)](https://github.com/modern-python/lite-bootstrap/stargazers) | [![Downloads](https://static.pepy.tech/badge/lite-bootstrap/month)](https://pepy.tech/projects/lite-bootstrap) |
| [`httpware`](https://github.com/modern-python/httpware) | Python HTTP client framework with sync & async clients and built-in resilience | [![Stars](https://img.shields.io/github/stars/modern-python/httpware)](https://github.com/modern-python/httpware/stargazers) | [![Downloads](https://static.pepy.tech/badge/httpware/month)](https://pepy.tech/projects/httpware) |
| [`faststream-redis-timers`](https://github.com/modern-python/faststream-redis-timers) | FastStream integration for Redis-backed distributed timer scheduling | [![Stars](https://img.shields.io/github/stars/modern-python/faststream-redis-timers)](https://github.com/modern-python/faststream-redis-timers/stargazers) | [![Downloads](https://static.pepy.tech/badge/faststream-redis-timers/month)](https://pepy.tech/projects/faststream-redis-timers) |
| [`faststream-concurrent-aiokafka`](https://github.com/modern-python/faststream-concurrent-aiokafka) | Concurrent message-processing middleware for FastStream + aiokafka | [![Stars](https://img.shields.io/github/stars/modern-python/faststream-concurrent-aiokafka)](https://github.com/modern-python/faststream-concurrent-aiokafka/stargazers) | [![Downloads](https://static.pepy.tech/badge/faststream-concurrent-aiokafka/month)](https://pepy.tech/projects/faststream-concurrent-aiokafka) |
| [`faststream-outbox`](https://github.com/modern-python/faststream-outbox) | FastStream transactional-outbox integration backed by a Postgres table | [![Stars](https://img.shields.io/github/stars/modern-python/faststream-outbox)](https://github.com/modern-python/faststream-outbox/stargazers) | [![Downloads](https://static.pepy.tech/badge/faststream-outbox/month)](https://pepy.tech/projects/faststream-outbox) |

### Utilities

| Project | What it is | Stars | Downloads |
|---|---|---|---|
| [`compose2pod`](https://github.com/modern-python/compose2pod) | Convert a Docker Compose file into a script that runs its services as a single Podman pod | [![Stars](https://img.shields.io/github/stars/modern-python/compose2pod)](https://github.com/modern-python/compose2pod/stargazers) | [![Downloads](https://static.pepy.tech/badge/compose2pod/month)](https://pepy.tech/projects/compose2pod) |
| [`db-retry`](https://github.com/modern-python/db-retry) | Retry helpers for PostgreSQL / SQLAlchemy database operations | [![Stars](https://img.shields.io/github/stars/modern-python/db-retry)](https://github.com/modern-python/db-retry/stargazers) | [![Downloads](https://static.pepy.tech/badge/db-retry/month)](https://pepy.tech/projects/db-retry) |
| [`eof-fixer`](https://github.com/modern-python/eof-fixer) | CLI tool that ensures text files end with exactly one newline | [![Stars](https://img.shields.io/github/stars/modern-python/eof-fixer)](https://github.com/modern-python/eof-fixer/stargazers) | [![Downloads](https://static.pepy.tech/badge/eof-fixer/month)](https://pepy.tech/projects/eof-fixer) |
| [`semvertag`](https://github.com/modern-python/semvertag) | Auto-tag GitHub & GitLab repos with semantic version tags from CI | [![Stars](https://img.shields.io/github/stars/modern-python/semvertag)](https://github.com/modern-python/semvertag/stargazers) | [![Downloads](https://static.pepy.tech/badge/semvertag/month)](https://pepy.tech/projects/semvertag) |

### Support

If these projects save you time, consider supporting development on [Boosty](https://boosty.to/lesnik512).

[![Boosty](https://img.shields.io/badge/Boosty-support-f15f2c?logo=boosty&logoColor=white)](https://boosty.to/lesnik512)

---
hide:
  - navigation
  - toc
---

<div class="mp-hero" markdown>

<svg class="mp-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 5.773 2.382" fill="currentColor" role="img" aria-label="Modern Python"><g transform="scale(0.000488) translate(696.3,2255.3) scale(1,-1)"><path transform="translate(0.0,0)" d="M131 0 456 1660 986 460 1535 1660 1827 0H1588L1439 932L982 -71L538 933L372 0Z"/><path transform="translate(2173.8,0)" d="M108 779Q108 1105 347 1339Q585 1573 919 1573Q1249 1573 1485 1337Q1722 1101 1722 770Q1722 437 1484 205Q1245 -28 907 -28Q608 -28 370 179Q108 408 108 779ZM343 776Q343 520 515 355Q686 190 910 190Q1153 190 1320 358Q1487 528 1487 772Q1487 1019 1322 1186Q1158 1354 916 1354Q675 1354 509 1186Q343 1020 343 776Z"/><path transform="translate(4208.6,0)" d="M185 0V1544H509Q742 1544 877 1498Q1022 1453 1140 1345Q1379 1127 1379 772Q1379 416 1130 196Q1005 86 868 43Q740 0 505 0ZM418 219H523Q680 219 784 252Q888 287 972 363Q1144 520 1144 772Q1144 1026 974 1184Q821 1325 523 1325H418Z"/><path transform="translate(5900.4,0)" d="M1037 1325H418V954H1019V735H418V219H1037V0H185V1544H1037Z"/><path transform="translate(7263.2,0)" d="M708 658 1186 0H901L460 632H418V0H185V1544H458Q764 1544 900 1429Q1050 1301 1050 1091Q1050 927 956.0 809.0Q862 691 708 658ZM418 835H492Q823 835 823 1088Q823 1325 501 1325H418Z"/><path transform="translate(8701.0,0)" d="M185 0V1649L1311 471V1544H1544V-94L418 1081V0Z"/></g><g transform="scale(0.000488) translate(1207.3,4183.0) scale(1,-1)"><path transform="translate(0.0,0)" d="M418 627V0H185V1544H449Q643 1544 742 1517Q842 1490 918 1415Q1051 1285 1051 1087Q1051 875 909.0 751.0Q767 627 526 627ZM418 843H505Q826 843 826 1090Q826 1329 495 1329H418Z"/><path transform="translate(1310.8,0)" d="M497 667 -7 1544H261L614 927L968 1544H1236L730 667V0H497Z"/><path transform="translate(2744.6,0)" d="M611 1325V0H378V1325H23V1544H965V1325Z"/><path transform="translate(3937.4,0)" d="M418 940H1084V1544H1317V0H1084V721H418V0H185V1544H418Z"/><path transform="translate(5644.2,0)" d="M108 779Q108 1105 347 1339Q585 1573 919 1573Q1249 1573 1485 1337Q1722 1101 1722 770Q1722 437 1484 205Q1245 -28 907 -28Q608 -28 370 179Q108 408 108 779ZM343 776Q343 520 515 355Q686 190 910 190Q1153 190 1320 358Q1487 528 1487 772Q1487 1019 1322 1186Q1158 1354 916 1354Q675 1354 509 1186Q343 1020 343 776Z"/><path transform="translate(7679.0,0)" d="M185 0V1649L1311 471V1544H1544V-94L418 1081V0Z"/></g><path fill="none" stroke="currentColor" stroke-width="0.07" d="M 0.035 0.550 L 0.035 0.035 L 0.550 0.035"/><path fill="none" stroke="currentColor" stroke-width="0.07" d="M 5.738 1.832 L 5.738 2.347 L 5.223 2.347"/></svg>

Open-source templates and libraries for building production-ready Python
applications — web services, microservices, and the dependency injection that
wires them together.

<p class="mp-tagline">Built with <a href="https://github.com/astral-sh/uv">uv</a>,
<a href="https://github.com/astral-sh/ruff">ruff</a>, and
<a href="https://github.com/astral-sh/ty">ty</a>.</p>

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

## Project templates { #templates }

- [`fastapi-sqlalchemy-template`](https://github.com/modern-python/fastapi-sqlalchemy-template) — dockerized web application with DI on FastAPI, SQLAlchemy 2, PostgreSQL.
- [`litestar-sqlalchemy-template`](https://github.com/modern-python/litestar-sqlalchemy-template) — dockerized web application on Litestar, SQLAlchemy 2, PostgreSQL.

## Dependency injection { #di }

- [`modern-di`](https://github.com/modern-python/modern-di) — powerful DI framework with scopes.
- [`modern-di-fastapi`](https://github.com/modern-python/modern-di-fastapi) — `modern-di` integration for FastAPI.
- [`modern-di-litestar`](https://github.com/modern-python/modern-di-litestar) — `modern-di` integration for Litestar.
- [`modern-di-faststream`](https://github.com/modern-python/modern-di-faststream) — `modern-di` integration for FastStream.
- [`modern-di-typer`](https://github.com/modern-python/modern-di-typer) — `modern-di` integration for Typer.
- [`modern-di-pytest`](https://github.com/modern-python/modern-di-pytest) — `modern-di` integration for pytest.
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

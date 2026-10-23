# Services

I'm Artur Shiriev, the maintainer of modern-python. Besides the open-source work, I help teams
with their Python backends: auditing a codebase, setting up observability and CI, modernizing
services, and leading the engineering side for a while.

The libraries stay free and MIT-licensed whether or not you hire me. You don't have to use them
either. When one fits, it saves time; when it doesn't, I work with what your team already runs.

## Engineering health audit { #audit }

For teams that inherited a codebase, are about to grow one, or keep fighting the same incidents.

I look at:

- recent outages and incidents, what caused them, and which ones keep coming back
- the defect backlog and the error tracker (Sentry, GlitchTip): which bugs matter and which can be
  closed
- logs, traces and metrics: what is collected, what is noise, and what is missing
- tech debt: outdated Python and packages, known vulnerabilities, test coverage, tests built on
  mocks, missing linters and type checks
- CI, the release process, and how a change reaches production
- the architecture diagrams, and whether they still match the code

You get a written report with findings ranked by impact and effort, a plan for the first fixes,
and a call to go through it with your team. The audit doesn't change your code; fixes are a
separate piece of work.

## Implementation sprints { #sprints }

Short, fixed-scope work that ends in merged pull requests in your repositories. Typical sprints:

- Observability. Structured logs, traces, metrics and error tracking in FastAPI, Litestar or
  FastStream services, usually with [`lite-bootstrap`](https://github.com/modern-python/lite-bootstrap),
  plus Grafana and Prometheus dashboards.
- Quality gates. A `justfile` whose lint and test tasks run the same way locally and in CI, with
  ruff, ty, coverage and dependency checks, along the lines of the org's own [standard](standard.md).
- A harness for coding agents. `AGENTS.md`, skills, CLI and MCP access to your error tracker, logs
  and metrics, and the hooks and CI checks that hold agent-written changes to the same bar as
  everyone else's.
- Modernization. Upgrading Python and dependencies, and introducing
  [`modern-di`](https://github.com/modern-python/modern-di) for dependency injection,
  [`httpware`](https://github.com/modern-python/httpware) for typed, resilient HTTP clients, or
  [`faststream-outbox`](https://github.com/modern-python/faststream-outbox) for reliable event
  publishing.
- Release process. Change requests, end-to-end tests built from test cases, and release scope
  collected automatically with [`release-scope`](https://github.com/modern-python/release-scope)
  and [`semvertag`](https://github.com/modern-python/semvertag).
- Architecture as code. A [LikeC4](https://likec4.dev) model of the current system, kept in the
  repo next to the code.

## Fractional tech lead { #tech-lead }

For teams without a tech lead, or between two. I join part-time and run the whole loop:

- one-on-ones with each engineer about what slows them down and what they want to work on
- regular outage and incident reviews that turn into prioritized follow-up tasks
- grooming the defect and tech-debt backlog
- the audit and sprints above, scheduled alongside product work

## Library support { #support }

For companies that run modern-python libraries in production: help with upgrades and migrations
(for example from `that-depends` or `dependency-injector` to `modern-di`), a review of how the
libraries are wired into your services, and help when an incident involves one of them.

## Get in touch { #contact }

Email [lesnik512@gmail.com](mailto:lesnik512@gmail.com) with a few lines about your team, your
stack, and what you'd like fixed. I'll reply with questions or a proposal for scope and timing.

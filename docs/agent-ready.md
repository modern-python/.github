# How the modern-python repos are set up for coding agents

modern-python is about thirty repositories, maintained by one person, with coding agents working
in every one of them. This page describes the setup that makes that workable, using the same four
parts as the [agent-ready backend](services.md#agent-ready) offer. Everything here is public and
linked, so you can check it.

## Context the agent can use { #context }

Every repo has an `AGENTS.md` at the root. It holds what an agent can't learn by reading the code:
the commands, where each concern lives, and the rules that leave no trace in the code that follows
them. [lite-bootstrap's](https://github.com/modern-python/lite-bootstrap/blob/main/AGENTS.md)
is a typical one. It explains why every link in `README.md` must be absolute (the README is also
the PyPI description, and PyPI doesn't rewrite relative links), and it lists four code style rules,
each with the reason behind it.

Most repos also carry a `CONTEXT.md`, a glossary limited to terms with a synonym to reject or a
meaning subtle enough that code and docs have to agree on it. Each entry names the words to avoid.
In [lite-bootstrap's](https://github.com/modern-python/lite-bootstrap/blob/main/CONTEXT.md), an
instrument being *configured* and a bootstrapper being *ready* are separate terms, and the agent is
told to use them exactly.

Decisions go into architecture decision records under `docs/adr/`, 88 of them across the repos. A
short [domain doc](https://github.com/modern-python/lite-bootstrap/blob/main/docs/agents/domain.md)
tells the agent to read the ADRs for the area it is changing, and to say so when its change
contradicts one instead of quietly overriding it. Two more docs in the same folder describe the
issue tracker and the triage labels, so an agent can pick up and file GitHub issues through `gh`.

Above the repos sits the [standard](standard.md): numbered requirements, each with a stable ID and
usually a *Why* line. An agent can cite [CI9](standard.md#CI9) in a pull request the same way a
person would.

## Checks for agent-written code { #checks }

An agent's change goes through the same checks as anyone's, and the commands are identical
locally and in CI:

- The `justfile` has a fixed set of recipes ([JF1](standard.md#JF1)). `just lint` rewrites files,
  and `just lint-ci` runs the same checks read-only.
- ruff, ty and eof-fixer, required by the standard ([TL2](standard.md#TL2)), with a 100% line
  coverage gate ([TS2](standard.md#TS2)). A `pragma: no cover` should carry its reason on the same
  line ([TS6](standard.md#TS6)).
- The `floors` job installs every dependency at its lowest declared version and runs the suite
  ([CI10](standard.md#CI10)), which catches code that only works on the latest release.
- A links job fails on any relative link or file path the diff broke ([CI7](standard.md#CI7)), and
  docs sites build with `mkdocs build --strict` ([CI8](standard.md#CI8)).
- A shared check fails when a file cites an ADR that doesn't exist ([CI9](standard.md#CI9)).

Some rules are tests. The org repo's
[`tests/test_site.py`](https://github.com/modern-python/.github/blob/main/tests/test_site.py)
asserts that the site's project lists match the brand manifest, and each test's docstring opens
with `INVARIANT:` and explains what breaks without it. An agent that removes the check has to argue
with the reason in front of it.

## Signals from outside the diff { #signals }

Libraries don't have a production environment, so this part is thin here. The closest thing is a
daily scheduled run of each published repo's checks ([CI2](standard.md#CI2)). When a dependency release or a
new Python breaks a repo, a
[shared workflow](https://github.com/modern-python/.github/blob/main/.github/workflows/report-scheduled-failure.yml)
opens or updates an issue linking the failing run, and an agent can pick that issue up like any
other.

## Telemetry { #telemetry }

The same applies to telemetry: a library has none of its own. For services, the org's answer is
[`lite-bootstrap`](https://github.com/modern-python/lite-bootstrap), which wires OpenTelemetry,
Prometheus, Sentry and structlog into FastAPI, Litestar or FastStream. In a client's service, this
part and the one above carry more weight than they do here.

## What we learned { #lessons }

Copies drift, even byte-identical ones. Twenty-five copies of the ADR citation test drifted within
a month of being written, so the repos now fetch one shared file from the org repo, unpinned
([CI9](standard.md#CI9)). Per-repo scripts that reported scheduled failures drifted the same way,
and several named a dependency their repo didn't have. They were replaced by one shared workflow
([CI2](standard.md#CI2)).

Not everything should be shared. A single CI workflow for all repos was built and rejected
([#95](https://github.com/modern-python/.github/issues/95)): reusable workflow inputs are plain
strings, so service containers and environment maps had to be flattened into them. Each repo keeps
its own `_checks.yml` ([CI3](standard.md#CI3)), and a change to the jobs is a sweep across repos.

Write down only what the code doesn't show. Agents read code well. What they miss is the reason a
link must be absolute, why a type checker's warning is noise, or which word the project has already
rejected, and that is what the `AGENTS.md` and `CONTEXT.md` files hold.

If you'd like the same setup in your own codebase, see [services](services.md#agent-ready).

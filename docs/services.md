# Services

I'm Artur Shiriev, the maintainer of modern-python. Besides the open-source work, I help Python
backend teams that use coding agents keep production stable: I make the codebase easier for agents
to work in, review where delivery stands, and lock down what agents can reach.

The libraries stay free and MIT-licensed whether or not you hire me. You don't have to use them
either. When one fits, it saves time; when it doesn't, I work with what your team already runs.

## Agent-ready backend { #agent-ready }

For teams where coding agents write a growing share of the code. A fixed-scope sprint that ends in
merged pull requests in your repositories:

- Context the agent can use. `AGENTS.md`, skills, and architecture rules written where the agent
  reads them and checked in CI, with a [LikeC4](https://likec4.dev) model of the system when the
  boundaries need one.
- Checks for agent-written code. Lint, type, test and coverage gates plus structural tests and
  hooks, run the same way locally and in CI, along the lines of the org's own
  [standard](standard.md).
- Access to production signals. CLI and MCP access to your error tracker, logs, metrics and traces,
  so an agent can check a change against how the service actually behaves.
- Telemetry worth querying. Structured logs, traces, metrics and error tracking in FastAPI, Litestar
  or FastStream services, usually with
  [`lite-bootstrap`](https://github.com/modern-python/lite-bootstrap), so people and agents can
  debug from the same data.

The [modern-python repos](agent-ready.md) run on the same setup, minus the production parts.

## Delivery health check { #audit }

A short, fixed-scope review, and a good first step before a sprint. Automated scanners for
dependencies, vulnerabilities and code smells run first, and I treat what they find as raw input.
Most of the time goes to what the tools can't see:

- recent outages and incidents, what caused them, and which ones keep coming back
- whether your logs, traces and metrics are good enough to debug from, for people and for agents
- whether code review keeps up with how much code the agents produce, and how deployment
  frequency, change failure rate and time to restore have moved since the team adopted them
- CI, the release process, and how a change reaches production
- whether the architecture docs still match the code

You get a written report with findings ranked by impact and effort, a plan for the first fixes, and
a call to go through it with your team. The review doesn't change your code. When it calls for
design changes, such as dependency injection with
[`modern-di`](https://github.com/modern-python/modern-di), a transactional outbox with
[`faststream-outbox`](https://github.com/modern-python/faststream-outbox), or resilient HTTP clients
with [`httpware`](https://github.com/modern-python/httpware), I can make them as follow-up work.

## Agent security and governance { #governance }

For teams rolling coding agents out beyond a few early users, or unsure what the agents can touch:

- a usage policy: which tools and repositories, which changes need human review, and the size and
  test requirements for agent pull requests
- permissions: which commands agents may run, which secrets and tokens are within their reach, and
  whether anything reaches production
- MCP servers and other integrations: which to trust and what data they see
- prompt injection through issues, pull requests, docs and CI, wherever agents read text they
  didn't write
- a rollout plan: one team first, then wider once the guardrails hold

## Library support { #support }

If you run modern-python libraries in production, I can help with migrations (for example from
`that-depends` or `dependency-injector` to `modern-di`) and with incidents that involve one of
them.

## Get in touch { #contact }

Email [lesnik512@gmail.com](mailto:lesnik512@gmail.com) with a few lines about your team, your
stack, and what you'd like fixed. I'll reply with questions or a proposal for scope and timing.

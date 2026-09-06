# Project marks are two-colour, differentiated by symbol not colour

**Decision:** Every per-project mark uses the constant green+gold snake frame with a single **gold**
inner symbol. Projects are told apart by the *shape* of the inner symbol, never by colour. There is
no per-family accent hue.

While designing the per-project system we evaluated giving each of the four families its own accent
colour for the inner symbol — a "Heritage" palette (dependency-injection = terracotta, templates =
slate blue, microservices = plum, utilities = teal) and a brighter "Vivid" alternative. The research
on comparable systems (JetBrains, Adobe, Astral) recommends two discriminators, shape **and**
colour — but only because those marks must survive favicon sizes. Our project marks are
large-format only; the org mark remains every repo's favicon.

Rendered side by side, the per-family accent made each mark a **three-colour** object (green frame +
gold frame + accent inner), which read as busy and diluted the org identity. Since favicon-size
legibility is explicitly a non-goal, the second discriminator buys little. A single gold inner keeps
every mark unmistakably part of one family, matches the brand palette exactly, and means a new repo
needs only a new *shape*, not a new colour to keep harmonious. Templates get no symbol at all — they
reuse the org chevron.

**Revisit trigger:** the org needs these marks at favicon scale, so shape alone no longer
disambiguates; or a family grows large enough that a colour band materially helps wayfinding on the
org site.

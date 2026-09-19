# Project marks are two-colour, differentiated by symbol, not colour

Every project mark is the constant snake frame plus a single gold inner symbol, so repos are told
apart by the shape of that symbol and never by a hue of their own. Per-family accent palettes were
drawn and rejected: research on comparable systems recommends two discriminators, shape and colour,
but only because those marks must survive favicon sizes, and ours are large-format only since the
org mark stays every repo's favicon. Side by side the accent made each mark a three-colour object
that read as busy and diluted the org identity, while one gold inner keeps the family coherent and
means a new repo needs only a new shape. The two templates get no symbol at all and reuse the org
chevron. `ALLOWED_COLORS` in `projects.py` holds the line; the pytest bars' four-step gold ramp is
its one sanctioned exception.

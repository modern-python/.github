# Light palette
GREEN = "#356852"
GOLD = "#c98a00"
TEAL = "#2a9d8f"
AMBER = "#c2722b"

# Dark palette
GREEN_DARK = "#3f8064"
GOLD_DARK = "#e0a300"

# Framework colors — verified against each upstream brand:
#   fastapi    teal      — Material teal / docs theme / simple-icons
#   litestar   gold      — litestar-org/branding (primary #EDB641)
#   faststream cyan-blue — faststream logo.svg fill (#56b7e0)
#   pytest     blue      — pytest brand (royal blue #0A9EDC)
#   typer      —         — Typer's logo is monochrome black/white; it has no
#                          chromatic brand color, so a neutral slate is used.
FRAMEWORK = {
    "fastapi": "#009688",
    "litestar": "#edb641",
    "faststream": "#56b7e0",
    "typer": "#475569",
    "pytest": "#0a9edc",
}

# Brighter framework inks for dark backgrounds (lightened toward the same hue;
# litestar uses its own light-gold secondary #FFD480).
FRAMEWORK_DARK = {
    "fastapi": "#2dd4bf",
    "litestar": "#ffd480",
    "faststream": "#82cdf0",
    "typer": "#94a3b8",
    "pytest": "#4cb8ee",
}

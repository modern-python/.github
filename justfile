default: test

test:
    uv run pytest

# Regenerate the brand kit and copy the subset the site serves into docs/assets.
sync-assets:
    uv run python -m brand.build.render
    cp brand/org/favicon.svg brand/org/mark.svg brand/org/wordmark.svg brand/org/wordmark-dark.svg docs/assets/
    cp brand/org/social-card-green.png docs/assets/

# Check every org repo against the standard's core (network: GitHub API + endoflife.date).
# CENSUS_LOCAL_ROOT=~/src/modern-python reads local checkouts instead.
census:
    uv run pytest -m census -p no:cacheprovider

# Same census as a Markdown report; exit 2 on findings (1 means the census itself broke). The weekly workflow files it as an issue.
census-report:
    uv run python -m census --markdown

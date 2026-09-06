default: test

test:
    uv run pytest

# Regenerate the brand kit and copy the subset the site serves into docs/assets.
sync-assets:
    uv run python -m brand.build.render
    cp brand/org/favicon.svg brand/org/mark.svg brand/org/wordmark.svg brand/org/wordmark-dark.svg docs/assets/
    cp brand/org/social-card-green.png docs/assets/

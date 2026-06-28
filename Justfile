default: check-planning test

index:
    uv run python planning/index.py

check-planning:
    uv run python planning/index.py --check

lint-ci: check-planning

test:
    uv run pytest

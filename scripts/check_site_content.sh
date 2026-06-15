#!/usr/bin/env bash
# Verifies the built homepage links to every modern-python project.
set -euo pipefail

HTML="site/index.html"
test -f "$HTML" || { echo "MISSING $HTML — run 'uv run mkdocs build' first"; exit 1; }

REPOS=(
  fastapi-sqlalchemy-template litestar-sqlalchemy-template
  modern-di modern-di-fastapi modern-di-litestar modern-di-faststream
  modern-di-typer modern-di-pytest that-depends
  lite-bootstrap httpware faststream-redis-timers
  faststream-concurrent-aiokafka faststream-outbox
  db-retry eof-fixer semvertag
)

missing=0
for r in "${REPOS[@]}"; do
  if ! grep -q "github.com/modern-python/${r}\"" "$HTML"; then
    echo "MISSING LINK: $r"
    missing=1
  fi
done

if [ "$missing" -eq 0 ]; then
  echo "ALL ${#REPOS[@]} PROJECT LINKS PRESENT"
else
  exit 1
fi

#!/usr/bin/env bash
# Files the census findings as one open issue: created on the first failure, the body replaced
# on every later one so the issue always shows the current state, and closed by hand once clean.
set -euo pipefail

REPORT="${1:?path to the census report}"
LABEL="census"
TITLE="Census: repos not meeting the standard's core"

gh label create "$LABEL" --color "FBCA04" --description "Weekly census findings against the standard" --force

body=$(printf '%s\n\n%s\n\n%s\n' \
  "Weekly census against <https://modern-python.org/standard/>. Latest run: ${RUN_URL}" \
  "$(cat "$REPORT")" \
  "Close this issue once a run is clean; the next failing run opens a fresh one.")

existing=$(gh issue list --label "$LABEL" --state open --json number --jq '.[0].number // empty')
if [ -z "$existing" ]; then
  gh issue create --title "$TITLE" --label "$LABEL" --body "$body"
else
  gh issue edit "$existing" --body "$body"
  gh issue comment "$existing" --body "Refreshed from ${RUN_URL}"
fi

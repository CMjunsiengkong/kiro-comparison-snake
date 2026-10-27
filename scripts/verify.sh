#!/usr/bin/env bash
# Usage: scripts/verify.sh <run-dir>
# Checks one finished M3 run without changing the run directory, and saves
# next to it:
#   <run-id>.verify.txt  the report below
#   <run-id>.diff        everything the agent changed, vs m3-start
#
# 1. Agent's own tests: the suite exactly as the agent left it (for info).
# 2. Official check, the PASS/FAIL that counts. On a scratch copy, test files
#    the agent edited or deleted are restored from m3-start, so a run cannot
#    pass by weakening tests; tests the agent added still run. The m3-start
#    suite plus the hidden acceptance tests must pass.
#
# M2 and M4 are not checked here: play the game and see the snake.
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "usage: $0 <run-dir>" >&2
  exit 2
fi
run_dir="$(cd "$1" && pwd)"
bench_dir="$(cd "$(dirname "$0")/.." && pwd)"
run_id="$(basename "$run_dir")"
report="$(dirname "$run_dir")/$run_id.verify.txt"
diff_file="$(dirname "$run_dir")/$run_id.diff"
tag=m3-start
acceptance="tests/test_m3_acceptance.py"

scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT

run_pytest() {
  set +e
  (cd "$1" && uv run pytest -q 2>&1)
  local status=$?
  set -e
  return $status
}

{
  echo "Run:     $run_id"
  echo "Check:   m3 (start tag $tag)"
  echo "Date:    $(date '+%Y-%m-%d %H:%M %Z')"
  echo
  echo "== Files changed by the agent (vs $tag; full diff in $run_id.diff) =="
  git -C "$run_dir" add -A --intent-to-add >/dev/null
  git -C "$run_dir" --no-pager diff --stat "$tag" -- . ":!$acceptance"
  git -C "$run_dir" --no-pager diff "$tag" -- . ":!$acceptance" > "$diff_file"
  echo

  echo "== 1. Agent's own tests (as the agent left them; for info) =="
  rsync -a --exclude .venv --exclude "$acceptance" "$run_dir/" "$scratch/own/"
  if run_pytest "$scratch/own"; then
    echo "-> own tests: PASS"
  else
    echo "-> own tests: FAIL"
  fi
  echo

  echo "== 2. Official check =="
  rsync -a --exclude .venv --exclude "$acceptance" "$run_dir/" "$scratch/official/"
  if ! git -C "$scratch/official" diff --quiet --diff-filter=MD "$tag" -- tests; then
    echo "Edited or deleted test files, restored from $tag for this check:"
    git -C "$scratch/official" --no-pager diff --name-only --diff-filter=MD "$tag" -- tests
    git -C "$scratch/official" checkout "$tag" -- tests
  fi
  cp "$bench_dir/acceptance/test_m3_acceptance.py" "$scratch/official/tests/"
  echo "Added hidden acceptance tests."
  if run_pytest "$scratch/official"; then
    echo
    echo "RESULT: PASS"
  else
    echo
    echo "RESULT: FAIL"
  fi
} 2>&1 | tee "$report"

echo "Saved: $report"
echo "Saved: $diff_file"

#!/usr/bin/env bash
# Usage: scripts/new-run.sh <start-tag> <run-id>
# Makes a fresh copy of the demo repo at <start-tag> for one run.
# The copy has no other history, no bench files and no remote, so the agent
# cannot see the acceptance tests or push back to the source repo.
set -euo pipefail

if [ $# -ne 2 ]; then
  echo "usage: $0 <start-tag> <run-id>" >&2
  exit 2
fi
tag="$1"
run_id="$2"
repo="${SNAKE_REPO:-$HOME/Project/kiro-comparison-snake}"
runs_dir="${KIRO_RUNS_DIR:-$HOME/Project/kiro-runs-snake}"
dest="$runs_dir/$run_id"

if [ -e "$dest" ]; then
  echo "already exists: $dest" >&2
  exit 1
fi
mkdir -p "$runs_dir"

src="$repo"
case "$src" in
  /*) src="file://$src" ;;  # --depth needs a URL for local repos
esac
git clone --quiet --depth 1 --branch "$tag" "$src" "$dest" 2>/dev/null
git -C "$dest" remote remove origin

echo "Run $run_id ready: $dest"
echo "Start tag: $tag ($(git -C "$dest" rev-parse --short HEAD))"
echo "Created:   $(date '+%Y-%m-%d %H:%M %Z')"

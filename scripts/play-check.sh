#!/usr/bin/env bash
# Usage: scripts/play-check.sh <run-dir>
# M3 play check for the high score. Deletes every high score file the M3 runs
# use, so no run sees another run's score, then starts the game twice and
# records what was saved after each game. Saves <run-id>.playcheck.txt next
# to the run directory.
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "usage: $0 <run-dir>" >&2
  exit 2
fi
run_dir="$(cd "$1" && pwd)"
run_id="$(basename "$run_dir")"
report="$(dirname "$run_dir")/$run_id.playcheck.txt"
save_files=(
  "$HOME/.snake_highscore"
  "$HOME/.snake_game/highscore.txt"
  "$HOME/.local/share/snake_game/highscore.txt"
  "$run_dir/snake_game/highscore.txt"
)

show_saved() {
  local found=0
  for f in "${save_files[@]}"; do
    if [ -f "$f" ]; then
      echo "  $f: $(cat "$f")"
      found=1
    fi
  done
  [ "$found" -eq 1 ] || echo "  (no high score file)"
}

rm -f "${save_files[@]}"
{
  echo "Run:  $run_id"
  echo "Date: $(date '+%Y-%m-%d %H:%M %Z')"
  echo
} > "$report"

echo "Game 1: score 2 or more, die, then press Esc to quit."
(cd "$run_dir" && uv run python -m snake_game.main)
{ echo "Saved after game 1:"; show_saved; echo; } | tee -a "$report"

echo "Game 2: look for your score from game 1 on screen, then press Esc to quit."
(cd "$run_dir" && uv run python -m snake_game.main)
{ echo "Saved after game 2:"; show_saved; } | tee -a "$report"

read -r -p "Did game 2 show your game 1 score on screen? (yes/no/not shown) " answer
echo "On screen in game 2: $answer" >> "$report"
echo "Saved: $report"

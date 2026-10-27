# Run log

One row per run. Fill it in right after the run, while it's fresh.

- **Run ID:** `R-<milestone>-<app>[-<mode>]-<n>`, e.g. `R-M2-IDE-1`, `R-M3-CLI-QUICKSPEC-1`
- **Play check:** run `uv run python -m snake_game.main` in the run folder for 30 seconds. Snake visible and moving? For M3: does the high score survive a restart of the game, and does the game speed up? Save one screenshot as `<run-id>.png` next to the run folder.
- **Result:** M3 only, the `RESULT` line from `scripts/verify.sh`. M2 and M4: the play check is the result.
- **Interventions:** how many times you had to step in or correct it
- **Asked first?:** whether it asked questions before coding, and how many
- **Decision points:** M3 only, from `decision-points.md`, as asked / written down / silent, e.g. `3 / 4 / 1`
- **Surprises:** gotchas and anything the docs didn't tell you

After each run, add its numbers (credits, agent time, approvals) under "Session stats" with `scripts/session-stats.py <run-id>`.

| Run ID | Milestone | App / mode | Start tag | Date | Play check | Result | Interventions | Asked first? | Decision points | Surprises |
|---|---|---|---|---|---|---|---|---|---|---|
| R-M2-IDE-1 | M2 | Kiro IDE 1.4.26 / default agent, Autopilot | m2-start | 2026-10-27 | Snake visible and moving | — | 0 (1 approval: `uv run python -m pytest tests/test_render.py -q`) | No | — | Identical fix to CLI, byte for byte. Can revert the agent's file change in one click |
| R-M2-CLI-1 | M2 | Kiro CLI 2.34.0 V3 / default agent | m2-start | 2026-10-27 | Snake visible and moving | — | 0 (1 approval: `uv run pytest tests/test_render.py -q`) | No | — | Identical fix to IDE, byte for byte |

## Session stats

| Run | Session start (UTC) | Mode | User msgs | Tool appr | Review appr | Appr wait s | Agent s | Wall s | Credits |
|---|---|---|---|---|---|---|---|---|---|
| R-M2-CLI-1 | 2026-10-27 08:26 | autopilot | 0 | 1 | 0 | 1 | 30 | 31 | 0.52 |
| R-M2-IDE-1 | 2026-10-27 08:01 | autopilot | 0 | 1 | 0 | 7 | 26 | 32 | 0.59 |

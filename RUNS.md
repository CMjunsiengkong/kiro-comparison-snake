# Run log

One row per run. Fill it in right after the run, while it's fresh.

- **Run ID:** `R-<milestone>-<app>[-<mode>]-<n>`, e.g. `R-M2-IDE-1`, `R-M3-CLI-QUICKSPEC-1`
- **Play check:** run `uv run python -m snake_game.main` in the run folder for 30 seconds. Snake visible and moving? For M3: does the high score survive a restart of the game, and does the game speed up? Save one screenshot as `<run-id>.png` next to the run folder.
- **Result:** M3 only, the `RESULT` line from `scripts/verify.sh`. M2: the play check is the result. M4 (Crew): the report against the known answer.
- **Interventions:** how many times you had to step in or correct it
- **Asked first?:** whether it asked questions before coding, and how many
- **Decision points:** M3 only, from `decision-points.md`, as asked / written down / silent, e.g. `3 / 4 / 1`
- **Surprises:** gotchas and anything the docs didn't tell you

After each run, add its numbers (credits, agent time, approvals) under "Session stats" with `scripts/session-stats.py <run-id>`.

| Run ID | Milestone | App / mode | Start tag | Date | Play check | Result | Interventions | Asked first? | Decision points | Surprises |
|---|---|---|---|---|---|---|---|---|---|---|
| R-M2-IDE-1 | M2 | Kiro IDE 1.4.26 / default agent, Autopilot | m2-start | 2026-10-27 | Snake visible and moving | — | 0 (1 approval: `uv run python -m pytest tests/test_render.py -q`) | No | — | Identical fix to CLI, byte for byte. Can revert the agent's file change in one click |
| R-M2-CLI-1 | M2 | Kiro CLI 2.34.0 V3 / default agent | m2-start | 2026-10-27 | Snake visible and moving | — | 0 (1 approval: `uv run pytest tests/test_render.py -q`) | No | — | Identical fix to IDE, byte for byte |
| R-M3-IDE-PLAIN-1 | M3 | Kiro IDE / default agent, Autopilot | m3-start | 2026-10-28 | Speeds up: yes. High score saved and shown after restart (`play-check.sh`) | PASS (65) | 0 | No | 0 / 0 / 8 | Built: `~/.snake_game/highscore.txt`, +0.5/point, cap 25, "Best" shown |
| R-M3-CLI-PLAIN-1 | M3 | Kiro CLI V3 / default agent | m3-start | 2026-10-28 | Speeds up: yes. High score saved and shown after restart (`play-check.sh`) | PASS (67) | 0 | No | 0 / 0 / 8 | Built: high score file inside the package folder (`snake_game/highscore.txt`, added to `.gitignore`), +0.5/point, cap 25, "Best" shown |
| R-M3-IDE-PLAN-1 | M3 | Kiro IDE / Plan | m3-start | 2026-10-28 | Speeds up: yes. High score saved to disk and loaded at start (in code), but never shown on screen (`play-check.sh`) | PASS (74) | 0 (2 answers + "go ahead") | Yes: 3 questions, then 2 follow-ups, as text options with "Other" | 5 (D1 D2 D3 D5 D6) / 3 (D4 D7 D8) / 0 | Built to the reference answers, but chose not to show the high score on screen and said so in the plan |
| R-M3-CLI-PLAN-1 | M3 | Kiro CLI V3 / Plan (`/plan`) | m3-start | 2026-10-28 | Speeds up: yes. High score saved and shown after restart (`play-check.sh`) | PASS (78) | 0 (2 answers + "go ahead") | Yes: 3 questions, then 2 follow-ups, as text options | 4 (D1 D3 D5 D6) / 3 (D4 D7 D8) / 1 (D2) | Made `draw()` take a required `high_score` argument and adapted existing tests; decoupled move timing from the render loop (asked) |
| R-M3-IDE-QUICKSPEC-1 | M3 | Kiro IDE / Quick Spec | m3-start | 2026-10-28 | Speeds up: yes. High score saved to disk and loaded at start (in code), but never shown on screen (`play-check.sh`) | PASS (68) | 1 ("go ahead" to run the tasks) | Yes: 3 question prompts with option buttons and "Skip" | 3 (D1 D5 D6; the D6 question was skipped, so it picked cap 25) / 5 / 0 | Stopped after writing the spec; tasks ran only after a second prompt. Added `hypothesis` as a dev dependency |
| R-M3-IDE-SPEC-1 | M3 | Kiro IDE / Spec | m3-start | 2026-10-28 | Speeds up: yes. High score saved to disk and loaded at start (in code), but never shown on screen (`play-check.sh`) | PASS (71) | 3 (phase buttons: requirements → design → tasks) | Process questions only (feature or bug? start with requirements or design?) | 0 / 8 / 0 | Decided everything in the documents: `~/.snake_game/highscore.txt`, +1/point, **cap 60**. Two sessions (spec, then tasks). Added `hypothesis` |
| R-M3-CLI-SPEC-1 | M3 | Kiro CLI V3 / Spec (`/spec new`) | m3-start | 2026-10-28 | Speeds up: yes. High score saved and shown after restart (`play-check.sh`) | PASS (64) | 1 ("Run all required tasks") | Process questions only, plus a review gate per phase | 0 / 8 / 0 | Decided everything in the documents: `~/.local/share/snake_game/highscore.txt`, +0.5/point, cap 25, "Best" shown. Made `draw()` take a required `high_score` argument |
| R-M3-CLI-QUICKSPEC-1 | M3 | Kiro CLI V3 / Quick Spec | — | 2026-10-28 | — | Not possible | — | — | — | No way found to start Quick Spec in CLI V3; folder deleted |

## Session stats

| Run | Session start (UTC) | Mode | User msgs | Questions | Tool appr | Review appr | Appr wait s | Agent s | Wall s | Credits |
|---|---|---|---|---|---|---|---|---|---|---|
| R-M2-CLI-1 | 2026-10-27 08:26 | autopilot | 0 | 0 | 1 | 0 | 1 | 30 | 31 | 0.52 |
| R-M2-IDE-1 | 2026-10-27 08:01 | autopilot | 0 | 0 | 1 | 0 | 7 | 26 | 32 | 0.59 |
| R-M3-CLI-PLAIN-1 | 2026-10-28 06:22 | autopilot | 0 | 0 | 1 | 0 | 116 | 129 | 244 | 2.88 |
| R-M3-CLI-PLAN-1 | 2026-10-28 06:40 | autopilot | 3 | 0 | 3 | 0 | 111 | 262 | 824 | 4.81 |
| R-M3-CLI-SPEC-1 | 2026-10-28 07:19 | autopilot | 1 | 5 | 8 | 0 | 635 | 1160 | 1795 | 27.22 |
| R-M3-IDE-PLAIN-1 | 2026-10-28 06:20 | autopilot | 0 | 0 | 1 | 0 | 24 | 119 | 143 | 2.64 |
| R-M3-IDE-PLAN-1 | 2026-10-28 06:36 | autopilot | 3 | 0 | 1 | 0 | 7 | 212 | 1186 | 3.95 |
| R-M3-IDE-QUICKSPEC-1 | 2026-10-28 07:06 | autopilot | 1 | 3 | 12 | 0 | 743 | 839 | 5061 | 20.24 |
| R-M3-IDE-SPEC-1 | 2026-10-28 07:24 | autopilot | 3 | 3 | 0 | 0 | 167 | 956 | 1242 | 18.34 |
| R-M3-IDE-SPEC-1 | 2026-10-28 07:48 | autopilot | 0 | 0 | 18 | 0 | 447 | 497 | 944 | 16.18 |

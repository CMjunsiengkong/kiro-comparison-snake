# Snake bench

The test harness for comparing Kiro IDE, Kiro CLI (V3) and Kiro Crew on the Snake demo repo. It lives on its own `bench` branch so that it never appears in a run's working copy.

## Contents

| Path | What it is |
|---|---|
| `prompts/` | The exact prompt for each task. Paste it unchanged. |
| `decision-points.md` | The choices the M3 prompt leaves open, and the reference answers to give when asked. Never show it to an agent. |
| `acceptance/` | Hidden M3 acceptance tests. The agent never sees them; `verify.sh` adds them after the run. |
| `scripts/new-run.sh` | Creates a fresh copy of the repo at a start tag for one run, in `~/Project/kiro-runs-snake/<run-id>`. |
| `scripts/verify.sh` | Checks a finished M3 run without changing it. Saves `<run-id>.verify.txt` and `<run-id>.diff`. |
| `scripts/session-stats.py` | Reads Kiro's session logs: approvals, agent time, credits per run. |
| `RUNS.md` | The run log. |

## Start tags (on `main`)

| Tag | State | Expected `uv run pytest` |
|---|---|---|
| `m2-start` | Bug: the snake is not drawn | 47 passed, 1 failed (`test_draw_normal_frame`) |
| `m3-start` | Bug fixed, no high score or speed-up | 48 passed |
| `m3-start` + `acceptance/` | Feature not built yet | collection error (`snake_game.highscore` missing) |

## Settings that keep runs comparable

- Model: Auto, in both apps.
- Kiro IDE: Autopilot (the IDE default).
- Kiro CLI: V3 only. In `~/.kiro/settings/permissions.yaml`, `fs_write` is `allow`.
- Shell commands ask for approval in both apps.
- A fresh copy for every run, and the prompt pasted unchanged.

## The runs

| Milestone | Run IDs | Start tag | Prompt | How it's checked |
|---|---|---|---|---|
| M2: small bug | `R-M2-IDE-1`, `R-M2-CLI-1` | `m2-start` | `m2-bugfix.md` | Play check |
| M3: feature | `R-M3-{IDE,CLI}-{PLAIN,PLAN,QUICKSPEC,SPEC}-1` (8 runs) | `m3-start` | `m3-feature.md` | `verify.sh` + play check + decision points |
| M4: headless | `R-M4-CLI-1` | `m2-start` | `m4-headless.md` | Play check |
| M5: Crew | `R-M5-CREW-1` | `m2-start` | `m5-crew.md` | Known answer: 47 passed, 1 failed (`test_draw_normal_frame`), and no file changed except `reports/health.md` |

## One run

```sh
cd ~/Project/kiro-comparison-snake-bench
scripts/new-run.sh m3-start R-M3-CLI-PLAN-1      # 1. fresh copy in ~/Project/kiro-runs-snake/R-M3-CLI-PLAN-1
# 2. open that folder in the app under test and paste the prompt
# 3. answer questions with decision-points.md; anything else: "Your choice."
scripts/verify.sh ~/Project/kiro-runs-snake/R-M3-CLI-PLAN-1   # 4. M3 only
# 5. play check, screenshot, then add a row to RUNS.md
scripts/session-stats.py R-M3-CLI-PLAN-1         # 6. paste under "Session stats"
```

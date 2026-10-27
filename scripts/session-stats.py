#!/usr/bin/env python3
"""Summarize Kiro sessions (IDE and CLI V3) for benchmark runs.

Usage: scripts/session-stats.py [RUN-ID ...]

Kiro writes every IDE and CLI V3 session to ~/.kiro/sessions/<hash>/sess_*/.
This finds the sessions whose workspace is a run copy in ~/Project/kiro-runs-snake
(or $KIRO_RUNS_DIR) and prints one row per session. With RUN-IDs, only those
runs are shown.

Columns:
  user msgs    messages you sent after the first prompt (answers, "go ahead")
  tool appr    tool approvals (Allow/Deny prompts)
  review appr  "Review changes" prompts (IDE Supervised mode)
  appr wait    seconds spent waiting on you inside approval prompts
  agent s      seconds the agent worked, minus approval waits
  wall s       first to last event, including your thinking time
  credits      credits charged for the session
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

SESSIONS = Path.home() / ".kiro" / "sessions"
RUNS_DIR = Path(os.environ.get("KIRO_RUNS_DIR", Path.home() / "Project" / "kiro-runs-snake"))


def ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def summarize(session_dir: Path) -> dict:
    events = [json.loads(line) for line in (session_dir / "messages.jsonl").open()]
    pending = {}
    stats = {
        "user_msgs": -1,  # the first user message is the prompt itself
        "tool_appr": 0,
        "review_appr": 0,
        "appr_wait": 0.0,
        "elapsed": 0.0,
        "credits": 0.0,
    }
    for event in events:
        payload = event["payload"]
        kind = payload["type"]
        if kind == "user":
            stats["user_msgs"] += 1
        elif kind == "pending_interaction":
            pending[payload["toolCallId"]] = ts(event["timestamp"])
            if payload.get("question") == "Review changes":
                stats["review_appr"] += 1
            else:
                stats["tool_appr"] += 1
        elif kind == "interaction_resolved" and payload["toolCallId"] in pending:
            started = pending.pop(payload["toolCallId"])
            stats["appr_wait"] += (ts(event["timestamp"]) - started).total_seconds()
        elif kind == "usage_summary":
            stats["elapsed"] += payload.get("elapsedTime", 0) / 1000
            stats["credits"] += sum(
                turn.get("usage", 0) for turn in payload.get("promptTurnSummaries", [])
            )
    times = [ts(event["timestamp"]) for event in events]
    stats["wall"] = (max(times) - min(times)).total_seconds()
    # elapsedTime covers whole turns, which include the time a prompt waits for you.
    stats["agent"] = max(stats["elapsed"] - stats["appr_wait"], 0)
    return stats


def main() -> None:
    wanted = set(sys.argv[1:])
    rows = []
    for meta_file in SESSIONS.glob("*/sess_*/session.json"):
        meta = json.loads(meta_file.read_text())
        workspace = Path(meta.get("workspacePaths", [""])[0])
        if workspace.parent != RUNS_DIR:
            continue
        if wanted and workspace.name not in wanted:
            continue
        stats = summarize(meta_file.parent)
        rows.append((workspace.name, meta["createdAt"][:16].replace("T", " "),
                     "autopilot" if meta.get("autopilot") else "supervised", stats))

    print("| Run | Session start (UTC) | Mode | User msgs | Tool appr | Review appr "
          "| Appr wait s | Agent s | Wall s | Credits |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for run, created, mode, s in sorted(rows, key=lambda row: (row[0], row[1])):
        print(f"| {run} | {created} | {mode} | {s['user_msgs']} | {s['tool_appr']} "
              f"| {s['review_appr']} | {s['appr_wait']:.0f} | {s['agent']:.0f} "
              f"| {s['wall']:.0f} | {s['credits']:.2f} |")


if __name__ == "__main__":
    main()

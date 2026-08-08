#!/usr/bin/env python3
"""Codex notify handler: append agent-turn-complete events to audit JSONL."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import sys


def main() -> int:
    if len(sys.argv) < 2:
        return 0

    try:
        payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        return 0

    if payload.get("type") != "agent-turn-complete":
        return 0

    cwd = Path(payload.get("cwd") or ".")
    audit_dir = cwd / "docs" / "sessions" / ".audit"
    audit_dir.mkdir(parents=True, exist_ok=True)

    thread_id = payload.get("thread-id", "unknown")
    out_file = audit_dir / f"{thread_id}.jsonl"

    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": payload.get("type"),
        "thread_id": thread_id,
        "turn_id": payload.get("turn-id"),
        "cwd": str(cwd),
        "last_assistant_message": payload.get("last-assistant-message", ""),
        "input_messages": payload.get("input-messages", []),
    }

    with out_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=True) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

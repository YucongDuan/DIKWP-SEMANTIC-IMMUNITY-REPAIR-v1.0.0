from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .utils import digest_json


class ResponsibilityLedger:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        previous = "0" * 64
        if self.path.exists():
            lines = [line for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]
            if lines:
                previous = json.loads(lines[-1])["event_digest"]
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "payload": payload,
            "previous_digest": previous,
        }
        event["event_digest"] = digest_json(event)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        return event

    def verify(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"valid": True, "events": 0, "last_digest": None}
        previous = "0" * 64
        count = 0
        for idx, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            event = json.loads(line)
            stored = event.pop("event_digest")
            if event.get("previous_digest") != previous or digest_json(event) != stored:
                return {"valid": False, "events": count, "failed_line": idx}
            previous = stored
            count += 1
        return {"valid": True, "events": count, "last_digest": previous if count else None}

from __future__ import annotations

import hashlib
import json
import math
from typing import Iterable


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


def digest_json(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def find_markers(text: str, phrases: Iterable[str]) -> list[str]:
    low = text.casefold()
    found: list[str] = []
    for phrase in phrases:
        if phrase.casefold() in low:
            found.append(phrase)
    return found


def saturation(count: int, scale: float = 2.0) -> float:
    if count <= 0:
        return 0.0
    return clamp(1.0 - math.exp(-count / scale))


def normalize_weights(items: dict[str, float]) -> dict[str, float]:
    safe = {k: max(0.0, float(v)) for k, v in items.items()}
    total = sum(safe.values()) or 1.0
    return {k: v / total for k, v in safe.items()}

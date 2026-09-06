from __future__ import annotations

from typing import Any


def to_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# DIKWP Semantic Immunity & Repair Analysis",
        "",
        f"- Decision: `{result['decision']}`",
        f"- Confidence: `{result['confidence']:.2f}`",
        f"- Protected expression: `{result['protected_expression']}`",
        f"- High-impact context: `{result['high_impact']}`",
        f"- Case digest: `{result['case_digest']}`",
        "",
        "## Signal vector",
        "",
        "| Signal | Score | Explanation |",
        "|---|---:|---|",
    ]
    for key, signal in result["signals"].items():
        lines.append(f"| {key} | {signal['score']:.2f} | {signal['explanation']} |")
    lines.extend(["", "## Retained worlds", ""])
    for world in result["worlds"]:
        lines.append(f"- **{world['label_cn']}** — {world['weight']:.1%}")
    lines.extend(["", "## Interventions", ""])
    for action in result["interventions"]:
        lines.append(f"- `{action['layer']}` — `{action['action']}` — automatic: `{action['automatic']}`")
    card = result["repair_card"]
    lines.extend([
        "", "## Context repair card", "",
        f"**Useful core:** {card['useful_core']}", "",
        "**Balanced rewrite:**", "", card["balanced_rewrite"], "",
        "**Omitted context:**",
    ])
    lines.extend(f"- {x}" for x in card["omitted_context"])
    lines.extend(["", "**Verification questions:**"])
    lines.extend(f"- {x}" for x in card["verification_questions"])
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {x}" for x in result["limitations"])
    return "\n".join(lines) + "\n"

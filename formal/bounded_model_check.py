from __future__ import annotations

import json
from itertools import product
from pathlib import Path

from dikwp_sirr import SemanticCase, analyze


def main() -> int:
    violations = []
    states = 0
    roles = ["advice", "criticism", "whistleblowing", "distress_expression", "marketing"]
    booleans = [False, True]
    values = [0.0, 0.5, 1.0]
    for role, monetized, verified_fabrication, imminent, evidence, trace in product(
        roles, booleans, booleans, booleans, values, values
    ):
        states += 1
        case = SemanticCase(
            text="我很痛苦。专家都说这是唯一真相，马上购买。",
            content_role=role,
            monetized=monetized,
            verified_fabrication=verified_fabrication,
            imminent_harm_or_illegal=imminent,
            evidence_quality=evidence,
            source_traceability=trace,
            appeal_available=True,
        )
        result = analyze(case)
        if not all(result.invariants.values()):
            violations.append({"case": case.__dict__ if hasattr(case, "__dict__") else {"role": role}, "invariants": result.invariants})
        if role in {"criticism", "whistleblowing", "distress_expression"} and not imminent and not verified_fabrication:
            if result.decision != "PROTECT_NEGATIVE_TRUTH_OR_DISTRESS":
                violations.append({"type": "protected_expression_restricted", "role": role, "decision": result.decision})
        if result.decision == "AUTHORIZED_REMOVAL_FOR_ILLEGAL_OR_IMMINENT_HARM" and not case.authorized_human_review:
            violations.append({"type": "removal_without_authorized_human"})
    receipt = {
        "model": "SIRP-1000 bounded reference workflow",
        "states_checked": states,
        "violations": violations,
        "violation_count": len(violations),
        "scope": "Finite combinatorial check of protected-expression, appeal, deception and removal invariants.",
    }
    out = Path(__file__).resolve().parents[1] / "validation" / "BOUNDED_MODEL_CHECK_RECEIPT.json"
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0 if not violations else 2


if __name__ == "__main__":
    raise SystemExit(main())

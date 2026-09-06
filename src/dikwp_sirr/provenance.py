from __future__ import annotations

from typing import Any


def c2pa_style_reference(result: dict[str, Any]) -> dict[str, Any]:
    """Return an unsigned reference mapping; this is not a C2PA Manifest."""
    return {
        "type": "SIRRProvenanceReference",
        "claim_generator": "DIKWP Semantic Immunity & Repair OS/1.0.0",
        "title": "Semantic analysis and context-repair record",
        "assertions": [
            {"label": "sirr.input_digest", "data": result.get("case_digest")},
            {"label": "sirr.decision", "data": result.get("decision")},
            {"label": "sirr.external_network_used", "data": False},
            {"label": "sirr.limitations", "data": result.get("limitations", [])},
        ],
        "signed": False,
        "notice": "Reference mapping only; not a signed C2PA Content Credential.",
    }

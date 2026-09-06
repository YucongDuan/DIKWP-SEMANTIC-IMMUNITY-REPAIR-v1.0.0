from itertools import product

from dikwp_sirr import SemanticCase, analyze


def test_negative_affect_alone_never_causes_restriction_across_grid():
    for role, evidence, trace in product(
        ["distress_expression", "criticism"], [0.0, 0.5, 1.0], [0.0, 0.5, 1.0]
    ):
        result = analyze(SemanticCase(
            text="我很痛苦、愤怒，也认为这个结果很糟糕。",
            content_role=role,
            evidence_quality=evidence,
            source_traceability=trace,
        ))
        assert result.decision == "PROTECT_NEGATIVE_TRUTH_OR_DISTRESS"


def test_no_result_contains_person_moral_score():
    result = analyze(SemanticCase(text="你必须马上购买。", monetized=True))
    payload = str(result.to_dict()).lower()
    assert "person_moral_score" not in payload
    assert result.invariants["no_person_level_moral_score"]


def test_adverse_action_has_appeal_invariant():
    result = analyze(SemanticCase(
        text="科学已经证明，马上报名，唯一机会。",
        domain="finance",
        content_role="marketing",
        monetized=True,
        paid_funnel=True,
        evidence_quality=0.0,
        source_traceability=0.0,
        reach=1.0,
        appeal_available=True,
    ))
    assert result.invariants["appeal_required_for_adverse_distribution_or_monetization_action"]

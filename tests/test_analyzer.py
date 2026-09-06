from dikwp_sirr import SemanticCase, analyze


def test_negative_distress_is_protected():
    result = analyze(SemanticCase(
        text="我最近很痛苦也很悲伤，只是在说自己的感受。",
        content_role="distress_expression",
        evidence_quality=0.5,
        source_traceability=0.5,
    ))
    assert result.decision == "PROTECT_NEGATIVE_TRUTH_OR_DISTRESS"
    assert result.invariants["negative_affect_alone_never_restricts"]


def test_whistleblowing_not_removed_for_negative_tone():
    result = analyze(SemanticCase(
        text="事故报告很糟糕，但日志和合同显示公司未按承诺执行，请独立复核。",
        content_role="whistleblowing",
        evidence_quality=0.8,
        source_traceability=0.85,
    ))
    assert result.protected_expression
    assert result.decision == "PROTECT_NEGATIVE_TRUTH_OR_DISTRESS"


def test_motherhood_marketing_gets_context_and_zero_sum_repair():
    result = analyze(SemanticCase(
        text="女性要先好好照顾自己才能照顾孩子，真正觉醒的妈妈都应该马上报名课程。",
        domain="family_parenting",
        content_role="marketing",
        audience_context=["caregiver_fatigue", "low_domain_literacy"],
        monetized=True,
        paid_funnel=True,
        evidence_quality=0.1,
        source_traceability=0.1,
        reach=0.7,
    ))
    assert result.signals["context_truncation"].score > 0.25
    assert result.signals["zero_sum_risk"].score > 0.20
    assert "孩子" in result.repair_card.balanced_rewrite
    assert result.decision in {
        "PAUSE_MONETIZATION_PENDING_REVIEW",
        "REDUCE_RECOMMENDER_AMPLIFICATION_PENDING_REVIEW",
        "ADD_SHARING_FRICTION",
    }


def test_health_miracle_requires_high_impact_review():
    result = analyze(SemanticCase(
        text="科学已经证明，这个秘密方法百分之百治愈焦虑，不需要医生，马上购买。",
        domain="health",
        content_role="marketing",
        audience_context=["acute_distress"],
        monetized=True,
        evidence_quality=0.0,
        source_traceability=0.0,
        reach=0.8,
    ))
    assert result.high_impact
    assert result.decision in {"HUMAN_REVIEW_HIGH_RISK", "PAUSE_MONETIZATION_PENDING_REVIEW"}


def test_deliberate_deception_not_inferred_without_evidence():
    result = analyze(SemanticCase(
        text="这是唯一真相，专家都说你必须相信。",
        evidence_quality=0.0,
        source_traceability=0.0,
    ))
    deliberate = next(w for w in result.worlds if w.key == "deliberate_deception")
    assert deliberate.weight < 0.15
    assert result.invariants["deliberate_deception_not_inferred_without_verified_fabrication"]


def test_verified_fabrication_can_raise_deception_world():
    result = analyze(SemanticCase(
        text="这是唯一真相。",
        verified_fabrication=True,
        evidence_quality=0.1,
        source_traceability=0.2,
    ))
    deliberate = next(w for w in result.worlds if w.key == "deliberate_deception")
    assert deliberate.weight > 0.20


def test_imminent_harm_without_authority_only_escalates():
    result = analyze(SemanticCase(
        text="立即实施危险行为。",
        imminent_harm_or_illegal=True,
        authorized_human_review=False,
    ))
    assert result.decision == "HUMAN_REVIEW_HIGH_RISK"


def test_authorized_imminent_harm_path_is_not_automatic():
    result = analyze(SemanticCase(
        text="立即实施危险行为。",
        imminent_harm_or_illegal=True,
        authorized_human_review=True,
    ))
    assert result.decision == "AUTHORIZED_REMOVAL_FOR_ILLEGAL_OR_IMMINENT_HARM"
    assert all(not action["automatic"] for action in result.interventions if action["layer"] == "authority")


def test_addictive_features_produce_interface_intervention():
    result = analyze(SemanticCase(
        text="继续看下一条。",
        addictive_features=["infinite_scroll", "autoplay", "variable_reward"],
    ))
    assert result.signals["addiction_design"].score > 0.5
    assert any(a["layer"] == "interface" for a in result.interventions)

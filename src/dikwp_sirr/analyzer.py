from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .lexicons import ADDICTIVE_FEATURE_WEIGHTS, HIGH_IMPACT_DOMAINS, LEXICONS, PROTECTED_ROLES
from .models import AnalysisResult, Decision, RepairCard, SemanticCase, Signal, WorldHypothesis
from .repair import build_repair_card
from .utils import clamp, digest_json, find_markers, normalize_weights, saturation

VERSION = "1.0.0"


def _signal(name: str, score: float, markers: list[str], explanation: str) -> Signal:
    return Signal(name=name, score=round(clamp(score), 4), markers=markers, explanation=explanation)


def _extract_signals(case: SemanticCase) -> dict[str, Signal]:
    text = case.text
    marks = {key: find_markers(text, values) for key, values in LEXICONS.items()}

    universal = saturation(len(marks["universalism"]))
    certainty = saturation(len(marks["certainty"]))
    causal = saturation(len(marks["causal_leap"]))
    qualifiers = saturation(len(marks["qualifiers"]))
    context = saturation(len(marks["context_markers"]))
    rights = saturation(len(marks["rights_markers"]))
    urgency = saturation(len(marks["urgency"]))
    authority = saturation(len(marks["authority_laundering"]))
    identity = saturation(len(marks["identity_coercion"]))
    zero_sum = saturation(len(marks["zero_sum"]))
    shaming = saturation(len(marks["shaming"]))
    self_sealing = saturation(len(marks["self_sealing"]))
    conspiracy = saturation(len(marks["conspiracy"]))
    monetization_text = saturation(len(marks["monetization"]))

    claim_strength = clamp(0.34 * universal + 0.33 * certainty + 0.33 * causal)
    evidence_gap = clamp(
        0.55 * claim_strength * (1.0 - case.evidence_quality)
        + 0.30 * (1.0 - case.source_traceability)
        + 0.15 * authority * (1.0 - case.source_traceability)
    )
    family_omission = 0.18 if case.domain == "family_parenting" and marks["family_roles"] and not marks["context_markers"] else 0.0
    context_truncation = clamp(
        0.34 * universal + 0.22 * causal + 0.27 * zero_sum + 0.17 * identity + family_omission
        - 0.18 * qualifiers - 0.18 * context - 0.10 * rights
    )
    manipulation_pressure = clamp(
        0.19 * urgency + 0.17 * authority + 0.18 * identity + 0.13 * shaming
        + 0.16 * self_sealing + 0.09 * conspiracy
        + 0.08 * max(monetization_text, float(case.monetized or case.paid_funnel))
    )
    addiction_design = clamp(sum(ADDICTIVE_FEATURE_WEIGHTS.get(x, 0.08) for x in case.addictive_features))

    vulnerability_base = min(1.0, len(set(case.audience_context)) / 4.0)
    vulnerability_exploitation = clamp(vulnerability_base * (0.55 * manipulation_pressure + 0.30 * context_truncation + 0.15 * urgency))
    zero_sum_risk = clamp(0.56 * zero_sum + 0.24 * identity + 0.20 * shaming - 0.12 * rights - 0.10 * context)
    unverifiability = clamp(
        0.36 * certainty + 0.22 * self_sealing + 0.18 * conspiracy
        + 0.24 * (1.0 - case.source_traceability)
        - 0.14 * qualifiers
    )
    commercial_capture = clamp(
        float(case.monetized or case.paid_funnel) * (0.42 * evidence_gap + 0.35 * manipulation_pressure + 0.23 * urgency)
    )
    repair_capacity = clamp(0.30 * qualifiers + 0.28 * context + 0.22 * rights + 0.20 * case.source_traceability)

    # Negative affect is recorded separately and never used as a restriction trigger.
    negative_affect_markers = find_markers(text, ("痛苦", "绝望", "生气", "愤怒", "失败", "悲伤", "危险", "伤害", "bad", "sad", "angry", "danger"))
    negative_affect = saturation(len(negative_affect_markers))

    return {
        "evidence_gap": _signal("evidence_gap", evidence_gap, marks["certainty"] + marks["authority_laundering"] + marks["causal_leap"], "强结论与可追溯证据之间的缺口。"),
        "context_truncation": _signal("context_truncation", context_truncation, marks["universalism"] + marks["zero_sum"] + marks["identity_coercion"], "省略成立条件、受影响方或反例造成的语境截断。"),
        "manipulation_pressure": _signal("manipulation_pressure", manipulation_pressure, marks["urgency"] + marks["identity_coercion"] + marks["shaming"] + marks["self_sealing"], "利用紧迫、身份、羞耻或封闭论证推动行动。"),
        "addiction_design": _signal("addiction_design", addiction_design, list(case.addictive_features), "界面或传播机制是否以持续停留、重复刷新和变量奖励为目标。"),
        "vulnerability_exploitation": _signal("vulnerability_exploitation", vulnerability_exploitation, list(case.audience_context), "内容压力与受众情境脆弱性的耦合，不是对人的固定能力评级。"),
        "zero_sum_risk": _signal("zero_sum_risk", zero_sum_risk, marks["zero_sum"] + marks["identity_coercion"] + marks["shaming"], "是否把关系、性别、家庭或群体塑造成只能一方获益的对立结构。"),
        "unverifiability": _signal("unverifiability", unverifiability, marks["certainty"] + marks["self_sealing"] + marks["conspiracy"], "主张是否缺少可观察反证，或用质疑本身证明主张。"),
        "commercial_capture": _signal("commercial_capture", commercial_capture, marks["monetization"] + marks["urgency"], "知识表达与付费漏斗、紧迫压力及证据缺口的绑定。"),
        "repair_capacity": _signal("repair_capacity", repair_capacity, marks["qualifiers"] + marks["context_markers"] + marks["rights_markers"], "内容是否公开边界、反例、退出和更正路径。"),
        "negative_affect": _signal("negative_affect", negative_affect, negative_affect_markers, "负面情绪或坏消息强度；此项永不单独触发限制。"),
    }


def _worlds(case: SemanticCase, signals: dict[str, Signal]) -> list[WorldHypothesis]:
    s = {k: v.score for k, v in signals.items()}
    protected = case.content_role in PROTECTED_ROLES
    raw = {
        "benign_support": 0.33 + 0.42 * s["repair_capacity"] + (0.18 if case.content_role in {"personal_experience", "advice"} else 0.0),
        "incomplete_simplification": 0.17 + 0.72 * s["context_truncation"],
        "negligent_misinformation": 0.10 + 0.68 * s["evidence_gap"] + 0.20 * s["unverifiability"],
        "commercial_manipulation": 0.06 + 0.65 * s["commercial_capture"] + 0.24 * s["manipulation_pressure"],
        "deliberate_deception": 0.01 + (0.80 if case.verified_fabrication else 0.0),
        "protected_adverse_truth": 0.06 + (0.90 if protected else 0.0) + 0.16 * case.source_traceability,
    }
    # deliberate_deception intentionally stays low without verified fabrication.
    if not case.verified_fabrication:
        raw["deliberate_deception"] = 0.01 + 0.06 * s["manipulation_pressure"]
    weights = normalize_weights(raw)
    templates = {
        "benign_support": ("善意但有限的支持或个人经验", ["补充适用条件后风险可显著下降"], ["出现隐瞒、强迫或被证明虚假的核心事实"]),
        "incomplete_simplification": ("语境不足的简化表达", ["存在普遍化、角色遗漏或因果跳跃"], ["补齐条件、反例和各方责任后结论仍保持稳定"]),
        "negligent_misinformation": ("未经充分核验的错误或误导", ["强结论与证据来源不匹配"], ["高质量独立证据支持核心主张且边界明确"]),
        "commercial_manipulation": ("以知识外观包装的商业操纵", ["付费漏斗、紧迫压力和证据缺口同时出现"], ["价格、证据、退款、适用边界和利益冲突完全透明"]),
        "deliberate_deception": ("有意欺骗", ["只有经核实的伪造或故意隐瞒才可提高此假设"], ["无法证明主观故意，或新证据支持善意错误"]),
        "protected_adverse_truth": ("受保护的批评、揭弊、坏消息或痛苦表达", ["内容角色属于批评、揭弊或痛苦表达"], ["独立证据证明其包含具体欺诈、威胁或违法伤害"]),
    }
    return [
        WorldHypothesis(key=key, label_cn=templates[key][0], weight=round(weights[key], 4), supporting_reasons=templates[key][1], falsifiers=templates[key][2])
        for key in sorted(weights, key=weights.get, reverse=True)
    ]


def _interventions(case: SemanticCase, signals: dict[str, Signal], protected: bool, high_impact: bool) -> tuple[str, list[dict[str, Any]], list[str]]:
    s = {k: v.score for k, v in signals.items()}
    risk = clamp(
        0.18 * s["evidence_gap"] + 0.16 * s["context_truncation"]
        + 0.18 * s["manipulation_pressure"] + 0.12 * s["addiction_design"]
        + 0.12 * s["vulnerability_exploitation"] + 0.12 * s["zero_sum_risk"]
        + 0.12 * s["unverifiability"]
    )
    exposure = clamp(0.60 + 0.25 * case.reach + 0.15 * case.repetition)
    effective = clamp(risk * exposure - 0.18 * s["repair_capacity"])
    reasons: list[str] = []
    actions: list[dict[str, Any]] = []

    if protected and not case.verified_fabrication and not case.imminent_harm_or_illegal:
        decision = Decision.PROTECT.value
        actions.extend([
            {"layer": "distribution", "action": "do_not_restrict_for_negative_tone", "automatic": True},
            {"layer": "reader", "action": "offer_optional_context_and_sources", "automatic": True},
        ])
        reasons.append("PROTECTED_CRITICISM_WHISTLEBLOWING_OR_DISTRESS")
    elif case.imminent_harm_or_illegal:
        if case.authorized_human_review:
            decision = Decision.AUTHORIZED_REMOVAL.value
            actions.append({"layer": "authority", "action": "lawful_time_bounded_removal_or_access_restriction", "automatic": False})
            reasons.append("IMMINENT_HARM_OR_ILLEGALITY_WITH_AUTHORIZED_REVIEW")
        else:
            decision = Decision.HUMAN_REVIEW.value
            actions.append({"layer": "authority", "action": "urgent_human_review_and_evidence_preservation", "automatic": False})
            reasons.append("IMMINENT_HARM_REQUIRES_AUTHORIZED_HUMAN")
    elif case.verified_harm:
        decision = Decision.CORRECT_REPAIR.value
        actions.extend([
            {"layer": "platform", "action": "propagate_correction_to_prior_recipients", "automatic": False},
            {"layer": "remedy", "action": "calculate_verified_repair_and_restitution", "automatic": False},
        ])
        reasons.append("VERIFIED_HARM_REQUIRES_CORRECTION_AND_REPAIR")
    elif high_impact and (s["evidence_gap"] > 0.40 or s["unverifiability"] > 0.40):
        decision = Decision.HUMAN_REVIEW.value
        actions.extend([
            {"layer": "reader", "action": "high_visibility_uncertainty_card", "automatic": True},
            {"layer": "distribution", "action": "temporary_recommendation_limit_pending_review", "automatic": False},
        ])
        reasons.append("HIGH_IMPACT_EVIDENCE_GAP")
    elif case.monetized and s["commercial_capture"] > 0.28:
        decision = Decision.PAUSE_MONETIZATION.value
        actions.extend([
            {"layer": "commerce", "action": "pause_paid_amplification_or_affiliate_conversion_pending_review", "automatic": False},
            {"layer": "creator", "action": "request_evidence_conflict_and_refund_boundaries", "automatic": True},
        ])
        reasons.append("MONETIZED_CLAIM_WITH_MANIPULATIVE_PRESSURE")
    elif effective >= 0.55:
        decision = Decision.DEAMPLIFY.value
        actions.extend([
            {"layer": "reader", "action": "context_card_and_share_confirmation", "automatic": True},
            {"layer": "distribution", "action": "reduce_algorithmic_amplification_pending_review", "automatic": False},
        ])
        reasons.append("MULTI_DIMENSION_SEMANTIC_HARM_RISK")
    elif effective >= 0.32:
        decision = Decision.FRICTION.value
        actions.extend([
            {"layer": "reader", "action": "show_context_card_before_reshare", "automatic": True},
            {"layer": "creator", "action": "offer_balanced_rewrite", "automatic": True},
        ])
        reasons.append("CONTEXT_AND_MANIPULATION_RISK")
    elif effective >= 0.15:
        decision = Decision.CONTEXT.value
        actions.append({"layer": "reader", "action": "optional_context_card", "automatic": True})
        reasons.append("LIMITED_CONTEXT_OR_EVIDENCE")
    else:
        decision = Decision.ALLOW.value
        actions.append({"layer": "distribution", "action": "no_restriction", "automatic": True})
        reasons.append("NO_MATERIAL_SEMANTIC_HARM_SIGNAL")

    if s["addiction_design"] > 0.28:
        actions.append({"layer": "interface", "action": "disable_autoplay_infinite_scroll_or_variable_reward_by_default", "automatic": True})
        reasons.append("ADDICTIVE_DESIGN_FRICTION")
    if s["zero_sum_risk"] > 0.32:
        actions.append({"layer": "relationship", "action": "generate_non_zero_sum_repair_card", "automatic": True})
        reasons.append("ZERO_SUM_RELATIONAL_FRAMING")
    if any(a["action"].startswith("reduce_") or a["action"].startswith("pause_") or "removal" in a["action"] for a in actions):
        actions.append({"layer": "due_process", "action": "notice_reason_codes_appeal_and_expiry", "automatic": False})
    return decision, actions, reasons


def analyze(case: SemanticCase) -> AnalysisResult:
    case.normalized()
    signals = _extract_signals(case)
    protected = case.content_role in PROTECTED_ROLES
    high_impact = case.domain in HIGH_IMPACT_DOMAINS or bool(set(case.audience_context) & {"minor", "acute_distress", "financial_crisis"})
    worlds = _worlds(case, signals)
    decision, interventions, reasons = _interventions(case, signals, protected, high_impact)
    repair = build_repair_card(case, signals)

    restriction = decision in {
        Decision.DEAMPLIFY.value,
        Decision.PAUSE_MONETIZATION.value,
        Decision.AUTHORIZED_REMOVAL.value,
        Decision.CORRECT_REPAIR.value,
    }
    invariants = {
        "negative_affect_alone_never_restricts": not (
            restriction and all(signals[k].score < 0.12 for k in signals if k not in {"negative_affect", "repair_capacity"})
        ),
        "protected_expression_not_removed_without_independent_harm_basis": not (
            protected and decision == Decision.AUTHORIZED_REMOVAL.value and not case.imminent_harm_or_illegal
        ),
        "high_impact_restriction_requires_human_process": not restriction or any(not a["automatic"] for a in interventions),
        "no_person_level_moral_score": True,
        "external_action_authority_zero": True,
        "appeal_required_for_adverse_distribution_or_monetization_action": (not restriction) or case.appeal_available,
        "deliberate_deception_not_inferred_without_verified_fabrication": (not case.verified_fabrication) and next(w.weight for w in worlds if w.key == "deliberate_deception") < 0.15 or case.verified_fabrication,
    }
    confidence = clamp(0.38 + 0.22 * case.source_traceability + 0.20 * case.evidence_quality + 0.20 * (1.0 - signals["unverifiability"].score))
    limitations = [
        "该结果是透明启发式风险分析，不是事实核查结论、心理诊断或恶意认定。",
        "文本模式不能可靠推断作者主观意图；故意欺骗只能由独立证据提高。",
        "高影响领域需要领域专家、适用法律和现实证据复核。",
        "对传播或变现的不利措施必须有通知、理由、期限和申诉。",
    ]
    provenance = {
        "engine": "DIKWP Semantic Immunity & Repair OS",
        "version": VERSION,
        "method": "transparent_rules_plural_worlds_context_repair",
        "ai_origin_declared": case.ai_origin,
        "external_network_used": False,
        "input_digest": digest_json(asdict(case)),
    }
    return AnalysisResult(
        version=VERSION,
        case_digest=provenance["input_digest"],
        decision=decision,
        confidence=round(confidence, 4),
        protected_expression=protected,
        high_impact=high_impact,
        signals=signals,
        worlds=worlds,
        interventions=interventions,
        repair_card=repair,
        reason_codes=reasons,
        limitations=limitations,
        invariants=invariants,
        provenance=provenance,
    )

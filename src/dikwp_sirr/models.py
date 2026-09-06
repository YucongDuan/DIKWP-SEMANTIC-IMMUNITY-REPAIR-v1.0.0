from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class Domain(str, Enum):
    GENERAL = "general"
    FAMILY = "family_parenting"
    HEALTH = "health"
    FINANCE = "finance"
    EDUCATION = "education"
    POLITICS = "politics_public_interest"
    RELATIONSHIPS = "relationships"
    COMMERCIAL_KNOWLEDGE = "commercial_knowledge"


class ContentRole(str, Enum):
    ADVICE = "advice"
    PERSONAL_EXPERIENCE = "personal_experience"
    CRITICISM = "criticism"
    WHISTLEBLOWING = "whistleblowing"
    MARKETING = "marketing"
    NEWS = "news"
    EDUCATION = "education"
    ENTERTAINMENT = "entertainment"
    DISTRESS_EXPRESSION = "distress_expression"


class Decision(str, Enum):
    PROTECT = "PROTECT_NEGATIVE_TRUTH_OR_DISTRESS"
    ALLOW = "ALLOW"
    CONTEXT = "ADD_CONTEXT_CARD"
    FRICTION = "ADD_SHARING_FRICTION"
    DEAMPLIFY = "REDUCE_RECOMMENDER_AMPLIFICATION_PENDING_REVIEW"
    PAUSE_MONETIZATION = "PAUSE_MONETIZATION_PENDING_REVIEW"
    HUMAN_REVIEW = "HUMAN_REVIEW_HIGH_RISK"
    AUTHORIZED_REMOVAL = "AUTHORIZED_REMOVAL_FOR_ILLEGAL_OR_IMMINENT_HARM"
    CORRECT_REPAIR = "CORRECTION_PROPAGATION_AND_RESTITUTION"


@dataclass(slots=True)
class SemanticCase:
    text: str
    domain: str = Domain.GENERAL.value
    content_role: str = ContentRole.ADVICE.value
    channel: str = "post"
    audience_context: list[str] = field(default_factory=list)
    monetized: bool = False
    paid_funnel: bool = False
    evidence_quality: float = 0.25
    source_traceability: float = 0.25
    reach: float = 0.35
    repetition: float = 0.25
    ai_origin: str = "unknown"
    addictive_features: list[str] = field(default_factory=list)
    verified_fabrication: bool = False
    verified_harm: bool = False
    imminent_harm_or_illegal: bool = False
    authorized_human_review: bool = False
    creator_notified: bool = False
    appeal_available: bool = True
    notes: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SemanticCase":
        allowed = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in allowed})

    def normalized(self) -> "SemanticCase":
        for name in ("evidence_quality", "source_traceability", "reach", "repetition"):
            setattr(self, name, max(0.0, min(1.0, float(getattr(self, name)))))
        self.text = self.text.strip()
        return self


@dataclass(slots=True)
class Signal:
    name: str
    score: float
    markers: list[str]
    explanation: str


@dataclass(slots=True)
class WorldHypothesis:
    key: str
    label_cn: str
    weight: float
    supporting_reasons: list[str]
    falsifiers: list[str]


@dataclass(slots=True)
class RepairCard:
    useful_core: str
    omitted_context: list[str]
    vulnerable_misreadings: list[str]
    balanced_rewrite: str
    verification_questions: list[str]
    next_actions: list[str]
    affected_parties: list[str]


@dataclass(slots=True)
class AnalysisResult:
    version: str
    case_digest: str
    decision: str
    confidence: float
    protected_expression: bool
    high_impact: bool
    signals: dict[str, Signal]
    worlds: list[WorldHypothesis]
    interventions: list[dict[str, Any]]
    repair_card: RepairCard
    reason_codes: list[str]
    limitations: list[str]
    invariants: dict[str, bool]
    provenance: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

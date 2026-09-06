from __future__ import annotations

# Transparent, deliberately small seed lexicons. They identify linguistic risk
# indicators, not truth or malicious intent. Deployments should localize and audit.
LEXICONS: dict[str, tuple[str, ...]] = {
    "universalism": (
        "一定", "所有人", "任何人", "从来都是", "永远", "绝对", "唯一", "必须", "根本不需要", "都应该", "不需要医生",
        "everyone", "always", "never", "the only way", "must", "guaranteed", "absolutely",
    ),
    "certainty": (
        "科学已经证明", "事实就是", "毫无疑问", "百分之百", "保证", "必然", "真相只有一个", "唯一真相",
        "science proves", "without doubt", "100%", "guarantee", "certainly", "proven fact",
    ),
    "urgency": (
        "马上", "立刻", "最后机会", "错过就", "赶紧", "仅限今天", "再不", "现在就",
        "act now", "last chance", "limited time", "before it is too late", "immediately",
    ),
    "authority_laundering": (
        "专家都说", "权威认证", "内部人士", "内部消息", "顶级专家", "研究表明", "官方都不敢说",
        "experts agree", "insiders say", "secret research", "authorities do not want you to know",
    ),
    "identity_coercion": (
        "真正的女人", "真正的男人", "好妈妈就", "好妻子就", "聪明人都", "不这样就是不爱",
        "real women", "real men", "good mothers", "smart people all", "if you cared you would",
    ),
    "zero_sum": (
        "你赢他就输", "只能先顾自己", "先好好照顾自己才能照顾孩子", "不要管别人", "男人和女人天生对立", "夫妻就是博弈",
        "win or lose", "choose yourself over everyone", "men versus women", "zero-sum",
    ),
    "shaming": (
        "低认知", "没脑子", "废物", "活该", "不配", "蠢", "弱者", "loser", "stupid", "deserve it",
    ),
    "causal_leap": (
        "所以一定会", "直接导致", "只要就", "根本原因就是", "这证明了", "因此所有",
        "therefore it causes", "this proves", "all you need is", "the root cause is simply",
    ),
    "monetization": (
        "报名", "课程", "训练营", "私聊", "购买", "咨询", "付费", "下单", "链接", "名额",
        "buy now", "course", "coaching", "DM me", "subscribe", "paid program", "limited seats",
    ),
    "self_sealing": (
        "不相信说明你被洗脑", "质疑就是认知低", "反对者都是既得利益", "只有觉醒的人懂",
        "if you disagree you are brainwashed", "critics prove the point", "only the awakened understand",
    ),
    "conspiracy": (
        "他们不想让你知道", "被隐藏的真相", "全网封杀", "资本控制一切", "幕后黑手",
        "they do not want you to know", "hidden truth", "cover-up", "secret cabal",
    ),
    "qualifiers": (
        "可能", "在某些情况下", "取决于", "不一定", "对部分人", "需要结合", "证据有限", "尚不清楚",
        "may", "in some cases", "depends on", "not always", "for some people", "evidence is limited",
    ),
    "context_markers": (
        "同时", "另一方面", "前提", "边界", "例外", "反例", "需要考虑", "不同家庭", "具体情况",
        "however", "on the other hand", "assumption", "boundary", "exception", "counterexample",
    ),
    "rights_markers": (
        "可以拒绝", "可以退出", "知情同意", "共同责任", "可申诉", "可更正", "不应强迫",
        "may refuse", "can opt out", "informed consent", "shared responsibility", "appeal",
    ),
    "family_roles": (
        "孩子", "母亲", "妈妈", "父亲", "爸爸", "丈夫", "妻子", "夫妻", "照护者", "家庭",
        "child", "mother", "father", "husband", "wife", "caregiver", "family",
    ),
    "health_claims": (
        "治愈", "疗效", "停药", "诊断", "抑郁", "焦虑", "癌症", "药物", "疫苗", "医生",
        "cure", "stop medication", "diagnosis", "depression", "cancer", "vaccine", "doctor",
    ),
    "financial_claims": (
        "稳赚", "保本", "翻倍", "内幕", "投资", "收益", "贷款", "财富自由",
        "risk-free", "guaranteed return", "double your money", "insider", "investment",
    ),
}

ADDICTIVE_FEATURE_WEIGHTS: dict[str, float] = {
    "infinite_scroll": 0.24,
    "autoplay": 0.18,
    "variable_reward": 0.24,
    "streaks": 0.13,
    "read_receipts_pressure": 0.08,
    "aggressive_notifications": 0.16,
    "social_comparison_rank": 0.17,
    "forced_continuation": 0.21,
}

HIGH_IMPACT_DOMAINS = {"health", "finance", "politics_public_interest"}
PROTECTED_ROLES = {"criticism", "whistleblowing", "distress_expression"}

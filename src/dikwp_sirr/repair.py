from __future__ import annotations

from .models import RepairCard, SemanticCase, Signal


def _family_repair(case: SemanticCase) -> RepairCard:
    return RepairCard(
        useful_core="照护者长期耗竭会削弱照护质量，因此照护者获得基本休息、支持和尊重是合理需要。",
        omitted_context=[
            "孩子在不同年龄和安全状态下具有不可取消的基本照护需要。",
            "自我照顾需要与父母共同责任、可用资源、工作负担和照护替代安排一起讨论。",
            "一方的恢复不能自动成为另一方无限加班或孩子失去稳定照护的理由。",
            "家庭冲突可能来自资源不足和责任分配，而不只是某个人‘不会爱自己’。",
            "存在暴力、控制或严重耗竭时，需要不同于一般家庭分工建议的安全路径。",
        ],
        vulnerable_misreadings=[
            "把‘照顾自己’理解为任何情况下个人需要都优先于孩子基本需要。",
            "把照护耗竭完全归咎于女性自己，而忽略伴侣、家庭和公共支持责任。",
            "把夫妻关系改写成一方争取自由、另一方必然受损的零和博弈。",
            "以一句口号替代对时间、睡眠、金钱、照护和安全的具体安排。",
        ],
        balanced_rewrite=(
            "照护者需要基本休息、健康和被支持，孩子也需要稳定、安全和持续的照护。"
            "家庭应把两者作为共同目标，明确父母或支持者各自承担什么、最低不能缺少什么、"
            "谁提供替代照护，以及一周后如何检查安排是否让任何一方持续受损。"
        ),
        verification_questions=[
            "这句话适用于什么年龄、健康和家庭条件？",
            "孩子不可妥协的基本需要是什么？",
            "伴侣或其他照护者承担哪些明确责任？",
            "所谓‘照顾自己’具体是休息、医疗、社交、消费还是退出责任？",
            "安排是否可逆，谁承担新增时间和金钱成本？",
            "一周后的现实指标是什么：睡眠、冲突、孩子状态还是照护负担？",
        ],
        next_actions=[
            "制定七天共同照护表：孩子基本需要、双方最低恢复时间、替代照护和紧急联系人。",
            "把争论从‘谁更自私’改成‘现有资源下怎样避免任何一方耗竭和孩子受损’。",
            "若存在暴力、严重精神健康危机或儿童安全问题，跳过一般沟通卡并寻求当地专业支持。",
        ],
        affected_parties=["照护者本人", "孩子或其他依赖者", "伴侣/共同照护者", "可提供支持的家庭与公共系统"],
    )


def build_repair_card(case: SemanticCase, signals: dict[str, Signal]) -> RepairCard:
    text = case.text
    if case.domain == "family_parenting" or any(token in text for token in ("孩子", "妈妈", "母亲", "夫妻", "照顾自己")):
        return _family_repair(case)

    omitted: list[str] = []
    if signals["evidence_gap"].score > 0.25:
        omitted.append("核心主张的来源、证据质量、反例和可推翻条件。")
    if signals["context_truncation"].score > 0.25:
        omitted.append("结论成立的对象、时间、地域、资源和例外条件。")
    if signals["commercial_capture"].score > 0.20:
        omitted.append("作者或平台的付费关系、佣金、退款和利益冲突。")
    if signals["zero_sum_risk"].score > 0.20:
        omitted.append("所有受影响方的最低需要、共同责任和非零和方案。")
    if not omitted:
        omitted.append("建议补充一个反例、一个适用边界和一个现实验证步骤。")

    misreadings = [
        "把条件性建议理解成适用于所有人的绝对规则。",
        "把个人经验误当作因果证明或普遍事实。",
    ]
    if signals["manipulation_pressure"].score > 0.25:
        misreadings.append("在紧迫、羞耻或身份压力下跳过核验并立即行动。")
    if case.monetized:
        misreadings.append("把购买产品或课程误当作已经获得能力或结果。")

    rewrite = (
        "这是一项有条件的观点或建议，而不是对所有人的普遍规律。"
        "在采取行动前，应说明适用对象、证据来源、可能反例、成本与受影响方；"
        "先进行一个低风险、可撤销的小规模现实测试，并根据结果修订。"
    )
    return RepairCard(
        useful_core="内容可能包含值得保留的问题意识或局部经验，但其适用范围需要单独验证。",
        omitted_context=omitted,
        vulnerable_misreadings=misreadings,
        balanced_rewrite=rewrite,
        verification_questions=[
            "这是事实、解释、价值判断、个人经验还是销售承诺？",
            "什么证据能支持它，什么观察会推翻它？",
            "对谁成立，对谁可能不成立？",
            "谁从我相信或转发这条内容中获益？",
            "最小可逆验证步骤是什么？",
        ],
        next_actions=[
            "查找至少一个独立来源和一个有力反例。",
            "在分享前加入适用边界与不确定性说明。",
            "若涉及健康、金融、法律或公共利益，交由具名专业人员复核。",
        ],
        affected_parties=["阅读者", "内容创作者", "被内容描述或影响的人", "传播平台或现实关系网络"],
    )

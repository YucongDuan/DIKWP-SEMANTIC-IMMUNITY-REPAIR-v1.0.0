# SIRR 数学基础

## 1. 语义行为

\[
a=(x,m,c,u,p,r,t)
\]

其中：主体 \(x\)、消息 \(m\)、情境 \(c\)、受众 \(u\)、Purpose \(p\)、传播机制 \(r\)、时间 \(t\)。同一句话在不同受众、商业关系和传播机制中不是同一个语义行为。

## 2. 风险向量

\[
\mathbf h(a)=(E,C,M,A,V,Z,U,B)
\]

- \(E\)：证据缺口；
- \(C\)：语境截断；
- \(M\)：操纵压力；
- \(A\)：成瘾设计；
- \(V\)：情境脆弱性利用；
- \(Z\)：零和对立；
- \(U\)：不可验证性；
- \(B\)：商业捕获。

负面情绪 \(N\) 单独保留：

\[
N\notin DecisionFeatures_{restriction}
\]

## 3. 证据缺口

\[
E=0.55S_c(1-q_e)+0.30(1-q_s)+0.15A_l(1-q_s)
\]

其中 \(S_c\) 为主张强度，\(q_e\) 为证据质量，\(q_s\) 为来源可追溯性，\(A_l\) 为权威借用强度。

## 4. 语境截断

\[
C=clip(0.34U_n+0.22L_c+0.27Z_f+0.17I_c+F_o-0.18Q-0.18K-0.10R)
\]

其中普遍化、因果跳跃、零和框架和身份强迫提高风险；限定语、反例、语境和权利说明降低风险。

## 5. 有效语义伤害负荷

\[
Risk=\sum_i w_i h_i
\]

\[
Exposure=0.60+0.25Reach+0.15Repetition
\]

\[
SHL=clip(Risk\cdot Exposure-0.18RepairCapacity)
\]

该标量只用于选择干预层级，不得替代风险向量，也不得用于人员排名。

## 6. 多世界解释

\[
\mathbb W=\{W_b,W_i,W_n,W_c,W_d,W_p\}
\]

分别对应善意支持、简化遗漏、疏忽误导、商业操纵、故意欺骗和受保护的负面真相。权重是解释强度，不是犯罪概率。

## 7. 干预优化

\[
a^*=\arg\min_a SHL(a)
\]

受以下约束：

\[
ProtectedExpressionLoss(a)\le\epsilon
\]

\[
AdverseAction(a)\Rightarrow Notice\land Reason\land Expiry\land Appeal
\]

\[
HighImpact(a)\Rightarrow NamedHumanAuthority
\]

\[
ExternalAutomaticAuthority=0
\]

## 8. 关系非零和修复

对关系中的主体集合 \(P\)，每个主体具有最低需要向量 \(n_i\)、责任向量 \(d_i\) 和资源约束 \(r_i\)。修复不最大化某一方主观效用，而先满足：

\[
\forall i,\quad NeedFloor_i\ge \tau_i
\]

然后最小化：

\[
BurdenInequality+UnassignedDuty+IrreversibleHarm
\]

这使“先照顾自己”被转换成可观察的时间、责任、替代照护和复盘安排。

## 9. 纠错闭环

\[
Wrong(d)\Rightarrow \Diamond(Restore\land Correct\land Notify\land Repair\land Revise)
\]

删除错误标签不是完整纠错。原接收者、现实机会和规则模型都必须进入修复。

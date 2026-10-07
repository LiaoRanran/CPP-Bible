# 686 · A2 最可能被 reviewer 攻击的 5 个点

- **批次**：686 ｜ **承接**：`686_self_critique.md`（23 条硬伤，按严重度排序）
- **选取标准**：致命/严重度 + 出现概率高 + 现有回应是否足够。

---

## 攻击点 1 〔致命〕"你的演化算子没有任何显著增益——'演化'这个核心贡献是空的？"

> **Reviewer 语气**：The paper is titled "Evolving Verifiers", yet your executable evolution operator beats the plain frequency-based FD selection in only 3 of 14 (pool, k) tiers, and the best case (+1.41pp, p=0.302) is not significant. Where is the empirical payoff of "evolution"?

**现有回应（基于数据）**：我们从不声称演化的召回增益。算子 E 的设计目标是**可证伪性**——它把"失败→规则→重测"链显式化并暴露两个规格坍缩（literal `novel≡failure`、`frequency≡FD`）。其"非显著"本身就是诚实结果：若算子显著优于 FD，反而说明我们选择机制有冗余；我们已把 claim 钉在"方向证据"而非"召回提升"。

**回应是否足够**：**部分足够，但标题叙事与证据张力仍会被追问**。必须在标题/贡献句显式降级为"演化提供可证伪的评估装置框架"，不再隐含"演化更好"。

**缺口 / 建议**：补一项**真实演化增益实验**——需要跨轮失败驱动轨迹（683 真实靶场可能提供：比较"带演化算子重排"vs"静态 FD"在真实缺陷上的逐轮召回曲线）。若 683 无此轨迹，则在局限中明确"演化召回增益未被本实验证实"。

---

## 攻击点 2 〔严重·U〕"1137 vs 1147，你的样本量自相矛盾"

> **Reviewer 语气**：In §6 you report 1137 samples in the A5 matrix, but in the capability-boundary section you use 1147. Are these the same population? If not, which number is authoritative?

**现有回应**：两者是**同一批样本的两种口径**——A5 矩阵为去重 10 条后的 1137；676g 能力边界为去重前的全集 1147（含 64 corpus-null + 74 source-derived-reconstruction）。差异仅 10 条，源于去重。

**回应是否足够**：**目前论文未显式澄清**，属本批新发现（#1）。仅当审稿人自己发现并质疑时才被动回应，风险高。

**缺口 / 建议**：**主动加脚注**（在方法论与能力边界段各一处）："676g 在 1137 去重之前的全集为 1147；A5 矩阵为去重后 1137，二者同一总体、两种口径，非矛盾。" 这是低成本的"先发制人"修复。

---

## 攻击点 3 〔中等〕"p=2.3×10⁻⁴¹ 听起来像大赢，但你的真实效应只有 ~10pp，而且主要来自池构成"

> **Reviewer 语气**：A p-value of 10⁻⁴¹ suggests a home run, but your mechanistic effect is only +7-12pp and the headline +24pp is mostly pool composition (two degenerate assets in the random draw). Isn't the "selection is smarter" claim overstated?

**现有回应**：我们已在正文**并排**报告全池 +24.0pp 与机制 +7-12pp（非退化池 k≤3 显著），并把 +24pp 拆为"+12pp 池构成 + 7-12pp 选择效应"。我们明确**不写 "FD>Random"**，结论停在方向证据。p 小是 n 大（有效 n≈133-140）与 c=0 结构的结果，不代表巨大效应；我们始终报效应量 + CI。

**回应是否足够**：**足够，但依赖摘要是否真的并排**。需核验摘要/贡献句措辞（见 #4）。

**缺口 / 建议**：核验 tex 摘要（建议 grep L76-99）确保 +24pp 与 +7-12pp 同句出现；CI 统一按 cluster 宽度（[+16.6,+30.4]）而非 naive（[+20.51,+27.55]）。

---

## 攻击点 4 〔严重〕"单标注者 + 你的 κ=0.727，标签到底可信吗？"

> **Reviewer 语气**：Your labels are self-produced with zero second annotators (T17), and you mention κ=0.727 — so the labels ARE validated? Or aren't they?

**现有回应**：**κ=0.727 是 AI 重标（35 类 defect_type，n=287），不是人类 IRR**——T17（无人类第二标注者）**仍然开放**，我们从未声称标签已验证。本批 B3 反事实证明：即使标签以 15% 概率翻转，FD-vs-Random 的**结论方向不反转**（Δ 仍 24-27pp 为正），但**绝对盲区率敏感**（6.6%→14.3%）——这正是我们主动登记 T17 的原因。已规划预注册人类双标注 + κ<0.6 全复核。

**回应是否足够**：**足够，关键是绝不把 κ=0.727 说成人类 IRR**。本批 B3 给了"标签噪声下结论稳健"的量化证据，强化回应。

**缺口 / 建议**：在 rebuttal 与论文中明确区分"AI 重标 κ"与"人类 IRR 缺失"；B3 的 15% 鲁棒性可作为 T17 的缓解证据（但不可作为标签已验证的证明）。

---

## 攻击点 5 〔致命〕"脱离 WSL 就复现不了（35%→10%），这算可复现吗？"

> **Reviewer 语气**：Without the specific WSL environment 15 samples degrade to 'unknown' and external recall drops 35%→10% while your guard stays green. Is this reproducible at all?

**现有回应**：**有效说是"条件复现"**——我们已把环境依赖记为观察到的失败（非残留），并在 `REPRODUCE.md` + `docker/paper/run_all.sh` 加入 **fail-loud 自检**：错误环境下脚本**抛错**而非静默降级（旧 35%→10% 静默掉分已封堵）。同时明确声明 macOS/Windows-native 不可复现。剩余项=让 guard **重跑探测器**以使 caliber/测量分歧无法保持绿。我们**仍不声称数字在声明环境外可复现**。

**回应是否足够**：**足够且诚实**，但"条件复现"在 E&D 赛道仍是减分项；fail-loud 已落地是加分。

**缺口 / 建议**：路线图落地 guard 重跑探测器；本批无新实验，仅需论文保持"条件复现"措辞一致（不得升级为"完全可复现"）。

---

## 小结

| 攻击点 | 严重度 | 现有回应是否足够 | 本批可修？ |
|---|---|---|---|
| 1 演化算子无增益 | 致命 | 部分（需降级标题叙事）| 否（需 683 轨迹）|
| 2 1137/1147 矛盾 | 严重·U | 不足（未主动澄清）| 否（需作者加脚注）|
| 3 p 小效应小/池构成 | 中等 | 足够（需核验摘要）| 否（核验 tex）|
| 4 单标注者/κ | 严重 | 足够（需澄清 κ 口径）| 部分（B3 证据）|
| 5 条件复现 | 致命 | 足够（保持措辞）| 否（guard 重跑 future）|

> 五个点中 **#2（1137/1147）是本批新发现且最便宜可修**；**#1（演化算子）是最实质的叙事风险**。两者都建议在下一次论文批次优先处理。

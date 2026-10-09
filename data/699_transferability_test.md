# 699-C · 测量漂移代数 → LLM 评估 迁移性预测试报告

> 目的：最小可行性测试 Queyi 的三个核心概念（口径漂移 / 环境漂移 / 结构性 Goodhart）能否迁移到 LLM 评估。
> 生成日期：2026-10-09 · 原始结果 `699_llm_drift_results.json` · 脚本 `tools/compute_699_llm_drift.py`

## 0. 诚实边界

- 本预测试**只实测了"结构性 Goodhart"**（用长度/信息量作为懒惰裁判，在真实下载的 240 条数据上计算）。
- **口径漂移（prompt invariance）与环境漂移（model invariance）需要真实 LLM 裁判**（GLM/DeepSeek 等端点 + key）。本环境未配置可用 key，故这两项返回 `None`，函数已就绪，仅需填端点即可实测。
- 与 Queyi C++ 数据的对比基线来自 **692 批 LLM 臂**；本 checkout 无 `data/692_*` 产物（见任务书诚实边界），相关数字须回填，下表仅占位。

## 1. 结构性 Goodhart（实测，真实数据）

方法：对每条 pairwise 样本，用"选更长的回答"作为懒惰裁判，比较其选择与人工标注（人类偏好侧）是否一致。若不一致，则该样本是"优化长度 ≠ 真实质量"的结构性 Goodhart 实例。

| 数据集 | n | 长度裁判一致率 | 结构性 Goodhart 率 | 人类侧更长占比 |
|--------|---|--------------|-------------------|---------------|
| **JudgeBench** | 120 | **0.4417** | **0.5583** | 0.45 |
| **RewardBench** | 120 | **1.0000** | **0.0000** | 1.00 |

**解读（关键发现）：**
- **JudgeBench**：长度裁判与人类一致率仅 44%，即 **56% 的样本上"更长"会误导判断**——这正对应 Queyi 在 C++ sanitizer 上发现的"能力按族分化 / 代理指标不可信"现象。长度是一个**强但错误的代理**，在 JudgeBench 这类"两回答质量接近"的困难样本上尤其危险。→ **结构性 Goodhart 概念直接迁移且显著。**
- **RewardBench**：长度裁判 100% 一致，因为 chosen 被策展为"更好且更长"。这本身是 reward modeling 中著名的**长度偏置混淆**的来源：RewardBench 的构造让"长度"成为质量的完美（却无信息量的）代理。→ 这印证了 Queyi 的论点：**当评估口径与真值口径耦合时，漂移被掩盖；必须解耦测量。**

## 2. 口径漂移 / 环境漂移（脚本就绪，待 LLM 裁判）

`tools/compute_699_llm_drift.py::invariance()` 已实现：
- `kind="prompt"`：同一回答 + 两个语义等价 judge prompt → verdict 一致率（prompt invariance）。
- `kind="model"`：同一 prompt+回答 + 两个 judge 模型 → verdict 一致率（model invariance）。
设置 `LLM_JUDGE_ENABLED=True` 并提供 `QUEYI_LLM_JUDGE_ENDPOINT` / `QUEYI_LLM_JUDGE_KEY` 即可实测。本环境无 key，结果为 `None`。

## 3. 与 Queyi C++ 数据对比（待回填 692 产物）

| 概念 | Queyi C++（692 LLM 臂，待回填） | LLM 评估（本批实测/待实测） | 迁移判断 |
|------|-------------------------------|----------------------------|----------|
| 结构性 Goodhart | LLM 失败拓扑与 sanitizer 正交（692 结论） | JudgeBench 56% / RewardBench 0%（实测） | **直接迁移，且量级显著** |
| 口径漂移 | prompt invariance 87.5%（未过 ≥0.9，692） | 待 LLM 裁判实测 | 方法可直接套用 |
| 环境漂移 | — | 待 LLM 裁判实测 | 方法可直接套用 |

## 4. 结论（初步，非证明）

- **可直接迁移**：结构性 Goodhart 在 LLM 评估中清晰存在且可被同一套代数度量；JudgeBench 的 56% 长度误导率是最干净的证据。
- **需改造**：口径/环境漂移在这里需要"LLM 裁判"作为被测对象，而非 C++ 静态分析器；测量代数形式不变，但"检测器"换成 judge prompt / judge 模型。
- **未声称**：本批不构成"已证明可迁移"，仅为最小可行性预测试（符合任务书诚实边界）。完整实验需在可联网、有 LLM key 的环境跑 `invariance()` 并回填 692 基线。

## 5. Top 结构性 Goodhart 实例

见 `699_llm_drift_results.json → top_structural_goodhart_cases`（人类偏好侧反而更短、长度裁判会判错的 10 条样本）。

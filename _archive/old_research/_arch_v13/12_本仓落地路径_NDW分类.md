# 12 · 本仓落地路径（NDW 分类）

## 12.1 关键路径（综合维度 1–11）

```
N1 候选攻击边自动生成 (MIS 关联种子)        [已做探针]
N2 攻击强度/可信度度量 (既有字段为主)        [已做探针：词汇度量不可用，改用 cred 字段]
   │
   ▼
D1 人审确认候选边 (accept/reject/改强度)     [需人时，小时级]
D2 mutation 反例验证 (overturned_events)     [需先 populate 数据]
   │
   ▼
W2 加权 grounded 实测 → IN/OUT/UNDEC
   │
   ▼
发布门槛校验 → grounded 层上线
```

## 12.2 NDW 分类

- **N（现在能做，零 Oracle 风险）**：
  - 候选攻击边自动生成（MIS `related_atoms`/`misconceptions`，本探针 194 单向边）
  - 攻击强度度量（词汇，已证不可用→改 cred 字段）
  - W2 可信度加权 grounded 求解器（已做，非退化）
  - Bipolar 支持边加成（已做）
  - 攻击边 consequence 模型级反例（已做）
- **D（攒数据）**：
  - 人审逐条确认候选边（维度 9，工作量小时级）
  - LLM 辅助标注验证（维度 5，需外部模型）
  - mutation 反例验证（需 populate `overturned_events.jsonl`）
- **W（等条件）**：
  - 概率 AF（#P 复杂度，维度 3）
  - preferred/stable（NP-完全，维度 11）
  - embedding 相似度（外部依赖，维度 6）
  - 多判官独立投票（arXiv:2605.29800 待核验）

## 12.3 每步前置条件与验收标准

| 步 | 前置 | 验收标准 |
|---|---|---|
| N1 | 无 | 候选边生成脚本可重跑、带 source_mis 溯源 |
| N2 | N1 | W2 模型下 IN=79/OUT=42/UNDEC=0（非退化） |
| D1 | N1+N2 | 零误伤率=0；攻击边密度>0 |
| D2 | D1 | 抽 1 条边做 mutation 反例通过 |
| 上线 | D1+D2 | 退化指数<0.9；IN 与现有 confirmed 一致性≥阈值 |

## 12.4 一句话边界

**W2 模型已证可用，落地只剩"边从哪来可信"（D1 人审）与"边是否被真实反驳验证"（D2）。算法与复杂度均非瓶颈。**

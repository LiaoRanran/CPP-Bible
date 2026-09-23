# 627 C1 · Blind Review 人审操作指南

## 零、为什么需要你（人）
- 当前「独立人类确认强度 = 0」：622 的 30 条执行被标注为 `user_authorized_execution`，**不计入独立人审**。
- 把强度从 0 变非 0 的**唯一途径**是真实 Blind Review——机器无法代办。

## 一、Pass A（盲审，最重要）
1. 打开 `blind_review_pack_top10_627.json`，逐条阅读 `question` 与 `evidence_refs`。
2. **在查看任何既有结论前**，先填写 `human_decision` 与 `human_rationale`。
3. ⚠ **严禁**参考包中以外提供的「AI 推荐 / Authority 结果」——一旦在盲态下看到推荐即视为盲审失效。
4. automation_bias 风险：人对 AI 推荐有顺从倾向，盲审的目的正是隔离该偏差。

## 二、Pass B（解盲一致性）
1. 盲审完成后，对照 626 C1 的 `blind_review_v1_626.py` 做解盲：
   - 将你的 `human_decision` 与既有 Authority `result` 比对。
2. 记录一致性比例与分歧项；对分歧项标注 `automation_bias_risk`（是否因看到推荐而动摇）。

## 三、回填（不自动写入）
- 结果经 `blind_review_backfill_627.py`（627 C2）**生成回填条目**，但**不自动落库**；
  最终写入 Authority Ledger 需人明确确认（交人项 #2）。

> 本指南与执行包**不修改任何 ledger / 受控目录**；盲审执行本身由人完成。

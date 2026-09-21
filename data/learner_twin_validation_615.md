# 615 D2 · 学习者镜像闭环验证（**模拟数据，门未开**）

> **诚实声明**：当前真实学习事件 = **0**，门未开。本验证**全部使用模拟数据**，
> 只验证**逻辑正确性**，**不代表真实学习效果**。不写 `data/learner_state.json`（只读验证）。

## 一、10 条模拟行为的掌握度变化（KC=ATOM-CONC-FENCE-001）
| # | 行为 | BKT 掌握度 |
|---|---|---|
| 0 | （初始） | 0.1000 |
| 1 | correct | 0.3667 |
| 2 | incorrect | 0.1141 |
| 3 | correct | 0.3986 |
| 4 | correct | 0.7615 |
| 5 | incorrect | 0.3210 |
| 6 | correct | 0.6962 |
| 7 | correct | 0.9160 |
| 8 | correct | 0.9810 |
| 9 | incorrect | 0.8727 |
| 10 | correct | 0.9702 |

- 读法：**correct → 上升、incorrect → 下降**，10 步后 0.10 → **0.9702**（BKT 递推正确）。
- 复算：`learner_behavior_logger.record/replay`。

## 二、推荐路径变化（前置门槛）
- 初始推荐集：根 KC（前置已满足）≥1 条。
- 某 KC 连续答对 6 次后掌握 ≥0.5 ⇒ **退出推荐集**（前置未达 0.5 的 KC 不再推荐）。
- 模拟轨迹（`simulate(10 KC×5 轮, seed=7)`）：**8 个 KC ≥0.5**、平均掌握度 **0.7306**。

## 三、跃迁触发验证
- 掌握度 ≥0.8 且 OOD 正确率 ≥80% ⇒ **jump**；OOD<0.8 ⇒ **no_jump**；掌握度<0.8 ⇒ **no_jump**。
- 全部通过（`learner_ood_evaluator.evaluate`）。

## 四、论证链联动验证
- `chains_for_kc("ATOM-CONC-FENCE-001")` ⇒ ✅ observation→inference 链（读真实 `propositions.db`）。
- 已掌握但论证链**未理解透** ⇒ 进入**论证复盘推荐**；逐条标记理解后 ⇒ **移出**推荐。
- 全部通过（`learner_argument_link.recommend_argument_review`）。

## 五、结论与边界
- 闭环逻辑（采集→BKT→推荐→跃迁→论证联动）在模拟数据下**全部正确**。
- **真实学习事件 = 0，门未开**；本验证**不代表**真实学习效果。
- 不修改 `learner_state.json`；不采集真实学习行为（需用户开始做题）。

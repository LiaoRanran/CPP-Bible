# 616 C3 · Goodhart 监控接入 metrics（报告）

> 铁律：`metrics_collector.py` 不在 CORE_TOOLS（可改）；**不动 27 项扁平 schema**（新字段挂 `collect_curves()["goodhart"]`）。

## 一、新增字段（`collect_curves()["goodhart"]`）
| 字段 | 含义 | 当前值 |
|---|---|---|
| `goodhart_score` | Goodhart 危险分（0–100，越高越危险） | **80.1** |
| `goodhart_warn_growth_rate` | warn 增长率/批 | 14.09 |
| `goodhart_legacy_growth_rate` | legacy 采纳增长率/批 | 0.5 |
| `goodhart_block_rate` | block 率 | 0.0 |
| `goodhart_rule_coverage` | 规则覆盖率 | `None`（未取到，**不臆造**） |
| `goodhart_human_reject_rate` | 人审拒绝率 | 0.0 |

## 二、当前各指标值（与 `goodhart_monitor.compute()` 完全一致）
- 危险分 **80.1/100**（4 个已知子项；coverage 未知已排除并按已知项重标定）。

## 三、解读：80.1/100 意味着什么
**贡献最大的子项**（各满分 20）：
1. `block_rate`（20）——**block=0**：无任何阻断 ⇒ "门禁全绿"可能是"没在拦"；
2. `human_reject_rate`（20）——**reject=0/388**：无拒绝 ⇒ rubber-stamp 风险；
3. `warn_growth`（14.1）——warn **31→136→186** 持续增长并被采纳为 legacy；
4. `legacy_growth`（10.0）——采纳率高；`coverage` 未知（未计入）。

⇒ 与 `_arch_v20/08` 的 Goodhart 判断一致：**目标（真实质量）被指标（block/warn 计数）渐次替代**。

## 四、降低危险分的建议（与 C1/C2 工作流关联）
1. **C1 warn 不增锁**：新 warn 不自动采纳 + 观察期 ⇒ 压 `warn_growth`/`legacy_growth`；
2. **C2 豁免到期制**：27 条 legacy 到期重评估 ⇒ 防豁免永久沉淀；
3. **引入"真信号"**：block/warn 之外补**独立经验证**（B3 双实现回归锁、D 线他验三件套）⇒ 抬 `coverage` 与"独立票"；
4. **提高 reject 率的正当性**：不是人为拒绝，而是让**逐条复核**（615 A2 的 30 条）真发生 ⇒ reject 率成为真实信号。

## 五、边界
- 新字段**附加**，27 项扁平 schema 未动（`test_metrics_collector` 仍全绿）。
- `coverage` 取不到时**记 `None`**（不填 0/不臆造）。
- 分数是**趋势提示**，**不是判决**；不自动修改任何基线。

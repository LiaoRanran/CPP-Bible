# 707 Task B — 零成本改进落地（P1/P2/P3）

- 日期：2026-10-09
- 科研依据：**700-F 零成本改进**（`data/700_design_simulation.json`）+ 703 只读验证（`data/703_zero_cost_validation.json`）
- 红线：detect_calls = 0；只用冻结矩阵验证；不改检测器/样本/冻结矩阵。

## 1. 科研结论（700-F / 700-D）

设计 B（aware 记账 + 6 资产声明 + 显式聚合）综合分 **0.7721** 胜过现状 A **0.6230**，**抗漂移评分 53.05 → 66.67**，而**检出率完全相同**。前三条改进成本≈0：

| 编号 | 改进 | 效果 |
|------|------|------|
| P1 | 移除零产资产（`wunsequenced` / `compile-time`）的声明 | 构成膨胀 0.4602 → 0.0000，检出率 Δ = 0 |
| P2 | 记账从 unaware 改为 aware（三组件向量） | Δunknown 0.00pp → 75.265pp（暴露静默退化） |
| P3 | 报告里显式声明聚合规则 | OR 对零产免疫；mean 稀释因子 1.3333（Type IV 暴露） |

## 2. 落地做了什么

| 文件 | 改动 | 科研依据标注 |
|------|------|--------------|
| `tools/asset_capabilities.py`（**新**） | 资产声明/记账/聚合的**单一事实源**：`ALL_ASSETS` / `ZERO_YIELD_ASSETS` / `EFFECTIVE_ASSETS`（P1）；`or_verdict(accounting=...)` + `triple()`（P2）；`AGGREGATION_RULES` + `aggregate_one/rate(rule=...)`（P3）；`--validate` 复算并对账 703 | 文件头 + 各常量注释均标注「700-F P1/P2/P3」 |
| `tools/detect_for_assets.py`（改） | 新增 `--aggregation {or,max,at_least_2,mean}`（默认 `or`，保持旧行为）；`mean` 触发**稀释警告**；`aggregate()` 增 `rule` 参数（默认 `or`，向后兼容）；导入单一事实源 | `aggregate`/`--aggregation` 注释标注「707-B / 700-F P3」 |

> **P1 的「声明」在哪里**：本项目**没有**独立的 asset 能力声明文件——能力声明散落为代码常量 + 逐 profile `supported_assets`（`analyze_692_environment.py`、`compute_697_drift_algebra.py`、`compute_703_zero_cost_validation.py`）。因此 707 把「声明池 / 零产资产 / 有效池」**收敛到 `asset_capabilities.py` 这一单一事实源**，实现 P1 的「从声明中移除零产资产」有明确落点。

## 3. 验证（`tools/asset_capabilities.py --validate`，冻结矩阵，detect_calls=0）

```
P1 零产资产 catch 合计=0；OR 8 资产=61.6391% vs 6 资产=61.6391% ⇒ Δ=0.0pp  hold=True
P2 Δunknown：unaware=0.0pp vs aware=75.265pp  hold=True
P3 OR Δ=0.0pp（免疫）；mean 稀释因子=1.333331  hold=True
抗漂移评分（700-D）：53.05 → 66.67
ALL_CLAIMS_HOLD = True
```

与 703 权威值**逐项一致**：Δ 检出率 0.0、Δunknown(aware) 75.265、mean 稀释 1.333331。产物：`data/707_zero_cost_landing_validation.json`。

## 4. 诚实边界（红线）

- **不声称「提升了检测性能」**：三项改进的**检出率不变**（59.55% / OR 61.6391%）；提升的是**抗漂移性**（53.05 → 66.67，来自 700-D 设计模拟）。
- 全部为**只读复算**（冻结矩阵 + 692 剖面），`detect_calls = 0`。
- P1 的「零产」是**在本冻结矩阵上**零 catch；换语料可能不再零产。
- P2 的 aware 读数基于**单一环境对**（E1 vs E2）⇒ 不声称普适。
- 抗漂移评分是**模拟量**（同冻结矩阵、四轴），非新实测。
- `mean` 警告是**提示性**的（不改默认行为）；默认仍为 `or`。

## 5. 产物

- `tools/asset_capabilities.py`（新）
- `tools/detect_for_assets.py`（+`--aggregation` 与 `rule` 透传）
- `data/707_zero_cost_landing_validation.json`（验证产物）
- 本报告

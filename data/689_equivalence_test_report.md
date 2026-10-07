# 689-B1 · 等价性检验（TOST）：真实靶场 vs 自造语料

- 生成：2026-10-07T21:41:50+08:00｜脚本：tools/equivalence_689.py｜种子登记：6891（确定性计算）
- 数据（只读）：`data/683_real_world_detection_matrix.json`（110 条） vs `data/blindspot_676g_detection_matrix.json`（1147 条）
- 口径：OR（任一 catch ⇒ catch；全部 unknown ⇒ unknown；其余 miss），两侧逐字一致。

## 1. 两臂

| 臂 | n | catch | 检出率 |
|---|---:|---:|---:|
| 真实（source-derived, 110 CVE 重构） | 110 | 65 | 59.09% |
| 合成（self-authored, 676g 冻结矩阵） | 1147 | 707 | 61.64% |

- 差异（real − synthetic）：**-2.55pp**，Wald SE 4.90pp。
- 两批样本独立（非配对），不能做 McNemar；此前 z=-0.52, p=0.60 为**非显著性**，不是等价性证据

## 2. 主分析（margin = ±10pp，α=0.05 双单侧 ⇒ 90% CI）

- 90% CI：**[-10.61, 5.52]pp**（CI 是否落入 ±10pp：否）
- p_lower = 0.0643｜p_upper = 0.0052｜**p_TOST = 0.0643**
- **判定：未通过（不能声明等价）**
- 说明：落在 +10pp 一侧的上单侧检验通过（p_upper≈0.005）；未通过的是 −10pp 一侧（真实更低方向的边界），差 0.61pp 未及。

- **最小通过 margin ≈ 10.61pp**（= |diff| + z90·SE；即 margin 需 ≥ 该值 TOST 才通过）。

## 3. Margin 敏感性

| margin | 90% CI | p_TOST | 等价？ |
|---:|---|---:|---|
| ±5pp | [-10.61, 5.52] | 0.3085 | 否 |
| ±7pp | [-10.61, 5.52] | 0.1819 | 否 |
| ±10pp | [-10.61, 5.52] | 0.0643 | 否 |
| ±12pp | [-10.61, 5.52] | 0.0269 | 是 |
| ±15pp | [-10.61, 5.52] | 0.0055 | 是 |

## 4. Margin 曲线（m ∈ [0,15]pp，步长 0.25）

曲线数据见 JSON `tost_margin_curve`。p_TOST 随 margin 单调下降；在 m≈10.61pp 处首次 <0.05。
**纪律**：不得为了"通过"事后放大 margin；本报告把曲线全量公开，供审稿人检查任何 margin 下的判定。

## 5. 设计效应保守敏感性（合成侧聚类）

- 合成侧样本来自模板家族（677b：design effect 4.05–4.26，本处取上界 4.26）。
- 校正后 SE 由 4.90pp 放宽到 5.55pp；
  margin=±10pp 仍未通过（p_TOST=0.0895），最小通过 margin ≈ 11.67pp。

## 6. 结论（可直接引用）

> TOST（margin=±10pp）未通过：90% CI 下界 −10.61pp 略超 −10pp（p_tost≈0.064>0.05）；最小通过 margin≈10.61pp（deff 校正后≈11.67pp）。因此不能说"合成与真实等价"；只能说"在本样本量与本 margin 下未能声明等价，差异点估计 −2.55pp、CI 宽约 ±8.1pp"。

复算：`python tools/equivalence_689.py`（只读两个矩阵，输出本报告与 JSON）。

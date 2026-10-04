# 677b · 任务B：Clone-aware split 对比与 leakage 量化

- 生成：`tools/analyze_677b_clone_aware.py splits`（2026-10-04T12:27:36+08:00）；seed=6771
- 分裂单位：**全对凝聚家族**（family_random / family_stratified，口径见任务A）与 **连通分量**（strict_stratified，最强不泄漏口径）
- 判据：同单位整体进同一 side；克隆对（C1∪C2∪C3）不得跨 side

## 1. 泄漏量化：原 split 的问题有多大

| 指标 | 原 split（676f） | family_random | family_stratified | strict_stratified |
|---|---:|---:|---:|---:|
| 派生/评估样本数 | 571/566 | 568/569 | 568/569 | 569/568 |
| 跨 split 的**家族**数 | 147 / 474 | 0 / 474 | 0 / 474 | 0 / 474 |
| 跨 split 家族涉及样本 | 736 | 0 | 0 | 0 |
| 原 split 跨 split 家族规模（前 10） | [21, 17, 16, 16, 15, 15, 15, 14, 12, 12] | — | — | — |
| 跨 split 的**单位**数 | 123 / 420 | 14 / 420 | 20 / 420 | 0 / 420 |
| 跨 split 单位涉及样本 | 773 | 209 | 268 | 0 |
| 跨 split 的**克隆对**数 | 1553 | 294 | 401 | 0 |
| 评估侧独立单位数 | 270 | 226 | 225 | 198 |
| 派生侧独立单位数 | 273 | 208 | 215 | 222 |

## 2. 分布均衡（最大偏差 pp；越小越均衡）

| 属性 | 原 split | family_random | family_stratified | strict_stratified |
|---|---:|---:|---:|---:|
| source_batch | 0.2745 | 7.0051 | 3.1353 | 5.1242 |
| defect_group | 0.1547 | 6.6533 | 3.1353 | 5.2631 |
| defect_type | 2.1341 | 5.2817 | 1.5864 | 3.5134 |
| planted | 0.9982 | 2.4512 | 1.044 | 0.7151 |

## 3. 各项校验

- **family_random**：家族跨 split 0（要求 0）；克隆对跨 split 294；派生 568 / 评估 569
- **family_stratified**：家族跨 split 0（要求 0）；克隆对跨 split 401；派生 568 / 评估 569
- **strict_stratified**：家族跨 split 0（要求 0）；克隆对跨 split 0；派生 569 / 评估 568

## 4. 结论

- 原 split 下：**同一家族的成员被劈到两侧**——147/474 个家族跨 split、涉及 736 条样本、1553 对判克隆的样本对分居两侧；这就是评审指出的 template-family leakage 的量化证据；
- clone-aware split 下：家族跨 split = 0（构造保证）；**strict 变体**（连通分量为单位）进一步保证**任意一对判克隆的样本**都不跨 split（克隆对跨越 = 0）。family 级变体仍有少量残余克隆对跨越（同分量内的跨族对），已如实记录；
- 均衡性代价：金标准是原 split 的分层均衡（batch 最大偏差 0.27pp）；family-aware split 无法同时满足「家族整体不动」与「批次完全均衡」（跨批家族把别的批次样本一起带走），各属性最大偏差见 §2（最大 7.0pp，出现在 family_random 的 source_batch）。A5 结论在三种 split 下的稳定性见 `data/677b_a5_comparison_table.md`；
- 样本数偏差：三种 split 评估侧 568–569 条，与原 566 的偏差 <0.4%（验收要求 ±5% 内）。

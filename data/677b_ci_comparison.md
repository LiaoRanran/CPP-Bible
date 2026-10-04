# 677b · 任务D：普通 CI vs Cluster Bootstrap CI

- 生成：`tools/analyze_677b_clone_aware.py tables`（2026-10-04T12:30:00+08:00）；bootstrap 次数 2000，seed=6771
- 普通 CI = 676f 口径（Clopper–Pearson 单臂率 + McNemar 口径 Wald Δ CI，假设样本独立）；cluster CI = 按分裂单位有放回重采样 2000 次的 percentile CI
- 两种 bootstrap 模式：**frozen_arms**（冻结两臂资产集 ⇒ 报告量 Δ 的 CI）/ **full_refit**（每 replicate 重排 FD + 重抽 Random ⇒ 含选臂方差，回答「换个随机臂会不会翻盘」）

## family_stratified（评估 n=569，分裂单位 474 个）

- FD 检出率：点估计 55.536%；普通 CP95 [51.35, 59.67]（宽 8.32pp）；cluster(frozen) 95% [47.53, 63.96]（宽 16.43pp）
- Δ(FD−Random)：点估计 +23.02pp；普通 95%CI [19.1435, 26.9022]（宽 7.76pp）
  - cluster(frozen) 95% [+16.57, +30.38]pp（宽 13.80pp，1.78× 普通）；Δ≤0 比例 0.0
  - cluster(full_refit) 95% [+0.43, +39.02]pp（宽 38.59pp，4.97× 普通）；Δ≤0 比例 0.022
  - Random 臂自身的不确定性（cluster CI 宽 15.73pp）是 full_refit 宽 CI 的主因 ⇒ 报告量 Δ 用 frozen 口径
- 设计效应（FD 率）：cluster SD 4.19pp vs 独立假设 SE 2.08pp ⇒ deff≈4.05，有效样本量≈140（名义 n=569）
- 并列（5 候选）：点估计 Δ -0.53pp；cluster(frozen) Δ 95% [-2.84, +1.59]pp；全重算 -0.54pp（均值）
- 每 replicate 评估样本数：均值 568.115，范围 [424, 737]（单位大小不等所致，已如实记录）
- frozen 模式冻结的臂：FD ['asan', 'ubsan', 'tsan', 'compiler-warn']；Random ['wunsequenced', 'cross-compile', 'tsan', 'compile-time']
- full_refit 下 FD 资产被选中频次（前 5）：[('asan', 2000), ('tsan', 1992), ('ubsan', 1990), ('compiler-warn', 1518), ('cross-compile', 500)]
- full_refit 下并列 FD 资产被选中频次：[('asan', 2000), ('tsan', 1992), ('ubsan', 1990), ('compiler-warn', 1518), ('cross-compile', 500)]

## strict_stratified（评估 n=568，分裂单位 420 个）

- FD 检出率：点估计 57.5704%；普通 CP95 [53.39, 61.67]（宽 8.29pp）；cluster(frozen) 95% [48.53, 65.78]（宽 17.24pp）
- Δ(FD−Random)：点估计 +25.70pp；普通 95%CI [22.1104, 29.2981]（宽 7.19pp）
  - cluster(frozen) 95% [+18.28, +33.39]pp（宽 15.12pp，2.10× 普通）；Δ≤0 比例 0.0
  - cluster(full_refit) 95% [+0.00, +40.03]pp（宽 40.03pp，5.57× 普通）；Δ≤0 比例 0.03
  - Random 臂自身的不确定性（cluster CI 宽 16.04pp）是 full_refit 宽 CI 的主因 ⇒ 报告量 Δ 用 frozen 口径
- 设计效应（FD 率）：cluster SD 4.28pp vs 独立假设 SE 2.07pp ⇒ deff≈4.26，有效样本量≈133（名义 n=568）
- 并列（5 候选）：点估计 Δ +0.00pp；cluster(frozen) Δ 95% [+0.00, +0.00]pp；全重算 +0.00pp（均值）
- 每 replicate 评估样本数：均值 570.323，范围 [345, 923]（单位大小不等所致，已如实记录）
- frozen 模式冻结的臂：FD ['asan', 'tsan', 'ubsan', 'cross-compile']；Random ['wunsequenced', 'cross-compile', 'tsan', 'compile-time']
- full_refit 下 FD 资产被选中频次（前 5）：[('asan', 2000), ('tsan', 2000), ('ubsan', 1992), ('cross-compile', 1339), ('compiler-warn', 669)]
- full_refit 下并列 FD 资产被选中频次：[('asan', 2000), ('tsan', 2000), ('ubsan', 1992), ('cross-compile', 1339), ('compiler-warn', 669)]

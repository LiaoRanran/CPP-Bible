# 677c · 5+ Baseline 对比报告（3 非退化池）

- 随机臂：单点 seed=20260930 配对检验 + 2000 次分布（676f 口径）；其余基线确定性跑 1 次
- 判定矩阵/切分：676f 冻结产物，未重跑 detect
- 复现：`.venv/Scripts/python.exe tools/analyze_677c_nondegenerate.py --stage baselines`
- 机读：`data/677c_baseline_results.json`

## 1. 基线定义

| 基线 | 选择规则 | 信息源 | 确定性 | 备注 |
|---|---|---|---|---|
| random | seed 抽样 top-k | 无（对照臂） | seed 可复现 | 2000 次报分布 |
| fd | 派生集 fail_hits 降序 top-k | 派生集 | 是 | 676f 当前方法 |
| frequency | 派生集 catch 频率降序 top-k | 派生集 | 是 | **与 fd 排序键相同**（见 §3） |
| greedy | 迭代残余覆盖贪心（set-cover） | 派生集 | 是 | ≡ operator 的 fd_only 配置 |
| oracle | 评估集上穷举 C(n,k) 选最优 | **评估集（泄漏）** | 是 | 上界参考，不可达 |
| static | 静态资产字典序 top-k | 无 | 是 | 只能选静态资产（≤n_static 个） |
| info_gain | 对池-OR 目标的互信息排序 | 派生集 | 是 | 探索性（卡片可选项） |

## 2. 全量结果（每池每 k 的 8 臂）

### Pool A（Pool A（严格）；候选 asan, compiler-warn, cross-compile, tsan, ubsan）

| k | 臂 | 选择 | 检出率% | Δ单点(Random) | p | Δvs均值2000 | 排名 |
|---|---|---|---|---|---|---|---|
| 1 | fd | asan | 33.04 | +11.31pp | 6.02e-08 | +12.26pp | 2 |
| 1 | random | tsan | 21.73 | +0.00pp | n/a | +0.95pp | 7 |
| 1 | static | compiler-warn | 11.84 | -9.89pp | 2.10e-05 | -8.94pp | 8 |
| 1 | frequency | asan | 33.04 | +11.31pp | 6.02e-08 | +12.26pp | 3 |
| 1 | greedy | asan | 33.04 | +11.31pp | 6.02e-08 | +12.26pp | 4 |
| 1 | oracle | asan | 33.04 | +11.31pp | 6.02e-08 | +12.26pp | 6 |
| 1 | info_gain | asan | 33.04 | +11.31pp | 6.02e-08 | +12.26pp | 5 |
| 1 | evo_full | asan | 33.04 | +11.31pp | 6.02e-08 | +12.26pp | 1 |
| 2 | fd | asan,ubsan | 45.05 | +7.42pp | 7.69e-05 | +10.06pp | 1 |
| 2 | random | tsan,ubsan | 37.63 | +0.00pp | n/a | +2.64pp | 7 |
| 2 | static | compiler-warn,cross-compile | 24.03 | -13.60pp | 6.76e-08 | -10.97pp | 8 |
| 2 | frequency | asan,ubsan | 45.05 | +7.42pp | 7.69e-05 | +10.06pp | 2 |
| 2 | greedy | asan,ubsan | 45.05 | +7.42pp | 7.69e-05 | +10.06pp | 3 |
| 2 | oracle | asan,ubsan | 45.05 | +7.42pp | 7.69e-05 | +10.06pp | 5 |
| 2 | info_gain | asan,ubsan | 45.05 | +7.42pp | 7.69e-05 | +10.06pp | 4 |
| 2 | evo_full | asan,compiler-warn | 41.34 | +3.71pp | 0.1434 | +6.35pp | 6 |
| 3 | fd | asan,ubsan,tsan | 51.06 | +7.42pp | 3.71e-06 | +5.78pp | 1 |
| 3 | random | tsan,ubsan,cross-compile | 43.64 | +0.00pp | n/a | -1.64pp | 7 |
| 3 | static | compiler-warn,cross-compile | 24.03 | -19.61pp | 1.20e-18 | -21.25pp | 8 |
| 3 | frequency | asan,ubsan,tsan | 51.06 | +7.42pp | 3.71e-06 | +5.78pp | 2 |
| 3 | greedy | asan,ubsan,tsan | 51.06 | +7.42pp | 3.71e-06 | +5.78pp | 3 |
| 3 | oracle | asan,tsan,ubsan | 51.06 | +7.42pp | 3.71e-06 | +5.78pp | 5 |
| 3 | info_gain | asan,ubsan,tsan | 51.06 | +7.42pp | 3.71e-06 | +5.78pp | 4 |
| 3 | evo_full | asan,compiler-warn,tsan | 48.06 | +4.42pp | 0.05199 | +2.78pp | 6 |
| 4 | fd | asan,ubsan,tsan,cross-compile | 54.59 | +0.00pp | 1 | +1.61pp | 4 |
| 4 | random | tsan,ubsan,cross-compile,asan | 54.59 | +0.00pp | n/a | +1.61pp | 7 |
| 4 | static | compiler-warn,cross-compile | 24.03 | -30.57pp | 8.05e-34 | -28.96pp | 8 |
| 4 | frequency | asan,ubsan,tsan,cross-compile | 54.59 | +0.00pp | 1 | +1.61pp | 5 |
| 4 | greedy | asan,ubsan,tsan,compiler-warn | 56.01 | +1.41pp | 0.302 | +3.02pp | 2 |
| 4 | oracle | asan,compiler-warn,tsan,ubsan | 56.01 | +1.41pp | 0.302 | +3.02pp | 3 |
| 4 | info_gain | asan,ubsan,tsan,cross-compile | 54.59 | +0.00pp | 1 | +1.61pp | 6 |
| 4 | evo_full | asan,compiler-warn,tsan,ubsan | 56.01 | +1.41pp | 0.302 | +3.02pp | 1 |

### Pool B（Pool B（中等）；候选 asan, compiler-warn, cross-compile, linker, tsan, ubsan）

| k | 臂 | 选择 | 检出率% | Δ单点(Random) | p | Δvs均值2000 | 排名 |
|---|---|---|---|---|---|---|---|
| 1 | fd | asan | 33.04 | +32.33pp | 3.50e-50 | +15.39pp | 2 |
| 1 | random | linker | 0.71 | +0.00pp | n/a | -16.94pp | 8 |
| 1 | static | compiler-warn | 11.84 | +11.13pp | 8.74e-16 | -5.81pp | 7 |
| 1 | frequency | asan | 33.04 | +32.33pp | 3.50e-50 | +15.39pp | 3 |
| 1 | greedy | asan | 33.04 | +32.33pp | 3.50e-50 | +15.39pp | 4 |
| 1 | oracle | asan | 33.04 | +32.33pp | 3.50e-50 | +15.39pp | 6 |
| 1 | info_gain | asan | 33.04 | +32.33pp | 3.50e-50 | +15.39pp | 5 |
| 1 | evo_full | asan | 33.04 | +32.33pp | 3.50e-50 | +15.39pp | 1 |
| 2 | fd | asan,ubsan | 45.05 | +21.55pp | 1.72e-32 | +14.44pp | 1 |
| 2 | random | linker,ubsan | 23.50 | +0.00pp | n/a | -7.11pp | 8 |
| 2 | static | compiler-warn,cross-compile | 24.03 | +0.53pp | 0.8806 | -6.58pp | 7 |
| 2 | frequency | asan,ubsan | 45.05 | +21.55pp | 1.72e-32 | +14.44pp | 2 |
| 2 | greedy | asan,ubsan | 45.05 | +21.55pp | 1.72e-32 | +14.44pp | 3 |
| 2 | oracle | asan,ubsan | 45.05 | +21.55pp | 1.72e-32 | +14.44pp | 5 |
| 2 | info_gain | asan,ubsan | 45.05 | +21.55pp | 1.72e-32 | +14.44pp | 4 |
| 2 | evo_full | asan,compiler-warn | 41.34 | +17.84pp | 1.29e-12 | +10.73pp | 6 |
| 3 | fd | asan,ubsan,tsan | 51.06 | +21.73pp | 1.46e-20 | +10.49pp | 1 |
| 3 | random | linker,ubsan,compiler-warn | 29.33 | +0.00pp | n/a | -11.24pp | 7 |
| 3 | static | compiler-warn,cross-compile,linker | 24.73 | -4.59pp | 0.03424 | -15.84pp | 8 |
| 3 | frequency | asan,ubsan,tsan | 51.06 | +21.73pp | 1.46e-20 | +10.49pp | 2 |
| 3 | greedy | asan,ubsan,tsan | 51.06 | +21.73pp | 1.46e-20 | +10.49pp | 3 |
| 3 | oracle | asan,tsan,ubsan | 51.06 | +21.73pp | 1.46e-20 | +10.49pp | 5 |
| 3 | info_gain | asan,ubsan,tsan | 51.06 | +21.73pp | 1.46e-20 | +10.49pp | 4 |
| 3 | evo_full | asan,compiler-warn,tsan | 48.06 | +18.73pp | 5.13e-14 | +7.48pp | 6 |
| 4 | fd | asan,ubsan,tsan,cross-compile | 54.59 | +15.19pp | 5.92e-13 | +6.19pp | 4 |
| 4 | random | linker,ubsan,compiler-warn,cross-compile | 39.40 | +0.00pp | n/a | -9.00pp | 7 |
| 4 | static | compiler-warn,cross-compile,linker | 24.73 | -14.66pp | 2.07e-25 | -23.67pp | 8 |
| 4 | frequency | asan,ubsan,tsan,cross-compile | 54.59 | +15.19pp | 5.92e-13 | +6.19pp | 5 |
| 4 | greedy | asan,ubsan,tsan,compiler-warn | 56.01 | +16.61pp | 2.33e-16 | +7.61pp | 2 |
| 4 | oracle | asan,compiler-warn,tsan,ubsan | 56.01 | +16.61pp | 2.33e-16 | +7.61pp | 3 |
| 4 | info_gain | asan,ubsan,tsan,cross-compile | 54.59 | +15.19pp | 5.92e-13 | +6.19pp | 6 |
| 4 | evo_full | asan,compiler-warn,tsan,ubsan | 56.01 | +16.61pp | 2.33e-16 | +7.61pp | 1 |
| 5 | fd | asan,ubsan,tsan,cross-compile,compiler-warn | 59.36 | +9.89pp | 7.36e-14 | +4.76pp | 1 |
| 5 | random | linker,ubsan,compiler-warn,cross-compile,tsan | 49.47 | +0.00pp | n/a | -5.13pp | 7 |
| 5 | static | compiler-warn,cross-compile,linker | 24.73 | -24.73pp | 1.43e-42 | -29.87pp | 8 |
| 5 | frequency | asan,ubsan,tsan,cross-compile,compiler-warn | 59.36 | +9.89pp | 7.36e-14 | +4.76pp | 2 |
| 5 | greedy | asan,ubsan,tsan,compiler-warn,cross-compile | 59.36 | +9.89pp | 7.36e-14 | +4.76pp | 3 |
| 5 | oracle | asan,compiler-warn,cross-compile,tsan,ubsan | 59.36 | +9.89pp | 7.36e-14 | +4.76pp | 5 |
| 5 | info_gain | asan,ubsan,tsan,cross-compile,compiler-warn | 59.36 | +9.89pp | 7.36e-14 | +4.76pp | 4 |
| 5 | evo_full | asan,compiler-warn,tsan,ubsan,linker | 56.71 | +7.24pp | 4.19e-06 | +2.11pp | 6 |

### Pool C（Pool C（宽松）；候选 asan, compiler-warn, cross-compile, linker, tsan, ubsan）

| k | 臂 | 选择 | 检出率% | Δ单点(Random) | p | Δvs均值2000 | 排名 |
|---|---|---|---|---|---|---|---|
| 1 | fd | asan | 33.04 | +32.33pp | 3.50e-50 | +15.39pp | 2 |
| 1 | random | linker | 0.71 | +0.00pp | n/a | -16.94pp | 8 |
| 1 | static | compiler-warn | 11.84 | +11.13pp | 8.74e-16 | -5.81pp | 7 |
| 1 | frequency | asan | 33.04 | +32.33pp | 3.50e-50 | +15.39pp | 3 |
| 1 | greedy | asan | 33.04 | +32.33pp | 3.50e-50 | +15.39pp | 4 |
| 1 | oracle | asan | 33.04 | +32.33pp | 3.50e-50 | +15.39pp | 6 |
| 1 | info_gain | asan | 33.04 | +32.33pp | 3.50e-50 | +15.39pp | 5 |
| 1 | evo_full | asan | 33.04 | +32.33pp | 3.50e-50 | +15.39pp | 1 |
| 2 | fd | asan,ubsan | 45.05 | +21.55pp | 1.72e-32 | +14.44pp | 1 |
| 2 | random | linker,ubsan | 23.50 | +0.00pp | n/a | -7.11pp | 8 |
| 2 | static | compiler-warn,cross-compile | 24.03 | +0.53pp | 0.8806 | -6.58pp | 7 |
| 2 | frequency | asan,ubsan | 45.05 | +21.55pp | 1.72e-32 | +14.44pp | 2 |
| 2 | greedy | asan,ubsan | 45.05 | +21.55pp | 1.72e-32 | +14.44pp | 3 |
| 2 | oracle | asan,ubsan | 45.05 | +21.55pp | 1.72e-32 | +14.44pp | 5 |
| 2 | info_gain | asan,ubsan | 45.05 | +21.55pp | 1.72e-32 | +14.44pp | 4 |
| 2 | evo_full | asan,compiler-warn | 41.34 | +17.84pp | 1.29e-12 | +10.73pp | 6 |
| 3 | fd | asan,ubsan,tsan | 51.06 | +21.73pp | 1.46e-20 | +10.49pp | 1 |
| 3 | random | linker,ubsan,compiler-warn | 29.33 | +0.00pp | n/a | -11.24pp | 7 |
| 3 | static | compiler-warn,cross-compile,linker | 24.73 | -4.59pp | 0.03424 | -15.84pp | 8 |
| 3 | frequency | asan,ubsan,tsan | 51.06 | +21.73pp | 1.46e-20 | +10.49pp | 2 |
| 3 | greedy | asan,ubsan,tsan | 51.06 | +21.73pp | 1.46e-20 | +10.49pp | 3 |
| 3 | oracle | asan,tsan,ubsan | 51.06 | +21.73pp | 1.46e-20 | +10.49pp | 5 |
| 3 | info_gain | asan,ubsan,tsan | 51.06 | +21.73pp | 1.46e-20 | +10.49pp | 4 |
| 3 | evo_full | asan,compiler-warn,tsan | 48.06 | +18.73pp | 5.13e-14 | +7.48pp | 6 |
| 4 | fd | asan,ubsan,tsan,cross-compile | 54.59 | +15.19pp | 5.92e-13 | +6.19pp | 4 |
| 4 | random | linker,ubsan,compiler-warn,cross-compile | 39.40 | +0.00pp | n/a | -9.00pp | 7 |
| 4 | static | compiler-warn,cross-compile,linker | 24.73 | -14.66pp | 2.07e-25 | -23.67pp | 8 |
| 4 | frequency | asan,ubsan,tsan,cross-compile | 54.59 | +15.19pp | 5.92e-13 | +6.19pp | 5 |
| 4 | greedy | asan,ubsan,tsan,compiler-warn | 56.01 | +16.61pp | 2.33e-16 | +7.61pp | 2 |
| 4 | oracle | asan,compiler-warn,tsan,ubsan | 56.01 | +16.61pp | 2.33e-16 | +7.61pp | 3 |
| 4 | info_gain | asan,ubsan,tsan,cross-compile | 54.59 | +15.19pp | 5.92e-13 | +6.19pp | 6 |
| 4 | evo_full | asan,compiler-warn,tsan,ubsan | 56.01 | +16.61pp | 2.33e-16 | +7.61pp | 1 |
| 5 | fd | asan,ubsan,tsan,cross-compile,compiler-warn | 59.36 | +9.89pp | 7.36e-14 | +4.76pp | 1 |
| 5 | random | linker,ubsan,compiler-warn,cross-compile,tsan | 49.47 | +0.00pp | n/a | -5.13pp | 7 |
| 5 | static | compiler-warn,cross-compile,linker | 24.73 | -24.73pp | 1.43e-42 | -29.87pp | 8 |
| 5 | frequency | asan,ubsan,tsan,cross-compile,compiler-warn | 59.36 | +9.89pp | 7.36e-14 | +4.76pp | 2 |
| 5 | greedy | asan,ubsan,tsan,compiler-warn,cross-compile | 59.36 | +9.89pp | 7.36e-14 | +4.76pp | 3 |
| 5 | oracle | asan,compiler-warn,cross-compile,tsan,ubsan | 59.36 | +9.89pp | 7.36e-14 | +4.76pp | 5 |
| 5 | info_gain | asan,ubsan,tsan,cross-compile,compiler-warn | 59.36 | +9.89pp | 7.36e-14 | +4.76pp | 4 |
| 5 | evo_full | asan,compiler-warn,tsan,ubsan,linker | 56.71 | +7.24pp | 4.19e-06 | +2.11pp | 6 |

## 3. 关键观察

- **frequency ≡ fd（选择完全一致：True）**：676f FD 的 fail_hits 操作定义就是派生集 catch 计数，因此当前 FD 无法与最朴素的频率基线区分。这直接回应了评审：FD 需要 novel/redundancy/cost 等正交分量（任务 C）才可能超越频率基线。
- Oracle 与 FD 的差距（pp，评估集上界参考）：Pool A k=1 +0.00pp, k=2 +0.00pp, k=3 +0.00pp, k=4 +1.41pp; Pool B k=1 +0.00pp, k=2 +0.00pp, k=3 +0.00pp, k=4 +1.41pp, k=5 +0.00pp; Pool C k=1 +0.00pp, k=2 +0.00pp, k=3 +0.00pp, k=4 +1.41pp, k=5 +0.00pp ⇒ 这是同预算下选择策略的理论空间。
- static 臂只能选静态资产（Pool A ≤2 个、Pool B/C ≤3 个），k 更大时不是同预算对比，只作参考（673p 预算语义）。

## 4. 多重比较

每个 (pool,k) 内 7 个臂 vs Random 单点的 McNemar p 已附 BH-FDR（JSON p_value_family.bh_fdr）；跨 (pool,k) 的扫描属探索性，未做全局校正。

## 5. 诚实边界

- Oracle 用评估集信息，只标上界不作证据；info_gain 是卡片标注的可选探索项。

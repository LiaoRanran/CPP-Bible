# 677c · A5 非退化池重算 vs 676f 原池对比

- 随机臂 2000 次 + 单点 seed=20260930；切分/矩阵与 676f 相同；k 扫描 1..|A|-1
- 复现：`.venv/Scripts/python.exe tools/analyze_677c_nondegenerate.py --stage a5`；机读 `data/677c_a5_nondegenerate_results.json`

## 1. 676f 原池（8 资产，含 3 预注册退化资产）基准数字

- k=4 主端点：FD 54.59% vs Random(单点) 30.57%，Δ+24.03pp，p=2.30e-41；2000 次均值 40.17% ⇒ FD−均值 +14.42pp
- 676f 并列分析（剔 3 退化，5 候选）：k=1..4 = +11.31pp, +7.42pp, +7.42pp, +0.00pp（k=4 两臂同集 ⇒ Δ=0）

## 2. 非退化池上的 A5（8 臂全表）

### Pool A

- 最优 k（FD−Random 单点最大）：k=1，FD 33.04% vs Random 单点 21.73%（2000 均值 20.78%），Δ单点 +11.31pp，Δvs均值 +12.26pp，p=6.02e-08

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

### Pool B

- 最优 k（FD−Random 单点最大）：k=1，FD 33.04% vs Random 单点 0.71%（2000 均值 17.64%），Δ单点 +32.33pp，Δvs均值 +15.39pp，p=3.50e-50

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

### Pool C

- 最优 k（FD−Random 单点最大）：k=1，FD 33.04% vs Random 单点 0.71%（2000 均值 17.64%），Δ单点 +32.33pp，Δvs均值 +15.39pp，p=3.50e-50

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

## 3. 内部对账

- Pool A 候选集 ≡ 676f 并列分析候选集 ⇒ k=1..4 的 Δ 与 676f 逐位一致：True（最大差 0.0pp）——两套代码路径、同一答案。

## 4. 退化资产贡献量化（k=4 主预算）

| 池 | FD% | Random单点% | 2000均值% | Δ单点 | Δvs均值 | 退化贡献(单点) | 退化贡献(vs均值) |
|---|---|---|---|---|---|---|---|
| 原池(8) | 54.59 | 30.57 | 40.17 | +24.03pp | +14.42pp | — | — |
| Pool A（严格） | 54.59 | 54.59 | 52.99 | +0.00pp | +1.61pp | +24.03pp | +12.81pp |
| Pool B（中等） | 54.59 | 39.40 | 48.40 | +15.19pp | +6.19pp | +8.83pp | +8.23pp |
| Pool C（宽松） | 54.59 | 39.40 | 48.40 | +15.19pp | +6.19pp | +8.83pp | +8.23pp |

## 5. uninterpretable 条款判定

- Pool A：残余预注册退化资产 = 无 ⇒ 条款不触发。池内无预注册退化资产 ⇒ 主分析即并列分析，条款不触发
- Pool B：残余预注册退化资产 = ['linker'] ⇒ 条款仍触发。池内仍有 catch 率<5% 的资产（linker）⇒ 按预注册条款本池主分析仍不可作选择策略优越性解读
- Pool C：残余预注册退化资产 = ['linker'] ⇒ 条款仍触发。池内仍有 catch 率<5% 的资产（linker）⇒ 按预注册条款本池主分析仍不可作选择策略优越性解读

## 6. 诚实边界

- 单点 Random 的 Δ 是一次抽样的配对差值（676f 口径，可对账）；期望效应看 delta_vs_random_mean_pp（对 2000 次均值）。
- Oracle 在评估集上选最优 ⇒ 只作上界参考。
- Pools B/C 含 linker（catch 0.88%<5%）⇒ 预注册 uninterpretable 条款在这些池仍触发；Pool A 不触发。

# 677b · 任务C：A5 重算结果并排对比（原 split vs 三种 clone-aware split）

- 生成：`tools/analyze_677b_clone_aware.py tables`（2026-10-04T12:30:00+08:00）
- 判定矩阵与检测器：**复用 676f**（1137×8 判定），本批未重跑 detect()，未改检测器
- 统计原语与 676f/673p 完全相同（exact McNemar、McNemar 口径 Δ CI、Clopper–Pearson、2000 次 Random 分布）
- 三种 clone-aware split 的构造见 `data/677b_split_comparison.md`；原 split 列为对照

## 1. 主分析 k=4（8 候选资产）

| split | 派生/评估 n | FD 检出率 | Random 检出率 | Δ(FD−Random) | Δ 95%CI | McNemar p | FD 严格优于随机的比例* | Static 检出率 | Δ(FD−Static) |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| original(676f 原 split) | 571/566 | 54.5936% | 30.5654% | **+24.03pp** | [20.5084, 27.5481] | 2.296e-41 | 97.6% | 24.735% | +29.86pp |
| family_random | 568/569 | 57.2935% | 30.58% | **+26.71pp** | [23.078, 30.3491] | 3.503e-46 | 97.6% | 25.6591% | +31.63pp |
| family_stratified | 568/569 | 55.536% | 32.5132% | **+23.02pp** | [19.1435, 26.9022] | 4.078e-29 | 97.6% | 22.8471% | +32.69pp |
| strict_stratified | 569/568 | 57.5704% | 31.8662% | **+25.70pp** | [22.1104, 29.2981] | 2.242e-44 | 96.3% | 29.0493% | +28.52pp |

*「FD 严格优于随机的比例」= 2000 次随机 k=4 抽样中 FD 的 catch 数严格更高的比例。

## 2. 并列分析 k=4（剔除退化资产后的 5 候选：asan / compiler-warn / cross-compile / tsan / ubsan）

| split | FD 检出率 | Random 检出率 | Δ(FD−Random) | Δ 95%CI | McNemar p | Δ(FD−Static) |
|---|---:|---:|---:|---|---:|---:|
| original(676f 原 split) | 54.5936% | 54.5936% | **+0.00pp** | [0.0, 0.0] | 1 | +30.57pp |
| family_random | 57.2935% | 57.2935% | **+0.00pp** | [0.0, 0.0] | 1 | +31.63pp |
| family_stratified | 55.536% | 56.0633% | **-0.53pp** | [-2.1786, 1.1242] | 0.6776 | +32.69pp |
| strict_stratified | 57.5704% | 57.5704% | **+0.00pp** | [0.0, 0.0] | 1 | +28.70pp |

## 3. k=1~4 的 Δ(FD−Random)（主分析（8 候选））

| k | original(676f 原 split) | family_random | family_stratified | strict_stratified |
|---:|---:|---:|---:|---:|
| k=1 | +33.04pp (p=1.02e-56) | +35.50pp (p=3.11e-61) | +34.80pp (p=4.98e-60) | +34.86pp (p=4.98e-60) |
| k=2 | +30.74pp (p=7.75e-35) | +27.24pp (p=2.84e-31) | +29.88pp (p=6.97e-37) | +22.54pp (p=1.02e-20) |
| k=3 | +20.49pp (p=2.15e-22) | +23.73pp (p=2.75e-28) | +21.27pp (p=1.72e-26) | +22.54pp (p=4.25e-26) |
| k=4 | +24.03pp (p=2.3e-41) | +26.71pp (p=3.5e-46) | +23.02pp (p=4.08e-29) | +25.70pp (p=2.24e-44) |

## 4. k=1~4 的 Δ(FD−Random)（并列分析（5 候选））

| k | original(676f 原 split) | family_random | family_stratified | strict_stratified |
|---:|---:|---:|---:|---:|
| k=1 | +11.31pp (p=6.02e-08) | +15.99pp (p=4.43e-12) | +12.83pp (p=6.16e-09) | +15.67pp (p=1.47e-13) |
| k=2 | +7.42pp (p=7.69e-05) | +6.50pp (p=0.00492) | +6.68pp (p=0.000598) | +0.88pp (p=0.756) |
| k=3 | +7.42pp (p=3.71e-06) | +8.96pp (p=2.18e-08) | +6.50pp (p=3.02e-06) | +6.69pp (p=1.11e-05) |
| k=4 | +0.00pp (p=1) | +0.00pp (p=1) | -0.53pp (p=0.678) | +0.00pp (p=1) |

## 5. 子组 Δ(FD−Random)（k=4，主分析；括号=评估集 n；p 为未校正 McNemar，q 见结果 JSON）

### 5.1 subgroups_defect_group

| 组 | original(676f 原 split) | family_random | family_stratified | strict_stratified |
|---|---:|---:|---:|---:|
| concurrency | +7.34pp (n=109, p=0.00781) | +8.80pp (n=125, p=0.000977) | -1.87pp (n=107, p=0.791) | +7.14pp (n=98, p=0.0156) |
| conditional_trigger | +45.00pp (n=20, p=0.00391) | +52.63pp (n=19, p=0.00195) | +52.63pp (n=19, p=0.00195) | +50.00pp (n=22, p=0.000977) |
| embedded | +8.11pp (n=74, p=0.0313) | +8.77pp (n=57, p=0.0625) | +7.04pp (n=71, p=0.0625) | +0.00pp (n=89, p=1) |
| language_semantics | +17.78pp (n=45, p=0.00781) | +12.20pp (n=41, p=0.0625) | +29.55pp (n=44, p=0.000244) | +33.33pp (n=30, p=0.00195) |
| legacy | +36.17pp (n=47, p=1.53e-05) | +29.79pp (n=47, p=0.000122) | +52.17pp (n=46, p=8.05e-07) | +46.00pp (n=50, p=2.38e-07) |
| memory_safety | +46.94pp (n=49, p=2.38e-07) | +51.28pp (n=39, p=1.91e-06) | +41.67pp (n=48, p=1.91e-06) | +33.33pp (n=45, p=6.1e-05) |
| odr_link | +6.67pp (n=15, p=1) | — | +6.67pp (n=15, p=1) | +0.00pp (n=14, p=1) |
| optimization_sensitive | +55.00pp (n=20, p=0.000977) | +45.83pp (n=24, p=0.000977) | +45.83pp (n=24, p=0.000977) | +95.00pp (n=20, p=3.81e-06) |
| real_world | +29.55pp (n=44, p=0.000244) | +31.37pp (n=51, p=3.05e-05) | +38.78pp (n=49, p=3.81e-06) | +30.00pp (n=40, p=0.000488) |
| stl | +15.00pp (n=100, p=6.1e-05) | +23.53pp (n=119, p=7.45e-09) | +4.59pp (n=109, p=0.267) | +15.09pp (n=106, p=3.05e-05) |
| undefined_behavior | +58.14pp (n=43, p=5.96e-08) | +68.09pp (n=47, p=4.66e-10) | +67.57pp (n=37, p=5.96e-08) | +61.11pp (n=54, p=2.33e-10) |

### 5.2 subgroups_defect_type

| 组 | original(676f 原 split) | family_random | family_stratified | strict_stratified |
|---|---:|---:|---:|---:|
| aba_problem | — | +42.86pp (n=21, p=0.00391) | +25.00pp (n=12, p=0.25) | +58.33pp (n=12, p=0.0156) |
| algorithm_misuse | — | +20.00pp (n=20, p=0.125) | +0.00pp (n=17, p=1) | +9.52pp (n=21, p=0.5) |
| alignment | — | +38.46pp (n=13, p=0.0625) | +38.46pp (n=13, p=0.0625) | — |
| atomic_ub | — | +0.00pp (n=17, p=1) | +18.75pp (n=16, p=0.25) | +0.00pp (n=19, p=1) |
| bit_operation | — | +0.00pp (n=13, p=1) | +0.00pp (n=12, p=1) | +0.00pp (n=22, p=1) |
| condition_variable | — | +0.00pp (n=13, p=1) | -40.00pp (n=15, p=0.0313) | +0.00pp (n=13, p=1) |
| conditional_trigger | — | +52.63pp (n=19, p=0.00195) | +52.63pp (n=19, p=0.00195) | +50.00pp (n=22, p=0.000977) |
| cross_tu_ub | — | — | +6.67pp (n=15, p=1) | +0.00pp (n=14, p=1) |
| deadlock | — | +0.00pp (n=28, p=1) | +0.00pp (n=17, p=1) | +0.00pp (n=15, p=1) |
| endianness | — | +0.00pp (n=10, p=1) | +0.00pp (n=14, p=1) | +0.00pp (n=15, p=1) |
| heap_overflow | — | +80.00pp (n=10, p=0.00781) | — | — |
| integer_overflow | — | +94.12pp (n=17, p=3.05e-05) | +91.67pp (n=12, p=0.000977) | +90.48pp (n=21, p=3.81e-06) |
| interrupt_safety | — | — | +0.00pp (n=12, p=1) | — |
| iterator_invalidation | — | +0.00pp (n=15, p=1) | +0.00pp (n=21, p=1) | +0.00pp (n=16, p=1) |
| lambda_capture | — | +0.00pp (n=25, p=1) | +0.00pp (n=18, p=1) | +0.00pp (n=19, p=1) |
| legacy_UB | — | +35.29pp (n=17, p=0.0313) | +62.50pp (n=16, p=0.00195) | +50.00pp (n=18, p=0.00391) |
| legacy_sanitizer | — | +31.58pp (n=19, p=0.0313) | +52.94pp (n=17, p=0.00391) | +60.00pp (n=20, p=0.000488) |
| lock_priority_inversion | — | +7.69pp (n=13, p=1) | -12.50pp (n=16, p=0.5) | +0.00pp (n=12, p=1) |
| logic_error | — | +0.00pp (n=13, p=1) | — | — |
| memory_order | — | +3.57pp (n=28, p=1) | +0.00pp (n=20, p=1) | +0.00pp (n=17, p=1) |
| move_semantics | — | +11.11pp (n=18, p=0.5) | +42.86pp (n=14, p=0.0313) | +16.67pp (n=12, p=0.5) |
| optimization_dependent | — | +45.83pp (n=24, p=0.000977) | +45.83pp (n=24, p=0.000977) | +95.00pp (n=20, p=3.81e-06) |
| other_ub | — | — | +40.00pp (n=10, p=0.125) | +21.43pp (n=14, p=0.25) |
| out_of_bounds | — | +100.00pp (n=10, p=0.00195) | +100.00pp (n=11, p=0.000977) | — |
| raii_violation | — | — | +40.00pp (n=15, p=0.0313) | +61.54pp (n=13, p=0.00781) |
| register_ub | — | — | +0.00pp (n=10, p=1) | +0.00pp (n=15, p=1) |
| smart_pointer | — | +77.78pp (n=27, p=9.54e-07) | +75.00pp (n=12, p=0.00391) | +82.35pp (n=17, p=0.000122) |
| stl_container_ub | — | +0.00pp (n=26, p=1) | -18.18pp (n=22, p=0.125) | +0.00pp (n=17, p=1) |
| string_ub | — | — | +0.00pp (n=19, p=1) | +0.00pp (n=16, p=1) |
| type_punning | — | +50.00pp (n=12, p=0.0313) | — | — |
| undefined_behavior | — | — | — | +100.00pp (n=10, p=0.00195) |
| uninitialized_read | — | +7.69pp (n=13, p=1) | +7.69pp (n=13, p=1) | +0.00pp (n=12, p=1) |
| virtual_function | — | +6.67pp (n=15, p=1) | +6.67pp (n=15, p=1) | — |
| volatile_misuse | — | — | +0.00pp (n=10, p=1) | +0.00pp (n=20, p=1) |

### 5.3 subgroups_planted

| 组 | original(676f 原 split) | family_random | family_stratified | strict_stratified |
|---|---:|---:|---:|---:|
| planted=False | +29.41pp (n=34, p=0.00195) | +36.36pp (n=44, p=3.05e-05) | +42.50pp (n=40, p=1.53e-05) | +35.90pp (n=39, p=0.000122) |
| planted=True | +23.68pp (n=532, p=2.35e-38) | +25.90pp (n=525, p=2.3e-41) | +21.55pp (n=529, p=1.14e-24) | +24.95pp (n=529, p=3.67e-40) |

### 5.4 subgroups_batch

| 组 | original(676f 原 split) | family_random | family_stratified | strict_stratified |
|---|---:|---:|---:|---:|
| corpus_672h | — | +28.57pp (n=28, p=0.00781) | +53.57pp (n=28, p=0.000275) | +37.93pp (n=29, p=0.000977) |
| expA | — | +60.00pp (n=40, p=1.19e-07) | +44.44pp (n=45, p=1.91e-06) | +45.83pp (n=48, p=4.77e-07) |
| expB | — | +53.19pp (n=47, p=5.96e-08) | +48.89pp (n=45, p=4.77e-07) | +41.07pp (n=56, p=2.38e-07) |
| expC | — | +30.95pp (n=84, p=2.98e-08) | +34.31pp (n=102, p=5.82e-11) | +46.51pp (n=86, p=1.82e-12) |
| expD | — | +23.53pp (n=119, p=7.45e-09) | +4.59pp (n=109, p=0.267) | +15.09pp (n=106, p=3.05e-05) |
| expE | — | +9.17pp (n=120, p=0.000977) | -2.08pp (n=96, p=0.791) | +7.95pp (n=88, p=0.0156) |
| expF | — | +8.77pp (n=57, p=0.0625) | +7.04pp (n=71, p=0.0625) | +0.00pp (n=89, p=1) |
| expG | — | +34.55pp (n=55, p=3.81e-06) | +40.00pp (n=55, p=4.77e-07) | +33.33pp (n=45, p=6.1e-05) |
| holdout_5_672h | — | +31.58pp (n=19, p=0.0313) | +50.00pp (n=18, p=0.00391) | +57.14pp (n=21, p=0.000488) |

## 6. 原 split 对照重算核对（管线正确性）

- 676f 登记：FD 54.5936%，Random 30.5654%，Δ+24.03pp，p=2.296e-41
- 677b 重算：FD 54.5936%，Random 30.5654%，Δ+24.03pp，p=2.296e-41
- 逐位一致：FD True、Random True、Δ True、p True、并列 Δ True

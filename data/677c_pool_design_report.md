# 677c · 非退化 Asset Pool 设计报告

- 数据源：`data/a5_676f_detection_matrix.json`（1137×8 冻结矩阵，未重跑 detect）+ `data/a5_676f_sample_manifest.json`（派生 571 / 评估 566）
- 复现：`.venv/Scripts/python.exe tools/analyze_677c_nondegenerate.py --stage pools`
- 机读：`data/677c_asset_pools.json`（本报告每个数字都能在 JSON 里按 key path 找到）

## 1. 8 资产退化统计（全池 n=1137）

| 资产 | catch | unknown | miss | unknown% | catch% | 恒unknown? | 预注册退化(catch率∉[5%,95%])? |
|---|---|---|---|---|---|---|---|
| asan | 399 | 10 | 728 | 0.88 | 35.09 | 否 | 否 |
| compile-time | 0 | 1137 | 0 | 100.00 | 0.00 | 是 | 是 |
| compiler-warn | 143 | 0 | 994 | 0.00 | 12.58 | 否 | 否 |
| cross-compile | 170 | 38 | 929 | 3.34 | 14.95 | 否 | 否 |
| linker | 10 | 0 | 1127 | 0.00 | 0.88 | 否 | 是 |
| tsan | 255 | 10 | 872 | 0.88 | 22.43 | 否 | 否 |
| ubsan | 268 | 10 | 859 | 0.88 | 23.57 | 否 | 否 |
| wunsequenced | 0 | 1137 | 0 | 100.00 | 0.00 | 是 | 是 |

关键事实：**linker 的 unknown 率是 0.00%**（10 catch + 1127 miss），不是卡片预估的">50%"。按 unknown 阈值（30%/50%/剔除恒 unknown）定义的三个池会**塌缩成同一个 6 资产集合**。因此 Pool A 在 unknown 阈值上叠加**预注册 catch 率 5% 下限**（论文 E4 勘误把 linker 列入三个退化资产的同一规则），恢复出卡片预期的 5 资产严格池；B/C 保持卡片字面定义（都是 6 资产，B≡C 如实记录）。

## 2. 三个池的定义与理由

### Pool A（严格）
- 规则：unknown_rate < 30% 且 catch_rate >= 5%（预注册产量下限）
- 资产（5 个）：asan, compiler-warn, cross-compile, tsan, ubsan
- 理由：同时剔除恒 unknown（wunsequenced/compile-time）与低产资产（linker catch 0.88%<5%）；候选集与 676f 预注册并列分析完全一致，可直接对账
- FD 排序（派生集 fail_hits）：asan > ubsan > tsan > cross-compile > compiler-warn
- 验证（1≤k≤|A|-1）：

| k | FD 选择 | Random 单点选择 | 单点集不同? | P(随机集==FD集)=1/C(n,k) |
|---|---|---|---|---|
| 1 | asan | tsan | 是 | 0.2 |
| 2 | asan,ubsan | tsan,ubsan | 是 | 0.1 |
| 3 | asan,ubsan,tsan | tsan,ubsan,cross-compile | 是 | 0.1 |
| 4 | asan,ubsan,tsan,cross-compile | tsan,ubsan,cross-compile,asan | 否（单点恰巧同集） | 0.2 |

### Pool B（中等）
- 规则：unknown_rate < 50% 且 catch_rate >= 0.5%
- 资产（6 个）：asan, compiler-warn, cross-compile, linker, tsan, ubsan
- 理由：放宽产量下限到 0.5%，容纳 linker（unknown=0% 但 catch 仅 0.88%）
- FD 排序（派生集 fail_hits）：asan > ubsan > tsan > cross-compile > compiler-warn > linker
- 验证（1≤k≤|A|-1）：

| k | FD 选择 | Random 单点选择 | 单点集不同? | P(随机集==FD集)=1/C(n,k) |
|---|---|---|---|---|
| 1 | asan | linker | 是 | 0.166667 |
| 2 | asan,ubsan | linker,ubsan | 是 | 0.066667 |
| 3 | asan,ubsan,tsan | linker,ubsan,compiler-warn | 是 | 0.05 |
| 4 | asan,ubsan,tsan,cross-compile | linker,ubsan,compiler-warn,cross-compile | 是 | 0.066667 |
| 5 | asan,ubsan,tsan,cross-compile,compiler-warn | linker,ubsan,compiler-warn,cross-compile,tsan | 是 | 0.166667 |

### Pool C（宽松）
- 规则：仅剔除 unknown_rate=100% 的恒 unknown 资产
- 资产（6 个）：asan, compiler-warn, cross-compile, linker, tsan, ubsan
- 理由：评审的字面要求：只去掉两个恒 unknown 资产，其余全保留
- FD 排序（派生集 fail_hits）：asan > ubsan > tsan > cross-compile > compiler-warn > linker
- 验证（1≤k≤|A|-1）：

| k | FD 选择 | Random 单点选择 | 单点集不同? | P(随机集==FD集)=1/C(n,k) |
|---|---|---|---|---|
| 1 | asan | linker | 是 | 0.166667 |
| 2 | asan,ubsan | linker,ubsan | 是 | 0.066667 |
| 3 | asan,ubsan,tsan | linker,ubsan,compiler-warn | 是 | 0.05 |
| 4 | asan,ubsan,tsan,cross-compile | linker,ubsan,compiler-warn,cross-compile | 是 | 0.066667 |
| 5 | asan,ubsan,tsan,cross-compile,compiler-warn | linker,ubsan,compiler-warn,cross-compile,tsan | 是 | 0.166667 |

## 3. 验收判定

- 3 个池定义完成：A（5 资产）/ B（6）/ C（6，≡B）。
- 每个池都存在 1<k<|A| 使 FD 与 Random 单点选择不同：A=True、B=True、C=True；且对一切 1≤k<|A|，P(随机抽到 FD 同集)=1/C(n,k)<1 ⇒ 结构上 Random 与 FD 必然可分（k=|A|-1 的单点重合只是抽样巧合，正是 676f 并列分析 k=4 失效的原因）。
- 退化资产 unknown 比例统计完整（第 1 节表 + JSON asset_stats）。

## 4. 诚实边界

- 退化统计用了全池率（含评估集）：这是池**构成**设计决策（676f 并列分析同口径），不是逐样本选择泄漏；逐样本选择只用派生集。
- Pool A 的候选集与 676f co_primary_excl_degenerate 完全一致 ⇒ 其结果应逐位复现 676f 并列分析（在 a5 stage 做了对账）。
- k=|A| 时三臂恒等于全池，属预算退化，不进扫描（676f is_degenerate_k 同口径）。

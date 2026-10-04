# 676l · 检测器能力深度 Benchmark 总报告

- **生成**：2026-10-04T09:53:56+08:00
- **脚本**：`tools/benchmark_676l_analysis.py`（可复现，`--stage all`）
- **数据源**：`data/blindspot_676g_detection_matrix.json`（676g 产物，**只读**）
- **红线**：判定矩阵 / 检测器（`tools/holdout_reveal_661.py`）/ 论文（`research/`）/ 样本数据（`data/holdout_expansion/`）零修改；未 push。

---

## 1. 分析范围与方法

### 1.1 数据来源与矩阵规模

- 判定矩阵：`data/blindspot_676g_detection_matrix.json`，schema `queyi-blindspot-matrix/676g`
- 规模：**1147 样本 × 8 资产 = 9176 格**，缺失 **0**，非法 verdict **0**
- verdict 分布：{'catch': 1216, 'miss': 5598, 'unknown': 2362}（catch 13.252% / miss 61.007% / unknown 25.7411%）
- ground truth：样本级 `expected_verdict`，catch 674 / miss 473
- 与样本 `.json` 交叉验证：比对 1042 条，不一致 **0** 条
- 缺陷类型：70 类；批次：{'holdout': 41, 'corpus': 64, 'expA': 100, 'expB': 94, 'expC': 200, 'expD': 200, 'expE': 200, 'expF': 149, 'expG': 99}
- 挂起样本：35 条

### 1.2 指标定义

| 指标 | 定义 |
|---|---|
| TP | expected=catch 且 detector=catch |
| FN | expected=catch 且 detector=miss |
| FP | expected=miss 且 detector=catch |
| TN | expected=miss 且 detector=miss |
| Precision | TP/(TP+FP) |
| Recall | TP/(TP+FN) |
| Specificity | TN/(TN+FP) |
| F1 | 2PR/(P+R) |
| Accuracy | (TP+TN)/(TP+FN+FP+TN) |
| unknown | 单独统计，**不进**混淆矩阵 |

OR 聚合（样本级）= 选中资产任一 catch ⇒ catch；全部 unknown ⇒ unknown；其余 miss（与 `AttributionExecutor` 同义）。

### 1.3 数据质量：676g vs 676f 矩阵差异（如实记录，不修改）

- 676f 矩阵 1137 条 / 676g 矩阵 1147 条；按 (source_batch, sample_id) 可比的交集 **349** 条（其余因批次命名不同不可直接配对）
- 交集内逐资产判定差异：`{'cross-compile': 10, 'asan': 13, 'tsan': 8, 'ubsan': 7}`
- 典型差异：`cross-compile` 在 expD 的 10 个 STL 样本上 676f=catch / 676g=miss。
- **影响**：FD 的 fail_hits 排序来自 676f 派生集，而本批评估用 676g 矩阵；本批因此同时给出 in-sample 排序作为对照（见 §4.2）。

---

## 2. 单检测器性能排名

| 排名 | 检测器 | Precision | Recall | F1 | Specificity | Accuracy | unknown率 | TP | FN | FP | TN |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `asan` | 95.34% | **58.50%** | 72.51% | 95.97% | 74.05% | 0.87% | 389 | 276 | 19 | 453 |
| 2 | `ubsan` | 94.07% | **38.20%** | 54.33% | 96.61% | 62.44% | 0.87% | 254 | 411 | 16 | 456 |
| 3 | `tsan` | 91.25% | **36.09%** | 51.72% | 95.13% | 60.60% | 0.87% | 240 | 425 | 23 | 449 |
| 4 | `compiler-warn` | 90.21% | **19.14%** | 31.58% | 97.04% | 51.26% | 0.00% | 129 | 545 | 14 | 459 |
| 5 | `cross-compile` | 83.61% | **15.62%** | 26.32% | 95.61% | 48.51% | 3.31% | 102 | 551 | 20 | 436 |
| 6 | `linker` | 90.00% | **1.34%** | 2.63% | 99.79% | 41.94% | 0.00% | 9 | 665 | 1 | 472 |
| 7 | `compile-time` | n/a | **n/a** | n/a | n/a | n/a | 100.00% | 0 | 0 | 0 | 0 |
| 8 | `wunsequenced` | n/a | **n/a** | n/a | n/a | n/a | 100.00% | 0 | 0 | 0 | 0 |

- 8 资产 OR（分母 expected=catch 674）= **94.21%**（635 hit）；全 1147 口径 catch-rate = 61.64%。
- 两个结构性恒 unknown 资产（`wunsequenced`、`compile-time`）的 precision/recall 均为 n/a（无已知判定）——它们在池里的作用是「被 FD 主动排除」，不是提供检出。

**与 676g 的交叉核对（口径不同，必须并报）**：

| 量 | 676g 报告 | 本批（676l） | 差异来源 |
|---|---|---|---|
| 样本级检出 | 707/1147 = 61.6% | 707/1147 = 61.64% | **一致**（同为 8 资产 OR） |
| 单资产 asan catch | 408 | 408 | **一致**（含 expected=miss 的 FP） |
| 边际贡献 asan | +12.1pp | +19.29pp | 676g 分母 = 全部 1147；本批分母 = expected=catch 的 674 |
| 边际贡献 ubsan / tsan / compiler-warn | +7.2 / +7.4 / +4.6pp | +10.98 / +10.39 / +5.93pp | 同上（集合一致，次序见下） |

- **排序一致性**：两种口径下 `asan` 都稳居第一（676g +12.1pp / 本批 +19.29pp），`ubsan`、`tsan`、`compiler-warn` 构成第二梯队（集合一致），`compile-time`/`wunsequenced` 都是 0.00pp。**次序差异**：676g 里 `tsan`(+7.4) 略高于 `ubsan`(+7.2)、`cross-compile`(+1.2) 高于 `linker`(+0.9)；本批相反（`ubsan` 10.98 > `tsan` 10.39；`linker` 1.34 > `cross-compile` 0.30）。两组差异都 < 1pp，属口径（分母不同）与矩阵差异的共同作用，**不改变「asan 最强、两个结构性资产零信息」的结论**。

- 详见 `676l_单检测器性能报告.md`（含 8×70 recall 矩阵、planted / 批次 / 家族分组）。

---

## 3. 检测器互补性

- 28 对共现分析完成；**实质对**（双方 catch ≥ 50）里最冗余对：`asan`+`tsan` J=0.3313；`asan`+`ubsan` J=0.2579；`ubsan`+`compiler-warn` J=0.2292
- 最互补对：`tsan`+`compiler-warn` J=0.0628；`asan`+`compiler-warn` J=0.0889；`compiler-warn`+`cross-compile` J=0.0996
- 结构性互补：`linker` 的 10 个 catch **全部**落在 `asan`/`ubsan`/`tsan` 的 10 个 unknown 里（强 ODR ⇒ 动态检测器链接失败）⇒ 它虽只贡献 1.34pp，但覆盖的正是动态资产看不见的那一块。

### 3.1 边际贡献排序（对 OR recall，分母 expected=catch）

| 排名 | 检测器 | 边际贡献(pp) |
|---:|---|---:|
| 1 | `asan` | 19.29 |
| 2 | `ubsan` | 10.98 |
| 3 | `tsan` | 10.39 |
| 4 | `compiler-warn` | 5.93 |
| 5 | `linker` | 1.34 |
| 6 | `cross-compile` | 0.30 |
| 7 | `compile-time` | 0.00 |
| 8 | `wunsequenced` | 0.00 |

### 3.2 聚类（1 − Jaccard，average linkage，切 3 组）

| 组 | 成员 | 代表 |
|---|---|---|
| 1 | `linker` | `linker` |
| 2 | `compile-time`, `wunsequenced` | `wunsequenced` |
| 3 | `asan`, `compiler-warn`, `cross-compile`, `tsan`, `ubsan` | `asan` |

- 详见 `676l_检测器互补性报告.md`（28 对全表、8×8 相关性矩阵、κ）。

---

## 4. 最佳组合分析

### 4.1 穷举最佳 k（分母 expected=catch）

| k | 最佳组合 | 最佳 recall | 最差 recall |
|---:|---|---:|---:|
| 1 | `asan` | **57.72%** | 0.00% |
| 2 | `asan`, `ubsan` | **75.67%** | 0.00% |
| 3 | `asan`, `ubsan`, `tsan` | **86.65%** | 1.34% |
| 4 | `asan`, `ubsan`, `tsan`, `compiler-warn` | **92.58%** | 16.47% |
| 5 | `asan`, `ubsan`, `tsan`, `compiler-warn`, `linker` | **93.92%** | 32.20% |
| 6 | `asan`, `ubsan`, `tsan`, `compiler-warn`, `cross-compile`, `linker` | **94.21%** | 55.49% |
| 7 | `asan`, `ubsan`, `tsan`, `compiler-warn`, `cross-compile`, `linker`, `compile-time` | **94.21%** | 74.93% |
| 8 | 全池 | 94.21% | 94.21% |

### 4.2 FD vs 最佳 vs Random（k=4）

| 臂 | 组合 | recall | 说明 |
|---|---|---:|---|
| 穷举最佳 | `asan`, `ubsan`, `tsan`, `compiler-warn` | **92.58%** | 全量 1147 上的上界 |
| FD(676f 派生集) | `asan`, `ubsan`, `tsan`, `cross-compile` | 86.94% | 预注册策略，派生集训练 |
| FD(in-sample) | `asan`, `ubsan`, `tsan`, `compiler-warn` | 92.58% | 全量排序（含泄漏），只作参考 |
| Random 均值 | — | 63.65% | 2000 次抽样 |
| Static | `compiler-warn`, `cross-compile`, `linker`, `wunsequenced` | 32.20% | 静态资产字典序前缀（k=4） |

- 最佳组合位于 Random 分布的 **99.0** 百分位；FD(676f) 位于 **96.5** 百分位。
- FD(676f) 的 k=4 组合**不等于**穷举最佳。

### 4.3 增量收益曲线与拐点

| k | 最佳 recall | Δ(pp) |
|---:|---:|---:|
| 1 | 57.72% | +57.72 |
| 2 | 75.67% | +17.95 |
| 3 | 86.65% | +10.98 |
| 4 | 92.58% | +5.93 |
| 5 | 93.92% | +1.34 |
| 6 | 94.21% | +0.30 |
| 7 | 94.21% | +0.00 |
| 8 | 94.21% | +0.00 |

- 拐点 **k = 5**；k=4 最佳组合已达全池的 98.3%。
- 详见 `676l_最佳组合分析报告.md`。

---

## 5. 错误模式

- 全检测器一致盲区（expected=catch 且 8 资产无一 catch）：**39 条**；严格 6 可用资产全 miss 口径 39 条。
- 盲区 Top 类型：deadlock(31)；condition_variable(3)；memory_safety(2)；raii_violation(1)；atomic_ub(1)；heap_overread(1)
- unknown 结构：`wunsequenced`/`compile-time` 各 1147 格恒 unknown；`asan`/`ubsan`/`tsan` 各 10 格；`cross-compile` 38 格。
- 详见 `676l_错误模式分析报告.md`（FN Top5、FP 成因、样本清单）。

---

## 6. 可视化图表（`data/676l_figures/`，PNG，300 DPI）

| 文件 | 内容 |
|---|---|
| `fig1_detector_performance.png` | (a) 8 检测器 recall 降序柱；(b) precision / recall / F1 分组柱 |
| `fig2_correlation_heatmap.png` | 8×8 相关性热力图（Pearson，两两完整观测；n/a = 无共同已知判定） |
| `fig3_marginal_contribution.png` | 8 检测器留一法边际贡献排序（分母 674） |
| `fig4_incremental_gain.png` | k=1…8 最佳组合 recall 曲线 + 最差组合 + 拐点 k=5 |
| `fig5_dendrogram.png` | 层次聚类树状图（1 − Jaccard，average linkage） |
| `fig6_confusion_composition.png` | 每检测器 TP/FN/FP/TN/unknown 堆叠构成（占 1147） |
| `fig7_k4_random_distribution.png` | k=4 的 2000 次 Random 分布 vs 最佳 / FD |

- 图表用 **matplotlib** 生成（英文标签，避免中文字体缺失）；matplotlib **不是本仓依赖**，未安装时 `--stage figures` 整体跳过，其余阶段与 JSON 产物不受影响。

---

## 7. 对论文的贡献（可写进论文的结果）

| # | 结论 | 支撑的 claim | 数据位置 |
|---:|---|---|---|
| C1 | 单资产 recall 排名：`asan` 最强（58.50%），8 资产 OR 达 94.21% | 资产池能力量化 | `676l_benchmark_results.json` → `perf.per_asset` |
| C2 | 资产间互补性（实质对，双方 catch ≥ 50）：最互补对 `tsan`+`compiler-warn` Jaccard = 0.0628，最冗余对 `asan`+`tsan` Jaccard = 0.3313 | 「池的价值来自互补而非冗余」 | `complement.pairs` |
| C3 | 边际贡献排序：asan(19.3pp) > ubsan(11.0pp) > tsan(10.4pp) > compiler-warn(5.9pp)，零信息资产 = ['compile-time', 'wunsequenced'] | FD「避开零信息资产」的机制证据 | `complement.marginal_contribution` |
| C4 | k=1…7 穷举：k=4 最佳 recall = 92.58%，k=5 起边际收益骤降，拐点 k=5 | 「k=4 是合理预算」 | `combo.exhaustive_by_k` / `incremental_curve` |
| C5 | 全检测器一致盲区 39 条（expected=catch），集中在语义/设计层类型 | 能力边界（Threats to Validity） | `errors.all_detector_blindspot` |
| C6 | `wunsequenced`/`compile-time` 边际贡献 0.00pp、恒 unknown | 「结构性零信息资产」的定义证据 | `complement.marginal_contribution` |

**不建议写进论文的**：任何把 `expected_verdict` 当真实缺陷真值的表述；把 FP 直接当检测器错误的表述（见 §7）。

---

## 8. 对 FD 策略的评价

1. **FD(676f) 的 k=4 组合**（`asan`, `ubsan`, `tsan`, `cross-compile`）不是全量穷举最佳（92.58%），差 5.64pp。差的来源是 rank-4 的选择：FD 派生集给 `cross-compile`（派生 fail_hits 89），而 676g 全量上 `cross-compile` 只 catch 122 条（边际贡献 0.30pp），`compiler-warn` catch 143 条（边际贡献 5.93pp）。**即：FD 在派生集上把 cross-compile 的命中率估高了**（676f 矩阵 cross-compile 170 vs 676g 122，见 §1.3）。
2. 它显著优于 Random（均值 63.65%），位于 Random 分布的 96.5 百分位。
3. **但 FD 的优势主要来自池构成效应，不是选择效应**：`wunsequenced`/`compile-time` 的边际贡献是 0.00pp，FD 的价值首先是「不把预算花在这两个资产上」。这与 676f 的 `uninterpretable` 条款一致，**不得**升级为「FD 选择策略更聪明」。
4. **矩阵来源差异**：FD 的排序来自 676f 派生集（cross-compile 89 次），本批 676g 全量排序把 compiler-warn（143 次）排到第 4 —— 说明 FD 是**真预测器**（在派生集上估计），不是 oracle。两者差异正是「训练/评估分离」的正常代价。

---

## 9. 局限性

1. **`expected_verdict` 是单标注**（生成样本的 Agent 自标），不是真实缺陷真值 ⇒ 所有指标都是「相对于标注」的。
2. **样本偏差**：planted=true 占 88%（1009/1147），指标偏向植入缺陷；对真实缺陷的泛化性有限（planted=false 仅 74 条）。
3. **OR 聚合假设**：本批的「组合 recall」假设任一资产 catch 即算 catch；实际使用中多资产报告可能需要人工审核，不是简单 OR。
4. **口径差异**：本批 recall 分母 = expected=catch 的 674 条；676f 报告的 catch-rate 分母 = 全部样本。两者数字不可直接相减。
5. **unknown 不进混淆矩阵**：`wunsequenced`/`compile-time` 恒 unknown，其 precision/recall 无定义；若 unknown 比例更高的资产存在，算出的性能会高估。
6. **矩阵间差异**：676g 与 676f 在共同样本上存在少量判定差异（cross-compile 10 例等），本批以 676g 为准、**不修改**任何矩阵。
7. **单机单工具链**：结论限于 MinGW g++ 13.1 / WSL g++ 13.3 / clang++ 22.1.8 环境；换平台/换检测器版本，数字会变。

---

## 10. 复现

```bash
# 全量分析（validate → perf → complement → combo → errors → figures → reports）
python tools/benchmark_676l_analysis.py --stage all

# 单阶段
python tools/benchmark_676l_analysis.py --stage validate
python tools/benchmark_676l_analysis.py --stage perf
python tools/benchmark_676l_analysis.py --stage complement
python tools/benchmark_676l_analysis.py --stage combo
python tools/benchmark_676l_analysis.py --stage errors
python tools/benchmark_676l_analysis.py --stage figures
```

机读结果：`data/676l_benchmark_results.json`（本报告全部数字的唯一来源）。

## 11. 提交信息

- commit：`676l: 检测器深度 Benchmark——8 资产 P/R/F1 + 互补性 + 最佳组合 + 边际贡献`（DCO 签署，`git log --oneline -1` 取 hash；未 push）
- `git add` 清单：`tools/benchmark_676l_analysis.py`、`data/676l_*.md`、`data/676l_benchmark_results.json`、`data/676l_figures/`
- 未 add：`data/blindspot_676g_*`、`data/holdout_expansion/`、`research/`、`tools/holdout_reveal_661.py`

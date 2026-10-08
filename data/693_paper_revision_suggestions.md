# 693-E7 · 论文修改建议（**不改正文**，只写建议）

- 生成：2026-10-08｜批次：693-E7
- 目标稿：`research/latex/queyi_neurips2027_v1.1.tex`（**本批未改动该文件**，693 红线 1）
- 锚点约定：**全部用 grep 锚点（唯一子串），不用行号**——行号会随任何一次编辑失效。
  用法：`grep -n '<锚点>' research/latex/queyi_neurips2027_v1.1.tex`
- 严重度：🔴 必须改（数字错/口径不一致）｜🟡 建议改（提升说服力）｜🟢 可选（补充材料）

---

## 0. 本批新发现的优先级排序

| # | 发现 | 严重度 | 出处 |
|---:|---|---|---|
| 1 | **单检测器表与并集 recall 使用了**过期的 ground truth（catch 674 / miss 473），当前冻结标签是 **catch 640 / miss 507** | 🔴 | `data/693_defect_type_deep_analysis.json::stale_metric_crosscheck_vs_676l` |
| 2 | 人类标注材料包有 **13 条源码残留 `expected_verdict` 注释**（去标识化失败） | 🔴 | `data/693_ai_double_label.json::leak_exposed` |
| 3 | AI 双标已完成：**raw 78.6% / κ=0.495**（剔除泄漏后 77.3% / κ=0.458） | 🟡 | 同上 |
| 4 | 逐资产 **AUC**：`linker` = **0.506**（等于随机） | 🟡 | `data/693_meta_evaluation_v2.json::discrimination` |
| 5 | LLM 臂 **ECE = 0.381**，置信度 0.995 处实际正确率仅 **0.6125**（强过自信） | 🟡 | `data/693_meta_evaluation_v2.json::calibration` |
| 6 | 模板克隆导致的可检测性模型**准确率高估**（随机折 vs 分组折） | 🟡 | `data/693_detectability_model.json::cv.leakage_inflation` |
| 7 | 反事实：**翻转 ground truth 不改变 A5 主端点 Δ**（结构性事实） | 🟡 | `data/693_counterfactual_extended.json::arm_c_label_quality` |
| 8 | 2026 年出现**同构外部证据**（fuzzer 并集与静态分析器并集几乎不相交） | 🟡 | `data/693_related_work_update.md` §1 N2 |
| 9 | 原始项目 CVE 检测臂**未执行**（红线 8 与任务 E1.2 冲突） | 🟢 | `data/693_original_repo_cve_report.md` §0 |

---

## 1. 🔴 必须改：单检测器表与并集 recall 的 ground truth 过期

### 1.1 锚点

```bash
grep -n 'recall uses the' research/latex/queyi_neurips2027_v1.1.tex          # 分母声明
grep -n 'Single-asset ranking' research/latex/queyi_neurips2027_v1.1.tex     # 表标题
grep -n 'Union and best-' research/latex/queyi_neurips2027_v1.1.tex         # 并集段
```

### 1.2 问题

论文的表与并集 recall 用的是 `expected=catch` 分母 **n=674**。该数字来自
**676m 标签修复之前**的 ground truth（catch 674 / miss 473）。
当前冻结矩阵（`data/blindspot_676g_detection_matrix.json`，681 修复后）为
**catch 640 / miss 507**，差 **34** 条 —— 正是 676m 修正的 **34 条挂起样本**
（sanitizer 挂起 ⇒ 超时 ⇒ miss）。

来源：`data/676l_单检测器性能报告.md` 在 676m 之后**从未重算**。
`TP` / `FP` / `TN` 逐位不变，**只有 `FN` 与分母变了**。

### 1.3 建议替换的数值（现算，命令见 §1.5）

分母口径沿用论文自己的约定（`expected=catch` 且该资产非 `unknown`）：

| Asset | recall（旧） | **recall（新）** | precision | F1（旧） | **F1（新）** | marginal（旧） | **marginal（新）** |
|---|---:|---:|---:|---:|---:|---:|---:|
| `asan` | 58.5% | **61.65%** | 95.3% | 0.725 | **0.749** | +19.29 | **+20.60** |
| `ubsan` | 38.2% | **40.25%** | 94.1% | 0.543 | **0.564** | +10.98 | **+11.73** |
| `tsan` | 36.1% | **38.03%** | 91.3% | 0.517 | **0.537** | +10.39 | **+11.09** |
| `compiler-warn` | 19.1% | **20.16%** | 90.2% | 0.316 | **0.330** | +5.93 | **+6.25** |
| `cross-compile` | 15.1% | **16.48%** | 83.6% | 0.255 | **0.275** | +0.30 | **+0.32** |
| `linker` | 1.3% | **1.41%** | 90.0% | 0.026 | **0.028** | +1.34 | **+1.41** |

**并集 recall**：`94.21% (635/674)` → **`99.22% (635/640)`**。

> ⚠ 这个变化**很大**（+5.01pp），必须处理。它同时说明一件事：
> 676m 修正后，`expected_verdict=catch` 的样本里只有 **5 条**是六资产全 miss 的。
> 也就是说 **"声明可检出"与"仪器实际检出"在修正后高度重合**——
> 这本身是需要在正文解释的现象（建议在并集段加一句口径说明），
> 而不是简单把 94.21 改成 99.22 就完事。

### 1.4 三选一，必须选一个（不要混用）

| 方案 | 做法 | 代价 |
|---|---|---|
| **A（推荐）** | 全文统一到当前冻结标签（catch 640），重算上表与并集 | 需同步检查附录里所有引用 674 的地方 |
| B | 回滚到 676m 之前的标签 | ❌ 不可行：676m 的修正是正确的（挂起 ≠ catch） |
| C | 正文并列两个 vintage | 会被审稿人质疑"为什么有两个真值" |

**注意**：38.4% 盲区率（440/1147）**不受影响**——它用全 1147 分母，
不依赖 `expected_verdict`。论文中所有 38.4% 的表述**不需要改**。

### 1.5 复算命令（一行可复核）

```bash
python tools/analyze_693_defect_types.py
python -c "import json;d=json.load(open('data/693_defect_type_deep_analysis.json',encoding='utf-8'));print(d['stale_metric_crosscheck_vs_676l'])"
```

---

## 2. 🔴 必须改：人类标注材料包的 13 条标签泄漏

### 2.1 锚点

```bash
grep -n 'leakage-sanitized sources' research/latex/queyi_neurips2027_v1.1.tex
grep -n 'Human annotation protocol' research/latex/queyi_neurips2027_v1.1.tex
```

### 2.2 问题

论文称材料包 `leakage-sanitized sources (280 comment redactions, 5 identifier renames,
residual scan clean, 144/145 compile)`。**实测发现残留**：145 条中有 **13 条**源码注释里
仍有 `// expected_verdict: <catch|miss>` 原文（689 的净化正则没覆盖这一行）。

泄漏条目：`S021 S022 S033 S034 S035 S039 S051 S055 S058 S074 S111 S120 S133`
（`data/693_ai_double_label.json::leak_exposed`）

### 2.3 建议

1. **把 `residual scan clean` 改成事实**：加一句限定——
   *"our residual scan covered 12 pattern families; a subsequent adversarial re-read
   found 13 files retaining an `expected_verdict` comment, now flagged
   `leak_suspected=yes` and excluded from the primary κ, with the full-κ reported as
   sensitivity."* ——**主动披露比被审稿人发现好得多**，而且这正好支撑 T1 的"未解决"立场。
2. 重跑净化（或直接把这 13 条从主 κ 里剔除），并在附录登记。
3. 论文中 `144/145 compile` 与本次 `13 leak` 不冲突（一个是编译、一个是泄漏），但要说明是两个独立扫描。

---

## 3. 🟡 建议改：AI 双标结果可以写进 T1

### 3.1 锚点

```bash
grep -n 'designed and packaged but not executed' research/latex/queyi_neurips2027_v1.1.tex
grep -n 'T1 --- Label validity' research/latex/queyi_neurips2027_v1.1.tex
```

### 3.2 建议新增的句子（T1 段内）

> *We additionally ran a **second AI annotator** (independent prompt, static semantic
> reading, no access to measured verdicts) over all 145 packaged samples:
> raw agreement **78.6%**, Cohen's κ **0.495** (77.3% / 0.458 after excluding the 13
> leak-flagged files). Disagreements are **concentrated in the fallback class**:
> `other_ub` alone contributes 21 of 31 disagreements (32.3%), and the `language_oop`
> family 22 of 73 (30.1%). This is direct evidence that **the 34-type vocabulary's
> fallback resolution is a label-side weakness**, independent of any human annotation.*

**为什么值得写**：这是"标签有效性"一节里**唯一一个可以立刻引用、且不依赖人类**的新证据，
而且它把问题定位到**词表分辨率**（可修）而不是"标注者不行"（不可修）。

### 3.3 需要一并说明的口径

- A 侧不是人类标注，是**实测标签**（`expected_verdict`）；A vs B 的分歧**部分**是
  "实测可检出 vs 静态判读认为不该检出"的语义层分歧，**不完全等价于两个人类的分歧**。
- 分歧方向：22 条 A=miss/B=catch，5 条 A=catch/B=miss，4 条涉及 `unknown`。

---

## 4. 🟡 建议改：逐资产 AUC 与校准（附录或 §Limitations）

### 4.1 锚点

```bash
grep -n 'linker is low-marginal but irreplaceable' research/latex/queyi_neurips2027_v1.1.tex
```

### 4.2 建议新增（可放该段末尾，或附录 T17）

| Asset | AUC（把资产当二分类器，真值 = expected_verdict） |
|---|---:|
| `asan` | 0.776 |
| `ubsan` | 0.674 |
| `tsan` | 0.672 |
| `compiler-warn` | 0.579 |
| `cross-compile` | 0.556 |
| `linker` | **0.506**（≈ 随机） |
| OR（八资产） | 0.891 |

> **这一组数字强化了论文已有的 "linker is low-marginal but irreplaceable" 论断**：
> `linker` 的 AUC 只有 0.506，**几乎没有区分能力**；它之所以不可替代，
> 完全来自那 10 个**落在 sanitizer `unknown` 里**的 catch。
> 建议在该段加一句：*"its AUC is 0.506 — indistinguishable from chance; its value is
> entirely concentrated in the 10 samples that no other asset can observe."*

### 4.3 校准（建议进 Limitations）

- LLM 臂 **ECE = 0.381**；在置信度 0.995 的桶里实际正确率仅 **0.6125**
  ⇒ LLM 的 confidence **不可用作可信度权重**。
- 检测器是确定性系统（confidence ≡ 1），其"ECE" 只是 `1 − accuracy`，**不可与 LLM 的 ECE 并列比较**。
- 数据源：`data/693_meta_evaluation_v2.json::calibration`

---

## 5. 🟡 建议改：模板克隆的泄漏效应（强化已有 caveat）

### 5.1 锚点

```bash
grep -n 'within-batch template-clone rate' research/latex/queyi_neurips2027_v1.1.tex
grep -n 'clone rate is' research/latex/queyi_neurips2027_v1.1.tex
```

### 5.2 建议

论文已披露 62.2% 克隆率，但**没有量化它对"建模类结论"的影响**。
693-E3 给出了一个可直接引用的数字：在 1147 条上拟合可检测性模型时，
**随机 5 折 vs 按结构签名分组 5 折**的准确率差就是泄漏高估幅度。

（具体数值见 `data/693_detectability_model.json::cv.leakage_inflation`，**引用时现读 JSON，不要抄本文件**。）

> 建议措辞：*"Any learned predictor trained on this corpus inherits an optimistic bias
> from template cloning; we quantify it by comparing random-fold and
> structure-grouped-fold CV (Δacc = X pp) and report the grouped figure as the
> honest one."*

---

## 6. 🟡 建议改：反事实口径分离

### 6.1 锚点

```bash
grep -n 'label-sensitive conclusions are flagged' research/latex/queyi_neurips2027_v1.1.tex
```

### 6.2 建议

论文现有表述（标签翻转可使绝对盲区率 `6.6% → 14.3%`）是对的，但容易与
"A5 主端点对标签噪声敏感"混淆。693-E4 显式分离了两种翻转对象：

- **翻转 ground truth（`expected_verdict`）⇒ A5 主端点 Δ 逐位不变（0.000pp）**；
- 翻转 `per_asset` 判定（检测器噪声）⇒ Δ 才变（±0.7pp @ 5–15%）。

> 建议加一句：*"Note that Δ(FD−Random) is **structurally invariant** to ground-truth
> noise: it is computed from `per_asset` verdicts only. Label quality therefore affects
> *rate* claims but not *contrast* claims — which is exactly why we separate them."*

---

## 7. 🟡 建议改：Related Work 补 2026 外部锚点

### 7.1 锚点

```bash
grep -n 'Related Work' research/latex/queyi_neurips2027_v1.1.tex | head -3
```

### 7.2 建议引用（详情见 `data/693_related_work_update.md`）

| 文献 | 一句话 | 用途 |
|---|---|---|
| Cao et al., *Code Benchmarks Should Prioritize Rigor, Reliability, and Reproducibility*, `arXiv:2501.10711`（v5 2026） | 672 个代码基准的十年调查 + HOW2BENCH 55 条检查单 | 把本装置的"自省"接到社区方法论上；**并用 HOW2BENCH 逐条自查、把未达标项写进 Limitations** |
| Hassler, Görz, Lipp, *A Comparative Study of Fuzzers and Static Analysis Tools…*, `arXiv:2505.22052`（v2 2026） | 5 静态分析器 + 13 fuzzer 作用于 100+ 真实漏洞；**两个家族的并集几乎不相交** | ⭐ **最强的外部同构证据**：支撑"并集 ≫ 单工具"。限定语：Queyi 的互补发生在**同一家族内**，比跨家族更难 |
| SV-COMP 2026 报告（TACAS 2026） | 61 个验证器 + 16 个校验器；witness 校验 + 第三方裁判 | 作为**方法论对照**，并诚实登记 Queyi **没有**第三方裁判 |

---

## 8. 🟢 可选：把 693 的新材料写进 Data/Code 附录

| 材料 | 建议位置 |
|---|---|
| `data/693_data_manifest.sha256`（14 项冻结产物） | 复现附录：说明"冻结产物有 sha256 清单，CI 逐条校验" |
| `docs/ENVIRONMENT.md` | 复现附录：环境锁定表（含两套画像与两个已知坑） |
| `data/693_human_adjudication_package.csv` + 指南 + 校准题 | 附录 `app:reframe689`：从"designed and packaged"升级为"**packaged, second-annotator piloted, awaiting human**" |
| `data/693_defect_type_report.md` | 盲区附录：逐类型盲区排序（`cross_tu_ub` / `strict_aliasing` / `uninitialized_read` **100% 盲**） |
| `data/693_meta_evaluation_report.md` | 新增的元评估维度表（区分度/稳定性/公平性/效率/校准） |

---

## 9. 不要改的地方（避免误伤）

| 内容 | 为什么不要动 |
|---|---|
| 所有 **38.4%** 盲区率表述 | 用全 1147 分母，**不受标签 vintage 影响** |
| `+24.03pp` / `+12.81pp` / `p=2.3×10⁻⁴¹` | 来自 676f 的 A5 主分析，**本批未复核其标签依赖**；如需复核需单独一批（本批红线 8 禁止重跑） |
| `62.2%` 克隆率 | 与 676k 一致，本批未重算 |
| `catch 707 / miss 440` 的**覆盖计数** | 这是 per_asset 判定的性质，**与 ground truth 无关**，不受 676m 影响 |
| 正文 tex 文件本身 | 693 红线 1：本批**只写建议**，不改正文 |

---

## 10. 一句话总结给作者

> **只有一处是"错"，其余都是"可以更强"**：单检测器表与并集 recall 的 ground truth
> 停留在 676m 之前（674 → 640），必须统一口径重算；
> 顺带主动披露材料包的 13 条泄漏、把 AI 双标的 κ=0.495 写进 T1、
> 补上 `linker` 的 AUC=0.506 与 LLM 的 ECE=0.381，并引用 2026 年的两个外部锚点。

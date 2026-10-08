# EXPERIMENTS · 实验复现手册

> 本文回答：**论文里每个数字是哪个实验、用什么命令、在什么环境下算出来的。**
> 环境锁定见 [`ENVIRONMENT.md`](ENVIRONMENT.md)；30 分钟上手见 [`GETTING_STARTED.md`](GETTING_STARTED.md)。

---

## 0. 一句话原则

**本仓库的"复现"= 从 `data/` 下已落盘的产物重新读算出论文数字，而不是重跑检测器。**
重跑检测器（需要 WSL + MinGW + clang + 数小时）是**再生产**，不是**复现**。
两者都支持，但默认路径是前者。

---

## 1. 一键复现（推荐入口）

```bash
bash Scripts/reproduce_all.sh --out out/693_reproduce
```

五个阶段，前一步失败即停（fail-loud）：

| 阶段 | 做什么 | 证据 |
|---|---|---|
| S0 | 环境体检 | `out/.../00_environment.txt` |
| S1 | 14 项冻结产物 sha256 完整性 | `out/.../10_sha256.txt` |
| S2 | 论文数字复算（复用 `docker/paper/run_all.sh`） | `out/.../20_run_all.log` |
| S3 | 门禁（论文门禁 + fast_gate） | `out/.../3*.txt` |
| S4 | 汇总验证报告 | `out/.../99_reproduce_report.md` |

693 执行环境实测：S0–S2 全过、论文门禁 PASS、fast_gate FAIL（三条失败均与 693 无关，
见 `data/693_docker_reproduce_report.md` §4）。

---

## 2. 实验清单

### E0 · 系统计数（最快判断环境对不对）

```bash
bash docker/paper/run_all.sh
# 期望：
#   OK  判决规则数 len(RULES) = 67
#   OK  权威账本事件数 = 452
#   OK  实卡数 atoms_real = 42
#   holdout  82.9% (34/41)
#   corpus   62.5% (40/64)
#   corpusC  52.6% (40/76)
#   layer sanitizer 85.3% / compiler-warn 50.0% / cross-compile 16.7%
```

### E1 · 冻结检测矩阵（1147 × 8）

- **产物**：`data/blindspot_676g_detection_matrix.json`
- **只读复算**：`python tools/recompute_a5_676f.py`（从原始矩阵独立重算 A5/盲区）
- **门禁**：`python tools/recompute_a5_676m.py --check`（修正标签后主端点须逐位一致）
- **环境**：WSL g++ 13.3（sanitizer 双档）+ MinGW g++ 13.1（warn/cross/linker）
- **关键数**：OR 口径 **61.6%**；盲区 **38.4%**；条件 recall **94.21%**

### E2 · 检测器深度 Benchmark（676l）

```bash
# 产物已落盘，读算即可
grep -n "recall" data/676l_单检测器性能报告.md
```

- 单资产 recall：asan **58.5%** > ubsan **38.2%** > tsan **36.1%** > compiler-warn **19.1%**
  > cross-compile **15.1%** > linker **1.3%**
- 八资产并集 **94.21%**；k=1…8 穷举最佳 k=4 = **92.58%**，拐点 k=5
- `linker` 的 10 个 catch **全部**落在 asan/ubsan/tsan 的 10 个 `unknown` 里
  ⇒ **低边际但不可替代**

### E3 · A5 主端点（组合算子 E 的选择效应）

- **产物**：`data/676f_A5重跑报告.md`
- **n = 566**（A5 evaluation split）
- 主分析（8 候选、k=4）：FD **54.59%** vs Random **30.57%** vs Static **24.74%**
  ⇒ Δ = **+24.03pp**，95% CI [+20.51, +27.55]，精确 McNemar **p=2.3×10⁻⁴¹**（b=136, c=0）
- ⚠ **并列分析 Δ = +0.00pp** —— 必须并报，**不宣称 FD 优于 Random**

### E4 · 敏感性分析（682）

```bash
python tools/analyze_682_sensitivity.py
```

- split 敏感性、5,000 次种子、255 个资产子集
- 产物：`data/682_a5_split_comparison.json`、`data/682_a5_seed_stability.json`、
  `data/682_asset_ablation.json`

### E5 · 真实世界靶场（683）

```bash
python tools/collect_realworld_683.py --stage verify   # NVD 在线验证（需网络）
python data/realworld_683_runner.py --stage detect     # 110 × 8（增量 checkpoint）
python data/realworld_683_runner.py --stage merge
python tools/analyze_683_realworld.py
```

- 110 条可追溯缺陷，**109/109** NVD FOUND
- ⚠ 靶场是**重构**，不等于原始项目上下文

### E6 · 公平外部对比（692-D）

```bash
python tools/run_692_fair_comparison.py
```

- clang-tidy **22.1.8** + cppcheck **2.21.0**，Windows native，4 个口径
- 协议**跑之前**落盘：`data/692_fair_comparison_protocol.md`
- 原始输出 1132 行：`data/692_fair_comparison_raw.jsonl`

### E7 · 环境感知配对实验（692-A）

```bash
python tools/analyze_692_environment.py
```

- E1 = WSL/g++13.3 六资产：**60.07%**（340/566）
- E2 = native MinGW 三资产 unaware：**24.74%**；aware：unknown 率 **75.27%**
- 配对 McNemar (b,c)=(200,0)，p=1.24×10⁻⁶⁰
- E1 的捕获有 **58.82%**（200/340）在 E2 **从未被测量**
- 能力撤退扫描 63 个非空子集，**62/63** 会产生不可信负例

### E8 · LLM 第四臂 audit transfer（692-C）

- N=80，2 个预算，2 个 prompt，480 次调用
- 产物：`data/692_llm_audit_results.json` / `raw.jsonl` / `report.md`
- ⚠ truth 参照是 `expected_verdict`（**声明可检出性**），**不是人审真值**

### E9 · AI 双标与人类裁决（693-A）

```bash
python tools/annotate_693_b.py --csv     # AI 双标 + 裁决表
python tools/compute_693_iaa.py          # 人类裁决回来后算 κ
```

- n=145；raw agreement **78.6%**；Cohen's κ = **0.495**；分歧 **31** 条
- 剔除 13 条泄漏样本后：raw **77.3%**，κ = **0.458**
- 分歧集中度：`language_oop` 家族 30.1%（22/73）；`other_ub` 单类 32.3%（21/65）

---

## 3. 环境矩阵（哪个实验需要什么）

| 实验 | WSL g++13.3 | MinGW g++13.1 | clang++ | 网络 | 耗时 |
|---|---|---|---|---|---|
| E0 系统计数 | — | — | — | — | 秒级 |
| E1 冻结矩阵（**再生产**） | ✅ | ✅ | ✅ | — | 数小时 |
| E2 深度 Benchmark（读算） | — | — | — | — | 秒级 |
| E3 A5（读算） | — | — | — | — | 秒级 |
| E4 敏感性 | — | — | — | — | 分钟 |
| E5 真实靶场 | ✅ | ✅ | ✅ | ✅（NVD） | 数十分钟 |
| E6 公平对比 | — | ✅ | ✅（clang-tidy） | — | 分钟 |
| E7 环境配对 | ✅ | ✅ | — | — | 数十分钟 |
| E8 LLM 臂 | — | — | — | ✅（API） | 分钟 |
| E9 AI 双标 | — | — | — | — | 秒级 |

---

## 4. 口径纪律

1. **分母写清**：61.6%（分母 1147）vs 94.21%（分母 674）是同一矩阵的两个合法读数。
2. **`unknown` 不折叠进 `miss`**。
3. **主分析与并列分析并报**（E3）。
4. **重构 ≠ 原始上下文**（E5）。
5. **任何"复现"都从 `data/` 读算**，不重写 `data/` 下已冻结的产物。

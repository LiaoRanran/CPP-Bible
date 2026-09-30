# 668 批次验收报告

> 目标：**修真实数字 → 按规划建设 → 排错 CI**。
> 执行时间：2026-09-30　｜　执行者：Agent（**有人工/人签项未完成**，见 §5）
> 纪律：所有数字脚本现算落盘；受控目录零改动**除本批授权的补卡**；做不完的诚实登记。

---

## 0. 一句话结论

- **P0 完成**：两个"改了代码没重跑"的假数字**全部修掉**，且发现真实值与两次声称值**都不同**：
  holdout 检出率 = **87.5%（14/16）**（666 声称 81.2%、665 产物 66.7%）；
  反事实 F1 = **1.0（分母 10 条）**（666 声称"20 条"，实际可打分只有 10 条）。
- **P0 防复发落地**：`--check` 射程补齐（三个率都比对）+ **射程自检**（改一个数必红）+ 纪律文档。
- **P1 部分完成**：规划 Q1 的"47 卡补边界"**前提被证伪**（缺边界的卡全是 `draft`，按规则不该补）；
  实卡 **37 → 42**（5 张机器实测卡），但**证据卡未配套** ⇒ 3 项 prop-graph 红（诚实登记）。
- **P2 部分完成**：evidence 写法修复（10 行 / 10 卡）并**暴露第二缺陷**（run 比对顺序敏感）；
  slow 6 红逐条归因，1 条修掉、3 条给出方案未做、2 条需人签。

---

## 1. P0-1 · holdout 检出率（真实值 87.5%）

| 项 | 值 |
|---|---|
| 声称（666） | 81.2%（13/16） |
| 产物（修前） | 66.7%（10/15），自述 **-O1 单档** |
| **重跑落盘（668）** | **87.5%（14/16）**：catch 14 / miss 2 / unknown 1 |
| 对照子集 | 9 条 / 误报 1 |
| 逐样本变化 | **4 条**：h1（tsan，`unknown→catch`）、h26/h27/h30（`miss→catch`） |

**产出**：`data/holdout_reveal_3_665.json`（含 `caliber` / `denominator` / `opt_levels` / `env` /
`per_sample_detail`）+ **`data/holdout/reveal_3_detail_668.json`**（30 条逐样本 + 运行环境 +
`changed_vs_previous_run`）。

**顺带修掉一个更隐蔽的问题**：h1 的 TSan 在 WSL **高熵 ASLR** 下**间歇性**无法初始化
（同一夹具时 `catch` 时 `unknown`）⇒ 这个数字本来**不可复现**。
`detect()` 改用 `setarch -R`（关 ASLR）后，**连跑 3 次结果逐样本一致**（`changed_vs_previous_run` 为空）。

**同步更新**：`research/paper_v0.4.md`（文首加 v0.4.1 修订表 + 全文数字）、`web/data/metrics_666.json`、
`web/data/verdicts_667.json`、`_auto/status.json`、`data/667_acceptance_report.md` 与
`docs/667_*.md` 的 668 修订行。

---

## 2. P0-2 · 反事实 F1（真实值 1.0，分母 10）

| 项 | 值 |
|---|---|
| 声称（666） | F1=1.0，**20 条** |
| 产物（修前） | F1=**0.0**，10 条（旧算子） |
| **重跑落盘（668）** | P=R=F1=**1.0**，混淆矩阵 tp2/fp0/tn8/fn0，**分母 10** |
| 第三判据命中 | **2 条**（cf14 / cf18，均为"平台测量"类） |

**"20 条"的真相**：本产物 10 条 + `counterfactual_cases_660.json` 的 10 条；
而 **660 的 10 条没有 `ground_truth` 标签**，进不了 P/R/F1。⇒ 产物新增 `denominator` 字段把这件事写死。
**F1=1.0 是上界**（判据 3 与真值标签同源），n=10 时 95% CI 约 ±30pp —— 两条都写进 `honest_note`。

---

## 3. P0-3 · 防复发

| 产出 | 说明 |
|---|---|
| `web_metrics_666 --check` 扩射程 | 增比 `holdout.{rate_pct,catch,miss,unknown,den}`、`external.{rate_pct,catch,miss,total,unknown}`、`counterfactual.{f1,cases}` |
| 射程自检（R4） | `tests/test_drift_guard_668.py`：**故意改一个数 ⇒ `--check` 必须 exit 1**（3 个率各一条）+ 未改则必须绿 |
| 口径来自产物 | `holdout.reveal_3` 新增 `caliber`/`denominator`/`opt_levels`/`env`；工具里**不再写死"双档"字样** |
| 纪律文档 | **`docs/discipline/改代码必重跑.md`**（含触发清单、三步规矩、已落地的护栏、例外） |
| 另一处自检路径的真 bug | `--check` 曾硬编码读落盘文件、无视 `OUT` ⇒ 该路径**从没被实测过**，已修 |

---

## 4. P1 · 按 667 规划建设

### 4.1 P1-1 卡边界（**规划前提被证伪**）

规划原文假设"47 卡 0 边界 ⇒ 四态全 unknown"。**实测不成立**：

| 事实（`semantic_scope_backfill_668.py --report`） | 值 |
|---|---|
| 有合法边界三元组的卡 | **26**（`verified` / `red-team-verified`）⇒ 四态 **pass** |
| 缺三元组的卡 | **26**（= 11 张 `draft` 实卡 + 10 张 draft650 + 5 张本批新卡） |
| 其中"在回填范围内却缺" | **0** |

⇒ 那 26 个 `unknown` **是 657 既定规则（"判决未定，不预先写边界"）的正确输出，不是缺陷**。
本批**没有**去"把 unknown 翻成 pass"（那会造出假边界）。产出：
`tools/semantic_scope_backfill_668.py` + `data/668_boundary_backfill.{md,json}`（逐卡 provenance /
semantic scope / evidence / 四态 + 理由），并与 `counts_659` 对账（42/10 一致）。

### 4.2 P1-2 断言拆卡（**部分完成**）

`tools/card_split_668.py` 把 665 的机器卡拆成 5 张原子卡（**实卡 37 → 42**）：

| 源 | 新卡 | 检测器 | 证据来源 |
|---|---|---|---|
| ig-01 | `ATOM-UB-WRAP-001` | ubsan | 真机夹具 + 实测输出（**读自 `index_665.json`，不手打**） |
| ig-02 | `ATOM-UB-OOB-001` | asan | 同上 |
| ig-07 | `ATOM-UB-NULLDEREF-001` | asan | 同上 |
| ig-08 | `ATOM-UB-DIVZERO-001` | ubsan | 同上 |
| ig-14 | `ATOM-MEM-NEWARR-001` | asan | 同上 |

**不代签**：全部 `status: machine-verified` + `human_review: required`，**无 `verified_by`**；
且**不预写边界三元组**（未跑变异 ⇒ 四态 `unknown`，规则正确输出）。测试锁死这三点。

**未完成（诚实登记）**：5 张卡**没有配套的证据卡** `evidence/**/EV-*.md` ⇒
`test_prop_graph` 的锚来源集合变成 `{evidence, none}`、命题总数 89 → 99。**3 项红，未修**（见 §5.2）。

### 4.3 P1-3 corpus 分母声明

`external_corpus_reveal_665.py` 产物新增 `denominator{value:32, meaning, excluded, all_samples:40}`
与 `rate_pct_all_samples:35.0`；`web_metrics_666` 同时给出两个分母。

---

## 5. P2 · CI / 门禁（详见 `docs/668_ci_triage.md`）

### 5.1 修掉的

4 项真修（含 2 处**假绿**：测试锁标签而非数据源、`--check` 无视 `OUT`）+ evidence 10 行写法修复。

### 5.2 **未修的红（不删、不掩盖）**

| 红 | 根因 | 为什么没修 | 修法与工作量 |
|---|---|---|---|
| `test_prop_graph::test_anchor_source_splits_card_vs_evidence` 等 3 条 | 5 张新卡无证据卡 | 需满足 `EV-FM-REQUIRED`/`EV-MATRIX`/`EV-ARTIFACT-PRODUCER`/`EV-FALSIFICATION` 等 block 规则 | 5 张证据卡 ≈ 半日 |
| `test_boundary_backfill_657::test_plan_scans_all_47_cards` | 断言**写死 47** | 属"去写死"类，应改 `counts_659.ATOMS_TOTAL` | 10 分钟 |
| `WinError 206`（3 条） | Windows 命令行长度上限 | 改动落在门禁核心，风险高于本批额度 | gate 改临时响应文件 |
| `golden_lock` / `debt_ledger`（2 条） | **唯人签** | 机器不代签 | 人 |
| `evidence run` 比对顺序敏感 | 运行器缺"按 `run_match_keys` 集合比对" | 同上门禁核心 | 人定 |
| **全量 fast 套件** | **收工时未跑完**（约 44%，`data/668_fast.txt`） | 时间 | 下一批续跑（**不假设绿**） |

---

## 6. 红线核对

| 红线 | 结果 |
|---|---|
| 受控目录零改动 | ⚠ **除本批明确授权的补卡**：新增 5 张 `atoms/**/*.md`、改 10 张 `evidence/**/*.md` 的**命令行写法**（`fixture`/`artifact_sha256`/`expected`/`actual` 一字未动）。**均已重钉 Merkle 并在报告中登记** |
| 452 账本 | ✅ 零改（只读计数） |
| 不代签 | ✅ 新卡 `machine-verified` 无 `verified_by`；未 `golden_lock --accept`；未解除 debt 停线 |
| 不擅自 push | ✅ 未 push（ahead 留给下一轮） |
| 所有数字脚本现算 | ✅ 全部产物由工具现算落盘；口径/分母写进产物 |
| 做不完的诚实登记 | ✅ 见 §5.2 |

**重钉记录（必须复核）**：因 P1-2 授权扩卡，`data/supply_chain/merkle_roots.json` 被**重建**
（atoms 49 → 54 文件）、`tools/.tool_checksums` 的 supply_chain 节被更新、
`data/baseline.json` 因卡数 48 → 53 做了一次 `--snapshot`。
**这三处都是"信任相关动作"，须人复核**；且 `merkle_roots.json` 的 **OTS 锚现已过期，待重打**。

---

## 7. 复算入口（本批新增/修改）

```powershell
.venv\Scripts\python.exe tools\holdout_reveal_3_665.py          # 重跑 reveal（双档 + 明细 + 环境）
.venv\Scripts\python.exe tools\counterfactual_extend_665.py     # 反事实重跑（分母 + 第三判据）
.venv\Scripts\python.exe tools\external_corpus_reveal_665.py    # 外部语料（分母声明）
.venv\Scripts\python.exe tools\web_metrics_666.py --check       # 三个率的漂移比对
.venv\Scripts\python.exe tools\semantic_scope_backfill_668.py --report
.venv\Scripts\python.exe tools\card_split_668.py --check
.venv\Scripts\python.exe tools\evidence_cmd_redirect_668.py --check
.venv\Scripts\python.exe tools\web_verdicts_667.py --check
.venv\Scripts\python.exe -m pytest tests\test_drift_guard_668.py tests\test_web_metrics_666.py tests\test_web_verdicts_667.py -q -n0
node tools\web_logic_check_667.mjs ; node tools\web_smoke_667.mjs
.venv\Scripts\python.exe tools\run_658_gate.py ; .venv\Scripts\python.exe tools\status_reconciler_658.py --check
```

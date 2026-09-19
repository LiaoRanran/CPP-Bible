# Metrics 指标详情台账（2026-09-19）

> 产品经理视角。27 项基础指标 + 5 项不变量 + 苦力 608 新增 5 类指标的完整分类、历史趋势和设计意图。
> 数据来源：tools/metrics_collector.py 实跑（27/27 项采集）+ data/metrics.jsonl（10 个时点）+ 苦力 608 metrics_608 扩展。

## 一、总览

| 类别 | 指标数 | 说明 |
|---|---|---|
| 基础指标 | 27 | gate/poison/replay/atoms/evidence/misconceptions/cost/git/debt |
| 不变量 | 5 | artifact_restore/build_reproducibility/sandbox_isolation/lock_consistency/manifest_consistency |
| 苦力 608 新增 | 5 类 | human_review/grounded/build_reproducibility/escape_rate_convergence/C-P 上界 |
| 曲线数据 | 3 条 | mutation_escape_rate/overturned_by_stronger_verifier/escape_survival_batches |
| 历史时点 | 10 | data/metrics.jsonl 共 10 行（2026-09-19 当天） |
| alerts | 0 | 当前无告警 |

## 二、27 项基础指标

### 2.1 制衡层（gate/poison/replay）

| 指标 | 当前值 | 说明 |
|---|---|---|
| gate_rule_count | 63 | 注册规则总数（block40/warn16/advice7） |
| gate_block_count | 0 | 当前卡集 block 命中数（硬阻断为 0 = 全库合规） |
| gate_warn_count | 186 | 当前卡集 warn 命中数（观察期，非阻断） |
| poison_total_count | 124 | 毒样例总数（P1-P83 含阴性对照） |
| poison_pass_count | 124 | 被 gate 拦截的毒样例数（100% 拦截） |
| poison_coverage_pct | 61.9% | 规则行为覆盖率（39/63，不含豁免） |
| replay_confirm_count | 56 | 编译通过+断言成立+工件还原的卡数 |
| replay_refute_count | 0 | 编译失败或断言不成立的卡数 |
| replay_infra_error_count | 0 | 基础设施错误（编译器缺失等） |

### 2.2 知识资产层（atoms/evidence/misconceptions）

| 指标 | 当前值 | 说明 |
|---|---|---|
| atoms_total | 27 | 原子卡总数（27 张，含 23 verified + 1 draft + 3 其他） |
| atoms_verified | 23 | 已 verified 的原子卡数（85.2%） |
| atoms_draft | 1 | draft 状态的原子卡数 |
| evidence_total | 56 | 证据卡总数（83 张卡中 56 张已 replay confirm） |
| evidence_confirm | 56 | replay confirm 的证据卡数（100%） |
| misconceptions_total | 79 | MIS 误解库总数（42 带 related_atoms，37 不带） |
| asm_files_count | 404 | Examples/ 下的 .asm 工件文件数 |

### 2.3 性能与成本

| 指标 | 当前值 | 说明 |
|---|---|---|
| pytest_wall_seconds | 180.5 | pytest 墙钟（fast+slow，来源 data/pytest_last.txt） |
| replay_wall_seconds | 0.28 | replay 墙钟（增量全命中缓存，未跑编译） |
| gate_wall_seconds | 4.53 | gate 墙钟 |
| ci_total_seconds | 4.81 | CI 估算总时长（replay+gate，不含 pytest/poison/编译） |
| cost_tracker_total_tokens | 155,655 | 累计 token 消耗（成本追踪） |
| cost_tracker_atoms_per_batch | 27 | 每批原子卡数 |
| cost_tracker_avg_per_atom | 5,765 | 每原子卡平均 token 消耗 |

### 2.4 仓库与债务

| 指标 | 当前值 | 说明 |
|---|---|---|
| git_ahead_count | 78 | 本地领先远程的 commit 数（未 push） |
| git_untracked_count | 0 | 未跟踪文件数（_arch_v*/_auto/ 按惯例不跟踪） |
| debt_ledger_open_count | 0 | 开放债务条目数（债务台账已清零） |
| golden_state_atoms_match | True | golden state 与原子卡一致 |

## 三、5 项不变量（invariants）

| 不变量 | 状态 | 说明 |
|---|---|---|
| artifact_restore | ✅ True | 工件还原不变量（Examples/ 指纹稳定，哨兵字节区分真还原） |
| build_reproducibility | ✅ True | 编译可复现不变量（10/10 卡 reproducible，跨时间窗口 5/5） |
| sandbox_isolation | ✅ True | 沙箱隔离不变量（临时目录不污染真实仓库，clean_before/after=True） |
| lock_consistency | ✅ True | 锁一致性不变量（default path correct + batch_root follows + no stale lock） |
| manifest_consistency | ✅ True | manifest 一致性不变量（56 卡 checked，0 fingerprint mismatches，0 invalid verdicts） |

**invariants_all_pass: True** — 5/5 不变量全过。

## 四、苦力 608 新增 5 类指标（metrics_608）

### 4.1 human_review（人审进度）

| 指标 | 当前值 | 说明 |
|---|---|---|
| total | 388 | 候选攻击边总数（194 MIS→命题 + 194 对称边） |
| pending | 388 | 待审边数（0/388 已审） |
| approved | 0 | 已确认边数 |
| rejected | 0 | 已拒绝边数 |
| modified | 0 | 已改权边数 |
| annotated_edges | 0 | 已标注边数 |
| candidate_edges_by_mis | 42 | MIS 群组数（388 边聚成 42 组，降 4.6 倍工作量） |

### 4.2 grounded（论证层状态）

| 指标 | 当前值 | 说明 |
|---|---|---|
| in | 79 | 命题全 IN（W2 可信度加权击败 + 对称边） |
| out | 42 | 误解全 OUT（42 个带 related_atoms 的 MIS） |
| undec | 0 | 无不确定（非退化且语义正确） |
| candidate_edges_total | 388 | 候选攻击边总数 |
| candidate_edges_by_mis | 42 | MIS 群组数 |

### 4.3 build_reproducibility（编译可复现深化）

| 指标 | 当前值 | 说明 |
|---|---|---|
| reproducible | True | 可复现（2 张卡抽样） |
| time_macro_drift | 0 | 时间宏漂移（__TIME__/__DATE__ 不导致漂移） |
| symtab_consistent | True | 符号表一致（nm 比对） |
| n_cards | 2 | 抽样卡数（EV-CONC-001/002） |

### 4.4 escape_rate_convergence（逃逸率收敛曲线 v1-v7）

| 版本 | judged | n_a | numerator | denominator | point | C-P95 下界 | C-P95 上界 | 说明 |
|---|---|---|---|---|---|---|---|---|
| v1 | 956 | 232 | 227 | 956 | 23.74% | 21.08% | 26.57% | 571 修 GATE_READ_KEYS 前，含 M2 假逃逸（口径修正） |
| v2 | 969 | 212 | 61 | 969 | 6.30% | 4.85% | 8.01% | 571 修尺子后，含 M3 的 52 条真洞（口径修正） |
| v3 | 997 | 186 | 38 | 997 | 3.81% | 2.71% | 5.19% | 574 修 M5 尺子后，M5 活雷未收（口径修正） |
| v4 | 998 | 185 | 38 | 998 | 3.81% | 2.71% | 5.19% | 575 命题级活性锚，M5 规则已拦但被 diff 键吞（口径修正） |
| v5 | 1375 | 185 | 1 | 1375 | 0.073% | 0.0018% | 0.40% | 578 _findings_key 并入文案后，587 起 1/1375（口径修正） |
| v6 | 1379 | 179 | 1 | 1379 | 0.073% | 0.0018% | 0.40% | 588 发现器补全后 1/1379，被 v7 取代（口径修正） |
| v7 | 1406 | 179 | 1 | 1406 | 0.071% | 0.0018% | 0.40% | 591 当前口径：589 T2 注释净化 un-mask 27 条（真实进展） |

**诚实声明**：v1→v5 为口径修正（非同一量时间序列），v6→v7 为真实进展；不得声称单调收敛（仅 1 含曲线时点）。

### 4.5 Clopper-Pearson 上界（C-P95）

| 指标 | 当前值 | 说明 |
|---|---|---|
| v7 point | 0.071% (1/1406) | 实测逃逸率 |
| v7 C-P95 下界 | 0.0018% | Clopper-Pearson 95% 下界 |
| v7 C-P95 上界 | 0.40% | Clopper-Pearson 95% 上界 |
| point_raw | 0.0007112375533428165 | 全精度点估计 |
| cp_low_raw | 1.8006813682120512e-05 | 全精度下界 |
| cp_high_raw | 0.003956325504751501 | 全精度上界 |

**外部独立验证**：scipy 精确计算 Clopper-Pearson，两侧 95% CI = [0.0018%, 0.3956%]，与 metrics 完全对上。

## 五、曲线数据（curves）

### 5.1 mutation_escape_rate（当前逃逸率）

- source: data/mutation/full_baseline_v7.json
- baseline_version: v7
- frozen_at_commit: d36d5c8
- judged: 1406
- n_a: 179
- numerator: 1
- denominator: 1406
- point: 0.071%
- C-P95: [0.0018%, 0.40%]

### 5.2 overturned_by_stronger_verifier（推翻事件）

- overturned_by_stronger_verifier: 0
- overturned_recent: []
- overturned_channel_initialized: True
- overturned_note: 事件流 data/overturned_events.jsonl（只追加）。系统绝不自动产生推翻——写入只能来自人或异族的显式动作，且 human 推翻者须过 git 作者绑定（fail-closed）

### 5.3 escape_survival_batches（逃逸存活批次）

| 算子 | 批次 | 逃逸数 | 产生于 | 收口于 | 说明 |
|---|---|---|---|---|---|
| M3 | 1 | 52 | 571 | 572 | 571 v2 浮出 52 条 → 572 全部收口 ⇒ survival = 1 批 |
| M5 | 1 | 29 | 574 | 575 | 574 v3 浮出 29 条 M5 活雷 → 575 命题级活性锚规则已拦（1 批）；但 v4/v5 台账里该批差异曾被 _findings_key 吞掉，度量可见的收口落在 578（v5）——两个批次都记 |
| M2 | 0 | 0 | — | — | 571 已证实 v1 的 207 条是 GATE_READ_KEYS 尺子 bug 的假逃逸（修后 0）⇒ 不计入 survival |
| M6 | 0 | 0 | — | — | 8 条 matrix 块式→flow 等价变异体（583 已定性，非真逃逸）⇒ 不计入 survival |

**诚实声明**：其余算子尚无"产生→收口"的完整批次 ⇒ None（不填 0）；M2/M6 的 0 是"真值 = 非逃逸"、与 None（缺数据）含义相反，别混读。

## 六、设计意图分析

### 1. 27 项基础指标是"项目健康度仪表盘"
27 项指标覆盖制衡层（gate/poison/replay）、知识资产层（atoms/evidence/misconceptions）、性能与成本（pytest/replay/gate/cost）、仓库与债务（git/debt/golden）四个维度。这不是"为了度量而度量"，而是"项目健康度的实时仪表盘"——任何一项异常都能立即发现。

### 2. 5 项不变量是"不退化的硬保证"
5 项不变量（artifact_restore/build_reproducibility/sandbox_isolation/lock_consistency/manifest_consistency）是"不退化的硬保证"——每次 metrics 采集都验证这 5 项不变量，任何一项失败都会触发 alerts。这是"度量诚实化"的体现——不满足于"看起来没退化"，而是证明"确实没退化"。

### 3. 逃逸率收敛曲线 v1-v7 是"尺子变更史"的诚实声明
v1→v5 是口径修正（23.7%→0.073% 主要是尺子变更），不是同一量的时间序列。metrics 明确标注每个版本的 note，说明"这是口径修正，不是真实进展"。只有 v6→v7 是真实进展（M2 un-mask +27）。这是"度量诚实化"的核心——不急于宣称"逃逸率在降"，而是如实声明"哪些是尺子变更、哪些是真实进展"。

### 4. Clopper-Pearson 上界是"错误率有上界"的工程实现
1/1406 的逃逸率不是"宣称零逃逸"，而是"实测 1 逃逸 + C-P95 上界 0.40%"。这是 PAC（Probably Approximately Correct）式保证——不追求零错误，而是给错误率一个统计上界。外部独立验证（scipy 精确计算）对上，证明不是统计黑话。

### 5. escape_survival_batches 是"逃逸→收口"的可追溯记录
M3（52 逃逸/1 批收口）、M5（29 逃逸/1 批收口，度量可见 3 批）是"逃逸→收口"的可追溯记录。这不是"宣称零逃逸"，而是"记录每一次逃逸的产生和收口"。M2/M6 的 0 是"真值 = 非逃逸"，与 None（缺数据）含义相反，别混读。

---

*数据源：tools/metrics_collector.py 实跑（27/27 项采集，2026-09-19T22:04:51）/ data/metrics.jsonl（10 时点）/ 苦力 608 metrics_608 扩展（5 类新指标）/ scipy 独立验证 Clopper-Pearson*

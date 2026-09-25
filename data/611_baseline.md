# 611 开工基线（任务0 · 只读采集，不写代码）

> 采集时间：2026-09-20 · HEAD `e5baf86`（610 监工 chore：governance 台账登记 610.md）
> 工作树：仅并行会话的 `References/00_导航/*.md` 变动（与 611 无关，不碰）
> 采集方式：`_auto/_b611.py`（只读探针，**未落库**）；所有数字可用同命令复算。

## 1. W2 判决三口径（同一 388 条候选边 / 388 条人审）

| 口径 | IN | OUT | UNDEC | 击败边 | 轮数 | 说明 |
|---|---|---|---|---|---|---|
| 无人审（`--no-human-reviewed`） | 79 | 42 | 0 | 194 | 3 | 594/596 冻结口径 |
| **keep-low**（入库权威：modify 不动档） | **114** | **7** | 0 | **17** | 3 | **与 `data/grounded_labels_w2.json` 逐项一致** ✓ |
| upgrade-medium（609 A3：modify 用 `new_confidence`） | 121 | 0 | 0 | 0 | 2 | 「全 IN ⇒ 攻击性被抽空」 |

- 权威产物 `data/grounded_labels_w2.json`：`summary={IN 114, OUT 7, UNDEC 0, nodes 121, IN_props 79, IN_mis 35}` ·
  `defeating_edges=17` · `edges=388` · `rounds=3` ⇒ **≡ keep-low 口径**。
- 两口径的**唯一差异来源**：34 条 `modify`（其余 354 条 approve 两口径同处理）。
- ⚠️ **现状**：`weighted_af_solver.reviewed_edges` 现行实现是 **upgrade-medium**（读 `new_confidence`），
  即「默认跑出来的不是入库权威口径」⇒ 611 B1 把默认改成 `keep-low` 并保留 `--modify-mode` 开关（口径不擅自统一）。

## 2. 论证漏洞检测（`tools/argument_audit.py summary`，exit 0）

- **P0 2 条**：`no_high_credibility=true`（可信度 high 档节点 0 个）· `no_attacker_propositions=4`
- **P1 4 条**：`no_defender_out_mis=1`（`MIS-LANG-001`）· `high_modify_mis=7`（modify 比例 1.0 的 MIS）·
  `topic_imbalanced=true`（MEM 312/388 = 80.41%）· **`components=11`**
- **P2 3 条**：`top_prop_overload=10`（`ATOM-UB-GRAY-001::prop-1` 10 个攻击者）· `top_mis_overload=12`（`MIS-MEM-031`）· `cycles=194`
- `totals={p0 2, p1 4, p2 3, defeating_edges 17}`

## 3. 辩护链（`tools/defense_chain.py stats`，exit 0）

- 节点 **121**（IN 114 / OUT 7 / UNDEC 0）· 命题 79（IN 79）· 误解 42（IN 35）
- 边 388 · **击败边 17** · 3 轮收敛 · `no_defenders=7` · `no_attackers=4`
- **OUT 的 7 个 MIS**：`MIS-LANG-001` · `MIS-MEM-001` · `MIS-MEM-003` · `MIS-UB-001` · `MIS-UB-004` · `MIS-UB-008` · `MIS-UB-014`
- 无辩护者节点 7：`ATOM-CONC-FENCE-001::prop-1/2` · `ATOM-CONC-LOCK-001::prop-1/2` · `MIS-CONC-003` · `MIS-LANG-001` · `MIS-MEM-015`

## 4. 人审 schema 现状（`data/human_attack_edge_annotations.jsonl`）

- **388 行**，字段计数：`edge_id 388` · `action 388` · `reason 388` · `reviewer 388` · `timestamp 388` · `new_confidence 34`
- **`review_seconds` 出现 0 次** ⇒ 耗时不可回溯（610 交人项 ⑤ 成立）
- kind 分布：approve **354** / reject **0** / modify **34**；reviewer 单一：`LiaoRanran`

## 5. append-only 校验现状（610 交人项 ④）

- ⚠️ **`tools/verify_append_only.py` 不存在**；实现在 **`tools/supply_chain_verify.py:123`**
  `def verify_append_only(old_text, new_text) -> tuple[bool, str]`
- 实现 = `splitlines(keepends=True)` 后**逐行**逐字节比对 + 行数不得减少
- **实测缺口**：末行**无换行**的文件（如 `data/supply_chain/merkle_roots.json` 末行无 `\n`）无法"行级追加" ——
  往末尾追加内容会被判成"第 N 行被改写"（假红）⇒ 611 A1 加**字节前缀快路径**。

## 6. 活性锚（`tools/proposition_liveness_audit.py --json`，exit 0）

- 命题 79：**observation 50** / inference 29 / other 0
- `liveness.with=0` · `without=79` · `observation_status.missing=50`（**50 条 observation 全缺活性锚**，与任务书一致）
- `missing_cards=27`（27 张原子命题卡）

## 7. oracle 验证

- **卡片总数 83 = 56 张证据卡（`evidence/**/EV-*.md`）+ 27 张原子卡（`atoms/**/ATOM-*.md`）**
  （任务书写"83 张证据卡"；**证据卡本身是 56 张**，83 是"证据卡+原子卡"的合口径 —— 已核实两者相加恰为 83）
- `verified_by_oracle` 非空卡数 = **0** ⇒ 与任务书"0 张填 verified_by_oracle"一致
- 既有工具：`tools/oracle_rotation.py`（含 `CHECKLIST`/`REGISTRY`/`build_report`）可复用

## 8. metrics 基线与键集（`tools/metrics_collector.py --json --no-heavy`，exit 0）

- 顶层：`alerts / curves / invariants / metrics / metrics_608 / metrics_610 / notes`
- **扁平 `metrics` = 27 项**（611 一字不动）：
  `asm_files_count, atoms_draft, atoms_total, atoms_verified, ci_total_seconds,
  cost_tracker_atoms_per_batch, cost_tracker_avg_per_atom, cost_tracker_total_tokens,
  debt_ledger_open_count, evidence_confirm, evidence_total, gate_block_count, gate_rule_count,
  gate_wall_seconds, gate_warn_count, git_ahead_count, git_untracked_count,
  golden_state_atoms_match, misconceptions_total, poison_coverage_pct, poison_pass_count,
  poison_total_count, pytest_wall_seconds, replay_confirm_count, replay_infra_error_count,
  replay_refute_count, replay_wall_seconds`
- `metrics_608` = 4 键（`escape_rate_convergence / escape_rate_note / grounded / human_review`）
- `metrics_610` = 3 键（`defense_chain_stats / grounded_status / human_review_progress`）

## 9. 口径偏差清单（任务书 → 实测 → 处置）

| # | 任务书假设 | 实测 | 处置 |
|---|---|---|---|
| 1 | `tools/verify_append_only.py` 存在 | **不存在**；实现在 `supply_chain_verify.py:123` | A1 改 `supply_chain_verify.verify_append_only`（真正被 governance/chain 调用的那支），并加测试 |
| 2 | 「83 张证据卡」 | 证据卡 **56**；83 = 56 证据卡 + 27 原子卡 | D3 显式写分母常量 `83（56+27）` 并同时给两者的分列计数 |
| 3 | 收工门禁第 391-404 行要求跑 `tool_integrity --check` / `gate --check` / `poison` / `replay --check` | 同文件第 428 行 + 第 445 行**明令禁止**（"这些是监工的事"） | 按**禁止**执行（后者更具体且在硬边界重复）；本处矛盾登记，见报告偏差表 |
| 4 | A2「读 `human_review_confirm.py` / `attack_edge_review.py`」 | `human_review_confirm.py` 是**并行会话的未跟踪文件**（非本仓入库工具）；本批自有工具是 609 的 `human_review_cli.py` | A2 扩展 `human_review_cli.py`（写侧）+ 兼容 596 `attack_edge_review.py` 写法 |
| 5 | B1「默认 keep-low」 | 现 `reviewed_edges` 实现 = upgrade-medium（609 A3） | B1 改默认 = keep-low + `--modify-mode`；**须同步修 609 既有测试**（若其断言默认口径），口径本身不裁决 |
| 6 | 任务 0.2「跑 `argument_audit.py --check`」 | `argument_audit.py --check` 存在且为**自洽校验**（非漏洞统计）；漏洞统计走 `summary`/`report` | 用 `summary` 采漏洞数字；`--check` 另跑（exit 0） |

## 10. 复算命令

```powershell
.\.venv\Scripts\python.exe tools/weighted_af_solver.py stats --json               # upgrade-medium（现状默认）
.\.venv\Scripts\python.exe tools/weighted_af_solver.py stats --no-human-reviewed --json
.\.venv\Scripts\python.exe tools/argument_audit.py summary
.\.venv\Scripts\python.exe tools/defense_chain.py stats
.\.venv\Scripts\python.exe tools/proposition_liveness_audit.py --json
.\.venv\Scripts\python.exe tools/metrics_collector.py --json --no-heavy
```


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `standard_textbook`
- `materiality_flag`: true

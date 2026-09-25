# 614 开工基线台账（任务0 · 只读测量）

> 测量时间：2026-09-21（本地，Windows PowerShell）
> 铁律边界：614 §五 禁止苦力跑 `gate --check / poison / replay --check / tool_integrity --check`
> 四类监工门禁。故下列「监工门禁基线」取自 **standing baseline**（612/613 收工时实测 + MEMORY），
> 本次**未重跑**；其余测量均为本次实跑。

## 1. git 状态
```
$ git log --oneline -5
6861a7f F3: 收工门禁 + 验收报告（613 自身结论 PASS）
3ac90d1 fix(A3): 适配 golden 锁已采纳 OBSERVATION-LIVENESS=legacy（基线 136→186）
cdd3b2d fix: golden_lock check 加 --no-replay（CI 跨平台 .exe 差异致 infra_error 误报）
f2c3b33 fix: test_cli_check_has_5_results 加 --no-heavy（CI 无编译环境）
d1508d6 fix: golden_lock 接受 OBSERVATION-LIVENESS 50 条 warn 为 legacy + run_613_gate 拆分 + 仓库盘点报告

$ git status --short   # 均为 613 遗留，非 614 引入
 M _adv_v80/probes/p57.cpp          # CRLF 假脏（铁律：勿提交）
 M data/metrics_612.md              # 时间戳再生（非 614）
?? _arch_v19/                       # 最新异族调研（614 G1 保留）
?? _arch_v19_brief.md
HEAD = 6861a7f
```

## 2. 监工门禁基线（standing，未重跑）
| 项 | 数值 | 来源 |
|---|---|---|
| gate_engine 规则/命中 | 63 / 191（block=0 warn=186 advice=5） | standing baseline |
| atom_evidence_replay confirm/refute/infra_error | 56 / 0 / 0 | standing baseline |
| poison_drill 124/124 · RULE-COVERAGE 63/63 · 表观/诚实 | 100% / 95.2% | standing baseline |
| tool_integrity 核心工具 | 5 核心 + 2 测试配置 + Merkle 目录级 | standing baseline |

> 注：若本次 614 改动触碰 CORE_TOOLS，须 `tool_integrity.py --update` 重钉（A2/G3 涉及）。

## 3. 文件计数（实跑）
| 类别 | 数量 | 命令 |
|---|---|---|
| tools/*.py | 196 | `(Get-ChildItem tools\*.py).Count` |
| tests/test_*.py | 174 | `(Get-ChildItem tests\test_*.py).Count` |
| atoms/ 文件（**无 ATOM- 前缀**） | 29 | 递归计数 |
| evidence/ 文件（**无 EV- 前缀**） | 57 | 递归计数（含 README） |

## 4. 学习者镜像现状
- `data/learner_state.jsonl`：**MISSING**（0 条记录）→ 线B 闭环验证从空白起步，B1 须先建采集+初始态。
- 既有工具：`learner_state.py`（init 27×0.1）、`bkt_solver.py`、`learner_behavior_ingest` / `learner_mastery_update_613` / `learner_path_graph_613` / `learner_twin_dashboard_613`（613 已建，但无真实输入）。

## 5. 攻击边标注
- `data/human_attack_edge_annotations.jsonl`：388 条（符合预期）。

## 6. 信任根现状（实地）
- `data/supply_chain/merkle_roots.json`：存在（Merkle 根台账）。
- `data/supply_chain/merkle_roots.json.ots`：存在 → **OTS pending**（未真实上链）。
- `data/supply_chain/link_613_verify.json`：存在 → in-toto link（HMAC 元数据，非真签名）。

## 7. CI 状态
- **无 gh / 网络通道**，无法用 GitHub API 取 #624 日志。
- 取自任务书：CI #581 起持续红；#624 gate job 失败（annotations 仅 "Process completed with exit code 1"，无详情）。
- 已知修复：`cdd3b2d` golden_lock 加 `--no-replay` + ci.yml 用 `--no-replay`；`f2c3b33` test 加 `--no-heavy`。
- A1 将在本地用 `golden_lock.py check --no-replay` 复跑确认，并排查 debt_ledger / poison 的 CI 风险（读码，不跑 poison 监工）。

## 8. 614 新工具预览（均不存在，待建）
learner_behavior_logger / learner_twin_dashboard_614 / learner_ood_evaluator /
learner_argument_link / trust_root_status_check / oracle_priority_614 /
oracle_verification_614 / run_614_gate（共 8 个）。


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `standard_textbook`
- `materiality_flag`: true

# 658 E1 · 口径收敛

> 目标：文档/README/baseline.json 数字对齐；差异登记并由 status_reconciler（D 段）对账。

## 已对齐（verified，入 baseline.json）

| 项 | 值 | 来源 |
|---|---|---|
| HEAD | eb700aec（657 收工，未含 658 提交） | `git rev-parse` |
| cards(atoms) | 48 | glob atoms |
| mutation | core 97.3% / all 81.5% | data/656_mutation_report_* |
| graph | 178 节点 / 1093 边 | web/data/graph.json |
| boundary | 26 卡有边界（23 verified + 3 red-team） | data/657_boundary_backfill.json |

status_reconciler_658.py 已對这五项与 git/fs 实际值对账（HEAD 漂移会在每次提交后刷新 baseline）。

## 待权威源确认的口径差（reconciler 容忍，不判冲突）

### 规则数：67 vs 63
- brief 说 67；658 任务书称"实际 `_gate_rules.json` 是 63"。
- 实测：仓库根**无 `tools/_gate_rules.json`**；`gate_engine.py` 也**未找到 RULES 注册表**（docs 描述其为"67 条规则引擎"，如 docs/core_rust_boundary_656.md、docs/c_domain_adaptation_647.md）。
- 处置：以 docs 既有口径"67 条规则引擎"为文档口径；`63` 的权威源（是否某个 JSON 注册表改名/迁移）**交人定位**。reconciler 对 rules 键容忍。

### 节点数：178 vs 121
- README 写"178 节点"，且 graph.json 实测 178（含 attack 388 / defend 616 等边类型计数）。
- 658 任务书称"权威源是 121"。
- 处置：以 graph.json 实测 178 为准（可复算、机器生成）；"121" 的权威源（可能指 121 张**知识卡**或去重后的知识节点）**交人确认**。reconciler 对 graph_nodes 以 graph.json 为准，121 不覆盖。

## 不变式
- 任何"文档数字"若能被 git/fs 机器复算，必须进 baseline.json 并由 reconciler 对账；
- 不能机器复算的（规则 67/63、节点 121）必须显式登记为口径差，禁止假装对齐。

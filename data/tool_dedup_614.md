# 614 G3 · 重复工具与测试合并评估

> 评估原则：**真重复才合并；不确定则只标注、交人裁决**（任务 G3 安全条款）。
> 铁律：不改 CORE_TOOLS；合并若触校验和须 `tool_integrity --update`。时间 2026-09-21。

## 一、盘点（tools/ 家族）
| 家族 | 成员 | 关系判定 |
|---|---|---|
| 门禁脚本 | `run_611_gate` `run_612_gate` `run_613_gate` `run_614_gate` | **有意按批次版本化**（各批收工门禁=该批冻结证据） |
| metrics | `metrics_610/611/612/613` + `metrics_collector`(L1 采集) + `metrics_honesty`(统计) + `metrics_snapshot`(事实) | **有意按批次**（610-613 各批度量）+ 3 个职责不同的核心 |
| 学习者 | `learner_state`(基础) `learner_behavior_ingest`(613) `learner_behavior_logger`(614) `learner_mastery_update_613` `learner_path_graph_613` `learner_twin_dashboard`(612) `_613` `_614` `learner_recommender` `learner_argument_link`(614) `learner_ood_evaluator`(614) | 混合：见二 |
| oracle | `oracle_priority`(612 基座) `oracle_priority_614`(**import 基座叠加**) `oracle_rotation` `oracle_verifier`(612 跑三门禁) `oracle_verification_plan`(611) `oracle_verification_614`(614 机制) | **叠加/分工**，非重复 |
| 逃逸率 | `escape_rate_honest_613` `escape_rate_trend` | 分工（单批诚实化 vs 趋势） |

## 二、重点检查（任务点名）
### 2.1 仪表盘 3 版（`learner_twin_dashboard` / `_613` / `_614`）
- 各有**独立测试**：`test_learner_twin_dashboard_612/613/614.py`；各产**独立 HTML**（`_612/_613/_614.html`）。
- `_614` 为真实数据版（读 B1 行为日志 + BKT 递推），`_612` 用 `learner_state.simulate` 模拟，`_613` 中间版。
- **判定：有意版本化，不合并**（合并会破坏三批回归与冻结产物）。

### 2.2 门禁脚本 4 版（`run_61x_gate`）
- 每版绑定**该批**工具清单/结论项（如 614 按 §五 不跑监工四类）。**判定：不合并**。

### 2.3 metrics 4 版（`metrics_610..613`）
- 各批**只读指标**，由 `metrics_collector` 统一挂载。**判定：不合并**（保留逐批可追溯）。

### 2.4 行为采集 2 版（`learner_behavior_ingest`(613) vs `learner_behavior_logger`(614)）
- **功能重叠**：均做行为采集→BKT。613 版被 `learner_mastery_update_613` + `test_learner_behavior_ingest_613` 使用；
  614 版 CLI 更全（log/import/stats/replay/recommend/simulate/--check），存于独立 `data/learner_behaviors.jsonl`。
- **判定：功能重叠，本批标注不合并**（合并会牵动 613 管线与其回归）⇒ **交人裁决**后续合并方向。

### 2.5 oracle 优先级 2 版（`oracle_priority` vs `_614`）
- `_614` **import 基座**并叠加 614 维度（known_tce×5 + kc_related×1）⇒ **非复制、属叠加**。**判定：保留（正确分层）**。

## 三、测试重复
- 逐批测试（`test_*_611/612/613/614`）**有意并存**：各自锁该批不变量。
- 未发现"同文件同断言"的真重复（如 `test_oracle_priority_612` 与 `_614` 断言维度不同）。

## 四、结论与动作
- **本批未执行任何合并**：经查不存在**可安全合并的真重复**——名为"重名"者均为**按批次版本化**（各有独立测试/产物）
  或**叠加复用**（import 基座 + 独立模块，未复制逻辑）。
- 唯一**功能重叠**为行为采集 2 版（2.4），已**标注交人裁决**。
- 依据：`git grep` 显示各版本工具分别被**不同批次测试**引用；合并将破坏逐批回归与冻结证据（违"一任务一commit/逐批可追溯"纪律）。
- 附：工具总览见 `data/repository_inventory_20260921.md`。

> 若人裁决需合并：建议方向 = 保留最新实现为 CLI，旧版降为 **shim**（import 新版并 deprecation 警告），
> 同 commit 跑 `tool_integrity --update`（若非 CORE 则免）+ 全量 pytest 复核。

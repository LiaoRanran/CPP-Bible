# 615 E1 · 重复工具合并决策（**仅决策，不执行合并**）

> 依据 614 G3 结论 + 本轮工具族扫描。铁律：**只做决策，不删除/不移动/不合并任何文件**（616 执行，需人审）。
> 说明：任务书提到"25 个可合并工具"，但 `_arch_v19` 未给出该清单；本报告以**真实工具族**（约 25 个工具）为准。

## 一、决策表

| 族 | 工具 | 决策 | 理由 |
|---|---|---|---|
| 门禁脚本 | `run_611_gate` `run_612_gate` `run_613_gate` `run_614_gate` | **不合并** | 各有独立工具清单/结论项与冻结证据；合并破坏逐批可追溯 |
| metrics | `metrics_610` `metrics_611` `metrics_612` `metrics_613` | **不合并** | 各批只读指标，由 `metrics_collector` 统一挂载 |
| 仪表盘 | `learner_twin_dashboard` `_613` `_614` | **不合并** | 各有独立测试与归档产物（612/613/614.html） |
| 行为采集 | `learner_behavior_ingest`(613) `learner_behavior_logger`(614) | **标注（交人）** | 功能重叠；合并牵动 613 管线与回归，须人定方向 |
| 逃逸率 | `escape_rate_honest_613` `escape_rate_trend` | **不合并** | 分工（单批诚实化 vs 跨基线趋势） |
| oracle 优先级 | `oracle_priority`(612) `oracle_priority_614` | **不合并** | 614 **import 基座叠加**（非复制），属正确分层 |
| oracle 验证 | `oracle_verifier`(612) `oracle_verification_614`(614) | **不合并** | 分工：612 跑门禁验证 / 614 机制与记录 |
| D5 门 | `d5_compile_gate` `d5_runtime_gate` `d5_source_integrity` | **不合并** | 三类判据（编译/运行/源完整性）语义不同 |
| 学习路径 | `learner_path_graph_613` `learner_recommender` | **标注（交人）** | 均给推荐，接口/口径待人裁决是否统一 |
| 命题图 | `prop_graph` `prop_closure` `prop_network_inventory` `prop_asof` | **不合并** | 各自职责（建库/闭包/盘点/时点） |
| 信任根 | `supply_chain` `supply_chain_verify` `merkle_integrity` `ots_anchor_613` `in_toto_link` | **不合并** | 各守一环（构建/验证/Merkle/OTS/in-toto） |
| 论证 | `defense_chain` `defense_chain_deepen` `defense_chain_deep_613` | **标注（交人）** | `defense_chain` 与 `defense_chain_deepen` 疑为同族两代；`deep_613` 为 613 版 |

**统计**：不合并 **9** 族 / 标注交人 **3** 族 / 合并 **0** 族。

## 二、为何"0 合并"
- 614 G3 已查明：所谓"重名"工具均为**按批次版本化**（各带独立测试与产物）或**叠加复用**（import 基座 + 独立模块）。
- 合并会：(a) 破坏逐批回归锁；(b) 破坏冻结证据可比性；(c) 引入 CORE/checksum 变动风险。
- ⇒ 除 **标注交人** 的 3 族（行为采集/学习路径/论证链）外，**无可安全合并项**。

## 三、交人裁决项（3 族）
1. **行为采集**（613 ingest vs 614 logger）：建议保留 614 为 CLI，613 降为 shim（下批执行，须人审）。
2. **学习路径**（path_graph_613 vs recommender）：接口与口径是否统一。
3. **论证链**（defense_chain vs deepen / deep_613）：是否保留两代。

## 四、边界
- 本报告**仅决策，未执行任何合并/删除/移动**；执行须 616 经**人审授权**。
- 不修改任何工具文件；未改受控目录。

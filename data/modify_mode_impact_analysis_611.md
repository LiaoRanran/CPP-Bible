# 611 B2 · modify 口径影响分析（keep-low vs upgrade-medium）

> 背景（610 交人项 ①）：34 条 `modify` 人审的 `new_confidence` **全是 medium**。两种口径对这 34 条的处置不同 ⇒ 判决不同。**本报告只量化差异、给优缺点与建议，不替谁裁决**（口径裁决是监工/人的事，见 §四）。

## 一、两档判决对比（现算，可复算）

| 口径 | IN | OUT | UNDEC | 击败边 | 轮次 |
|---|---:|---:|---:|---:|---:|
| `keep-low`（入库权威 / 611 B1 默认） | 79 | 42 | 0 | 194 | 3 |
| `upgrade-medium`（609 A3） | 79 | 42 | 0 | 194 | 3 |

> **差异**：IN 差 **0** 个（79→79）、OUT 差 **0** 个（42→42）、击败边差 **0** 条（194→194）。

## 二、34 条 modify 边的分布

- 总数：**34** 条（全部 `kind=modify`）；
- 按 target 节点：落在 **15** 个不同节点上 —— 7 个 MIS（**恰好是全部 OUT MIS**）+ 8 个命题；
- 按 MIS 主题组（仅对 MIS target 计）：LANG 3 / MEM 6 / UB 8；
- 关键事实（640 A1 更新）：签署后 OUT MIS 共 **42** 个，其中只有 **7** 个是 `modify` 目标（`all_out_mis_are_modify_targets=False`）——历史 7 个 OUT MIS（611 快照）至今仍 OUT；

top 分布（节点 → 该节点作为 target 的 modify 边数）：

- `ATOM-UB-GRAY-001::prop-1` → 4 条 
- `ATOM-UB-GRAY-001::prop-2` → 4 条 
- `MIS-LANG-001` → 3 条 （OUT MIS）
- `MIS-MEM-001` → 3 条 （OUT MIS）
- `MIS-MEM-003` → 3 条 （OUT MIS）
- `ATOM-MEM-MOVE-002::prop-1` → 2 条 
- `ATOM-MEM-MOVE-002::prop-2` → 2 条 
- `ATOM-MEM-MOVE-002::prop-3` → 2 条 
- `MIS-UB-001` → 2 条 （OUT MIS）
- `MIS-UB-004` → 2 条 （OUT MIS）
- `MIS-UB-008` → 2 条 （OUT MIS）
- `MIS-UB-014` → 2 条 （OUT MIS）
- `ATOM-LANG-INLINE-001::prop-1` → 1 条 
- `ATOM-LANG-INLINE-001::prop-2` → 1 条 
- `ATOM-LANG-INLINE-001::prop-3` → 1 条 

## 三、两档优缺点（事实，不是裁决）

**`keep-low`（入库权威，640 重算后 IN79/OUT42/击败194）**：
- ✅ 与已冻结的 `data/grounded_labels_w2.json` **逐字段一致**（640 A1 按签署后状态重算），不推翻既有交付；
- ✅ 保守：人审说「保持 low」就保持 low，不替人升档；
- ❌ 与 34 条 modify 人审的**字面意图**（`new_confidence=medium`）**不符** —— 人审想升档，工具没升；
- ❌ OUT MIS 42 个（签署后命题可信度 high，误解本就无法击败命题）。

**`upgrade-medium`（609 A3）**：
- ✅ 尊重 34 条 modify 人审的**字面意图**（medium 落档）；
- ❌ 640 A1 实测：签署后命题可信度 high，34 条 low→medium 的升档**不足以翻转任何判决** ⇒ 两档判决趋同（IN79/OUT42/击败194）——「upgrade 抽空攻击性」的 611 论据已随签署失效；
- ⚖️ 两档的**机制差异**仍在（keep-low 下 34 条 modify 未生效留痕），若未来出现足以翻转的 modify 档位将重新分歧。

## 四、口径裁决建议（不擅自执行）

- 640 A1 诚实登记：**当前数据下两档判决一致**，611 的口径冲突在现有图上不再产生判决差异；冲突的**语义定义**（「modify 到底要不要改权重」）仍未钉死，留待未来出现实际分歧时再裁决。
- 无论哪种，本工具与 `metrics_610.collect_modify_mode` 都已把两档数字**量化显形**，每次采集都能看到 divergence，不会悄悄换口径。
- 无论哪种，本工具与 `metrics_610.collect_modify_mode` 都已把两档数字**量化显形**，每次采集都能看到 divergence，不会悄悄换口径。

> 数字来源：全部由 `weighted_af_solver.reviewed_edges(..., modify_mode=...)` + `solve` 现算，与 `tools/modify_mode_analysis.py --stats` 一致。


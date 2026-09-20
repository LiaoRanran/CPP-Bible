# 611 B2 · modify 口径影响分析（keep-low vs upgrade-medium）

> 背景（610 交人项 ①）：34 条 `modify` 人审的 `new_confidence` **全是 medium**。两种口径对这 34 条的处置不同 ⇒ 判决不同。**本报告只量化差异、给优缺点与建议，不替谁裁决**（口径裁决是监工/人的事，见 §四）。

## 一、两档判决对比（现算，可复算）

| 口径 | IN | OUT | UNDEC | 击败边 | 轮次 |
|---|---:|---:|---:|---:|---:|
| `keep-low`（入库权威 / 611 B1 默认） | 114 | 7 | 0 | 17 | 3 |
| `upgrade-medium`（609 A3） | 121 | 0 | 0 | 0 | 2 |

> **差异**：IN 差 **7** 个（114→121）、OUT 差 **7** 个（7→0）、击败边差 **17** 条（17→0）。

## 二、34 条 modify 边的分布

- 总数：**34** 条（全部 `kind=modify`）；
- 按 target 节点：落在 **15** 个不同节点上 —— 7 个 MIS（**恰好是全部 OUT MIS**）+ 8 个命题；
- 按 MIS 主题组（仅对 MIS target 计）：{'LANG': 3, 'MEM': 6, 'UB': 8}；
- 关键巧合：**7 个 OUT MIS 全部是被 `modify` 过的 MIS**（`all_out_mis_are_modify_targets=True`）—— 所以这 7 个 OUT 是不是该改为 IN，完全取决于口径怎么定；

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

**`keep-low`（入库权威）**：
- ✅ 与已冻结的 `data/grounded_labels_w2.json` **逐字段一致**（IN114/OUT7/击败17），不推翻既有交付；
- ✅ 保守：人审说「保持 low」就保持 low，不替人升档；
- ❌ 与 34 条 modify 人审的**字面意图**（`new_confidence=medium`）**不符** —— 人审想升档，工具没升；
- ❌ 留下 7 个 OUT MIS（含 4 个 UB、2 个 MEM、1 个 LANG），论证层攻击性「被压住」。

**`upgrade-medium`（609 A3）**：
- ✅ 尊重 34 条 modify 人审的**字面意图**（medium 落档）；
- ✅ 消除全部 7 个 OUT MIS（IN121/OUT0）⇒ 论证层「更自洽」；
- ❌ 但 medium 升档让 **42 个 MIS 中 35 个与命题同档** ⇒ **击败边从 17 掉到 0** —— 等于**抽空了论证层的攻击性**（所有 MIS 都和命题一样可信 ⇒ 没有 MIS 能被击败）；
- ❌ 与入库权威产物**不一致**，若采用需重新冻结 `grounded_labels_w2.json`。

## 四、口径裁决建议（不擅自执行）

- **两种口径都不是显然错的**：`keep-low` 保守但违背人审字面意图；`upgrade-medium` 尊重人审但抽空攻击性。冲突的症结是「modify 到底要不要改权重」这个**语义定义**没在任务书里钉死。
- 建议把决策权交**人/监工**，并至少二选一落地：
  1. 若认为「人审的 new_confidence 必须被尊重」 ⇒ 采用 `upgrade-medium`，并**重新冻结** `grounded_labels_w2.json`（IN121/OUT0/击败0）；
  2. 若认为「入库权威产物不可擅动、且 modify 默认只记不生效」 ⇒ 维持 `keep-low`（现状），但应**显式登记**「34 条 modify 字面意图未被采纳」这个事实（避免后续误读）。
- 无论哪种，本工具与 `metrics_610.collect_modify_mode` 都已把两档数字**量化显形**，每次采集都能看到 divergence，不会悄悄换口径。

> 数字来源：全部由 `weighted_af_solver.reviewed_edges(..., modify_mode=...)` + `solve` 现算，与 `tools/modify_mode_analysis.py --stats` 一致。


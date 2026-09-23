# 628 C1 · 人审仪表盘 v2 设计说明

## 视觉设计决策

- **深色底 `#0a0e1a` + 双径向渐变**：长时间盯人审清单不刺眼，且让霓虹强调色有对比度。
- **玻璃拟态**（`backdrop-filter: blur(10px)` + 半透明面板 + 内高光）：卡片有层次，信息密度高时也不糊成一片。
- **青(#3ad6c5)/紫(#8b6cff)霓虹**：青=稳定/已确证，紫=结构性/衍生，玫瑰=需注意，琥珀=待办。
- **粒子背景**：38 个纯 CSS 动画光点（JS 只负责撒点，无外部库），暗示"审计轨迹在持续流动"。
- **CSS 3D 论证图**：`perspective:900px` + `transform-style:preserve-3d`，外层 stage 46s 匀速 rotateY，节点用 `translate3d` 落在黄金角球面上，hover 放大 2.1×。

## 数据模块（6 个）

| # | 模块 | 数据源 | 当前值 |
|---|---|---|---|
| 1 | 人审进度环形图 | `review_item_ledger.jsonl` | 唯一 93 · 待审 93 · 独立盲审 0 |
| 2 | 歧义度热力图 | `review_item_ledger.jsonl` | 高 30 · 中 63 · 低 0 |
| 3 | review_method 饼图 | `decision_event_v2_ledger.jsonl` | {"ITEM_OPEN": 30, "MIRROR_DERIVED": 194, "BATCH_AUTH": 228} |
| 4 | W2 论证图 3D | `grounded_labels_w2.json` | 121 节点 · IN114/OUT7/UNDEC0 |
| 5 | 独立人类确认强度 | DecisionEvent `blind_review_id` | 0 / 93 |
| 6 | 他验三件套状态 | `data/vsa/` + `transparency_log.jsonl` | 凭证 10 张 · 日志 15 条 |

## 与 v1（625 D2）对比

- v1：纯静态深色 + SVG 条形图 + 可筛选表格，无动效、无 3D、无他验状态。
- v2：玻璃拟态 + 霓虹 + 粒子动画 + CSS 3D 论证图 + 环形/饼图/仪表 + 他验三件套状态卡。
- v2 **纯静态自包含**（无 CDN、无网络），双击即可离线打开。

## 偏差登记（任务书假设 vs 实测）

- 任务书写"人审进度环形图（388 条…）"：仓库内**无 388 这一口径**（`grep 388 data/` 零命中）。
  实测口径为 **93 unique 审查项**（记录 93 条）与 **452 条 DecisionEvent**；环行图按"唯一审查项"画，另在 KPI 卡并列展示决定事件 452 条。
- 任务书饼图列出的 `ITEM_BLIND` 当前为 **0 条**（真实盲审未执行），饼图按实际存在的三类画。

## 局限性

- 纯 CSS 3D（非 WebGL/Three.js）：节点只有位置和缩放，没有边/连线与真实图布局。
  若要更炫的 3D 论证图（含边、可旋转拖拽），需引入 Three.js——按硬边界 14 留后续批次。
- 环形/饼图用 SVG stroke 与 `conic-gradient`，非图表库；配色对色盲不友好（未做可访问性配色）。
- 只读展示：不做任何判决、不改日志。

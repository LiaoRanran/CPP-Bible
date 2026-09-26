# 640 A1 · 36 项 B 类存量逐项修复记录

> 根因综述：632/634 命题级人审授权签署（639 修正 `v0.2:`→`human:` 前缀）使命题可信度
> 升为 **high** ⇒ W2 中误解节点无法再击败命题 ⇒ 权威产物 `grounded_labels_w2.json`
> 重算为 **IN79/OUT42/击败边194**（旧 114/7/17 为签署前快照）⇒ 下游全部依赖该图的
> 指标/测试随之演进。所有"新值"均从实际输出取得（测量记录：`640_w2_measure.txt`）。

| # | 测试 | 根因 | 修法 | 结果 |
|---|---|---|---|---|
| 1 | autoimmune_diagnose_630::test_report_json_and_selftest | 工具自检断言"三条规则都覆盖"，现仅 1 条规则有 warn（另两条被 631/632 填充消解） | 自检改为"存量 warn 仅剩 ATOM-CLAIM-CONCEPT-NORMALIZED" | ✅ |
| 2-5 | autoimmune_human_queue_631 ×4 | 清单 90→65（signed_by 类全消解）；工具 selftest 同硬编码 | 测试与工具 selftest 同步 65；fields={object}；行数 65 | ✅ |
| 6 | autoimmune_recalc_630::test_read_only_report_and_selftest | 场景断言（auto=42/悲观 block>0）过期 | auto=0（631 已填完）；悲观安全内核（机器签署被拒）保留 | ✅ |
| 7-9 | autoimmune_threshold_630 ×3 | 随组内数据修复连带自绿 | 无需改 | ✅ |
| 10 | baseline_629::test_gate_counts_measured_equals_standing | 实测 121 vs 历史快照 191 | 实测/历史分账：断言现值，STANDING 存档不动 | ✅ |
| 11-13 | bridge_edge_impact_612 ×3 | base_summary 114/7、121/0 过期；工具 --check 对账 | KNOWN_BASE 更新（两档 79/42） | ✅ |
| 14-16 | metrics_612 ×3 | KNOWN_KEEP_LOW/UPGRADE 常量过期 | (79,42)/(79,42) + docstring 更新 | ✅ |
| 17 | metrics_grounded_status_610::test_divergence_is_surfaced_not_hidden | divergence 恒 True（工具 bug）+ 数值过期 | 修 bug（比判决数值）+ 断言 (79,42,194)/False | ✅ |
| 18-22 | modify_mode_611 ×5 | 双模式趋同（34 条 modify 不足以翻转）；diff 翻转 35→0 | 断言按新权威值 + 机制断言保留（34 条未生效留痕） | ✅ |
| 23-25 | modify_mode_analysis_611 ×3 | OUT_MIS_7 历史常量 vs 现 42 | 工具改现算口径（历史 7 留档），报告重写，check 令牌同步 | ✅ |
| 26-33 | prop_graph ×8 | 签署后 prop_signed=79/unsigned=0（测试锁"存在 3 条未签"） | 断言全签；pending 视图空态；正式 propositions.db 重建 | ✅ |
| 34-38 | replay_invariants 605/606/608 ×5 | **真 bug**：toolchain 模块级守卫劫持导入方 ⇒ 真实不变量从未运行 | 守卫移入 __main__（toolchain + 8 个同风险工具）+ 审计 + 回归锁 | ✅ |
| 39 | weighted_af_human_review_609::test_single_approve | 单 approve 翻转 OUT→IN 依赖"命题未签" | 翻转=0（签署后不可能）；promote 机制断言保留 | ✅ |

## 修复过程新发现（本轮新增、已修）

- **toolchain 守卫劫持**（#34-38 的真根因，影响面见 `640_check_backfill.md` §二）；
- **metrics_610 divergence 恒 True**（整字典比较含恒异 caliber 标签，两处）。

## "假绿"防线

- 每处数值更新前先**测量实际输出**（`640_w2_measure.txt` / `640_modify_check.txt`）；
- 行为类断言（翻转/归因/安全内核）不是简单删掉，而是**改锁当前正确行为**；
- 发现任意"新值与设计语义冲突"即停——本轮未遇到（签署后果是 documented
  credibility ladder 的直接推论）。

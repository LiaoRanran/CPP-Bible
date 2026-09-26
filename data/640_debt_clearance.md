# 640 债务清算

## 一、639 移交的 36 项 B 类测试常量过期

| 组 | 项数 | 修法 | 状态 |
|---|---|---|---|
| autoimmune_diagnose_630 | 1 | 自检断言改现算（warn 剩 1 规则/65 条） | ✅ |
| autoimmune_recalc_630 | 1 | 场景断言按 631/632 后实测更新（auto=0；悲观安全内核保留） | ✅ |
| autoimmune_human_queue_631 | 4 | 90→65（signed_by 类已消解）；工具 selftest 同步 | ✅ |
| autoimmune_threshold_630 | 3 | 随组内修复连带自绿 | ✅ |
| baseline_629 | 1 | 实测(121/0/116/5)与历史快照(191)分账 | ✅ |
| bridge_edge_impact_612 | 3 | KNOWN_BASE 更新（79/42 趋同）+ 工具重生成 | ✅ |
| metrics_612 | 3 | 常量 (79,42)；--check/报告连带 | ✅ |
| metrics_grounded_status_610 | 1 | divergence 真 bug 修复 + 数值更新 | ✅ |
| modify_mode_611 | 5 | 双模式趋同断言 + diff 翻转 35→0 + CLI 121→79 | ✅ |
| modify_mode_analysis_611 | 3 | 工具改现算口径（OUT MIS 42，历史 7 留档）+ 报告重写 | ✅ |
| prop_graph | 8 | 签署后 79 全签/0 未签；正式库重建；空态 fail-soft | ✅ |
| replay_invariants 605/606/608 | 5 | **真 bug**：toolchain 模块级守卫劫持导入方 ⇒ 守卫移入 __main__，真实不变量恢复运行 | ✅ |
| weighted_af_human_review_609 | 1 | 单 approve 翻转=0（签署后误解不可 IN），机制断言保留 | ✅ |

**合计 36/36 全清，0 假绿**（每项修法与依据见 `640_b_class_fix.md`；根因综述见
`639_round3.md` §二.B——632/634 命题级人签使命题可信度升 high，误解无法再击败命题）。

## 二、D9/D11/D12/D8 登记项

| 项 | 处置 | 状态 |
|---|---|---|
| D9 闭环路线图对齐 | `roadmap_align_640.py` 覆盖层（方向标签 + ×1.5/×0.5/×1.0 加权重排） | ✅ |
| D11 工具数表 | 实测 437/437，活数表均为动态取值，无过期硬编码；登记于 `640_baseline.md` §四 | ✅ |
| D12 老工具 --check | 终验 434 工具：430 有 / 4 例外（无 CLI 库模块×3 + 脚本即体检×1，注明理由） | ✅ |
| D8 conftest 防复发 | 清理器安全化（tracked 不删/豁免名单/临时才删/保守默认保留/全留痕 jsonl），6 例单测 + 实况金丝雀 | ✅ |

## 三、640 过程中新发现并修复的真 bug

1. **toolchain 模块级守卫劫持**（634 A2 范式缺陷）：被导入时 `sys.exit(0)` 劫持调用方
   —— `replay_invariants --check` 从未真正运行过不变量。修复 + 全库审计
   （`guard_audit_640.py`：79 守卫工具中 8 个有劫持风险，全部移入 `__main__`）+ 4 例回归锁；
2. **metrics_610 divergence 恒 True**：整字典比较含恒异的 `caliber` 标签字段 ⇒ 指标失去
   意义。两处（collect_modify_mode / collect_grounded_status）改为只比判决数值。

## 四、遗留（交 641）

- 真实仓库 376 项 data/*.md 行尾空白（CRLF 归一，git 内容零 diff）——低价值，未批量处理；
- `ruff format --check tools/` 触发 ruff 自身崩溃（超大文件 Annotation range bug）——ruff 侧问题，登记；
- auto_executor 的 `ruff_fix` / `snapshot_update` 两类已定义未实弹（仓库当前无对应待修项），
  首战使用时人工盯一次。

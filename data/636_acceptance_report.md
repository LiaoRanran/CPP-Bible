# 636 验收报告（E1 · 收工门禁）

- 总体结论：**通过 ✅**

## 一、门禁各项

| 项 | 结果 |
|---|---|
| 新工具 --check | 8/8 |
| ruff tools/ tests/ | ✅ |
| mypy tools/ 0 errors | ✅ Success: no issues found in 417 source files |
| 受控目录零污染 | ✅ |
| 交付文件齐备 | 8/8 |

## 二、8 任务完成情况

| # | 任务 | 状态 | 交付 |
|---|---|---|---|
| 0 | 开工快照+基线复测 | ✅ | `636_baseline.md`（15 指标无漂移） |
| 2.1 | 冲突检测器影子 | ✅ | `636_conflict_detector_shadow.md`（23 卡，超阈 2） |
| 2.2 | anti-windup 设计 | ✅ | `636_anti_windup_design.md`（半饱和，223 冻结模拟） |
| 2.3 | blind_protocol 影子 | ✅ | `636_blind_protocol_design.md`（违规 258，分歧率无数据） |
| 2.4 | 校准追踪器+known_error_rate | ✅ | `636_calibration_tracker_report.md`（67 全无数据） |
| 2.5 | MDL 试运行 | ✅ | `636_mdl_trial_run.md`（admit 30/reject 37） |
| V26-补1 | 污染追踪器影子 | ✅ | `636_contamination_tracker_shadow.md` |
| V26-补2 | 四态判决模拟 | ✅ | `636_four_state_simulation.md`（假 pass 1） |
| E1 | 收工门禁 | ✅ | 本报告 |

## 三、偏差与诚实登记（§七）

1. **全部保护器为影子**：不拦截、不改判（§零.1/§零.7）；
2. 冲突检测器 `agreement` 用证据存在率近似、RR 无区分度（已登记）；
3. anti-windup 的周处理能力为**假设值**、等待天数为近似；
4. blind_protocol **分歧率无盲评基线 ⇒ 写「无法计算」**，未编造；
5. known_error_rate **67 条全部「无数据」**（未编造）；
6. MDL **编码长度为启发式**（非严格 MDL）；7 条新规则不在热力图 ⇒ 必 reject；
7. 四态/污染分类均为**关键词/文本级启发式**；
8. **本批未 push**（§零.13）⇒ 收工 ahead>0。

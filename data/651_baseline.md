# 651 阶段 0 · 开工基线快照（整体建设 W0-W3）

> 写于 2026-09-27。批次 651：W0 词表 + W1 头部 + W2 尾部 + W3 中间，边建设边修。

## 一、协议确认
- 650 已收工：`_auto/status.json` 记录 `last_completed_batch=650`，queyi-core 7 提交、CPP-Bible 2 提交。
- 本轮工作落在 **CPP-Bible**（知识库：atoms/docs/data/tools），非 queyi-core。

## 二、双仓库 git 状态（开工）
| 仓库 | HEAD | ahead(origin/master) |
|---|---|---|
| CPP-Bible | `3f2b6f32` | 6 |
| queyi-core | `b9832d1` | 7 |

## 三、关键资产定位（651 依赖）
| 资产 | 位置 |
|---|---|
| 452 条改判账本 | `data/authority/decision_event_v2_ledger.jsonl` |
| 648 十张 C 卡 | decay / malloc / strbound / fnptr / volatile / setjmp / intpromo / bitfield / macro / signedovf |
| 648 实测/命令/期望值 | `data/648_c_probe.json`（含 fixture 源码路径 + 各编译器/标准/优化档 cmd + kv） |
| 648 标准原文 | `data/648_c_standard.md`（N1570 逐字条款） |
| 信任根 | `tools/tool_integrity.py`：CORE_TOOLS(5) + TEST_CONFIG_TOOLS(2) + SUPPLY_CHAIN_FILES；**新增 651 工具不影响闭包**；E 阶段跑 `--check` 证明未破 |
| 两阶段 pytest 纪律 | `docs/pytest_two_phase.md` |
| 保护器 | `tools/blind_protocol_647.py` / `anti_windup_647.py` / `calibration_tracker_642.py` / `mdl_gate_647.py` / 冲突检测 |
| 编译缓存 | `tools/.compile_cache.json`（649/650 提及的"编译缓存"确在此仓库） |

## 四、限界与诚实边界（开工登记）
1. **受控目录写保护**：卡片是内容寻址（PCK hash），**改 atoms/*.md 会致 hash 漂移**（626/628 实证）。
   故 H7「卡片 frontmatter 加 verified_at/superseded_by/recheck_after」本批**只出 dry-run 计划 + 陈旧标记队列，不真写卡**，交人审批（符合 W1 只读/旁路）。
2. **全量 pytest 时长**：642 实测整仓 ~36 分钟，超出本工具 idle-timeout（644/649 已登记）。
   本批 E 阶段跑 **651 新测试两阶段 + 相关子集**，全量以诚实登记（不虚报）。
3. W2 改 schema **只加字段不改语义**、向后兼容；W3 新东西**一律 shadow，不真上岗**。

## 五、651 交付清单（对照任务书）
| 阶段 | 交付 |
|---|---|
| A W0 | `docs/evidence_dual_axis.md`、`docs/verdict_extension.md`、`docs/pck_c2pa_mapping.md` |
| B W1 | `tools/evidence_aging_651.py`(H7)、`tools/seeker_replay_651.py`(H1)、`data/651_h2_dual_axis_review.md`(H2) |
| C W2 | `tools/ledger_checkpoint_651.py`(T4)、`tools/verdict_extension_651.py`(T1)、`tools/replay_probe_651.py`(T5)、`tests/test_core_pbt_651.py`(T6) |
| D W3 | `tools/shadow_rotator_651.py`(M2)、`tools/calibration_upgrade_651.py`(M3)、`tools/human_review_queue_651.py`(M7) |
| E | `tools/run_651_gate.py` + `data/651_acceptance_report.md` + `_auto/outbox/651.md` |

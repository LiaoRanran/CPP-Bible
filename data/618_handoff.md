# 618 交接清单（继承 617 未完成 12 任务）

> 来源：617 收工（`data/617_acceptance_report.md` + `data/617_debt_clearance.md`）。617 已完成 11 任务，余 **12 任务**诚实登记于此，待 618 执行。
> 铁律（继承）：不跑监工门禁（run_614_gate 等全量 --check）；不碰受控目录（atoms/evidence/Examples/Book/CORE_TOOLS/golden_lock/poison_drill）；数字取 SNAPSHOT_MANIFEST_617.json + 616 基线；一任务一 commit。

## 一、待执行任务（12）
| 任务 | 内容 | 依赖/参考 |
|---|---|---|
| **A3** | escaped/equivalent 的 L2b 精确工具落地（e-process mixture / conformal prediction）| 方法见 `data/confidence_sequence_l3_shrinkage.md`；接入 `tools/confidence_sequence.py` 新分支；A1 枚举器当前对二者标 None（禁填 0）|
| **B2** | independence_level 接入 gate 报告（gate 结果标注独立性等级）| `tools/verify_independence_level.py`（B1）；注意避免改受控 `gate_engine.py`，优先只读消费 |
| **B3** | independence_level 接入 poison 报告 | 同上 |
| **B4** | independence_level 接入 replay 报告 + 收尾 doc | 同上 |
| **C2** | 3 个分类计数脚本（replay / poison / gate category）| taxonomy 见 `data/test_taxonomy_617.md`（C1）|
| **C3** | slash-command doc（`/verify` 等按类别触发验证）| 配合 C2/C4 |
| **C4** | 分类映射表（机器可读，tests → 类别）| 落 `tests/test_category_map.py` 或 JSON |
| **D1** | SNAPSHOT 治理方案 doc（manifest 规范 + CI 集成策略）| 工具已就 `tools/snapshot_manifest.py`（D2）|
| **D3** | CI 集成 doc（SNAPSHOT_MANIFEST 进 CI 防回归漂移）| 配合 D1 |
| **E1** | 人审可执行化 doc（30 条逐条复核工作流）| 交人项 615 #1 / 616 #1 |
| **E2** | 人审待办清单生成工具（从 evidence 卡生成 30 条逐条复核清单）| 参考 `tools/human_review_honesty_615.py` |
| **E3** | 人审待办清单文档（清单 + 裁决模板）| 配合 E1/E2 |

## 二、已被 617 覆盖、勿重复
- **D4/G2**（数字漂移）：已建 `data/SNAPSHOT_MANIFEST_617.json` + `data/project_key_numbers_quickref_20260921_v7.md`（manifest 派生，废弃手填 v6）。历史 PM 报告（34/33 等）中的手写计数可系统性重指向 v7（低优先，可并入 D1）。
- **G1**（桌面离线包）：已建 `dist/queyi_offline_launcher.bat` + `dist/OFFLINE_README.md`。

## 三、交接口径
- 617 验证数字：commits 1517 / tools 218 / tests 213 / atoms 28 / EV 56（SNAPSHOT_MANIFEST_617.json）。
- 冻结基线：gate 63/191、poison 124/124、replay 56/0/0、mutation 1/1406、CS 0.9062%/CP 0.3370%、人审 388、独立性 L1/scalar 0.153、信任根 partially_anchored。
- 新增工具（A1/B1/D2）均带单测且本地通过，可直接复用。
- 本交接不执行任何裁决；交人项（616 的 10 项 + 617 新增 1 项）继续有效。

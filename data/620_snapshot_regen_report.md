# 620 任务 2 · 权威 SNAPSHOT_MANIFEST 重钉报告

> 命令：`.venv\Scripts\python.exe tools/snapshot_manifest.py`（默认输出 `data/SNAPSHOT_MANIFEST.json`）
> 本工具只读 git/filesystem 直取计数，不跑任何监工门禁（符合铁律）。

---

## 一、旧 SNAPSHOT_MANIFEST（重钉前）

| 字段 | 值 |
|---|---|
| generated_at | 2026-09-21T13:50:24+00:00 |
| head_commit | `d2f412ba990e28721e43502fc792c00470061487` |
| live_counts.commits | 1553 |
| live_counts.tools_py | 233 |
| live_counts.tests_py | 226 |
| live_counts.atoms_md | 28 |
| live_counts.evidence_ev_md | 56 |
| FROZEN_VERIFICATION.gate | 63 / **191** / **block 0** / warn 186 / advice 5 |
| FROZEN_VERIFICATION.poison | 124/124，诚实 60/63 |
| FROZEN_VERIFICATION.replay | 56/0/0 |
| FROZEN_VERIFICATION.mutation_v7 | 1593 / 1406 / escaped 1 / n_a 179 / equivalent 8 |

> 619 独立验收曾判定该文件「权威源失准（记 191/block=0 而活体 195/block=2）」。
> 任务 1 已证伪该判定（活体稳态即 191/block=0，见 `620_block_fix_report.md`），
> 故旧文件的 **FROZEN_VERIFICATION 本就正确**，本次不作改动。

## 二、新 SNAPSHOT_MANIFEST（重钉后）

| 字段 | 值 |
|---|---|
| generated_at | **2026-09-21T15:05:38+00:00** |
| head_commit | **`bf9e5b08f02d9d930fe37fdf8d21858914534994`** |
| live_counts.commits | **1555** |
| live_counts.tools_py | 233 |
| live_counts.tests_py | 226 |
| live_counts.atoms_md | 28 |
| live_counts.evidence_ev_md | 56 |
| FROZEN_VERIFICATION.gate | 63 / 191 / block 0 / warn 186 / advice 5（**保持不变**） |
| FROZEN_VERIFICATION.poison | 124/124（保持不变） |
| FROZEN_VERIFICATION.replay | 56/0/0（保持不变） |

## 三、差异对比

| 字段 | 旧 | 新 | 变化 |
|---|---|---|---|
| generated_at | 13:50:24 | 15:05:38 | 刷新 |
| head_commit | d2f412b | bf9e5b0 | 前进 2 commit（620 任务0 / 任务1） |
| commits | 1553 | **1555** | +2 ✅（= 620 任务0、任务1） |
| tools_py | 233 | 233 | 不变（620 尚未新增工具） |
| tests_py | 226 | 226 | 不变（620 尚未新增单测） |
| atoms_md | 28 | 28 | 不变 |
| evidence_ev_md | 56 | 56 | 不变 |
| FROZEN_VERIFICATION 全部字段 | — | — | **未改动**（本就与实测一致） |

**结论**：本次重钉只刷新了 `generated_at` / `head_commit` / `live_counts.commits` 三项时间戳与计数；
`verification_baseline_frozen` 逐字保持不变。

## 四、与任务 1 结论的一致性核验

| 门禁/数字 | 冻结基线 | 任务1 稳态实测 | 一致？ |
|---|---|---|---|
| gate 规则/命中 | 63 / 191 | 63 / 191 | ✅ |
| gate block | 0 | 0（连跑 3 次） | ✅ |
| gate warn/advice | 186 / 5 | 186 / 5 | ✅ |

⇒ **权威源与实际状态一致**，重钉完成。

## 五、权威源重钉确认

- `data/SNAPSHOT_MANIFEST.json` 已重新生成并提交；
- README / qmd / quickref 应引用本 manifest 的 `live_counts`，禁止手填（manifest `note` 字段已声明）；
- `verification_baseline_frozen` 为冻结数字，重跑须走监工门禁（本工具不跑，本批亦未重跑）。

## 六、遗留说明

- 工作树中 `data/SNAPSHOT_MANIFEST.json` 此前为「已修改未提交」状态（619 遗留），
  本次重钉后已随本 commit 入库。
- 620 后续任务新增工具/单测后，收工前（E1/E2）将再次重钉，使 `tools_py` / `tests_py` 反映最终值。

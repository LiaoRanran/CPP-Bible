# 619 C2 · 历史手填计数重指向 manifest 策略

> 背景：617 D4 治理数字漂移时，发现多处手填计数相互矛盾（README 写 1469 commits/204 tools/183 tests，
> quickref_v5 写 1446/196/175，实际 live = 1517/218/213）。619 C1 已把**权威**快照收敛为
> `data/SNAPSHOT_MANIFEST.json`。本文件制定「历史手填计数如何重指向、何时做」的策略。

## 一、唯一事实源（已落地）

| 维度 | 事实源 | 守护 |
|---|---|---|
| 仓库计数（commits / tools_py / tests_py / atoms_md / evidence_ev_md） | `data/SNAPSHOT_MANIFEST.json` → `live_counts` | `tools/snapshot_manifest.py`（git/filesystem 直取，零手写） |
| 书稿计数（章 / cpp 块 / 密度） | `build/metrics.json` | `tools/gen_metrics.py --check` + `consistency_check.py` |
| 冻结门禁基线（gate/poison/replay/mutation…） | `SNAPSHOT_MANIFEST.*.verification_baseline_frozen` | 616 基线，重跑须监工门禁 |

> 两类计数是**不同维度**，不要混用：仓库计数 ≠ 书稿计数。README 头部的「147 章 / 7515 cpp」属于书稿维度，
> 由 `gen_metrics` 守护，**无需**指向 SNAPSHOT_MANIFEST（C2 不改 README，避免越界）。

## 二、现存手填计数盘点

| 文档 | 手填计数 | 状态 |
|---|---|---|
| `data/project_key_numbers_quickref_20260921_v7.md` | 仓库计数 | **C1 已重指向** `SNAPSHOT_MANIFEST.json` ✅ |
| `README.md`（头部） | 书稿计数 | 由 `gen_metrics` 守护，维度不同，**保留** |
| `data/project_key_numbers_quickref_v5.md` / `v6.md`（历史） | 漂移旧值 | 已被 v7 取代，归档，**标注过期** |
| `00_README` / 旧 PM 文档（1469/204/183） | 漂移旧值 | 历史证据，**标注过期**，不修 |
| `_arch_v21/*`（并行会话存档，未入库） | 引用旧值 | 未跟踪，非仓库口径 |

**结论**：在**已入库的活跃文档**中，唯一会漂移的仓库计数源 `quickref_v7` 已在 C1 修复；
其余手填均为历史/归档或书稿维度，无需重指向。

## 三、重定向方法

1. **新文档 / 改文档**：凡引用仓库计数，写「见 `data/SNAPSHOT_MANIFEST.json` 的 `live_counts.<字段>`」，
   或粘贴该字段的当前值并标注「派生自 manifest，重跑 `snapshot_manifest.py` 更新」，禁止裸手填。
2. **版本化 pin**：需要冻结某批次快照时，用 `snapshot_manifest.py --batch <id>` 生成
   `SNAPSHOT_MANIFEST_<id>.json`（如 617 归档），活跃文档指向权威 `SNAPSHOT_MANIFEST.json`。
3. **书稿维度**：继续由 `gen_metrics` 守护，与仓库 manifest 平行，不混。

## 四、何时做（执行计划）

- **现在（619 C1）**：quickref_v7 datasource 已改 ✅。
- **620（建议）**：
  - 为过期 quickref_v5/v6 加「本文件已废弃，见 v7」顶部标注（不删，保历史 provenance）。
  - 在 `governance verify` 增加一条规则：**扫描活跃 md/qmd，凡出现 `commits`/`tools`/`tests` 字样的裸数字，
    与 `SNAPSHOT_MANIFEST.json` 比对，偏差 >5% 即红**，从机制上杜绝再漂移。
  - 评估是否把 618 等工具内部的 `SNAPSHOT_MANIFEST_617` 常量统一改为权威文件名（低优先级，因冻结段一致）。
- **不做**：不动 `Book/`（书稿维度，由 gen_metrics 管）、不动未入库的 `_arch_*` 存档。

## 五、诚实登记

- C2 只产出**策略**，不批量改历史文档（避免误伤 provenance 与历史记录）。
- 重定向的「机制保障」（`governance verify` 规则）留 620；619 仅把活跃事实源收敛到位。
- 经盘点，619 结束时**已入库活跃文档中无残留漂移的仓库计数**（quickref_v7 已修）。

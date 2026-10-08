# data/ CHANGELOG · 数据版本记录

> 只记**权威数据的版本变化**，不记报告类产物。
> 每次改动冻结产物，必须在这里追加一条，并说明**为什么改**。
> 校验命令：`python tools/gen_693_manifest.py --check` + `python tools/verify_data_integrity.py`

---

## 记录格式

```
## YYYY-MM-DD · <批次号> · <变更标题>
- 变更：<哪个文件，从什么变成什么>
- 原因：<为什么要改；不改会怎样>
- 影响：<哪些数字会变 / 不变>
- 复核：<用什么命令验证>
- sha256 清单：<已更新 / 不需要更新>
```

---

## 2026-10-08 · 693 · 新增人类 IAA 材料包与数据完整性设施（**不改任何冻结数据**）

- 变更：**新增**（不改动既有冻结产物）
  - `693_ai_double_label.json` —— AI 双标（n=145）
  - `693_human_adjudication_package.csv` —— 31 条裁决表（`human_verdict` 留空）
  - `693_data_manifest.sha256` / `693_data_manifest.json` —— 14 项冻结产物 sha256 清单
  - `693_data_integrity.json` —— 数据完整性校验结果
  - `693_perf_bench.json` —— 数据访问性能实测
- 原因：692 验收报告 H1 登记"人类 IAA 仍为 0"。本批补齐人类裁决材料，
  并首次给冻结产物建立 sha256 清单（此前只有 `data_integrity_676h.py` 的样本清单检查）。
- 影响：**论文数字全部不变**。本批对 `data/*_matrix.json` **只读**。
- 复核：
  ```bash
  python tools/gen_693_manifest.py --check      # 14 项，失配 0
  python tools/verify_data_integrity.py         # 六项全过
  python tools/annotate_693_b.py --csv          # 复算 κ=0.495
  ```
- sha256 清单：**新建**（本批首次建立）

---

## 2026-10-08 · 692 · 环境感知实验与公平对比（**不改冻结矩阵**）

- 变更：**新增**
  - `692_environment_paired_experiment.json` —— E1/E2 配对实验（0 次 detect）
  - `692_fair_comparison_raw.jsonl` / `692_fair_comparison_results.json` —— clang-tidy 22.1.8 + cppcheck 2.21.0 公平对比
  - `692_llm_audit_raw.jsonl` / `692_llm_audit_results.json` —— LLM 第四臂（N=80，480 次调用）
- 原因：环境是测量的坐标；缺资产的"掉点"叙述本身是错的，需要显式化。
- 影响：论文数字不变；新增的是"环境敏感性"证据。
- 复核：`python tools/analyze_692_environment.py`
- sha256 清单：N/A（当时尚未建立）

---

## 2026-10-07 · 683 · 真实世界靶场（**新增数据集**）

- 变更：**新增** `683_real_world_detection_matrix.json`（110 × 8）、
  `683_real_world_project_matrix.json`、`683_real_world_type_matrix.json`、
  `683_real_world_candidates_verified.json`（109/109 NVD FOUND）
- 原因：合成语料的仪器性证据不足以支撑"真实缺陷"claim，需要可追溯靶场。
- 影响：新增 **110 条真实缺陷重构**；论文新增 Real-World Validation 附录。
- 复核：`python data/realworld_683_runner.py --stage merge` + `python tools/analyze_683_realworld.py`
- sha256 清单：N/A

---

## 2026-10-04 · 681 · 缺陷类型词表归一化（**56 → 34 项**）

- 变更：`blindspot_676g_detection_matrix.json` 的 `samples[].defect_type`
  从 56 个 legacy 取值归一到 **34 项闭集**（覆盖 1147 行）
- 原因：38 个 legacy 标签里 24 个只出现在扩样行的旧列，14 个出现在 105 条原始行；
  词表不统一会让"按类型统计"失去意义。
- 影响：类型分布统计全部重算（`681_type_stats_normalized.json`）；
  **A5 主端点不变**（标签修正对主分析零影响，676m 已逐位复核）。
- 复核：`python tools/repair_681_labels.py`（幂等）+ `data/681_标签修复日志.json`
- sha256 清单：N/A

---

## 2026-10-04 · 676m · 字段完整性修复（M1–M5）（**不改 A5 主端点**）

- 变更：34 条挂起样本判据修正；字段完整性 M1–M5 补齐；
  产出 `676m_sample_manifest_corrected.json`（含 34 项 `vocabulary`）
- 原因：挂起样本被误记为 `miss`（应为 `unknown` 或按超时口径）；字段缺失影响可复算性。
- 影响：**A5 主端点逐位不变**（`tools/recompute_a5_676m.py --check` 门禁守护）。
- 复核：
  ```bash
  python tools/fix_676m_schema.py --verify       # H1 残留 0 / 待迁移 0
  python tools/recompute_a5_676m.py --check      # 与 676f 逐位一致
  ```
- sha256 清单：N/A

---

## 2026-10-03/04 · 676g · 冻结检测矩阵 v1.0（**基线**）

- 变更：**新增** `blindspot_676g_detection_matrix.json` —— **1147 样本 × 8 资产**
- 原因：需要一份可被独立复算的、带完整环境画像的检测矩阵。
- 影响：OR 口径检出 **61.6%**（707/1147）；盲区 **38.4%**（440/1147）；
  条件 recall（分母 674）**94.21%**。
- 环境：WSL g++ 13.3.0（asan/ubsan/tsan）+ MinGW g++ 13.1.0 + clang 22.1.8，`-O0/-O2` 双档
- 复核：`python tools/recompute_a5_676f.py`
- sha256 清单：N/A

---

## 变更纪律（重申）

1. **冻结产物只增不改**。要改就在新批次产出新文件。
2. 改了就必须**重生成 sha256 清单**并在此处追加记录。
3. **绝不允许**为"让校验通过"而重生成清单来掩盖改动。
4. `unknown` 永不折叠进 `miss`。
5. 每条记录必须写清**原因**与**复核命令**——只写"更新了 X"不算记录。

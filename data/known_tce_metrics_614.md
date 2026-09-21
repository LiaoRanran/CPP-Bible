# 614 D2 · known-TCE metrics（M1 状态反映）

> 铁律：数字取自冻结基线 `data/mutation/full_baseline_v7.json`；**不**重跑 mutation 监工门禁。

## 一、登记条目
- 文件：`data/known_tce.jsonl` ｜ 条目：**1**
- `id=TCE-614-001`：`M1 / evidence/conc/EV-CONC-001.md / 删 negative_controls`，`status=known-structural`。

## 二、metrics（M1 状态）
| 指标 | 值 | 说明 |
|---|---|---|
| `known_tce_count` | **1** | 已登记的结构性逃逸 |
| `variants` | 1593 | 全量变体 |
| `blocked` | 1405 | 被拦 |
| `escaped` | **1** | 唯一（= TCE-614-001） |
| `judged`（可判分母） | 1406 | blocked + escaped |
| `escape_contract` | **1/1406** | 逃逸率契约（**未变**） |
| 其中 `known_structural` | 1 | M1（冻结 TCE） |
| 其中 `live_bugs` | **0** | 活雷数（本批无新增） |

## 三、口径纪律
- 逃逸率契约**仍为 1/1406**——登记**不**移除该逃逸，只**标注其性质**（known-structural）。
- **禁止**用"已登记"当作"已修复"⇒ 更**禁止**宣称「0 逃逸」。
- 若未来 TCE（W2）解冻并实现 M1 检测，该条目应转为 `fixed` 并从 `escaped` 移除（届时契约再重算）。

## 四、gate 豁免标注
- `tools/gate_engine.py` 的 `negative_controls` nc-form 规则区已加**注释索引**（指向本登记），
  明确「本规则不覆盖『键整段缺失』」这一已知边界；**未**改任何规则行为（冻结基线不变）。

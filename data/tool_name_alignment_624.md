# 624 D2 · 工具名对齐 + 功能合并确认

> 背景：623 提示词点名要新建的 `escape_root_cause_v2_623.py` 与 `vfdr_updater_623.py` **在仓库中不存在**。
> 本任务核查：623 A3/A5 的功能是否完整、实际以何种形式交付。

---

## 一、623 工具名对应关系（提示词名 vs 实际）

| 623 提示词声明的工具 | 实际是否存在 | 实际交付形式 |
|---|---|---|
| `tools/escape_root_cause_v2_623.py` | ❌ 不存在 | **数据件 + 测试**：`data/escape_root_cause_v2_623.md` + `tests/test_escape_root_cause_v2_623.py`（共 134 行，见 commit `17eb0e45`） |
| `tools/vfdr_updater_623.py` | ❌ 不存在 | **数据件 + 测试**：`data/vfdr_report_623.md` + `data/_heatmap_summary.json` + `data/rule_touch_heatmap_623.md` + `tests/test_rule_touch_heatmap_623.py`（共 528 行，见 commit `708e7782`） |

**结论**：623 A3/A5 的功能**未做成 CLI 工具**，而是以**数据件（md/json）+ 可复现测试**交付。

## 二、功能完整性确认

### 2.1 A3 根因分析（`data/escape_root_cause_v2_623.md`）
- 内容：4 条 escaped 的根因（全为 M1 删 `claim_structured` 假象）、真实危险逃逸 = 0、口径修正建议。
- 测试 `tests/test_escape_root_cause_v2_623.py`（3 例）：从 `high_complexity_sandbox_run_623.json` **可复现**验证
  （4 条 escaped 均为内容删除、无新增 block、触达 > 622 的 9）。
- **判定：功能完整**（分析结论 + 可复现验证俱在）。

### 2.2 A5 VFDR + 热力图（`data/vfdr_report_623.md` / `rule_touch_heatmap_623.md`）
- 内容：VFDR 双轴口径 + 63 规则 × 2 轮热力图 + 累计 26/63 + 37 盲区清单。
- 测试 `tests/test_rule_touch_heatmap_623.py`（3 例）：热力图存在、summary 一致（26/63）、累计可复算。
- **判定：功能完整**（数据 + 可复现验证俱在）。

## 三、624 已提供工具化后继（带 `--check`）

| 623 功能 | 624 工具化后继 | 说明 |
|---|---|---|
| 根因分析 v2 | **`tools/escape_root_cause_v3_624.py`** | 升级：新增跨卡 4 维度 + 0 逃逸四问 + `--check`（8 例单测） |
| VFDR 更新 | **`tools/vfdr_updater_v2_624.py`** | 升级：6 轮累计 + 热力图 v2 + 盲区缩减 + `--check`（6 例单测） |

## 四、结论与动作

- **不改代码**：623 A3/A5 功能完整（以数据+测试交付），无功能缺失。
- 工具名对应关系已记录于本文件；624 已为两者补上工具化后继（v3 / v2，含 `--check`）。
- 若 625 需要统一命名，可将 `escape_root_cause_v3_624` / `vfdr_updater_v2_624` 作为规范工具名。

## 五、局限性声明

1. 623 的"工具"实为**一次性数据件**（重算需重跑沙箱以生成 run JSON），非即用 CLI；624 后继已弥补。
2. 命名历史不一致（`_v2` / `_v3` / `_v2_624`）属仓库存量，统一命名留 625。

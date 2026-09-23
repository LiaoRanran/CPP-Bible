# 631 B1 · auto 42 条 liveness 字段填充结果

- 方案来源：630 A2 方案甲（`mode == auto`）：**0 条**
- 来源独立复核：**0/0** 条通过（重推导符号一致 + 引用卡原文出现该符号）
- 填充：`--apply` 已改 **23** 张卡 / **42** 处（dry_run=False）
- 备份目录：`data/autoimmune_backup_631/`（原文件逐张留档）

## 一、填了什么（按卡汇总）

| 卡 | 填充处数 | 符号 |
|---|---|---|

## 二、来源复核（每条值的出处）

| # | 卡 / 命题 | 符号 | 引用卡 | 复核 |
|---|---|---|---|---|

## 三、填充后自身免疫率复算

- 干净卡：23 张；仍被 warn：**23** 张 ⇒ 自身免疫率 **100.0%**
- warn 规则条数：**92**（填充前 132 条）· advice 0 · block 0（硬开火率仍 0%）

### 逐卡剩余 warn 规则（Top 卡）

| 卡 | 剩余 warn 规则 |
|---|---|
| `atoms/conc/ATOM-CONC-FENCE-001.md` | 3 |
| `atoms/conc/ATOM-CONC-LOCK-001.md` | 3 |
| `atoms/conc/ATOM-CONC-RACE-001.md` | 5 |
| `atoms/hist/ATOM-HIST-AUTOPTR-001.md` | 4 |
| `atoms/mem/ATOM-MEM-ALIGN-001.md` | 4 |
| `atoms/mem/ATOM-MEM-ALLOC-001.md` | 5 |
| `atoms/mem/ATOM-MEM-LEAK-001.md` | 4 |
| `atoms/mem/ATOM-MEM-MOVE-002.md` | 4 |
| `atoms/mem/ATOM-MEM-NEW-001.md` | 4 |
| `atoms/mem/ATOM-MEM-PERF-001.md` | 3 |
| `atoms/mem/ATOM-MEM-PERF-002.md` | 3 |
| `atoms/mem/ATOM-MEM-PERF-003.md` | 5 |

### 剩余 warn 的规则分布

| 规则 | 条数 |
|---|---|
| `ATOM-CLAIM-CONCEPT-NORMALIZED` | 65 |
| `INFERENCE-NOT-MACHINE-VERIFIED` | 25 |
| `ATOM-REL-TARGET` | 2 |

## 四、诚实登记

1. **只填 `liveness`**：`object`（语义）与 `signed_by`（人签）**一条没填**（§零.3 不代签、机器不做语义判断）；
2. **写入方式是逐行最小编辑**：改前备份 + 改后用 YAML 结构比对，确认除 `liveness` 外零变化（`unexpected_diffs` 为空）；
3. 符号取自**引用卡的 artifact_assert**，与 gate 判定 `OBSERVATION-LIVENESS` 的口径一致；但「符号存在」**不等于**「该符号确为本命题的观测证据」——语义正确性仍需人复核（B2 清单的 human 项不含这些，但建议抽检）；
4. 若填充后 warn 数未下降，如实记录（见 §三 与验收报告偏差表）。

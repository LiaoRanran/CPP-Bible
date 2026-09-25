# 638 3.1 · 四态结论 schema（真上线 · 向后兼容）

> 生成时间：2026-09-25T09:30:27。工具：`tools/four_state_verdict_638.py`。

## 一、四态定义（schema）

| 态 | 含义 | 必填 | 旧态映射来源 |
|---|---|---|---|
| `pass` | 完全通过，无例外 | boundary_triple | pass, APPROVE |
| `pass_with_exception` | 通过但附例外说明（explanation 必填） | boundary_triple, explanation | pass, APPROVE |
| `fail` | 被 block/拒绝 | boundary_triple | block, REJECT, fail |
| `unknown` | 证据不足/边界缺失，无法判决 | — | — |

## 二、边界三元组强制（§3.1.3）

- 必填三字段：`mutation_set_hash`（64hex）、`mutation_count`（>0）、`generator_version`（非空）；
- **缺任一 ⇒ 降级 `unknown`**；`pass_with_exception` 另需非空 `explanation`，否则同样降级；
- 三元组**权威口径**见 `data/638_baseline.md` §1.1（当前统一值 count=1593, version=`mutation_fuzz@v7`）。

## 三、语料审计（新规则下的真实归属）

- `data/*baseline*` 报告：**37** 份，其中有边界 **34** 份；
  四态分布：`{'pass': 34, 'unknown': 3}`；
- `atoms/` verified 卡：**23** 张，其中有边界 **0** 张；
  四态分布：`{'unknown': 23}`。

### 3.1 无边界 ⇒ 降级的卡清单（真实）

| 卡 | 四态 | 有边界 |
|---|---|---|
| `atoms/conc/ATOM-CONC-FENCE-001.md` | unknown | 否 |
| `atoms/conc/ATOM-CONC-LOCK-001.md` | unknown | 否 |
| `atoms/conc/ATOM-CONC-RACE-001.md` | unknown | 否 |
| `atoms/hist/ATOM-HIST-AUTOPTR-001.md` | unknown | 否 |
| `atoms/mem/ATOM-MEM-ALIGN-001.md` | unknown | 否 |
| `atoms/mem/ATOM-MEM-ALLOC-001.md` | unknown | 否 |
| `atoms/mem/ATOM-MEM-LEAK-001.md` | unknown | 否 |
| `atoms/mem/ATOM-MEM-MOVE-002.md` | unknown | 否 |
| `atoms/mem/ATOM-MEM-NEW-001.md` | unknown | 否 |
| `atoms/mem/ATOM-MEM-PERF-001.md` | unknown | 否 |
| `atoms/mem/ATOM-MEM-PERF-002.md` | unknown | 否 |
| `atoms/mem/ATOM-MEM-PERF-003.md` | unknown | 否 |
| `atoms/mem/ATOM-MEM-RAII-001.md` | unknown | 否 |
| `atoms/mem/ATOM-MEM-RAII-002.md` | unknown | 否 |
| `atoms/mem/ATOM-MEM-RVREF-001.md` | unknown | 否 |
| `atoms/mem/ATOM-MEM-SHARED-001.md` | unknown | 否 |
| `atoms/mem/ATOM-MEM-SHARED-002.md` | unknown | 否 |
| `atoms/mem/ATOM-MEM-UNIQUE-001.md` | unknown | 否 |
| `atoms/mem/ATOM-MEM-UNIQUE-002.md` | unknown | 否 |
| `atoms/mem/ATOM-MEM-VALUE-001.md` | unknown | 否 |
| `atoms/mem/ATOM-MEM-VALUE-002.md` | unknown | 否 |
| `atoms/mem/ATOM-MEM-WEAK-001.md` | unknown | 否 |
| `atoms/ub/ATOM-UB-GRAY-001.md` | unknown | 否 |

## 四、向后兼容策略

| 项 | 策略 |
|---|---|
| 历史 452 条判决（Authority ledger） | **不重新分类**，保持 APPROVE/MODIFY 原值 |
| 历史 38 份 baseline 报告 | **不重写**，仅离线审计其四态归属 |
| 新判决 | **必须**用四态；缺边界自动 `unknown` |
| 批量迁移 | 仅提供 `migrate_plan()` **计划**（只算不写），`--migrate` 只打印，**不自动跑** |

## 五、诚实登记

1. 本工具是**新格式执行器**，不修改任何历史判决/报告（§零.1 向后兼容）；
2. 卡级判决抽取用正则（`status:`/`verdict:`/`falsification:`），**非逐条判读**；
   未识别到显式 verdict 的 verified 卡按 `pass` 处理，已在 §3.1 表逐张列出；
3. baseline 报告的边界抽取同样是正则近似（§1.1 已说明三元组不在 ledger）；
4. **实测结论**：23 张 verified 卡**全部无边界三元组** ⇒ 新规则下**全部为 `unknown`**。
   这不是缺陷，是「边界回填」欠债的量化（交人项）。

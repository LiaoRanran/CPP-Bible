# 643 D1 · 逃逸案例归因（智能层：自动提案规则 #1）

> 案例 **27** 条（B4 历史 9 + C3 新发现 18）；归因分布 `{'规则缺失': 1, '验证器能力天花板': 8, '责任错配': 11, '不可达': 7}`。
> C3 并入情况：已并入 C3 沙箱结果（20 条计划，局限样本：20）

## 一、根因 → 改进方向（机械映射）

| 根因 | 改进方向 | 条数 |
|---|---|---|
| `规则缺失` | 提新规则草案（D2） | 1 |
| `规则太弱` | 收紧条件 / 升 block（D2 出修改草案） | 0 |
| `规则冲突` | 调整优先级（人审） | 0 |
| `验证器能力天花板` | 人审（能力天花板 ⇒ 不该自动化） | 8 |
| `责任错配` | 重标 expected_oracle（不改判据） | 11 |
| `不可达` | 接 B3 退役候选（人审） | 7 |

## 二、**可行动**案例（规则缺失/太弱 ⇒ 交 D2 出草案）

共 **1** 条：

| 来源 | case_id | 目标规则 | 卡 | 算子 | 根因 | 理由 |
|---|---|---|---|---|---|---|
| B4 | `v7#0` | `—` | `evidence/conc/EV-CONC-001.md` | `M1` | **规则缺失** | 逃逸且 new_block / new_warn 均为空 ⇒ 没有任何规则对该变异有反应 |

## 三、**不可行动**案例（不该自动化）

共 **26** 条：

| 来源 | case_id | 根因 | 理由 |
|---|---|---|---|
| B4 | `v7#1` | 验证器能力天花板 | 该变异被标 equivalent（语义等价 ⇒ 本就不该报） |
| B4 | `v7#2` | 验证器能力天花板 | 该变异被标 equivalent（语义等价 ⇒ 本就不该报） |
| B4 | `v7#3` | 验证器能力天花板 | 该变异被标 equivalent（语义等价 ⇒ 本就不该报） |
| B4 | `v7#4` | 验证器能力天花板 | 该变异被标 equivalent（语义等价 ⇒ 本就不该报） |
| B4 | `v7#5` | 验证器能力天花板 | 该变异被标 equivalent（语义等价 ⇒ 本就不该报） |
| B4 | `v7#6` | 验证器能力天花板 | 该变异被标 equivalent（语义等价 ⇒ 本就不该报） |
| B4 | `v7#7` | 验证器能力天花板 | 该变异被标 equivalent（语义等价 ⇒ 本就不该报） |
| B4 | `v7#8` | 验证器能力天花板 | 该变异被标 equivalent（语义等价 ⇒ 本就不该报） |
| C3 | `ATOM-FM-REQUIRED#break_ref#1` | 责任错配 | C3 沙箱 verdict=oracle_mismatch（关系目标 EV-CONC-003 → EV-CONC-003-XX（不存在）） |
| C3 | `ATOM-FM-REQUIRED#equiv_rewrite#2` | 不可达 | C3 沙箱 verdict=not_triggered（同义改写 必须 → 应当（语义等价）） |
| C3 | `ATOM-ID-FORMAT#field_delete#0` | 责任错配 | C3 沙箱 verdict=oracle_mismatch（删除 frontmatter 字段 id） |
| C3 | `ATOM-ID-FORMAT#format_perturb#1` | 不可达 | C3 沙箱 verdict=not_triggered（注入尾随空格（格式微扰）） |
| C3 | `ATOM-ID-FORMAT#break_ref#2` | 责任错配 | C3 沙箱 verdict=oracle_mismatch（关系目标 EV-CONC-005 → EV-CONC-005-XX（不存在）） |
| C3 | `ATOM-ID-FORMAT#equiv_rewrite#3` | 不可达 | C3 沙箱 verdict=not_triggered（同义改写 必须 → 应当（语义等价）） |
| C3 | `ATOM-ID-UNIQUE#field_delete#0` | 责任错配 | C3 沙箱 verdict=oracle_mismatch（删除 frontmatter 字段 id） |
| C3 | `ATOM-ID-UNIQUE#break_ref#1` | 责任错配 | C3 沙箱 verdict=oracle_mismatch（关系目标 EV-CONC-003 → EV-CONC-003-XX（不存在）） |
| C3 | `ATOM-ID-UNIQUE#equiv_rewrite#2` | 不可达 | C3 沙箱 verdict=not_triggered（同义改写 必须 → 应当（语义等价）） |
| C3 | `ATOM-VERIFIED-BOUND#break_ref#1` | 责任错配 | C3 沙箱 verdict=oracle_mismatch（关系目标 EV-CONC-003 → EV-CONC-003-XX（不存在）） |
| C3 | `ATOM-VERIFIED-BOUND#equiv_rewrite#2` | 不可达 | C3 沙箱 verdict=not_triggered（同义改写 必须 → 应当（语义等价）） |
| C3 | `ATOM-NO-UNVERIFIED#field_delete#0` | 责任错配 | C3 沙箱 verdict=oracle_mismatch（删除 frontmatter 字段 status） |
| C3 | `ATOM-NO-UNVERIFIED#break_ref#1` | 责任错配 | C3 沙箱 verdict=oracle_mismatch（关系目标 EV-CONC-003 → EV-CONC-003-XX（不存在）） |
| C3 | `ATOM-NO-UNVERIFIED#equiv_rewrite#2` | 不可达 | C3 沙箱 verdict=not_triggered（同义改写 必须 → 应当（语义等价）） |
| C3 | `ATOM-STATUS-VALUE#field_delete#0` | 责任错配 | C3 沙箱 verdict=oracle_mismatch（删除 frontmatter 字段 status） |
| C3 | `ATOM-STATUS-VALUE#break_ref#1` | 责任错配 | C3 沙箱 verdict=oracle_mismatch（关系目标 EV-CONC-003 → EV-CONC-003-XX（不存在）） |
| C3 | `ATOM-STATUS-VALUE#equiv_rewrite#2` | 不可达 | C3 沙箱 verdict=not_triggered（同义改写 必须 → 应当（语义等价）） |
| C3 | `ATOM-STATUS-TRANSITION#field_delete#0` | 责任错配 | C3 沙箱 verdict=oracle_mismatch（删除 frontmatter 字段 status） |

## 诚实登记

1. **归因是机械映射，不是诊断**：`规则缺失/太弱` 只在「逃逸且无规则反应/只有 warn 反应」这一**行为证据**上成立；**为什么**缺/弱（条件写错？字段名不匹配？）需要人读代码；
2. **C3 并入的样本量极小**（见其 `limit`）⇒ C3 来的案例只作**线索**；若 C3 未跑，`n_from_c3=0` 并已显式登记；
3. **`责任错配` 不是缺陷**：它是「生成器的预期猜错了」（§十二.7），改进方向是**重标 oracle**，不是改规则；
4. **能力天花板类占比高（8/9）**：说明 v7 的「逃逸」多数是**语义等价**（`equivalent_invalid`）⇒ 这本身是对 B4 口径的重要修正：**「逃逸」必须看去掉等价后的口径**；
5. 本工具**只读**：不改规则、不写规则库、不跑沙箱。

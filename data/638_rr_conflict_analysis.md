# 638 B2 · RR 冲突分类（规则间冲突逐条分类）

> 生成时间：2026-09-25T09:36:44。工具：`tools/rr_conflict_classifier_638.py`。

## 一、口径说明（必须先说）

- 636 的 RR 记录**没有规则对**（`rr/er/ee/und/...`，无 `rule_a/rule_b`）——
  **RR 是全局规则集属性**（23/23 卡全为 1，区分度有限，见 636 报告诚实登记 3）；
- 因此本报告**卡级对齐 636**（23 张卡逐卡），**规则对级为本批新增**（从权威 `gate_engine.RULES` 枚举同 scope 规则对）；
- 两级的数目**不可互相换算**，已在 §五 登记。

## 二、规则对级分类（真实，可逐条处置）

- 规则数：**67**（scope 分布 `{'atom': 36, 'evidence': 24, 'repo': 7}`）；
- 同 scope 规则对（**候选**集）：**927** 对；
- 其中 **高置信**（同前缀族，真可能管同一事实）：**24** 对； **低置信**（仅同 scope，非同一事实）：**903** 对；
- 高置信类型分布：`{'type2': 14, 'type1': 6, 'type3': 4}`；
- 高置信严重度分布：`{'P2': 14, 'P0': 6, 'P1': 4}`；
- 全候选（含低置信）类型分布：`{'type4': 903, 'type2': 14, 'type1': 6, 'type3': 4}`。

> **重要**：927 对是**同 scope 机械配对**的结果——同 scope 内每条规则都与其余全部配对，
> 因此冲突度恒为「scope 内规则数 − 1」（atom 域恒 35），**本身不构成 927 个真实冲突**。
> 真正可处置的是**高置信**那一批（同前缀族）。此退化与 636「RR 为全局规则集属性、
> 区分度有限」是同一根因，已在 §五 登记。

| 类型 | 含义 | 判据（启发式） | 置信度 |
|---|---|---|---|
| `type1` | 对同一事实给出相反判断 | **同前缀族** + severity 为 block↔warn/advice | high |
| `type2` | 适用范围重叠但阈值不同 | **同前缀族** + 同 severity | high |
| `type3` | 一条规则的前提是另一条的结论 | 同族（`X` 与 `X-HC`）派生对 | high |
| `type4` | 其他不一致 | 同前缀族但 severity 组合非 block-vs-warn；或**仅同 scope**（前缀族不同） | high / low |

> 前缀族 = 规则 id 去掉最后一段（如 `ATOM-REL-TARGET` → `ATOM-REL`）。

### 2.1 top 3 最值得修的冲突

> 选法：**P0（影响判决正确性）优先**，按「两条规则各自的冲突度之和」降序，
> 且三条**互不重复 rule_a**——即给出 3 个**不同的**待修规则，而非同一规则霸榜。

| # | 规则 A（冲突度） | 规则 B（冲突度） | scope | 类型 | 严重度 | 建议处置 |
|---|---|---|---|---|---|---|
| 1 | `ATOM-REL-CONFLICT` (5) | `ATOM-REL-UNKNOWN` (5) | atom | type1 | P0 | 修规则 ATOM-REL-CONFLICT（把 block 降为 warn）或加优先级 |
| 2 | `ATOM-REL-DAG` (5) | `ATOM-REL-UNKNOWN` (5) | atom | type1 | P0 | 修规则 ATOM-REL-DAG（把 block 降为 warn）或加优先级 |
| 3 | `ATOM-REL-TARGET` (5) | `ATOM-REL-CONFLICT` (5) | atom | type1 | P0 | 修规则 ATOM-REL-TARGET（把 block 降为 warn）或加优先级 |

### 2.1.1 冲突度最高的规则（系统性问题制造者，top 10）

| 规则 | 参与冲突对数 |
|---|---|
| `ATOM-REL-TARGET` | 5 |
| `ATOM-REL-DAG` | 5 |
| `ATOM-REL-CONFLICT` | 5 |
| `ATOM-REL-UNKNOWN` | 5 |
| `ATOM-REL-TARGET-HC` | 5 |
| `ATOM-REL-UNKNOWN-HC` | 5 |
| `PED-MOTIVATION` | 2 |
| `PED-MISCONCEPTION` | 2 |
| `PED-SOCRATIC` | 2 |
| `ATOM-ID-FORMAT` | 1 |

- 单条规则最大冲突度：**5** 对。

### 2.2 高置信 P0 冲突全量（type1，同前缀族 + severity 相反）

共 **6** 对：

| 规则 A | 规则 B | scope | 为什么 |
|---|---|---|---|
| `ATOM-REL-TARGET` | `ATOM-REL-DAG` | atom | 同前缀族 `ATOM-REL` 下 `ATOM-REL-TARGET`(warn) 与 `ATOM-REL-DAG`(block) 对同一事实处置相反 |
| `ATOM-REL-TARGET` | `ATOM-REL-CONFLICT` | atom | 同前缀族 `ATOM-REL` 下 `ATOM-REL-TARGET`(warn) 与 `ATOM-REL-CONFLICT`(block) 对同一事实处置相反 |
| `ATOM-REL-TARGET` | `ATOM-REL-UNKNOWN-HC` | atom | 同前缀族 `ATOM-REL` 下 `ATOM-REL-TARGET`(warn) 与 `ATOM-REL-UNKNOWN-HC`(block) 对同一事实处置相反 |
| `ATOM-REL-DAG` | `ATOM-REL-UNKNOWN` | atom | 同前缀族 `ATOM-REL` 下 `ATOM-REL-DAG`(block) 与 `ATOM-REL-UNKNOWN`(warn) 对同一事实处置相反 |
| `ATOM-REL-CONFLICT` | `ATOM-REL-UNKNOWN` | atom | 同前缀族 `ATOM-REL` 下 `ATOM-REL-CONFLICT`(block) 与 `ATOM-REL-UNKNOWN`(warn) 对同一事实处置相反 |
| `ATOM-REL-UNKNOWN` | `ATOM-REL-TARGET-HC` | atom | 同前缀族 `ATOM-REL` 下 `ATOM-REL-UNKNOWN`(warn) 与 `ATOM-REL-TARGET-HC`(block) 对同一事实处置相反 |

### 2.3 type3 同族派生对全量

| 基规则 | 派生规则 | scope | 建议 |
|---|---|---|---|
| `ATOM-REL-TARGET` | `ATOM-REL-TARGET-HC` | atom | 加优先级（基规则先判，派生规则仅在基规则通过时生效） |
| `ATOM-REL-UNKNOWN` | `ATOM-REL-UNKNOWN-HC` | atom | 加优先级（基规则先判，派生规则仅在基规则通过时生效） |
| `EV-SERVES-EXIST` | `EV-SERVES-EXIST-HC` | evidence | 加优先级（基规则先判，派生规则仅在基规则通过时生效） |
| `CARD-PATH-NOT-CANONICAL` | `CARD-PATH-NOT-CANONICAL-HC` | repo | 加优先级（基规则先判，派生规则仅在基规则通过时生效） |

## 三、卡级分类（对齐 636：23 张 verified 卡）

- 卡数：**23**；类型分布：`{'type2': 21, 'type1': 2}`。

| 卡 | 冲突型 | C | 超阈值 | 本批类型 | 严重度 | 建议 |
|---|---|---|---|---|---|---|
| `ATOM-CONC-FENCE-001` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-CONC-LOCK-001` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-CONC-RACE-001` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-HIST-AUTOPTR-001` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-MEM-ALIGN-001` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-MEM-ALLOC-001` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-MEM-LEAK-001` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-MEM-MOVE-002` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-MEM-NEW-001` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-MEM-PERF-001` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-MEM-PERF-002` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-MEM-PERF-003` | RR/EE | 1.333 | 是 | type1 | P0 | 人工复核该卡的 RR+cross 证据（C≥0.3） |
| `ATOM-MEM-RAII-001` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-MEM-RAII-002` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-MEM-RVREF-001` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-MEM-SHARED-001` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-MEM-SHARED-002` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-MEM-UNIQUE-001` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-MEM-UNIQUE-002` | RR/EE | 0.5 | 是 | type1 | P0 | 人工复核该卡的 RR+cross 证据（C≥0.3） |
| `ATOM-MEM-VALUE-001` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-MEM-VALUE-002` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-MEM-WEAK-001` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |
| `ATOM-UB-GRAY-001` | RR | 0.0 | — | type2 | P1 | 记录 RR，待规则优先级策略上线后自动消解 |

## 四、统计汇总

| 维度 | 值 |
|---|---|
| 规则数 | 67 |
| 同 scope 规则对（候选集） | 927 |
| 高置信（同前缀族） / 低置信（仅同 scope） | 24 / 903 |
| **高置信** type1 / type2 / type3 / type4 | 6 / 14 / 4 / 0 |
| **高置信** P0 / P1 / P2 | 6 / 4 / 14 |
| verified 卡（逐卡分类） | 23 |

## 五、诚实登记

1. **分类是启发式**：判据是 scope/severity/命名族三个**结构性字段**，未做语义分析（§四.3）；
2. **口径差异**：636 的「23 张卡全有 RR」是**卡级**计数；本批的规则对级枚举共 927 对候选，其中**只有 24 对是高置信**（同前缀族），其余 903 对仅是「同 scope」的低置信同域对。**三者不可换算**；
3. **RR 全局属性**的根因未解决（636 已指出区分度有限）——本批只是把「全局的 1」拆成可处置的规则对，**未改规则**；
4. type3 判据依赖 `-HC` 后缀约定（实测 4 对：ATOM-REL-TARGET / EV-SERVES-EXIST / ATOM-REL-UNKNOWN / CARD-PATH-NOT-CANONICAL 各有 `-HC` 变体）；
5. 本批**不改任何规则**，仅分类 + 给建议（§零：判决逻辑不在本批改动范围）。

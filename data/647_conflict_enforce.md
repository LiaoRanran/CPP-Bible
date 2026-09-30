# 647 B1 · 冲突检测器**真上岗**（高置信 block / 中置信 warn / 低置信 pass）

- 当前模式：**enforce**（`QUEYI_PROTECTOR_MODE`；shadow = 一键回滚）
- 阈值：block ≥ **0.8**（且双方有证据）· warn ≥ **0.5** · 其余 pass

## 一、三档口径

| 条件 | 动作 | enforce 后果 |
|---|---|---|
| C ≥ 0.8 且双方都有证据 | **block** | 内核态**强制改判 `fail`** + 原因 |
| 0.5 ≤ C < 0.8 | warn | 只加标记，交人审 |
| C < 0.5 | pass | 通过（无标记） |

**「双方都有证据」**：卡侧引用 ≥1 条证据 **且** 检测器报出 ER/EE/欠定之一（**RR 不算** —— 它是全局规则集属性，会把 23/23 全打成高置信）。

## 二、对**新判决面**实跑（真实 verified 卡，当作新判决；**不回溯历史**）

- 判决数：**23**；动作分布 `{'pass': 21, 'block': 1, 'warn': 1}`
- **被 block：1**；判决态被改变：**1**

### 2.1 ⚠️ 真实卡上的实际拦截（**生产影响，必须看**）

- 实测：C ≥ 0.8 且双方有证据的卡 **1 张**，**判决态被改变 1 条** ⇒ **enforce 下这些卡会被真的改判为 `fail`**（不是纸面推演）。

| 卡 | 动作 | C | 型 | 双方证据 | 判决态被改变 |
|---|---|---|---|---|---|
| `ATOM-MEM-PERF-003` | **block** | 1.333 | RR/EE | True | ⚠️ 是 |
| `ATOM-MEM-UNIQUE-002` | **warn** | 0.5 | RR/EE | True | 否 |

- **EE 型由「≥2 条引用且有悬挂」推出 ⇒ 可能是误判**（证据 id 与证据文件名口径不一致会造假悬挂）——本批**未**逐一核实该卡是否真悬挂引用；
- 若判定为误拦：`QUEYI_PROTECTOR_MODE=shadow` 立即回滚（只标记不改判）。

### 2.2 合成卡三档边界验证

### 2.2 合成卡三档边界验证

| 用例 | 期望 | 实测 | C | 双方有证据 | 型 | 通过 |
|---|---|---|---|---|---|---|
| 高置信（C=1.0：欠定 + 悬挂引用 + 反证） | block | **block** | 3.0 | True | RR/ER/EE | ✅ |
| 中置信（C≈0.5：唯一悬挂引用 + 有证据） | warn | **warn** | 1.0 | False | RR | ✅ |
| 低置信（C=0：证据全在 + 无反证） | pass | **pass** | 0.0 | False | RR | ✅ |

## 三、逐卡明细

| 卡 | 动作 | C | 型 | 双方证据 | 判决态改变 |
|---|---|---|---|---|---|
| `ATOM-CONC-FENCE-001` | pass | 0.0 | RR | False | 否 |
| `ATOM-CONC-LOCK-001` | pass | 0.0 | RR | False | 否 |
| `ATOM-CONC-RACE-001` | pass | 0.0 | RR | False | 否 |
| `ATOM-HIST-AUTOPTR-001` | pass | 0.0 | RR | False | 否 |
| `ATOM-MEM-ALIGN-001` | pass | 0.0 | RR | False | 否 |
| `ATOM-MEM-ALLOC-001` | pass | 0.0 | RR | False | 否 |
| `ATOM-MEM-LEAK-001` | pass | 0.0 | RR | False | 否 |
| `ATOM-MEM-MOVE-002` | pass | 0.0 | RR | False | 否 |
| `ATOM-MEM-NEW-001` | pass | 0.0 | RR | False | 否 |
| `ATOM-MEM-PERF-001` | pass | 0.0 | RR | False | 否 |
| `ATOM-MEM-PERF-002` | pass | 0.0 | RR | False | 否 |
| `ATOM-MEM-PERF-003` | block | 1.333 | RR/EE | True | ⚠️ 是 |
| `ATOM-MEM-RAII-001` | pass | 0.0 | RR | False | 否 |
| `ATOM-MEM-RAII-002` | pass | 0.0 | RR | False | 否 |
| `ATOM-MEM-RVREF-001` | pass | 0.0 | RR | False | 否 |
| `ATOM-MEM-SHARED-001` | pass | 0.0 | RR | False | 否 |
| `ATOM-MEM-SHARED-002` | pass | 0.0 | RR | False | 否 |
| `ATOM-MEM-UNIQUE-001` | pass | 0.0 | RR | False | 否 |
| `ATOM-MEM-UNIQUE-002` | warn | 0.5 | RR/EE | True | 否 |
| `ATOM-MEM-VALUE-001` | pass | 0.0 | RR | False | 否 |
| `ATOM-MEM-VALUE-002` | pass | 0.0 | RR | False | 否 |
| `ATOM-MEM-WEAK-001` | pass | 0.0 | RR | False | 否 |
| `ATOM-UB-GRAY-001` | pass | 0.0 | RR | False | 否 |

## 四、误判风险评估 + 回滚方案

| 风险 | 触发条件 | 回滚动作 |
|---|---|---|
| θ_block=0.8/θ_warn=0.5 是**设计值**，未用真实样本回填 ⇒ 可能误拦/漏拦 | block 清单里出现人工确认无冲突的卡 | `QUEYI_PROTECTOR_MODE=shadow` 一键退回只标记；或调 THETA_BLOCK 常量后重跑 |
| **block 会真的改判**（内核态 → fail），不再是「只标记」 | 误拦导致正确判决被写成 fail | shadow 模式 + 本模块不改任何历史/账本（只处理调用方递进来的新判决） |
| RR 被排除出「双方证据」口径，可能低估冲突 | 只报 RR 的卡未被拦 | 把 `er/ee/und` 扩到含 `rr` 即回到「全拦」（对比实验用，不建议生产） |
| 占位新判决（verified ⇒ pass）不是真实 gate 判决 | 有人把本模块输出当成生产判决源 | 判决唯一来源仍是 gate_engine；本模块只在 gate 之后做**附加保护** |

## 诚实登记

1. **θ 是设计值**，未用真实样本回填（交人项）；
2. **真实卡上确有高置信样本**（`ATOM-MEM-PERF-003`，C=1.333）⇒ enforce 下**真会被改判 fail**；另有 1 张落 warn 档；EE 型可能是**假悬挂** ⇒ 需人工核实（**不夸大也不隐瞒**）；
3. **block 真的改判**（→ `fail`）——这是 647 与 642 的本质差别，也是本批最大风险；
4. **历史不回溯**：本模块只处理调用方递进来的**新判决**，不重扫、不改账本；
5. `agreement` 仍是「被引用证据存在率」**启发式**（636 同口径），非统计一致度。

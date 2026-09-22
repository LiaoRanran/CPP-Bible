# 624 A4 · 闭环第五轮（针对性跨卡 mutation，策略 X5–X8）

> 工具：`tools/round5_mutator_624.py`（复用 A1 多卡沙箱 `cross_card_attack_624.CrossCardSandbox`）
> 输入：`data/adversarial_loop_round5_624.json`（40 条）× 真跑 gate
> 耗时：**112.9s**

---

## 一、第五轮判决结果（40 条）

| 判决 | 条数 |
|---|---|
| **blocked** | **40** |
| detected_nonblock | 0 |
| neutral | 0 |
| **escaped** | **0** |
| infra_error | 0 |

**40/40 全部被 block，0 逃逸。**

按策略（各 10 条，全部 blocked）：
| 策略 | 目标规则 | 结果 |
|---|---|---|
| X5 幽灵证据引用 | S2-EVIDENCE-VERDICT | ✅ 触达 |
| X6 观测断链 | OBSERVATION-NEEDS-ARTIFACT | ✅ 触达 |
| X7 误解引用孤儿（嵌套 pedagogy.misconceptions） | ATOM-MISCONCEPTION-REF | ✅ 触达（修正 A2 X4 的字段误用） |
| X8 verified 未绑定（删 first_hand） | ATOM-VERIFIED-BOUND | ✅ 触达 |

**预测命中 4/4（100%）** —— A3 的改进建议（针对嵌套字段/证据绑定/命题闭环/verified 绑定）精准有效。

## 二、本轮触达规则与累计

- 本轮触达 5 条：`ATOM-FM-REQUIRED` · **ATOM-MISCONCEPTION-REF** · **ATOM-VERIFIED-BOUND** ·
  **OBSERVATION-NEEDS-ARTIFACT** · **S2-EVIDENCE-VERDICT**（后 4 条为 623 盲区）。

## 三、六轮对比与累计触达（核心压力指标）

| 轮次 | 载体 | 条数 | blocked | nonblock | escaped | 本轮新触达 |
|---|---|---|---|---|---|---|
| R1（620，v7 既有） | 单卡 field-edit | 1406 | — | — | 1 | 9 |
| R2（622 A2） | 单卡 | 50 | 13 | 0 | 0 | — |
| R3（623 A2） | 单卡高复杂度 | 80 | 46 | 16 | 4* | 16（→累计25） |
| R4（623 A4） | 单卡定向 | 40 | 12 | 14 | 0 | 1（→累计26） |
| **R5（624 A2）** | **跨卡** | 60 | 47 | 13 | 0 | **2**（→累计28） |
| **R6（624 A4）** | **跨卡定向** | 40 | 40 | 0 | 0 | **4**（→累计32） |

\* R3 的 4 条 escaped 经 A3 证实为删字段假象。

| 口径 | 623 | **624（六轮）** | 目标 |
|---|---|---|---|
| **累计触达规则** | 26/63（41.3%） | **32/63（50.8%）** | >45/63 |
| 盲区 | 37 | **31** | <25 |
| 新增（相对 623） | — | **6**：ATOM-REL-CONFLICT · EV-ARTIFACT-FILE-EXISTS · ATOM-MISCONCEPTION-REF · ATOM-VERIFIED-BOUND · OBSERVATION-NEEDS-ARTIFACT · S2-EVIDENCE-VERDICT | — |

> **诚实登记**：A2 目标 >40、A4 六轮目标 >45、盲区 <25 **均未达标**（实测 32/63、盲区 31）。
> 跨卡攻击确实突破了「多卡构造」类的 6 条盲区（+23% 相对增幅），但仍受限于
> `gate_engine` 无编译/复算/git/词表类规则的可构造性（剩余 31 条盲区中，约 16 条需编译/复算产物、
> 2 条需 git 历史、7 条为 advice 级、其余为词表黑盒）。

## 四、累计新逃逸

**0 条**（R5+R6 共 100 条跨卡攻击，无基线 finding 消失）。

## 五、VFDR

- R5 检测率 = (47+13)/60 = **100%**（无 neutral，全部新检出）；R6 = **100%**。
- **危险逃逸（dangerous）全程 0**。

## 六、局限性声明

1. **X5–X8 各 10 条全部命中**，但**策略目标单一**（每策略只打一条规则）⇒ 新增 4 条属"精准打击"而非"广度覆盖"。
2. **剩余 31 条盲区**多需编译/复算/git/词表载体，跨卡 sandbox 亦不可达 ⇒ 载体天花板未完全突破。
3. 判决只含 gate（规则层），不含 replay 复算层。
4. 复杂度评分仍为代理值。

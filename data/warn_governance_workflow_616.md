# 616 C1 · warn 治理完整工作流（分类→观察期→采纳建议→到期提醒→重评估）

> **只做分类、跟踪、建议和提醒；不自动采纳/删除任何 warn。所有采纳/删除决策需人审授权。**

## 一、工作流设计

1. **分类**：五桶（new / observation / considerable / adopted_legacy / expired_reassess）；
2. **观察期跟踪**：记录每条 warn 首次出现批次；观察期 3 批；
3. **采纳建议**：对 `considerable` 生成建议（不自动采纳）；
4. **到期提醒**：对 `expired_reassess`（采纳满 10 批）生成重评估提醒（不自动删除）。

## 二、当前状态（五桶）

| 桶 | 规则数 |
|---|---|
| new | 0 |
| observation | 2 |
| considerable | 1 |
| adopted_legacy | 4 |
| expired_reassess | 2 |
| warn 总数 | 186 |

### 逐规则观察期

| 规则 | 首次批次 | 已历批次 | 桶 |
|---|---|---|---|
| `ATOM-CLAIM-CONCEPT-NORMALIZED` | 19 | 1 | adopted_legacy |
| `ATOM-REL-TARGET` | 1 | 19 | expired_reassess |
| `EV-ASSERT-SYMBOL-MAPPED` | 19 | 1 | observation |
| `EV-FALSIFICATION-QUANT` | 14 | 6 | considerable |
| `EV-MATRIX-UNBACKED` | 19 | 1 | adopted_legacy |
| `EV-OUT-UNDECLARED-KEY` | 19 | 1 | observation |
| `EV-SERVES-EXIST` | 0 | 20 | expired_reassess |
| `INFERENCE-NOT-MACHINE-VERIFIED` | 19 | 1 | adopted_legacy |
| `OBSERVATION-LIVENESS` | 20 | 0 | adopted_legacy |

## 三、采纳建议（交人审，**不自动执行**）

- `EV-FALSIFICATION-QUANT`（已历 6 批）：可考虑采纳为 legacy（须人审授权 + 显式 acceptance 记录）

## 四、到期重评估清单（交人审，**不自动执行**）

- `ATOM-REL-TARGET`（已历 19 批）：已到期，须重评估：继续豁免(续期+10) / 修规则后撤销 / 人审裁决
- `EV-SERVES-EXIST`（已历 20 批）：已到期，须重评估：继续豁免(续期+10) / 修规则后撤销 / 人审裁决

> **重要声明**：本工作流**只做分类、跟踪、建议和提醒**，**不自动采纳/删除任何 warn**。所有采纳/删除决策需要**人审授权**。



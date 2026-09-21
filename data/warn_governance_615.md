# 615 C1 · warn 治理（不增锁机制）

> **只分类与提醒**；不自动修改 golden 基线、不自动采纳/删除任何 warn。不重跑 gate --check（615 铁律）。

## 一、现状

- `golden_state.warn_findings` = **186**（standing baseline）；已分类规则 **9** 条。

## 二、warn 分类（五桶）

| 桶 | 规则数 |
|---|---|
| 新出现 new | 0 |
| 观察期中 observation | 2 |
| 可考虑采纳 considerable | 1 |
| 已采纳legacy adopted_legacy | 4 |
| 已到期需重评估 expired_reassess | 2 |

### 逐规则

| 规则 | 桶 |
|---|---|
| `ATOM-CLAIM-CONCEPT-NORMALIZED` | adopted_legacy |
| `ATOM-REL-TARGET` | expired_reassess |
| `EV-ASSERT-SYMBOL-MAPPED` | observation |
| `EV-FALSIFICATION-QUANT` | considerable |
| `EV-MATRIX-UNBACKED` | adopted_legacy |
| `EV-OUT-UNDECLARED-KEY` | observation |
| `EV-SERVES-EXIST` | expired_reassess |
| `INFERENCE-NOT-MACHINE-VERIFIED` | adopted_legacy |
| `OBSERVATION-LIVENESS` | adopted_legacy |

## 三、不增锁机制设计

1. **新出现的 warn 不自动进入 golden 基线**（永不自动采纳）；
2. warn 须经**观察期 3 个批次**才可被**考虑**采纳为 legacy；
3. 采纳为 legacy 必须**显式人审授权**（`accepted[]` 留痕），**不自动采纳**；
4. 已采纳 legacy 有**到期日**（10 个批次后**重新评估**，见 `expired_reassess`）。

### 参数与理由

- `OBSERVATION_BATCHES = 3`：3 批足以观察「新 warn 是否自愈」（历史多为例行漂移）；
- `EXPIRY_BATCHES = 10`：10 批后强制重评估，防 legacy 永久沉淀（Goodhart）。

## 四、warn 趋势（metrics.jsonl）

| 时间 | warn 数 |
|---|---|
| 2026-09-14T21:18:07 | 31 |
| 2026-09-14T21:19:53 | 31 |
| 2026-09-14T21:30:35 | 31 |
| 2026-09-17T17:40:45 | 136 |
| 2026-09-19T16:18:50 | 186 |
| 2026-09-19T16:30:51 | 186 |
| 2026-09-19T19:17:51 | 186 |
| 2026-09-19T21:25:28 | 186 |
| 2026-09-19T22:04:51 | 186 |
| 2026-09-20T16:00:07 | 186 |
| 2026-09-20T18:39:00 | 186 |

> **重要声明**：本机制只做分类和提醒，**不自动修改 golden 基线**，**不自动采纳或删除任何 warn**；采纳/解冻均需人审授权。



# 642 A4 · 校准追踪器上岗（规则错误率自动累积；初值为**全库代理**）

## 一、全库代理重建（可复算性已标注）

| 代理 | 值 | 分子/分母 | 可复算 | 来源 |
|---|---|---|---|---|
| ledger_modify_rate | **0.1881** | 85/452 | ✅ | data/authority/decision_event_v2_ledger.jsonl |
| human_modify_rate | **0.0876** | 34/388 | ✅ | data/human_attack_edge_annotations.jsonl |
| escape_rate | **0.0007** | 1/1406 | ⛔ 冻结契约 | 616 v7 契约（可判分母 1406，本工具不复算） |

## 二、67 规则 known_error_rate 初值（**全部为代理**）

- 规则总数：**67**；有自身样本：**0**；用代理：**67**
- 代理值 = 0.1881（ledger 改判率 85/452）

| 规则 | total | error | known_error_rate | 是代理 | 代理来源 |
|---|---|---|---|---|---|
| `ATOM-FM-REQUIRED` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-ID-FORMAT` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-ID-UNIQUE` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-VERIFIED-BOUND` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-NO-UNVERIFIED` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-STATUS-VALUE` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-STATUS-TRANSITION` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-DAL-MATCH` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-REL-TARGET` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-REL-DAG` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-REL-CONFLICT` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-SUPERIORITY-WORDS` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-FM-REQUIRED` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-ID-UNIQUE` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-FALSIFICATION` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-MATRIX` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-GRAY-ZONE` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-MISCONCEPTION-LEVELS` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `MIS-LIBRARY` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-MISCONCEPTION-REF` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-AUDIENCE` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-PREREQ-READABLE` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-SERVES-EXIST` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `DOC-ZERO-PLACEHOLDER` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `META-MANIFEST` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `S1-AUTHOR-SELF-VERIFY` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `S1-GIT-AUTHOR-BINDING` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-VERIFY-REASON` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-ARTIFACT-VERSION-MATCH` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `S2-EVIDENCE-VERDICT` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `S3-EXPECTED-HARDCODED` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-SELF-SATISFIED-ASSERT` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-FALSIFICATION-QUANT` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-TRIVIAL-OBSERVATION` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-MATRIX-UNBACKED` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-ZERO-DIAG-WERROR` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-WERROR-DECL-BIND` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-ASSERT-COUNT-BELOW-BASELINE` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-OUT-UNDECLARED-KEY` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-RUN-KEY-DECLARED-EXISTS` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-ASSERT-SYMBOL-MAPPED` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-ARTIFACT-PRODUCER` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-ARTIFACT-FILE-EXISTS` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-MSCV-NO-VERIFY` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-FM-DUP-KEY` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-FM-YAML-HARDENING` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-ENV-DEPENDENT-KEY` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-REL-UNKNOWN` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-CLAIM-STRUCTURED` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `OBSERVATION-NEEDS-ARTIFACT` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `INFERENCE-NOT-MACHINE-VERIFIED` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-CLAIM-CONCEPT-NORMALIZED` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `OBSERVATION-LIVENESS` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-FIXTURE-NO-ECHO-DATA` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-OUT-STALE-MTIME` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `CARD-PATH-NOT-CANONICAL` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `EV-SERVES-EXIST-HC` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-REL-TARGET-HC` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `ATOM-REL-UNKNOWN-HC` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `CARD-PATH-NOT-CANONICAL-HC` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `PED-MOTIVATION` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `PED-MISCONCEPTION` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `PED-SOCRATIC` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `PED-PREDICT-FIRST` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `LLM-SUPERIORITY-QUALITY` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `HYBRID-TEACHING-DEPTH` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |
| `HUMAN-GOLDEN-REVIEW` | 0 | 0 | 0.1881 | ⚠️ 是 | 全库代理：ledger 改判率（MODIFY/总数） |

## 三、新判决累积演示（3 条，其中 1 条被推翻）

| seq | decision_id | 结果 | 命中规则 | 已推翻 |
|---|---|---|---|---|
| 1 | NEW-001 | APPROVE | `ATOM-FM-REQUIRED`,`ATOM-ID-FORMAT` | ✅ |
| 2 | NEW-002 | APPROVE | `ATOM-FM-REQUIRED`,`ATOM-ID-FORMAT` | — |

- `ATOM-FM-REQUIRED`：total=2，error=1，`known_error_rate=0.5`（**自身样本 2 条**，已不再是代理）;
- 首次命中记录：`{"seq": 1, "decision_id": "NEW-001", "result": "APPROVE", "rule_ids": ["ATOM-FM-REQUIRED", "ATOM-ID-FORMAT"], "overturned": true}`

## 四、ECE 三级降级格式（**只提供格式，不启用**）

- 每验证器：`ECE = Σ_b (n_b/N) × |acc(b) − conf(b)|（b 为置信分桶）`
- 分域：['简单', '中等', '复杂']
- 启用：**False**（本批不改判决）

| 级别 | 阈值 | 动作 |
|---|---|---|
| L1 重校准(ECE>0.10) | — | 重校准置信映射 |
| L2 禁言(ECE>0.20) | — | 该验证器不单独判 block |
| L3 降级(ECE>0.30) | — | 降级为 advice |

## 五、误判风险评估 + 回滚方案

| 风险 | 触发条件 | 回滚动作 |
|---|---|---|
| 代理初值被当成实测值使用（最危险） | 有人引用 `known_error_rate` 而忽略 `is_proxy=True` | 每个值都带 `is_proxy` 字段 + 报告显式标注；对接方必须判 `is_proxy` 再决定是否采信 |
| 「未被推翻」被当成「没错」（短窗口必然全未推翻） | 用 `known_error_rate=0` 推断规则无错 | 只统计 `total_count`，**不把 0 当作证据**；报告登记「未推翻 ≠ 证明无误」 |
| 「命中规则」缺失（ledger 无 rule_id）⇒ 归入 `__unattributed__` | 未归属桶计数远超已归属桶 | 不改判定；把未归属量作为**数据缺口指标**上报（信号而非噪声） |

## 诚实登记

1. **初值不是精确值**（§十.2）：历史无规则归属字段（638 实证）⇒ 67/67 用的是**全库代理**，逐条 `is_proxy=True`；
2. **逃逸率代理不可复算**（分母 1406 是 616 v7 契约，无单一数据文件）⇒ 标为冻结上下文；
3. **「未推翻」≠「没错」**：短窗口内必然全部未推翻，只涨 `total_count`，不得把 `known_error_rate=0` 当作证据；
4. 日志 **append-only**：`record()` 只追加，`overturn()` 只回标 `overturned` 字段（不改数值、不删条目）；
5. **不改任何判决**、不启用任何降级动作；本模块只记账，是否按错误率调整规则由人裁决。

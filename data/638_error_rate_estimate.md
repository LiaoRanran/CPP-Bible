# 638 B1 · known_error_rate 估算（67 条规则）

> 生成时间：2026-09-25T09:32:27。工具：`tools/error_rate_collector_638.py`。

## 一、估算方法（三层，绝不编造）

| 层级 | 样本来源 | 本批实测结果 |
|---|---|---|
| `rule` | ledger 中可归属到该规则的判决 | **0** 条（ledger 无规则字段） |
| `scope` | 同 scope 共享样本 | 0（target_type 全为 `edge`，与 scope 不可映射） |
| `global` | 全库代理（非规则级） | 见 §三 |

- 样本 ≥30 ⇒ 直接算频率；<30 且 >0 ⇒ 「样本不足」+ 先验；**=0 ⇒ 「无数据」，不给估算值**；
- 先验值（参考列）：`0.05`。

## 二、逐规则估算（67 条）

| # | 规则 | severity | scope | 假阳性率 | 假阴性率 | 样本量 | 置信度 | 层级 |
|---|---|---|---|---|---|---|---|---|
| 1 | `ATOM-FM-REQUIRED` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 2 | `ATOM-ID-FORMAT` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 3 | `ATOM-ID-UNIQUE` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 4 | `ATOM-VERIFIED-BOUND` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 5 | `ATOM-NO-UNVERIFIED` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 6 | `ATOM-STATUS-VALUE` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 7 | `ATOM-STATUS-TRANSITION` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 8 | `ATOM-DAL-MATCH` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 9 | `ATOM-REL-TARGET` | warn | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 10 | `ATOM-REL-DAG` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 11 | `ATOM-REL-CONFLICT` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 12 | `ATOM-SUPERIORITY-WORDS` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 13 | `EV-FM-REQUIRED` | block | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 14 | `EV-ID-UNIQUE` | block | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 15 | `EV-FALSIFICATION` | block | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 16 | `EV-MATRIX` | block | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 17 | `ATOM-GRAY-ZONE` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 18 | `ATOM-MISCONCEPTION-LEVELS` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 19 | `MIS-LIBRARY` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 20 | `ATOM-MISCONCEPTION-REF` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 21 | `ATOM-AUDIENCE` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 22 | `ATOM-PREREQ-READABLE` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 23 | `EV-SERVES-EXIST` | warn | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 24 | `DOC-ZERO-PLACEHOLDER` | block | repo | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 25 | `META-MANIFEST` | warn | repo | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 26 | `S1-AUTHOR-SELF-VERIFY` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 27 | `S1-GIT-AUTHOR-BINDING` | warn | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 28 | `ATOM-VERIFY-REASON` | warn | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 29 | `EV-ARTIFACT-VERSION-MATCH` | block | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 30 | `S2-EVIDENCE-VERDICT` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 31 | `S3-EXPECTED-HARDCODED` | block | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 32 | `EV-SELF-SATISFIED-ASSERT` | warn | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 33 | `EV-FALSIFICATION-QUANT` | warn | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 34 | `EV-TRIVIAL-OBSERVATION` | warn | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 35 | `EV-MATRIX-UNBACKED` | warn | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 36 | `EV-ZERO-DIAG-WERROR` | block | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 37 | `EV-WERROR-DECL-BIND` | block | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 38 | `EV-ASSERT-COUNT-BELOW-BASELINE` | block | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 39 | `EV-OUT-UNDECLARED-KEY` | warn | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 40 | `EV-RUN-KEY-DECLARED-EXISTS` | block | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 41 | `EV-ASSERT-SYMBOL-MAPPED` | block | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 42 | `EV-ARTIFACT-PRODUCER` | block | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 43 | `EV-ARTIFACT-FILE-EXISTS` | block | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 44 | `EV-MSCV-NO-VERIFY` | block | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 45 | `EV-FM-DUP-KEY` | block | repo | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 46 | `EV-FM-YAML-HARDENING` | block | repo | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 47 | `EV-ENV-DEPENDENT-KEY` | block | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 48 | `ATOM-REL-UNKNOWN` | warn | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 49 | `ATOM-CLAIM-STRUCTURED` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 50 | `OBSERVATION-NEEDS-ARTIFACT` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 51 | `INFERENCE-NOT-MACHINE-VERIFIED` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 52 | `ATOM-CLAIM-CONCEPT-NORMALIZED` | warn | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 53 | `OBSERVATION-LIVENESS` | warn | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 54 | `EV-FIXTURE-NO-ECHO-DATA` | warn | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 55 | `EV-OUT-STALE-MTIME` | warn | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 56 | `CARD-PATH-NOT-CANONICAL` | warn | repo | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 57 | `EV-SERVES-EXIST-HC` | block | evidence | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 58 | `ATOM-REL-TARGET-HC` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 59 | `ATOM-REL-UNKNOWN-HC` | block | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 60 | `CARD-PATH-NOT-CANONICAL-HC` | block | repo | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 61 | `PED-MOTIVATION` | advice | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 62 | `PED-MISCONCEPTION` | advice | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 63 | `PED-SOCRATIC` | advice | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 64 | `PED-PREDICT-FIRST` | advice | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 65 | `LLM-SUPERIORITY-QUALITY` | advice | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 66 | `HYBRID-TEACHING-DEPTH` | advice | atom | 无数据 | 无数据 | 0 | 无数据 | 无数据 |
| 67 | `HUMAN-GOLDEN-REVIEW` | advice | repo | 无数据 | 无数据 | 0 | 无数据 | 无数据 |

## 三、全库代理指标（真实数字，**非规则级**）

| 指标 | 值 | 口径 |
|---|---|---|
| ledger 判决总数 | 452 | `decision_event_v2_ledger.jsonl` |
| APPROVE / MODIFY / REJECT | 367 / 85 / 0 | 同上（**无 REJECT**） |
| 假阳性代理（ledger 改判率） | 0.1881 | MODIFY / 总数 |
| 假阳性代理（人审改判率） | 0.0876 | 34 / 388（human_attack_edge_annotations） |
| 假阴性代理（逃逸率） | 0.0007 | 1 / 1406（known_tce.jsonl） |

> 代理值**不能**下推到单条规则，只作为「全库错误率量级」的参照。

## 四、样本不足 / 无数据清单（透明）

- **无数据**规则：**67 / 67** 条；
- 层级分布：`{'无数据': 67}`；
- scope 分布：`{'atom': 36, 'evidence': 24, 'repo': 7}`。

### 4.1 为什么 67 条全部「无数据」（根因）

1. Authority ledger 的 26 字段里**没有规则 id**（实测候选字段 `['rule_id', 'rule', 'rule_ref', 'gate_rule']` 全部不存在）；
2. ledger 的 `target_type` **452/452 全为 `edge`**，与规则 `scope`（atom/evidence/repo）不可映射；
3. 因此**任何**规则都取不到「该规则判错」的样本 ⇒ 按 §三.B1.3 一律标「无数据」，
   **不编造数字**（636 的 `calibration_tracker_636` 结论一致）。

## 五、诚实登记

1. **0 条真实规则级估算值**：67/67 标「无数据」——本批没有产出任何一条规则错误率，
   这是数据缺口，不是实现缺陷；
2. 先验 5% 仅作**参考列**，不冒充实测（`fp_rate=None`）；
3. 代理指标（18.8% / 8.76% / 0.071%）是**全库级**，误当规则级使用会失真；
4. 本批**未回填** `calibration_tracker` 的 known_error_rate 字段（交人项）。

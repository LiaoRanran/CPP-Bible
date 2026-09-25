# 636 2.4 · 校准追踪器报告模式 + known_error_rate 回填

## 一、67 规则 known_error_rate 清单

- 有数据：**0**；**无数据：67**（不编造）；
- 进观察态（缺失 known_error_rate）：**67**

| 规则 | known_error_rate | 状态 | VFDR 覆盖 |
|---|---|---|---|
| `ATOM-FM-REQUIRED` | **无数据** | 无数据 | ✅ |
| `ATOM-ID-FORMAT` | **无数据** | 无数据 | ✅ |
| `ATOM-ID-UNIQUE` | **无数据** | 无数据 | ✅ |
| `ATOM-VERIFIED-BOUND` | **无数据** | 无数据 | ✅ |
| `ATOM-NO-UNVERIFIED` | **无数据** | 无数据 | ✅ |
| `ATOM-STATUS-VALUE` | **无数据** | 无数据 | ✅ |
| `ATOM-STATUS-TRANSITION` | **无数据** | 无数据 | ✅ |
| `ATOM-DAL-MATCH` | **无数据** | 无数据 | ✅ |
| `ATOM-REL-TARGET` | **无数据** | 无数据 | ✅ |
| `ATOM-REL-DAG` | **无数据** | 无数据 | ✅ |
| `ATOM-REL-CONFLICT` | **无数据** | 无数据 | ✅ |
| `ATOM-SUPERIORITY-WORDS` | **无数据** | 无数据 | — |
| `EV-FM-REQUIRED` | **无数据** | 无数据 | ✅ |
| `EV-ID-UNIQUE` | **无数据** | 无数据 | ✅ |
| `EV-FALSIFICATION` | **无数据** | 无数据 | ✅ |
| `EV-MATRIX` | **无数据** | 无数据 | ✅ |
| `ATOM-GRAY-ZONE` | **无数据** | 无数据 | ✅ |
| `ATOM-MISCONCEPTION-LEVELS` | **无数据** | 无数据 | — |
| `MIS-LIBRARY` | **无数据** | 无数据 | — |
| `ATOM-MISCONCEPTION-REF` | **无数据** | 无数据 | ✅ |
| `ATOM-AUDIENCE` | **无数据** | 无数据 | ✅ |
| `ATOM-PREREQ-READABLE` | **无数据** | 无数据 | ✅ |
| `EV-SERVES-EXIST` | **无数据** | 无数据 | ✅ |
| `DOC-ZERO-PLACEHOLDER` | **无数据** | 无数据 | — |
| `META-MANIFEST` | **无数据** | 无数据 | — |
| `S1-AUTHOR-SELF-VERIFY` | **无数据** | 无数据 | — |
| `S1-GIT-AUTHOR-BINDING` | **无数据** | 无数据 | — |
| `ATOM-VERIFY-REASON` | **无数据** | 无数据 | ✅ |
| `EV-ARTIFACT-VERSION-MATCH` | **无数据** | 无数据 | ✅ |
| `S2-EVIDENCE-VERDICT` | **无数据** | 无数据 | ✅ |
| `S3-EXPECTED-HARDCODED` | **无数据** | 无数据 | — |
| `EV-SELF-SATISFIED-ASSERT` | **无数据** | 无数据 | — |
| `EV-FALSIFICATION-QUANT` | **无数据** | 无数据 | — |
| `EV-TRIVIAL-OBSERVATION` | **无数据** | 无数据 | — |
| `EV-MATRIX-UNBACKED` | **无数据** | 无数据 | — |
| `EV-ZERO-DIAG-WERROR` | **无数据** | 无数据 | — |
| `EV-WERROR-DECL-BIND` | **无数据** | 无数据 | — |
| `EV-ASSERT-COUNT-BELOW-BASELINE` | **无数据** | 无数据 | ✅ |
| `EV-OUT-UNDECLARED-KEY` | **无数据** | 无数据 | — |
| `EV-RUN-KEY-DECLARED-EXISTS` | **无数据** | 无数据 | — |
| `EV-ASSERT-SYMBOL-MAPPED` | **无数据** | 无数据 | ✅ |
| `EV-ARTIFACT-PRODUCER` | **无数据** | 无数据 | ✅ |
| `EV-ARTIFACT-FILE-EXISTS` | **无数据** | 无数据 | ✅ |
| `EV-MSCV-NO-VERIFY` | **无数据** | 无数据 | ✅ |
| `EV-FM-DUP-KEY` | **无数据** | 无数据 | ✅ |
| `EV-FM-YAML-HARDENING` | **无数据** | 无数据 | ✅ |
| `EV-ENV-DEPENDENT-KEY` | **无数据** | 无数据 | — |
| `ATOM-REL-UNKNOWN` | **无数据** | 无数据 | ✅ |
| `ATOM-CLAIM-STRUCTURED` | **无数据** | 无数据 | ✅ |
| `OBSERVATION-NEEDS-ARTIFACT` | **无数据** | 无数据 | ✅ |
| `INFERENCE-NOT-MACHINE-VERIFIED` | **无数据** | 无数据 | — |
| `ATOM-CLAIM-CONCEPT-NORMALIZED` | **无数据** | 无数据 | — |
| `OBSERVATION-LIVENESS` | **无数据** | 无数据 | — |
| `EV-FIXTURE-NO-ECHO-DATA` | **无数据** | 无数据 | — |
| `EV-OUT-STALE-MTIME` | **无数据** | 无数据 | — |
| `CARD-PATH-NOT-CANONICAL` | **无数据** | 无数据 | ✅ |
| `EV-SERVES-EXIST-HC` | **无数据** | 无数据 | — |
| `ATOM-REL-TARGET-HC` | **无数据** | 无数据 | — |
| `ATOM-REL-UNKNOWN-HC` | **无数据** | 无数据 | — |
| `CARD-PATH-NOT-CANONICAL-HC` | **无数据** | 无数据 | — |
| `PED-MOTIVATION` | **无数据** | 无数据 | — |
| `PED-MISCONCEPTION` | **无数据** | 无数据 | — |
| `PED-SOCRATIC` | **无数据** | 无数据 | — |
| `PED-PREDICT-FIRST` | **无数据** | 无数据 | — |
| `LLM-SUPERIORITY-QUALITY` | **无数据** | 无数据 | — |
| `HYBRID-TEACHING-DEPTH` | **无数据** | 无数据 | — |
| `HUMAN-GOLDEN-REVIEW` | **无数据** | 无数据 | — |

## 二、校准追踪器报告格式（影子设计）

- 每验证器：`ECE = Σ_b (n_b/N) × |acc(b) − conf(b)|（b 为置信分桶）`
- 分域：['简单', '中等', '复杂']
- 三级降级：L1 重校准 ECE > 0.10 ⇒ 重校准置信映射；L2 禁言 ECE > 0.20 ⇒ 该验证器禁言（不单独判 block）；L3 降级 ECE > 0.30 ⇒ 降级为 advice
- 影子设计；本批不启用、不改判决。

## 三、观察态规则的历史影响（离线模拟）

- 观察态规则：**67** 条（全部规则）；
- 历史判决总数（Authority ledger）：**452** 条 ——若按 v26「观察态不得单独判 block」，这些判决**都需复核**（模拟口径，非实际）。

## 诚实登记

1. **known_error_rate 全部「无数据」**：仓库无逐规则误报/漏报台账（VFDR 只记**覆盖率**）；**未编造**任何数字；
2. ECE 格式为**影子设计**，本批不启用、不改判决；
3. 「历史影响」用**判决总数**近似（无法逐规则归因）——如实说明。

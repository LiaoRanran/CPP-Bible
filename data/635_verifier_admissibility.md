# 635 V26-5 · 验证器准入表（Daubert 五问）

- 验证器：**68**（67 规则 + 1 mutation 生成器）
- **观察态**（缺 known_error_rate）：**67**

## 一、五问填表

| 验证器 | 可检验性 | 同行评审 | 已知错误率 | 操作标准 | 社区接受 | 观察态 |
|---|---|---|---|---|---|---|
| `ATOM-FM-REQUIRED` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-ID-FORMAT` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-ID-UNIQUE` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-VERIFIED-BOUND` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-NO-UNVERIFIED` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-STATUS-VALUE` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-STATUS-TRANSITION` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-DAL-MATCH` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-REL-TARGET` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-REL-DAG` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-REL-CONFLICT` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-SUPERIORITY-WORDS` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-FM-REQUIRED` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-ID-UNIQUE` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-FALSIFICATION` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-MATRIX` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-GRAY-ZONE` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-MISCONCEPTION-LEVELS` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `MIS-LIBRARY` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-MISCONCEPTION-REF` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-AUDIENCE` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-PREREQ-READABLE` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-SERVES-EXIST` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `DOC-ZERO-PLACEHOLDER` | ✅ | ❌ | ❌ | ✅ | ❌ | ⚠️ 是 |
| `META-MANIFEST` | ✅ | ❌ | ❌ | ✅ | ❌ | ⚠️ 是 |
| `S1-AUTHOR-SELF-VERIFY` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `S1-GIT-AUTHOR-BINDING` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-VERIFY-REASON` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-ARTIFACT-VERSION-MATCH` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `S2-EVIDENCE-VERDICT` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `S3-EXPECTED-HARDCODED` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-SELF-SATISFIED-ASSERT` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-FALSIFICATION-QUANT` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-TRIVIAL-OBSERVATION` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-MATRIX-UNBACKED` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-ZERO-DIAG-WERROR` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-WERROR-DECL-BIND` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-ASSERT-COUNT-BELOW-BASELINE` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-OUT-UNDECLARED-KEY` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-RUN-KEY-DECLARED-EXISTS` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-ASSERT-SYMBOL-MAPPED` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-ARTIFACT-PRODUCER` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-ARTIFACT-FILE-EXISTS` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-MSCV-NO-VERIFY` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-FM-DUP-KEY` | ✅ | ❌ | ❌ | ✅ | ❌ | ⚠️ 是 |
| `EV-FM-YAML-HARDENING` | ✅ | ❌ | ❌ | ✅ | ❌ | ⚠️ 是 |
| `EV-ENV-DEPENDENT-KEY` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-REL-UNKNOWN` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-CLAIM-STRUCTURED` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `OBSERVATION-NEEDS-ARTIFACT` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `INFERENCE-NOT-MACHINE-VERIFIED` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-CLAIM-CONCEPT-NORMALIZED` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `OBSERVATION-LIVENESS` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-FIXTURE-NO-ECHO-DATA` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `EV-OUT-STALE-MTIME` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `CARD-PATH-NOT-CANONICAL` | ✅ | ❌ | ❌ | ✅ | ❌ | ⚠️ 是 |
| `EV-SERVES-EXIST-HC` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-REL-TARGET-HC` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `ATOM-REL-UNKNOWN-HC` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `CARD-PATH-NOT-CANONICAL-HC` | ✅ | ❌ | ❌ | ✅ | ❌ | ⚠️ 是 |
| `PED-MOTIVATION` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `PED-MISCONCEPTION` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `PED-SOCRATIC` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `PED-PREDICT-FIRST` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `LLM-SUPERIORITY-QUALITY` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `HYBRID-TEACHING-DEPTH` | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ 是 |
| `HUMAN-GOLDEN-REVIEW` | ✅ | ❌ | ❌ | ✅ | ❌ | ⚠️ 是 |
| `mutation_generator` | ✅ | ❌ | ✅ | ✅ | ✅ | 否 |

## 二、观察态验证器（可报信号，不能单独判 block）

- `ATOM-FM-REQUIRED`
- `ATOM-ID-FORMAT`
- `ATOM-ID-UNIQUE`
- `ATOM-VERIFIED-BOUND`
- `ATOM-NO-UNVERIFIED`
- `ATOM-STATUS-VALUE`
- `ATOM-STATUS-TRANSITION`
- `ATOM-DAL-MATCH`
- `ATOM-REL-TARGET`
- `ATOM-REL-DAG`
- `ATOM-REL-CONFLICT`
- `ATOM-SUPERIORITY-WORDS`
- `EV-FM-REQUIRED`
- `EV-ID-UNIQUE`
- `EV-FALSIFICATION`
- `EV-MATRIX`
- `ATOM-GRAY-ZONE`
- `ATOM-MISCONCEPTION-LEVELS`
- `MIS-LIBRARY`
- `ATOM-MISCONCEPTION-REF`
- `ATOM-AUDIENCE`
- `ATOM-PREREQ-READABLE`
- `EV-SERVES-EXIST`
- `DOC-ZERO-PLACEHOLDER`
- `META-MANIFEST`
- `S1-AUTHOR-SELF-VERIFY`
- `S1-GIT-AUTHOR-BINDING`
- `ATOM-VERIFY-REASON`
- `EV-ARTIFACT-VERSION-MATCH`
- `S2-EVIDENCE-VERDICT`
- `S3-EXPECTED-HARDCODED`
- `EV-SELF-SATISFIED-ASSERT`
- `EV-FALSIFICATION-QUANT`
- `EV-TRIVIAL-OBSERVATION`
- `EV-MATRIX-UNBACKED`
- `EV-ZERO-DIAG-WERROR`
- `EV-WERROR-DECL-BIND`
- `EV-ASSERT-COUNT-BELOW-BASELINE`
- `EV-OUT-UNDECLARED-KEY`
- `EV-RUN-KEY-DECLARED-EXISTS`
- `EV-ASSERT-SYMBOL-MAPPED`
- `EV-ARTIFACT-PRODUCER`
- `EV-ARTIFACT-FILE-EXISTS`
- `EV-MSCV-NO-VERIFY`
- `EV-FM-DUP-KEY`
- `EV-FM-YAML-HARDENING`
- `EV-ENV-DEPENDENT-KEY`
- `ATOM-REL-UNKNOWN`
- `ATOM-CLAIM-STRUCTURED`
- `OBSERVATION-NEEDS-ARTIFACT`
- `INFERENCE-NOT-MACHINE-VERIFIED`
- `ATOM-CLAIM-CONCEPT-NORMALIZED`
- `OBSERVATION-LIVENESS`
- `EV-FIXTURE-NO-ECHO-DATA`
- `EV-OUT-STALE-MTIME`
- `CARD-PATH-NOT-CANONICAL`
- `EV-SERVES-EXIST-HC`
- `ATOM-REL-TARGET-HC`
- `ATOM-REL-UNKNOWN-HC`
- `CARD-PATH-NOT-CANONICAL-HC`
- `PED-MOTIVATION`
- `PED-MISCONCEPTION`
- `PED-SOCRATIC`
- `PED-PREDICT-FIRST`
- `LLM-SUPERIORITY-QUALITY`
- `HYBRID-TEACHING-DEPTH`
- `HUMAN-GOLDEN-REVIEW`

## 三、缺失 known_error_rate 的验证器

- **67** 个（= 全部 67 规则）

## 诚实登记

1. **67 规则全缺逐规则错误率**（VFDR 只记**覆盖率**，非错误率）⇒ 全部观察态；
2. 五问中 `peer_reviewed` 全为 False（**无独立第三方评审记录**），`testable/operational_standard` 为 True（有 check 函数与 scope/severity 口径）；
3. **「观察态」仅标记，不改任何判决逻辑**（§零.1：只加数据）——实际「不能单独判 block」的落地需人审决定（交人项）；
4. 唯一 `known_error_rate=True` 的是 mutation 生成器（逃逸率 1/1406）。

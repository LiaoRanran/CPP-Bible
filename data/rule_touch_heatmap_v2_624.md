# 624 A5 · 规则触达热力图 v2（63 规则 × 6 轮）

> 图例：`T`=该轮触达；`.`=未触达。

| 规则 | 严重 | R1 | R2 | R3 | R4 | R5 | R6 | 累计 |
|---|---|---|---|---|---|---|---|---|
| ATOM-FM-REQUIRED | block | T | . | T | T | . | T | T |
| ATOM-ID-FORMAT | block | . | . | T | . | T | . | T |
| ATOM-ID-UNIQUE | block | . | . | T | . | T | . | T |
| ATOM-VERIFIED-BOUND | block | . | . | . | . | . | T | T |
| ATOM-NO-UNVERIFIED | block | . | . | T | . | . | . | T |
| ATOM-STATUS-VALUE | block | . | T | T | . | . | . | T |
| ATOM-STATUS-TRANSITION | block | T | . | . | . | . | . | T |
| ATOM-DAL-MATCH | block | . | . | T | . | . | . | T |
| ATOM-REL-TARGET | warn | . | . | T | . | T | . | T |
| ATOM-REL-DAG | block | . | . | T | . | T | . | T |
| ATOM-REL-CONFLICT | block | . | . | . | . | T | . | T |
| ATOM-SUPERIORITY-WORDS | block | . | . | . | . | . | . | . |
| EV-FM-REQUIRED | block | T | . | T | . | . | . | T |
| EV-ID-UNIQUE | block | . | . | T | . | . | . | T |
| EV-FALSIFICATION | block | T | . | . | . | . | . | T |
| EV-MATRIX | block | T | . | T | . | . | . | T |
| ATOM-GRAY-ZONE | block | . | . | T | . | . | . | T |
| ATOM-MISCONCEPTION-LEVELS | block | . | . | . | . | . | . | . |
| MIS-LIBRARY | block | . | . | . | . | . | . | . |
| ATOM-MISCONCEPTION-REF | block | . | . | . | . | . | T | T |
| ATOM-AUDIENCE | block | . | . | T | . | . | . | T |
| ATOM-PREREQ-READABLE | block | . | . | T | . | T | . | T |
| EV-SERVES-EXIST | warn | . | T | T | . | T | . | T |
| DOC-ZERO-PLACEHOLDER | block | . | . | . | . | . | . | . |
| META-MANIFEST | warn | . | . | . | . | . | . | . |
| S1-AUTHOR-SELF-VERIFY | block | . | . | . | . | . | . | . |
| S1-GIT-AUTHOR-BINDING | warn | . | . | . | . | . | . | . |
| ATOM-VERIFY-REASON | warn | . | . | T | . | T | . | T |
| EV-ARTIFACT-VERSION-MATCH | block | . | T | T | T | T | . | T |
| S2-EVIDENCE-VERDICT | block | . | . | . | . | . | T | T |
| S3-EXPECTED-HARDCODED | block | . | . | . | . | . | . | . |
| EV-SELF-SATISFIED-ASSERT | warn | . | . | . | . | . | . | . |
| EV-FALSIFICATION-QUANT | warn | . | . | . | . | . | . | . |
| EV-TRIVIAL-OBSERVATION | warn | . | . | . | . | . | . | . |
| EV-MATRIX-UNBACKED | warn | . | . | . | . | . | . | . |
| EV-ZERO-DIAG-WERROR | block | . | . | . | . | . | . | . |
| EV-WERROR-DECL-BIND | block | . | . | . | . | . | . | . |
| EV-ASSERT-COUNT-BELOW-BASELINE | block | . | . | T | T | . | . | T |
| EV-OUT-UNDECLARED-KEY | warn | . | . | . | . | . | . | . |
| EV-RUN-KEY-DECLARED-EXISTS | block | . | . | . | . | . | . | . |
| EV-ASSERT-SYMBOL-MAPPED | block | . | . | . | T | T | . | T |
| EV-ARTIFACT-PRODUCER | block | . | . | T | . | . | . | T |
| EV-ARTIFACT-FILE-EXISTS | block | . | . | . | . | T | . | T |
| EV-MSCV-NO-VERIFY | block | . | . | T | . | . | . | T |
| EV-FM-DUP-KEY | block | . | . | T | . | . | . | T |
| EV-FM-YAML-HARDENING | block | . | . | T | T | T | . | T |
| EV-ENV-DEPENDENT-KEY | block | . | . | . | . | . | . | . |
| ATOM-REL-UNKNOWN | warn | . | . | T | . | T | . | T |
| ATOM-CLAIM-STRUCTURED | block | . | . | T | . | . | . | T |
| OBSERVATION-NEEDS-ARTIFACT | block | . | . | . | . | . | T | T |
| INFERENCE-NOT-MACHINE-VERIFIED | block | . | . | . | . | . | . | . |
| ATOM-CLAIM-CONCEPT-NORMALIZED | warn | . | . | . | . | . | . | . |
| OBSERVATION-LIVENESS | warn | . | . | . | . | . | . | . |
| EV-FIXTURE-NO-ECHO-DATA | warn | . | . | . | . | . | . | . |
| EV-OUT-STALE-MTIME | warn | . | . | . | . | . | . | . |
| CARD-PATH-NOT-CANONICAL | warn | . | . | T | T | . | . | T |
| PED-MOTIVATION | advice | . | . | . | . | . | . | . |
| PED-MISCONCEPTION | advice | . | . | . | . | . | . | . |
| PED-SOCRATIC | advice | . | . | . | . | . | . | . |
| PED-PREDICT-FIRST | advice | . | . | . | . | . | . | . |
| LLM-SUPERIORITY-QUALITY | advice | . | . | . | . | . | . | . |
| HYBRID-TEACHING-DEPTH | advice | . | . | . | . | . | . | . |
| HUMAN-GOLDEN-REVIEW | advice | . | . | . | . | . | . | . |

**累计触达 34/63；盲区 29（623 为 37，缩减 8）**


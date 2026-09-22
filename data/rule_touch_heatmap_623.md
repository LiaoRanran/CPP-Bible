# 623 A5 · 规则触达热力图（闭环覆盖 63 条 gate 规则）

> 数据来源：A2(80 条) + R3(40 条) 沙箱实跑。累计触达 **26/63** 条（block 21/40、warn 5/16、advice 0/7）。

> 图例：`T`=闭环触达（A2 或 R3 触发过）`.`=未触达；`B`=仅 block 触发，`W`=仅 warn 触发。


## BLOCK 级（40 条）

| 规则 | 严重 | A2 | R3 | 累计 | 触发级别 |
|---|---|---|---|---|---|
| ATOM-FM-REQUIRED | block | T | T | T | B |
| ATOM-ID-FORMAT | block | T | . | T | B |
| ATOM-ID-UNIQUE | block | T | . | T | B |
| ATOM-VERIFIED-BOUND | block | . | . | . | - |
| ATOM-NO-UNVERIFIED | block | T | . | T | B |
| ATOM-STATUS-VALUE | block | T | . | T | B |
| ATOM-STATUS-TRANSITION | block | . | . | . | - |
| ATOM-DAL-MATCH | block | T | . | T | B |
| ATOM-REL-DAG | block | T | . | T | B |
| ATOM-REL-CONFLICT | block | . | . | . | - |
| ATOM-SUPERIORITY-WORDS | block | . | . | . | - |
| EV-FM-REQUIRED | block | T | . | T | B |
| EV-ID-UNIQUE | block | T | . | T | B |
| EV-FALSIFICATION | block | . | . | . | - |
| EV-MATRIX | block | T | . | T | B |
| ATOM-GRAY-ZONE | block | T | . | T | B |
| ATOM-MISCONCEPTION-LEVELS | block | . | . | . | - |
| MIS-LIBRARY | block | . | . | . | - |
| ATOM-MISCONCEPTION-REF | block | . | . | . | - |
| ATOM-AUDIENCE | block | T | . | T | B |
| ATOM-PREREQ-READABLE | block | T | . | T | W |
| DOC-ZERO-PLACEHOLDER | block | . | . | . | - |
| S1-AUTHOR-SELF-VERIFY | block | . | . | . | - |
| EV-ARTIFACT-VERSION-MATCH | block | T | T | T | B |
| S2-EVIDENCE-VERDICT | block | . | . | . | - |
| S3-EXPECTED-HARDCODED | block | . | . | . | - |
| EV-ZERO-DIAG-WERROR | block | . | . | . | - |
| EV-WERROR-DECL-BIND | block | . | . | . | - |
| EV-ASSERT-COUNT-BELOW-BASELINE | block | T | T | T | W |
| EV-RUN-KEY-DECLARED-EXISTS | block | . | . | . | - |
| EV-ASSERT-SYMBOL-MAPPED | block | . | T | T | - |
| EV-ARTIFACT-PRODUCER | block | T | . | T | B |
| EV-ARTIFACT-FILE-EXISTS | block | . | . | . | - |
| EV-MSCV-NO-VERIFY | block | T | . | T | B |
| EV-FM-DUP-KEY | block | T | . | T | B |
| EV-FM-YAML-HARDENING | block | T | T | T | B |
| EV-ENV-DEPENDENT-KEY | block | . | . | . | - |
| ATOM-CLAIM-STRUCTURED | block | T | . | T | W |
| OBSERVATION-NEEDS-ARTIFACT | block | . | . | . | - |
| INFERENCE-NOT-MACHINE-VERIFIED | block | . | . | . | - |

## WARN 级（16 条）

| 规则 | 严重 | A2 | R3 | 累计 | 触发级别 |
|---|---|---|---|---|---|
| ATOM-REL-TARGET | warn | T | . | T | W |
| EV-SERVES-EXIST | warn | T | . | T | W |
| META-MANIFEST | warn | . | . | . | - |
| S1-GIT-AUTHOR-BINDING | warn | . | . | . | - |
| ATOM-VERIFY-REASON | warn | T | . | T | W |
| EV-SELF-SATISFIED-ASSERT | warn | . | . | . | - |
| EV-FALSIFICATION-QUANT | warn | . | . | . | - |
| EV-TRIVIAL-OBSERVATION | warn | . | . | . | - |
| EV-MATRIX-UNBACKED | warn | . | . | . | - |
| EV-OUT-UNDECLARED-KEY | warn | . | . | . | - |
| ATOM-REL-UNKNOWN | warn | T | . | T | W |
| ATOM-CLAIM-CONCEPT-NORMALIZED | warn | . | . | . | - |
| OBSERVATION-LIVENESS | warn | . | . | . | - |
| EV-FIXTURE-NO-ECHO-DATA | warn | . | . | . | - |
| EV-OUT-STALE-MTIME | warn | . | . | . | - |
| CARD-PATH-NOT-CANONICAL | warn | T | T | T | W |

## ADVICE 级（7 条）

| 规则 | 严重 | A2 | R3 | 累计 | 触发级别 |
|---|---|---|---|---|---|
| PED-MOTIVATION | advice | . | . | . | - |
| PED-MISCONCEPTION | advice | . | . | . | - |
| PED-SOCRATIC | advice | . | . | . | - |
| PED-PREDICT-FIRST | advice | . | . | . | - |
| LLM-SUPERIORITY-QUALITY | advice | . | . | . | - |
| HYBRID-TEACHING-DEPTH | advice | . | . | . | - |
| HUMAN-GOLDEN-REVIEW | advice | . | . | . | - |

## 未触达规则清单（闭环盲区，需 compile/replay/git/多卡 构造）

- 共 **37** 条未触达：block 19 / warn 11 / advice 7

  - `ATOM-VERIFIED-BOUND` (block)
  - `ATOM-STATUS-TRANSITION` (block)
  - `ATOM-REL-CONFLICT` (block)
  - `ATOM-SUPERIORITY-WORDS` (block)
  - `EV-FALSIFICATION` (block)
  - `ATOM-MISCONCEPTION-LEVELS` (block)
  - `MIS-LIBRARY` (block)
  - `ATOM-MISCONCEPTION-REF` (block)
  - `DOC-ZERO-PLACEHOLDER` (block)
  - `META-MANIFEST` (warn)
  - `S1-AUTHOR-SELF-VERIFY` (block)
  - `S1-GIT-AUTHOR-BINDING` (warn)
  - `S2-EVIDENCE-VERDICT` (block)
  - `S3-EXPECTED-HARDCODED` (block)
  - `EV-SELF-SATISFIED-ASSERT` (warn)
  - `EV-FALSIFICATION-QUANT` (warn)
  - `EV-TRIVIAL-OBSERVATION` (warn)
  - `EV-MATRIX-UNBACKED` (warn)
  - `EV-ZERO-DIAG-WERROR` (block)
  - `EV-WERROR-DECL-BIND` (block)
  - `EV-OUT-UNDECLARED-KEY` (warn)
  - `EV-RUN-KEY-DECLARED-EXISTS` (block)
  - `EV-ARTIFACT-FILE-EXISTS` (block)
  - `EV-ENV-DEPENDENT-KEY` (block)
  - `OBSERVATION-NEEDS-ARTIFACT` (block)
  - `INFERENCE-NOT-MACHINE-VERIFIED` (block)
  - `ATOM-CLAIM-CONCEPT-NORMALIZED` (warn)
  - `OBSERVATION-LIVENESS` (warn)
  - `EV-FIXTURE-NO-ECHO-DATA` (warn)
  - `EV-OUT-STALE-MTIME` (warn)
  - `PED-MOTIVATION` (advice)
  - `PED-MISCONCEPTION` (advice)
  - `PED-SOCRATIC` (advice)
  - `PED-PREDICT-FIRST` (advice)
  - `LLM-SUPERIORITY-QUALITY` (advice)
  - `HYBRID-TEACHING-DEPTH` (advice)
  - `HUMAN-GOLDEN-REVIEW` (advice)

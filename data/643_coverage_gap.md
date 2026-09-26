# 643 B1 · 规则覆盖盲区扫描（智能层 #1：自动发现问题）

> 矩阵口径：`矩阵[rule][card] = 1 ⟺ 该规则在该卡上产生 Finding`；
> 数据源 = `gate_engine.run(include_advice=True)` **现算**（121 条 Finding）。
> 规模：**67 条规则 × 27 张 ATOM 卡**，命中单元 **32** 个。

## 一、盲区清单（四类）

| 类别 | 条数 | 清单 |
|---|---|---|
| **P0** 卡零规则命中 | 0 | （无） |
| **P0** block 规则零命中 | 44 | `ATOM-AUDIENCE`, `ATOM-CLAIM-STRUCTURED`, `ATOM-DAL-MATCH`, `ATOM-FM-REQUIRED`, `ATOM-GRAY-ZONE`, `ATOM-ID-FORMAT`, `ATOM-ID-UNIQUE`, `ATOM-MISCONCEPTION-LEVELS`, `ATOM-MISCONCEPTION-REF`, `ATOM-NO-UNVERIFIED`, `ATOM-PREREQ-READABLE`, `ATOM-REL-CONFLICT`, `ATOM-REL-DAG`, `ATOM-REL-TARGET-HC`, `ATOM-REL-UNKNOWN-HC`, `ATOM-STATUS-TRANSITION`, `ATOM-STATUS-VALUE`, `ATOM-SUPERIORITY-WORDS`, `ATOM-VERIFIED-BOUND`, `CARD-PATH-NOT-CANONICAL-HC` … |
| **P1** 规则只命中 1 张卡 | 1 | `ATOM-REL-TARGET` |
| **P2** 卡被 >10 条规则命中 | 0 | （无） |

**优先级分布**：P0 44 / P1 1 / P2 0。

### 1.1 全部零命中规则（64 条）

`ATOM-AUDIENCE`, `ATOM-CLAIM-STRUCTURED`, `ATOM-DAL-MATCH`, `ATOM-FM-REQUIRED`, `ATOM-GRAY-ZONE`, `ATOM-ID-FORMAT`, `ATOM-ID-UNIQUE`, `ATOM-MISCONCEPTION-LEVELS`, `ATOM-MISCONCEPTION-REF`, `ATOM-NO-UNVERIFIED`, `ATOM-PREREQ-READABLE`, `ATOM-REL-CONFLICT`, `ATOM-REL-DAG`, `ATOM-REL-TARGET-HC`, `ATOM-REL-UNKNOWN`, `ATOM-REL-UNKNOWN-HC`, `ATOM-STATUS-TRANSITION`, `ATOM-STATUS-VALUE`, `ATOM-SUPERIORITY-WORDS`, `ATOM-VERIFIED-BOUND`, `ATOM-VERIFY-REASON`, `CARD-PATH-NOT-CANONICAL`, `CARD-PATH-NOT-CANONICAL-HC`, `DOC-ZERO-PLACEHOLDER`, `EV-ARTIFACT-FILE-EXISTS`, `EV-ARTIFACT-PRODUCER`, `EV-ARTIFACT-VERSION-MATCH`, `EV-ASSERT-COUNT-BELOW-BASELINE`, `EV-ASSERT-SYMBOL-MAPPED`, `EV-ENV-DEPENDENT-KEY`, `EV-FALSIFICATION`, `EV-FALSIFICATION-QUANT`, `EV-FIXTURE-NO-ECHO-DATA`, `EV-FM-DUP-KEY`, `EV-FM-REQUIRED`, `EV-FM-YAML-HARDENING`, `EV-ID-UNIQUE`, `EV-MATRIX`, `EV-MATRIX-UNBACKED`, `EV-MSCV-NO-VERIFY`, `EV-OUT-STALE-MTIME`, `EV-OUT-UNDECLARED-KEY`, `EV-RUN-KEY-DECLARED-EXISTS`, `EV-SELF-SATISFIED-ASSERT`, `EV-SERVES-EXIST`, `EV-SERVES-EXIST-HC`, `EV-TRIVIAL-OBSERVATION`, `EV-WERROR-DECL-BIND`, `EV-ZERO-DIAG-WERROR`, `HUMAN-GOLDEN-REVIEW`, `HYBRID-TEACHING-DEPTH`, `INFERENCE-NOT-MACHINE-VERIFIED`, `LLM-SUPERIORITY-QUALITY`, `META-MANIFEST`, `MIS-LIBRARY`, `OBSERVATION-NEEDS-ARTIFACT`, `PED-MISCONCEPTION`, `PED-MOTIVATION`, `PED-PREDICT-FIRST`, `PED-SOCRATIC`, `S1-AUTHOR-SELF-VERIFY`, `S1-GIT-AUTHOR-BINDING`, `S2-EVIDENCE-VERDICT`, `S3-EXPECTED-HARDCODED`

## 二、热力图（规则 × 卡）

| 规则 | c00 c01 c02 c03 c04 c05 c06 c07 c08 c09 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24 c25 c26 | 命中卡数 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ATOM-AUDIENCE` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-CLAIM-CONCEPT-NORMALIZED` | x x x x x x x x x x x x x x x x x x x x x x x x x x x | 27 |
| `ATOM-CLAIM-STRUCTURED` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-DAL-MATCH` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-FM-REQUIRED` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-GRAY-ZONE` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-ID-FORMAT` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-ID-UNIQUE` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-MISCONCEPTION-LEVELS` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-MISCONCEPTION-REF` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-NO-UNVERIFIED` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-PREREQ-READABLE` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-REL-CONFLICT` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-REL-DAG` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-REL-TARGET` | . . . . . . . . . . . . . . . . . . . . . . . . . . x | 1 |
| `ATOM-REL-TARGET-HC` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-REL-UNKNOWN` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-REL-UNKNOWN-HC` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-STATUS-TRANSITION` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-STATUS-VALUE` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-SUPERIORITY-WORDS` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-VERIFIED-BOUND` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `ATOM-VERIFY-REASON` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `CARD-PATH-NOT-CANONICAL` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `CARD-PATH-NOT-CANONICAL-HC` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `DOC-ZERO-PLACEHOLDER` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-ARTIFACT-FILE-EXISTS` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-ARTIFACT-PRODUCER` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-ARTIFACT-VERSION-MATCH` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-ASSERT-COUNT-BELOW-BASELINE` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-ASSERT-SYMBOL-MAPPED` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-ENV-DEPENDENT-KEY` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-FALSIFICATION` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-FALSIFICATION-QUANT` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-FIXTURE-NO-ECHO-DATA` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-FM-DUP-KEY` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-FM-REQUIRED` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-FM-YAML-HARDENING` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-ID-UNIQUE` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-MATRIX` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-MATRIX-UNBACKED` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-MSCV-NO-VERIFY` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-OUT-STALE-MTIME` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-OUT-UNDECLARED-KEY` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-RUN-KEY-DECLARED-EXISTS` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-SELF-SATISFIED-ASSERT` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-SERVES-EXIST` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-SERVES-EXIST-HC` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-TRIVIAL-OBSERVATION` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-WERROR-DECL-BIND` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `EV-ZERO-DIAG-WERROR` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `HUMAN-GOLDEN-REVIEW` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `HYBRID-TEACHING-DEPTH` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `INFERENCE-NOT-MACHINE-VERIFIED` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `LLM-SUPERIORITY-QUALITY` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `META-MANIFEST` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `MIS-LIBRARY` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `OBSERVATION-LIVENESS` | . . . . x . . x . x . . . . . x . . . . . . . . . . . | 4 |
| `OBSERVATION-NEEDS-ARTIFACT` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `PED-MISCONCEPTION` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `PED-MOTIVATION` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `PED-PREDICT-FIRST` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `PED-SOCRATIC` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `S1-AUTHOR-SELF-VERIFY` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `S1-GIT-AUTHOR-BINDING` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `S2-EVIDENCE-VERDICT` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |
| `S3-EXPECTED-HARDCODED` | . . . . . . . . . . . . . . . . . . . . . . . . . . . | 0 |

列号 → 卡片：
- `c00` = `atoms/conc/ATOM-CONC-FENCE-001.md`
- `c01` = `atoms/conc/ATOM-CONC-LOCK-001.md`
- `c02` = `atoms/conc/ATOM-CONC-RACE-001.md`
- `c03` = `atoms/hist/ATOM-HIST-AUTOPTR-001.md`
- `c04` = `atoms/lang/ATOM-LANG-INLINE-001.md`
- `c05` = `atoms/mem/ATOM-MEM-ALIGN-001.md`
- `c06` = `atoms/mem/ATOM-MEM-ALLOC-001.md`
- `c07` = `atoms/mem/ATOM-MEM-ALLOC-002.md`
- `c08` = `atoms/mem/ATOM-MEM-LEAK-001.md`
- `c09` = `atoms/mem/ATOM-MEM-LEAK-002.md`
- `c10` = `atoms/mem/ATOM-MEM-MOVE-002.md`
- `c11` = `atoms/mem/ATOM-MEM-NEW-001.md`
- `c12` = `atoms/mem/ATOM-MEM-PERF-001.md`
- `c13` = `atoms/mem/ATOM-MEM-PERF-002.md`
- `c14` = `atoms/mem/ATOM-MEM-PERF-003.md`
- `c15` = `atoms/mem/ATOM-MEM-PERF-004.md`
- `c16` = `atoms/mem/ATOM-MEM-RAII-001.md`
- `c17` = `atoms/mem/ATOM-MEM-RAII-002.md`
- `c18` = `atoms/mem/ATOM-MEM-RVREF-001.md`
- `c19` = `atoms/mem/ATOM-MEM-SHARED-001.md`
- `c20` = `atoms/mem/ATOM-MEM-SHARED-002.md`
- `c21` = `atoms/mem/ATOM-MEM-UNIQUE-001.md`
- `c22` = `atoms/mem/ATOM-MEM-UNIQUE-002.md`
- `c23` = `atoms/mem/ATOM-MEM-VALUE-001.md`
- `c24` = `atoms/mem/ATOM-MEM-VALUE-002.md`
- `c25` = `atoms/mem/ATOM-MEM-WEAK-001.md`
- `c26` = `atoms/ub/ATOM-UB-GRAY-001.md`

## 三、逐卡命中数

| 卡 | 命中规则数 |
|---|---|
| `atoms/conc/ATOM-CONC-FENCE-001.md` | 1 |
| `atoms/conc/ATOM-CONC-LOCK-001.md` | 1 |
| `atoms/conc/ATOM-CONC-RACE-001.md` | 1 |
| `atoms/hist/ATOM-HIST-AUTOPTR-001.md` | 1 |
| `atoms/mem/ATOM-MEM-ALIGN-001.md` | 1 |
| `atoms/mem/ATOM-MEM-ALLOC-001.md` | 1 |
| `atoms/mem/ATOM-MEM-LEAK-001.md` | 1 |
| `atoms/mem/ATOM-MEM-MOVE-002.md` | 1 |
| `atoms/mem/ATOM-MEM-NEW-001.md` | 1 |
| `atoms/mem/ATOM-MEM-PERF-001.md` | 1 |
| `atoms/mem/ATOM-MEM-PERF-002.md` | 1 |
| `atoms/mem/ATOM-MEM-PERF-003.md` | 1 |
| `atoms/mem/ATOM-MEM-RAII-001.md` | 1 |
| `atoms/mem/ATOM-MEM-RAII-002.md` | 1 |
| `atoms/mem/ATOM-MEM-RVREF-001.md` | 1 |
| `atoms/mem/ATOM-MEM-SHARED-001.md` | 1 |
| `atoms/mem/ATOM-MEM-SHARED-002.md` | 1 |
| `atoms/mem/ATOM-MEM-UNIQUE-001.md` | 1 |
| `atoms/mem/ATOM-MEM-UNIQUE-002.md` | 1 |
| `atoms/mem/ATOM-MEM-VALUE-001.md` | 1 |
| `atoms/mem/ATOM-MEM-VALUE-002.md` | 1 |
| `atoms/mem/ATOM-MEM-WEAK-001.md` | 1 |
| `atoms/lang/ATOM-LANG-INLINE-001.md` | 2 |
| `atoms/mem/ATOM-MEM-ALLOC-002.md` | 2 |
| `atoms/mem/ATOM-MEM-LEAK-002.md` | 2 |
| `atoms/mem/ATOM-MEM-PERF-004.md` | 2 |
| `atoms/ub/ATOM-UB-GRAY-001.md` | 2 |

## 四、优先级条目（逐条）

| 级别 | 类别 | 对象 | 理由 |
|---|---|---|---|
| **P0** | `block_rule_zero_hit` | `ATOM-AUDIENCE` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `ATOM-CLAIM-STRUCTURED` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `ATOM-DAL-MATCH` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `ATOM-FM-REQUIRED` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `ATOM-GRAY-ZONE` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `ATOM-ID-FORMAT` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `ATOM-ID-UNIQUE` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `ATOM-MISCONCEPTION-LEVELS` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `ATOM-MISCONCEPTION-REF` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `ATOM-NO-UNVERIFIED` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `ATOM-PREREQ-READABLE` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `ATOM-REL-CONFLICT` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `ATOM-REL-DAG` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `ATOM-REL-TARGET-HC` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `ATOM-REL-UNKNOWN-HC` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `ATOM-STATUS-TRANSITION` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `ATOM-STATUS-VALUE` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `ATOM-SUPERIORITY-WORDS` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `ATOM-VERIFIED-BOUND` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `CARD-PATH-NOT-CANONICAL-HC` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `DOC-ZERO-PLACEHOLDER` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `EV-ARTIFACT-FILE-EXISTS` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `EV-ARTIFACT-PRODUCER` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `EV-ARTIFACT-VERSION-MATCH` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `EV-ASSERT-COUNT-BELOW-BASELINE` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `EV-ASSERT-SYMBOL-MAPPED` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `EV-ENV-DEPENDENT-KEY` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `EV-FALSIFICATION` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `EV-FM-DUP-KEY` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `EV-FM-REQUIRED` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `EV-FM-YAML-HARDENING` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `EV-ID-UNIQUE` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `EV-MATRIX` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `EV-MSCV-NO-VERIFY` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `EV-RUN-KEY-DECLARED-EXISTS` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `EV-SERVES-EXIST-HC` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `EV-WERROR-DECL-BIND` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `EV-ZERO-DIAG-WERROR` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `INFERENCE-NOT-MACHINE-VERIFIED` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `MIS-LIBRARY` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `OBSERVATION-NEEDS-ARTIFACT` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `S1-AUTHOR-SELF-VERIFY` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `S2-EVIDENCE-VERDICT` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P0** | `block_rule_zero_hit` | `S3-EXPECTED-HARDCODED` | block 级规则零命中 ⇒ 规则空转或卡全合规，需人判 |
| **P1** | `rule_single_card` | `ATOM-REL-TARGET` | 只命中 1 张卡 ⇒ 过拟合候选（规则可能写死到该卡） |

## 诚实登记

1. **自动发现问题 ≠ 问题真的存在**（§十二.1）：这是**启发式扫描**，清单是**线索**不是判决，需人复核；
2. **卡口径差异**：本工具用 `atoms/**/ATOM-*.md` = **27 张**；638 census 的"28 张"是 `atoms/**/*.md`（多 `atoms/README.md`）⇒ 口径不同已登记；
3. **矩阵只反映当前仓库状态**：干净仓里"零命中"是正常的 —— 规则的判别力要看 622/623 的变异跑批（B2/B4 覆盖那一面），不能据此判规则无用；
4. **`block` 零命中不必然是缺陷**：可能是卡全合规（好事），也可能是规则条件写死了（坏事）—— 工具**不给结论**，只列为 P0 线索；
5. `advice`/`warn` 规则计入矩阵；若排除它们，"零命中"会虚增 —— 口径已固定为含全部 67 条。

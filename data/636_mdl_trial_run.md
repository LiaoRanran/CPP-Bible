# 636 2.5 · MDL 边际判据试运行（影子，未拦截新规则）

## 一、判据与编码长度定义（启发式近似）

- `admit(rule) ⟺ savings > L(rule)`；`savings = samples_explained × log2(1593)`；
- `L(rule) = 8×len(id) + 8×len(title) + 32`；
- `samples_explained` = VFDR 热力图触达轮数 × 50（近似样本解释量）。

## 二、67 规则模拟结果

- **admit：30**；**reject：37**；通过率 **44.8%**

| 规则 | 样本数 | savings(bits) | cost(bits) | admit |
|---|---|---|---|---|
| `ATOM-FM-REQUIRED` | 200 | 2127.5 | 232 | ✅ |
| `ATOM-ID-FORMAT` | 100 | 1063.8 | 264 | ✅ |
| `ATOM-ID-UNIQUE` | 100 | 1063.8 | 352 | ✅ |
| `ATOM-VERIFIED-BOUND` | 50 | 531.9 | 408 | ✅ |
| `ATOM-NO-UNVERIFIED` | 50 | 531.9 | 248 | ✅ |
| `ATOM-STATUS-VALUE` | 100 | 1063.8 | 288 | ✅ |
| `ATOM-STATUS-TRANSITION` | 50 | 531.9 | 400 | ✅ |
| `ATOM-DAL-MATCH` | 50 | 531.9 | 248 | ✅ |
| `ATOM-REL-TARGET` | 100 | 1063.8 | 200 | ✅ |
| `ATOM-REL-DAG` | 100 | 1063.8 | 216 | ✅ |
| `ATOM-REL-CONFLICT` | 50 | 531.9 | 592 | ❌ |
| `ATOM-SUPERIORITY-WORDS` | 0 | 0.0 | 328 | ❌ |
| `EV-FM-REQUIRED` | 100 | 1063.8 | 216 | ✅ |
| `EV-ID-UNIQUE` | 50 | 531.9 | 360 | ✅ |
| `EV-FALSIFICATION` | 50 | 531.9 | 264 | ✅ |
| `EV-MATRIX` | 100 | 1063.8 | 168 | ✅ |
| `ATOM-GRAY-ZONE` | 50 | 531.9 | 256 | ✅ |
| `ATOM-MISCONCEPTION-LEVELS` | 0 | 0.0 | 480 | ❌ |
| `MIS-LIBRARY` | 0 | 0.0 | 400 | ❌ |
| `ATOM-MISCONCEPTION-REF` | 50 | 531.9 | 328 | ✅ |
| `ATOM-AUDIENCE` | 50 | 531.9 | 520 | ✅ |
| `ATOM-PREREQ-READABLE` | 100 | 1063.8 | 280 | ✅ |
| `EV-SERVES-EXIST` | 150 | 1595.6 | 224 | ✅ |
| `DOC-ZERO-PLACEHOLDER` | 0 | 0.0 | 248 | ❌ |
| `META-MANIFEST` | 0 | 0.0 | 256 | ❌ |
| `S1-AUTHOR-SELF-VERIFY` | 0 | 0.0 | 456 | ❌ |
| `S1-GIT-AUTHOR-BINDING` | 0 | 0.0 | 472 | ❌ |
| `ATOM-VERIFY-REASON` | 100 | 1063.8 | 408 | ✅ |
| `EV-ARTIFACT-VERSION-MATCH` | 200 | 2127.5 | 464 | ✅ |
| `S2-EVIDENCE-VERDICT` | 50 | 531.9 | 432 | ✅ |
| `S3-EXPECTED-HARDCODED` | 0 | 0.0 | 296 | ❌ |
| `EV-SELF-SATISFIED-ASSERT` | 0 | 0.0 | 400 | ❌ |
| `EV-FALSIFICATION-QUANT` | 0 | 0.0 | 352 | ❌ |
| `EV-TRIVIAL-OBSERVATION` | 0 | 0.0 | 368 | ❌ |
| `EV-MATRIX-UNBACKED` | 0 | 0.0 | 304 | ❌ |
| `EV-ZERO-DIAG-WERROR` | 0 | 0.0 | 336 | ❌ |
| `EV-WERROR-DECL-BIND` | 0 | 0.0 | 440 | ❌ |
| `EV-ASSERT-COUNT-BELOW-BASELINE` | 100 | 1063.8 | 440 | ✅ |
| `EV-OUT-UNDECLARED-KEY` | 0 | 0.0 | 480 | ❌ |
| `EV-RUN-KEY-DECLARED-EXISTS` | 0 | 0.0 | 648 | ❌ |
| `EV-ASSERT-SYMBOL-MAPPED` | 100 | 1063.8 | 472 | ✅ |
| `EV-ARTIFACT-PRODUCER` | 50 | 531.9 | 568 | ❌ |
| `EV-ARTIFACT-FILE-EXISTS` | 50 | 531.9 | 608 | ❌ |
| `EV-MSCV-NO-VERIFY` | 50 | 531.9 | 464 | ✅ |
| `EV-FM-DUP-KEY` | 50 | 531.9 | 440 | ✅ |
| `EV-FM-YAML-HARDENING` | 150 | 1595.6 | 512 | ✅ |
| `EV-ENV-DEPENDENT-KEY` | 0 | 0.0 | 504 | ❌ |
| `ATOM-REL-UNKNOWN` | 100 | 1063.8 | 472 | ✅ |
| `ATOM-CLAIM-STRUCTURED` | 50 | 531.9 | 616 | ❌ |
| `OBSERVATION-NEEDS-ARTIFACT` | 50 | 531.9 | 520 | ✅ |
| `INFERENCE-NOT-MACHINE-VERIFIED` | 0 | 0.0 | 560 | ❌ |
| `ATOM-CLAIM-CONCEPT-NORMALIZED` | 0 | 0.0 | 576 | ❌ |
| `OBSERVATION-LIVENESS` | 0 | 0.0 | 592 | ❌ |
| `EV-FIXTURE-NO-ECHO-DATA` | 0 | 0.0 | 560 | ❌ |
| `EV-OUT-STALE-MTIME` | 0 | 0.0 | 368 | ❌ |
| `CARD-PATH-NOT-CANONICAL` | 100 | 1063.8 | 624 | ✅ |
| `EV-SERVES-EXIST-HC` | 0 | 0.0 | 416 | ❌ |
| `ATOM-REL-TARGET-HC` | 0 | 0.0 | 440 | ❌ |
| `ATOM-REL-UNKNOWN-HC` | 0 | 0.0 | 448 | ❌ |
| `CARD-PATH-NOT-CANONICAL-HC` | 0 | 0.0 | 408 | ❌ |
| `PED-MOTIVATION` | 0 | 0.0 | 248 | ❌ |
| `PED-MISCONCEPTION` | 0 | 0.0 | 240 | ❌ |
| `PED-SOCRATIC` | 0 | 0.0 | 184 | ❌ |
| `PED-PREDICT-FIRST` | 0 | 0.0 | 272 | ❌ |
| `LLM-SUPERIORITY-QUALITY` | 0 | 0.0 | 360 | ❌ |
| `HYBRID-TEACHING-DEPTH` | 0 | 0.0 | 304 | ❌ |
| `HUMAN-GOLDEN-REVIEW` | 0 | 0.0 | 272 | ❌ |

## 三、豁免率趋势（早期 vs 近期）

- 早期一半规则通过率：**66.7%**
- 近期一半规则通过率：**23.5%**
- 趋势：近期更低（规则更冗余）

## 四、若 MDL 在线会挡多少？

- **37/67** 条规则会被 reject（若在线）；
- **本批为影子**，未拦截任何规则（§零.7）。

## 诚实登记

1. **编码长度为启发式近似**（非严格 MDL，§七.4）；
2. `samples_explained` 用「VFDR 触达轮数」近似样本解释量；
3. 7 条规则不在 VFDR 热力图（新增）⇒ samples_explained=0 ⇒ 必 reject（如实说明）；
4. **影子**：未拦截、未改判。

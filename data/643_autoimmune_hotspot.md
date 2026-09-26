# 643 B3 · 自身免疫热点扫描（智能层 #3：自动发现问题）

> 规模：**67 条规则**；阈值：豁免率 ≥ 0.3、常报 ≥ 10、变异场活跃 ≥ 4/6 轮。
> 代理初值：**67/67 条规则**的 `known_error_rate` 仍是代理（642 实测：全库无自身样本）⇒ 本工具**不用它做判据**，只展示。

## 一、热点清单（非'观察'条目）

| 规则 | 声明级别 | 当前命中 | 触达轮数 | 豁免率 | known_error_rate | 建议 | 理由 |
|---|---|---|---|---|---|---|---|
| `ATOM-CLAIM-CONCEPT-NORMALIZED` | warn | 77 | 0/6 | 1.000 | 0.1881（代理） | **不适用候选** | 豁免率 1.000 ≥ 0.3（未触达 6/6 轮）⇒ 规则可能不适用 |
| `EV-MATRIX-UNBACKED` | warn | 16 | 0/6 | 1.000 | 0.1881（代理） | **不适用候选** | 豁免率 1.000 ≥ 0.3（未触达 6/6 轮）⇒ 规则可能不适用 |
| `OBSERVATION-LIVENESS` | warn | 8 | 0/6 | 1.000 | 0.1881（代理） | **不适用候选** | 豁免率 1.000 ≥ 0.3（未触达 6/6 轮）⇒ 规则可能不适用 |
| `EV-OUT-UNDECLARED-KEY` | warn | 6 | 0/6 | 1.000 | 0.1881（代理） | **不适用候选** | 豁免率 1.000 ≥ 0.3（未触达 6/6 轮）⇒ 规则可能不适用 |
| `EV-FALSIFICATION-QUANT` | warn | 4 | 0/6 | 1.000 | 0.1881（代理） | **不适用候选** | 豁免率 1.000 ≥ 0.3（未触达 6/6 轮）⇒ 规则可能不适用 |
| `EV-ASSERT-SYMBOL-MAPPED` | block | 3 | 2/6 | 0.667 | 0.1881（代理） | **不适用候选** | 豁免率 0.667 ≥ 0.3（未触达 4/6 轮）⇒ 规则可能不适用 |
| `ATOM-REL-TARGET` | warn | 2 | 2/6 | 0.667 | 0.1881（代理） | **不适用候选** | 豁免率 0.667 ≥ 0.3（未触达 4/6 轮）⇒ 规则可能不适用 |
| `EV-ENV-DEPENDENT-KEY` | block | 2 | 0/6 | 1.000 | 0.1881（代理） | **不适用候选** | 豁免率 1.000 ≥ 0.3（未触达 6/6 轮）⇒ 规则可能不适用 |
| `EV-OUT-STALE-MTIME` | warn | 2 | 0/6 | 1.000 | 0.1881（代理） | **不适用候选** | 豁免率 1.000 ≥ 0.3（未触达 6/6 轮）⇒ 规则可能不适用 |
| `EV-SERVES-EXIST` | warn | 1 | 3/6 | 0.500 | 0.1881（代理） | **不适用候选** | 豁免率 0.500 ≥ 0.3（未触达 3/6 轮）⇒ 规则可能不适用 |
| `ATOM-AUDIENCE` | block | 0 | 1/6 | 0.833 | 0.1881（代理） | **不适用候选** | 豁免率 0.833 ≥ 0.3（未触达 5/6 轮）⇒ 规则可能不适用 |
| `ATOM-CLAIM-STRUCTURED` | block | 0 | 1/6 | 0.833 | 0.1881（代理） | **不适用候选** | 豁免率 0.833 ≥ 0.3（未触达 5/6 轮）⇒ 规则可能不适用 |
| `ATOM-DAL-MATCH` | block | 0 | 1/6 | 0.833 | 0.1881（代理） | **不适用候选** | 豁免率 0.833 ≥ 0.3（未触达 5/6 轮）⇒ 规则可能不适用 |
| `ATOM-FM-REQUIRED` | block | 0 | 4/6 | 0.333 | 0.1881（代理） | **不适用候选** | 豁免率 0.333 ≥ 0.3（未触达 2/6 轮）⇒ 规则可能不适用 |
| `ATOM-GRAY-ZONE` | block | 0 | 1/6 | 0.833 | 0.1881（代理） | **不适用候选** | 豁免率 0.833 ≥ 0.3（未触达 5/6 轮）⇒ 规则可能不适用 |
| `ATOM-ID-FORMAT` | block | 0 | 2/6 | 0.667 | 0.1881（代理） | **不适用候选** | 豁免率 0.667 ≥ 0.3（未触达 4/6 轮）⇒ 规则可能不适用 |
| `ATOM-ID-UNIQUE` | block | 0 | 2/6 | 0.667 | 0.1881（代理） | **不适用候选** | 豁免率 0.667 ≥ 0.3（未触达 4/6 轮）⇒ 规则可能不适用 |
| `ATOM-MISCONCEPTION-REF` | block | 0 | 1/6 | 0.833 | 0.1881（代理） | **不适用候选** | 豁免率 0.833 ≥ 0.3（未触达 5/6 轮）⇒ 规则可能不适用 |
| `ATOM-NO-UNVERIFIED` | block | 0 | 1/6 | 0.833 | 0.1881（代理） | **不适用候选** | 豁免率 0.833 ≥ 0.3（未触达 5/6 轮）⇒ 规则可能不适用 |
| `ATOM-PREREQ-READABLE` | block | 0 | 2/6 | 0.667 | 0.1881（代理） | **不适用候选** | 豁免率 0.667 ≥ 0.3（未触达 4/6 轮）⇒ 规则可能不适用 |
| `ATOM-REL-CONFLICT` | block | 0 | 1/6 | 0.833 | 0.1881（代理） | **不适用候选** | 豁免率 0.833 ≥ 0.3（未触达 5/6 轮）⇒ 规则可能不适用 |
| `ATOM-REL-DAG` | block | 0 | 2/6 | 0.667 | 0.1881（代理） | **不适用候选** | 豁免率 0.667 ≥ 0.3（未触达 4/6 轮）⇒ 规则可能不适用 |
| `ATOM-REL-UNKNOWN` | warn | 0 | 2/6 | 0.667 | 0.1881（代理） | **不适用候选** | 豁免率 0.667 ≥ 0.3（未触达 4/6 轮）⇒ 规则可能不适用 |
| `ATOM-STATUS-TRANSITION` | block | 0 | 1/6 | 0.833 | 0.1881（代理） | **不适用候选** | 豁免率 0.833 ≥ 0.3（未触达 5/6 轮）⇒ 规则可能不适用 |
| `ATOM-STATUS-VALUE` | block | 0 | 2/6 | 0.667 | 0.1881（代理） | **不适用候选** | 豁免率 0.667 ≥ 0.3（未触达 4/6 轮）⇒ 规则可能不适用 |
| `ATOM-VERIFIED-BOUND` | block | 0 | 1/6 | 0.833 | 0.1881（代理） | **不适用候选** | 豁免率 0.833 ≥ 0.3（未触达 5/6 轮）⇒ 规则可能不适用 |
| `ATOM-VERIFY-REASON` | warn | 0 | 2/6 | 0.667 | 0.1881（代理） | **不适用候选** | 豁免率 0.667 ≥ 0.3（未触达 4/6 轮）⇒ 规则可能不适用 |
| `CARD-PATH-NOT-CANONICAL` | warn | 0 | 2/6 | 0.667 | 0.1881（代理） | **不适用候选** | 豁免率 0.667 ≥ 0.3（未触达 4/6 轮）⇒ 规则可能不适用 |
| `EV-ARTIFACT-FILE-EXISTS` | block | 0 | 1/6 | 0.833 | 0.1881（代理） | **不适用候选** | 豁免率 0.833 ≥ 0.3（未触达 5/6 轮）⇒ 规则可能不适用 |
| `EV-ARTIFACT-PRODUCER` | block | 0 | 1/6 | 0.833 | 0.1881（代理） | **不适用候选** | 豁免率 0.833 ≥ 0.3（未触达 5/6 轮）⇒ 规则可能不适用 |
| `EV-ARTIFACT-VERSION-MATCH` | block | 0 | 4/6 | 0.333 | 0.1881（代理） | **不适用候选** | 豁免率 0.333 ≥ 0.3（未触达 2/6 轮）⇒ 规则可能不适用 |
| `EV-ASSERT-COUNT-BELOW-BASELINE` | block | 0 | 2/6 | 0.667 | 0.1881（代理） | **不适用候选** | 豁免率 0.667 ≥ 0.3（未触达 4/6 轮）⇒ 规则可能不适用 |
| `EV-FALSIFICATION` | block | 0 | 1/6 | 0.833 | 0.1881（代理） | **不适用候选** | 豁免率 0.833 ≥ 0.3（未触达 5/6 轮）⇒ 规则可能不适用 |
| `EV-FM-DUP-KEY` | block | 0 | 1/6 | 0.833 | 0.1881（代理） | **不适用候选** | 豁免率 0.833 ≥ 0.3（未触达 5/6 轮）⇒ 规则可能不适用 |
| `EV-FM-REQUIRED` | block | 0 | 2/6 | 0.667 | 0.1881（代理） | **不适用候选** | 豁免率 0.667 ≥ 0.3（未触达 4/6 轮）⇒ 规则可能不适用 |
| `EV-FM-YAML-HARDENING` | block | 0 | 3/6 | 0.500 | 0.1881（代理） | **不适用候选** | 豁免率 0.500 ≥ 0.3（未触达 3/6 轮）⇒ 规则可能不适用 |
| `EV-ID-UNIQUE` | block | 0 | 1/6 | 0.833 | 0.1881（代理） | **不适用候选** | 豁免率 0.833 ≥ 0.3（未触达 5/6 轮）⇒ 规则可能不适用 |
| `EV-MATRIX` | block | 0 | 2/6 | 0.667 | 0.1881（代理） | **不适用候选** | 豁免率 0.667 ≥ 0.3（未触达 4/6 轮）⇒ 规则可能不适用 |
| `EV-MSCV-NO-VERIFY` | block | 0 | 1/6 | 0.833 | 0.1881（代理） | **不适用候选** | 豁免率 0.833 ≥ 0.3（未触达 5/6 轮）⇒ 规则可能不适用 |
| `OBSERVATION-NEEDS-ARTIFACT` | block | 0 | 1/6 | 0.833 | 0.1881（代理） | **不适用候选** | 豁免率 0.833 ≥ 0.3（未触达 5/6 轮）⇒ 规则可能不适用 |
| `S2-EVIDENCE-VERDICT` | block | 0 | 1/6 | 0.833 | 0.1881（代理） | **不适用候选** | 豁免率 0.833 ≥ 0.3（未触达 5/6 轮）⇒ 规则可能不适用 |
| `ATOM-MISCONCEPTION-LEVELS` | block | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `ATOM-REL-TARGET-HC` | block | 0 | 0/6 | — | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `ATOM-REL-UNKNOWN-HC` | block | 0 | 0/6 | — | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `ATOM-SUPERIORITY-WORDS` | block | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `CARD-PATH-NOT-CANONICAL-HC` | block | 0 | 0/6 | — | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `DOC-ZERO-PLACEHOLDER` | block | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `EV-FIXTURE-NO-ECHO-DATA` | warn | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `EV-RUN-KEY-DECLARED-EXISTS` | block | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `EV-SELF-SATISFIED-ASSERT` | warn | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `EV-SERVES-EXIST-HC` | block | 0 | 0/6 | — | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `EV-TRIVIAL-OBSERVATION` | warn | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `EV-WERROR-DECL-BIND` | block | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `EV-ZERO-DIAG-WERROR` | block | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `HUMAN-GOLDEN-REVIEW` | advice | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `HYBRID-TEACHING-DEPTH` | advice | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `INFERENCE-NOT-MACHINE-VERIFIED` | block | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `LLM-SUPERIORITY-QUALITY` | advice | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `META-MANIFEST` | warn | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `MIS-LIBRARY` | block | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `PED-MISCONCEPTION` | advice | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `PED-MOTIVATION` | advice | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `PED-PREDICT-FIRST` | advice | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `PED-SOCRATIC` | advice | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `S1-AUTHOR-SELF-VERIFY` | block | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `S1-GIT-AUTHOR-BINDING` | warn | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |
| `S3-EXPECTED-HARDCODED` | block | 0 | 0/6 | 1.000 | 0.1881（代理） | **退役候选** | 从未触达且当前零命中 ⇒ 该规则可能已死（需人判：也可能是卡全合规） |

## 二、建议分布

- `{'不适用候选': 41, '退役候选': 26}`

## 三、四类建议的逐条清单

- **退役候选**（26）：`ATOM-SUPERIORITY-WORDS`, `ATOM-MISCONCEPTION-LEVELS`, `MIS-LIBRARY`, `DOC-ZERO-PLACEHOLDER`, `META-MANIFEST`, `S1-AUTHOR-SELF-VERIFY`, `S1-GIT-AUTHOR-BINDING`, `S3-EXPECTED-HARDCODED`, `EV-SELF-SATISFIED-ASSERT`, `EV-TRIVIAL-OBSERVATION`, `EV-ZERO-DIAG-WERROR`, `EV-WERROR-DECL-BIND`, `EV-RUN-KEY-DECLARED-EXISTS`, `INFERENCE-NOT-MACHINE-VERIFIED`, `EV-FIXTURE-NO-ECHO-DATA`, `EV-SERVES-EXIST-HC`, `ATOM-REL-TARGET-HC`, `ATOM-REL-UNKNOWN-HC`, `CARD-PATH-NOT-CANONICAL-HC`, `PED-MOTIVATION`, `PED-MISCONCEPTION`, `PED-SOCRATIC`, `PED-PREDICT-FIRST`, `LLM-SUPERIORITY-QUALITY`, `HYBRID-TEACHING-DEPTH`, `HUMAN-GOLDEN-REVIEW`
- **不适用候选**（41）：`ATOM-FM-REQUIRED`, `ATOM-ID-FORMAT`, `ATOM-ID-UNIQUE`, `ATOM-VERIFIED-BOUND`, `ATOM-NO-UNVERIFIED`, `ATOM-STATUS-VALUE`, `ATOM-STATUS-TRANSITION`, `ATOM-DAL-MATCH`, `ATOM-REL-TARGET`, `ATOM-REL-DAG`, `ATOM-REL-CONFLICT`, `EV-FM-REQUIRED`, `EV-ID-UNIQUE`, `EV-FALSIFICATION`, `EV-MATRIX`, `ATOM-GRAY-ZONE`, `ATOM-MISCONCEPTION-REF`, `ATOM-AUDIENCE`, `ATOM-PREREQ-READABLE`, `EV-SERVES-EXIST`, `ATOM-VERIFY-REASON`, `EV-ARTIFACT-VERSION-MATCH`, `S2-EVIDENCE-VERDICT`, `EV-FALSIFICATION-QUANT`, `EV-MATRIX-UNBACKED`, `EV-ASSERT-COUNT-BELOW-BASELINE`, `EV-OUT-UNDECLARED-KEY`, `EV-ASSERT-SYMBOL-MAPPED`, `EV-ARTIFACT-PRODUCER`, `EV-ARTIFACT-FILE-EXISTS`, `EV-MSCV-NO-VERIFY`, `EV-FM-DUP-KEY`, `EV-FM-YAML-HARDENING`, `EV-ENV-DEPENDENT-KEY`, `ATOM-REL-UNKNOWN`, `ATOM-CLAIM-STRUCTURED`, `OBSERVATION-NEEDS-ARTIFACT`, `ATOM-CLAIM-CONCEPT-NORMALIZED`, `OBSERVATION-LIVENESS`, `EV-OUT-STALE-MTIME`, `CARD-PATH-NOT-CANONICAL`
- **收紧候选**（0）：（无）
- **放宽候选**（0）：（无）

## 四、⚠️ 数据缺口（inbox 要求但**现有数据无法支撑**）

- 每规则的 **warn 率**（需逐次判决级别统计 ⇒ 现有落盘数据无此维）
- 每规则的 **block 率**（同上 ⇒ 无法判'block 率=0 但 warn 率高'）
- 每规则的**误报率趋势**（需时序标签 ⇒ 只有 1/1406 的逃逸样本）

> 这三项**不是漏做**，而是**落盘数据缺该维度**：智能层照出的第一条真缺陷。
> 已作为 issue 交给 B5（`missing_dimension` 类）。

## 诚实登记

1. **自动发现问题 ≠ 问题真的存在**（§十二.1）：分类是**启发式**，`退役候选` 也可能是「卡全合规」（好事）⇒ 必须人审；
2. **`known_error_rate` 全是代理**（67/67）⇒ 本工具**不**用它做判据，只作展示；用它下结论等于自己骗自己；
3. **豁免率是 642 口径**（热力图未触达轮次占比），反映的是「变异场里没打到」，不等于「生产里没用」—— 两种含义已并列展示，交集才建议退役；
4. 阈值（0.30 / 10 / 4）沿用 642 既有值或本批新定，**属经验值**，边界已在单测里固定，改阈值会改变分类结果；
5. **不改任何规则**：本工具只读 `gate_engine.RULES`、不写规则库、不重钉台账。

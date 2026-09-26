# 643 C2 · 针对性 mutation 计划（智能层：自动生成攻击 #2；**dry-run**）

> 计划条数 **100**（覆盖 **31** 条规则）；算子分布 `{'field_delete': 30, 'break_ref': 29, 'equiv_rewrite': 31, 'format_perturb': 3, 'value_tamper': 7}`；方向分布 `{'B': 91, 'A': 9}`。
> **dry-run**：本文件只列计划，**不修改任何生产卡片**（实际变异由 C3 在沙箱副本上做）。

## 一、算子与方向

| 算子 | 含义 |
|---|---|
| `field_delete` | 删 frontmatter 字段/列表项 |
| `value_tamper` | 数值 +1 / 布尔翻转 |
| `break_ref` | 关系目标改成不存在的 id |
| `format_perturb` | 尾随空格等格式微扰（语义不变） |
| `equiv_rewrite` | 同义改写（语义等价） |

- **方向 A（逃逸型）** 9 条：目标规则**当前命中该卡** ⇒ 变异后仍应命中，不命中=逃逸；
- **方向 B（触发型）** 91 条：目标规则当前**不**命中 ⇒ 变异后应命中，不命中=规则不可达（死规则候选）。

## 二、被跳过的规则（附原因）

| 规则 | 原因 |
|---|---|
| `EV-FM-REQUIRED` | scope=evidence（本批只对 atom 卡生成） |
| `EV-ID-UNIQUE` | scope=evidence（本批只对 atom 卡生成） |
| `EV-FALSIFICATION` | scope=evidence（本批只对 atom 卡生成） |
| `EV-MATRIX` | scope=evidence（本批只对 atom 卡生成） |
| `EV-SERVES-EXIST` | scope=evidence（本批只对 atom 卡生成） |
| `DOC-ZERO-PLACEHOLDER` | scope=repo（本批只对 atom 卡生成） |
| `META-MANIFEST` | scope=repo（本批只对 atom 卡生成） |
| `EV-ARTIFACT-VERSION-MATCH` | scope=evidence（本批只对 atom 卡生成） |
| `S3-EXPECTED-HARDCODED` | scope=evidence（本批只对 atom 卡生成） |
| `EV-SELF-SATISFIED-ASSERT` | scope=evidence（本批只对 atom 卡生成） |
| `EV-FALSIFICATION-QUANT` | scope=evidence（本批只对 atom 卡生成） |
| `EV-TRIVIAL-OBSERVATION` | scope=evidence（本批只对 atom 卡生成） |
| `EV-MATRIX-UNBACKED` | scope=evidence（本批只对 atom 卡生成） |
| `EV-ZERO-DIAG-WERROR` | scope=evidence（本批只对 atom 卡生成） |
| `EV-WERROR-DECL-BIND` | scope=evidence（本批只对 atom 卡生成） |
| `EV-ASSERT-COUNT-BELOW-BASELINE` | scope=evidence（本批只对 atom 卡生成） |
| `EV-OUT-UNDECLARED-KEY` | scope=evidence（本批只对 atom 卡生成） |
| `EV-RUN-KEY-DECLARED-EXISTS` | scope=evidence（本批只对 atom 卡生成） |
| `EV-ASSERT-SYMBOL-MAPPED` | scope=evidence（本批只对 atom 卡生成） |
| `EV-ARTIFACT-PRODUCER` | scope=evidence（本批只对 atom 卡生成） |
| `EV-ARTIFACT-FILE-EXISTS` | scope=evidence（本批只对 atom 卡生成） |
| `EV-MSCV-NO-VERIFY` | scope=evidence（本批只对 atom 卡生成） |
| `EV-FM-DUP-KEY` | scope=repo（本批只对 atom 卡生成） |
| `EV-FM-YAML-HARDENING` | scope=repo（本批只对 atom 卡生成） |
| `EV-ENV-DEPENDENT-KEY` | scope=evidence（本批只对 atom 卡生成） |
| `EV-FIXTURE-NO-ECHO-DATA` | scope=evidence（本批只对 atom 卡生成） |
| `EV-OUT-STALE-MTIME` | scope=evidence（本批只对 atom 卡生成） |
| `CARD-PATH-NOT-CANONICAL` | scope=repo（本批只对 atom 卡生成） |
| `EV-SERVES-EXIST-HC` | scope=evidence（本批只对 atom 卡生成） |
| `CARD-PATH-NOT-CANONICAL-HC` | scope=repo（本批只对 atom 卡生成） |
| `PED-MOTIVATION` | C1 未映射到 check 函数（无法定向） |
| `PED-SOCRATIC` | C1 未映射到 check 函数（无法定向） |
| `PED-PREDICT-FIRST` | C1 未映射到 check 函数（无法定向） |
| `LLM-SUPERIORITY-QUALITY` | C1 未映射到 check 函数（无法定向） |
| `HYBRID-TEACHING-DEPTH` | C1 未映射到 check 函数（无法定向） |
| `HUMAN-GOLDEN-REVIEW` | C1 未映射到 check 函数（无法定向） |

## 三、计划明细（前 60 条）

| mutation_id | 目标规则 | 方向 | 卡 | 算子 | 字段 | expected_oracle |
|---|---|---|---|---|---|---|
| `ATOM-FM-REQUIRED#field_delete#0` | `ATOM-FM-REQUIRED` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | sources | `ATOM-FM-REQUIRED` |
| `ATOM-FM-REQUIRED#break_ref#1` | `ATOM-FM-REQUIRED` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `break_ref` | sources | `ATOM-FM-REQUIRED` |
| `ATOM-FM-REQUIRED#equiv_rewrite#2` | `ATOM-FM-REQUIRED` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `equiv_rewrite` | sources | `ATOM-FM-REQUIRED` |
| `ATOM-ID-FORMAT#field_delete#0` | `ATOM-ID-FORMAT` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | id | `ATOM-ID-FORMAT` |
| `ATOM-ID-FORMAT#format_perturb#1` | `ATOM-ID-FORMAT` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `format_perturb` | type | `ATOM-ID-FORMAT` |
| `ATOM-ID-FORMAT#break_ref#2` | `ATOM-ID-FORMAT` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `break_ref` | id | `ATOM-ID-FORMAT` |
| `ATOM-ID-FORMAT#equiv_rewrite#3` | `ATOM-ID-FORMAT` | B | `atoms/hist/ATOM-HIST-AUTOPTR-001.md` | `equiv_rewrite` | type | `ATOM-ID-FORMAT` |
| `ATOM-ID-UNIQUE#field_delete#0` | `ATOM-ID-UNIQUE` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | id | `ATOM-ID-UNIQUE` |
| `ATOM-ID-UNIQUE#break_ref#1` | `ATOM-ID-UNIQUE` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `break_ref` | status | `ATOM-ID-UNIQUE` |
| `ATOM-ID-UNIQUE#equiv_rewrite#2` | `ATOM-ID-UNIQUE` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `equiv_rewrite` | id | `ATOM-ID-UNIQUE` |
| `ATOM-VERIFIED-BOUND#field_delete#0` | `ATOM-VERIFIED-BOUND` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | evidence | `ATOM-VERIFIED-BOUND` |
| `ATOM-VERIFIED-BOUND#break_ref#1` | `ATOM-VERIFIED-BOUND` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `break_ref` | first_hand | `ATOM-VERIFIED-BOUND` |
| `ATOM-VERIFIED-BOUND#equiv_rewrite#2` | `ATOM-VERIFIED-BOUND` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `equiv_rewrite` | status | `ATOM-VERIFIED-BOUND` |
| `ATOM-NO-UNVERIFIED#field_delete#0` | `ATOM-NO-UNVERIFIED` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | status | `ATOM-NO-UNVERIFIED` |
| `ATOM-NO-UNVERIFIED#break_ref#1` | `ATOM-NO-UNVERIFIED` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `break_ref` | status | `ATOM-NO-UNVERIFIED` |
| `ATOM-NO-UNVERIFIED#equiv_rewrite#2` | `ATOM-NO-UNVERIFIED` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `equiv_rewrite` | status | `ATOM-NO-UNVERIFIED` |
| `ATOM-STATUS-VALUE#field_delete#0` | `ATOM-STATUS-VALUE` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | status | `ATOM-STATUS-VALUE` |
| `ATOM-STATUS-VALUE#break_ref#1` | `ATOM-STATUS-VALUE` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `break_ref` | status | `ATOM-STATUS-VALUE` |
| `ATOM-STATUS-VALUE#equiv_rewrite#2` | `ATOM-STATUS-VALUE` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `equiv_rewrite` | status | `ATOM-STATUS-VALUE` |
| `ATOM-STATUS-TRANSITION#field_delete#0` | `ATOM-STATUS-TRANSITION` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | status | `ATOM-STATUS-TRANSITION` |
| `ATOM-STATUS-TRANSITION#format_perturb#1` | `ATOM-STATUS-TRANSITION` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `format_perturb` | status_history | `ATOM-STATUS-TRANSITION` |
| `ATOM-STATUS-TRANSITION#value_tamper#2` | `ATOM-STATUS-TRANSITION` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `value_tamper` | status | `ATOM-STATUS-TRANSITION` |
| `ATOM-STATUS-TRANSITION#break_ref#3` | `ATOM-STATUS-TRANSITION` | B | `atoms/hist/ATOM-HIST-AUTOPTR-001.md` | `break_ref` | status_history | `ATOM-STATUS-TRANSITION` |
| `ATOM-STATUS-TRANSITION#equiv_rewrite#4` | `ATOM-STATUS-TRANSITION` | B | `atoms/lang/ATOM-LANG-INLINE-001.md` | `equiv_rewrite` | status | `ATOM-STATUS-TRANSITION` |
| `ATOM-DAL-MATCH#field_delete#0` | `ATOM-DAL-MATCH` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | dal | `ATOM-DAL-MATCH` |
| `ATOM-DAL-MATCH#break_ref#1` | `ATOM-DAL-MATCH` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `break_ref` | status | `ATOM-DAL-MATCH` |
| `ATOM-DAL-MATCH#equiv_rewrite#2` | `ATOM-DAL-MATCH` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `equiv_rewrite` | dal | `ATOM-DAL-MATCH` |
| `ATOM-REL-TARGET#field_delete#0` | `ATOM-REL-TARGET` | A | `atoms/ub/ATOM-UB-GRAY-001.md` | `field_delete` | id | `ATOM-REL-TARGET` |
| `ATOM-REL-TARGET#break_ref#1` | `ATOM-REL-TARGET` | A | `atoms/ub/ATOM-UB-GRAY-001.md` | `break_ref` | relations | `ATOM-REL-TARGET` |
| `ATOM-REL-TARGET#equiv_rewrite#2` | `ATOM-REL-TARGET` | A | `atoms/ub/ATOM-UB-GRAY-001.md` | `equiv_rewrite` | target | `ATOM-REL-TARGET` |
| `ATOM-REL-DAG#field_delete#0` | `ATOM-REL-DAG` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | id | `ATOM-REL-DAG` |
| `ATOM-REL-DAG#value_tamper#1` | `ATOM-REL-DAG` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `value_tamper` | target | `ATOM-REL-DAG` |
| `ATOM-REL-DAG#break_ref#2` | `ATOM-REL-DAG` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `break_ref` | type | `ATOM-REL-DAG` |
| `ATOM-REL-DAG#equiv_rewrite#3` | `ATOM-REL-DAG` | B | `atoms/hist/ATOM-HIST-AUTOPTR-001.md` | `equiv_rewrite` | id | `ATOM-REL-DAG` |
| `ATOM-REL-CONFLICT#field_delete#0` | `ATOM-REL-CONFLICT` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | claim | `ATOM-REL-CONFLICT` |
| `ATOM-REL-CONFLICT#break_ref#1` | `ATOM-REL-CONFLICT` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `break_ref` | id | `ATOM-REL-CONFLICT` |
| `ATOM-REL-CONFLICT#equiv_rewrite#2` | `ATOM-REL-CONFLICT` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `equiv_rewrite` | relations | `ATOM-REL-CONFLICT` |
| `ATOM-SUPERIORITY-WORDS#field_delete#0` | `ATOM-SUPERIORITY-WORDS` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | superiority | `ATOM-SUPERIORITY-WORDS` |
| `ATOM-SUPERIORITY-WORDS#break_ref#1` | `ATOM-SUPERIORITY-WORDS` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `break_ref` | superiority | `ATOM-SUPERIORITY-WORDS` |
| `ATOM-SUPERIORITY-WORDS#equiv_rewrite#2` | `ATOM-SUPERIORITY-WORDS` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `equiv_rewrite` | superiority | `ATOM-SUPERIORITY-WORDS` |
| `ATOM-GRAY-ZONE#field_delete#0` | `ATOM-GRAY-ZONE` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | domain | `ATOM-GRAY-ZONE` |
| `ATOM-GRAY-ZONE#break_ref#1` | `ATOM-GRAY-ZONE` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `break_ref` | domain | `ATOM-GRAY-ZONE` |
| `ATOM-GRAY-ZONE#equiv_rewrite#2` | `ATOM-GRAY-ZONE` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `equiv_rewrite` | domain | `ATOM-GRAY-ZONE` |
| `ATOM-MISCONCEPTION-LEVELS#field_delete#0` | `ATOM-MISCONCEPTION-LEVELS` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | pedagogy | `ATOM-MISCONCEPTION-LEVELS` |
| `ATOM-MISCONCEPTION-LEVELS#value_tamper#1` | `ATOM-MISCONCEPTION-LEVELS` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `value_tamper` | pedagogy | `ATOM-MISCONCEPTION-LEVELS` |
| `ATOM-MISCONCEPTION-LEVELS#break_ref#2` | `ATOM-MISCONCEPTION-LEVELS` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `break_ref` | pedagogy | `ATOM-MISCONCEPTION-LEVELS` |
| `ATOM-MISCONCEPTION-LEVELS#equiv_rewrite#3` | `ATOM-MISCONCEPTION-LEVELS` | B | `atoms/hist/ATOM-HIST-AUTOPTR-001.md` | `equiv_rewrite` | pedagogy | `ATOM-MISCONCEPTION-LEVELS` |
| `MIS-LIBRARY#field_delete#0` | `MIS-LIBRARY` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | id | `MIS-LIBRARY` |
| `MIS-LIBRARY#value_tamper#1` | `MIS-LIBRARY` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `value_tamper` | id | `MIS-LIBRARY` |
| `MIS-LIBRARY#break_ref#2` | `MIS-LIBRARY` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `break_ref` | id | `MIS-LIBRARY` |
| `MIS-LIBRARY#equiv_rewrite#3` | `MIS-LIBRARY` | B | `atoms/hist/ATOM-HIST-AUTOPTR-001.md` | `equiv_rewrite` | id | `MIS-LIBRARY` |
| `ATOM-MISCONCEPTION-REF#field_delete#0` | `ATOM-MISCONCEPTION-REF` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | pedagogy | `ATOM-MISCONCEPTION-REF` |
| `ATOM-MISCONCEPTION-REF#break_ref#1` | `ATOM-MISCONCEPTION-REF` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `break_ref` | pedagogy | `ATOM-MISCONCEPTION-REF` |
| `ATOM-MISCONCEPTION-REF#equiv_rewrite#2` | `ATOM-MISCONCEPTION-REF` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `equiv_rewrite` | pedagogy | `ATOM-MISCONCEPTION-REF` |
| `ATOM-AUDIENCE#format_perturb#0` | `ATOM-AUDIENCE` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `format_perturb` | — | `ATOM-AUDIENCE` |
| `ATOM-AUDIENCE#break_ref#1` | `ATOM-AUDIENCE` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `break_ref` | — | `ATOM-AUDIENCE` |
| `ATOM-AUDIENCE#equiv_rewrite#2` | `ATOM-AUDIENCE` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `equiv_rewrite` | — | `ATOM-AUDIENCE` |
| `ATOM-PREREQ-READABLE#field_delete#0` | `ATOM-PREREQ-READABLE` | B | `atoms/conc/ATOM-CONC-FENCE-001.md` | `field_delete` | id | `ATOM-PREREQ-READABLE` |
| `ATOM-PREREQ-READABLE#break_ref#1` | `ATOM-PREREQ-READABLE` | B | `atoms/conc/ATOM-CONC-LOCK-001.md` | `break_ref` | target | `ATOM-PREREQ-READABLE` |
| `ATOM-PREREQ-READABLE#equiv_rewrite#2` | `ATOM-PREREQ-READABLE` | B | `atoms/conc/ATOM-CONC-RACE-001.md` | `equiv_rewrite` | type | `ATOM-PREREQ-READABLE` |

## 诚实登记

1. **`expected_oracle` 是生成器猜的**（§十二.7）：可能预期错了（以为该被规则 A 拦，实际由规则 B 拦）⇒ C3 实测后**记录 `oracle_mismatch`，但不改预期**；
2. **空变异存在**：某个算子在该卡上找不到可改对象时返回原文（说明串已标注）⇒ C3 会把它们计为 `noop`，**不计入逃逸**；
3. **方向 B 的语义**：规则不命中**可能**是「卡本来就合规」（好事），所以 B 的失败**不等于**规则坏 —— 只作「**不可达候选**」线索；
4. **本批只对 `scope=atom` 的规则生成**（evidence/repo 面的变异需要不同的载体策略，留 644+）⇒ 覆盖规则数小于 67；
5. 本工具**不读写生产卡片**：`apply_op` 是**纯文本函数**（输入输出都是字符串），真正落盘只在 C3 的临时沙箱里发生。

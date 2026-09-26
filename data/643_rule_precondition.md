# 643 C1 · 规则 precondition 分析（智能层：自动生成攻击 #1）

> 规模：**67 条规则**；成功映射到 `check` 函数 **61** 条，未映射 **6** 条。
> **限制**：规则条件是**内嵌闭包**（无声明式 precondition）⇒ 本分析是**静态近似**，不是语义解析。

## 一、盲点分布

| 盲点类别 | 规则数 | 含义 |
|---|---|---|
| `cross_card_dependency` | **57** | 依赖跨卡/目录遍历 ⇒ 单卡损伤不触发 |
| `field_missing_silent` | **44** | 引用字段但可能没有「缺失即报」分支 ⇒ 静默跳过 |
| `regex_fragile` | **15** | 正则可被格式微扰绕过 |
| `numeric_threshold` | **14** | 数值阈值可被压线值绕过 |
| `path_scope_only` | **7** | scope=repo ⇒ 与单卡变异不同量纲 |

**零盲点规则**（5 条）：`PED-MOTIVATION`, `PED-SOCRATIC`, `PED-PREDICT-FIRST`, `LLM-SUPERIORITY-QUALITY`, `HYBRID-TEACHING-DEPTH`

## 二、字段引用直方图（被最多规则引用的字段 = 攻击面最集中的字段）

| 字段 | 引用它的规则数 |
|---|---|
| `id` | 17 |
| `status` | 9 |
| `falsification` | 5 |
| `relations` | 5 |
| `target` | 5 |
| `type` | 5 |
| `evidence` | 4 |
| `artifact` | 3 |
| `claim` | 3 |
| `pedagogy` | 3 |
| `status_history` | 3 |
| `claim_boundary` | 2 |
| `kind` | 2 |
| `run_match` | 2 |
| `serves` | 2 |
| `superiority` | 2 |
| `dal` | 1 |
| `domain` | 1 |
| `first_hand` | 1 |
| `key` | 1 |

## 三、逐规则 precondition + 盲点

| 规则 | 级别 | scope | check 函数 | 引用字段 | 跨卡 | 正则 | 数值阈值 | 盲点数 |
|---|---|---|---|---|---|---|---|---|
| `ATOM-FM-REQUIRED` | block | atom | `check_atom_frontmatter` | sources | ✅ | — | — | 2 |
| `ATOM-ID-FORMAT` | block | atom | `check_atom_id_format` | id, type | ✅ | ✅ | — | 3 |
| `ATOM-ID-UNIQUE` | block | atom | `check_atom_id_unique` | id, status | ✅ | — | — | 2 |
| `ATOM-VERIFIED-BOUND` | block | atom | `check_verified_bound` | evidence, first_hand, status, superiority | ✅ | — | — | 2 |
| `ATOM-NO-UNVERIFIED` | block | atom | `check_no_unverified_status` | status | ✅ | — | — | 2 |
| `ATOM-STATUS-VALUE` | block | atom | `check_status_value` | status | ✅ | — | — | 2 |
| `ATOM-STATUS-TRANSITION` | block | atom | `check_status_transition` | status, status_history | ✅ | ✅ | ✅ | 4 |
| `ATOM-DAL-MATCH` | block | atom | `check_dal_match` | dal, status | ✅ | — | — | 2 |
| `ATOM-REL-TARGET` | warn | atom | `check_relations_target_exists` | id, relations, target | ✅ | — | — | 2 |
| `ATOM-REL-DAG` | block | atom | `check_relations_dag` | id, target, type | ✅ | — | ✅ | 3 |
| `ATOM-REL-CONFLICT` | block | atom | `check_atom_rel_conflict` | claim, id, relations, target | ✅ | — | — | 2 |
| `ATOM-SUPERIORITY-WORDS` | block | atom | `check_superiority_banned_words` | superiority | ✅ | — | — | 2 |
| `EV-FM-REQUIRED` | block | evidence | `check_evidence_frontmatter` | kind | ✅ | — | — | 2 |
| `EV-ID-UNIQUE` | block | evidence | `check_evidence_id_unique` | id | ✅ | — | — | 2 |
| `EV-FALSIFICATION` | block | evidence | `check_evidence_falsification` | falsification | ✅ | — | — | 2 |
| `EV-MATRIX` | block | evidence | `check_evidence_matrix` | — | ✅ | — | ✅ | 2 |
| `ATOM-GRAY-ZONE` | block | atom | `check_atom_gray_zone` | domain | ✅ | — | — | 2 |
| `ATOM-MISCONCEPTION-LEVELS` | block | atom | `check_misconception_levels` | pedagogy | ✅ | — | ✅ | 3 |
| `MIS-LIBRARY` | block | atom | `check_mis_library` | id | ✅ | — | ✅ | 3 |
| `ATOM-MISCONCEPTION-REF` | block | atom | `check_misconception_ref` | pedagogy | ✅ | — | — | 2 |
| `ATOM-AUDIENCE` | block | atom | `check_audience` | — | ✅ | ✅ | — | 2 |
| `ATOM-PREREQ-READABLE` | block | atom | `check_prereq_readable` | id, target, type | ✅ | — | — | 2 |
| `EV-SERVES-EXIST` | warn | evidence | `check_evidence_serves_exist` | id, serves | ✅ | — | — | 2 |
| `DOC-ZERO-PLACEHOLDER` | block | repo | `check_zero_placeholder` | — | ✅ | ✅ | — | 3 |
| `META-MANIFEST` | warn | repo | `check_manifest_consistency` | — | ✅ | ✅ | — | 3 |
| `S1-AUTHOR-SELF-VERIFY` | block | atom | `check_s1_human_signoff` | status | ✅ | — | — | 2 |
| `S1-GIT-AUTHOR-BINDING` | warn | atom | `check_git_author_binding` | status_history | ✅ | — | — | 2 |
| `ATOM-VERIFY-REASON` | warn | atom | `check_verify_reason` | id, status | ✅ | — | — | 2 |
| `EV-ARTIFACT-VERSION-MATCH` | block | evidence | `check_artifact_version_match` | artifact | ✅ | — | — | 2 |
| `S2-EVIDENCE-VERDICT` | block | atom | `check_s2_evidence_verdict` | evidence, id | ✅ | — | — | 2 |
| `S3-EXPECTED-HARDCODED` | block | evidence | `check_s3_hardcoded_expected` | — | ✅ | — | ✅ | 2 |
| `EV-SELF-SATISFIED-ASSERT` | warn | evidence | `check_evidence_self_satisfied_assert` | — | ✅ | ✅ | ✅ | 3 |
| `EV-FALSIFICATION-QUANT` | warn | evidence | `check_evidence_falsification_quantified` | falsification | ✅ | ✅ | — | 3 |
| `EV-TRIVIAL-OBSERVATION` | warn | evidence | `check_evidence_trivial_observation` | claim | ✅ | ✅ | ✅ | 4 |
| `EV-MATRIX-UNBACKED` | warn | evidence | `check_evidence_matrix_backed` | — | ✅ | ✅ | ✅ | 3 |
| `EV-ZERO-DIAG-WERROR` | block | evidence | `check_evidence_zero_diag_werror` | claim_boundary, falsification | ✅ | ✅ | — | 3 |
| `EV-WERROR-DECL-BIND` | block | evidence | `check_evidence_werror_decl_binding` | claim_boundary, falsification | ✅ | ✅ | ✅ | 4 |
| `EV-ASSERT-COUNT-BELOW-BASELINE` | block | evidence | `check_evidence_assert_count_baseline` | — | ✅ | — | — | 1 |
| `EV-OUT-UNDECLARED-KEY` | warn | evidence | `check_evidence_out_undeclared_key` | key | ✅ | ✅ | — | 3 |
| `EV-RUN-KEY-DECLARED-EXISTS` | block | evidence | `check_run_key_declared_exists` | — | ✅ | — | — | 1 |
| `EV-ASSERT-SYMBOL-MAPPED` | block | evidence | `check_evidence_assert_symbol_mapped` | kind | ✅ | ✅ | ✅ | 4 |
| `EV-ARTIFACT-PRODUCER` | block | evidence | `check_evidence_artifact_producer` | artifact, id | ✅ | ✅ | ✅ | 4 |
| `EV-ARTIFACT-FILE-EXISTS` | block | evidence | `check_artifact_file_exists` | artifact, run_match | ✅ | — | — | 2 |
| `EV-MSCV-NO-VERIFY` | block | evidence | `check_evidence_msvc_no_verify` | — | ✅ | — | — | 1 |
| `EV-FM-DUP-KEY` | block | repo | `check_frontmatter_duplicate_key` | — | ✅ | ✅ | — | 3 |
| `EV-FM-YAML-HARDENING` | block | repo | `check_frontmatter_hardening` | — | ✅ | — | — | 2 |
| `EV-ENV-DEPENDENT-KEY` | block | evidence | `check_env_dependent_key` | — | ✅ | — | — | 1 |
| `ATOM-REL-UNKNOWN` | warn | atom | `check_relations_unknown_type` | relations, target, type | ✅ | — | — | 2 |
| `ATOM-CLAIM-STRUCTURED` | block | atom | `check_atom_claim_structured` | claim, id | ✅ | — | — | 2 |
| `OBSERVATION-NEEDS-ARTIFACT` | block | atom | `check_observation_needs_artifact` | evidence, id | ✅ | — | — | 2 |
| `INFERENCE-NOT-MACHINE-VERIFIED` | block | atom | `check_inference_not_machine_verified` | id, status, status_history | ✅ | — | ✅ | 3 |
| `ATOM-CLAIM-CONCEPT-NORMALIZED` | warn | atom | `check_claim_concept_normalized` | id | ✅ | — | — | 2 |
| `OBSERVATION-LIVENESS` | warn | atom | `check_observation_liveness` | evidence, falsification, id, run_match | ✅ | — | — | 2 |
| `EV-FIXTURE-NO-ECHO-DATA` | warn | evidence | `check_fixture_no_echo_findings` | — | ✅ | — | — | 1 |
| `EV-OUT-STALE-MTIME` | warn | evidence | `check_evidence_out_stale_mtime` | — | ✅ | — | ✅ | 2 |
| `CARD-PATH-NOT-CANONICAL` | warn | repo | `check_card_path_canonical` | — | ✅ | — | — | 2 |
| `EV-SERVES-EXIST-HC` | block | evidence | `check_evidence_serves_exist_hc` | serves | — | — | — | 1 |
| `ATOM-REL-TARGET-HC` | block | atom | `check_relations_target_exists_hc` | relations | — | — | — | 1 |
| `ATOM-REL-UNKNOWN-HC` | block | atom | `check_relations_unknown_type_hc` | relations | — | — | — | 1 |
| `CARD-PATH-NOT-CANONICAL-HC` | block | repo | `check_card_path_canonical_hc` | — | — | — | — | 1 |
| `PED-MOTIVATION` | advice | atom | `—` | — | — | — | — | 0 |
| `PED-MISCONCEPTION` | advice | atom | `_misconception_gap` | pedagogy | ✅ | — | — | 2 |
| `PED-SOCRATIC` | advice | atom | `—` | — | — | — | — | 0 |
| `PED-PREDICT-FIRST` | advice | atom | `—` | — | — | — | — | 0 |
| `LLM-SUPERIORITY-QUALITY` | advice | atom | `—` | — | — | — | — | 0 |
| `HYBRID-TEACHING-DEPTH` | advice | atom | `—` | — | — | — | — | 0 |
| `HUMAN-GOLDEN-REVIEW` | advice | repo | `—` | — | — | — | — | 1 |

## 四、盲点明细（逐条 why）

| 规则 | 盲点 | 理由 |
|---|---|---|
| `ATOM-FM-REQUIRED` | `field_missing_silent` | 规则引用字段 sources；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-FM-REQUIRED` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-ID-FORMAT` | `field_missing_silent` | 规则引用字段 id, type；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-ID-FORMAT` | `regex_fragile` | 函数体有 2 处正则调用 ⇒ 格式微扰可能绕过 |
| `ATOM-ID-FORMAT` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-ID-UNIQUE` | `field_missing_silent` | 规则引用字段 id, status；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-ID-UNIQUE` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-VERIFIED-BOUND` | `field_missing_silent` | 规则引用字段 evidence, first_hand, status, superiority；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-VERIFIED-BOUND` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-NO-UNVERIFIED` | `field_missing_silent` | 规则引用字段 status；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-NO-UNVERIFIED` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-STATUS-VALUE` | `field_missing_silent` | 规则引用字段 status；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-STATUS-VALUE` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-STATUS-TRANSITION` | `field_missing_silent` | 规则引用字段 status, status_history；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-STATUS-TRANSITION` | `regex_fragile` | 函数体有 1 处正则调用 ⇒ 格式微扰可能绕过 |
| `ATOM-STATUS-TRANSITION` | `numeric_threshold` | 数值常量 [2.0] ⇒ 值篡改可能刚好压线 |
| `ATOM-STATUS-TRANSITION` | `cross_card_dependency` | 循环 2 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-DAL-MATCH` | `field_missing_silent` | 规则引用字段 dal, status；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-DAL-MATCH` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-REL-TARGET` | `field_missing_silent` | 规则引用字段 id, relations, target；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-REL-TARGET` | `cross_card_dependency` | 循环 3 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-REL-DAG` | `field_missing_silent` | 规则引用字段 id, target, type；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-REL-DAG` | `numeric_threshold` | 数值常量 [2.0] ⇒ 值篡改可能刚好压线 |
| `ATOM-REL-DAG` | `cross_card_dependency` | 循环 4 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-REL-CONFLICT` | `field_missing_silent` | 规则引用字段 claim, id, relations, target …；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-REL-CONFLICT` | `cross_card_dependency` | 循环 5 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-SUPERIORITY-WORDS` | `field_missing_silent` | 规则引用字段 superiority；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-SUPERIORITY-WORDS` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-FM-REQUIRED` | `field_missing_silent` | 规则引用字段 kind；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `EV-FM-REQUIRED` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-ID-UNIQUE` | `field_missing_silent` | 规则引用字段 id；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `EV-ID-UNIQUE` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-FALSIFICATION` | `field_missing_silent` | 规则引用字段 falsification；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `EV-FALSIFICATION` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-MATRIX` | `numeric_threshold` | 数值常量 [3.0] ⇒ 值篡改可能刚好压线 |
| `EV-MATRIX` | `cross_card_dependency` | 循环 2 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-GRAY-ZONE` | `field_missing_silent` | 规则引用字段 domain；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-GRAY-ZONE` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-MISCONCEPTION-LEVELS` | `field_missing_silent` | 规则引用字段 pedagogy；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-MISCONCEPTION-LEVELS` | `numeric_threshold` | 数值常量 [2.0, 40.0] ⇒ 值篡改可能刚好压线 |
| `ATOM-MISCONCEPTION-LEVELS` | `cross_card_dependency` | 循环 2 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `MIS-LIBRARY` | `field_missing_silent` | 规则引用字段 id；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `MIS-LIBRARY` | `numeric_threshold` | 数值常量 [2.0] ⇒ 值篡改可能刚好压线 |
| `MIS-LIBRARY` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-MISCONCEPTION-REF` | `field_missing_silent` | 规则引用字段 pedagogy；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-MISCONCEPTION-REF` | `cross_card_dependency` | 循环 2 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-AUDIENCE` | `regex_fragile` | 函数体有 1 处正则调用 ⇒ 格式微扰可能绕过 |
| `ATOM-AUDIENCE` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-PREREQ-READABLE` | `field_missing_silent` | 规则引用字段 id, target, type；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-PREREQ-READABLE` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-SERVES-EXIST` | `field_missing_silent` | 规则引用字段 id, serves；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `EV-SERVES-EXIST` | `cross_card_dependency` | 循环 2 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `DOC-ZERO-PLACEHOLDER` | `regex_fragile` | 函数体有 1 处正则调用 ⇒ 格式微扰可能绕过 |
| `DOC-ZERO-PLACEHOLDER` | `cross_card_dependency` | 循环 3 处 / 目录遍历 1 处 ⇒ 单卡损伤可能不触发 |
| `DOC-ZERO-PLACEHOLDER` | `path_scope_only` | scope=repo ⇒ 与单卡变异不同量纲，C2 生成时应降权 |
| `META-MANIFEST` | `regex_fragile` | 函数体有 1 处正则调用 ⇒ 格式微扰可能绕过 |
| `META-MANIFEST` | `cross_card_dependency` | 循环 2 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `META-MANIFEST` | `path_scope_only` | scope=repo ⇒ 与单卡变异不同量纲，C2 生成时应降权 |
| `S1-AUTHOR-SELF-VERIFY` | `field_missing_silent` | 规则引用字段 status；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `S1-AUTHOR-SELF-VERIFY` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `S1-GIT-AUTHOR-BINDING` | `field_missing_silent` | 规则引用字段 status_history；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `S1-GIT-AUTHOR-BINDING` | `cross_card_dependency` | 循环 3 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-VERIFY-REASON` | `field_missing_silent` | 规则引用字段 id, status；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-VERIFY-REASON` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-ARTIFACT-VERSION-MATCH` | `field_missing_silent` | 规则引用字段 artifact；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `EV-ARTIFACT-VERSION-MATCH` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `S2-EVIDENCE-VERDICT` | `field_missing_silent` | 规则引用字段 evidence, id；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `S2-EVIDENCE-VERDICT` | `cross_card_dependency` | 循环 2 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `S3-EXPECTED-HARDCODED` | `numeric_threshold` | 数值常量 [6.0, 40.0] ⇒ 值篡改可能刚好压线 |
| `S3-EXPECTED-HARDCODED` | `cross_card_dependency` | 循环 2 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-SELF-SATISFIED-ASSERT` | `regex_fragile` | 函数体有 1 处正则调用 ⇒ 格式微扰可能绕过 |
| `EV-SELF-SATISFIED-ASSERT` | `numeric_threshold` | 数值常量 [3.0] ⇒ 值篡改可能刚好压线 |
| `EV-SELF-SATISFIED-ASSERT` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-FALSIFICATION-QUANT` | `field_missing_silent` | 规则引用字段 falsification；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `EV-FALSIFICATION-QUANT` | `regex_fragile` | 函数体有 1 处正则调用 ⇒ 格式微扰可能绕过 |
| `EV-FALSIFICATION-QUANT` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-TRIVIAL-OBSERVATION` | `field_missing_silent` | 规则引用字段 claim；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `EV-TRIVIAL-OBSERVATION` | `regex_fragile` | 函数体有 1 处正则调用 ⇒ 格式微扰可能绕过 |
| `EV-TRIVIAL-OBSERVATION` | `numeric_threshold` | 数值常量 [3.0] ⇒ 值篡改可能刚好压线 |
| `EV-TRIVIAL-OBSERVATION` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-MATRIX-UNBACKED` | `regex_fragile` | 函数体有 8 处正则调用 ⇒ 格式微扰可能绕过 |
| `EV-MATRIX-UNBACKED` | `numeric_threshold` | 数值常量 [2.0] ⇒ 值篡改可能刚好压线 |
| `EV-MATRIX-UNBACKED` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-ZERO-DIAG-WERROR` | `field_missing_silent` | 规则引用字段 claim_boundary, falsification；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `EV-ZERO-DIAG-WERROR` | `regex_fragile` | 函数体有 1 处正则调用 ⇒ 格式微扰可能绕过 |
| `EV-ZERO-DIAG-WERROR` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-WERROR-DECL-BIND` | `field_missing_silent` | 规则引用字段 claim_boundary, falsification；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `EV-WERROR-DECL-BIND` | `regex_fragile` | 函数体有 4 处正则调用 ⇒ 格式微扰可能绕过 |
| `EV-WERROR-DECL-BIND` | `numeric_threshold` | 数值常量 [72.0] ⇒ 值篡改可能刚好压线 |
| `EV-WERROR-DECL-BIND` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-ASSERT-COUNT-BELOW-BASELINE` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-OUT-UNDECLARED-KEY` | `field_missing_silent` | 规则引用字段 key；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `EV-OUT-UNDECLARED-KEY` | `regex_fragile` | 函数体有 1 处正则调用 ⇒ 格式微扰可能绕过 |
| `EV-OUT-UNDECLARED-KEY` | `cross_card_dependency` | 循环 2 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-RUN-KEY-DECLARED-EXISTS` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-ASSERT-SYMBOL-MAPPED` | `field_missing_silent` | 规则引用字段 kind；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `EV-ASSERT-SYMBOL-MAPPED` | `regex_fragile` | 函数体有 4 处正则调用 ⇒ 格式微扰可能绕过 |
| `EV-ASSERT-SYMBOL-MAPPED` | `numeric_threshold` | 数值常量 [2.0] ⇒ 值篡改可能刚好压线 |
| `EV-ASSERT-SYMBOL-MAPPED` | `cross_card_dependency` | 循环 5 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-ARTIFACT-PRODUCER` | `field_missing_silent` | 规则引用字段 artifact, id；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `EV-ARTIFACT-PRODUCER` | `regex_fragile` | 函数体有 1 处正则调用 ⇒ 格式微扰可能绕过 |
| `EV-ARTIFACT-PRODUCER` | `numeric_threshold` | 数值常量 [88.0] ⇒ 值篡改可能刚好压线 |
| `EV-ARTIFACT-PRODUCER` | `cross_card_dependency` | 循环 3 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-ARTIFACT-FILE-EXISTS` | `field_missing_silent` | 规则引用字段 artifact, run_match；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `EV-ARTIFACT-FILE-EXISTS` | `cross_card_dependency` | 循环 2 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-MSCV-NO-VERIFY` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-FM-DUP-KEY` | `regex_fragile` | 函数体有 1 处正则调用 ⇒ 格式微扰可能绕过 |
| `EV-FM-DUP-KEY` | `cross_card_dependency` | 循环 3 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-FM-DUP-KEY` | `path_scope_only` | scope=repo ⇒ 与单卡变异不同量纲，C2 生成时应降权 |
| `EV-FM-YAML-HARDENING` | `cross_card_dependency` | 循环 3 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-FM-YAML-HARDENING` | `path_scope_only` | scope=repo ⇒ 与单卡变异不同量纲，C2 生成时应降权 |
| `EV-ENV-DEPENDENT-KEY` | `cross_card_dependency` | 循环 2 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-REL-UNKNOWN` | `field_missing_silent` | 规则引用字段 relations, target, type；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-REL-UNKNOWN` | `cross_card_dependency` | 循环 3 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-CLAIM-STRUCTURED` | `field_missing_silent` | 规则引用字段 claim, id；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-CLAIM-STRUCTURED` | `cross_card_dependency` | 循环 2 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `OBSERVATION-NEEDS-ARTIFACT` | `field_missing_silent` | 规则引用字段 evidence, id；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `OBSERVATION-NEEDS-ARTIFACT` | `cross_card_dependency` | 循环 2 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `INFERENCE-NOT-MACHINE-VERIFIED` | `field_missing_silent` | 规则引用字段 id, status, status_history；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `INFERENCE-NOT-MACHINE-VERIFIED` | `numeric_threshold` | 数值常量 [60.0] ⇒ 值篡改可能刚好压线 |
| `INFERENCE-NOT-MACHINE-VERIFIED` | `cross_card_dependency` | 循环 2 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `ATOM-CLAIM-CONCEPT-NORMALIZED` | `field_missing_silent` | 规则引用字段 id；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-CLAIM-CONCEPT-NORMALIZED` | `cross_card_dependency` | 循环 2 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `OBSERVATION-LIVENESS` | `field_missing_silent` | 规则引用字段 evidence, falsification, id, run_match；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `OBSERVATION-LIVENESS` | `cross_card_dependency` | 循环 2 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-FIXTURE-NO-ECHO-DATA` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `EV-OUT-STALE-MTIME` | `numeric_threshold` | 数值常量 [5.0] ⇒ 值篡改可能刚好压线 |
| `EV-OUT-STALE-MTIME` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `CARD-PATH-NOT-CANONICAL` | `cross_card_dependency` | 循环 4 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `CARD-PATH-NOT-CANONICAL` | `path_scope_only` | scope=repo ⇒ 与单卡变异不同量纲，C2 生成时应降权 |
| `EV-SERVES-EXIST-HC` | `field_missing_silent` | 规则引用字段 serves；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-REL-TARGET-HC` | `field_missing_silent` | 规则引用字段 relations；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `ATOM-REL-UNKNOWN-HC` | `field_missing_silent` | 规则引用字段 relations；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `CARD-PATH-NOT-CANONICAL-HC` | `path_scope_only` | scope=repo ⇒ 与单卡变异不同量纲，C2 生成时应降权 |
| `PED-MISCONCEPTION` | `field_missing_silent` | 规则引用字段 pedagogy；若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过 |
| `PED-MISCONCEPTION` | `cross_card_dependency` | 循环 1 处 / 目录遍历 0 处 ⇒ 单卡损伤可能不触发 |
| `HUMAN-GOLDEN-REVIEW` | `path_scope_only` | scope=repo ⇒ 与单卡变异不同量纲，C2 生成时应降权 |

## 诚实登记

1. **静态近似 ≠ 真实 precondition**：规则条件是闭包，本工具只能看**字符串字面量/调用形态/数值常量**；`fields` 的识别依赖内置字段名表，**可能漏**（自定义字段名不在表内）也可能**误收**（注释/消息文本里的词）；
2. **盲点是「可能性」不是「已证缺陷」**：`field_missing_silent` 只说明「引用字段」这一事实，**没有**证明该规则缺「缺失即报」分支（要证明需逐规则读代码）⇒ 全部盲点必须人核后才可作为 C2 的目标；
3. **未映射的规则**（`n_unmapped>0`）说明注册形态超出本工具的两种模式，它们**没有** precondition 分析结果 ⇒ C2 应跳过；
4. 本工具**只读** `gate_engine.py`：不改规则、不重钉台账、不生成任何攻击。

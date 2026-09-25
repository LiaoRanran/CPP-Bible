# 624 任务0 · 开工基线台账

> 批次：624（突破天花板 + 修问题）· 前置：623 收工（`4ef44c19`，17/17，awaiting_review）
> 解释器：`.venv\Scripts\python.exe`

---

## 一、快照计数（SNAPSHOT_MANIFEST.json）

| 项 | 值 |
|---|---|
| live_counts.commits | 1606 |
| live_counts.tools_py | 257 |
| live_counts.tests_py | 263 |
| live_counts.atoms_md | 28 |
| live_counts.evidence_ev_md | 56 |
| frozen.gate | rules 63 / hits 191 / block 0 / warn 186 / advice 5 |
| frozen.poison | 124/124（coverage honest 60/63） |
| frozen.replay | confirm 56 / refute 0 / infra 0 |
| frozen.mutation_v7 | variants 1593 / blocked 1405 / escaped 1 / judge_denom 1406 |
| frozen.human_review | total 388（approve 354 / modify 34 / reject 0） |
| frozen.trust_root | partially_anchored |

**实测校验**：`gate_engine.py --list` 输出 64 行（63 规则 + 表头）⇒ **规则数 63 确认**。
卡库存实测：`atoms/` 27 张、`evidence/` 56 张（含 README 不计）。

---

## 二、623 闭环触达明细（26/63）与 37 条盲区分类

### 2.1 已触达 26 条（block 21 / warn 5 / advice 0）

block：ATOM-FM-REQUIRED · ATOM-ID-FORMAT · ATOM-ID-UNIQUE · ATOM-NO-UNVERIFIED · ATOM-STATUS-VALUE · ATOM-DAL-MATCH · ATOM-REL-DAG · ATOM-GRAY-ZONE · ATOM-AUDIENCE · ATOM-PREREQ-READABLE · EV-FM-REQUIRED · EV-ID-UNIQUE · EV-MATRIX · EV-ARTIFACT-VERSION-MATCH · EV-ASSERT-COUNT-BELOW-BASELINE · EV-ASSERT-SYMBOL-MAPPED · EV-ARTIFACT-PRODUCER · EV-MSCV-NO-VERIFY · EV-FM-DUP-KEY · EV-FM-YAML-HARDENING · ATOM-CLAIM-STRUCTURED
warn：ATOM-REL-TARGET · EV-SERVES-EXIST · ATOM-VERIFY-REASON · ATOM-REL-UNKNOWN · CARD-PATH-NOT-CANONICAL

### 2.2 37 条盲区（block 19 / warn 11 / advice 7）按所需载体分类

| 所需载体 | 规则 | 说明 |
|---|---|---|
| **需多卡构造（624 A 线主攻）** | ATOM-REL-CONFLICT · OBSERVATION-NEEDS-ARTIFACT · INFERENCE-NOT-MACHINE-VERIFIED · ATOM-VERIFIED-BOUND · ATOM-MISCONCEPTION-REF · MIS-LIBRARY · ATOM-MISCONCEPTION-LEVELS · S2-EVIDENCE-VERDICT | 需跨卡引用/命题/误解库/证据-verdict 绑定 |
| **需编译/复算产物** | EV-ZERO-DIAG-WERROR · EV-WERROR-DECL-BIND · S3-EXPECTED-HARDCODED · EV-RUN-KEY-DECLARED-EXISTS · EV-ASSERT-SYMBOL-MAPPED(已 T) · EV-ARTIFACT-FILE-EXISTS · EV-ENV-DEPENDENT-KEY · EV-OUT-UNDECLARED-KEY · EV-OUT-STALE-MTIME · EV-FIXTURE-NO-ECHO-DATA | 需真实夹具/.out/编译产物 |
| **需 git 历史** | S1-AUTHOR-SELF-VERIFY · S1-GIT-AUTHOR-BINDING · META-MANIFEST | 需 git 作者/manifest 一致 |
| **需 provenance 链** | EV-ARTIFACT-FILE-EXISTS（同编译产物） | 需 sha256/artifact 实际存在 |
| **状态跃迁** | ATOM-STATUS-TRANSITION | 需 status_history 链 |
| **词表黑盒/文风** | ATOM-SUPERIORITY-WORDS · EV-FALSIFICATION · EV-FALSIFICATION-QUANT · EV-TRIVIAL-OBSERVATION · EV-MATRIX-UNBACKED · EV-SELF-SATISFIED-ASSERT · ATOM-CLAIM-CONCEPT-NORMALIZED · OBSERVATION-LIVENESS · DOC-ZERO-PLACEHOLDER | 需命中未逆向的词表 |
| **advice（不该被 field-edit 触发）** | PED-MOTIVATION · PED-MISCONCEPTION · PED-SOCRATIC · PED-PREDICT-FIRST · LLM-SUPERIORITY-QUALITY · HYBRID-TEACHING-DEPTH · HUMAN-GOLDEN-REVIEW | 教学设计/人审通道 |

> **A 线可现实触达的重点**：ATOM-REL-CONFLICT（X3 矛盾引用）、ATOM-MISCONCEPTION-REF（X4 孤儿误解引用）、ATOM-VERIFIED-BOUND/S2-EVIDENCE-VERDICT（跨卡证据绑定）、OBSERVATION-NEEDS-ARTIFACT / INFERENCE-NOT-MACHINE-VERIFIED（命题-工件）。

---

## 三、E2 高复杂度带 block 规则定义（623 遗留，待 624 B1 接线）

文件：`data/gate_rules_high_complexity_block_623.yaml`（**独立规则定义文件，未接入 gate_engine**）

| 规则 ID | severity | scope | promotes（既有 warn） | bind（既有 check 函数） |
|---|---|---|---|---|
| EV-SERVES-EXIST-HC | block | evidence | EV-SERVES-EXIST | check_evidence_serves_exist |
| ATOM-REL-TARGET-HC | block | atom | ATOM-REL-TARGET | check_relations_target_exists |
| ATOM-REL-UNKNOWN-HC | block | atom | ATOM-REL-UNKNOWN | check_relations_unknown_type |
| CARD-PATH-NOT-CANONICAL-HC | block | atom | CARD-PATH-NOT-CANONICAL | check_card_path_canonical |

**接线约束（B1）**：gate_engine.py 的 `Rule` 类字段为 `(id, title, kind, quadrant, severity, scope, check, basis, fix_hint, meta)`；规则在 `_register_all()` 内的 `fact` 列表（元组 `(rid,title,scope,fn)`）+ `sev` 覆盖表注册，默认 severity=block。既有 check 函数返回 `Finding(rule_id, severity, target, message, fix_hint)` 且内部硬编码 warn。
**约束**：接线后 `gate_engine.py --list` 须为 67；全库 gate 须 block=0（新规则零误伤存量卡）。
**受影响的既有测试（断言 63）**：`tests/test_618_b.py`、`test_high_complexity_attack_surface_623.py`、`test_rule_touch_heatmap_623.py`、`test_snapshot_manifest.py`、`test_output_snapshots.py` ⇒ 接线后须同步更新。

---

## 四、623 D2 W2 重算结果（8 原子 UNRESOLVED→IN）

原 annotations 67 原子 59 IN / 8 UNRESOLVED → synced 67 IN / 0 UNRESOLVED。
翻转原子：`ATOM-LANG-INLINE-001 / MIS-LANG-001 / MIS-MEM-001 / MIS-MEM-003 / MIS-UB-001 / MIS-UB-004 / MIS-UB-008 / MIS-UB-014`。
根因：原 34 条 `modify` 被 W2 当 UNRESOLVED，D1 合并 Authority（ACCEPT→approve）后转为 IN。

---

## 五、CI 远程状态（GitHub API）

| run | sha | 结论 | 时间 |
|---|---|---|---|
| **627** | 96fc0b8（622 push） | **failure** | 2026-09-22T05:25:42Z |
| 626 | d2f412b | failure | 2026-09-21T14:04:56Z |
| 625 | cbd0fbd | failure | 2026-09-21T08:57:33Z |
| 624 | cdd3b2d | failure | 2026-09-21T02:10:17Z |
| 623 | f2c3b33 | failure | 2026-09-21T02:00:36Z |

**结论**：远程 master HEAD = `96fc0b8`（622 push），**CI 自 #623 起长期红**；623/624 尚未 push。624 C1 需 push 后由 C2 验证是否转绿。

---

## 六、624 核心指标（对照）

| 指标 | 623 基线 | 624 目标 |
|---|---|---|
| 闭环累计触达规则 | 26/63（41.3%） | **>40/63（>63.5%）** |
| 六轮累计触达 | 26/63 | **>45/63（>71.4%）** |
| 盲区缩减 | 37 | **<25** |
| gate 规则数 | 63 | **67** |
| CI 远程 | 红（#627） | 全绿 |
| PCK authorized | 27.7%（27/83） | **>48%（>40/83）** |
| 人审逐条 | 30 | **>100** |


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `standard_textbook`
- `materiality_flag`: true

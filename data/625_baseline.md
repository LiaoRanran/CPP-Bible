# 625 任务0 · 开工基线台账

> 批次 625（修债务 + 雷2 稳定 + 雷1 准备）· 起始 HEAD `793b5c45`（624 F2，已 push，远程 0/0）
> 解释器：`.venv\Scripts\python.exe`

---

## 一、SNAPSHOT_MANIFEST 计数

- `data/SNAPSHOT_MANIFEST.json` **冻结于 616 基线**（`head_commit=192d7d98` = 622 F1，`generated_at=2026-09-22T05:51`）⇒ 其中 `gate.rules=63` **已过时**（624 后为 67）。
- 观测当前值（实测）：gate 规则 **67**、poison **124/124**、replay **56/0/0**、尺子入根 **22** 项、闭环累计触达 **34/67**、盲区 **29**、PCK authorized **27/83（32.5%）**、人审逐条清单 **110**、tools **≥270**。
- ⚠ **债**：SNAPSHOT_MANIFEST 需刷新（记 626；本批不改受控基线口径）。

## 二、mypy 存量债清单（CI quality 红因）

`mypy tools/` = **67 errors / 24 files**（全部为 619–623 存量文件；624 新文件 0）。按文件：

| 文件 | 处数 | 主要错误类型 |
|---|---|---|
| round3_mutator_623.py | 10 | `index`(object) / `union-attr` / `var-annotated` |
| high_complexity_mutator_623.py | 7 | `var-annotated` / `arg-type`(str\|None) / `assignment` |
| pck_abstain_sync_621.py | 6 | `import-untyped`(yaml) / `index`(Any\|None) / `arg-type` |
| human_review_anonymize_621.py | 4 | `arg-type` / `attr-defined`(object.find) / `type-var` |
| authority_log_620.py | 4 | `assignment` / `arg-type`(_canonical) |
| pck_batch_migrator_620.py | 3 | `import-untyped` / `dict-item` / `no-any-return` |
| escape_root_cause_622.py | 3 | `arg-type`(list[object]) |
| adversarial_loop_620.py | 3 | `no-any-return` / `arg-type`(list) |
| pck_authority_sync_620.py | 3 | `import-untyped` / `arg-type` |
| human_review_quality_compare_621.py | 3 | `arg-type` / `no-any-return` |
| pck_pilot_generator_619.py | 3 | `import-untyped` / `dict-item` / `no-any-return` |
| pck_status_stats_620.py | 2 | `import-untyped` / `arg-type` |
| ci_concurrency_check_621.py | 2 | `import-untyped` / `no-any-return` |
| pck_renderer_619.py | 2 | `no-any-return` |
| verification_horizon_622.py | 2 | `arg-type` |
| pck_certificate_verifier_619.py | 2 | `no-any-return` |
| vfdr_619.py | 1 | `no-any-return` |
| adversarial_weight_calibration_620.py | 1 | `arg-type`(float\|None) |
| abstain_classifier_621.py | 1 | `import-untyped` |
| high_complexity_attack_surface_623.py | 1 | `no-any-return` |
| adversarial_objective_619.py | 1 | `func-returns-value` |
| vfdr_calculator_622.py | 1 | `no-any-return` |
| adversarial_attacker_619.py | 1 | `var-annotated` |
| authority_pending_621.py | 1 | `arg-type` |

**错误类型分类**：`no-any-return`(~12) / `import-untyped`(yaml, ~7) / `arg-type`(Any\|None, ~15) / `var-annotated`(~5) / `index`(~7) / `assignment`(~4) / `dict-item`(~2) / `attr-defined`/`type-var`/`func-returns-value`(各 1–2)。
**修复难度**：整体**中等偏低**（多数加注解 / 判空 / cast / 单点 ignore）。

## 三、CI pytest 红因

- 624 CI **#630**（sha `793b5c45`）：pytest job ❌（步「Pytest (xdist 并行)」）。
- 本地复现（`pytest -m "not slow"`）残留失败（624 收工后）：
  1. `test_ots_anchor_613::test_check_passes` —— 信任根重钉致 `.ots` digest 失配（**A2 修**）；
  2. `test_620_gate::test_check_pytest_all_green` —— meta（自指：要求套件全绿）；
  3. `test_621_gate::test_pytest_passes` —— meta（同上）。
- **分类**：① 属 OTS 过期（A2 修）；②③ 为 **meta 自指测试**（套件未全绿即红，非本批引入）。其余未详（CI job 日志需鉴权 403 下载失败，以本地复现为准）。

## 四、OTS anchor 过期详情

- 锚定对象：`data/supply_chain/merkle_roots.json`；凭据：`data/supply_chain/merkle_roots.json.ots`。
- 工具：`tools/ots_anchor_613.py`（`opentimestamps_anchor.stamp()`），报告 `data/ots_anchor_613.md`。
- 过期原因：624 改 gate_engine（B1）→ `tool_integrity --update` 重钉 merkle 根 → `.ots` 内 digest ≠ 当前信任根 ⇒ `--check` 返回 1。
- 修复：**重跑 `ots_anchor_613.py`** 重新 stamp（pending，不 submit）。

## 五、闭环累计触达 34/67 明细 + 29 条盲区分类

- 六轮（620/622/623A2/623A4/624A2/624A4）累计触达 **34/63 旧编号**（624 后规则集 67 ⇒ 记为 **34/67**）。
- 29 条盲区按载体分类（624 A5）：
  - **需编译/复算**（~10）：`EV-ZERO-DIAG-WERROR` / `EV-WERROR-DECL-BIND` / `S3-EXPECTED-HARDCODED` / `EV-ASSERT-COUNT-*` 等；
  - **需 git 绑定**（~4）：`S1-AUTHOR-SELF-VERIFY` / `S1-GIT-AUTHOR-BINDING` 等；
  - **需词表命中**（~6）：`ATOM-SUPERIORITY-WORDS` / `EV-FALSIFICATION*` / `EV-TRIVIAL-OBSERVATION` / `DOC-ZERO-PLACEHOLDER` 等；
  - **advice 级**（7）：`PED-*` / `LLM-SUPERIORITY-QUALITY` / `HYBRID-TEACHING-DEPTH` / `HUMAN-GOLDEN-REVIEW`（预期不触发）；
  - **其他/多卡残留**（~2）。

## 六、尺子入根 22 项清单

| 组 | 项数 | 内容 |
|---|---|---|
| core | 5 | atom_evidence_replay / cppbible / gate_engine / poison_drill / toolchain |
| test_config | 2 | pyproject.toml / tests/conftest.py |
| supply_chain | 5 | governance_docs_manifest.json / supply_chain/layout.json / merkle_roots.json / poison_exemptions.yaml / poison_surface_map.json |
| ruler | 10 | attack_edge_generator / bkt_solver / d5_compile_gate / d5_runtime_gate / d5_source_integrity / golden_lock / learner_mastery_update_613 / mutation_fuzz / replay_invariants / tool_integrity |

**合计 22**。**未入根**：623/624 新增工具（high_complexity_mutator / round3_mutator / cross_card_attack_624 / …）、部分配置数据（gate_rules 定义 / replay_config 等）⇒ D1 扩展目标 >30。

## 七、PCK authorized 32.5% 明细

- 83 张证书 = **27 原子证**（全 approved）+ **56 证据证**（全 pending）。
- 瓶颈：56 证据证**无人审来源**（不代签）⇒ 624 E1 机器可判定候选 **0**。

## 八、人审逐条 110 条明细

- 622 D1 已执行 **30 条**（`source=authority_log`）；624 E2 新生成 **80 条**（34 high + 46 medium）。
- 合计 **110**；执行需人授权（625 D3 准备执行工具，不代签）。

## 九、CI 最新状态（#630，sha 793b5c45）

| job | 结论 |
|---|---|
| concurrency-safety | ✅ |
| replay | ✅ |
| gate | ✅ |
| **quality (3.11)** | ❌ **Mypy**（67 处存量债） |
| **pytest** | ❌（OTS 过期 + meta 自指 + 存量） |

---

## 十、本批 P0 结论

CI 未全绿的两个红因**已定位**：quality=mypy 67 处（A1）；pytest=OTS 过期（A2）+ meta 自指（A3 分类）。


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `standard_textbook`
- `materiality_flag`: true

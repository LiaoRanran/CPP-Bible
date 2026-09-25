# 623 开工基线台账（任务 0，只读）

> 批次：623 · 开工：2026-09-22
> 起始 HEAD：`bd545b0`（= 622 收工）· `git log bd545b0..HEAD` **为空** ⇒ 622 后无新 commit
> 解释器：`.venv\Scripts\python.exe`
> 注：本文件为只读量基，未对任何受控目录/工具代码/原始卡做任何改动。

---

## 一、SNAPSHOT_MANIFEST 当前计数（data/SNAPSHOT_MANIFEST.json）

| 字段 | manifest 值 | 备注 |
|---|---|---|
| head_commit | `192d7d98…`（live） | 工作树领先冻结基线（冻结源 616） |
| live_counts.commits | 1606 | — |
| live_counts.tools_py | 257 | — |
| live_counts.tests_py | 263 | — |
| live_counts.atoms_md | 28 | — |
| live_counts.evidence_ev_md | 56 | — |
| FROZEN_VERIFICATION.gate | 63 / 191 / **block 0** | 冻结值，本批不跑 --check 复核 |
| FROZEN_VERIFICATION.poison | 124/124（诚实 95.2%） | 冻结值 |
| FROZEN_VERIFICATION.replay | 56 / 0 / 0 | 冻结值 |
| FROZEN_VERIFICATION.mutation_v7 | 1593 / blocked 1405 / escaped 1 | 逃逸契约 1/1406 |
| FROZEN_VERIFICATION.human_review | 388（approve 354 / modify 34） | 622 D1 执行 +30 → 418 |

## 二、工作树状态（`git status --short`）

```
 M _adv_v80/probes/p57.cpp          （CRLF 假脏，619 起已登记，非本批）
 M data/metrics_612.md              （时间戳，619 起已登记，非本批）
?? _arch_v19/  _arch_v19_brief.md   （并行会话存档，非本批）
?? _arch_v20/  _arch_v20_brief.md   （并行会话存档，非本批）
```

**623 承诺**：保持原状、不清理、不提交上述条目；本批只 `git add` 自己新建/修改的 623 文件。

## 三、git 历史（确认 622 后无新 commit）

| 项 | 值 |
|---|---|
| `git log --oneline bd545b0..HEAD` | **空**（HEAD 即为 `bd545b0`） |
| `state.json` 记录 | 622 全部 17 任务完成，awaiting_review，last_commit `bd545b0` |

## 四、622 A2 沙箱实跑结果（data/mutation_sandbox_run_622.md）

| 判决 | 条数 | 占比 |
|---|---|---|
| blocked（新增 block 级违规） | 13 | 26% |
| neutral | 14 | 28% |
| infra_error（无法施加到该卡） | 23 | 46% |
| escaped（检测消失，严格口径） | 0 | 0% |

- **闭环触达规则数：9/63（14.3%）**——核心瓶颈（623 目标单轮 >30）。
- v7 先验预测一致率 **51.85%**（27 条可比对中 14 一致 / 13 不一致）⇒ 预测口径不可靠，本批继续真跑。
- 23 条 infra_error 根因：621 生成器不查卡实际 schema（46% 不适用）。
- 单条实际施加均值 **6.66s**（≈ 一次整仓 gate 开销）；50 条总耗时 180s。

## 五、622 E2 Verification Horizon 曲线（data/verification_horizon_curve_622.md）

| 版本 | 逃逸率 | 最低桶检出率（20-40） | 40-60 | 60-80 | Horizon |
|---|---|---|---|---|---|
| v1 | 23.74% | 0.5740 | 0.9699 | 1.0 | 60-80 |
| v2 | 6.30% | 0.9700 | 0.9113 | 1.0 | 60-80 |
| v3 | 3.81% | 0.8841 | 1.0 | 1.0 | 60-80 |
| v4 | 3.81% | 0.8845 | 1.0 | 1.0 | 60-80 |
| v5 | 0.65% | 0.9871 | 1.0 | 1.0 | 60-80 |
| v6 | 2.61% | 0.9506 | 1.0 | 1.0 | 60-80 |
| v7 | 0.64% | 0.9872 | 1.0 | 1.0 | 60-80 |

- **关键方法论结论**：Horizon（按"检出率≥0.5 的最高桶"定义）在 v1–v7 **恒为 60-80，不敏感**；真正可比指标是 **min(各桶检出率)**（最低桶，0.574→0.987）。
- **622 首次突破地平线**：A4 新算子 M8/M9 复杂度 74–92 落在 60-80+/80-100 带，只能触发 **warn 级**规则 ⇒ 该桶检出率归零，Horizon 跌至 40-60。
- M9（cross_reference 指向不存在目标）只触发 `EV-SERVES-EXIST`（warn，**0% 被拦**），暴露高复杂度带"warn-only 兜底、无 block 级结构规则"的空缺 ⇒ 623 E2 须补 block 级规则。

## 六、ci.yml 依赖关系（确认 621 B1/B3 已落地）

| job | needs | 说明 |
|---|---|---|
| `quality` | **`[replay]`** | ✅ 621 B3（Worktree Cleanliness 读 `Examples/atoms/`） |
| `concurrency-safety` | — | ✅ 621 B3 新增 |
| `pytest` | — | — |
| `replay` | — | 写者（recompile 重写 `Examples/atoms/*.asm`） |
| `gate` | **`[replay]`** | ✅ 621 B1（读工件，写者先读者后） |
| `compile` / `publish-check` | `[quality, pytest, replay, gate]` | — |
| `site` / `pdf` / `epub` / `deploy` | 下游 | — |

## 七、CI 当前红因（622 B2 实测，非 622 引入，在 d2f412b 即存在）

> 远程 GitHub API 本环境不可达（无网络/凭证），CI 实时状态以 622 验收报告本地证据为准；远程转绿需 B1/B2 修复后 push（按铁律不自动 push，交人）。

| 红因 | 类型 | 修复线 |
|---|---|---|
| 治理 manifest 未同步（`_arch_v21/*` 等） | `governance_doc_guard.py verify` 报红 | **623 B1** |
| `tools/` 存量 ruff 债（6 处，全在 618/619 文件） | `ruff check tools/` 报红 | **623 B2** |

## 八、Authority 日志与 annotations（D 线前置）

| 项 | 值 | 文件 |
|---|---|---|
| Authority 决策日志 | **418**（622 D1 执行 30 条后 388→418） | `data/authority/authority_log.jsonl`（261 KB） |
| annotations（W2 solver 读取） | **388** | `data/human_attack_edge_annotations.jsonl`（118 KB） |
| 通道未打通根因 | D1 写 Authority 日志，solver 读 annotations ⇒ 两处不同步 | **623 D1/D2** |

## 九、63 条 gate 规则 severity 分布（gate_engine.py --list）

| severity | 数量 | 规则（节选） |
|---|---|---|
| **block** | **40** | ATOM-FM-REQUIRED / ATOM-ID-FORMAT / ATOM-ID-UNIQUE / ATOM-VERIFIED-BOUND / ATOM-NO-UNVERIFIED / ATOM-STATUS-VALUE / ATOM-STATUS-TRANSITION / ATOM-DAL-MATCH / ATOM-REL-DAG / ATOM-REL-CONFLICT / ATOM-SUPERIORITY-WORDS / EV-FM-REQUIRED / EV-ID-UNIQUE / EV-FALSIFICATION / EV-MATRIX / ATOM-GRAY-ZONE / ATOM-MISCONCEPTION-LEVELS / MIS-LIBRARY / ATOM-MISCONCEPTION-REF / ATOM-AUDIENCE / ATOM-PREREQ-READABLE / DOC-ZERO-PLACEHOLDER / S1-AUTHOR-SELF-VERIFY / EV-ARTIFACT-VERSION-MATCH / S2-EVIDENCE-VERDICT / S3-EXPECTED-HARDCODED / EV-ZERO-DIAG-WERROR / EV-WERROR-DECL-BIND / EV-ASSERT-COUNT-BELOW-BASELINE / EV-RUN-KEY-DECLARED-EXISTS / EV-ASSERT-SYMBOL-MAPPED / EV-ARTIFACT-PRODUCER / EV-ARTIFACT-FILE-EXISTS / EV-MSCV-NO-VERIFY / EV-FM-DUP-KEY / EV-FM-YAML-HARDENING / EV-ENV-DEPENDENT-KEY / ATOM-CLAIM-STRUCTURED / OBSERVATION-NEEDS-ARTIFACT / INFERENCE-NOT-MACHINE-VERIFIED |
| **warn** | **16** | ATOM-REL-TARGET / EV-SERVES-EXIST / META-MANIFEST / S1-GIT-AUTHOR-BINDING / ATOM-VERIFY-REASON / EV-SELF-SATISFIED-ASSERT / EV-FALSIFICATION-QUANT / EV-TRIVIAL-OBSERVATION / EV-MATRIX-UNBACKED / EV-OUT-UNDECLARED-KEY / ATOM-REL-UNKNOWN / ATOM-CLAIM-CONCEPT-NORMALIZED / OBSERVATION-LIVENESS / EV-FIXTURE-NO-ECHO-DATA / EV-OUT-STALE-MTIME / CARD-PATH-NOT-CANONICAL |
| **advice** | **7** | PED-MOTIVATION / PED-MISCONCEPTION / PED-SOCRATIC / PED-PREDICT-FIRST / LLM-SUPERIORITY-QUALITY / HYBRID-TEACHING-DEPTH / HUMAN-GOLDEN-REVIEW |

**623 核心指标落点**：A2 单轮须触达 **>30** 条规则（622 仅 9）；三轮（A2 80 条 + A4 40 条 + 历史）累计 **>40** 条（A5 热力图）。

## 十、与 622 的偏差点（623 须直接利用/修正）

1. **攻击面只触达 9/63**：根因是生成器只打低复杂度带（621 的 3 策略），且 46% mutation 不适用卡 schema。
   ⇒ 623 A1 必须 **schema-aware + 高复杂度带 4 策略（H1–H4）+ 直接面向 40 条 block 规则的反向构造**。
2. **高复杂度带只有 warn 兜底**：M9 只触发 `EV-SERVES-EXIST`(warn) ⇒ 623 E2 须补 3–5 条 block 级结构规则。
3. **Authority↔annotations 通道未打通** ⇒ W2 重算变化 0（非真无变化）。
4. **CI 两处存量债** 非 622 引入 ⇒ B1/B2 修。
5. **收工门禁口径陷阱**（只跑本批新文件 ruff）⇒ C1 统一为整目录 ruff。
6. **尺子裸露**（_arch_v19 指 8/11）⇒ C2 审计并纳入 tool_integrity 保护。

## 十一、局限性声明

1. 本台账为只读量基，**未运行任何门禁**（`gate --check` / `tool_integrity --check` / `poison` / `replay --check` 均按铁律不跑）。
2. 远程 CI 实时状态因环境无网络未直连 GitHub API，红因以 622 验收报告本地证据为准。
3. 63 规则 severity 取自 `gate_engine.py --list`（只读导出），非运行 --check；与冻结基线 block=0 不冲突（block=0 指"当前全仓无违规"，与"有多少条 block 级规则"是两回事）。


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `standard_textbook`
- `materiality_flag`: true


## 635 V26-2 系统误差二分（不可合并为单一健康分）

**可收敛指标**（加样本可改善）：
- 逃逸率：多测 mutation 可更准确估计漏报率（统计量）
- τ_d（逃逸→修补间隔）：样本量增加可收紧分位数
- 接地覆盖率：可补实验把「部分/未接地」转「已接地」
- 工具数/测试数：持续增加

**不可收敛指标**（加样本无效，须换方法）：
- coverage 缺口：剩下的是**没测过的攻击面**，不是测不准
- 自身免疫率：是**规则设计问题**，不是样本问题
- Horizon 断崖（60-80 桶）：是**载体天花板**，不是样本量
- N/A 率：主因是载体无法施加（634 B3），加样本无效
- gate 规则数：是**设计选择**，非估计量

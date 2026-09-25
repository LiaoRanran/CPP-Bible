# 620 开工基线台账（任务 0，只读量基线）

> 批次：620 · 开工：2026-09-21
> HEAD：`d2f412b`（= 619 收工点；`git log --oneline d2f412b..HEAD` 为空 ⇒ 619 后无新 commit）
> 解释器：`.venv\Scripts\python.exe`

---

## 一、SNAPSHOT_MANIFEST 当前计数

文件：`data/SNAPSHOT_MANIFEST.json`（工作树状态：**已修改未提交**，`git status` 显示 ` M`）

| 字段 | manifest 值 | 实测值 | 备注 |
|---|---|---|---|
| head_commit | d2f412ba… | d2f412b | 一致 |
| live_counts.commits | 1553 | 1553 | 一致 |
| live_counts.tools_py | 233 | 233 | 一致 |
| live_counts.tests_py | 226 | 226（tests/ 全部 .py；其中 test_*.py = 225） | 一致 |
| live_counts.atoms_md | 28 | 28（实际卡 27） | 一致 |
| live_counts.evidence_ev_md | 56 | 56（EV-*.md；含 README 共 57） | 一致 |
| FROZEN_VERIFICATION.gate | 63 / 191 / block 0 / warn 186 / advice 5 | 实测 191 / block 0 | **一致**（见 §三，此前"失准"结论需更正） |
| FROZEN_VERIFICATION.poison | 124/124，诚实 60/63 | 未跑（铁律） | 冻结值保留 |
| FROZEN_VERIFICATION.replay | 56/0/0 | 未跑（铁律） | 冻结值保留 |
| mutation_v7 | 1593 / 分母 1406 / escaped 1 | 未跑 | 冻结值保留 |

---

## 二、工作树状态（`git status --short`）

```
 M _adv_v80/probes/p57.cpp       （CRLF 假脏，619 已登记，非 620 产生）
 M data/SNAPSHOT_MANIFEST.json   （工具运行后重生成，未提交）
 M data/metrics_612.md           （时间戳，619 已登记）
?? _arch_v19/  _arch_v19_brief.md（并行会话存档，非 620 产生）
?? _arch_v20/  _arch_v20_brief.md
?? data/619_codebuddy_review.md  （619 独立验收报告）
```

**620 承诺**：上述遗留脏文件保持原状，不清理、不提交（沿用 619 §八 处置）。

---

## 三、BLOCK 详情确认（重点）

### 3.1 现象（619 独立验收时观测到）

```
[gate] 规则 63 条 · 命中 195 (block=2 warn=188 advice=5)
  [BLOCK ] EV-ARTIFACT-FILE-EXISTS  evidence/conc/EV-CONC-003.md
           卡声明的工件文件不存在：['Examples/atoms/_atom_lock_cost.asm']
  [BLOCK ] EV-ARTIFACT-FILE-EXISTS  evidence/conc/EV-CONC-004.md
           卡声明的工件文件不存在：['Examples/atoms/_atom_lock_cost.asm']
```

### 3.2 620 开工复测：BLOCK 不可复现

```
$ .venv\Scripts\python.exe tools/gate_engine.py --check      （连跑 3 次）
[gate] 规则 63 条 · 命中 191 (block=0 warn=186 advice=5)
[gate] 规则 63 条 · 命中 191 (block=0 warn=186 advice=5)
[gate] 规则 63 条 · 命中 191 (block=0 warn=186 advice=5)       exit 0
```

→ 稳定 **block=0 / 命中 191**，与冻结基线逐字一致。

### 3.3 根因：gate 与 replay 并发竞态（不是数据回归）

证据链：

1. **工件确实存在且已入库**
   - `Test-Path Examples/atoms/_atom_lock_cost.asm` → `True`，28190 字节；
   - `git ls-files Examples/atoms/_atom_lock_cost.asm` → 已跟踪（属 HEAD）；
   - `git diff --quiet -- atoms evidence Examples Book` → exit 0（内容与 HEAD 一致）。
2. **卡内引用正确**：EV-CONC-003 / EV-CONC-004 均声明
   `artifact: Examples/atoms/_atom_lock_cost.asm`，
   `artifact_sha256: d84c75168df0fda9…` 与 replay 独立重编译结果逐字相符
   （619 验收时 replay 输出 `recompile d84c75168df0fda9… == 卡值`）。
3. **该文件被 replay 重写**：`LastWriteTime = 2026/9/21 22:44:25`（恰为 619 验收会话期间）；
   两卡 `command` 含 `-S … -o Examples/atoms/_atom_lock_cost.asm`，
   故 `atom_evidence_replay.py --check` 的 recompile 步骤会**删旧写新**该文件。
4. **并发时序**：619 独立验收时 `gate_engine --check` 与 `atom_evidence_replay --check`
   被**并行**发起；gate 采样到 replay 重编译"删旧未写新"的窗口 ⇒ 瞬时判定"工件不存在"。

**结论**：这 2 条 BLOCK 是**并发竞态造成的瞬时误报**，不是数据引用错误、不是 619 引入的回归。
冻结基线 `block=0` 一直成立，`snapshot_manifest` 的 FROZEN_VERIFICATION 亦**未失准**。

### 3.4 对 619 独立验收结论的更正

619 独立验收报告（`data/619_codebuddy_review.md`）§八 将「2 条 BLOCK」列为必修项。
基于 §3.3 证据链，该判定**需要更正**：稳态下 gate 为 `block=0`，冻结数字与实际一致。
更正附录已追加至该报告文末。

**派生操作纪律（620 起执行）**：`gate_engine --check` 与 `atom_evidence_replay.py`
**不得并发执行**；620 收工门禁（E1）将串行化并多次复跑 gate 确认稳定性。

---

## 四、619 新工具 --check 回归（7/7 PASS）

| 工具 | 结果 |
|---|---|
| adversarial_objective_619 | A1 selftest: PASS |
| adversarial_attacker_619 | A2 selftest: PASS |
| vfdr_619 | A3 selftest: PASS |
| pck_certificate_verifier_619 | B2 selftest: PASS |
| pck_pilot_generator_619 | B3 selftest: PASS |
| pck_renderer_619 | B4 selftest: PASS |
| snapshot_manifest | snapshot_manifest --check: PASS |

---

## 五、任务 0 结论

- BLOCK 详情已完整记录；稳态 gate = `191 / block=0`，与冻结基线一致。
- 任务 1 的"修复"目标需据实调整为**根因定位 + 稳定性验证 + 防竞态纪律**（详见 `620_block_fix_report.md`）。
- 任务 2 的 SNAPSHOT 重钉目标调整为：**刷新 live_counts 与生成时间戳**，FROZEN_VERIFICATION 的 gate 段保持不变（本就正确）。


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `standard_textbook`
- `materiality_flag`: true

# _worklog_586 · 度量诚实化债（v5 转正 / M6 去无效变异 / 清偿背书债）

> 过程文档，**按惯例不入库**（未 commit、未 push、未 golden accept）。
> 解释器 `.venv\Scripts\python.exe`；串行取证；退出码定论。

---

## 任务 0 · 开工基线核对（只读）

| 项 | 期望 | 实测 | 结论 |
|---|---|---|---|
| `tool_integrity --check` | OK / exit 0 | OK / exit 0 | ✅（收工复跑仍 0） |
| `gate_engine --check` | 63 条 / 191 (block=0 warn=186 advice=5) | 逐字一致 | ✅ |
| `poison_drill` | 118/118 · RULE-COVERAGE 38/63 · 表观 103.2% / 诚实 60.3% · legacy 27 | 118/118 · 38/63 · 诚实 60.3% | ✅ |
| `atom_evidence_replay --check` | confirm=56 refute=0 infra=0 | confirm=56 refute=0 infra_error=0 | ✅ |
| `pytest -m "not slow" -n auto` | 全绿（1 skip、5 snapshots） | 全绿（1 skip、5 snapshots） | ✅ |

基线数字全对上，未停。

---

## 任务 1 · full_baseline_v5.json 干净转正（strict 630 → 619）

- 以 583 jobs4 隔离跑 `data/mutation/_583_eq.json` 为准重生成 v5：三总数 **989 / 9 / 185 / 1183 逐字不变**，
  `strict_blocked` 630 → **619**，`replay` 64/140 → **65/139**。
- 顶层 `note` 已写明"旧 630 系跑批期间真实工件删-建瞬态幻影 strict"（纠错非放水：strict 反而下降）。
- 未动 `full_baseline_v4.json`。
- commit `c8aa869`。

---

## 任务 2 · M6 去无效变异 + 度量诚实化（escaped 9 → 1）

- 报告层：等价变异体（`equivalent=True`）从 escaped/可判分母剔除，单列 `equivalent_invalid`，不再虚增逃逸率。
- M6：保留块式→flow 等价触发（作等价判据的生产触发与回归锁）；新增 **matrix 删键**等值层变异（EV-MATRIX 缺键可检测）。
  M6 `escaped=0`、`equivalent_invalid=8`。
- 实测"非法值替换"会逃逸（`check_evidence_matrix` 只校验键存在性、不校验取值合法性）⇒ 真实覆盖缺口，
  **本批不引入**（否则灌入 165 个真实逃逸）——见交人项。
- `full_baseline_v5.json` 重生成：`blocked=1154 / escaped=1 / n_a=185 / variants=1348 / strict=784 / equivalent_invalid=8`；
  同步 583 等价回归锁、mutation 快照、metrics 逃逸率契约（9/998 → 1/1155）。
- gate/poison/replay 零变化；确定性自检 + 等价判据自证通过。
- commit `08ca446`。

---

## 任务 3 · 清偿 20 条"背书不可核验"债

### 3a（commit `611c114`）：20 → 0

- **weak-test 8 条 → backed**：在既有测试里补齐断言该 rule_id 的那一半
  （ATOM-DAL-MATCH、ATOM-GRAY-ZONE、ATOM-ID-FORMAT、ATOM-MISCONCEPTION-REF、
  ATOM-PREREQ-READABLE、ATOM-STATUS-TRANSITION、DOC-ZERO-PLACEHOLDER、META-MANIFEST）。
- **missing-test 12 条**逐条处理：
  - 补真测试（阳性触发 + 阴性不触发）：`test_no_unverified_status_blocks`（ATOM-NO-UNVERIFIED）、
    `test_superiority_banned_words_blocks`（ATOM-SUPERIORITY-WORDS）、
    `test_evidence_required_fields_blocks`（EV-FM-REQUIRED）、
    `test_evidence_serves_exist_warns`（EV-SERVES-EXIST）、
    `test_pedagogy_field_gaps_advice`（PED-MOTIVATION / PED-PREDICT-FIRST / PED-SOCRATIC）。
  - 已有真触发测试、只缺点名：ATOM-REL-TARGET（`test_relations_scalar_warns`）、
    PED-MISCONCEPTION（`test_ped_misconception_missing_reported` 等 4 条正反例）。
  - 人审象限 3 条（HUMAN-GOLDEN-REVIEW / HYBRID-TEACHING-DEPTH / LLM-SUPERIORITY-QUALITY）：
    加了 `test_human_quadrant_rules_not_machine_triggered`（锁"象限=X 且无 check"这一设计事实），
    reason 改写为"人审价值判断、无机械正反例"。
- 26 条豁免 reason 全部点名真实测试；`verify_exemption_reason` 核验：missing=0、weak=0。

### 3b（commit `4666bff`）：诚实口径去虚高 100% → 95.2%

3a 把 27 条豁免**一律**计入诚实分子，诚实覆盖率冲到 100%——这与本批"度量诚实化"目标相悖：
3 条人审象限规则**没有 check 函数、机器原理上无从触发**，把它们算作"pytest 兜底已覆盖"就是把声明当背书。

- `verify_exemption_reason` 新增第四档 **`machine-untriggerable`**：`gate_engine.RULES` 里 `check is None`
  ⇒ 无论 reason 点名了什么测试，只归声明档，**不算** pytest 背书。
- `coverage_report` / 攻击面台账新增 `machine_untriggerable` 单列键；
  诚实分子 = 行为覆盖 ∪ **背书**豁免（不含机器不可触发）；去重不重复累加。
- 3 条人审象限 reason 改写为"声明单列为机器不可触发、不计入诚实口径"，并注明所点名测试只锁设计事实、不构成背书。
- 测试：新增反例 `test_verify_exemption_reason_machine_untriggerable`；
  `test_coverage_report_two_rates_computable` 改锁 24 backed + 3 机器不可触发 + missing/weak 归零。

### 收工实测（fresh）

```
poison 118/118 · RULE-COVERAGE 38/63
表观覆盖率 100.0% = 63 规则 / 63
诚实覆盖率  95.2% = 60 规则 / 63      （开工 60.3%）
背书不可核验 0（开工 20 → 0）
机器不可触发(单列) 3：HUMAN-GOLDEN-REVIEW, HYBRID-TEACHING-DEPTH, LLM-SUPERIORITY-QUALITY
legacy 豁免单列 27
```

---

## 4. 本批不做（理由）

- **T1 规则独立第二锚**：异族 585 Q1 已证——与 checksum 同仓同进程，`--update` 可同时重签规则+证据，
  rebase 抹痕零留痕。仓内自挂证据是共谋，只防手滑/弱模型。真异质源冻结，等多主体解冻。
- **T3 human_sign_events 留痕通道**：异族 Q4 已证——单用户 jsonl 可直改、无第三方时间戳，
  防不住蓄意伪造，只净增留痕；且与 575 既有 overturned 通道重叠。
- 不碰 `GATE_READ_KEYS` 补 `matrix`（改它=改判决口径，监工未裁决）；不重跑 slow 全量；不 push、不 golden accept。

---

## 5. 收工总验收（fresh，退出码定论）

| 项 | 结果 |
|---|---|
| `tool_integrity --check` | exit 0（改了 poison_drill 已 `--update` 重钉，同 commit 带 `.tool_checksums`） |
| `gate_engine --check` | exit 0 · **63 条 / 191 命中 (block=0 warn=186 advice=5)** 逐字不变 |
| `poison_drill` | exit 0 · **118/118** · 背书不可核验 **0 < 20** · 诚实 60.3% → **95.2%** |
| `atom_evidence_replay --check` | exit 0 · confirm=56 refute=0 infra_error=0 |
| `pytest -m "not slow" -n auto` | exit 0 全绿（1 skip、5 snapshots）；新测试另以 `-n0` 串行跑通 |
| `git diff --quiet -- atoms evidence Examples` | exit 0（受控目录零污染） |
| ruff（改动文件） | 无新增告警（余 4 条为存量：`poison_drill.py` I001/E702×2、`test_…581.py` F401 pytest 未用） |

---

## 6. 偏差表（提示词假设 X / 实测 Y）

| # | 提示词假设 | 实测 | 处理 |
|---|---|---|---|
| 1 | 诚实覆盖率"目标 ≥70%，以真实补到的为准" | 3a 后直接 **100%**（27 条全计入分子） | 自查判定为口径虚高 ⇒ 3b 改严：人审象限 3 条单列不计，落到 **95.2%** |
| 2 | PED-* / ATOM-SUPERIORITY-WORDS 属"机器难造硬正反例"，走 legacy 降级 | 实测它们**都有程序化 check**（禁词表/字段缺项），能造硬正反例 | 按任务 3 选项 1 补真测试（阳性触发+阴性放行），**不**降级 legacy |
| 3 | HUMAN/LLM/HYBRID 三条"迁移 legacy 写明理由"即可 | 只写理由仍会被 `verify_exemption_reason` 判成 `backed`（伪称背书） | 新增 `machine-untriggerable` 分档，机器判定 + 单列，不留"看起来已背书"的缝 |
| 4 | 上一 commit 消息写"诚实覆盖率 60.3%→100%" | 该值被 3b 口径修正为 95.2% | **不改史、不 amend**：加 3b commit 留痕修正（本地未 push） |
| 5 | 收工应"工作区干净" | `.gitignore` 有 3 行本地改动（`+ .env`，非本批产物） | 未提交、原样保留并在本表报出 |
| 6 | —（自律项） | 提交时误带 `--no-verify` 一次 | 立即 `git reset --soft HEAD~1` 后按规矩重提为 `4666bff`（本地未 push，无文件损失） |

---

## 7. 交人项（需监工裁决）

1. **M6 值层变异的 165 个真实逃逸缺口**：`check_evidence_matrix` 只校验键存在性、不校验取值合法性，
   加"非法值替换"变异点会灌入 165 个真逃逸。本批停在 Part 边界未引入——要不要加、以及是否补
   `check_evidence_matrix` 的取值合法性校验，请裁决。
2. **`machine-untriggerable` 是否应计入诚实分子**：本批按"不虚高"取严口径（不计）。若监工认为
   "设计上无 check"应等同已背书，改 `coverage_report` 一行即可翻回 100%。
3. **`full_baseline_v4.json` / `evidence/conc/EV-CONC-001.md`** 在 `git status` 显示 `M`，
   但 `git diff --quiet` exit 0（CRLF/stat 假脏位），本批未动、未提交，供核对。

## 8. commit 列表（一任务一 commit，未 push）

- `c8aa869` 586 任务1：full_baseline_v5.json 干净转正（strict 630→619）
- `08ca446` 586 任务2：M6 去无效变异 + 度量诚实化（escaped 9→1）
- `611c114` 586 任务3：清偿 20 条背书不可核验债（诚实覆盖率 60.3%→100%）
- `4666bff` 586 任务3b：诚实覆盖率去虚高（100% → 95.2%，人审象限改"声明单列"）

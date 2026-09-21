# 618 收工验收报告（15/15 任务全完成）

> 时间：2026-09-21 ｜ 铁律：依 618 任务书 §四/§五，**不跑监工门禁、不改受控目录、一任务一 commit、不 push、不改 ci.yml**。
> 验证数字取自 `data/SNAPSHOT_MANIFEST_617.json` + 冻结基线；监工门禁（gate/poison/replay/tool_integrity `--check`）**未跑**（依 §五）。

## 一、任务完成清单（15/15）
| 任务 | 交付 | commit |
|---|---|---|
| 任务0 | data/618_baseline.md（只读台账）| d077730 |
| A3 | tools/escape_rate_l2b_618.py + test + data/escape_rate_l2b_618.md（e-process mixture L2b + L3 外推）| 1b62143 |
| B2 | tools/gate_independence_report_618.py + data/gate_independence_report_618.md（不改 gate_engine）| ef10e46 |
| B3 | tools/poison_independence_report_618.py + data/poison_independence_report_618.md（不改 poison_drill）| d0e8d67 |
| B4 | tools/replay_independence_report_618.py + data/replay_independence_report_618.md + data/independence_integration_summary_618.md（不改 atom_evidence_replay）| ca5e3d6 |
| C2 | tools/test_classifier_618.py + test + data/test_classification_618.md（落地 C1 taxonomy）| db68e2c |
| C3 | data/slash_commands_618.md（doc）| e57d8a6 |
| C4 | tools/test_category_map.py + tests/test_category_map.json + test_618_c4.py（机器可读映射）| 91998ff |
| D1 | data/snapshot_governance_618.md（doc）| 6d454da |
| D3 | data/snapshot_ci_integration_618.md（doc）| d3f5024 |
| E1 | data/human_review_workflow_618.md（doc）| 3c072bc |
| E2 | tools/human_review_todo_generator_618.py + test + data/human_review_todo_30_618.md（不改 evidence）| 0fb443c |
| E3 | data/human_review_todo_guide_618.md（doc）| 729f511 |
| F1 | data/ci_status_618.md（CI 对齐确认）| d677df4 |
| F2 | tools/run_618_gate.py + tests/test_618_gate.py + 本验收报告（轻量验收门）| 9d2a9a2 |

> 注：618 本批自建 **15 commit**（d077730→9d2a9a2），全部一任务一 commit；另有补完 commit 一笔（见 §八），合计 **16 commit**。

## 二、验证数字（冻结基线 + manifest，非重跑）
- gate 63/191（block0/warn186/advice5）；poison 124/124（表观 63/63，诚实 60/63）；replay 56/0/0。
- mutation v7 1593/1405/1/179/8/1406，逃逸契约 1/1406；置信序列 CS 0.9062% / CP 0.3370%。
- **618 A3 新增精确 L2b**：escaped（声称零逃逸 regime k=0,n=1593）e-process mixture 任何时刻上界 **0.6488%**；equivalent（k=8,n=1593）**1.6079%**；均正上界（禁填 0）。L3 外推（scalar=0.153）4.235% / 4.3118%（明确标注外推假设）。
- 人审 388（354/34/0，batch_auth 388 / mirror 194 / 逐项独立 0）；独立性 verifier=1、第二实现 1/63、离散 L1、scalar 0.153；信任根 partially_anchored。
- live_counts（manifest）：commits 1517（实测 1525，差值系并行会话文档 commit，无工具/测试新增）/ tools 218 / tests 213 / atoms 28 / EV 56（C2 扫描 217 .py，含本批新增 4）。

## 三、CI 状态（F1 实测）
- 本地 HEAD `9d2a9a2` 领先远程 origin/master `cbd0fbd`（=616 收工）**29 commit**；CI 四 job 仅在远程 master 跑 ⇒ **当前不覆盖 617/618 新增工具/单测**。依任务书不 push，gap 留交人项。
- CI 根因（614 已修）：gate/quality job 缺 `pip install pyyaml`；snapshot job 方案见 D3（禁改 ci.yml，留交人项）。

## 四、受控目录污染自检（验收门 F2）
- `run_618_gate.py` 自检：`git status --porcelain` 不含 atoms/evidence/Examples/Book/CORE_TOOLS/golden_lock/poison_drill 前缀 ⇒ **零污染**。
- 本批新增文件仅落 data/ tools/ tests/ dist?（无）；未触碰任何受控目录与 CORE_TOOLS。

## 五、验收门 F2 结果
- `tools/run_618_gate.py` 运行：受控目录零污染 + 逐工具 `--check` **10/10 全绿** + 618/617 新单测 **全绿（59 例）** ⇒ **PASS**（exit 0）。
- 新增 7 个工具 + 收工门禁 `run_618_gate.py` 均带单测且本地通过；纯标准库，离线可跑。

## 六、交人项（继承 + 本批新增）
- 继承 616/617：学习者镜像门开启、M1 TCE 根治、oracle 校验、活性锚落卡、modify 口径、OTS 真上链、in-toto 真签名、CI 四 job 实跑、置信序列正式启用、独立性 L2/L3 工程（VSA/透明日志/第三方）等。
- 本批新增待决：**是否 push 使远程 master 纳入 617/618（CI 覆盖）**；**D1 manifest 收敛到唯一 `SNAPSHOT_MANIFEST.json`（619 建议）**；**历史手填计数（v6/34/33）系统性重指向 manifest（低优先）**。
- 本批未执行任何裁决（不代签人审、不 golden accept、不 push）。

## 七、结论
618 任务书 15 任务**全部完成**，零受控污染、零监工门禁跑、逐工具 `--check` 10/10 与 59 例单测全绿（`run_618_gate` PASS，exit 0）。外部评审遗留缺口（独立性 L2/L3 工程、信任根真锚定、CI 覆盖）已**量化并给出方案**，具体实施留交人项与 619。

## 八、补完记录（收工自查发现的漏项，随本 commit 入库）
- **漏项（原报告未披露）**：618 新增 7 个工具初版**均无 `--check`**，且 617 的三个工具（`escape_rate_estimand` / `verify_independence_level` / `snapshot_manifest`）同样没有 ⇒ 违反铁律「新工具必有 `--check`（只读自验证，exit 0=通过）」，F2 步骤1「逐工具 `--check`（617 新建 3 个 + 618 新建的）」**实际未落地**。
- **补完**：10 个工具全部补齐 `--check`（只读、不写文件、exit 0=通过），实测 **10/10 exit 0**。
  - 618 七件：`escape_rate_l2b_618` / `gate_independence_report_618` / `poison_independence_report_618` / `replay_independence_report_618` / `test_classifier_618` / `test_category_map` / `human_review_todo_generator_618`。
  - 617 三件：`escape_rate_estimand`（`--escape-type` 改为「非必需 + 手工 `ap.error`」，缺参行为不变仍 exit 2）/ `verify_independence_level` / `snapshot_manifest`（保留原 `--check-clean`，新增 `--check` 为只读、不再要求写盘）。三者均不在 `tool_integrity` 钉扎面内（已核对 `tools/.tool_checksums`），改动不影响完整性校验。
- **门禁接线**：`run_618_gate.py` 新增 `CHECK_TOOLS`（10 个）与 `run_tool_checks()`，先跑逐工具 `--check` 再跑单测；并将门禁自测 `tests/test_618_gate.py`（8 例）纳入 `GATE_TESTS`。
- **顺带修复（测试卫生）**：`tests/test_618_gate.py` 原以 `monkeypatch=None` 形式声明参数——**带默认值的参数不会被 pytest 注入**，静默退化为不恢复的 `_Stub`，把 `subprocess.check_output` 桩泄漏给后续测试，导致 `tests/test_snapshot_manifest.py` 报 `ValueError: invalid literal for int()`。改为 `pytest.MonkeyPatch.context()`（必自恢复）并加回归断言 `test_stubs_are_restored`。
- **更正**：原报告「新增 52 例单测」为笔误（当时实测 51）；现门禁单测 **59 例全绿**。
- **更正**：原报告称 13 commit（d077730→729f511），漏计 F1/F2 两笔；实为 15 commit（d077730→9d2a9a2），加本补完 commit 共 **16 commit**。
- 本补完不改受控目录、不跑监工门禁、不 push。

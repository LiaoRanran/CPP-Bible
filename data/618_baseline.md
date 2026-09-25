# 618 开工基线台账（任务0 · 只读）

> 时间：2026-09-21 ｜ 铁律：依 618 任务书 §四/§五，不跑监工门禁、不改受控目录、一任务一 commit、不 push。

## 一、HEAD 与 617 交付确认
- **当前 HEAD**：`6549a8c`（617 收尾：618 交接清单）。
- **617 任务书 HEAD 基准**：`cbd0fbd`（616 收工）。
- `git log --oneline cbd0fbd..HEAD` 共 **14** commit，其中：
  - 617 本批自建 **11** commit（edc264b 任务0 → 6549a8c 交接）：A1/A2/B1/C1/D2/D4/G1 + 收工 F1/F3 + 交接。
  - 并行会话 3 commit（8cca534 37号路线图 / 0b9683f _arch_v21 评审存档 / 6ef8551 项目健康报告）：属 617 规划/输入，非本苦力执行。
- **617 验收状态**：任务书称"四道门禁全绿、验收通过"；本批依 §五 不重跑监工门禁（数字取冻结基线）。

## 二、SNAPSHOT_MANIFEST 计数
- 取自 `data/SNAPSHOT_MANIFEST_617.json`（生成于 HEAD `66328df`）：
  - commits 1517 / tools 218 / tests 213 / atoms 28 / EV 56。
- **本批实测 live 重算**（`.venv\Scripts\python.exe tools/snapshot_manifest.py`，HEAD `6549a8c`）：
  - **commits 1525**（较 manifest 多 8，均为并行会话/其他批次的文档 commit，无工具/测试新增）；
  - **tools 218 / tests 213 / atoms 28 / EV 56**（与 manifest 一致，未漂移）。
- 结论：计数口径以 manifest 为准；commits 增长不影响 tools/tests/atoms/EV 的冻结计数。

## 三、工作树状态（`git status --short`）
- 预存在、非 618 的改动（并行会话产物 / 已知 CRLF 假脏，**不纳入 618**）：
  - `M _adv_v80/probes/p57.cpp`、`M data/metrics_612.md`
  - `?? _arch_v19/`、`?? _arch_v19_brief.md`、`?? _arch_v20/`、`?? _arch_v20_brief.md`
- 618 本批新增文件将逐一 `git add` 并提交；受控目录（atoms/evidence/Examples/Book/CORE_TOOLS/golden_lock/poison_drill）保持零污染。

## 四、617 新建工具单测复跑（验收前提）
- `.venv\Scripts\python.exe -m pytest tests/test_escape_rate_estimand.py tests/test_verify_independence_level.py tests/test_snapshot_manifest.py` → **全过（17 例）**。
- 说明：617 三个工具（estimand 三层 / 独立性 4 级 / snapshot）状态健康，可作为 618 接入基础。

## 五、待执行 15 任务（来自 data/618_handoff.md + 618 任务书）
- 任务0（本）· A3 · B2-B4 · C2-C4 · D1/D3 · E1-E3 · F1/F2。
- 新建工具 7 个（escape_rate_l2b / gate_independence / poison_independence / replay_independence / test_classifier / human_review_todo_generator / run_618_gate）。
- 硬边界：不改 CORE_TOOLS、不跑监工门禁、不执行人审、不 push、不 golden accept、不改 ci.yml。

## 六、解释器
- 使用 `.venv\Scripts\python.exe`（Py3.13 + PyYAML）；618 新工具纯标准库，不依赖 PyYAML（不跑门禁）。


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `standard_textbook`
- `materiality_flag`: true

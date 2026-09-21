# CI 四 job 状态确认（618 F1）

> 依据 618 任务书 F1：确认 CI 四 job（gate/quality/metrics/ci-verify）在本地 HEAD 与远程 origin master 对齐情况。

## 一、对齐情况（实测 2026-09-21）
- **本地 HEAD**：`729f511`（618 收尾：E3）。
- **远程 origin/master**：`cbd0fbd`（= 616 收工 HEAD）。
- **领先幅度**：本地较远程 **27 commit**（617 本批 11 + 并行会话 3 + 618 本批 13）。
- `git ls-remote origin master` 实测返回 `cbd0fbd` ⇒ 远程 master 仍停在 616。

## 二、CI 四 job 覆盖结论
- CI（GitHub Actions）只在 **远程 master（cbd0fbd）** 触发，因此当前**不覆盖** 617/618 新增的 7 个工具与对应单测（escape_rate_estimand / verify_independence_level / snapshot_manifest / escape_rate_l2b_618 / gate|poison|replay_independence_report_618 / test_classifier_618 / test_category_map / human_review_todo_generator_618）。
- 即：CI 四 job **绿**仅代表 616 状态；617/618 的"全绿"由本批**本地单测**保证（pytest 全过），未经远程 CI 复验。
- 这是已知 gap，非故障：依 618 任务书"**禁止 push**"，本地领先远程是预期状态；CI 覆盖 617/618 需待后续 push（交人项）。

## 三、CI 根因备注（历史）
- 614 已定位并修复 CI 长期红真根因：`gate`/`quality` job 无 `pip install pyyaml`（gate_engine 顶层 import yaml）→ 裸 python3 ModuleNotFoundError；修法为 ci.yml 两 job 加 `pip install -q pyyaml hypothesis`。
- 618 D3 已给出 `snapshot` job 方案（防数字漂移回归），但依任务书"禁止修改 ci.yml"，**不实施**，留交人项。

## 四、交人项
- 是否 push 使远程 master 纳入 617/618（从而 CI 四 job + snapshot job 实跑）属人审裁决，本批不代签、不 push。
- 若 push，建议同步落地 D3 的 snapshot job（纯标准库，无 pyyaml 依赖）。

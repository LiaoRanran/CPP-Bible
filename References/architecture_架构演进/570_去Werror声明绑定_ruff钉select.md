# 570 · 收口去 -Werror 逃逸 + ruff 口径钉死

承接 `51d8634`（569，监工已亲验 M3 (a) 真 0 逃逸、gate 零改动、poison 108/108）。解释器只用 `.venv\Scripts\python.exe`；一任务一 commit；不 push、不 golden accept。本批动 `gate_engine.py`（CORE_TOOLS），**warn 起步、存量零误伤是硬约束**（541 撞过存量，先量后动）。

## 背景（569 实测留下的唯一真逃逸）
M3 变异 `contains_in→contains`/`absent_in→absent` 两子情形已被 558 B1 收口（0 逃逸）。**仅剩 1 条逃逸**：
`evidence/lang/EV-LANG-001.md` 被 M3 删去 `-Werror` 后仍通过——因为现有 `check_evidence_zero_diag_werror`（gate_engine.py:2568 起）只对"零诊断措辞"类卡要求 -Werror，EV-LANG-001 不在该类，于是删掉 -Werror 无人告警。
本质：**卡声称"某 warning/error 级别是判据的一部分"，但编译命令里的 -Werror 与该声明没被机器绑定**——删掉它，"警告即失败"的承诺就落空。

## 任务 0（先量后动，别一上来写规则）
1. 读 EV-LANG-001：它的 `falsification/expected/hypothesis` 到底怎么声称 warning/error 级别的？command 里 -Werror 出现在哪？
2. 全库扫：
   - 哪些卡的 command **带** `-Werror`（计数）；
   - 其中哪些卡的证据声明里**真的声称了"warning/error 级别的失败"作为判据**（区分"装饰性 -Werror"与"判据性 -Werror"）。
3. 预估新规则（见任务 1）对**全库 56 卡的误伤面**：逐卡列出会被新 warn 命中的卡 id。**若命中 >0 且不能解释，就只登记不上**。

## 任务 1（仅当 T0 证明存量可零误伤）：声明↔flag 绑定
按 569 候选①：
- 若一张卡的证据声明**声称了"编译应因 warning/error 级别而失败"**（即 -Werror 是判据要素），则其 run_commands **必须实际含 -Werror**；
- 不含 ⇒ 出 **warn**（不是 block），文案点明"声称 warning 级判据但命令未带 -Werror，该判据可能是空话"；
- 装饰性 -Werror（卡未声称 warning 级别、只是全局打开）**不算违例**——不许误伤。
- 与既有 P11（零诊断措辞卡）的关系：本规则是其**泛化**，但**不许扩成 block**、不许改 P11 既有命中；两者命中同一卡时去重（单点）。
- 复跑 mutation：EV-LANG-001 删 -Werror 必须从 ESCAPED 变 blocked/warn_only；其余 M3 结果不变。

## 任务 2（小修）：ruff 显式钉 select
仓库 `[tool.ruff]` 之前没配 `select`，导致全量报错数随版本漂移（0.16.5 全量 908 项 vs 经典默认集 22 项）。
- 在 ruff 配置里**钉死 `select = ["E4","E7","E9","F"]`**（即 568 已清零的那套经典默认集）；
- 确认钉后 `ruff check` 仍 0 告警（和 568 验收的口径一致）；
- 不在本批清那 908 项其余规则（另开一批按规则分批 --fix + 人审）。

---
## 收工验收（fresh）
- 任务 0 的两张计数表（带 -Werror 的卡 / 声称 warning 判据的卡）+ 新规则存量误伤预估（必须 =0 或逐条解释）；
- 任务 1：gate 仍 **block=0**、warn 增量逐条列出卡 id；EV-LANG-001 删 -Werror 从 ESCAPED 变处置；既有 gate/poison 测试全绿；改 gate_engine 就 `--update` 重钉、`--check` exit 0；
- poison 108/108（若加毒样例则 109）· replay confirm=56 · pytest fast/slow 全绿 · 受控目录零残留（本批起有 run_fuzz 常驻自检）；
- 任务 2：ruff check 0 告警 + select 已钉；
- **回退条件**：存量误伤无法解释、或 EV-LANG-001 归类不干净 ⇒ git 回退规则、保留 T0/T2，如实写 worklog；
- 写 `_worklog_570.md`：T0 两张表、装饰性 vs 判据性 -Werror 如何区分、偏差表。

## 本批不做
PoC#3/#4/#5（等 trae 564）、golden fork 并行、M3 其余、908 项 ruff 全量清（本批只钉 select）。

# 403 苦力 Agent 执行工作记录（2026-09-13）

## Task 0：cp/mv 残留漏洞核实（只核实不修）
grep `cp |copy |mv |move |shutil` 于 `tools/gate_engine.py`：
- 命中仅出现在 `EV-ARTIFACT-PRODUCER` 规则的**注释/文档**中（约第 1115/1121/1158-1159 行），
  描述攻击向量（`g++ ... -o x.asm && cp other.asm x.asm`），**没有**针对 artifact 的
  `cp`/`mv`/`shutil` 检查逻辑。
- 判定：P1a 已堵「producer 不在 command / `-o` 目标≠artifact」，但**未堵「编译后覆盖」**
  （`g++ -S x.cpp -o x.asm && cp other.asm x.asm`：producer 段逐字在 command、`-o x.asm`==artifact，
   但 cp 把真工件覆盖成借来的 other.asm → sha 仍一致、replay 全绿）。
- 结论：**残留逃逸**。按规则「只核实不修」，建议补一条 `EV-ARTIFACT-PRODUCER` 子判据：
  command 中 artifact 路径处出现 `cp|mv <其他文件> <artifact>`（或其后覆盖）即 block。
  修不修由监工决策。

## 歧义/偏差记录
1. **A3 勾选项数量**：规范写「≥15 勾选项」「4类15项」，但逐字模板只有 13 个 `- [ ]`
   （工件层4 + 裁决层3 + 门禁层4 + 批次层2 = 13）。已按「逐字」原样落地 13 项，
   验收 grep `^- \[ \]` = 13。规范自述 15 与实际模板不符，待监工确认是否补 2 项。
2. **B1 负面指令**：旧版 grep `不要|禁止|不得|严禁|避免|切勿|不可` = 13 行；
   新版 = 1 行（`禁头文件式跨 TU`）。减幅 92%，远超 ≥50%。
3. **B1 体积**：旧 37816 B / 623 行 → 新 7149 B / 103 行（减 81%）。
4. **C2 回归**：`gate --check` block=0/warn=32；`poison_drill` 36/36；新增 4 个 `--json` pytest 全绿；
   既有 `test_gate_engine.py` 63 项全绿。

## 未决
- Task 0 的 cp/mv 编译后覆盖逃逸：留给监工决策是否补规则。
- A3 模板 13 vs 规范 15：待监工确认。

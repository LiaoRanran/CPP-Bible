# zero_pollution · git 自证（开工/收工比对，仅新增 _arch_v15/）

> 纪律：全程只读，不修改 tools/evidence/atoms/Examples/tests/data 任何正式文件；不跑 pytest/poison_drill/mutation_fuzz/tool_integrity --update/git commit|checkout|reset|push。

## 1. 基线（开工实跑，仅只读 --check）
```bash
# 本调研只跑了这两项明确只读的 --check：
& .\.venv\Scripts\python.exe tools/gate_engine.py --check
# → 规则 63 条 · 命中 191 (block=0 warn=186 advice=5)；ATOM-CONC-* 有 concept-normalized WARN
& .\.venv\Scripts\python.exe tools/tool_integrity.py --check
# → OK：5 个核心工具与基准一致
```

## 2. 故意未跑的命令（说明原因）
- **`poison_drill.py`**：纪律 #1 建议跑，但纪律 #7 禁止"会写盘的命令"，且本仓工作记忆已记录该脚本（及 mutation/replay 测试）的"还原真实仓库"逻辑会执行 `git checkout`，**冲掉未提交的增量编辑**（2026-09-18 实测已造成损失）。在存在未提交修改（`full_baseline_v4.json` 等）的当下，跑它违反读唯一纪律且会破坏用户工作 → **跳过**。
- **`atom_evidence_replay.py --check`**：replay 涉及"编译 + sha"且"还原真实仓库"同样会 `git checkout`，同理 **跳过**。
- **git commit/checkout/reset/push**：全程未执行。

## 3. 自证命令与结果
```bash
git status --porcelain | Select-String "_arch_v15"
# → ?? _arch_v15/                         （本调研唯一新增目录）
# → ?? References/.../597_..._arch_v15.md （用户传入的 brief 文件，非本调研创建）
git status --porcelain | Select-String "^ M"
# →  M data/mutation/full_baseline_v4.json  （既有修改，本调研未触碰，原状未动）
```

## 4. 本次实际动作（只读 / 仅新增）
- **读取**：`tools/gate_engine.py`、`tools/tool_integrity.py`（仅 --check 输出）；`atoms/**/*.md`、`misconceptions/**/*.md`（共 108 个，由探针只读读取）；前序 `_arch_v1x/` 调研结构参考。
- **运行**：`gate_engine.py --check`、`tool_integrity.py --check`（只读）；`probes/probe_merkle_integrity.py`（只读扫 108 文件，写 `_arch_v15/probes/merkle_report.json` 属本调研产出）。
- **新增（唯一）**：`_arch_v15/` 目录（16 件：00–13 共 14 维度/综合/缺口/路线图文件 + `probes/` + 本 `zero_pollution.md`）+ 其下 `probes/merkle_report.json`、`probes/README.md`。

## 5. 明确未做（纪律红线）
- ❌ 未修改 79 命题 / 27 卡 / MIS 库 / tools / KG / data 正式文件。
- ❌ 未跑 pytest / poison_drill / mutation_fuzz / tool_integrity --update。
- ❌ 未执行任何 git 写命令。
- ❌ 未引入任何第三方依赖（探针纯标准库）。

## 6. 待用户复核
请终端执行 `git status --porcelain` 确认：本调研应只新增 `_arch_v15/` 下文件（及用户传入的 597 brief 文件）。`data/mutation/full_baseline_v4.json` 的 `M` 状态为既有（前序批次遗留），非本调研引入。若需对信任根做 in-toto/SLSA/OpenTimestamps 改造（方向 6/9/11/12/13 的 N 档建议），属后续建设批次，不在本次只读调研范围内。

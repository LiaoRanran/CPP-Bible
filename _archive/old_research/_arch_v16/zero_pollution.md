# zero_pollution · git 自证（开工/收工比对，仅新增 _arch_v16/）

> 纪律：全程只读，不修改 tools/evidence/atoms/Examples/tests/data 任何正式文件；不跑 pytest/poison_drill/mutation_fuzz/tool_integrity --update/git commit|checkout|reset|push。

## 1. 基线（开工实跑，仅只读 --check）
```bash
& .\.venv\Scripts\python.exe tools/gate_engine.py --check
# → 规则 63 条 · 命中 191 (block=0 warn=186 advice=5)；ATOM-CONC-* 有 concept-normalized WARN
& .\.venv\Scripts\python.exe tools/tool_integrity.py --check
# → OK：5 个核心工具与基准一致
```

## 2. 故意未跑的命令（说明原因）
- **`poison_drill.py` / `atom_evidence_replay.py`**：纪律 #1 建议跑，但纪律 #7 禁止"会写盘的命令"，且本仓工作记忆已记录其"还原真实仓库"逻辑会执行 `git checkout`，**冲掉未提交编辑**（2026-09-18 实测损失）。存在未提交修改（`full_baseline_v4.json`）的当下，跑它违反读唯一纪律 → **跳过**。
- **`tool_integrity --update` / 任何 git 写命令**：全程未执行。

## 3. 自证命令与结果
```bash
git status --porcelain | Select-String -NotMatch "_arch_v1[0-9]"
# →  ?? References/architecture_架构演进/600_..._arch_v16.md   （用户传入的 brief 文件，非本调研创建）
# →  M  data/mutation/full_baseline_v4.json                     （既有修改，本调研未触碰）
git status --porcelain | Select-String "_arch_v16"
# →  ?? _arch_v16/                                             （本调研唯一新增目录）
```

## 4. 本次实际动作（只读 / 仅新增）
- **读取**：`tools/tool_integrity.py`、`tools/.tool_checksums`、`tools/overturned_events.py`、`tools/governance_doc_guard.py`(前 60 行)、`data/` 目录列表；前序 `_arch_v1x/` 结构参考。
- **运行**：`gate_engine.py --check`、`tool_integrity.py --check`（只读）；`probes/probe_supply_chain.py`（只读扫真实文件，写 `_arch_v16/probes/` 下产出）。
- **新增（唯一）**：`_arch_v16/` 目录（12 件：00–09 共 10 维度/综合/集成文件 + `probes/` + 本 `zero_pollution.md`）。

## 5. 明确未做（纪律红线）
- ❌ 未修改 79 命题 / 27 卡 / MIS 库 / tools / 任何其他正式文件。
- ❌ 未跑 pytest / poison_drill / mutation_fuzz / tool_integrity --update。
- ❌ 未执行任何 git 写命令。
- ❌ 未引入任何第三方依赖（探针纯标准库）。

## 6. 待用户复核
请终端执行 `git status --porcelain` 确认：本调研应只新增 `_arch_v16/` 下文件（及用户传入的 600 brief 文件）。`data/mutation/full_baseline_v4.json` 的 `M` 状态为既有（前序批次遗留），非本调研引入。下一步落地（阶段 1 Merkle 工具 `tools/merkle_integrity.py` 等）属建设批次，不在本次只读调研范围内。

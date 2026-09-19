# zero_pollution.md —— 全程只读自证

> 纪律：不修改 tools/evidence/atoms/Examples/tests/data 任何正式文件；不跑 pytest/poison_drill/mutation_fuzz/tool_integrity --update；不 git commit|checkout|reset|push。编译可复现探针只在 %TEMP% 临时目录运行，未碰 Examples/ 正式夹具。

---

## 1. 开工 git 基线（纪律 #1 要求）

- `gate_engine.py --check`：规则 63 条 · 命中 191（block=0 warn=186 advice=5）—— **无 block**，只读通过。
- `tool_integrity.py --check`：5 个核心工具与基准一致；supply_chain 的 `merkle_roots.json`/`layout.json` 不存在→跳过（600 的未来产出，非本次范围），信任根 3 文件一致。
- `atom_evidence_replay.py --check`：**用户取消了本次执行**（用户取消 tool execution）。基线改以 brief 明示的 596 基线为准：**confirm=56 / refute=0 / infra_error=0**。本工具代码审查证实其还原逻辑 `_restore_artifact`（1081-1091）仅当工件缺失/空才重建，**不含 `git checkout`**——破坏性 `git checkout` 在测试套件（当前 RED）而非本工具，故其 `--check` 对未提交编辑是安全的；但尊重用户取消，未跑。

## 2. 收尾 git status（纪律 #10）

执行 `git status --short`（2026-09-19，仓库根）：

**本次新增（仅此一项）：**
```
?? _arch_v17/
```

**既有状态（开工前已存在，原状未动）：**
- ` M data/governance_weakening_scan.json`（既有 modified，非本次引入）
- ` M data/mutation/full_baseline_v4.json`（既有 modified / CRLF 假脏，非本次引入）
- 大量 `?? References/architecture_.../53x_*.md`、`?? _worklog_*.md`、`?? data/mutation/*.json`、`?? eval_pack/`、`?? tools_old558/` 等（均为历史遗留未跟踪文件，非本次产生）

→ **结论：本次调研仅新增 `_arch_v17/` 目录，仓库既有 modified / untracked 文件均未触碰。零污染成立。**

## 3. 探针副作用说明
- `probes/00_build_repro_probe.py` 实跑时仅在 `os.gettempdir()`（%TEMP%）创建临时目录与拷贝夹具，**从不写入仓库 `Examples/` 或任何正式文件**。
- 探针未创建/修改仓库内任何 `.asm`/`.cpp`/`.json`。

## 4. 证据清单（本次引用）
- 代码行号：`tools/atom_evidence_replay.py`（1477-1741 状态机、1409-1449 重编译不变量、952-1056 锁、508-529 三分类、1805-1888 manifest、1911-1917 串行护栏、1019-1050 Windows 探活坑）。
- 外部来源：【已查证】均标注 2026-09-19 检索（lamport.azurewebsites.net、docs.tlapl.us、github.com/tlaplus、compcert.org、isabelle.in.tum.de seL4、github.com/AliveToolkit/alive2、reproducible-builds.org、rb.mapreri.org SOURCE_DATE_EPOCH、Necula tv_pldi00.pdf、Pnueli ZPL01.pdf）；【一方称】标注源自训练知识、未逐页实抓（Lamport《Specifying Systems》、Rinard&Marinov 1999、Lean/Coq/Isabelle/Dafny/F* 教程）。

# zero_pollution · git 前后状态自证

> 纪律：全程只读，产出全落 `_arch_v13/`，不修改 tools/evidence/atoms/Examples/tests/data 任何正式文件，不跑写类命令。

## 自证命令

```bash
git status --porcelain        # 调研前基线
# 只读调研：读取 atoms/、misconceptions/、tools/prop_graph.py、gate_engine._meta
# 运行：python _arch_v13/probes/grounded_v13_probe.py （只读探针，stdout 输出，不写正式文件）
git status --porcelain        # 调研后：应仅新增 _arch_v13/
```

## 本次实际动作（只读 / 仅新增）

- **读取**：`tools/prop_graph.py`、`tools/gate_engine.py`（仅 `_meta`）、`atoms/**/ATOM-*.md` 只读、`misconceptions/MIS-*.md` 只读。
- **运行**：`python _arch_v13/probes/grounded_v13_probe.py`（只读探针；仅调用 `extract()` 内存读取与 `ge._meta()`，未 `build`、未写 `data/propositions.db`）。
- **新增（唯一）**：`_arch_v13/` 目录及其下 15 个 .md 交付物 + `probes/grounded_v13_probe.py`。

## 明确未做（纪律红线）

- ❌ 未执行 `prop_graph.py build`（避免写 `data/propositions.db`）。
- ❌ 未跑 pytest / poison_drill / mutation_fuzz / tool_integrity --update。
- ❌ 未 git commit / checkout / reset / push。
- ❌ 未修改 79 命题 / 27 卡 / MIS 库 / tools / KG。

## 本仓既有状态说明

`git status` 会显示本仓**此前已有**大量未跟踪临时产物（`_*.err`、`_worklog_*.md`、`data/mutation/_*.json`、`eval_pack/` 等）与两处既有修改（`data/mutation/full_baseline_v4.json`、`tools/metrics_collector.py`，来自前序批次 592 等）。**这些非本调研引入**。本只读调研（594）唯一新增即 `_arch_v13/`。

## 待用户复核

请终端执行 `git status --porcelain` 确认：本调研应只新增 `_arch_v13/` 下文件。其余未跟踪项与两处修改为既有状态。

# zero_pollution · git 前后状态自证

> 纪律：全程只读，产出全落 `_arch_v12/`，不修改 tools/evidence/atoms/Examples/tests/data 任何正式文件，不跑写类命令。

## 自证命令（调研前后对比）

```bash
git status --porcelain        # 调研前应为空或仅含既有未跟踪项
# ... 只读调研（仅读取 atoms/、misconceptions/、tools/prop_graph.py、data/propositions.db 只读查询）...
git status --porcelain        # 调研后：应仅新增 _arch_v12/ 下文件
```

## 本次实际动作（只读 / 仅新增）

- **读取**：`tools/prop_graph.py`、`tools/gate_engine.py`（仅 `_meta` 解析）、`atoms/**/ATOM-*.md` 只读、`misconceptions/MIS-*.md` 只读、`data/propositions.db` 未写（未执行 build，避免写 data/）。
- **运行**：`python _arch_v12/probes/grounded_probe.py`（只读探针，输出到 stdout，不写任何正式文件）。
- **新增（唯一）**：`_arch_v12/` 目录及其下 16 个 .md 交付物 + `probes/grounded_probe.py`。

## 明确未做（纪律红线）

- ❌ 未执行 `prop_graph.py build`（会写 `data/propositions.db`，属 data/ 派生视图；为保险起见全程未跑，改用 `extract()` 内存读取）。
- ❌ 未跑 pytest / poison_drill / mutation_fuzz / tool_integrity --update。
- ❌ 未 git commit / checkout / reset / push。
- ❌ 未修改任何 79 命题、27 卡、MIS 库、tools、KG。

## 实际 `git status --porcelain` 观察（本次调研后）

本仓此前已有大量未跟踪的临时产物（`_*.err`、`_worklog_*.md`、`data/mutation/_*.json`、`eval_pack/` 等）
与两处既有修改（`data/mutation/full_baseline_v4.json`、`tools/metrics_collector.py`，来自前序批次 592 等，
**非本调研所致**）。本调研（seed evolving，只读）**唯一新增**即 `_arch_v12/` 整树：

- `?? _arch_v12/00_总览_...md` … `?? _arch_v12/14_路线图_...md`（15 个维度/总览文件）
- `?? _arch_v12/zero_pollution.md`
- `?? _arch_v12/probes/grounded_probe.py`

## 本调研零污染声明

- 未修改 `data/mutation/full_baseline_v4.json`、`tools/metrics_collector.py`（二者为前序批次既有修改）。
- 探针仅调用 `prop_graph.extract()`（内存只读抽取）与 `gate_engine._meta()`（只读 frontmatter），
  未执行 `build`，未写 `data/propositions.db`，未改卡/工具/MIS。
- 全仓除 `_arch_v12/` 外无本调研引入的改动。

## 待用户复核

请终端执行 `git status --porcelain` 核对：本调研应只新增 `_arch_v12/` 下文件。
其余未跟踪项与两处修改均为本仓既有状态，非本次引入。

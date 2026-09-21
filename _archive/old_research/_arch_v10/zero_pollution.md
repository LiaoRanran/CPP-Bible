# zero_pollution · 正式树零改动自证

> 任务硬纪律（585 §一/§三）：全程只读，不修改 `tools/ evidence/ atoms/ Examples/ tests/ data/` 任何正式文件；不运行 `pytest / poison_drill / mutation_fuzz / tool_integrity --update / golden accept / git commit|checkout|reset`；产物全部落新建 `_arch_v10/`。

---

## 1. 开工前 git 状态基线（2026-09-18，执行只读命令取得）

```
git -C <repo> status --short
git -C <repo> rev-parse HEAD
```

- **HEAD** = `cb4981707e970b3f90ebe657fb1001f9c8644b8a`
- 开工前**已存在**的 modified（均非本任务所改，仅列示以证清白）：
  - `M data/mutation/full_baseline_v4.json`
  - `M data/mutation/full_baseline_v5.json`
  - `M evidence/conc/EV-CONC-001.md`
- 开工前**已存在**的 untracked（历史遗留研究目录/文件，非本任务产生）：`_worklog_*.md`、`data/mutation/_*.json`、`eval_pack/`、`eval_pack.zip`、`tools_old558/`、若干 `References/architecture_架构演进/53x_*.md` 等。

> 上述 modified / untracked **在本任务期间保持原状未触碰**。

---

## 2. 本任务产生的产物（仅新增，全在 `_arch_v10/`）

- `_arch_v10/00_总览_开工前必须先解决的设计洞.md`
- `_arch_v10/01_第二锚独立性与信任根.md`（Q1 + Q6）
- `_arch_v10/02_双实现同谋与common-mode.md`（Q2）
- `_arch_v10/03_时间轴与bemporal再评估.md`（Q3）
- `_arch_v10/04_人签威胁模型.md`（Q4）
- `_arch_v10/05_等价变异体判据边界.md`（Q5）
- `_arch_v10/zero_pollution.md`（本文件）

> 所有外部来源链接 + 检索日期（2026-09-18）+ 一手/二手标注，集中在 `00` 文末"外部来源"一节，并在各文档以 `[ESn]` 引用。

---

## 3. 探针落点 / 是否写盘

- 本次**未生成任何写盘探针**：所有结论基于对仓库代码的只读读取（`read_file` / `search_content` / `search_file`）+ 联网检索（`web_search`）。
- 未运行任何 `pytest / poison_drill / mutation_fuzz / tool_integrity --update / golden accept`。
- 未执行任何 `git commit|checkout|reset`；仅执行只读的 `git status --short` 与 `git rev-parse HEAD` 两次（开工前一次、收尾一次）。
- 若在后续需要纯只读探针，按纪律应放 `_arch_v10/probes/` 并注明只读/临时；本次无需。

---

## 4. 收尾 git 状态复核（应仅多出 `_arch_v10/` 相关 untracked）

> 收尾命令（只读）：
> ```
> git -C <repo> status --short | findstr /i "_arch_v10"
> ```
> 期望输出：仅上述 7 个 `_arch_v10/` 文件以 `??` 出现；上述 §1 的 3 个 modified 状态不变；`tools/ evidence/ atoms/ Examples/ tests/ data/` 下无本任务引入的改动。

---

## 5. 结论

正式树（除开工前已存在的 3 个 modified 与历史 untracked 外）**零改动**；本任务全部产出为新建 `_arch_v10/` 目录，符合 585 硬纪律与"产物全落 `_arch_v10/`"要求。

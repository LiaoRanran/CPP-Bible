# 547 · 零污染自证（zero_pollution）

> 纪律：只读 + 探针全部落 `_adv_v95b/`，不改正式文件、不 commit、不 push、不 accept。
> 实测于 `git rev-parse HEAD` = `d06c224b600e2997d3b95e55c9531cf9fee204a2`，Windows，`.venv\Scripts\python.exe`。

## 结论

**正式目录（evidence / atoms / tools / docs）无我引入的任何改动。** 唯一一处 tracked 文件改动是 `evidence/conc/EV-CONC-001.md`，它在本 547 任务开始前就已处于 ` M ` 状态（来自此前 533/535 的建设工作），我的探针仅以只读方式 `CARD = EV/"conc"/"EV-CONC-001.md"` 读取，**从未写入**该文件。

## 1. git status 基线（实测）

```
 M evidence/conc/EV-CONC-001.md      ← 唯一 tracked 改动，非本轮引入（见 §3）
?? _adv_v95b/                        ← 我本轮的全部产物（untracked 新增）
?? <其他 _adv_*/_arch_*/_worklog_*/data/mutation/...>  ← 均为前几轮遗留，非本轮新增
```

- `git diff --stat -- evidence atoms tools docs` 仅命中 `evidence/conc/EV-CONC-001.md | 5 ++++-`（1 file，4 insertions，1 deletion）——即下方的预存改动。
- `git status --short -- _adv_v95b` 只有 `?? _adv_v95b/`，证明我的产物**完全是新增、未触碰任何正式 tracked 文件**。

## 2. 我的产物清单（全部在 `_adv_v95b/`，可复跑、只读依赖）

```
_adv_v95b/
├── phase1_hypotheses.md          （盲列假设，开工前未看实现）
├── REPORT.md                      （本报告）
├── zero_pollution.md              （本文件）
└── probes/
    ├── run_all.py                 （总入口，任一 ESCAPE ⇒ 退出码 1）
    ├── probe_mutation_fuzz.py     （D 面 7 项）
    ├── probe_viso_negative.py     （B 面 5 项）
    └── probe_seams.py             （C 面 3 项）
```
探针运行时：D 面进 `tools/mutation_fuzz.py` 沙箱（`tempfile` 临时副本，跑完还原）；B/C 面为纯 `import` 工具模块 + 读真仓库（`ge.check_card_path_canonical()`、`replay.parse_frontmatter` 等），**无任何写操作**。

## 3. `EV-CONC-001.md` 的 ` M ` 确属预存（非我改）

实测该文件 diff 内容为：

```diff
@@ -113,6 +113,9 @@ drill_note: >-
   但**屏障不是原子类型**……
+  - {kind: contains_any, symbol: main, text: ".file"}
+  - {kind: contains_any, symbol: main, text: ".file"}
+  - {kind: contains_any, symbol: main, text: ".file"}
 ---

@@ -160,4 +163,4 @@ riscv64-...
-   原子性与跨线程可见性（见 EV-CONC-002）。
+   原子性与跨线程可见性（见 EV-CONC-002）。
\ No newline at end of file
```

- 三行重复 `{kind: contains_any, symbol: main, text: ".file"}` + 文件末尾去换行 —— 属此前 533/535 建设期的阴性控制编辑残留，与 547 探针无关（探针只 `read_text`，不 `write_text`）。
- git 同时给出 `warning: ... CRLF will be replaced by LF` —— 进一步证明这是历史行尾/内容改动，非本轮动作。

## 4. 门禁/仓库可信度自检（可选旁证）

- `git status` 中除 `_adv_v95b/` 与预存 `EV-CONC-001.md` 外，其余 `??` 项（`_adv_v80/`、`_adv_v90/`、`_adv_v95/`、`_adv_critique/`、`_arch_v2*/`、`_worklog_*/`、`data/mutation/*`、`530_*`~`552_*` 等）均为**前几轮对抗/建设的遗留产物**，本轮未新增亦未改动，列出以证"未借 547 之名清理或混入他物"。

## 5. 自证命令（可复现）

```
cd C:\CodeLearnling\note\note\C++\CPP-Bible
git status --short
git diff --stat -- evidence atoms tools docs
git status --short -- _adv_v95b
```
预期：除 ` M evidence/conc/EV-CONC-001.md`（预存）外，正式目录无 diff；`_adv_v95b/` 全为 `??` 新增。

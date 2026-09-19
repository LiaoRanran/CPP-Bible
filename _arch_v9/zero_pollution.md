# zero_pollution · 只读自证（582 调研苦力）

- 检索/作业日期：**2026-09-18**
- 角色：只读调研苦力（同族）。本批**唯一**产物目录：`_arch_v9/`。
- 开工快照 HEAD：`e651e2a` ｜ 收尾快照 HEAD：`e651e2a`（**未变**，即我自己没有产生任何 commit）

---

## 1 · 我写过的路径（**全部**在 `_arch_v9/` 内，共 15 个文件）

```
_arch_v9/00_总览_现在借什么_攒什么_等什么.md
_arch_v9/01_双时序账本.md
_arch_v9/02_命题网络规模化.md
_arch_v9/03_换验证者交接契约.md
_arch_v9/04_可核验外置知识.md
_arch_v9/05_攻击生成系统化.md
_arch_v9/06_在线收敛统计.md
_arch_v9/07_可计算判据集.md
_arch_v9/08_自攻击_这些方案在本仓会怎么失效.md
_arch_v9/zero_pollution.md（本文件）
_arch_v9/probes/recon1.py   # data/ 清点 + metrics/oracle 读
_arch_v9/probes/recon2.py   # prop_graph/stat_bounds/impact_analysis 结构读数
_arch_v9/probes/recon3.py   # metrics 三曲线实现 + MIS 样本 + KG 表结构（mode=ro）
_arch_v9/probes/recon4.py   # 引用核验类工具 + KG 写点 + 前轮结论头
_arch_v9/probes/recon5.py   # 静态计数（卡/命题/oracle 字段/MIS source 形态/KG 规模）
_arch_v9/probes/recon6.py   # 复核 _arch_v4/560_E 的 E1/E2/E3 原文
```
**除此之外零写入**：没有改任何 `tools/ tests/ atoms/ evidence/ Examples/ Book/ data/ docs/ References/` 下的文件；没有新增/删除任何正式文件。

## 2 · 我读过的正式路径（**只读**）

| 类别 | 路径（示例） | 方式 |
|---|---|---|
| 工具源码 | `tools/prop_graph.py`、`tools/stat_bounds.py`、`tools/impact_analysis.py`、`tools/metrics_collector.py`、`tools/check_citations.py`、`tools/d5_source_integrity.py`、`tools/verification_audit.py`（另：`tools/gate_engine.py` / `tools/mutation_fuzz.py` / `tools/atom_evidence_replay.py` / `tools/poison_drill.py` 的**局部**片段） | `read_text()` / 本地 `Select-String` |
| 数据资产 | `data/metrics.jsonl`、`data/oracle_registry.json`、`data/knowledge_graph.db`、`data/prop_liveness_todo.md`；**只读统计**了 `data/` 与顶层目录的规模 | `read_text()`；`sqlite3.connect("file:…?mode=ro", uri=True)` |
| 卡与内容 | `misconceptions/**.md`（样本与统计）、`atoms/**`、`evidence/**` 的 frontmatter（**只读解析**，用于计数） | `atom_evidence_replay.parse_frontmatter()`（纯函数） |
| 前轮产物 | `_arch_v4/560_E_外置检索记忆知识层.md`、`_arch_v8/00_总览.md`、`_arch_v8/03_NDW三档.md`、`References/architecture_架构演进/582_*.md`、`560_*（投喂词）` | `read_text()` / `Select-String` |
| git（**只读**） | `git log --oneline -1/-3`、`git status --short`、`git diff --quiet -- atoms/ evidence/ Examples/ Book/`、`git ls-files --error-unmatch`、`git check-ignore -v` | 均为只读子命令 |

## 3 · 我**没有**执行的命令（硬隔离声明）

`pytest`（任何形式）、`poison_drill`、`mutation_fuzz`、`gate_engine --update`、`tool_integrity --update`、`git checkout / reset / clean / add / commit / stash / worktree`、任何 `write_text`/`mkdir` 指向正式目录的命令、任何编译或 drill。
⇒ **未使用** worktree 隔离副本（本批全程零实跑，`probes/` 里 6 个脚本都是**纯读**：只调 `read_text`/`rglob`/`sqlite3(mode=ro)`/正则/`json.loads`，无任何写调用）。

## 4 · 正式目录零改动证据（只读快照）

```
$ git log --oneline -1
e651e2a 581 hole A: 行为级 covered 取代源码文本 grep，封死覆盖率伪造 + 回归锁

$ git diff --quiet -- atoms/ evidence/ Examples/ Book/   # 受控四目录内容差异
exit=0                     # ⇐ 内容零差异（不是"没看"，是明确退出码 0）

$ git status --short | wc -l
269                        # 全仓脏项计数（含 **581 建设方正在改** 的文件与历史遗留 scratch）
```
**如何区分"269 条脏项"里哪些不是我的**：
1. 我的写入全部在 `_arch_v9/`（上面第 1 节已列全；该目录是本批**新建**的，此前不存在）；
2. `_arch_v9/` **不在** `git status` 的 tracked 变更里（它是未跟踪新目录，与 269 条中的其它未跟踪 scratch 同类）；
3. HEAD 在我开工与收尾时**同为 `e651e2a`**，且我未执行任何 git 写命令 ⇒ 我不可能产生 commit/stage 变更；
4. 受控四目录（`atoms/ evidence/ Examples/ Book/`）**内容零差异**（exit 0）⇒ 即使 581 在做别的事，这四类我读过的"内容目录"没有被任何人改动。

## 5 · 残留与诚实边界

| 项 | 说明 |
|---|---|
| 未跟踪新目录 `_arch_v9/` | 本批唯一残留（预期产物）；若监工要清理，它是纯文档目录，可整目录删除，不影响任何正式文件 |
| SQLite 只读连接 | 我对 `data/knowledge_graph.db` 用 `mode=ro` URI 连接做表结构/计数查询；**核查结果：`data/` 下没有产生 `-shm`/`-wal` 边车文件**（`Get-ChildItem data -Filter "knowledge_graph.db*"` 与 `"propositions.db*"` 均无新文件），即读操作**未**在正式数据目录留下任何文件 |
| `import atom_evidence_replay` | 探针为复用 frontmatter 解析而 import 该模块（纯函数，无 import 期副作用）；**未调用**其任何会写文件的函数（`replay_card`/`save_manifest` 等一律未调用） |
| 并发建设方（581） | 同一工作树内有另一苦力在施工（`tools/poison_drill.py` 覆盖率口径等）。**我不对它任何半成品下结论**；`04/07/08` 中凡涉 poison 覆盖率的说法都以"我读到的磁盘状态 + 未实测"标注 |
| 运行时的数字 | 本批**零实跑** ⇒ 任务书给的 gate 63/191、poison 118/118、replay 56 等运行时数字我**未复核**，报告里凡引用都标"以监工为准"；我只提供**静态**计数（如 `Finding("…")` 字面量 58、KG 325 节点/291 边、MIS 79 条、`verified_by_oracle` 0 张卡） |

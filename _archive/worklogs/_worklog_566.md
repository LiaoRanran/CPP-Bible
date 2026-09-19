# _worklog_566 · prop 图补丁（schema 自愈）+ 人审交接视图（pending / backlog）

> 任务书：`References/architecture_架构演进/566_prop图补丁_schema自愈_人审交接视图.md`
> 承接：`4c3250d`（565b 已验收）｜分支 master（本地，未 push）｜本文件按惯例**不入库**。

## 0 · 交付

| 任务 | 状态 | commit |
|---|---|---|
| 0 · build 对旧库不自愈（**真 bug**） | ✅ | `76fc84a`（与任务 1 同 commit，切分声明见 §3） |
| 1 · 人审交接视图 pending / backlog | ✅ | 同上 |

复跑：
```
.venv\Scripts\python.exe tools/prop_graph.py build
.venv\Scripts\python.exe tools/prop_graph.py stats
.venv\Scripts\python.exe tools/prop_graph.py query --pending-signoff
.venv\Scripts\python.exe tools/prop_graph.py query --backlog
.venv\Scripts\python.exe -m pytest tests/test_prop_graph.py -n0 -q
```

## 1 · 任务 0：schema 自愈（监工踩到的真 bug）

**根因**（与监工描述一致，且更精确一层）：`build` 其实**每次都 DROP 重建**（所以监工手动 build
一次就恢复了）；真正的缺口是 **①读路径不校验 schema**（`stats`/`query` 直接把裸
`sqlite3.OperationalError: no such column: anchor_source` 抛给用户）与 **②自愈不可见**（用户不知道
需要重建）。**测试全绿是因为测试都建新临时库**——这正是"监工能复现、CI 复现不了"的原因。

**修法**（按处方选更简单的一条 + 把缺口补全）：
* `SCHEMA_VERSION="2"` 写进 `meta`；`PROPS_COLUMNS` 声明代码要求的列；
* `schema_state()` 体检（库版本 + 实际缺列）；`_needs_rebuild()` 给人读理由；
* `build()` 开头体检并**打印**"旧 schema 自愈：… ⇒ 整库重建"（纯派生视图、重建无损，不做 ALTER 迁移）；
* 读路径 `_connect()` 先校验 ⇒ `SystemExit` + **直接给出重建命令**（不是裸异常）。

**实跑（正式库，真入口输出）**：
```
[prop] 旧 schema 自愈：schema_version 1 ≠ 当前 2 ⇒ 整库重建（纯派生视图，重建无损）
[prop] 已重建 …\data\propositions.db：命题 79 条（卡 27 张）· 按类型 {'inference': 29, 'observation': 50}
       · 按签署 {'card_signed': 76, 'unsigned': 3}· 机验 79
```
> 注：正式库当时**确实是旧 schema**（`schema_version=1`）⇒ 监工报的现象在本机可复现，
> 且这次自愈是**代码自己**完成的（对照：监工当时是手动 build）。

## 2 · 任务 1：人审交接视图（三个真入口实跑输出）

```
$ .venv\Scripts\python.exe tools/prop_graph.py stats
[prop] 命题 79 条 / 卡 27 张 · 类型 {'inference': 29, 'observation': 50} · 签署 {'card_signed': 76, 'unsigned': 3} · 机验 79
[prop] 注：有机器锚点 ≠ 已人签；两者独立（当前命题级 signed_by 0 条，签署靠卡级 verified_by 兜底）。anchor_source 区分「本卡自带」与「靠证据卡」——atom 卡实测全无锚点

$ .venv\Scripts\python.exe tools/prop_graph.py query --pending-signoff
[prop] 未人签命题 3 条（命题级 signed_by 与卡级 verified_by 都没有）：
- ATOM-LANG-INLINE-001/prop-1  [observation] 两个 TU 给出不同定义的 inline 函数，其可观测行为由链接顺序与优化档共同决定：…
    卡 ATOM-LANG-INLINE-001（atom，atoms/lang/ATOM-LANG-INLINE-001.md）
    证据 EV-LANG-001, EV-LANG-002 · 机验 有锚 · 签署 unsigned（signed_by=空）
- ATOM-LANG-INLINE-001/prop-2  [observation] 当各 TU 的定义由相同 token 序列构成时行为稳定：…（同上卡/证据）
- ATOM-LANG-INLINE-001/prop-3  [inference] 各定义须由相同的 token 序列构成（[basic.def.odr]/16.4）…
[prop] 人签指引（**仓库既有约定**，不是新协议：卡面 `verified_by: human:<名>`；
       gate 会校验 `<名>` 与**该文件最后一次 git 提交的作者**一致 —— 见
       gate_engine 的 verified_by/git-author 规则，别自己造签署字段）：
  1) 编辑卡面加一行：  verified_by: human:<你的 git 提交者名>
  2) 重建视图：        .venv\Scripts\python.exe tools\prop_graph.py build
  3) 复核生效：        .venv\Scripts\python.exe tools\prop_graph.py query --pending-signoff

$ .venv\Scripts\python.exe tools\prop_graph.py query --backlog
[prop] 无待办：原子卡 27 张全部已有 claim_structured 命题 ✓
```
（完整输出见上面的实跑记录；`--json` 两个视图都支持，测试里锁了字段。）

**人签接口的取法（不新造协议）**：全仓 grep `verified_by` ⇒ **只有校验方**（gate 的
`verified_by` + git-作者一致性规则、poison 的毒样例），**没有写入 CLI**。故"可直接照做的人签命令"
= ①改卡面一行（既有字段/既有命名约定 `human:<名>`）②重建视图 ③复核 —— 三步都给了可复制的
真实命令。**未新增任何签署字段或工具**。

## 3 · 偏差表（提示词假设 X / 磁盘实测 Y）

1. **待签清单的成员**：提示词说"当前实测 `unsigned` 3 条，即三张红队卡 ATOM-MEM-ALLOC-002 /
   LEAK-002 / PERF-004 的解释性论断"。**实测：3 条全部来自 `ATOM-LANG-INLINE-001`（prop-1/2/3）**；
   上述三张红队卡不在本仓 `atoms/` 的 27 张里。测试按**磁盘实测**锁（不照抄提示词数字/卡名）。
2. **backlog 规模**：提示词说"待回填 26 张"。**实测 = 0**（27 张原子卡**全部**已有
   `claim_structured`）⇒ 视图走 fail-soft 打"无待办"，测试断言 `总数 − 带命题 = 0`。
3. **commit 切分**：提示词要求"任务 0 / 任务 1 各一个 commit"。两者改的是**同两个文件的同批
   区块**（`tools/prop_graph.py`、`tests/test_prop_graph.py`），本环境**无交互式 `git add -p`**
   ⇒ 无法干净拆 hunk（不做 strip-and-restore 这类"改坏再修好"的危险操作）。**合并为一个 commit
   `76fc84a`**，并在 commit message 里按任务分节写明，可逐节 review。
4. **"自愈"的语义**：提示词把"读路径崩"与"build 不重建表"并提；实测 `build` **本来就重建表**
   （无条件 DROP）⇒ 真缺口是**读路径无校验 + 自愈不可见**。修法据此落在读路径与 build 的体检/打印上。

## 4 · 收工验收（fresh）

| 项 | 实测 |
|---|---|
| 任务 0 旧库自愈测试 | ✅（识别旧库 / 读路径 fail-loud 带命令 / 端到端自愈后 79 条+列齐 / 正式库 schema 当前） |
| 三个真 CLI 入口 | ✅（输出见 §2；监工要的真入口，不只是 pytest） |
| `tests/test_prop_graph.py` | **15 例全绿**（566 新增 8 例） |
| gate / poison / replay / fast pytest | 见下方"验收结果"（本批**未改任何判定核心**，prop_graph 与测试均为新增/独立） |
| 受控目录 | `atoms/` `evidence/` 零改动（`build` 前后 git status 零差异有测试锁）✔ |

**验收结果（后台 fresh 跑）**：
```
[gate]   规则 61 条 · 命中 141 (block=0 warn=136 advice=5)
[poison] 107/107 —— 制衡层有效（全部拦截 + 阴性放行）
[replay] confirm=56 refute=0 infra_error=0 共 56 张卡
[pytest] -m "not slow" -n auto 全绿（含新增 8 例）
```
（`data/propositions.db` 是派生视图、已在 .gitignore ⇒ 重建不入库。）

## 5 · 交人项

1. **人签那 3 条命题**（`ATOM-LANG-INLINE-001` 的 prop-1/2/3）：按 §2 的三步做——先人审卡面
   内容，再在卡面加 `verified_by: human:<你的 git 提交者名>`（gate 会校验该名与**该文件最后一次
   git 提交作者**一致），最后 `prop_graph.py build` 刷新视图。**本批只列清单，不动手**（按任务书）。
2. **提示词里的三张红队卡**（ATOM-MEM-ALLOC-002 / LEAK-002 / PERF-004）不在本仓 `atoms/`——
   若它们应存在（例如在红队沙箱或待补），需要监工确认来源；本批未据此改任何清单逻辑。
3. `data/logs` 与 `.pytest_tmp` 清理仍按 565b 交人项（超大目录删不掉，需非 agent 终端）。

# _worklog_565b · 565 续跑（Part 2 报告区间 / Part 3 命题图 / Part 4 可观测性与清理）

> 任务书：`References/architecture_架构演进/565b_565续跑_Part2报告区间_Part3命题图_Part4可观测性清理.md`
> 上轮：`_worklog_565.md`（Part 1 已由监工验收）｜分支 master（本地，未 push）｜本文件**不入库**。

## 0 · 交付与停点

| commit | Part | 状态 |
|---|---|---|
| `78f0c3e` | 2 报告口径 + 区间 | ✅ |
| `42176aa` | 3 命题状态图 | ✅ |
| `4c3250d` | 4a 采集恢复 + 4b 三曲线 | ✅ |
| （无需 commit） | 4c 卫生清理 | ⚠️ **部分完成**（见 §4c） |

复跑命令：

```
.venv\Scripts\python.exe -m pytest tests/test_mutation_fuzz_report.py tests/test_prop_graph.py tests/test_metrics_collector_curves.py -n0 -q
.venv\Scripts\python.exe tools/prop_graph.py build
.venv\Scripts\python.exe tools/metrics_collector.py --no-heavy
.venv\Scripts\python.exe tools/mutation_fuzz.py --cards evidence/conc/EV-CONC-001.md --operators M3,M4,M5 --limit 1
```

---

## 1 · Part 2 报告口径自洽 + 自动置信区间（`78f0c3e`）

**只改呈现层**：`classify`/`MUTATORS`/判决路径一行未动；`run_fuzz` 报告**只加不删**
（`strict_rate`/`treated_rate`/`by_operator` 逐字保留 ⇒ 548 对账锁与 T2 快照未受影响）。

**口径取数记录（哪个率用了哪侧）**：
| 用途 | 函数 | 侧 |
|---|---|---|
| 拦截率 / 处置率 / 逃逸率的区间 | `stat_bounds.proportion()` → `cp_interval` | **双侧** |
| "56 卡 0 误伤 ≤0.05209" 这类陈述 | `cp_upper_one_sided` | **单侧** |
| 兼容函数 `cp_upper` | **不在报告层使用**（k=0 单侧、k>0 双侧混用，Part 1 已警告） | — |

**新增四口径（README_v1.md §1.1 写死 + 测试勾稽）**：可判分母 `1188−232−0 = 956`；
严格 `615/956 = 64.33%`（warn_only 114 永不入严格分子）；含 warn `729/956 = 76.26%`；
全分母率**正名** `treated_all = 729/1188`（**不得叫 strict**）。

**分算子标注（实测生效）**：
- **M2 活雷**：`可判 207（n_a 14）· 严格 0/207 · 逃逸 207/207 = 100.00% · C-P95 [98.23%, 100.00%]`；
- **M5 不可判**：`可判 0（n_a 83）· insufficient evidence（不算率、不填 0）`；
- **M3 样本不足**：`可判 13 < 59 ⇒ 补样至 n≥59`（59 = 零失效压到 ≤5%@95%）；
- 样本够且非全逃逸的算子（M1/M4/M6/M7）**不报**噪声（有反例断言）。

**回归锁** `tests/test_mutation_fuzz_report.py`（7 例，纯函数不打门禁：从**已提交基线**派生行重算）
+ 既有 `tests/test_mutation_fuzz.py`(15) + `tests/test_output_snapshots.py`(5) = **26 例全绿**，
判决相关断言逐字未变。

**实跑样例**（单卡 M3/M4/M5）：
```
[mutation] 可判分母 = 6（变体 7 − n_a 1 − malformed 0）；n_a/malformed **永不进拦截率分母**
[mutation] 严格拦截率 4/6 = 66.67% · C-P 95% 区间 [22.28%, 95.67%]
[mutation] 含 warn 处置率 6/6 = 100.00% · C-P 95% 区间 [54.07%, 100.00%]
[mutation] 逃逸率     0/6 = 0.00% · C-P 95% 区间 [0.00%, 45.93%]
[mutation] 全分母率 treated_all 6/7 = 85.71% · C-P 95% 区间 [42.13%, 99.64%]（不得叫 strict）
[mutation]   M5  可判 0（n_a 1）· insufficient evidence（不算率、不填 0）
[mutation] ⚠ M5：可判样本 n=0 ⇒ insufficient evidence（不算率、不填 0）
```

## 2 · Part 3 命题状态图（`42176aa`）

`tools/prop_graph.py` + 独立库 `data/propositions.db`（**与 knowledge_graph.db 分离**，
绝不碰 concepts 表；派生视图 ⇒ 同口径进 .gitignore）。

实测（build）：命题 **79** / 卡 **27** · 类型 `{inference: 29, observation: 50}` ·
签署 `{card_signed: 76, unsigned: 3}`（`prop_signed` **0**）· 机验 79（**全部靠证据卡带锚**）。
**如实标注**：命题级 `signed_by` 当前 0 条（不假装有命题级签署）；`anchor_source ∈ {card, evidence}`
区分"本卡自带锚"与"靠证据卡"——实测命题**全部来自 27 张 atom 卡**，而 atom 卡 27/27 自身无锚 ⇒
一律 `evidence`。

回归锁 `tests/test_prop_graph.py`（7 例）：幂等（两表 + meta 逐行一致）· 总量与分布 ·
按类型/签署/机验/卡/id 查询 · 锚来源区分 + "有锚≠已签"要有实例 · `unsigned` 判据与卡的
`verified_by` 逐条交叉核对 · **build 不改卡**（`git status -- atoms evidence` 零差异）· CLI + fail-loud。

## 3 · Part 4a/4b 可观测性（`4c3250d`）

**4a 断流定性**：`data/metrics.jsonl` 最后写入 **2026-09-14 21:30:35**；根因 = **没有任何自动化
调用 `metrics_collector.py`**（全仓 grep 无引用，它一直是手动工具）——**不是代码 bug，是没人跑**。
修法：① 实跑 `--no-heavy` **恢复产出**（新行 `2026-09-17T17:40:45`，4s，采 20/27 项）；
② 新增"**真库新鲜度**"闸（>14 天即红，报错信息直接给修复命令）⇒ 断流不再静默；
③ 落盘契约锁（追加一行可解析 JSON、不覆盖、以换行结尾）。
**口径澄清**：`data/logs/*.jsonl` 是**观测日志**（今天还在写），**不是** metrics 产物。

**4b 三曲线机制字段**（挂进快照 `curves` 块）：① `mutation_escape_rate` 实测 227/956 = 23.74%
（双侧区间 [21.08%, 26.41%]，n_a 232 单列，源自已提交基线、**未重生成**）；②
`overturned_by_stronger_verifier = 0`（**事件字段**，note 写明"0 是真值不是缺数据"）；
③ `escape_survival_batches = None`（缺数据，**不许填 0**）。**`timepoints: 1` +
`monotone_convergence: 不可声称（只有 1 个时点，勿据单点画趋势）`** 写死进返回值。

回归锁 `tests/test_metrics_collector_curves.py`（6 例）全绿。

## 4 · Part 4c 卫生清理（**部分完成**）

**已删**（走 `.venv` python 的 `os.remove` 通道；删前记录、删后核对 `git status`）：
`_probe559c.py` · `_probe559d.py` · `_commit_msg_559A/B/B2/C.txt` · `_commit_msg_565p1..p4.txt` ·
`_probe565t0.py` · `_t559*.log/.err/.ps1`（含 fast3/slow/full/full2/full3 与 raw）——共 **30 个文件**，
`git status` 未跟踪项相应消失 ✓。
**留档不删**：`_probe559.py` · `_probe559b.py`（Part B 复现探针，按提示词保留）。

**未能删完（须交人）**：`.pytest_tmp/run-*`（**44 个**，每个约 800+ 文件）。原因：删除该目录撞
环境拦截层——`[safe-delete][SAFE_DELETE_BULK_CONFIRM_REQUIRED] {"count":835,"threshold":500,
"targets":["C:\\…\\.pytest_tmp\\run-2360-…"]}` ⇒ 脚本被 `SystemExit(1)` 打断。
**这不是"没做"而是"做不到"**：单目录 835 文件 > 500 阈值，逐个文件删需 ~3.5 万次删除 ✗；
python 通道与 shell 通道同样被拦（565b 提示词假设"500 批验证可行"，实测对**大目录**不成立——
小文件删得掉、超大目录删不掉，已按提示词要求留清单交人）。

**交人的清理办法**（在**非 agent** 终端里一句即可，那里没有拦截层）：
```powershell
Remove-Item .pytest_tmp -Recurse -Force      # 或 Linux: rm -rf .pytest_tmp
```
另外建议：把 `.pytest_tmp` 清理写进 CI 的收尾步骤（或在 565b 的 basetemp 方案里改成"跑完即删
小批量"），否则它仍会随运行次数堆积。

## 5 · 收工总验收（fresh）

| 项 | 实测 |
|---|---|
| gate | `规则 61 条 · 命中 141 (block=0 warn=136 advice=5)` ✔ 不变 |
| poison | `107/107` ✔（双指标 trap 100%(6/6) · clean 100%(2/2)） |
| replay | `confirm=56 refute=0 infra_error=0` ✔ |
| fast `-n auto` | 全绿（本轮新增 7+7+6=20 例全含在内）✔ |
| slow `-n0` | 本批未重跑（**未改任何 slow 组用例与判定核心**；新增测试均落 fast 组）|
| 受控目录 | evidence/atoms 语义零改动（`prop_graph` build 前后 `git status` 零差异有测试锁）✔ |
| 重钉 | 未改 `.tool_checksums` 钉住的 5 个 CORE_TOOLS ⇒ 无需重钉 ✔ |

## 6 · 偏差表（提示词假设 X / 磁盘实测 Y）

1. **Part 2 的 M2 区间数值**：提示词写 `cp_interval(207,207) = [98.24%, 100%]`；**真值**
   `0.025**(1/207) = 0.9823372` ⇒ 显示 **98.23%**（98.24% 是另一种取整）。按 `cp_interval` 逐值为准。
2. **Part 4a 的断流对象**：提示词/上轮均提到 "`data/logs`"，实测 `data/logs/*.jsonl` 一直有写入
   （观测日志），真正停的是 **`data/metrics.jsonl`** ⇒ 修的是后者。
3. **Part 4c 的通道假设不成立（关键）**：提示词说"用 `.venv` python 的 `os.remove`/`shutil.rmtree`
   通道（500 批验证可行）"；实测**小文件可行、超大目录不可行**（835 > 500 阈值 ⇒ 批量闸拦截）。
   故 4c 只完成文件部分，目录部分留清单交人（并建议把清理写进 CI 收尾）。
4. **4c 无 commit**：删掉的全是未跟踪/已忽略文件 ⇒ 版本库里**没有**可提交的差异，
   "独立 commit" 在本环境下自然落空（不是漏做）。
5. **Part 3 命题来源**：提示词说"27 张卡 frontmatter 的 claim_structured"；实测这 27 张**全部是
   原子卡**（证据卡不带该字段）⇒ `card_kind` 恒为 atom、锚一律 `evidence`，已写进测试断言。

## 7 · 交人清单

1. `.pytest_tmp/run-*`（44 个）清理 —— 见 §4c 的命令与建议。
2. **Part 4a 的自动化缺口**：`metrics_collector.py` 至今无人自动调用（本轮只加了"断流会红"的闸）。
   建议在 CI 的 pytest job 之后加一步 `python3 tools/metrics_collector.py --no-heavy`（未改 CI：
   本环境无法验证 CI 配置，按纪律不擅自改）。
3. 565 主批的 §5.2/§5.3 里与本轮重叠的施工点已全部消化（Part 2/3/4 完成）。

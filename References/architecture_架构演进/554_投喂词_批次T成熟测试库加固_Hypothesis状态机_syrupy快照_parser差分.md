# 554 · 投喂词：批次 T —— 成熟测试库加固（Hypothesis 状态机自动攻击 + syrupy 输出快照 + parser 差分）

> 来源：552 调研"现在就用"档。目的：用工业级测试库，把过去靠人肉对抗（545/546 手工构造 task_queue 三洞、547 手工构造 parser 分歧）才能发现的问题，变成**自动、可 shrink、持续回归**的性质测试。
> 范围纪律：本批**纯测试/分析侧**，不改任何正式判定逻辑（除非测试抓到真 bug，那时单独 commit 修 bug 并说明）；依赖只进 `[dev]`，不进核心。
> 前置：**553（V-iso B3/B5 修复）合入后再做 T3**；T0/T1/T2 与 553 文件不重叠，可在 553 验收后立即接。
> 解释器：`.venv\Scripts\python.exe`。

## 〇、开工基线
先跑并记录：`gate --check` / `poison_drill` / `replay --check`（应 confirm=56）/ `pytest -m fast -q` / `pytest -m slow -q`，以及 `git status`（应只剩 553 预期改动）。本批收工这些数字除"测试数增加"外不得回归。

---

## T0 · 依赖落地（dev extras，不进核心）
1. 编辑 `pyproject.toml` 的 `[project.optional-dependencies].dev`，加入 `"hypothesis>=6.100"`、`"syrupy>=4.7"`（纯 Python wheel、无编译、无系统库）。
2. `.venv\Scripts\python.exe -m pip install hypothesis syrupy`，并同步 `requirements.lock.txt`（若该锁文件由工具生成，按仓库既有方式更新；手改则记录）。
3. **明确不装** scipy/duckdb/pydantic/mutmut（分属批次 J/分析侧，本批不碰）。
4. 验收：`python -c "import hypothesis, syrupy; print(hypothesis.__version__, syrupy.__version__)"` 出版本号；核心安装（不带 dev）仍能跑 gate（依赖隔离不破坏）。

## T1 · Hypothesis stateful 自动攻击 task_queue（本批最高价值）
545/546 已手工证明 task_queue 状态机有攻击面（A5 yield 无限续命、A3 未来心跳占坑、A7 verify 自证裸 done，均已修但缺**自动化回归**）。用 `hypothesis.stateful.RuleBasedStateMachine` 把它变成持续枚举。

**前置侦察（先读码，别猜）**：读 `tools/task_queue.py`：
- 列全 argparse 子命令（enqueue/claim/checkpoint/heartbeat/yield/complete/done/blocked/takeover/touch/list/next/downgrade…，以磁盘为准）；
- **确认 DB 路径如何定位**（grep `data/tasks` / DB 连接函数）：stateful 必须把库重定向到 `tmp_path`，绝不能打真实 `data/tasks/`。若当前 DB 路径不可注入，做**最小可测性改造**：给连接函数加一个可选 `db_path` 参数 / 读一个环境变量（默认值与现状逐字一致），单独 commit，注明"仅为测试可重定向，默认行为不变"。

**机器模型**：
- 每个用例独立临时库（`tmp_path_factory` / setup 里 init）；模拟 2-4 个 worker 身份（不同 worker id）。
- `@rule` 操作（参数用 hypothesis strategy，预算/深度/attempts 用 bounded `integers`，worker 用 `sampled_from`）：
  enqueue（含 deps、budget、verify_cmd/verify_source）、claim（指定 worker）、heartbeat（含**未来时间戳**变体）、checkpoint、yield（切 1..MAX_CHILDREN 个子任务、嵌套 yield 冲深度）、complete（rc=0/非0、custom verify、有/无 --second-party）、touch 冲突路径（含大小写/`./`/反斜杠异体）、takeover（--force/不带）、downgrade、陈旧等待（用假时钟或直接改 heartbeat_at）。
- `@invariant()` 每步后查库断言（这些是系统已声明的铁律，stateful 负责找违反序列）：
  1. **无双领**：任一时刻同一 task 不会被两个不同 worker 同时持有有效 claim；
  2. **深度上界**：子任务 depth ≤ MAX_YIELD_DEPTH，除非有 force 留痕事件；
  3. **预算账**：任一子树累计发放预算 ≤ 根任务 budget（overdraw 必须有事件留痕，不静默）；
  4. **重试封顶**：attempts > MAX_ATTEMPTS 的任务必为 blocked，不会再被 claim；
  5. **verify 不自证**：verify_source=custom 且 rc=0 且无 --second-party ⇒ 不得裸 done（须 needs_review）；
  6. **未来心跳无效**：heartbeat_at > now+容差 不延长租约（被 clamp/不采信，其他 worker 可接管）；
  7. **touch 锁归一**：同一物理文件的大小写/`./`/正反斜杠异体必须撞同一把锁（回归 538/539 A1）；
  8. **deps 门**：依赖未 done 的任务不会被 next/claim 放行。
- **必须显式回归 545/546 三洞**：除随机枚举外，各写一个确定性场景（或用 `@precondition` 引导）断言 A3/A5/A7 的修复序列仍然成立（未来心跳→可接管；第 4 级 yield→reject；custom verify 无 second-party→needs_review）。
- 配置：stateful 较慢，`@settings(max_examples=...)` 取一个 CI 可承受值（先 100-200，报实测耗时）；**不碰 replay 锁/asm 工件**（只用临时 SQLite）⇒ 标 `fast`，可被 `pytest -m "not slow" -n auto` 并行（每用例独立 tmp 库，无共享状态）。
- shrink 是核心价值：任何 invariant 失败，Hypothesis 会 shrink 出最短操作序列；把最终发现（若有）按"真 bug / 测试期望写错"分类，真 bug 单独 commit 修，不许改 invariant 去迁就 bug。

## T2 · syrupy 快照锁"结构化输出漂移"
历史上规则数/warn 数/卡数多次文档与磁盘失真、warn 32→54→59→136 缺显形。用 syrupy（零依赖 pytest 快照）锁关键工具的**结构化输出**。
- 新增 `tests/test_output_snapshots.py`，对以下命令的可解析结果（建议直接 import 其 report/run 函数取 dict，而非比对 stdout 字符串）做 `assert data == snapshot`：
  - gate 汇总：规则总数、block/warn/advice 计数（不锁具体 Finding 文本全文，避免噪声）；
  - poison：通过数、RULE-COVERAGE 分子分母、攻击面覆盖；
  - kg stats：节点/边/概念/命题边/连通分量计数；
  - mutation 汇总：变体总数、严格拦截率/含 warn 处置率的**计算结构**（数值可锁当前基线，但标注口径）。
- **动态字段必须排除**：timestamp、绝对路径、耗时秒数、平台分隔符——用 syrupy 的 matcher/自定义 comparer 忽略或归一化，否则快照必然抖动。
- **首次快照纪律（approval testing，与 golden accept 权唯人同构）**：首次生成的 `tests/__snapshots__/` 必须在 commit message / worklog 里显式列出"这些基线值我已人审"；**禁止在同一个改动里既改逻辑又 `--snapshot-update`**（那会把回归一起洗白）。逻辑变更导致快照变化时，单独一个 commit 人审后 update 并说明原因。
- 不替代 golden_lock：golden_lock 管 warn 四桶分类签署（领域语义），syrupy 管其余工具的"结构/计数不被悄悄改动"，互补。

## T3 · parser 差分（**553 合入后做**）
落地 551 的 parser differential，正是 547 B5（flow 式 nc 逃逸硬化层）的根治性回归。
- 用 Hypothesis 生成多态/畸形 frontmatter：重复键、缩进提升、tab/空格混用、全角字符、block↔flow、引号变体、注释位置、`negative_controls` 的 flow 与 block 两形态。
- 对每个样本，分别过 ① 自定义 `parse_frontmatter`（replay 侧）② PyYAML `safe_load` ③ gate 硬化 `_fm_hardening` 信号集合，断言三者对"门禁关心的键"（id/verdict/status/artifact_sha256/negative_controls 等）**要么判决一致，要么分歧被硬化层显式 block**——不允许出现"一个收下、另一个也收下但语义不同"或"硬化层沉默放行"的灰色态。
- 553 修完 B5 后，flow 式 nc 必须落在"硬化层 block"分支，用一个确定性用例钉死（回归 547 B5）。
- 标 fast（纯字符串解析，不编译）。

---

## 验收（收工机器判据）
1. `pytest -m "not slow" -n auto` 与 `pytest -m slow -n0` 全绿；新增 stateful/快照/差分测试计入 fast，报新增测试点数与 stateful 实测耗时。
2. `gate --check` / `poison_drill` / `replay --check`（confirm=56）与开工基线一致，**block/warn 数字不因本批变化**（本批不改判定逻辑；若变了说明误改正式代码，回退）。
3. 核心环境（不装 dev）仍可跑 gate：依赖隔离成立。
4. stateful 若抓出真 bug：单独 commit 修复 + 该序列进确定性回归；若 max_examples 内零违例，如实报"未发现新违例，三洞回归锁已就位"，**不硬凑 bug**。
5. syrupy 首次快照基线值在 worklog 列出并声明已人审。
6. `git status` 受控目录改动仅限：pyproject/lock、tests/ 新增、（若有）task_queue 的 db_path 可测性小改；零污染。

## 硬纪律
- 一任务一 commit：T0 依赖 / T1a（若有 db_path 可测性改造）/ T1b（stateful）/ T2（快照）/ T3（差分，553 后）分开。
- 不 push、不 --no-verify、不 golden accept、不 snapshot-update 洗白逻辑变更、不动人签字段。
- 不碰 gate_engine/poison_drill/atom_evidence_replay/viso_diff 的判定逻辑（T3 只读它们；553 正在改其中两个，避免冲突）。
- 改 task_queue（仅 db_path 注入这类可测性小改）后跑其全量 pytest + ruff 0.6.9；不引慢测试进 fast 组。

## 紧随其后（不在本批，单列批次 R，先记录）
- **impact_analysis 补传递闭包（纯 Python，不是 CTE）**：读码确认现版 upstream/downstream 只有一跳、数据源是 atoms frontmatter dict（非 SQLite）。正确做法是加 `upstream_transitive/downstream_transitive`（DFS + 环检测 + 深度/路径输出），27 节点纯 Python 毫秒级，**不要**硬塞 SQLite recursive CTE；用 T2 的快照钉"现有一跳结果 ⊆ 新闭包结果"。
- **knowledge_graph.py 的多跳遍历**才适合 recursive CTE（它本就是 data/knowledge_graph.db，SQLite 内置、零新依赖）：仅当那里存在手搓多跳图算法时再改，改前先 grep 确认是否真有。

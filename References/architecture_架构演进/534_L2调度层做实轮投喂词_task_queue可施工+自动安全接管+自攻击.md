# 534 · L2 调度层做实轮：会话断点续跑 + task_queue + 自动安全接管（投喂强模型 trae · 第四轮 · 极致版）

> **你的身份**：L2 调度层的**设计师 + 第一个攻击者**。前三轮：现状批判（529）、下一代蓝图（532）、V-iso 做实（533，规格+沙箱实测+六攻击自证）。这一轮把图上最大凹陷 **L2 调度层（当前 12%）** 从空壳打成苦力可照做的精确规格，并沙箱实测。
>
> **先纠一个定位（最重要，别理解偏）**：用户的真实痛点不是"缺一个任务队列"，而是——**一个 Agent 会话跑到约 500 次工具调用就到顶，必须人手动开新会话，而新会话没有旧会话上下文，接不上**。所以本轮的核心交付物不是 SQLite 队列本身（那是手段），而是 **"会话级断点续跑"：会话随时死，下一个会话零上下文、一条命令就能从最近检查点接着干，且不重复劳动、不踩已踩过的坑**。队列只是承载它的状态机。
>
> **"自动接管"的现实形态（守住 532 纪律，别越界）**：当前阶段**不是系统自己拉起新会话/新 worker 进程**（那是 G-supervisor，默认 OFF、要 8 周数据门）。现实形态是：会话到顶前**自动留下完整结构化交接物** → 人只做"开一个新会话"这一个动作 → 新会话跑一条 `next` 命令，读交接物零上下文接上。**人从"手动梳理进度+复述上下文"降级为"只点一下开新会话"**，这就是本轮要达成的"自动"。越界去设计守护进程/自拉起 = 违反纪律，直接打回。
>
> **仓库**：`C:\CodeLearnling\note\note\C++\CPP-Bible`，Windows；门禁用 `.venv\Scripts\python.exe`（有 PyYAML 6.0.3；别用 workbuddy python）。
>
> **【关键现状锚点——别重造已落地的东西】** task_queue 的**基础骨架已由苦力落地**（commit `d976170`，`tools/task_queue.py` 433 行，8 个 CLI 子命令已实现并通过 8 个 pytest：`init/enqueue/claim/next/heartbeat/done/fail/blocked/list`，且已带 deps 门 `_deps_done`、stale 接管 `_sweep_stale`、双连接争抢只中一个 `_pick`）。**所以你不是从零设计队列**——先 Read `tools/task_queue.py` 和 `tests/test_task_queue.py`，搞清已有表结构与 `_pick` 排序逻辑；你的增量工作是它**还没做**的四件事：①handoff 结构化交接物+断点续跑；②`yield` 到顶让出/拆子任务；③touch_set 文件级写冲突锁；④complete 必须先过验证门禁（现在的 `done` 是 worker 自报，没绑 verify）。已存在的 `next` 命令不要重写，只在其 `_pick` 排序里加"touch_set 不冲突"过滤。

> **纪律**：只读 + 产出在 `_arch_v3/`，不改正式文件、不 commit/push/accept；沙箱探针放 `_arch_v3/probe_queue/`。
> **别重复劳动**：529 已给过 task_queue 的表结构/6 子命令/6 pytest 草案——**先在 `_adv_critique/529_架构升级提示词.md` 找到那份，在它基础上深化，不许从零重写一遍同样的东西**；你的增量是断点续跑、写冲突、验证闭环。
> **已知死路**：replay 刻意串行（共享 build/ 瞬时态，--jobs 加速 <2× 不默认开）；pytest-xdist `-n auto` 不稳定；taskset 测不出核数差异；heartbeat 只按 mtime 判 stale 会被僵尸进程骗（529 B.6 僵尸锁 DoS）。

---

## 第 0 步 · 读穿真实现状（别凭蓝图想象，逐个给行号）
0. **先读 `tools/task_queue.py`（d976170）与 `tests/test_task_queue.py`**：现有 tasks 表有哪些列？`_pick` 的排序与过滤逻辑、`_stale` 阈值、`attempts` 处理。明确列出"已有/缺失"两张清单——缺失列（touch_set/budget_used/handoff_path/verify_cmd/parent_task/produced_by_model）与缺失命令（yield）就是你本轮要补的，别重复造已有的。
1. `tools/task_state.py`：现在记了哪些字段？`>450 自动 needs_continue` 是怎么实现的？它为什么只是"手工笔记本"——离"结构化交接物"差哪几个字段？
2. `tools/impact_analysis.py`：上游依赖遍历产出什么？能不能直接当任务 deps 和"改了这个文件会影响哪些原子"？
3. `tools/atom_evidence_replay.py` 增量 manifest（card_fingerprint / select_incremental）：任务 claim 后怎么知道该跑全量还是增量？
4. 翻 3-5 份真实 `_worklog_*.md`（如 _worklog_470/479/498/528）：**这些就是现在"人肉交接物"的真实形态**——它们散、长、靠人读。提炼：一个新会话要接上，到底需要哪几类信息？哪些是散文、哪些能结构化？
5. 找历史"并行会话写冲突"事故（55b53ae 带删并行索引、527 并发 golden/replay 瞬时红）：冲突的物理形态是什么？

---

## 任务 1 · 在已落地队列上补列 + 补 yield（增量，不重写）
1. **补表列**：在现有 tasks 表上新增——`touch_set`（任务将改的文件集合，JSON）、`budget_calls/budget_used_calls`（工具调用预算/已用）、`handoff_path`、`verify_cmd`（完成前必跑的验证）、`parent_task`（拆分出的子任务指回父任务）、`produced_by_model`。给出 ALTER 迁移（存量行这些列可为空，零破坏）与回退。
2. **补 `yield --task <id>`（新会话接力的关键命令）**：会话接近预算（如已用 400/500）时调用，原子地：写最终 handoff、把任务退回 pending（保留 checkpoint，不是 fail）、按剩余步骤自动 enqueue 子任务（parent 指回）。给出"怎么把一个没做完的任务干净地切成可续子任务"的算法。其余 8 个已有子命令只在必要处小改（如 `done`→`complete` 接验证，见任务 3），不要推翻重写。
3. **现有 `next` 的增强**：不重写，只在 `_pick` 选任务时加一条过滤——该任务 touch_set 与所有 in-progress 任务相交则跳过；其余排序（deps 全满足→优先级→最早入队）保持现有逻辑。**并补租约语义**：已被 claim 且心跳在租约内的任务，`next` 不能抢走；要接管必须人显式 `takeover <task>`，或等心跳过期走 stale 回收（这是上一沙箱会话现场实测发现、必须继承的设计点——否则新会话一进来就顶掉别人正在干的活）。
4. **状态机画全**：pending→claimed→in_progress→（yield 回 pending / complete 待验证 / fail→retry / blocked）的迁移，标出哪些是已有、哪些新增；非法迁移怎么拒。

## 任务 2 · 会话断点续跑交接物 handoff（本轮真正核心，做到苦力能照写）
设计一个**结构化、机器可校验、新会话读完即可继续**的 handoff（不是散文 worklog）：
1. **字段写死**，至少含：`goal`（任务目标，一句话可验证）；`steps_done` / `steps_remaining`（可枚举步骤，不是叙述）；`verified_facts`（已验证结论，每条带证据锚点=文件:行号 或 命令输出，新会话**不必重验**）；`tried_and_failed`（踩过的坑+为什么此路不通，防止新会话重踩）；`next_action`（下一步具体到命令）；`touched_files`；`budget_used`；`open_questions`（需人裁决的，没有就空）。
2. **checkpoint 频率**：不是任务结束才写，是每完成一个关键步骤原子更新一次——保证会话**在任意时刻被杀**都能从最近 checkpoint 接，最多丢一步。给出"什么算一个该落盘的关键步骤"的判据。
3. **机器校验 handoff 质量**：handoff 缺 next_action / verified_facts 无锚点 / steps_remaining 为空时，`yield` 拒绝让出（fail-closed，防止留下"看着有交接实则接不上"的废 checkpoint）。设计成 gate 可复用的检查。
4. **端到端续跑剧本**：精确写出"会话 A 在第 3 步到顶 → yield → 人开新会话 B → B 跑 next → 读到什么、怎么判断从第 4 步继续、怎么确认前 3 步不用重做"的完整时序。这是验收主场景。

## 任务 3 · 写冲突隔离 + 完成验证闭环（两个历史真坑）
1. **文件级 touch_set 锁**：任务 enqueue 时声明要改的文件；`next/claim` 时若与任一 in-progress 任务的 touch_set 相交则**拒绝派发并返回冲突任务 id**（不是报错了事，要告诉它等谁）。对照历史事故（55b53ae）说明这能挡住什么；touch_set 声明不全（实际改了没声明的文件）怎么事后发现（对比 git diff 与声明集）。
2. **完成验证闭环**：`done` 不允许 worker 自证——`complete <id>` 必须先跑该任务 `verify_cmd`（增量 replay / gate / poison 子集，按任务 type 绑定），全过才置 done 并记录验证输出哈希；不过则回 in_progress、记 fail 原因、attempts+1。给出三类任务（原子生产/工具改动/文档）各自该绑什么 verify_cmd。

## 任务 4 · 沙箱实测（拿真实数字，必须含"被杀续跑"端到端）
在 `_arch_v3/probe_queue/`：
1. 建临时 SQLite 队列，enqueue 5-10 个任务（带 deps 链、带 touch_set 冲突对、带故意失败、带慢任务）。
2. 实测报数：①两进程同时 next 是否只一个拿到；②touch_set 相交的两任务是否正确挡住第二个；③**主场景：脚本模拟"worker 做到第 3 步被 kill -9"，再起一个新 worker 跑 next，验证它是否从第 4 步零上下文接上、前 3 步不重跑**（这是本轮最重要的实测，必须真做，不许纸面推演）；④yield 把残任务切成子任务；⑤complete 时 verify 失败是否正确回退；⑥全链路毫秒级开销。
3. 诚实报告 SQLite 在 Windows 多进程下的坑（锁等待/BEGIN IMMEDIATE 行为/编码/ WAL 要不要开）。

## 任务 5 · 你自己攻击这个调度设计
1. **冒名**：worker A 冒充 B done/yield B 的任务（E12 教训），claimed_by 怎么绑才够。
2. **deps 环**：A 等 B、B 等 A，怎么在 enqueue 时就检出而非运行时挂死。
3. **假活/僵尸**：心跳在但不推进——进度指纹（两次 heartbeat 间 touched_files 与 checkpoint 都没变=假活）怎么判。
4. **handoff 投毒**：上一个会话在 verified_facts 里写一条假结论（没锚点或锚点造假），新会话盲信就被带沟里——handoff 的"已验证"凭什么被信任？哪些必须新会话独立复核、哪些可继承？（这条最关键，关系到断点续跑会不会把错误也"续"下去）
5. **预算误判**：任务估 200 次实际要 600 次，反复 yield 拆出一堆碎片子任务，调度被碎片淹没——粒度判据怎么定。

---

## 任务 6 · 架构质变调研（顺便，主线仍是 L2；批判吸收不膜拜）
每条挂 1-2 个真实可打开的 2025-2026 来源，回答"解决本系统哪个真问题/现在做还是等/落到哪个字段或开关"，并指出"业界流行但对本系统是错的"：
1. **长流程工作流的断点恢复（重点，直接支撑任务 2）**：Temporal 的 event sourcing / workflow replay、Airflow 的 task instance 与 retry、LangGraph 的 checkpoint/persistence——它们怎么让一个长流程在进程崩溃后从确定状态续跑？哪些思想（事件溯源、确定性重放）能迁到 handoff/checkpoint，哪些是重型基础设施对单人仓库是负担？
2. **预注册/可重复性危机（preregistration）**：怎么防"事后编故事"，给 claim 生产补"动笔前冻结要证什么/怎么算证伪"的机器留痕；哪些是过度仪式化。
3. **模型换代时知识长存**：每颗原子记 `produced_by_model`，模型换代后哪些 claim 必须重验、重验任务怎么作为队列一种 type 自动入队（和任务 1 的 type 体系打通）。
4. **可复现构建/溯源（reproducible builds）**：.asm sha 锚证据但工具链会漂移，怎么存"重建工件的最小环境快照"（结合 env_check/toolchain），什么粒度不沦为存档负担。

## 任务 7 · 产出 534 施工规格（`_arch_v3/534_L2调度层施工规格.md`）
- 8 子命令 + 状态机 + 表结构（含本轮新增列）的苦力级伪代码；
- handoff 字段模板 + checkpoint 规则 + 质量校验 + 端到端续跑时序；
- touch_set 锁 + complete 验证闭环；
- 任务 4 全部实测数字（尤其"被杀续跑"主场景）；
- 任务 5 自攻与回应（handoff 投毒必须给出"哪些可继承/哪些必复核"的明确判据）；
- 任务 6 调研结论，末尾"下一轮质变候选"标【现在可落/攒数据/等模型】；
- 苦力执行批次：一任务一 commit + pytest + 存量零误伤，每条挂"为什么现在做"+机器验收判据；
- 三档清单：现在做（人工派发队列+断点续跑骨架）/ 攒数据（接管率、卡死率、预算准确率字段先留）/ 等模型（Supervisor 自拉起、模型路由）。

## 验收（建设者逐条核，达不到打回）
- **任务 4 的"kill 到第 3 步→新 worker 从第 4 步接上"必须有真实脚本和输出，纸面推演不算**；
- 任务 1 每条 SQL、任务 2 每个 handoff 字段、任务 3 每条锁规则可执行；任务 5 handoff 投毒必须给出可继承/必复核的机器判据；
- 数字全部实跑，区分【实测/推断/待实验】；
- 严守"人只开新会话、系统不自起 worker"的边界，不偷跑 G-supervisor；
- 不重写 529 已有草案、存量零误伤；`git status` 证明正式目录零改动。

## 开头一句话（实做后回答，不要理论）
你真的把一个 worker 在任务中途 kill 掉、再让一个"零上下文"新 worker 跑 next 接上之后——**断点续跑这套机制最可能在哪一步让新会话"看似接上了、其实接错了"**？

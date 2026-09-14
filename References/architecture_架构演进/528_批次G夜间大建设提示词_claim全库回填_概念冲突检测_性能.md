# 528 批次G夜间大建设提示词 · claim全库回填 + 概念冲突检测 + 性能

> 投喂对象：苦力（便宜模型，夜间无人值守，长任务）
> 路径：`C:\CodeLearnling\note\note\C++\CPP-Bible`
> 设计原则：**幂等可中断**——每任务独立commit，即使到请求上限，已完成的任务都已落盘不丢。
> 按任务顺序做，做不完就停在当前任务，worklog写清进度，下一个会话从断点续。
> 全程不push（push权在监工）；不golden accept；一任务一commit。

---

## 〇、开工实测（先跑，记录基线数字）

```
python tools/gate_engine.py --check    # 记录 规则数/BLOCK/WARN/ADVICE
python tools/poison_drill.py           # 记录 passed/total、RULE-COVERAGE
python tools/knowledge_graph.py stats  # 记录 节点/边/概念/命题边
pytest -m fast -q                      # 记录点数
git log --oneline -1                   # 记录开工HEAD
```
把这些写进 `_worklog_528.md` 开头。**所有后续数字都和这个基线比。**

---

## 任务1：20张存量卡全量回填 claim_structured（最大机械活，优先做）

### 精确清单（staging 27 − 已完成7 = 20，逐张做）
```
ATOM-CONC-LOCK-001   ATOM-CONC-RACE-001   ATOM-HIST-AUTOPTR-001
ATOM-LANG-INLINE-001 ATOM-MEM-ALIGN-001   ATOM-MEM-LEAK-001
ATOM-MEM-MOVE-002    ATOM-MEM-NEW-001     ATOM-MEM-PERF-001
ATOM-MEM-PERF-003    ATOM-MEM-RAII-001    ATOM-MEM-RVREF-001
ATOM-MEM-SHARED-001  ATOM-MEM-SHARED-002  ATOM-MEM-UNIQUE-001
ATOM-MEM-UNIQUE-002  ATOM-MEM-VALUE-001   ATOM-MEM-VALUE-002
ATOM-MEM-WEAK-001    ATOM-UB-GRAY-001
```

### 每张卡的标准动作（照 CONC-FENCE-001 粒度）
1. Read 卡 + 它 evidence: 指向的证据卡
2. 把 claim 拆成 1-N 条原子命题，每条：
   - `subject/predicate/object`：概念名，**先查 tools/concept_aliases.txt 用规范名**（"栅栏"→"内存屏障(fence)"）
   - `claim_type`：
     - **observation**：证据卡有 artifact 断言/run_match 支撑（机器可验）
     - **inference**：标准推断/法理，必须填 external_basis（ISO/cppreference/commit）
   - `statement`：人类可读一句话
   - `evidence`：支撑证据卡ID
   - `extracted_by: writer`
3. **拿不准 claim_type 的，一律标 inference + needs_human_review: true，绝不擅自定 observation**（铁律）
4. 每回填 5 张，跑一次 `gate_engine --check`，确认 BLOCK=0、WARN 在下降（回填一张，STAGING warn 少一条）
5. **每 5 张一个 commit**（commit message 写明回填了哪5张），不要20张攒一个大commit

### 验收
- 20张全部带 claim_structured
- `gate_engine --check` 的 WARN 从基线下降约20（STAGING warn清零）
- `knowledge_graph.py build && stats`：概念数/命题边数显著增长（记录前后值）
- replay confirm=56 不变（回填只动frontmatter，不动工件）

### 中断点
做到第N张被打断也没关系：worklog 写"已完成X张，剩Y张，清单如下"，下次从未做的继续。

---

## 任务2：概念冲突检测（L3建设，纯图查询零LLM）

**背景**：claim命题已进 concept_edges，但"两个原子的命题是否矛盾"只有数据没有判据。本任务写判据。

### 做法
1. Read `tools/knowledge_graph.py` 的 SCHEMA 和 build()，看 concept_edges 结构。
2. 新增子命令 `python tools/knowledge_graph.py conflicts`：
   - 纯SQL：找满足以下条件的命题对：
     - 两条命题的 subject 归一后相同（走 concept_aliases）
     - predicate/object 语义相反（先做最保守的：一条 object 含"阻止/不/禁止"而另一条含"允许/会/能"，或两条命题间存在 CONTRADICTS 边）
   - 输出候选矛盾对（atom id + 两条statement），**只报候选不判对错**（语义判断归人/红队，L1只做结构检测）
3. 这是**分析工具不是gate block**——输出报告即可，不阻断门禁（避免误报卡死全库）。
4. 跑一次，把检测到的候选矛盾写进worklog（哪怕0条也要如实报）。

### 验收
- `conflicts` 子命令存在且能跑
- 至少3个pytest：构造一对真矛盾能检出、一对正常命题不误报、空库不崩
- 零LLM调用（纯SQL+字符串规则）

---

## 任务3：命题级签署精确化（规则3从卡级到命题级）

**现状**：INFERENCE-NOT-MACHINE-VERIFIED 只判"这张卡有没有人签"，不判"具体哪条inference命题被签了"。

### 做法
1. Read gate_engine.py 里 INFERENCE-NOT-MACHINE-VERIFIED 的实现。
2. claim_structured 的每条 inference 命题支持可选 `signed_by: human:<名>` 字段。
3. 规则精确化：卡status=verified时，**每条** inference 命题要么有 signed_by（走principal_ok单点校验），要么 external_basis 在独立来源表登记；缺一条就报该命题id（而不是笼统报卡）。
4. 存量兼容：命题没写 signed_by 但卡级 status_history 有人签的，视为全卡命题已签（不破坏现状），warn 提示"建议精确到命题"。
5. 配毒样例：一条inference命题缺签→block；卡级有签命题级没签→warn；命题级有签→放行。pytest各一例。

### 验收
- 新毒样例全过，poison 总数增加，RULE-COVERAGE 不出现 uncovered
- 存量27卡（含任务1回填后）零新增BLOCK

---

## 任务4：golden_lock / replay 并行化（性能，508定位的真瓶颈）

**背景**：508实测 pytest 已两阶段并行，但总时长卡在 test_golden_lock_json 单进程125s——它逐卡 replay 真编译。要压时长得并行化 replay 自身。

### 先做只读分析（别急着改）
1. Read `tools/atom_evidence_replay.py`，找逐卡循环和共享状态：
   - replay 锁（.replay_lock，E09/N1僵尸锁问题）
   - Examples/atoms/*.asm 的"删→重生成→比sha→还原"瞬时态（这是不能多进程共享工作树的根因）
2. 写 `_worklog_528.md` 一节：并行化方案对比——
   - 方案A：每卡复制到独立临时worktree编译（隔离asm瞬时态），主进程汇总
   - 方案B：进程池+每卡独立build目录
   - 评估各自对"重编译不变量(P0-A)"、sha比对、锁的影响
3. **只实现最安全的版本**：`--jobs N` 参数，每卡在独立临时目录编译，产物sha回主进程比对。默认 N=1（不改变现有行为），显式 --jobs 4 才并行。
4. 僵尸锁防护（N1教训）：锁文件写pid，取锁时 os.kill(pid,0) 判存活，死锁可接管；stale从3600s缩到300s。

### 验收
- N=1 行为和现在逐字一致（confirm=56）
- --jobs 4 时结果一致且耗时下降（记录单卡串行总时长 vs 并行总时长）
- pytest 覆盖：死锁pid接管、并行结果汇总顺序无关
- **如果评估后发现并行会破坏重编译不变量，就只交分析+僵尸锁修复，不硬上并行**（诚实，不制造不稳定）

---

## 任务5：小问题守护（收尾，快）

1. **全量pytest守护**：527教训"只跑单个test文件漏了NameError"。在 prepush_check.py 或 cppbible quality 里确认跑的是全量 pytest（不是单文件）；写一条注释说明为何不能只跑单文件。
2. **PyYAML依赖显式化**：527根因是workbuddy python缺pyyaml静默return []。确认修复已落地（缺yaml留warn不静默），并在 README 或 docs 写清"运行门禁需要 PyYAML"，列出两个解释器路径各自的依赖状态。
3. **frontmatter硬化测试**：确认 statement 里含 `SUMMARY: AddressSanitizer:` 这类ASCII冒号不会误触发 EV-FM-YAML-HARDENING（527踩过，加一条回归测试钉死）。

---

## 全局铁律

1. 不push、不golden accept
2. 一任务一commit（任务1每5张一commit）；改规则必配毒样例+pytest
3. **改核心工具后必须跑全量 pytest -m fast，不是只跑单个test文件**（527 NameError教训）
4. 存量零误伤：每任务后 gate BLOCK=0，WARN变化要能解释
5. 拿不准claim_type标inference+needs_human_review，不假装机验
6. 概念名先查 concept_aliases.txt 用规范名
7. 有其他agent并发时（tasklist查python进程多、replay_busy），等其退出再跑全量
8. 不编造数字，跑多少报多少；做不到的任务写清原因，不硬凑

---

## 中断与续跑（夜间无人值守关键）

- 每完成一个任务，在 `_worklog_528.md` 顶部更新"进度看板"：
  ```
  ## 进度
  - [x] 任务1：已回填 X/20（清单...）
  - [ ] 任务2：未开始/进行中（做到哪）
  ...
  ```
- 到请求上限就正常停。新会话第一动作：Read `_worklog_528.md` 进度看板，从第一个未打勾的任务继续。
- 已commit的任务不重做（git log 核对）。

---

## 收工验收（做到哪算哪，但每任务都要fresh run）

```
python tools/gate_engine.py --check     # BLOCK=0；WARN应较基线下降（任务1回填）
python tools/poison_drill.py            # 全过，RULE-COVERAGE无uncovered
python tools/atom_evidence_replay.py --check  # confirm=56 不变
pytest -m fast -q                       # 全绿，点数记录
python tools/knowledge_graph.py build
python tools/knowledge_graph.py stats   # 概念/命题边增长
python tools/knowledge_graph.py conflicts # 任务2候选矛盾
```

worklog 最终写：每个任务状态、前后数字对比、哪些没做完及原因、ahead多少commit（不push）。

---

## 明确不做

- 不push、不golden accept
- 不新建L2调度层/多模型路由（更后批次）
- 不改Book/教学原文
- 任务4并行化若会破坏重编译不变量就只交分析，不硬上
- 不新造大工具目录，都在现有文件扩展
- 不碰 .git/hooks 之外的git历史操作

---

## 为什么这一批

任务1把526点火的claim结构化从"7张样板"推到"全库27张"——这是L3智能层有足够数据的前提；任务2让图谱第一次能问"有没有自相矛盾"（从文件图到概念图的关键一跃）；任务3把放权闸精确到每条命题；任务4攻508定位的真性能瓶颈；任务5堵527暴露的两个工程疏漏。做完这轮，L3从12%显著上抬，且全部幂等可续。

---

*文档编号 528。批次G夜间大建设，直接投喂苦力。*

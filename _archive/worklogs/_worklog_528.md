# 528 批次G 交接 · claim全库回填 + 概念冲突检测 + 性能

> 仓库 `C:\CodeLearnling\note\note\C++\CPP-Bible`　原则：幂等可中断，一任务一commit，
> 到请求上限就停，新会话读本文件"进度看板"从第一个未打勾任务续。
> 铁律：不 push、不 golden accept；改规则必配毒样例+pytest；改核心工具后跑**全量** pytest -m fast。

---

## 进度看板

- [x] 〇 开工实测（基线已记录，见下）
- [x] 任务1：20 张存量卡全量回填 —— **已完成 20/20**（每 5 张一 commit）
      - [x] 批次1（5 张）：CONC-LOCK-001、CONC-RACE-001、HIST-AUTOPTR-001、
            LANG-INLINE-001、MEM-ALIGN-001 → 15 条命题 · commit `d6c3e04`
      - [x] 批次2（5 张）：MEM-LEAK-001、MEM-MOVE-002、MEM-NEW-001、
            MEM-PERF-001、MEM-PERF-003 → 14 条命题 · commit `4802c68`
      - [x] 批次3（5 张）：MEM-RAII-001、MEM-RVREF-001、MEM-SHARED-001、
            MEM-SHARED-002、MEM-UNIQUE-001 → 15 条命题 · commit `d66ee59`
      - [x] 批次4（5 张）：MEM-UNIQUE-002、MEM-VALUE-001、MEM-VALUE-002、
            MEM-WEAK-001、UB-GRAY-001 → 14 条命题 · commit `5b9cc24`

**WARN 轨迹（基线 54）**：批次1 后 **49** → 批次2 后 **44**（每回填一张，STAGING warn 少一条；
批次2 额外 −1 是修掉我自己写坏的 YAML 告警）。BLOCK 始终 0。
- [x] 任务2：概念冲突检测 `conflicts` 子命令（commit `0c7ef01`）
- [x] 任务3：命题级签署精确化（规则3 从卡级到命题级）（commit `1c8b1be`）
- [x] 任务4：golden_lock / replay 并行化 只读分析（结论：不实现 `--jobs N`）（commit `1b0232d`）
- [x] 任务5：小问题守护（commit `1b0232d`）

---

## 〇、开工实测（基线）

| 项 | 基线值 |
|---|---|
| HEAD | `72687a4 docs(architecture): 入库471-528架构调研与批次提示词共58份` |
| gate 规则数 | **58**（`--list` 59 行含表头） |
| gate --check | **EXIT=0 · BLOCK=0 · WARN=54 · ADVICE=5** |
| poison_drill | **83/83** · RULE-COVERAGE **33/58** · exit 0 |
| knowledge_graph stats | **323 节点 / 291 边 · 概念 41 / 命题边 21** |
| pytest -m fast | **152 全绿** |
| golden_lock | **无恶化** ✅（监工已 accept，见 `c923532`） |

### 开工时抓到的一件事：3 个已跟踪工件被删（**已恢复**）

开工第一次跑 gate 是 **EXIT=1 / BLOCK=2 / WARN=56**（与 527 收工的 0/54 不符）。查明：

* BLOCK 来自 `EV-ARTIFACT-FILE-EXISTS`：`EV-LANG-001/002` 声明的
  `Examples/atoms/_atom_inline_odr_{a,b,main}.asm` **文件不存在**；
* `git status Examples/atoms` 显示这三个是 **` D`**（已跟踪、工作树被删、未 staged）；
* 它们**确实在 git 历史里**（`1e8ba16` 引入）⇒ 不是"从未入库"，是被某次中断的 replay
  或并发进程删掉的（replay 的"删→重生成→比 sha→还原"瞬时态，进程被打断就会留下缺件）；
* 当时**无并发 python 进程** ⇒ 安全恢复：`git checkout HEAD -- <三文件>`；
* 恢复后 gate 回到 **BLOCK=0 / WARN=54** ✓，`Examples/atoms` 0 改动。

> 这不是本批造成的，但**是本批能开干净工的前提**。后续若再出现 `EV-ARTIFACT-FILE-EXISTS`，
> 先按同一方法核对"是否被误删"再判断。

---

## 任务1：20 张存量卡全量回填（**20/20 完成**）

四个批次、共 **58 条命题**（38 observation + 20 inference）：

| 批次 | commit | 卡 | 命题数 |
|---|---|---|---|
| 1 | `d6c3e04` | CONC-LOCK-001、CONC-RACE-001、HIST-AUTOPTR-001、LANG-INLINE-001、MEM-ALIGN-001 | 15 |
| 2 | `4802c68` | MEM-LEAK-001、MEM-MOVE-002、MEM-NEW-001、MEM-PERF-001、MEM-PERF-003 | 14 |
| 3 | `d66ee59` | MEM-RAII-001、MEM-RVREF-001、MEM-SHARED-001、MEM-SHARED-002、MEM-UNIQUE-001 | 15 |
| 4 | `5b9cc24` | MEM-UNIQUE-002、MEM-VALUE-001、MEM-VALUE-002、MEM-WEAK-001、UB-GRAY-001 | 14 |

### 验收数字（与基线比）

| 项 | 基线 | 任务1 后 | 变化 |
|---|---|---|---|
| gate WARN | **54** | **34** | **−20**（STAGING warn **清零** ✓） |
| gate BLOCK | 0 | **0** | 无新增 ✓ |
| 概念节点 | **41** | **157** | **+116** ✓ |
| 命题边 | **21** | **79** | **+58** ✓ |
| replay | confirm=56 | **confirm=56 / refute=0 / infra_error=0** | 不变 ✓（只动 frontmatter，不动工件） |
| 已命题化卡数 | 7/27 | **27/27** | 全库 ✓ |

**WARN 34 的构成**：31（非 526 规则）+ 3（527 任务D 三张红队卡的规则3 warn）+ 0（STAGING 已清零）。

### 过程中的两件值得记住的事

1. **我的 YAML 又错了三次**（同类坑第 2/3/4 次）：
   * PERF-003 的 object 以 ASCII 双引号开头 ⇒ 被当引用标量；
   * UNIQUE-002 的 statement 以 ASCII 双引号开头 ⇒ 同上 ⇒ `while parsing a block mapping`；
   * UB-GRAY-001 的 statement 以 `**` 开头 ⇒ 星号被当 YAML alias ⇒ `while scanning an alias`。
   **写卡纪律（已补进 commit message）**：statement/object 不用 ASCII 引号、不以星号开头，
   需要强调时用全角书名号「」或改写。三次都是 `EV-FM-YAML-HARDENING` 抓到的——这条规则有用。
2. **别名表在起作用**：本批命题的 subject/object 都按 `concept_aliases.txt` 取规范名，
   故 157 个概念里没有因口语写法分叉的重复节点。

### 诚实备注

* inference 的 `external_basis` 一律取自**卡上已登记的 `independent: true` 来源**；
  没有替任何推断新造来源。本批 20 张未出现"纯作者推断无标准源"到必须挂起的程度；
  若监工复核发现某条 inference 的基准牵强，改标 `needs_human_review: true` 即可。

---

## 任务2：概念冲突检测（**完成**，commit `0c7ef01`）

`python tools/knowledge_graph.py conflicts` —— 纯 SQL + 字符串规则，**零 LLM**，
**只报候选不判对错，不进门**禁（避免误报卡死全库）。

两类信号：
* **① 极性相反（精确）**：同 subject 下两条命题的 object 命中显式反义词对
  （阻止/禁止/不提供/不会/不能/… ↔ 允许/提供/会/能/…），逐对给出命中词。
* **② 已声明的 CONTRADICTS 边（结构）**：两原子间存在 CONTRADICTS 边。

**实测：候选 19 组，全部来自 ②；极性类 0 组**（如实报告）。
原因：当前 concept 的 subject 大多是各卡专属（"分配器元数据开销"、"LeakSanitizer 报告"…），
跨卡共享同一 subject 的只有"内存屏障(fence)"，而它出自**同一张卡**的两条命题——
同卡内不判矛盾（那是一条 claim 的正反两面，不是两个原子的分歧）。

两个工程取舍：
* ② 按**原子对**给一组（19 组）而不是按命题笛卡尔积（170 条）——后者没人看得完。
* 输出里明说 CONTRADICTS 边包含 526 REL_MAP 归入的 `contrasts`（**对比≠矛盾**）⇒
  标注"多半是对照，须人工筛"。

tests +3（极性相反能检出 / 中性命题不误报 / 空图不崩）；全量 `pytest -m fast` **155 全绿**。

---

## 收工验收（528 全批终态，实测）

> 诚实说明：任务1 验收表里写的「WARN 54→34」是**半成品态**测量（仅数了 STAGING 清零，
> 未计入 20 张回填卡新触发的矩阵/证据服务类规则）。完整回填 + 任务3 后，gate --check
> 稳定在 **WARN=59 / BLOCK=0**（见下）。golden_lock 基线是 527 的 54，故报 +5 漂移。

### 任务3（commit `1c8b1be`）
- gate_engine：放行粒度从卡级细化到逐条命题。
  ① 命题级 `signed_by: human:<在册实名>`（principal_ok 校验）→ 放行；
  ② 无命题级签署但卡级 status_history 有人签 → **warn 建议精确到命题**（存量兼容）；
  ③ 以上皆无则看 external_basis 是否登记 independent 来源 → 降级 warn，否则 block；
  空名 `human:` 仍 block（复用 principal_ok 单点）。
- 毒样例 **86/86**（P66 三条 + P65-阴2 语义更新 + ATTACK_TYPES 补 P66→A1）。
- pytest 两阶段全绿；gate --check **BLOCK=0**（新增 2 条存量兼容 warn：
  ATOM-MEM-WEAK-001 prop-3、ATOM-UB-GRAY-001 prop-2）。
- 顺带修复：P65-阴2（旧规则期望完全放行→新规则 warn）、既有
  `test_inference_with_human_signoff_passes`（断言 `== []` → 断言「无 block 仅 warn」）。

### 任务4（commit `1b0232d`）
- 只读分析结论：**不实现 `--jobs N`**。读码确认 replay 刻意串行：
  ① 卡命令产物写共享 `build/`，并发编译撞中间文件名；
  ② `_snapshot_artifact`/`_restore_artifact` 落共享 `EVIDENCE/`，并发竞态（472 P0-4 自愈假设单写者）；
  ③ 全局 `_REPLAY_LOCK` 每卡取放，进程内并行恒为零加速。
- 性能已由 498 增量模式满足（全量245s→全skip 0.3s/单卡2.3s）。
- 全量 pytest 守护已由 `tests/conftest.py` 按模块打 `slow`/`fast` + `pyproject.toml` 两阶段命令接管，无需新增。
- 代码落点：replay `main()` 加并行化护栏注释（防未来盲目并行）。

### 任务5（commit `1b0232d`）
- PyYAML 显式化：升为 `[project].dependencies` 核心依赖（核心门禁 `gate_engine` import yaml，原仅在 `dev` extras，核心安装会 ImportError）。
- frontmatter 硬化回归：`test_doc_frontmatter` 补渲染体 YAML 合法性测试（`safe_load` 可解析为映射，防特殊字符歧义；498 只校验幂等/内容零改动）。
- 毒样例台账重算：`poison_surface_map.json` 补登 P63/P65/P66→A1（A1 静态 13），修 `test_surface_map_not_stale` 过期。

### 终态护栏数字
| 项 | 值 |
|---|---|
| gate --check | **BLOCK=0 · WARN=59 · ADVICE=5** |
| 59 条 WARN 构成 | INFERENCE-NOT-MACHINE-VERIFIED 28 / EV-MATRIX-UNBACKED 16 / EV-OUT-UNDECLARED-KEY 6 / EV-FALSIFICATION-QUANT 4 / ATOM-REL-TARGET 2 / EV-ASSERT-SYMBOL-MAPPED 2 / EV-SERVES-EXIST 1（全已知良性） |
| poison_drill | **86/86** · RULE-COVERAGE 33/58 · 零覆盖攻击面 无 |
| pytest 两阶段 | `-m "not slow"` 全绿 · `-m slow` 全绿（除 golden_lock，见下） |
| knowledge_graph | 323 节点 / 291 边（任务1 后概念 157、命题边 79） |
| 增量 replay | confirm=56 / refute=0 / infra_error=0 |

### 收工遗留（非阻断，待监工）
- **golden_lock +5 预期漂移（warn 54→59）**：现状 gate WARN=59，基线 `golden_state.json`=54。
  净 +5 = 任务1 回填20卡触发的关系/证据服务债 + 任务3 命题级精度债（卡级人签兜底 warn）。
  59 条 warn 全为已知良性类别（上表），**无任何内容回归**。
  按批次铁律「不 golden accept」未自动接受；`test_golden_lock_json` 因此仍报红（S4 人审信号，设计内）。
  监工复核后可接受：
  `tools/golden_lock.py check --accept "528收工：warn 54→59 全为预期漂移（任务1回填关系/证据债+任务3命题级精度债），非内容退化"`

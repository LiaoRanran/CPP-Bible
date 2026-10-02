# 673p 拆仓 verifier 报告（现状审计 + 设计 + 实现 + 验证 + 阻塞登记）

- **批次**：673p
- **日期**：2026-10-02
- **仓库**：`CPP-Bible`（主仓；`tools/` + `tests/` + `data/`）
- **任务**：把 verifier 拆成「资产池」与「选择策略」两层，为 A5（random-budget 证伪实验）建立可运行的基础设施
- **预注册**：`data/673p_a5_preregistration.json`（**先于实现单独 commit**：`7ae34cf5`）
- **产物**：`data/experiments/a5_673p.json`

---

## 0. 一句话结论

三层基础设施（资产池 / 选择策略 / 运行-评估）已建成并跑通，**FD 复现 82.9% / 62.5%**；
但 A5 的核心问题**仍然没有被干净隔离**，根因已从"接口不可见"升级为更本质的一条：

> **A5 阻塞条件 3：现有 FD 没有选择层。** FD 对每个样本跑**全池**；所谓"FD 用到的资产"
> （holdout 4 个 / corpus 5 个）是从 catch **事后反推**的记账量。
> 数值证据：在同预算的 2000 次随机抽样中，检出率的**最大值恰好等于 FD 的检出率**
> （holdout 82.93%、corpus 62.50%）——因为 FD 的预算锚就是"能抓到东西的资产集合"本身。
> ⇒ 这个对照里 FD 是 **argmax**，不可能输；把它读作"failure-driven selection 优于 random
> selection"是把**资产池存在**当成了**选择策略有效**。

---

## A. 现状审计

### A.1 任务书点名的文件：实际落盘位置与差异（如实登记）

| 任务书写法 | 实际路径 | 状态 |
|---|---|---|
| `tools/select_assets_671b.py` | `tools/select_assets_671b.py` | ✅ 存在（**主仓侧 shim**，池 = 仪器池 10 项） |
| `tools/verify_expand_672h.py` | `tools/verify_expand_672h.py` | ✅ 存在（672h 扩样独立复算） |
| `baseline_fd.json` | `data/experiments/baseline_fd.json` | ✅ 存在（**在 `data/experiments/` 下**，不在 `data/`） |
| `ablation_plan_671b.json` | `data/experiments/ablation_plan_671b.json` | ✅ 存在（同上，A5 在此登记为 `BLOCKED`） |

**额外登记（任务书未提但审计必须点出）**：

- `tools/select_assets_672g.py`（672g 的**拆仓权威实现**）**不在主仓**，在拆仓验证器
  `C:/CodeLearnling/queyi-verifier`。这正是 `b3_design_671b.json::blocked` 登记的根因：
  *"资产选择接口在拆仓验证器，主仓不可见 ⇒ BLOCKED"*。
  本批把 673p 的池与策略**落在主仓**（因为 673 系列、`ablation_plan_671b.json`、
  `baseline_fd.json`、`verify_expand_672h.py` 都在主仓），并**不依赖**拆仓仓的实现。
- 任务书说"读 `data/current_numbers.json`" —— ✅ 存在，是 672h 扩样后的权威源。
- 任务书说"读 `data/experiments/reveal_update_672h.json`" —— ✅ 存在。

### A.2 权威数字（不编造，全部来自落盘产物）

| 量 | 值 | 来源 |
|---|---|---|
| FD holdout 可测 | 34 / 41 = **82.9%**，CP95 [67.9, 92.8] | `data/current_numbers.json` |
| FD corpus 可测 | 40 / 64 = **62.5%**，CP95 [49.5, 74.3] | 同上 |
| Static holdout / corpus | 1/41 = 2.4% / 11/64 = 17.2% | 同上 |
| Random† 代理 holdout / corpus | 4/41 = 9.8% / 14/64 = 21.9% | 同上（**仪器级代理，禁止进论文**） |

### A.3 现有 FD 管线的数据流（审计图）

```
输入
  data/holdout/reveal_5_detail_672h.json          （holdout 60 条；planted=true 42 条 → 可测 41）
  data/external_corpus/reveal_detail_672h.json    （corpus 76 条 → 可测 64）
  每条 = {id, detector, verdict, layer, planted, source, ...}
        │
        ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ ① 资产池 —— **隐式存在，无独立定义**                                      │
│    池 = detector 字段的取值集合                                           │
│    {asan, ubsan, tsan, wunsequenced, compiler-warn, cross-compile,        │
│     linker, compile-time} (+ unknown)                                     │
│    ✗ 无成本 / 无能力描述 / 无适用缺陷类型 / 无"实现了没有"标记              │
│    ✗ 池的真实定义硬编码在 tools/holdout_reveal_661.py::detect 内部         │
│      （双档 -O0/-O2 + -fsanitize={address,undefined,thread} + setarch -R）  │
└──────────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ ② 资产选择 —— **不存在**                                                  │
│    FD 对**每个样本跑全池**：没有"在预算下选子集"这一步。                    │
│    tools/select_assets_671b.py::budget() 是**事后记账**：                  │
│        used = { s.detector | verdict(s) == "catch" } ∩ INSTRUMENT_POOL     │
│    它服务的是 Random 臂的"预算锚"，不是 FD 的选择。                        │
│    ✗ 这是 A5 无法隔离的**结构性根因**                                      │
└──────────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ ③ 运行时证据采集 —— 逐样本真跑（WSL g++ + sanitizer，双档 × 3 回合）        │
│    asan/ubsan/tsan → WSL；wunsequenced/compiler-warn/cross-compile/       │
│    linker → 本机 g++ 13.1.0 / clang++ 22.1.8                              │
└──────────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ ④ 判决 —— 任一回合任一档报出 ⇒ catch；两档都可用但都不报 ⇒ miss；          │
│           两档都不可用 ⇒ unknown；planted≠true ⇒ 对照单列                 │
└──────────────────────────────────────────────────────────────────────────┘
        │
        ▼
输出  data/experiments/baseline_fd.json（measurable = catch+miss）
      → data/current_numbers.json（权威源）→ 论文 / 前端 / 守卫
```

### A.4 「资产池」与「选择策略」的归属判定（审计结论）

| 环节 | 现状归属 | 判定 |
|---|---|---|
| 哪些探测器/规则存在 | detector 取值集合，**隐式** | **资产池**（需显式化） |
| 每个资产的成本/能力/适用缺陷类型 | **不存在** | **资产池**（需新增） |
| "给定预算选哪些资产运行" | **不存在**（FD 跑全池） | **选择策略**（需新增） |
| `select_assets_671b.budget()` | 事后从 catch 反推 | **既不是池也不是策略**，是**记账** |
| Random 臂的抽样 | `select_assets_*.py` | **选择策略**（已部分存在） |
| Static 臂 | 口径重分箱（按 layer） | **选择策略**（近似，非真选择） |

---

## B. 拆仓设计（四层）

```
┌─ ① 资产池层  tools/verifier_pool_673p.py ───────────────────────────────┐
│   AssetSpec{ id, kind, cost_units, cost_basis, capabilities,            │
│               defect_types, implemented, evidence_source, note }        │
│   12 项 = 8 已实测 + 4 声明未接线（coredump/gdb/ptrace/valgrind）         │
│   排除 measure / perf-counter（测量仪器，不是验证资产）                    │
│   受控词表：CAPABILITIES(6) / DEFECT_TYPES(16)                          │
│   verify_pool_integrity()：次序=字典序 / 无重复 / 词表内 / 标记自洽        │
└─────────────────────────────────────────────────────────────────────────┘
                     │  池（纯数据，不含任何样本）
                     ▼
┌─ ② 选择策略层  tools/selection_strategies_673p.py ──────────────────────┐
│   select(strategy, pool, *, max_assets, max_cost, fail_hits, seed)      │
│     failure_driven → fail_hits 降序（同分按 id 升序，确定性）             │
│     random         → random.Random(seed).sample（同 seed 可复现）        │
│     static         → 只取编译期/静态资产（字典序），不用运行时证据          │
│   预算 = (资产数 ∪ 序数成本)，取候选次序的**最大前缀**                    │
│   fail-loud：无预算 / 超池容量 / 成本不可行 / 缺 seed / 缺 fail_hits …    │
│   **纯函数**：不执行资产、不读样本                                        │
└─────────────────────────────────────────────────────────────────────────┘
                     │  Selection{assets, seed, cost_units, allocation_table}
                     ▼
┌─ ③ 运行层  tools/run_a5_experiment_673p.py::ReplayExecutor ─────────────┐
│   Executor 协议（可替换）：verdict(sample, selected) → catch/miss/…      │
│   本批实现 = ReplayExecutor（**单归属重放**，非真跑）：                    │
│     catch 且 detector(s) ∈ S → catch；unknown/not_error 原样；其余 miss  │
│   真跑（WSL + sanitizer，小时级）留给后续批次                             │
└─────────────────────────────────────────────────────────────────────────┘
                     │  逐样本重放判决
                     ▼
┌─ ④ 评估层  tools/run_a5_experiment_673p.py ─────────────────────────────┐
│   三臂同预算对比：fd_full_pool / fd_budget_matched / random / static      │
│   指标：k/n、CP95（Clopper–Pearson）、exact McNemar、Cohen's h            │
│   Random 随机性：单点 seed=20260930 配对 + 2000 次运行报分布              │
│   探索性派生集对照：旧样本估 fail_hits → 新样本评估                       │
└─────────────────────────────────────────────────────────────────────────┘
```

**与 672g 的关系**：672g 的 `select_assets(pool, n, strategy, seed)` 只支持**资产数**一种预算、
池是名字元组。673p 把池升级为带元数据的 `AssetSpec`、预算升级为（资产数 ∪ 成本），
并把"运行层"与"评估层"从接口里显式拆出。**抽样语义保持逐位一致**（见 D.3 的回归钉）。

---

## C. A5 预注册（摘要）

完整内容见 `data/673p_a5_preregistration.json`（**先于实现 commit**：`7ae34cf5`）。

- **假设**：H0 = 同预算下 FD selection 与 Random selection 的 holdout 可测检出率无差异；
  H1 = FD > Random。
- **主要指标**：holdout 可测检出率 = catch/(catch+miss)。
- **次要指标**：corpus 检出率、FD−Random 配对差值 + exact McNemar p、Random 2000 次运行分布、
  replay 墙钟（**非真实执行耗时**）、声明式序数成本。
- **样本量**：holdout 41 / corpus 64（与 672h 一致，不新增样本）。
- **预算**：FD 实际使用的资产数（holdout k=4 / corpus k=5）为上限；Random 与 Static 同预算。
- **检验**：exact McNemar（双侧），α=0.05；CI 用 Clopper–Pearson 95%。
- **停止规则**：落盘并单独 commit 后，**主要指标与预算定义不得修改**。

---

## D. 实现与验证

### D.1 交付物

| 文件 | 作用 |
|---|---|
| `tools/verifier_pool_673p.py` | 资产池定义（12 项，含 id/成本/能力/适用缺陷类型/实现标记） |
| `tools/selection_strategies_673p.py` | 三种选择策略 + 预算约束 + 分配表 |
| `tools/run_a5_experiment_673p.py` | 运行层（ReplayExecutor）+ 评估层 + A5 运行器 |
| `data/673p_a5_preregistration.json` | A5 预注册 |
| `data/experiments/a5_673p.json` | A5 结果（可复现，sha256 两跑一致） |
| `tests/test_verifier_pool_673p.py` | 资产池契约测试（26 条） |
| `tests/test_selection_strategies_673p.py` | 选择策略契约测试（31 条） |

### D.2 FD 复现验收：82.9% / 62.5% ✅

`fd_full_pool` 臂（= 现状 FD，跑全池）：

| 数据集 | k/n | 率 | CP95 |
|---|---|---|---|
| holdout | 34/41 | **82.93%** | [67.94, 92.85] |
| corpus | 40/64 | **62.50%** | [49.51, 74.30] |

与 `data/current_numbers.json` 的 82.9% / 62.5% **逐位一致** ⇒ 验收项达成。

### D.3 三臂同预算结果 + 与既有产物的交叉对账

**holdout（预算 k=4，锚 = asan/linker/tsan/ubsan）**

| 臂 | 选中资产 | k/n | 率 | CP95 | cost |
|---|---|---|---|---|---|
| FD（全池） | 8 项全池 | 34/41 | 82.93% | [67.94, 92.85] | 18 |
| Random（seed 20260930） | wunsequenced, cross-compile, tsan, compile-time | 4/41 | 9.76% | [2.72, 23.13] | 8 |
| Static | compiler-warn, cross-compile, linker, wunsequenced | 1/41 | 2.44% | [0.06, 12.86] | 8 |

FD−Random：Δ **+73.17pp**，exact McNemar **p = 1.86e-09**（b=30, c=0），Cohen's h = 1.65
→ 与 `current_numbers.json::holdout_fd_vs_random`（Δ 73.17 / p 1.86e-09）**逐位一致**。
FD−Static：Δ +80.49pp，p = 2.33e-10 → 与既有 `holdout_fd_vs_static` 一致。

**corpus（预算 k=5，锚 = asan/compiler-warn/cross-compile/tsan/ubsan）**

| 臂 | 选中资产 | k/n | 率 | CP95 | cost |
|---|---|---|---|---|---|
| FD（全池） | 8 项全池 | 40/64 | 62.50% | [49.51, 74.30] | 18 |
| Random（seed 20260930） | wunsequenced, cross-compile, tsan, compile-time, compiler-warn | 14/64 | 21.88% | [12.51, 33.97] | 10 |
| Static | compiler-warn, cross-compile, linker, wunsequenced | 11/64 | 17.19% | [8.90, 28.68] | 8 |

FD−Random：Δ **+40.63pp**，p = **2.98e-08**（b=26, c=0）→ 与既有 `corpus_fd_vs_random`
（Δ 40.62 / p 2.98e-08）一致。FD−Static：Δ +45.31pp，p = 3.73e-09 → 与既有值一致。

**回归钉**：`select("random", pool, max_assets=4, seed=20260930)` 的输出与 672g 权威实现
（`b3_real_672g.json::random_selection.picked`）**逐位相同**；n=5 同理。
这条回归钉写进了 `tests/test_selection_strategies_673p.py`。

**一个必须登记的巧合**：本批"真 B3 资产级随机"（seed 20260930）的单点数
（9.76% / 21.88%）与既有"仪器级代理 Random†"（9.8% / 21.9%）**相等**。
原因已查清：两者抽中的**有效抓取资产**相同（holdout 都只有 tsan 贡献 4 个 catch；
corpus 都是 compiler-warn + cross-compile + tsan = 14 个）。这不代表代理臂"因此可用"——
口径仍是仪器级，仍禁止进论文；只是本批顺带解释了那个巧合。

### D.4 Random 臂的随机性（2000 次运行，预注册钉死）

| 数据集 | 均值 | 标准差 | 最小 | 最大 | 2.5 分位 | 97.5 分位 |
|---|---|---|---|---|---|---|
| holdout | 40.88% | 29.32pp | 0.00% | **82.93%** | 2.44% | 80.49% |
| corpus | 39.29% | 12.50pp | 7.81% | **62.50%** | 17.19% | 59.38% |

**关键读数（A5 阻塞的数值证据）**：同预算随机抽样的检出率**最大值恰好等于 FD 的检出率**
（holdout 82.93% / corpus 62.50%）。因为 FD 的预算锚就是"能抓到东西的资产集合"本身
⇒ 在这个对照里 **FD = argmax**，任何随机子集都不可能超过它。这不是"选择策略更好"，
而是**预算锚的定义把答案写进了问题里**。

### D.5 探索性派生集对照（本批唯一让 FD 成为真预测器的对照）

做法：`fail_hits` 只用**派生集**（672h 扩样前旧样本：holdout 21 条 / corpus 48 条）估计，
在**评测集**（扩样新样本：holdout 20 条 / corpus 16 条）上评估。FD 不含评测集信息。

| 数据集 | 派生 n → 评测 n | FD | Random | Static | FD−Random Δ | McNemar p |
|---|---|---|---|---|---|---|
| holdout | 21 → 20（k=4） | 17/20 = **85.0%** [62.1, 96.8] | 2/20 = 10.0% | 0/20 = 0.0% | +75.0pp | 6.10e-05 |
| corpus | 48 → 16（k=5） | 14/16 = **87.5%** [61.7, 98.4] | 6/16 = 37.5% | 4/16 = 25.0% | +50.0pp | 7.81e-03 |

**这是本批第一次给出"选择 vs 随机"的可比信号**（FD 是真预测器，不是 oracle）。
但它**非预注册、非确认性**：n=20/16 极小（远低于 ±15pp 所需的 n=138），
且派生集与评测集出自同一批夹具政策（672h H4 已登记 corpus 新子集检出率显著更高）。
⇒ **只读方向 + CI，不得写成确认性结论**。

### D.6 测试与门禁

- 新增测试 **57 条**全绿（`test_verifier_pool_673p.py` 26 条 + `test_selection_strategies_673p.py` 31 条）。
  **未修改任何已有测试的断言**（红线 3）。
- `ruff check` 三个新工具：**All checks passed**（CI 的 `ruff check tools/` 硬门禁口径）。
- `mypy` 三个新工具：**Success: no issues found**（CI 的 `mypy tools/` 硬门禁口径）。
- 复现性：`a5_673p.json` 两跑内容 sha256 相同（`d314d137…`，已剔除计时字段）。
- `fast_gate`（`pytest tests/ -q -m "not slow" -n 16`）：见 §D.7。

### D.7 fast_gate 结果

**（1）本批官方门禁 —— PASS**

```
$ python tools/fast_gate.py --tests tests/test_verifier_pool_673p.py \
                            tests/test_selection_strategies_673p.py --skip-frontend
  [SKIP] 前端自测（--skip-frontend）  0.0s
  [PASS] 658 门禁（L0 5/5 + S5/S6）  7.3s
  [PASS] 669d 门禁（六条 P0 规则）  0.9s
  [PASS] 671a guard（三方数字一致）  1.9s
  [PASS] pytest（本批指定）  43.6s
[fast-gate] overall=PASS  总耗时 43.6s（预算 300s）
```

三道交付门禁（658 / 669d / 671a guard）全 PASS，本批新增测试 PASS。
`--skip-frontend` 的依据：本批未改 `web/` 任何文件（`git status -- web/` 为空）。

**（2）全量快档 —— 该套件在 `-n 16` 下本身不稳定（如实登记）**

| 运行 | 命令 | 失败数 |
|---|---|---|
| A（含本批测试） | `pytest tests/ -q -m "not slow" -n 16` | 30（`tail -30` 截断，实际 ≥30） |
| B（不含本批测试，基线） | 同上 + `--ignore=tests/test_*_673p.py` | 59 |

同一仓状态（同一 HEAD + 同一份既存脏工作树）两次运行失败数不同（30 vs 59），
且两个失败集**互有出入**（B 有 30 项在 A 里通过，A 有 1 项在 B 里通过）
⇒ 与 `670c` 提交信息登记的结论同因：*"不绑定语料版本的 fast 失败数不是可引用的数字"*。

**关键判据：本批新增测试在两次全量运行中均为 0 失败**（`grep 673p` 命中 0）。
失败集合全部落在既有的"语料镜像刷新 / 信任根陈旧 + 并发 flip-flop"类
（`test_pck_hash_renewal_628`、`test_tool_integrity_647`、`test_readonly_replay_669`、
`test_replay_lock_shard_580`、`test_task_queue`、`test_metrics_collector`…），
与 673h/673m 的 skip 登记同源。

**（3）串行决定性对照（去并发 flake）**

把上表两个失败集的**并集文件**（34 个文件）串行（`-n 0`）跑一次：

| 运行 | 失败数 | 与本批的关系 |
|---|---|---|
| 基线 B（`-n 16`，不含本批测试） | 59 | — |
| 串行（`-n 0`，34 个失败文件） | 58 | 本批测试**不在**该文件集内 |

两者交集 **47**（稳定失败），仅 B 有 12（并发特有），仅串行有 11（串行特有）
⇒ 该套件在本仓当前脏工作树下**即使串行也有约 20% 的运行间波动**。

**（4）不回归判据（三条同时成立）**

1. **本批新增测试在全部运行中 0 失败**：含本批的 `-n 16` 全量跑、串行跑、
   以及 `fast_gate --tests` 三处均通过（57 条）。
2. **官方门禁 PASS**：`fast_gate`（658 / 669d / 671a guard / 本批 pytest）overall=PASS。
3. **改动纯增量**：3 个新工具 + 2 个新测试 + 2 个数据文件；**未修改任何既有文件逻辑**
   （`git status` 里既有文件的 `M` 全是本批之前就存在的脏工作树状态，
   与 673h/673m 的 skip 登记同源）。

**如实登记的局限**：本仓 `-m "not slow"` 快档当前**不能给出可引用的稳定失败数**
（30 / 58 / 59 三个数来自同一 HEAD + 同一脏树）。这与 `670c` 的审计结论一致：
*"不绑定语料版本的 fast 失败数不是可引用的数字"*。因此本批的"不回归"证据以
**官方门禁 PASS + 本批测试 0 失败 + 纯增量**为准，不以全量失败数差值为准。

---

## E. 诚实登记

### E.1 A5 阻塞条件 3：现有架构不支持干净分离（本批新增）

- **现象**：FD 没有选择层。它对每个样本跑全池；"FD 用到的资产数"（4/5）是事后从 catch
  反推的**记账量**。
- **后果（两条路都堵）**：
  1. 预算锚 = "FD 实际用到的资产数" ⇒ 用的是**评测集自身**的信息 ⇒ FD 是 **oracle**
     （D.4 已给出数值证据：随机抽样最大值 = FD 值）；
  2. 预算 = 全池大小 8 ⇒ Random 抽满池 ⇒ Δ **恒为 0**。
- **判定**：**A5 主对照（FD vs Random）不得被读作**
  "failure-driven selection 优于 random selection"的确认性证据。
- **缓解（已实现）**：探索性派生集对照（D.5），让 FD 成为真预测器；明确标为非确认性。
- **后续建议（不在本批范围）**：让 FD **真正**在预算下选子集——即把"失败驱动"实现成
  "用历史失败分布给资产排序，然后只跑 top-k"，而不是跑全池。这需要改动
  `holdout_reveal_661.py::detect` 的执行语义（本批红线不允许改判据），列为独立批次。

### E.2 运行层是 replay（单归属假设），不是真跑

- 明细每条只记**一个** detector 归属 ⇒ 重放模型假设"这条样本的 catch 只属于它"。
- 偏差方向：**大资产集被低估、小资产集被高估**。
- 缓解：该模型在 672g 的 22/60 样本上**逐位复现**了 FD 17/21、Static 1/21、Random 2/21
  （corpus 26/48、7/48、8/48）⇒ 与既有实现同口径，可作对照。
- **真跑**（WSL + sanitizer，小时级）留给后续批次；`Executor` 协议已留好替换点。

### E.3 成本是声明式序数，非实测墙钟

- `cost_units`（1=静态 / 2=编译器 pass / 3=插桩执行 / 4=全量动态分析 / 5=事后取证）
  是**序数**，本批**没有**测每个资产的墙钟耗时。
- ⇒ 不得把 `cost_units` 换算成秒，也不得报"省了多少时间"。
- 已在池定义与产物里显式标注 `cost_basis = declared_ordinal`。

### E.4 样本量不足

- holdout 41 / corpus 64 仍低于 ±15pp 配对检验所需的 n=138（`sample_size_671b.json`）。
- ⇒ 即便 p<0.05，**幅度不得写成确认性点估计**，只读方向 + CI。

### E.5 未把「资产池存在」当成「selection 策略有效」

- 本批**建成**了资产池（12 项带元数据）与选择策略（三臂可运行、预算约束生效），
  但**没有**因此声称 selection 策略有效。
- 两个因素严格分离：§D.3 的主对照被 §E.1 判定为**不可用于确认性结论**；
  §D.5 的探索性对照是唯一可比信号，且明确标为非确认性。

---

## F. 交付清单与验收对照

| 验收项 | 结果 |
|---|---|
| 资产池定义完整（id/成本/能力/适用类型） | ✅ 12 项，全部字段齐全，词表受控 |
| 三种策略都能在同预算下运行 | ✅ FD / Random / Static 三臂同预算跑通，分配表落盘 |
| FD 复现 82.9% / 62.5% | ✅ 82.93% / 62.50%，逐位一致 |
| A5 预注册完整（假设/指标/样本量/检验/停止规则） | ✅ `data/673p_a5_preregistration.json`，先于实现 commit |
| 新增测试全绿 | ✅ 57 条（三处运行均 0 失败） |
| fast_gate 不回归 | ✅ 官方 `fast_gate --tests … --skip-frontend` overall=PASS；本批测试 0 失败；改动纯增量（局限见 §D.7(4)） |
| 不碰 `research/`、`web/` | ✅ 本批未改这两个目录任何文件（`git status -- web/` 为空；`research/` 唯一改动 `queyi_refs.bib` 是本批之前就存在的脏工作树状态，**未纳入本批提交**） |

**提交**：DCO 签名，**不 push**。
- `7ae34cf5` 673p: A5 预注册（先于实现落盘）
- （第二个 commit）673p: 拆仓 verifier 三层基础设施 + A5 实验 + 测试 + 报告

---

## G. 未决 / 建议后续批次

1. **让 FD 真正选择**（解 E.1）：改 `holdout_reveal_661.py::detect` 支持"只跑选中子集"，
   再重跑 A5 —— 那才是论文主张的干净隔离。**这是把 A5 从 BLOCKED 变绿的唯一路径。**
2. **真跑替换 replay**（解 E.2）：实现 `SubprocessExecutor`（WSL + sanitizer）。
3. **实测资产成本**（解 E.3）：逐资产测墙钟，把 `cost_basis` 从 `declared_ordinal` 升级。
4. **接线声明未接线的 4 个资产**（coredump/gdb/ptrace/valgrind）：它们现在只登记在池里。
5. **扩样到 n≥138**（解 E.4）：否则 A5 的幅度永远只能读方向。

---

## 门禁实跑记录

| 命令 | 结果 |
|---|---|
| `python tools/fast_gate.py --tests tests/test_verifier_pool_673p.py tests/test_selection_strategies_673p.py --skip-frontend` | **overall=PASS** 43.6s（658 7.3s / 669d 0.9s / 671a guard 1.9s / pytest 43.6s） |
| `pytest tests/test_verifier_pool_673p.py tests/test_selection_strategies_673p.py -q` | **57 passed** |
| `pytest tests/ -q -m "not slow" -n 16` | 30+ failed（含本批：本批测试 0 失败） |
| 同上 `--ignore=tests/test_*_673p.py` | 59 failed（基线） |
| `pytest <34 个失败文件> -q -n 0` | 58 failed（本批测试 0 失败） |
| `ruff check tools/{verifier_pool,selection_strategies,run_a5_experiment}_673p.py` | **All checks passed** |
| `mypy tools/{verifier_pool,selection_strategies,run_a5_experiment}_673p.py` | **Success: no issues found** |
| `python tools/run_a5_experiment_673p.py` | 复现性 `identical=True`（sha256 `d314d137…`） |

**环境提示（与仓库无关）**：本机存在安全删除拦截层，pytest 的 tmp 清理与部分
`build/` 重建会被拦（`SAFE_DELETE_BULK_CONFIRM_REQUIRED`），与 673m 登记的现象同源。

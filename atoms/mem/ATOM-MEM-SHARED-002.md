---
id: ATOM-MEM-SHARED-002
title: shared_ptr 的线程安全边界与原子代价：控制块原子、对象不原子
domain: MEM
type: pitfall
status: verified               # 唯人可置 verified（S1 三权分立）
verified_by: human:liaoranran  # 签署人（非 Agent）
verified_at: 2026-09-11        # 签署日期
# ---- 认知适切 ----
audience: intermediate                # 默认读者：听过"shared_ptr 引用计数是原子的"、于是以为怎么用都安全的人
cognitive_load: medium                # 需同时持有"计数安全 ≠ 对象安全"与"实现层 lock 指令"两条线索
prerequisites_readable: true          # 前置 ATOM-MEM-SHARED-001 已 verified
claim: >-
  shared_ptr 的控制块引用计数用 LOCK 前缀的原子 RMW 修改，因此**各线程持有各自副本**时的并发
  拷贝/销毁是安全的；但**被指对象**与**同一个 shared_ptr 实例**都不受这层保护（并发读写同一实例
  需外部同步，C++20 起可用 std::atomic<std::shared_ptr<T>>；use_count() 在并发下只是近似值）。
  unique_ptr 的所有权转移是纯指针搬运、不含原子 RMW，代价是**不可拷贝**——要共享必须显式改用
  shared_ptr，于是"要不要付原子代价"成了编译期可判的选择，而不是运行期祈祷。
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]
  compilers: [GCC 15.3.0]
  stdlib: [libstdc++]                 # lock 指令形态与控制块符号名是实现特性
  opt: [-O0, -O2]
  platform: [x86-64 MinGW-w64]
relations:
  - {type: prerequisite, target: ATOM-MEM-SHARED-001}   # 共享所有权的基本语义（本原子答"并发下哪一层安全、代价在哪"）
  - {type: contrasts, target: ATOM-MEM-WEAK-001}        # 弱计数与过期提升：另一条 CAS 路径（lock cmpxchg）
evidence:
  - EV-MEM-034          # 引用计数原子：控制块锚点 + lock 指令 + 多线程副本并发（烟测）
  - EV-MEM-035          # 镜像对照：unique_ptr 工件全文零 lock（单条 absent 覆盖全形态）
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [util.smartptr.shared]（shared_ptr 的线程安全要求：仅控制块计数保证原子，对象与实例本身不保证）", independent: true}
  - {kind: cppreference, ref: "std::shared_ptr 的线程安全说明（含『不同实例可并发修改』与 use_count 近似性）、std::atomic<std::shared_ptr>（C++20）", independent: true}
  - {kind: implementation, ref: "libstdc++ shared_ptr_base.h：_Sp_counted_base::_M_add_ref_copy / _M_release 的原子 RMW 实现（lock add/sub/xadd；weak 提升用 lock cmpxchg 重试）", independent: true}
first_hand: true
superiority: >-
  ISO [util.smartptr.shared]：标准只给"哪些操作安全"的条文，本书多给了可执行的判据与**指令级归属**
  （lock 指令全部落在控制块符号作用域内，且夹具自身不含原子计数器 ⇒ 排除"编译器到处撒 lock"的
  替代解释）。
  cppreference：条目给出 use_count 是近似值，本书多给了**为什么**（它是对控制块强计数的一次无锁
  32 位读，与 lock 加/减同地址）以及"在 join 之后读它才是确定值"的操作口径。
  libstdc++ 实现：源码给出实现形态，本书多给了**跨编译器实测**（MinGW `lock add/sub` vs gcc-14
  `lock add/xadd`）以及被红队逼出来的**判决性对照**（unique_ptr 工件同档零 lock，8 vs 0）。
depth:
  layer: asm
  drill_note: >-
    两层证据：指令级（LOCK 前缀 RMW + 控制块符号锚点，确定性、可复算）与运行级（4 线程各持副本
    并发拷贝/销毁，join 后计数收敛；单次拷贝使 use_count 1→2 的确定性观测）。运行级**只作烟测**
    ——竞态窗口不保证必定重叠，本夹具不是竞态检测器（TSan 才是，其缺口已在 EV-MEM-034 的矩阵
    sanitizer 维显式声明）。`-O2` 下引用计数以 `lock add/sub/xadd` 直接出现在控制块方法体内。
pedagogy:
  motivation: >-
    "shared_ptr 引用计数是原子的"这句话到底保证什么、不保证什么？把它传进多个线程，什么情况下
    还需要加锁？为什么 unique_ptr 在同样场景下根本不给编译的机会？
  misconceptions: [MIS-MEM-026]
  socratic:
    - "两个线程各自持有 shared_ptr 的副本并发拷贝/销毁，安全吗？换成它们读写**同一个** shared_ptr 实例呢？"
    - "把 shared_ptr 传给多个线程之后，被指对象的成员变量需要加锁吗？为什么？"
    - "能不能用 use_count()==1 判断'当前只有我持有'，据此决定是否原地修改对象？"
    - "unique_ptr 为什么不允许拷贝？这条限制给你换来了什么？"
  predict_first: >-
    先预测两个数字再看证据：① `sizeof(shared_ptr<int>)` 与 `sizeof(unique_ptr<int>)`；
    ② 在 shared_ptr 的汇编工件里，与引用计数相关的 `lock` 前缀指令大约有多少条，unique_ptr 的
    工件里呢？（再看 EV-MEM-034 / 035 的工件实测）
---

## 论断

**"引用计数原子"只保护计数，不保护对象，也不保护实例。** 一句话判据：**计数安全 ≠ 对象安全。**

| 被并发访问的东西 | 是否安全 | 依据 |
|---|---|---|
| **各持一份副本**，并发拷贝/销毁 | ✅ 安全 | 控制块强/弱计数是原子 RMW（EV-MEM-034：lock 指令落在控制块符号作用域内） |
| **同一个 shared_ptr 实例**被并发读写 | ❌ 不安全 | 实例本身只是"对象指针 + 控制块指针"两个普通字段，无原子修饰；需外部同步或 C++20 `std::atomic<std::shared_ptr<T>>` |
| **被指对象**被并发访问 | ❌ 不受保护 | shared_ptr 只管计数，对象内部状态要自己的同步 |
| 用 `use_count()` 做并发判断 | ❌ 不可靠 | 实现为一次无锁 32 位读，并发下只是近似值 |

## 为什么（代价从哪来、边界在哪）

**代价侧**：控制块计数用 LOCK 前缀的原子 RMW（MinGW 实测 `lock add` ×3 / `lock sub` ×5；
gcc-14 实测 `lock add` ×3 / `lock xadd` ×5），且这些指令**全部落在控制块符号作用域内**
（`_Sp_counted_base::_M_releaseEv` 等）——这一点由夹具设计保证：夹具自身不含任何原子计数器
（每线程写各自的 `std::vector` 槽位、join 后主线程求和），所以工件里的每条 lock 都可归因 shared_ptr。

**对照侧**：unique_ptr 的所有权转移是纯指针搬运，工件**全文零 `lock`**（EV-MEM-035，两平台均为 0），
且它的拷贝构造被删除（`copyable=0`）——共享这条路在**编译期**就被关掉。"要不要付原子代价"因此
是类型层面可见的选择。

**边界侧**：`weak_ptr::lock()` 的"提升"走的是另一条更重的路（CAS 重试，仓内工件实测
`lock cmpxchg`），这正是"过期竞态"的机器形态（详见 ATOM-MEM-WEAK-001 的领域）。

## 证据

| 证据 | 观测 | 结论 |
|---|---|---|
| `EV-MEM-034`（c++23 -O0/-O2 同串） | 控制块锚点 9–10 次；`lock add` ×3 + `lock sub` ×5（MinGW）；4 线程 × 2000 次后 `use_count after join=1`；单次拷贝后 `use_count=2` | 引用计数是原子 RMW，各持副本并发拷贝安全 |
| `EV-MEM-035`（c++23 -O0/-O2 同串） | 工件全文零 `lock`；`sizeof=8`、`copyable=0`、`movable=1`；析构恰 1 次 | unique_ptr 所有权管理无原子操作，共享在编译期被禁止 |

## 反例（证伪导向：让它失败的实验）

- **证伪条件 A（指令级，主证）**：若引用计数不是原子的，工件里就不会有 `lock` 前缀 RMW 落在控制块
  符号作用域内——实测存在，且夹具自身无原子计数器可供"冒名"。
- **证伪条件 B**：若 unique_ptr 的转移需要原子操作，其工件会出现 `lock`——实测 0（一条 `absent`
  覆盖全部指令形态）。
- **证伪条件 C（确定性对照）**：`use_count after one copy=2`——拷贝**必然**改变计数；若这条不成立，
  说明观测点没落在拷贝上。
- **已降级的"伪对照"（红队拦截留痕）**：`use_count after join=1` 曾被当作原子性证据，实际上 join 后
  任何"增减配平"的执行都会读到 1，对原子/非原子**零判别力**——现只作烟测，主证责任在指令级锚点。

## 学习者常见误解

1. **`[MIS-MEM-026]` "shared_ptr 是线程安全的"**——把"计数原子"外推成"对象安全"；三条边界
   （同一实例 / 被指对象 / `use_count()` 近似性）在本卡与误解条目里逐条列出。

## 不该用 / 边界

- **不要用 `use_count()` 做同步或唯一性判断**（并发下只是近似值）。
- **同一实例跨线程共享必须加锁**（或 C++20 `std::atomic<std::shared_ptr<T>>`）。
- **对象的并发访问与智能指针无关**——shared_ptr 不是对象级锁。
- **unique_ptr 的"零原子"不等于"线程无关"**：它只是把共享变成编译期错误，跨线程传递仍需外部同步
  （例如通过队列交接所有权）。

## 学习路径

`ATOM-MEM-SHARED-001`（共享所有权与引用计数语义）→ **本原子**（并发下哪一层安全、代价在哪）→
`ATOM-MEM-WEAK-001`（弱计数与过期提升的 CAS 路径）→ `ATOM-MEM-UNIQUE-002`（删除器与类型参数化）。

---

## Step 1：3 分平庸版（留痕）

初版 claim 写"shared_ptr 引用计数是原子的，所以 shared_ptr 是线程安全的；unique_ptr 没有原子开销，
更快"——**把结论说得比证据大**：① 把"计数原子"外推成"整体线程安全"（与证据卡自己的边界声明
相互矛盾）；② "更快"零计时数据；③ 未提同一实例/被指对象/`use_count()` 近似性；④ 缺边界与学习路径；
⑤ 只引 1 条独立源；⑥ 教学封装各 1 条。自评 **3/5**。

## Step 2：红队攻击报告（独立子 agent，S1–S6）

> 红队由 Task 工具启动的独立子 agent 执行，**只挑错不改正文**。以下为要点，完整报告含逐行工件行号。

**阻断项（4）**

1. **B1 · claim 与证据自相矛盾**：claim/正文写"shared_ptr 线程安全""unique_ptr 更快"，而 EV-MEM-034
   的边界声明明确否认；且两张卡的 `hypothesis` 都是收窄版 ⇒ **没有任何卡检验过该 claim**（M2 §1
   "可直接抄 claim"未达成）。违反"一原子 = 一可证伪断言（单句）"。
   → 处置：claim 重写为可辩护单句（见 Step 3）。
2. **B2 · `MIS-MEM-026` 不存在**：草稿引用了未创建的误解条目 ⇒ `ATOM-MISCONCEPTION-REF` 是 **block**；
   因门禁只扫 `atoms/`，该 block 会在 `git mv` 那一刻引爆（S4 停线）。
   → 处置：**已新建 `misconceptions/MIS-MEM-026.md`**（deep 级、4 条 refutations，反例绑 034/035）。
3. **B3 · 断言对关键变异免疫（伪证据）**：034 原夹具用 `std::atomic<long> g_copies` 自计数，工件 9 条
   lock 里 **2 条属于夹具自身** ⇒ 若把 shared_ptr 换成手工非原子计数，断言**仍然通过**。
   → 处置：夹具改为"每线程写各自 vector 槽位 + join 后求和"（**零自带原子**），lock 数 9→8 且全部
   可归因控制块；断言补**控制块符号锚点**（`_M_releaseEv` / `_Sp_counted_base`）。
4. **B4 · `use_count after join=1` 无判别力**：join 后所有副本已销毁，任何配平执行都读到 1；且
   `total copies=8000` 是自计数（真实拷贝数 8004）。
   → 处置：降级为**烟测**并在卡内写明"本夹具不是竞态检测器"；新增确定性对照
   `use_count after one copy=2`；`total copies` 改名 `copies observed`（明确是"观测到的循环次数"）。

**高危项（4）**

5. **H1 · `moves=2` 被 -O2 常量折叠**（非 volatile，工件里是 `mov edx, 2`）——与 M2 §5 事故链同型；
   且两卡都缺 `-O0` 双跑与口径披露。 → 处置：`moves` 改 **volatile**；两卡补 `-O0` 复跑留痕 +
   矩阵 `opt: [-O0, -O2]` + 「机器口径」节。
6. **H2 · 并发类卡缺 TSan 维**（M2 §2 要求"并发类加 TSan"）。 → 处置：在 034 矩阵 `sanitizer` 维
   **显式声明缺口**（MinGW 无 TSan，Linux/WSL 待补跑），并以指令级锚点承担主证。
7. **H3 · lock 候选集不完备**：漏 `lock cmpxchg`（仓内 `_atom_weak_obs.asm:293` 就是同控制块反例）、
   `lock inc/dec`。 → 处置：候选补全为 6 形态（add/sub/xadd/cmpxchg/inc/dec）。
8. **H4 · "更快"零计时数据**，且与 EV-MEM-032/033 已量化内容重叠。 → 处置：claim 收窄为"无原子 RMW
   + sizeof=8 + 少一次控制块分配（引用 EV-MEM-032/033）"，删除速度断言。

**中危项（6，摘要）**：仅 1 条独立源（已补 cppreference + libstdc++ 实现，共 3 条）；superiority 未按
逐源格式（已改写）；gcc-14 数字无仓内工件（已在卡内标注"外部复跑留痕"，不入断言）；主题与
`References/20/25` 的计划绑定不一致（本卡按用户口径"线程安全与代价"执行，**留痕待裁决**）；
035 的 5 条 absent 是开集枚举（已改夹具名 + 单条 `absent: "lock"`）；未标编译期常量 vs 运行期读
（已加机器口径节）；`rc=0` 被当证据（已降级为"未观察到崩溃"，不进 falsification 主证）。

**S6 制衡缺口（工具债）**：变异 **M1（引用计数非原子）** 在原设计下会全绿漏网——正是 B3 揭示的
"断言被夹具自身满足"模式；变异 **M2（掏空循环体保留标签）** 也会漏网（缺"绑定到拷贝动作"的观测，
现已由 `use_count after one copy=2` 补上）。建议下一批新增毒样例 **P4 自证断言 / P5 伪证伪 /
P6 恒真观测 / P7 无留痕矩阵**（与 UNIQUE-002 红队提出的是同一批工具债）。

## Step 3：升 5 分候选（逐条回应红队）

| 红队指控 | 处置 | 证据 / 落点 |
|---|---|---|
| B1 claim 越界/自相矛盾 | claim 重写为单句可辩护版（各持副本 / 三条边界 / 编译期选择） | frontmatter claim + 论断节的边界表 |
| B2 MIS-MEM-026 缺失 | **新建** deep 级误解条目（4 条 refutations） | `misconceptions/MIS-MEM-026.md` |
| B3 断言对变异免疫 | 夹具去自带原子计数器（改 per-thread 槽位求和）；断言加控制块锚点 | 夹具 + 034 断言 1；lock 数 9→8 全归因控制块 |
| B4 烟测冒充证据 | 降级为烟测 + 加确定性对照 + 改标签名 | 034 的 falsification 与 actual |
| H1 常量折叠 + 缺 -O0 | `moves` 改 volatile；两卡补 -O0 留痕与口径节 | 035 夹具 + 两卡矩阵/口径节 |
| H2 缺 TSan | 矩阵显式声明缺口 | 034 的 `matrix.sanitizer` |
| H3 lock 形态遗漏 | 候选补至 6 形态 | 034 断言 2 |
| H4 "更快"无据 | 收窄表述并指向 EV-MEM-032/033 | claim + superiority |
| 中危 6 项 | 逐项落卡（见上"中危项"摘要） | 两卡与 frontmatter |

**平庸版 → 5 分候选的关键补丁（三处增量）**

1. **统一解释有增量**：把"shared_ptr 线程安全"拆成**四格边界表**（各持副本 / 同一实例 / 被指对象 /
   `use_count()`），并用"计数安全 ≠ 对象安全"一句收束——多数资料只给结论，不给这张表。
2. **量化到机器证据且归属可判**：代价侧用**控制块锚点 + lock 指令**（并证明夹具自身不含原子计数器，
   排除"编译器到处撒 lock"），对照侧用**同档同工具链的零 lock 工件**（8 vs 0）。
3. **过程本身有教学价值**：本卡记录了一次真实的"伪证伪被拆穿"——`use_count after join=1` 曾被当作
   原子性证据，红队指出它对原子/非原子零判别力后降级为烟测，并补上确定性对照。这条留痕给出一个
   可复用的自检问题：**"这个数字在假设结论为假时会不会变？"**

## Step 4：人审准备（等 human:liaoranran）

1. **主题归属裁决**：`References/20`/`25` 把 SHARED-002 计划为"make_shared 优势与控制块布局"，而
   用户口径与本卡是"线程安全与代价"（其中 make_shared 的分配证据已由 EV-MEM-033 用掉）。是否需要
   更新计划表，或把"控制块布局"（强/弱计数压成 8 字节，`movabs rdx, 4294967297`）另开一张卡？
2. **TSan 缺口的处置**：并发类卡按 M2 §2 应加 TSan 维。本卡目前以"指令级锚点承担主证 + 矩阵显式声明
   缺口"过关。是否接受（本卡判断：接受，因为 lock 指令是比 TSan 更强的**充分**证据——TSan 证明
   "本次运行无竞态"，lock 指令证明"实现层不可能有竞态"），还是要求在 WSL 侧补跑 TSan 后再签？
3. **非原子反例是否要另立卡**：红队建议做一张"手工非原子计数"的变异夹具并报告崩溃/偏离**出现率**
   （概率性对照）。它能把"若计数非原子则失败"从假设变成实测，但会引入一个概率性输出的卡
   （与"确定性"夹具纪律有张力）。是否值得？

## Writer 自评（最高 4，不自称达标）

| 维度 | 自评 | 说明 |
|---|---|---|
| rubric 总分 | **4/5** | 五重剖面齐全（3 条独立源含 ISO 段级 + cppreference + libstdc++ 实现；两卡一手实证含控制块锚点与镜像对照、-O0/-O2 双档一致；superiority 逐源写；depth=asm；教学封装 4 条 socratic + predict_first）；自评上限 4：**TSan 维缺口未闭合（Linux 侧待补跑）**、跨编译器仅 GCC 系（Clang 列待 CI 回填）、gcc-14 数字无仓内工件留痕。 |

---
id: ATOM-MEM-LEAK-001
title: 内存泄漏的检测信号分层：为什么"ASan 没报"不等于"没泄漏"
domain: MEM
type: contrast                 # 三档 × 两结构的检测结论对照（M1_ontology §2 的 10 类之内；原写的 "tool" 不在枚举内，入库时被 ATOM-ID-FORMAT 拦下）
status: verified               # 唯人可置 verified（S1 三权分立）
verified_by: human:liaoranran  # 签署人（非 Agent）
verified_at: 2026-09-11        # 签署日期
# ---- 认知适切 ----
audience: intermediate                # 默认读者：把"跑一遍 ASan 没报错"当成泄漏检查完成的人
cognitive_load: medium                # 需同时持有"信号分层"与"sanitizer 判定依赖优化档/存活位置"两条线索
prerequisites_readable: true          # 前置 ATOM-MEM-WEAK-001 / ATOM-MEM-SHARED-001 均已 verified
claim: >-
  内存泄漏的机器检测信号分三层且强度不同——进程退出码与 stderr **不携带**泄漏信号（泄漏进程照常
  `return 0`、无任何错误输出），夹具内 volatile 析构计数与控制块 `use_count()` 是**不依赖 sanitizer
  环境**的确定信号，而 ASan/LSan 的判定**对优化档与对象存活位置高度敏感**（同一泄漏：`-O0` 极简环报
  80 B/2 次分配、同档树形不报、`noinline` 隔离后 `-O2` 树形报 224 B/4 次分配、而 `-O2` 极简环不报）
  ——因此"ASan 没报"不能推出"没泄漏"。
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]
  compilers: [GCC 15.3.0]                  # 运行层留痕（MinGW）；sanitizer 层留痕见下
  sanitizer_env: [WSL Ubuntu g++-14.2, -std=c++23, -fsanitize=address,undefined, ASAN_OPTIONS 默认]
  opt: [-O0, -O1, -O2]                     # 三档均已实测（sanitizer 层）
  platform: [x86-64 MinGW-w64（运行层）; x86-64 Linux（sanitizer 层）]
relations:
  - {type: prerequisite, target: ATOM-MEM-WEAK-001}     # 机制侧（环如何形成、weak 如何打破）由该原子承担，本卡不复述
  - {type: prerequisite, target: ATOM-MEM-SHARED-001}   # 引用计数语义
evidence:
  - EV-MEM-036          # 正确侧基线：owner/observer 结构整树析构（destroyed=3）+ 两个运行期观测
  - EV-MEM-037          # 缺陷侧 + 检测标定：零析构（destroyed=0）+ 三档 × 两结构 5 个 LSan 数据点
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [util.smartptr.shared]/[util.smartptr.weak]（所有权与弱引用语义：机制侧归 prerequisite 原子）", independent: true}
  - {kind: doc, ref: "AddressSanitizer/LeakSanitizer 官方文档：泄漏检测基于退出时的可达性分析（reachability），被存活栈帧/寄存器引用的块不算泄漏", independent: true}
  - {kind: cppreference, ref: "std::weak_ptr::expired / use_count 的语义（零额外仪器的独立信号）", independent: true}
first_hand: true
superiority: >-
  ISO [util.smartptr.*]：条文只规定所有权与弱引用语义，不涉及检测；本书多给了"检测侧"的可操作分层
  （退出码/stderr 无信号 → 内置观测为确定信号 → sanitizer 受优化档与存活位置影响）。
  ASan 官方文档：文档说明泄漏检测基于退出时可达性，本书多给了**本仓库工具链上的档位实测矩阵**
  （5 个数据点，含"极简环 -O0 报 / -O2 不报"与"树形 -O0/-O1 不报 / noinline 后 -O2 报"这组反直觉对照），
  以及一条被实测推翻的初始归因（原以为"LSan 有结构性漏报"）。
  cppreference：只给 `expired()`/`use_count()` 的语义，本书多给了"它们是不依赖 sanitizer 的确定信号"
  这一层工程判据，并把它与 `destroyed` 计数并列为"零 sanitizer 依赖"的信号族。
depth:
  layer: runtime
  drill_note: >-
    本卡的落点是**检测信号的可信度分层**，机制（环 → 计数不归零 → 不析构；weak 打破）全部由
    prerequisite 原子承担。核心量化是"三档 × 两结构"的 LSan 标定矩阵（5 个实测点），它把
    "ASan 没报"从一个"结论"降级为一个"未判定"。
pedagogy:
  motivation: >-
    泄漏检测到底该信什么？跑一遍 ASan 干净就能收工吗？为什么同一个泄漏，换个优化档、换个结构，
    ASan 一会儿报一会儿不报？
  misconceptions: [MIS-MEM-027, MIS-MEM-016]   # ASan 没报=没泄漏；智能指针自动安全
  socratic:
    - "泄漏进程的退出码是多少？stderr 里有什么？"
    - "同一个泄漏，`-O0` 和 `-O2` 下 LSan 的结论会不会不同？为什么？"
    - "如果不装 sanitizer，你还能靠什么发现泄漏？"
    - "为什么把构树函数标上 noinline，LSan 就从'不报'变成'报'？"
  predict_first: >-
    先预测再看数据：同一份泄漏代码，`-O0` 与 `-O2` 下 LSan 的报告会相同吗？（再看 EV-MEM-037
    的三档矩阵——注意"极简环"与"树形结构"在两种档位下的结论正好互换。）
---

## 论断

**泄漏检测没有单一可靠手段；信号按"是否依赖 sanitizer 环境"分层，最弱的一层（退出码/stderr）恰好最常被当作检查依据。**

| 层 | 信号 | 是否携带泄漏 | 是否依赖 sanitizer | 本卡实测 |
|---|---|---|---|---|
| L0 | 进程退出码 / stderr | ❌ **不携带** | — | 泄漏进程 `rc=0`、stderr 干净（EV-MEM-037） |
| L1 | 夹具内 volatile 析构计数 | ✅ 确定信号 | 否 | `destroyed after scope=0`（泄漏）vs `3`（正确） |
| L1' | 控制块 `use_count()` | ✅ 确定信号 | 否 | `root use_count=3`（= 局部变量 1 + 两条强边 2） |
| L1'' | `weak_ptr::expired()` | ✅ 确定信号 | 否 | 弱边下的过期两态 |
| L2 | ASan/LSan 报告 | ⚠️ **可能漏报** | 是 | 三档 × 两结构 5 个数据点（见下） |
| L3 | 进程内存增长（RSS/heap） | ⚠️ 需放大才可见 | 否 | 本夹具只构树一次，**不适用**（如实声明） |

## 为什么（L2 为什么不可靠：三档实测）

同一类泄漏（`shared_ptr` 参与的环，进程退出时内存不可达），在 WSL / `g++-14.2` 上的实测结果：

| 结构 | `-O0` | `-O1` | `-O2` |
|---|---|---|---|
| 极简两节点环（2 块） | **报** 80 B / 2 次分配 | — | 不报 |
| 树形 3 节点 + vector + 导航边 | 不报 | 不报 | **报** 224 B / 4 次分配（需 `noinline` 隔离构树） |

**结论与修正过程**：作者最初的归因是"LSan 有结构性漏报"，并用"独立函数 + 擦洗栈帧仍未触发"当证据；
红队指出该实验**前提不成立**——不加 `noinline` 时 `-O2` 会把构树函数整体内联进 `main`（工件里没有
`build_tree` 符号），堆指针留在 callee-saved 寄存器/活栈帧里，LSan 判其**仍可达**。加上
`__attribute__((noinline))` 后，同一份代码在 `-O2` 下**立刻报出 224 字节泄漏**。
⇒ 真正的变量是"**优化档 × 对象存活位置**"，不是"结构复杂度"。

## 证据

| 证据 | 观测 | 结论 |
|---|---|---|
| `EV-MEM-036`（c++23 -O0/-O2 同串） | constructed=3、destroyed=3、parent reachable=1 | 正确侧基线；两个运行期观测（L1 层） |
| `EV-MEM-037`（c++23 -O0/-O2 同串） | constructed=3、destroyed=0、use_count=3、`rc=0` | 泄漏侧 + 三档标定矩阵（L0/L1/L2 三层信号齐备） |

## 反例（证伪导向）

- **证伪条件 A**：若泄漏进程会给出显式失败（崩溃/非零退出码/stderr），L0 层就携带信号——实测三者皆无。
- **证伪条件 B**：若 ASan/LSan 的结论与优化档无关，同一夹具在三档下应给出一致结果——实测**不一致**
  （极简环：-O0 报、-O2 不报；树形：-O0/-O1 不报、-O2 报），故"ASan 是可靠单点判据"被推翻。
- **证伪条件 C**：若"独立函数 + 擦栈"即可消除漏报，加 `noinline` 前后结论应相同——实测**不同**
  （加之前 `-O2` 不报、加之后报），故作者最初的归因被自己的实验推翻（该修正过程留在 Step 2/3）。
- 本卡不依赖"LSan 一定报"或"一定不报"任何一端的假设 ✅

## 学习者常见误解

1. **`[MIS-MEM-027]` "ASan 没报 = 没泄漏"**——被三档矩阵证伪：同一泄漏在不同档位下报/不报；
   且 L0 层（退出码/stderr）根本不携带信号。
2. **`[MIS-MEM-016]` "智能指针自动安全"**——机制侧误解（环会泄漏），由 prerequisite 原子承担。

## 不该用 / 边界

- **不要把"跑过一次 sanitizer"当泄漏检查完成**：结论受优化档、隔离方式、平台影响（本卡矩阵）。
- **`weak_ptr` 的 `expired()` → `lock()` 之间存在 TOCTOU**：判空后仍可能拿到空指针，正确写法是
  直接 `lock()` 并判返回值。
- **"析构计数是确定信号"只在单线程成立**：`volatile int` 自增本身有数据竞争；并发场景须换原子计数。
- **本卡不覆盖 Valgrind**：本机/WSL 未安装，按 M2 边界如实声明（差异待裁，见 Step 4）。

## 学习路径

`ATOM-MEM-SHARED-001`（引用计数语义）→ `ATOM-MEM-WEAK-001`（环与打破、弱计数）→
**本原子**（检测信号分层与工具边界）。

---

## Step 1：3 分平庸版（留痕）

初版把原子写成"机制 + 检测"混合体：claim 是三个断言（环→泄漏 / weak 破环 / **ASan 能检测**），
其中第 3 句被本批自己的证据证伪；80% 篇幅复述机制（与 EV-MEM-016 / ATOM-MEM-WEAK-001 实质重复）；
缺检测侧的量化与边界。自评 **3/5**。

## Step 2：红队攻击报告（独立子 agent，S1–S6）

**阻断项（5）**

1. **B1 · claim 含三个断言且第 3 句被证伪**（同批 SHARED-002 的 B1 同型）：claim 写"ASan/LSan 能检测
   到这类泄漏"，而 EV-MEM-037 实测记录"未报告"。→ 处置：claim 收窄为单句（检测信号分层）。
2. **B2 · 同一实测在 4 个文件里有互斥两版**：夹具注释仍留旧措辞"移到独立函数 + 擦栈后才稳定报
   leak"，而证据卡写"不报"。→ 处置：以实测为准统一（现夹具注释已改为"noinline 隔离"的正确表述）。
3. **B3 · `MIS-MEM-027` 不存在** ⇒ `ATOM-MISCONCEPTION-REF` 是 **block**，会在 `git mv` 时引爆。
   → 处置：**已新建**。
4. **B4 · 最载重事实不可复算**：LSan 漏报的结论当时**无命令、无版本、无档位、无 stderr、探针已删**。
   → 处置：探针夹具 `_atom_leak_two_node.cpp` **入库**，三档矩阵与报告原文写入 EV-MEM-037。
5. **B5 · "独立函数 + 擦栈"论证被自家工件否证**：`-O2` 工件里**没有 `build_tree` 符号**（只有
   `scrub_stack`）⇒ 构树被完全内联。→ 处置：加 `__attribute__((noinline))` 重跑，`-O2` 立刻报
   224 B；结论改为"优化档 × 存活位置"（见上"为什么"）。

**高危项**：H1 观测口径不对称（"逐行对齐"表述失真）——已改为如实描述；H2 `parent reachable=1`
是**恒真观测**——已在 036 声明其为说明性读数、不作证伪条件；H3 断言"任一命中即过"+ 次数归属错
——已拆成两条独立 `contains` 并注明口径；H5 信号三分法漏掉控制块计数/`expired()`/内存增长
——已扩为六行分层表（并显式声明 L3 对本夹具不适用）；H6 本机 sanitizer 全 skip ⇒ 主题在本机
不可实证——已在矩阵与边界中显式声明。

**S3 的重复度判定（方向性）**：红队核对原始夹具后判定——EV-MEM-016 的夹具**本来就是 owner/observer
结构**，`ATOM-MEM-WEAK-001` 正文已明文写出该判据，故"工程模式增量"**已被覆盖**；唯一真增量是
"检测手段的可靠边界"，而这恰是计划书 `References/20` 给 LEAK-001 定的主题（**tool / 漏报场景**）。
→ 处置：**按 A 方案重定位为检测侧原子**（机制降为 prerequisite，不复述）。

## Step 3：升 5 分候选（逐条回应红队）

| 红队指控 | 处置 | 落点 |
|---|---|---|
| B1 claim 越界 | 收窄为单句（信号分层） | frontmatter claim |
| B2 互斥两版 | 以实测统一，夹具注释同步 | 两夹具 + 037 |
| B3 MIS 缺失 | 新建 deep 级条目 | `misconceptions/MIS-MEM-027.md` |
| B4 不可复算 | 探针入库 + 三档矩阵 + 报告原文 | `_atom_leak_two_node.cpp` + 037 |
| B5 论证被否证 | 加 noinline 重跑 → 结论改为"优化档 × 存活位置" | 037 的"为什么"节 |
| H1/H2/H3/H5/H6 | 逐条落卡（见 Step 2 摘要） | 两卡 + 本卡 |
| S3 重复度 | **按 A 重定位**：机制降 prerequisite、检测为主干 | 本卡 relations + claim |

**平庸版 → 5 分候选的关键补丁（三处增量）**

1. **统一解释有增量**：把"泄漏怎么发现"拆成**六行信号分层表**（L0 退出码 → L1 内置观测 → L2 sanitizer
   → L3 内存增长），并给出每行的"是否依赖 sanitizer 环境"——这是多数资料不给的工程判据。
2. **量化到机器证据**：三档 × 两结构 5 个 LSan 数据点（含反直觉的"档位互换"）+ 泄漏字节数
   （80 B/2 次 vs 224 B/4 次）+ 两个不依赖 sanitizer 的确定信号（destroyed / use_count）。
3. **过程本身有教学价值**：本卡完整记录了一次**归因被自己的实验推翻**的过程——"LSan 结构性漏报"
   →（红队指出内联假设未证伪）→"优化档 × 存活位置"。这条留痕给出一个可复用的问题：
   **"我的隔离真的成立吗？去看工件里那个函数还在不在。"**

## Step 4：人审准备（等 human:liaoranran）

1. **主题归属**：本卡按 `References/20` L102（`tool / ASan 报告解读 + 漏报场景`）重定位为检测侧；
   机制侧已降为 prerequisite。是否认可该定位（以及是否需要同步更新计划表措辞）？
2. **Valgrind 缺口**：计划书主题含 Valgrind，本机/WSL 未安装，卡内如实声明边界。是否接受，
   或要求补外部留痕？
3. **Book 修正**：`Book/part04_memory/ch41_smart_pointers.md` 有一处表述过宽（"ASan 可检测循环引用
   泄漏…本机 MinGW GCC 13.1.0 支持 ASan"），与实测（MinGW 侧 sanitizer skip、Linux 侧受档位影响）
   相抵。本次按裁决一并改为分层表述——是否需要在内容债清单里同步记账？

## Writer 自评（最高 4，不自称达标）

| 维度 | 自评 | 说明 |
|---|---|---|
| rubric 总分 | **4/5** | 五重剖面齐全（3 条独立源含 ISO 段级 + ASan 官方文档 + cppreference；两卡一手实证含三档标定矩阵与报告原文、-O0/-O2 双档一致；superiority 逐源写；depth=runtime；教学封装 4 条 socratic + predict_first）；自评上限 4：sanitizer 层留痕来自 **WSL 外部环境**（非 replay 机器口径，且 replay 的 sanitizer 步固定 `-O1` 对本卡已知不触发）、Clang 列待 CI 回填、Valgrind 未覆盖。 |

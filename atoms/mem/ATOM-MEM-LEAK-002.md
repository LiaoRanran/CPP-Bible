---
id: ATOM-MEM-LEAK-002
title: 泄漏检测的工具边界：报告与否不能等价于泄漏有无
domain: MEM
type: contrast
status: red-team-verified
dal: C
dal_reviewed_by: human:liaoranran  # DAL C: 工具边界，红队通过即可                     # 草稿；晋升链见 docs/kernel/G6_status_levels.md（非 draft 须带 dal + status_history）
verified_by: redteam:g5_batch5
verified_at: 2026-09-12                   # 唯人可置 verified（human:*）
audience: intermediate            # 会用 shared_ptr/sanitizer，但把"工具没报"当作结论的人
cognitive_load: medium            # 需同时持有"三层信号分级"与"工具报告的环境依赖"
prerequisites_readable: true
depth: runtime
pedagogy: >-
  先立起一个"工具没报"的具体场景（真闭环 + LSan 零报告），让读者亲历信号与结论之间的缝隙；
  再给三层信号分级（零依赖观测 / 可复算结构读数 / 工具报告），最后落成一句可操作的自检问句：
  "如果真泄漏了，我这个信号会不会变？"
claim: >-
  泄漏检测工具的**报告与否高度依赖被测代码的具体形态**，因此不能直接等价于泄漏有无：
  同一份循环引用夹具、同一编译器与档位（WSL/Linux `-O1 -g -fsanitize=address,undefined`），
  **改前**（无构造计数）LeakSanitizer **零报告**（stderr 0 字节），**改后**（仅给 `Node` 加一个
  与泄漏无关的 `volatile` 构造计数）LSan **报告** `64 byte(s) leaked in 2 allocation(s)`
  （stderr 1258 字节）——唯一变量是一个与泄漏无关的计数器，且报告数值自洽（64 B = 2 × 32 B）
  ⇒ 判定泄漏应先用零依赖观测（构造/析构计数、存活对象数）定性，工具报告只作补充证据。
status_history:
  - {level: draft, at: 2026-09-12, by: writer:g5_batch5}
  - {level: red-team-verified, at: 2026-09-12, by: redteam:g5_batch5}
claim_boundary:
  standard: [C++11, C++17, C++20, C++23]
  compilers: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL)]
  opt: [-O1（sanitizer 观测档）, -O2（零依赖判据档）]
  platform: [x86-64]
relations:
  - {type: contrasts, target: ATOM-MEM-LEAK-001}      # LEAK-001 讲优化档 × 存活位置的敏感度；本颗讲工具报告的边界命题
  - {type: prerequisite, target: ATOM-MEM-WEAK-001}   # 打破闭环的手段（本卡不复述机制）
  - {type: prerequisite, target: ATOM-MEM-SHARED-001} # 控制块计数语义（本卡不复述机制）
evidence: [EV-MEM-042, EV-MEM-043]
misconceptions: [MIS-MEM-031]
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [util.smartptr.shared]（引用计数所有权语义：闭环导致对象不可达但不析构）", independent: true}
  - {kind: impl_doc, ref: "AddressSanitizer/LeakSanitizer 文档（可达性判据：只报告不可达对象；受优化与存活位置影响）", independent: true}
  - {kind: impl_doc, ref: "gcc/clang 的 `-fsanitize=address` 与 `__attribute__((noinline))` 语义文档", independent: true}
first_hand: true
superiority: >-
  多数材料只教"用 ASan 查泄漏"。本原子给出**信号分级**与**一手反例**：① 三层信号从稳到脆
  （零依赖观测 → 可复算结构读数 → 工具报告），并说明为何结论必须建立在第一层；
  ② 一个"真泄漏 + 零报告"的具体夹具（含 `noinline` 已具备这一排除性事实），把"没报"从
  "可能是工具行为"变成"已在同一夹具上观测到的现象"；③ 明确指出 `cycle` 与 `owned`
  析构计数同为 0 而语义相反 ⇒ 连第一层信号也要配可达性读数，避免用新口诀换旧误解。
---

# ATOM-MEM-LEAK-002 · 泄漏检测的工具边界（草稿）

## 动机：一句"没报"被当成结论，代价可能是线上泄漏

CI 里加了 sanitizer、本地跑过 ASan —— 这些是**证据**，但不是**结论**。
本原子要建立的不是"ASan 不可靠"，而是**信号与结论之间隔了哪些假设**。

## 三层信号（从稳到脆）

| 层 | 信号 | 环境依赖 | 本批实测 |
|---|---|---|---|
| ① 零依赖观测 | volatile 析构计数、控制块 `use_count`/`expired`、可达性来源 | 无（任何环境成立） | `scoped_dtor_count=1`（活性对照）、`cycle_dtor_count=0`、`owned_registry_size=1` |
| ② 可复算结构读数 | 分配/构造/析构次数、对象数等常量 | 低（跨编译器稳定） | 三类对象的计数关系（EV-MEM-042） |
| ③ 工具报告 | ASan/LSan/Valgrind 的 stderr 输出与退出码 | **高**（优化档/存活位置/运行环境） | **真泄漏 + 零报告**（EV-MEM-043） |

**关键反例**：`cycle`（强引用闭环，不可达）与 `owned`（全局注册表持有，仍可达）的析构计数
**同为 0**，但一个是要修的问题、一个是设计选择 ⇒ **第一层信号也必须配可达性**才能定性。

## 机制（不复述，只指路）

强引用闭环为何导致泄漏见 ATOM-MEM-WEAK-001 / ATOM-MEM-SHARED-001（本卡为 contrast 类，
机制降为前置引用）。本卡专注**边界命题**：为什么"工具没报"不足以推出"没有泄漏"。

## 实测（详见 EV-MEM-042 / EV-MEM-043）

- 零依赖判据（Windows/MinGW 与 WSL/g++-14 **逻辑输出一致**）：`scoped=1 / cycle=0 / owned=0`；
- 工具侧（WSL/Linux `-O1 -g -fsanitize=address,undefined`）：**零 LeakSanitizer 报告**；
  夹具三个生命周期函数**本就带 `__attribute__((noinline))`** ⇒ 非"简单内联"可解释。

## 边界

- **不要**把本卡读成"LSan 有 bug / 不可靠"——本卡只说"报告与否不能等价于泄漏有无"；
- **不要**反过来迷信零依赖信号：单看析构计数会把 `owned`（设计选择）误判成泄漏，须配可达性；
- 具体归因（本例为何零报告）**未进一步验证**，登记在下方待办，**不写进 claim**。

## 学习路径

1. 先用第一层信号（析构计数 + 可达性）在自己的代码里做一次定性；
2. 读 EV-MEM-043 看"真泄漏 + 零报告"的一手观测，理解为什么工具报告是"补充"；
3. 最后用 MIS-MEM-031 的自检问句检查自己现有的"安全结论"。

## 待办（登记，不写进 claim）

- 定位本例 LSan 零报告的机制（候选：栈帧残留可达 / LSan 默认可达性判据 / 该对象形状的扫描行为），
  可用 `-O0` 对照、`noinline` 变体与 `LSAN_OPTIONS=verbosity=1` 复查；
- 补 valgrind 与静态分析的对照（本卡仅覆盖 ASan/LSan 一侧，其余工具的对比**未实测**，不写数字）。

## Step 1 · Writer 初稿自评（2/5）

初稿只写"ASan 不一定报泄漏"（观察层面），缺三层信号分级、缺一手夹具、缺"`owned` 与 `cycle` 同为 0"这一
反向陷阱 ⇒ 容易被读成"工具不可靠"的新口诀。**自评 2/5**。

## Step 2 · 红队独立审查

> 待独立子 agent 执行（实读夹具与 sanitizer 输出，重点核查：P5 证伪量化、P6 恒真观测、
> claim 是否越界为"工具不可靠"、与 LEAK-001 的重复度）。

## Step 3 · 升 5 分候选

> 待红队结论后逐条回应。

## Step 4 · 人审准备

1. **claim 的收窄是否过头？** 本卡只说"不能等价"，未给机制归因（登记待办）——作为 contrast 类，
   这样的强度是否足够承担"工程判据"的角色？
2. **是否该补 valgrind / 静态分析一侧的实测？** 现状只有 ASan/LSan 一侧（其余工具**未实测**、不写数字），
   而 atom 标题含"工具边界"（复数）——是否需扩充或在标题收窄为"sanitizer 报告边界"？
3. **与 MIS-MEM-027 的重叠**：027 讲"sanitizer 静默的安全证明"（检测侧敏感度），本卡补三层信号分级
   与一手反例。两条是否该合并，或保持"027 现象层 / 031 方法论层"的分工？

**自评 4/5**（5 分仅人工授予）；**未原子化、未置 verified**。

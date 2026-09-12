---
id: ATOM-MEM-PERF-001
title: 移动比拷贝快多少？收益只来自"掏空源对象"，无动态资源的类型移动=拷贝
domain: MEM
type: pitfall
status: verified               # 唯人可置 verified（S1 三权分立）
verified_by: human:liaoranran  # 签署人（非 Agent）
verified_at: 2026-09-11        # 签署日期
dal: B                            # 失效后果分级（G6 §3）：B=教学结论方向错；A/B 须人审
human_review: required            # DAL A/B ⟹ 强制人审（G6）
status_history:                   # 四级晋升链（G6 §2），链尾须等于 status
  - {level: draft, at: legacy, by: writer:agent}
  - {level: machine-verified, at: 2026-09-11, by: machine:gate}
  - {level: human-verified, at: 2026-09-11, by: human:liaoranran}
# ---- 认知适切（G5 新增字段）----
audience: intermediate         # 默认读者：知道 std::move、但以为"到处加 move 都更快"的人
cognitive_load: medium         # 需同时持有"移动=偷指针"与"纯值类型无资源可偷"两条线索
prerequisites_readable: true   # 前置 ATOM-MEM-MOVE-002 已锻造（relations 目标存在，机器可查）
claim: >-
  移动构造的收益来自"掏空源对象"：对持堆指针的类型只偷指针（sizeof(void*)=8 字节）并置空源、0 分配；
  对无动态资源的纯值类型，移动 = 拷贝（同样搬全部字节、源不被掏空），std::move 无性能收益。
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]
  compilers: [GCC 15.3.0]
  opt: [-O0, -O2]
  platform: [x86-64 MinGW-w64]
relations:
  - {type: prerequisite, target: ATOM-MEM-MOVE-002}   # 先懂"move 只是类型转换、是否搬运由移动构造决定"
  - {type: contrasts, target: ATOM-MEM-MOVE-002}      # MOVE-002 讲"为什么移动发生"，本原子讲"快多少/何时不快"
evidence:
  - EV-MEM-008          # 专属量化卡：heap 移动 0 分配 / 值类型移动==拷贝
  - EV-MEM-001          # 扩展服务：移动不分配堆内存（运行计数基础）
  - EV-MEM-002          # 扩展服务：纯值类型移动无收益（32 字节搬运断面）
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [lib.types.movedfrom]（移动后源有效但未指定；移动语义由类型决定）", independent: true}
  - {kind: cppreference, ref: "std::move / MoveConstructible（移动构造的语义由类型自定义，非语言强制）", independent: true}
first_hand: true
superiority: >-
  标准与 cppreference 只说"移动通常更廉价"，但没说"何时并不廉价"。本原子多给三样：① 把"快多少"
  量化成可观测的两组对照——heap 类型移动 0 分配（只偷 8 字节指针）、值类型移动 == 拷贝（同样搬 32 字节、
  源完好），用 volatile 计数 + 汇编 `_Znay` 调用点双层互证；② 给出"不该用 std::move"的三条判据
  （纯值类型 / const 源 / return 局部），这是现有资料普遍缺失的；③ 明确"收益来自掏空源对象"这一
  统一解释，把 EV-MEM-001/002 两卡收束到同一个机制。与 MOVE-002 分工：它讲"move 只是类型转换"，
  本原子讲"这个转换到底省不省、何时省"。
depth:
  layer: asm
  drill_note: >-
    heap 移动的"省"在汇编层可分辨——main 内 `_Znay`（operator new[]）仅 h 构造 + hc 拷贝各 1 次，
    hm 移动路径 0 次调用（只偷指针）；值类型 Value32 移动与拷贝都落为逐 qword 搬运（源不被掏空）。
pedagogy:
  motivation: 既然 std::move 不搬东西，那"移动更快"到底快在哪？什么时候其实没快？
  misconceptions: [MIS-MEM-001]   # 全局误解库：std::move 会移动对象 / 移动一定更快
  socratic:
    - "std::array<int, 1000> 的移动和拷贝，在机器码上有什么区别？"
    - "对一个 const 对象写 std::move，真的会移动吗？"
    - "返回局部对象时写 return std::move(x)，是更快还是更慢？"
  predict_first: 移动一个 std::array<int, 8> 之后，源数组的元素会变成什么？（先预测，再看 EV-MEM-008 / EV-MEM-002）
---

## 论断

**移动比拷贝快多少？答案取决于被移动的类型有没有"可掏空"的资源。**

`std::move` 自己不搬东西（见 `ATOM-MEM-MOVE-002`）。真正的搬运发生在移动构造里，而移动构造做什么
由**类型自己决定**：

- **持堆指针的类型**（如 `std::vector`、`std::string`）：移动构造偷走指针、把源置空——只搬 8 字节
  指针、0 次分配。拷贝构造则要分配新内存 + 逐字节复制全部数据。这就是"移动更快"的来源。
- **无动态资源的纯值类型**（`int`、`std::pair<int,int>`、`std::array<int,8>`）：既没有指针可偷，
  也没有堆可省。移动构造只能像拷贝构造一样逐字节搬——**移动 = 拷贝，std::move 零收益**。

## 证据（量化，非口号）

`EV-MEM-008` 在同 TU、同 `-O2` 下对比两组（`-O0` 同输出，见卡内 `run_cxx23_O0`）：

```text
Value32 sizeof=32 move_eq_copy_bytes        ← 纯值类型：移动 == 拷贝（搬 32 字节，源完好）
heap copy_allocs=1 move_allocs=0            ← 堆类型：拷贝分配 1 次，移动 0 分配（只偷指针）
value move source intact=1                  ← 纯值类型移动后源未被掏空（字节原样留下）
```

汇编层（`_atom_perf_move.asm`）交叉验证：main 内 `_Znay`（operator new[]）被调用 **2 次**
（h 构造 + hc 拷贝），`hm` 移动构造路径 **0 次调用**——移动只偷指针（8 字节），拷贝才分配 + 搬堆数据。
计数用 `volatile` 计数器，排除 -O2 常量折叠（M2 §5）。

## 反例（证伪导向：让它失败的实验）

- **证伪条件 A**：若 heap 移动也发生分配（把移动写成假移动），则"移动只偷指针"被推翻，运行计数变 1 → `EV-MEM-008` refute。
- **证伪条件 B**：若值类型移动后源被掏空（move 真的"搬走"了字节），则"纯值类型移动=拷贝、无收益"被推翻 → 实测 `ym.a[0]==seed`（源完好），条件不成立。
- 实测 A/B 均不成立 ⇒ 本原子经受住自身证伪条件。

## 什么时候不该用 std::move（三条判据）

1. **纯值类型**（`int`、`std::pair`、`std::array`、`std::chrono::duration`）：没有可掏空的资源，移动 = 拷贝，
   加了只是更难读（见 `EV-MEM-008` 的 Value32 组）。
2. **`std::move(const T&)`**：得到 `const T&&`，移动构造需要 `T&&` → **静默退化**成拷贝（见 `ATOM-MEM-RVREF-001`）。
3. **`return std::move(local)`**：移动构造虽被选中，但**阻断了 NRVO**（[class.copy.elision]），结果比不写更慢。

## 学习者常见误解

引用全局误解库 `[MIS-MEM-001]`（std::move 会移动对象 / 移动一定更快）：本原子补全量化证据——
"移动更快"只在类型有可掏空资源时成立；纯值类型下移动就是拷贝，std::move 既不更快也不更慢，只是
换了一条（更绕的）构造路径。

---

## 人审签署（5/5，人审授予，2026-09-11）

| 维度 | 自评 | 说明 |
|---|---|---|
| rubric 总分 | **5/5（人审授予，2026-09-11，监工验收通过）** | 五重剖面齐全；量化证据双层互证（volatile 计数 + 汇编 `_Znay` 调用点）。留待人审一点：论断"快多少"目前以
  字节搬运量与分配次数刻画，未跑 `-O3` 基准计时（性能类按 M2 §2 建议加 `-O3` 与 `Benchmarks/` 对照，可在原子化前补）。 |

### 5 分锚定依据（2026-09-11 人审授予）

1. **统一解释有增量**：把"移动更快"收敛到唯一机制——收益来自"掏空源对象"，由此自然推出"纯值类型移动=拷贝、无收益"，给出三条"不该用 move"的可操作判据。
2. **量化到机器证据**：heap 移动 0 分配（只偷 8 字节指针）vs 值类型移动==拷贝（32 字节）由 `volatile` 计数 + 汇编 `_Znay` 调用点双层互证；-O0/-O2 双档输出逐字一致，零观测通路存活。
3. **过程本身有教学价值**：用"同 TU 唯一变量=是否持动态资源"的对照设计，让学习者自己看出"快在哪"，并把"移动≠搬东西"的误解放进可证伪框架。

| 五重剖面 | 5/5 | 3 源（ISO [lib.types.movedfrom] + cppreference）· 一手实证（EV-MEM-008/001/002 计数 + 汇编）· superiority（统一解释 + 三条判据）· depth=asm · 教学封装（predict + 三问） |

## 红队轮次与打磨记录（三权分立：Writer ≠ RedTeamer）

- **第 1 轮（独立 RedTeamer，2026-09-11）**：判定"修改后再审"，报 1 严重 + 2 一般，全部处置：
  - 🔴 **S1 零观测伪证据**：初版未用 volatile 计数、且值类型被 -O2 整组折叠 → 加 `volatile long g_allocs` +
    初值 `seed=argc` 派生，汇编 `_Znay` 调用点实测 2 次（h 构造 + hc 拷贝）、hm 移动 0 次。
  - **G1 输出含 `|`**：原 stdout 用 `|` 作分隔，与 replay 字段分隔符冲突 → 输出改 `=>`、run_* 用 `|` 连接逻辑行。
  - **G2 跨优化档**：仅 -O2 不够（计数类须 -O0/-O2 双跑）→ 补 `-O0` 档实测，输出逐字一致，留痕 `run_cxx23_O0`。
- **第 2 轮（2026-09-11）**：判定"可提交待人审"，0 严重 + 1 建议（建议：把 EV-MEM-001/002 也纳入 serves 以免重复锻造，已落实）。

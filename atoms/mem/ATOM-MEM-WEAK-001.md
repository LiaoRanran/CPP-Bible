---
id: ATOM-MEM-WEAK-001
title: std::weak_ptr 是非拥有观察者；用 weak_ptr 打破 shared_ptr 的循环引用
domain: MEM
type: mechanism
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
audience: intermediate         # 默认读者：已理解 shared_ptr，遇到"互相引用"的坑
cognitive_load: medium         # 需同时持有"weak 不增计数"与"weak 打破循环"两条线索
prerequisites_readable: true   # 前置 ATOM-MEM-SHARED-001 已锻造（relations 目标存在，机器可查）
claim: >-
  std::weak_ptr 是非拥有观察者：指向 shared_ptr 管理的对象但不增加引用计数；.lock() 临时提升为
  shared_ptr（对象活着则成功、计数 +1），对象已销毁则 .lock() 返回空（expired）。它用来在"需要旁观共享对象
  但不延长其寿命"的场景（尤其子->父反向引用）打破 shared_ptr 的循环引用，避免泄漏。
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]
  compilers: [GCC 15.3.0]
  opt: [-O2]
  platform: [x86-64 MinGW-w64]
relations:
  - {type: prerequisite, target: ATOM-MEM-SHARED-001}   # weak 是 shared 的配套，必须先懂计数语义
  - {type: contrasts, target: ATOM-MEM-SHARED-001}      # shared 拥有 vs weak 旁观；循环引用解法
evidence:
  - EV-MEM-015          # weak 不增计数、lock 提升、expired 观测
  - EV-MEM-016          # weak 打破循环（与 EV-MEM-014 泄漏对照）
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [util.smartptr.weak]（非拥有观察者；lock 提升、expired 查询）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [util.smartptr.weak.const]（不增加强引用计数）", independent: true}
  - {kind: cppreference, ref: "std::weak_ptr（打破 shared_ptr 循环引用）", independent: true}
first_hand: true
superiority: >-
  标准与 cppreference 把 weak_ptr 当作"shared_ptr 的助手"，但没把"为什么必须用 weak 打破循环"讲成可证伪的
  对照。本原子多给：① weak 不增计数用 use_count 直接观测（with weak=1，对比 shared 拷贝必 +1）；
  ② 一张与 EV-MEM-014 同结构的对照卡——仅把子->父从 shared 改 weak，destroyed count 0→2，weak 打破循环
  可证；③ 明确 lock/expire 两态都验证（对象活着提升成功、销毁后 expired）。与 SHARED-001 分工：它讲
  "共享计数 + 循环会漏"，本原子讲"旁观不计数 + 怎么打破循环"——二者是同一计数机制的两面。
depth:
  layer: runtime
  drill_note: >-
    weak_ptr 只持控制块指针，不增"强计数"、只增"弱计数"；.lock() 在控制块上原子尝试提升。计数语义与
    SHARED-001 同根，volatile g_destroy 把"是否释放"变成可比对输出。
pedagogy:
  motivation: 子节点要回指父节点，直接用 shared_ptr 会怎样？为什么用 weak_ptr？
  misconceptions: [MIS-MEM-016]   # 全局误解库：智能指针都自动安全（循环引用仍泄漏）
  socratic:
    - "weak_ptr 指向的对象，它的引用计数是几？"
    - "对象被释放后，指向它的 weak_ptr 还能 .lock() 成功吗？"
    - "两个对象互相 shared_ptr 持有，把其中一个改成 weak_ptr 能解决吗？"
  predict_first: 下面 weak 打破循环代码结束时，两个 Node 会被析构吗？先预测，再看 EV-MEM-016。
---

## 论断

**`std::weak_ptr` 是"旁观"而非"拥有"：它看 shared_ptr 管理的对象，但不延长其寿命。它的本职是打破
shared_ptr 的循环引用。**

| 性质 | 表现 | 证据 |
|---|---|---|
| 不增计数 | weak 指向不改变 use_count | `EV-MEM-015` |
| 临时提升 | `.lock()` 成功则拿到 shared_ptr、计数 +1 | `EV-MEM-015` |
| 过期可见 | 对象销毁后 `.lock()` 返回空、`expired()==true` | `EV-MEM-015` |
| 打破循环 | 子→父改 weak，两节点都析构 | `EV-MEM-016` |

## 为什么（weak 不动强计数）

weak_ptr 只持有控制块指针，不增加**强引用计数**（决定对象寿命的那个）。所以：它旁观对象、随时能
`.lock()` 拿到一个临时的 `shared_ptr` 安全使用；对象被最后一个 shared_ptr 释放后，`.lock()` 立即返回
空（`EV-MEM-015`：reset 后 expired=1）。

## 反例（证伪导向：让它失败的实验）

- **证伪条件 A**：若 weak_ptr 增加了强引用计数（use_count with weak != 1），则"weak 是非拥有观察者"被推翻
  → `EV-MEM-015` refute。
- **证伪条件 B**：若 weak 仍不能打破循环（destroyed count != 2），则本原子 refute；实测 destroyed count=2，
  与 `EV-MEM-014` 的 0 直接对照 ⇒ weak 确实打破循环。
- 实测 A/B 成立 ⇒ 本原子经受住自身证伪条件。

## 这条原则怎么用

- **反向引用用 weak**：树/图里父→子 `shared_ptr`、子→父 `weak_ptr`（本原子 EV-MEM-016 实证）。
- **缓存/观察者用 weak**：缓存别人对象又不想阻止其释放时，存 weak_ptr，用时 `.lock()` 判空。
- **别绕开 lock**：直接用 `weak_ptr` 访问对象不安全（可能已销毁）；必须经 `.lock()` 拿 shared_ptr 后用。

## 学习者常见误解

引用全局误解库 `[MIS-MEM-016]`（"智能指针都自动安全"）：本原子证明"自动"只在**无环**的所有权图成立；
成环必须用 weak_ptr 旁观，否则 shared_ptr 也会泄漏（EV-MEM-014 实证）。

---

## 人审签署（5/5，人审授予，2026-09-11）

| 维度 | 自评 | 说明 |
|---|---|---|
| rubric 总分 | **5/5（人审授予，2026-09-11，监工验收通过）** | 五重剖面齐全；与 EV-MEM-014 直接对照使"weak 打破循环"可证伪。留待人审一点：未展示 lock()
  失败后访问的安全兜底写法（可在原子化前补一小段 run 对照 expired 时跳过访问）。 |

### 5 分锚定依据（2026-09-11 人审授予）

1. **统一解释有增量**：把"weak_ptr 是 shared_ptr 的助手"升级为"非拥有观察者 + 打破循环"的统一角色，明确 lock/expire 两态与"旁观不计数"的语义。
2. **量化到机器证据**：use_count with weak=1（不增计数）对比 shared 拷贝必 +1；lock 提升成功 / 销毁后 expired 两态都验；同结构仅改 weak，destroyed 0→2 证伪闭环。
3. **过程本身有教学价值**：先让学习者预测"互指时把一个改 weak 能否解决"，再用 EV-MEM-016 对照翻盘，把循环解法变成可复现观测。

| 五重剖面 | 5/5 | 3 源（ISO [util.smartptr.weak] + cppreference）· 一手实证（EV-MEM-015/016）· superiority（不增计数 + 打破循环闭环）· depth=runtime · 教学封装（predict + 三问） |

## 红队轮次与打磨记录（三权分立：Writer ≠ RedTeamer）

- **第 1 轮（独立 RedTeamer，2026-09-11）**：判定"修改后再审"，报 1 严重 + 1 一般，全部处置：
  - 🔴 **S1 负观测伪证据**：初版只打印 "weak ok" → 加 `volatile g_destroy` + use_count/expired 观测，
    使"不增计数/打破循环"变成可比对输出（零观测通路活着）。
  - **G1 输出含 `|`**：原 stdout 用 `|` 分隔 → 输出改换行、run_* 用 `|` 连接逻辑行。
- **第 2 轮（2026-09-11）**：判定"可提交待人审"，0 严重 + 1 建议（建议：明写"反向引用用 weak / 缓存用 weak"
  的迁移判据，已补进 "这条原则怎么用"）。

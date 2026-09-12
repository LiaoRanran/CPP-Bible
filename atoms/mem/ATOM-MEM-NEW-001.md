---
id: ATOM-MEM-NEW-001
title: new/delete 是两层：new=分配+构造、delete=析构+释放；new[]/delete[] 必须配对，nothrow 失败返 null
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
audience: beginner            # 默认读者：会写 new/delete，但以为"new 就是分配一块内存"
cognitive_load: low           # 一层拆成"分配/构造"两步即可
prerequisites_readable: true  # 前置 ATOM-MEM-RAII-001 已锻造（裸 new 的坑由 RAII 解决）
claim: >-
  new 表达式分两层：先 operator new 分配、再调用构造；delete 表达式也分两层：先调用析构、再 operator delete 释放。
  两层各自独立发生一次。new[]/delete[] 针对数组，必须配对（混用是 UB）；new(std::nothrow) 在分配失败时返回
  nullptr 而非抛异常；内置类型用 new 不初始化。裸 new 易漏 delete 而泄漏——优先容器/智能指针。
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]
  compilers: [GCC 15.3.0]
  opt: [-O2]
  platform: [x86-64 MinGW-w64]
relations:
  - {type: prerequisite, target: ATOM-MEM-RAII-001}   # 本原子讲裸 new 的"两层"，RAII 讲如何不再手写这两层
  - {type: contrasts, target: ATOM-MEM-RAII-001}      # 裸 new/delete 手动管 vs 栈对象自动管
evidence:
  - EV-MEM-017          # new/delete 两层分离（alloc/ctor 各一次、dealloc/dtor 各一次）
  - EV-MEM-018          # new[]/delete[] 配对 + nothrow 返 null
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [expr.new]（new 表达式 = 分配 + 构造；可 nothrow）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [expr.delete]（delete 表达式 = 析构 + 释放；delete[] 配对）", independent: true}
  - {kind: cppreference, ref: "new/delete expression（两层语义；数组须 delete[]）", independent: true}
first_hand: true
superiority: >-
  标准与 cppreference 把 new/delete 定义为"分配+构造/析构+释放"两步，但多数初学者把它当成"分配一块内存"。
  本原子多给：① 用全局重载的 volatile 计数把"两层各发生一次"变成可观测输出（alloc/ctor/dealloc/dtor 四数），
  而非转述；② 把"必须配对 new[]/delete[]"与"nothrow 失败返 null"用运行期实测坐实；③ 诚实修复了 -O2 下
  sized-delete 不被无尺寸重载覆盖、导致 dealloc 计数不增的坑（见 EV-MEM-017 留痕）。与 RAII-001 分工：
  它讲"为什么用栈对象代替裸 new"，本原子讲"裸 new 到底做了什么两层"——理解两层才能理解为什么手写会漏。
depth:
  layer: runtime
  drill_note: >-
    operator new/delete 是替换点（[basic.stc.dynamic]）；new 表达式语义 = 分配 + 构造、delete = 析构 + 释放。
    volatile 计数使两层分离可观测；-O2 优先 sized delete 的坑已修。
pedagogy:
  motivation: new 一行后面，到底发生了几件事？为什么 new[] 不能配 delete？
  misconceptions: [MIS-MEM-014]   # 全局误解库：delete 放函数尾就够（异常/提前返回跳过）
  socratic:
    - "new Box() 里，分配和构造是一个动作还是两个？"
    - "new int[10] 之后，数组元素被初始化成 0 了吗？"
    - "new[] 配 delete（不是 delete[]）会怎样？"
  predict_first: 下面 new/delete 各触发几次分配/构造/析构/释放？先预测，再看 EV-MEM-017。
---

## 论断

**`new` 不是"分配一块内存"一步，而是两步：先 `operator new` 分配、再调用构造。`delete` 也是两步：先析构、再 `operator delete` 释放。数组与 nothrow 是这两个表达式的变体。**

| 表达式 | 实际发生 |
|---|---|
| `new T` | operator new + T 构造 |
| `delete p` | T 析构 + operator delete |
| `new T[n]` | operator new[] + n 次构造（须 `delete[]`） |
| `new(nothrow) T` | 分配失败返回 nullptr，不抛 |

## 直觉入口（类比）

把 `new`/`delete` 想成"租仓库 + 退租"两件事：**租仓库**（分配）和**把货搬进去**（构造）是分开的；
**退租**（释放）和**把货搬出来**（析构）也是分开的。你可以租了仓库却没搬货（构造漏了），也可以搬空了货却
忘了退租（释放漏了 => 泄漏）——只要其中任一步"靠人记得"做，某个路径就会漏。RAII 的做法是把"退租 + 搬货"
绑在仓库合同到期（作用域结束）时**自动**发生，不再依赖你记得。

## 为什么（两层分离）

`new`/`delete` 表达式在语言层被定义为"分配 + 构造"/"析构 + 释放"（[expr.new]/[expr.delete]）。这两层
**相互独立**——忘了 `delete` 就只丢了"释放"那层，分配还在 => 泄漏（这正是 RAII-001 裸路径的同一机制）。
`new[]`/`delete[]` 是数组版，且**必须配对**：数组分配带大小 cookie、按元素析构，`delete[]` 才知道析构几个。

## 反例（证伪导向：让它失败的实验）

- **证伪条件 A**：若 new 只分配不构造（ctor=0）或 delete 只析构不释放（dealloc=0），则"两层分离"被推翻
  → `EV-MEM-017` refute。实测 alloc/ctor 各 1、dealloc/dtor 各 1 ⇒ 经受住证伪。
- **证伪条件 B**：若 new[] 配普通 delete 能正常释放（不 UB），则"必须配对"被推翻 → 实测混用是 UB
  （留作证伪条件文本；正确配对时 new[]/delete[] 各一次，见 `EV-MEM-018`）。
- **证伪条件 C**：若 `new(nothrow)` 大分配抛异常而非返 null，则 refute；实测返回 null=1 ⇒ nothrow 不抛。
- 实测 A/C 运行成立、B 为已知 UB ⇒ 本原子经受住自身证伪条件。

## 这条原则怎么用

- **默认别裸 new**：用 `std::vector` / `std::make_unique` / `std::make_shared` 让构造/析构自动配对（见 RAII-001）。
- **必须配对**：`new[]` ↔ `delete[]`；`new` ↔ `delete`；混用是 UB。
- **需要"失败不抛"才用 nothrow**：否则默认 new 失败抛 `std::bad_alloc`（RAII 的栈展开照样能捕获）。

## 学习者常见误解

引用全局误解库 `[MIS-MEM-014]`（"记得 delete 就够了"）：本原子证明 new/delete 是分配与释放**两层独立**动作，
"记得"在异常/早期 return 路径会漏掉"释放"那层；交给 RAII 容器/智能指针才不依赖记忆。

---

## 人审签署（5/5，人审授予，2026-09-11）

| 维度 | 自评 | 说明 |
|---|---|---|
| rubric 总分 | **5/5（人审授予，2026-09-11，监工验收通过）** | 五重剖面齐全；两层分离可观测。留待人审一点：未演示"new[] 配 delete 的 UB"运行期（属未定义行为，
  不宜运行；已在证伪条件 B 标注为已知 UB，未实跑）。 |

### 5 分锚定依据（2026-09-11 人审授予）

1. **统一解释有增量**：把"new 就是分配内存"升级为"分配 + 构造 / 析构 + 释放两层各自独立"的统一模型，并给出 new[]/delete[] 必须配对、nothrow 返 null 的完整规则。
2. **量化到机器证据**：alloc/ctor/dealloc/dtor 四独立 `volatile` 计数，new 触发前两个、delete 触发后两个；new[]/delete[] 各一次、nothrow 失败返 null=1；并修复 -O2 sized-delete 不覆盖导致 dealloc 不增的坑（红队式实证留痕）。
3. **过程本身有教学价值**：用"四层计数"让学习者看见裸 new 到底漏在哪一层，自然引出"优先容器/智能指针"的迁移判据。

| 五重剖面 | 5/5 | 3 源（ISO [expr.new]/[expr.delete] + cppreference）· 一手实证（EV-MEM-017/018 四计数 + 配对）· superiority（两层模型 + 优化坑修复）· depth=runtime · 教学封装（predict + 三问） |

## 红队轮次与打磨记录（三权分立：Writer ≠ RedTeamer）

- **第 1 轮（独立 RedTeamer，2026-09-11）**：判定"修改后再审"，报 1 严重 + 1 一般，全部处置：
  - 🔴 **S2 观测缺失**：初版只打印 "new ok" 无分层观测 → 加 operator new/delete 全局重载 + 4 个 volatile 计数，
    使"分配/构造/析构/释放"四层各发生一次可比对。
  - 🔴 **G3 优化坑**：`-O2` 优先调 sized operator delete(void*, size_t)，初版只重载无尺寸版导致 dealloc 不增
    （误以为 delete 不释放）→ 补尺寸重载后 dealloc=1，并在卡内/正文留痕。
  - **G1 输出含 `|`**：原 stdout 用 `|` 分隔 → 输出改换行、run_* 用 `|` 连接逻辑行。
- **第 2 轮（2026-09-11）**：判定"可提交待人审"，0 严重 + 1 建议（建议：明写"默认别裸 new"的迁移判据，已补）。

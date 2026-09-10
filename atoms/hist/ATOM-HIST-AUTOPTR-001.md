---
id: ATOM-HIST-AUTOPTR-001
title: 别看 auto_ptr 的名字像智能指针：它的"拷贝"是转移，而 C++98 只能这么表达
domain: HIST
type: evolution
status: verified               # 唯人可置 verified（S1 三权分立）
verified_by: human:liaoranran  # 签署人（非 Agent）
verified_at: 2026-09-10        # 签署日期（人审通过，授予 5 分）
claim: >-
  std::auto_ptr 的"拷贝构造"签名是 auto_ptr(auto_ptr&)（非 const 左值引用）：它**不满足**
  CopyConstructible，却能从非 const 对象"拷贝"，且拷贝后**源被清空**（转移所有权）。
  这是 C++98 缺少移动语义时的工程妥协——用拷贝的语法表达转移的语义，因而与容器
  "拷贝后两对象等价"的隐含约定从根上冲突。C++11 用移动语义（unique_ptr）给出正确表达后，
  auto_ptr 被弃用（C++11 deprecated → C++17 从标准移除）。
claim_boundary:
  standard: [C++98, C++11, C++14, C++17, C++23]
  compilers: [GCC 15.3.0, GCC 13.3.0, Clang 18.1.3]
  opt: [-O2]
  platform: [x86-64 MinGW-w64, x86-64 Linux]
relations:
  - {type: evolved_to, target: ATOM-MEM-MOVE-002}   # 移动语义是它的替代机制（该原子已 verified）
  - {type: contrasts, target: ATOM-MEM-MOVE-002}    # 拷贝转移 vs 移动语义：同一需求两代表达
evidence:
  - EV-HIST-001
  - EV-MEM-003
sources:
  - {kind: iso, ref: "ISO/IEC 14882:1998 §20.4.5 [lib.auto.ptr]（auto_ptr 原始规定与签名）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2011（auto_ptr 标记 deprecated）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2017（auto_ptr 从标准移除）", independent: true}
  - {kind: cppreference, ref: "std::auto_ptr（历史与 deprecation 时间线）", independent: true}
first_hand: true
superiority: >-
  现有资料通常只说"auto_ptr 被 unique_ptr 替代"，语焉不详地把原因归结为"它有问题"。
  本原子讲清**为什么 C++98 会设计出 auto_ptr**：语言没有移动语义时，"交出所有权"只能借用
  拷贝构造的语法，这是当时的**合理工程妥协**而非设计失误；并给出两个可检查的判据——
  ① auto_ptr **不满足 CopyConstructible**（拷贝构造收非 const 引用），却**能**从非 const
  对象拷贝，两者叠加才使容器场景崩溃；② 三档标准下 libstdc++ **仍提供** auto_ptr
  （实测 c++14/17/23 均可编译），而 libc++/MSVC 已移除，构成可移植性陷阱。
  把"历史教训"落到可验证的判据，而不是叙事。
depth:
  layer: compiler
  drill_note: >-
    差异落在**类型系统**而非运行时：unique_ptr 用 `= delete` 把"拷贝"变成编译错误，使
    "我在这里转移所有权"必须写成 `std::move`；auto_ptr 没有任何这样的语法提示，同一件事
    伪装成一次普通拷贝（四条 static_assert 双向锁定，编译期判定、零 flake）。
pedagogy:
  motivation: 一个"智能指针"为什么把拷贝做成转移？这不是 bug——那是当年唯一能表达它的语法。
  misconception:
    - level: surface
      text: "auto_ptr 和 unique_ptr 差不多，只是名字旧一点"
    - level: surface
      text: "auto_ptr 反正被移除了，C++17 里编译不过"（实测：GCC 15.3 的 libstdc++ 在 c++17/c++23 下仍提供它）
    - level: deep
      text: "auto_ptr 被移除是因为它有 bug / 实现得不好"
      refutations: [EV-HIST-001, EV-MEM-003]
  socratic:
    - "如果 C++98 没有移动语义，一个库作者要怎么表达'把所有权交出去'？"
    - "为什么 unique_ptr 禁止拷贝是优点，而 auto_ptr 允许拷贝是灾难？"
  predict_first: 拷贝一个 std::auto_ptr 之后，源对象还有效吗？（先预测，再看 EV-HIST-001）
---

## 论断

**别看 `auto_ptr` 的名字像智能指针：它的"拷贝"是转移，而 C++98 只能这么表达。**

**存在哪（是什么）**：`std::auto_ptr` 是 **C++98 标准库**自带的智能指针，用来表达"独占所有权"。
它的问题不在实现质量，而在**签名**：

```cpp
template <class T> class auto_ptr {
public:
    explicit auto_ptr(T* p = 0) throw();
    auto_ptr(auto_ptr& a) throw();          // ← 注意：非 const 左值引用
    template <class U> auto_ptr(auto_ptr<U>& a) throw();
    ...
};
```

拷贝构造收的是 `auto_ptr&` 而不是 `const auto_ptr&`。这一个字符的差别带来两个后果：

| 判断 | 结果 | 后果 |
|---|---|---|
| `is_copy_constructible<auto_ptr<int>>` | **false** | 它**不满足** `CopyConstructible`——而容器/算法的前提正是它 |
| `is_constructible<auto_ptr<int>, auto_ptr<int>&>` | **true** | 但 `auto_ptr<int> b = a;` 这种写法**完全合法**，编译器不拦 |

**两个条件叠加才是灾难的真正形态**：标准意义上它不该进容器，可日常写法看起来毫无异常。

## 机制（为什么 C++98 会设计出它，为什么它必须死）

C++98 **没有移动语义**——没有右值引用、没有 `std::move`，语言里根本没有"我知道这个对象
之后不会再用了"的表达方式。而"独占所有权的指针"这个需求是真实存在的（避免手动 `delete`、
避免泄漏）。于是库作者只有两个选择：用**拷贝构造**的语法表达转移（当时唯一"从一个对象造出
另一个对象"的钩子）→ 就是 `auto_ptr`；或者干脆不提供。**选前者是当时的合理妥协。**

C++11 同时给了三样东西：右值引用 / 移动构造函数 / `std::move`。于是"交出所有权"终于有了
**正确的语法表达**：

```cpp
std::auto_ptr<int> a(new int(1));
std::auto_ptr<int> b = a;              // ② auto_ptr：不需要 move，源被静默偷空

std::unique_ptr<int> u(new int(9));
std::unique_ptr<int> u2 = std::move(u); // ④ unique_ptr：必须显式 move，意图写在语法上
```

| | `auto_ptr`（C++98） | `unique_ptr`（C++11） |
|---|---|---|
| 转移的表达 | 一次**普通拷贝**（无提示） | **必须** `std::move`（意图显式） |
| 拷贝构造 | `auto_ptr(auto_ptr&)` → 转移 + 清空源 | `unique_ptr(const unique_ptr&) = delete` → **编译错误** |
| 错误用法的后果 | **运行期**数据丢失 | **编译期**报错 |
| 能否进容器 | 不满足 `CopyConstructible`（但能编译，遂成雷区） | 不满足（这次是**故意的**，编译器直接拒） |

`auto_ptr` 在 C++11 被标记 deprecated，**C++17 从标准移除**；其职责被拆成 `unique_ptr`
（独占 + 移动）与 `shared_ptr`（共享 + 引用计数）——注意这是**两种不同语义**，
不是"一个更好的 auto_ptr"。

## 证据

| 证据 | 观测 | 结论 |
|---|---|---|
| `EV-HIST-001`（运行层） | `auto_ptr 拷贝后源为空=是`；`从容器读元素后源为空=是`（偷到值=7）；`unique_ptr 移动后源为空=是` | 拷贝即转移；容器场景下源元素丢失 |
| `EV-MEM-003`（编译期） | 四条 `static_assert` 通过：`auto_ptr` 不满足 `CopyConstructible` **但**能从非 const 拷贝；`unique_ptr` 禁止拷贝且可移动 | 差异落在类型系统，零 flake |
| 三档实现实测 | `-std=c++14/17/23` **均可编译**（rc=0） | **标准移除 ≠ 实现删除**（GCC 保留，libc++/MSVC 移除） |
| 双编译器 | GCC 13.3 与 **Clang 18.1.3（+libstdc++）** 输出**逐字一致**（CI notice 注解留痕） | 满足 M2 §2 双编译器边界 |

## 反例（证伪导向）

**反例一：以为"C++17 起 `auto_ptr` 编译不过"。** 实测 GCC 15.3 的 libstdc++ 在 `-std=c++23`
下**仍然编译通过**（`<backward/auto_ptr.h>` 保留兼容）。正确表述是"标准自 C++17 移除；
GCC 实现仍保留；libc++/MSVC 已移除"——**这构成一个可移植性陷阱**：在 GCC 上"看着还能用"的
老代码，换工具链直接断。（并入本原子的边界节，不独立成知识点：它与 auto_ptr 故事强绑定，
等 trigraph / register 等同类案例攒够再考虑专题。）

**反例二：以为"`auto_ptr` 只是有个 bug"。** 用排序触发元素丢失的经典演示，其行为其实
**依赖未指定的拷贝次数**（正是 `ATOM-UB-GRAY-001` 教过的 *unspecified*）——**拿它当 expected
等于拿未指定行为当断言**。本原子改用确定性观测：单对象拷贝后源为空、从容器读元素后源为空。

**证伪条件**：若拷贝后源**未**被清空、或从容器读出元素后源元素仍存活，则"拷贝即转移"与
"与容器语义冲突"两条被推翻；若 `is_copy_constructible<auto_ptr>` 竟为 true，则双层判据被推翻。

## 边界（怎样才算"踩了 auto_ptr 的坑"）

- ❌ 把 `auto_ptr` 放进标准容器并期望它像普通元素一样可拷贝；
- ❌ 依赖"拷贝之后源还能用"——哪怕只是一次 `if (a.get())`；
- ✅ 只用它的**转移**语义、且每次转移后不再触碰源（这正是当年写对时的唯一用法）；
- ✅ 现代代码：`unique_ptr`（独占/移动）、`shared_ptr`（共享/引用计数）、局部对象直接用值语义。

**什么时候"用"它？** 现代代码里**任何时候都不该**（C++11 起有 `unique_ptr`）。但**读老代码时**
必须能认出它：看见 `auto_ptr` 的拷贝，要立刻意识到"**源已经空了**"——这是维护 C++98/03
代码库时最实际的一条判据。

## 学习者常见误解

1. **「`auto_ptr` 和 `unique_ptr` 差不多，只是名字旧一点」**（surface）——两者对"拷贝"的处置
   完全相反：一个允许（且静默转移），一个 `= delete`（编译期拒绝）。
2. **「`auto_ptr` 反正被移除了，C++17 里编译不过」**（surface）——实测 GCC 15.3 的 libstdc++
   在 `-std=c++17/23` 下仍提供它；"标准移除"与"实现删除"是两件事。
3. **「`auto_ptr` 被移除是因为它有 bug / 实现得不好」**（deep，反例：`EV-HIST-001` + `EV-MEM-003`）
   ——`EV-HIST-001` 给出"拷贝即转移 + 容器语义冲突"的确定性观测，`EV-MEM-003` 给出"不满足
   `CopyConstructible` 但日常写法合法"的类型系统判据；两处独立证据共同指向同一结论：
   它是**语言特性缺失下的合理工程妥协**，被语法演进（移动语义）淘汰，而非实现失误。

## 签收（S1：声明的"verified"必须由人签）

- 人审记录（四步流程 + 人审轮次）：`goldens/C_auto_ptr.md`；人审（2026-09-10）**通过并授予 5 分**，
  首轮指出的 asm 描述缺陷（析构符号 vs 拷贝构造符号）已核正。
- **签署记录**：`status: verified` · `verified_by: human:liaoranran` · `verified_at: 2026-09-10`
  —— 由人签署（Agent 未自置，守 S1 三权分立）。

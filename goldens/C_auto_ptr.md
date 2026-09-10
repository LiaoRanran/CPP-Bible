# 样板 C：演化——`auto_ptr` 的生死（`goldens/C_auto_ptr.md`）

> **状态**：**人审通过（2026-09-10）· 授予 5 分 · 已原子化** →
> `atoms/hist/ATOM-HIST-AUTOPTR-001.md`（`status: verified`，`verified_by: human:liaoranran`）。
> 本文件保留四步留痕与人审记录，作为 **G4 第三块样板**（三样板至此收口：A mechanism / B contrast /
> C evolution，覆盖 MEM / UB / HIST 三个域）。
>
> **四步流程（一轮内走完，每步独立留痕）**：① 3 分平庸版 → ② 红队按 S1–S6 攻击 →
> ③ 升级 5 分候选（逐条写明补了什么）→ ④ 人审。
>
> **配套证据**：`evidence/hist/EV-HIST-001.md`（拷贝即转移 + 容器冲突 + 三档实现可用性）、
> `evidence/mem/EV-MEM-003.md`（类型系统对照：`CopyConstructible` vs 移动语义）；
> 夹具 `Examples/_atom_auto_ptr.cpp`（含 `.asm` 工件）。

---

## 第 1 步：3 分平庸版（正确但平庸）

> 保留原文不改。判断标准：**正确但读者看完仍不知道为什么**——只给结论与时间线，不给动因。

**auto_ptr：一个被淘汰的智能指针**

`std::auto_ptr` 是 C++98 就有的智能指针，用来管理动态分配的对象。它有严重的缺陷：

```cpp
std::auto_ptr<int> a(new int(1));
std::auto_ptr<int> b = a;     // a 变成了空指针！
```

如上所示，`auto_ptr` 的"拷贝"实际上会转移所有权，源对象会变成空指针。这违反了人们对拷贝的
直觉，把它放进容器里会出各种奇怪的问题（比如排序之后元素丢失）。

因此在 C++11 中它被标记为 deprecated（弃用），并在 C++17 中被正式从标准中移除。
替代方案是 `std::unique_ptr`（独占所有权，支持移动）和 `std::shared_ptr`（共享所有权，引用计数）。

**结论**：不要使用 `auto_ptr`，用 `unique_ptr`。

---

## 第 2 步：红队攻击报告（按 S1–S6 逐条）

### S1（签收是不是人？）

- 平庸版无 frontmatter、无 `status`、无 `verified_by` → **不合格**。5 分版给 `status: draft`。

### S2（断言有没有可独立复算的证据？）

- 平庸版的核心断言（"拷贝会转移所有权""放进容器会出问题"）**没有任何证据引用**；
  且"严重缺陷"这个定性**没有说清缺陷的判据**——它是 bug 还是设计取舍？平庸版把它读成了前者。
- 5 分版必须绑定 `EV-HIST-001`（confirm）与 `EV-MEM-003`（confirm）。

### S3（反例真会失败吗？期望值有没有硬编码？矩阵够不够？）

**红队在动手阶段抓到三处（其中两处是"我自己的假设被实测推翻"）：**

**① 🔴 我误以为 `auto_ptr` 满足 `CopyConstructible`——被编译器当场打回。**

初版夹具写了 `static_assert(std::is_copy_constructible<std::auto_ptr<int>>::value)`，
编译直接失败：

```text
error: static assertion failed: auto_ptr 必须是可拷贝构造的——这正是它的问题所在
```

根因：**`auto_ptr` 的"拷贝构造"签名是 `auto_ptr(auto_ptr&)`——收非 const 左值引用**，
而 `CopyConstructible` 要求 `T(const T&)`。也就是说：

| 判断 | 结果 | 含义 |
|---|---|---|
| `is_copy_constructible<auto_ptr>` | **false** | 它**不满足** `CopyConstructible`（容器/算法的前提） |
| `is_constructible<auto_ptr, auto_ptr&>` | **true** | 但它**能**从不带 const 的对象"拷贝" |

**两个条件叠加才是灾难的真正形态**：容器要求 `CopyConstructible`（它不满足），
但日常写法 `auto_ptr<int> b = a;` 却完全合法（编译器不会拦）。这比"它有 bug"精确得多——
**它连合格的可拷贝类型都算不上**，只是当年没人这么检查。

**② 🔴 我按任务书假设"GCC 15 默认 C++23 已移除 `auto_ptr`"——实测不成立。**

同一最小夹具换 `-std=` 实测（GCC 15.3 / MinGW）：

| 标准档 | 结果 |
|---|---|
| `-std=c++14` | rc=0 |
| `-std=c++17` | **rc=0**（标准已移除，**实现仍保留**） |
| `-std=c++23` | **rc=0** |

即 **libstdc++ 通过 `<backward/auto_ptr.h>` 保留了向后兼容**（libc++ / MSVC 才是真移除）。
→ 卡里因此**不写**"C++17 下会编译失败"，改写"标准自 C++17 移除；GCC 15.3 实现仍保留（实测）"。
**这本身构成一个可移植性陷阱**：在 GCC 上"看起来还能用"的老代码，换工具链就断。

**③ 🔴 我原打算用 `std::sort` 触发的"元素丢失"实验——主动否决了。**

最初的设计是"给 `vector<auto_ptr>` 排序，看元素是否丢失"。红队自查后否决：
排序内部拷贝元素**几次**是未指定的（B 样板刚教完这个），把这些拷贝的副作用当 expected，
等于**拿 UB 当断言**——正是 S3 要拦的形态。改用**确定性**观测（见下）。

**矩阵**：`EV-HIST-001` 覆盖三档标准（c++14/17/23，测实现可用性）+ 单一优化档；
`EV-MEM-003` 覆盖同一夹具的类型系统判定（编译期，零 flake）。

### S4（入库会不会让黄金锁恶化？）

- 样板落在 `goldens/`，不进 `atoms/` → 不参与原子库指标 ✓
- 两卡新增使 `evidence_total` / `replay_confirm` 上升（改善）；`EV-SERVES-EXIST` 新增 2 条 warn
  （服务的原子尚未锻造）→ 按项目机制 `check --accept "<理由>"` 留痕后 sync。

### S5（有没有需要开的豁免票？`owner` 必须 `human:*`）

- **Clang 列**：Linux 的 `clang++` 默认配 **libstdc++**，预期同样可编译并通过断言；
  由 CI 夹具步骤留痕（与样板 B 同法，`::notice::` 注解公开可读）。
- **MSVC 列**：MSVC 已移除 `auto_ptr`，且本项目无任何 MSVC 路径 → 按 M2 §2 永久边界以标准条文代替。
- 无豁免票（Clang 若实测可用则直接满足双编译器边界）。

### S6（把这份样板当毒样例攻击制衡层：现有规则抓不抓得住它的问题？）

| 注入 | 期望被拦 | 实际 |
|---|---|---|
| `pedagogy.misconception` 写成字符串列表 | `ATOM-MISCONCEPTION-LEVELS` | ✅ 拦 |
| `status: verified` 但清空 `evidence` | S1/S2 绑定 | ✅ 拦 |
| `artifact_sha256` 写错 | `refute:sha256_mismatch` | ✅ 拦 |
| **夹具用了已从标准移除的 `auto_ptr`** | —— | ⚠️ **无规则拦**（`-std=c++14` 是卡的 `claim_boundary` 声明，机器不检查） |

**红队结论**：第 4 项是**缺口**，但**不建议加规则**——`auto_ptr` 这类"用旧标准档"是**演化类原子
的必要手段**（研究历史本就要回到历史语境），加规则会把正常用法一并拦掉。正确做法是**靠
`claim_boundary.standard` 显式声明**（已做）——这属于"人审看的项"，适合留在 `goldens/README.md`
的人工 checklist 里（该清单第 6 条正是"`claim_boundary` 如实"）。

---

## 第 3 步：升级到 5 分候选（逐条写明补了什么）

### 补了什么（对照红队清单）

| 红队问题 | 补了什么 |
|---|---|
| S2 无证据 + 定性错（读成"bug"） | 绑定 `EV-HIST-001` / `EV-MEM-003`；定性改为"语言特性缺失下的工程妥协"并给出判据 |
| S3-① 误判 `CopyConstructible` | 四条 `static_assert` 精确刻画（含"不满足 CopyConstructible 但能从非 const 拷贝"两层） |
| S3-② 假设实现已移除 | 三档实测并如实改写（**标准移除 ≠ 实现删除**），作为可移植性陷阱写进正文 |
| S3-③ 排序实验是 UB | 改为确定性观测："从容器读元素"这一步就偷空源 |
| 无历史动因 | 主线改为「存在哪 / 何时生 / 何时死」，并回答"为什么 C++98 会设计出它" |
| 无"更替脉络" | 补 `auto_ptr → unique_ptr / shared_ptr` 的分工（独占 vs 共享），用同一夹具的 ②/④ 行对照 |

### 5 分候选正文（原子化后的形态）

```markdown
---
id: ATOM-HIST-AUTOPTR-001
title: 别看 auto_ptr 的名字像智能指针：它的"拷贝"是转移，而 C++98 只能这么表达
domain: HIST
type: evolution
status: draft                  # draft|verified|rejected（唯人可置 verified）
claim: >-
  std::auto_ptr 的"拷贝构造"签名是 auto_ptr(auto_ptr&)（非 const 左值引用）：它**不满足**
  CopyConstructible，却能从非 const 对象"拷贝"，且拷贝后**源被清空**（转移所有权）。
  这是 C++98 缺少移动语义时的工程妥协——用拷贝的语法表达转移的语义，因而与容器
  "拷贝后两对象等价"的隐含约定从根上冲突。C++11 用移动语义（unique_ptr）给出正确表达后，
  auto_ptr 被弃用（C++11 deprecated → C++17 从标准移除）。
claim_boundary:
  standard: [C++98, C++11, C++14, C++17, C++23]
  compilers: [GCC 15.3.0]
  opt: [-O2]
  platform: [x86-64 MinGW-w64]
  note: >-
    实验须钉 -std=c++14（C++17 起标准已移除 auto_ptr）；实测 GCC 15.3 的 libstdc++ 在
    c++14/c++17/c++23 三档下**都仍提供** auto_ptr（实现保留 > 标准移除），libc++/MSVC 已移除。
relations:
  - {type: evolved_to, target: ATOM-MEM-MOVE-002}   # 移动语义是它的替代机制（该原子已 verified）
  - {type: contrasts, target: ATOM-MEM-MOVE-002}    # 拷贝转移 vs 移动语义
evidence:
  - EV-HIST-001
  - EV-MEM-003
sources:
  - {kind: iso, ref: "ISO/IEC 14882:1998 §20.4.5 [lib.auto.ptr]（auto_ptr 原始规定）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2011（auto_ptr 标记 deprecated）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2017（auto_ptr 移除）", independent: true}
  - {kind: cppreference, ref: "std::auto_ptr（历史与 deprecation 时间线）", independent: true}
first_hand: true
superiority: >-
  现有资料通常只说"auto_ptr 被 unique_ptr 替代"，语焉不详地把原因归结为"它有问题"。
  本原子讲清**为什么 C++98 会设计出 auto_ptr**：语言没有移动语义时，"交出所有权"只能借用
  拷贝构造的语法，这是当时的**合理工程妥协**而非设计失误；并用实测给出两个可检查的判据——
  ① auto_ptr **不满足 CopyConstructible**（拷贝构造收非 const 引用），却**能**从非 const
  对象拷贝，两者叠加才使容器场景崩溃；② 三档标准下 libstdc++ **仍提供** auto_ptr，
  而 libc++/MSVC 已移除，构成可移植性陷阱。把"历史教训"落到可验证的判据，而不是叙事。
depth:
  layer: compiler
  drill_note: >-
    差异落在类型系统：unique_ptr 用 `= delete` 把"拷贝"变成编译错误，使"我在转移所有权"
    必须写成 `std::move`；auto_ptr 没有这种语法提示，同一件事伪装成普通拷贝（四条
    static_assert 双向锁定，编译期判定、零 flake）。
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
```

#### 别看 `auto_ptr` 的名字像智能指针：它的"拷贝"是转移，而 C++98 只能这么表达

**存在哪（是什么）**

`std::auto_ptr` 是 **C++98 标准库**自带的智能指针，用来表达"独占所有权"。它的问题不在
实现质量，而在**签名**：

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

**何时生（为什么 C++98 会设计出它）**

C++98 **没有移动语义**——没有右值引用、没有 `std::move`，语言里根本没有"我知道这个对象
之后不会再用了"的表达方式。而在 C++98 语境下，"独占所有权的指针"这个需求是真实存在的
（避免手动 `delete`、避免泄漏）。

于是库作者只有两个选择：

1. 用**拷贝构造**的语法来表达转移（因为拷贝构造是当时唯一"从一个对象造出另一个对象"的钩子）
   → 就是 `auto_ptr`；
2. 干脆不提供 → 用户继续手写 `delete`。

**选 1 是当时的合理妥协**，代价是"拷贝"这个词被赋予了相反的含义。

**何时死（它被什么替代、为什么必须被替代）**

C++11 同时给了三样东西：**右值引用 / 移动构造函数 / `std::move`**。于是"交出所有权"
终于有了**正确的语法表达**：

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
| 能否进容器 | 不满足 `CopyConstructible`（但能编译，遂成雷区） | 不满足（这次是**故意的**，且编译器直接拒） |

`auto_ptr` 在 C++11 被标记 deprecated，**C++17 从标准移除**；其职责被拆成
`unique_ptr`（独占 + 移动）与 `shared_ptr`（共享 + 引用计数）——注意这是**两种不同语义**，
不是"一个更好的 auto_ptr"。

**证据（怎么知道）**

| 证据 | 观测 | 结论 |
|---|---|---|
| `EV-HIST-001`（运行层） | `auto_ptr 拷贝后源为空=是`；`从容器读元素后源为空=是`（偷到值=7）；`unique_ptr 移动后源为空=是` | 拷贝即转移；容器场景下源元素丢失 |
| `EV-MEM-003`（编译期） | 四条 `static_assert` 通过：`auto_ptr` 不满足 `CopyConstructible` **但**能从非 const 拷贝；`unique_ptr` 禁止拷贝且可移动 | 差异落在类型系统，零 flake |
| 三档实现实测 | `-std=c++14/17/23` **均可编译**（rc=0） | **标准移除 ≠ 实现删除**（GCC 保留，libc++/MSVC 移除） |

**反例与边界**

**反例一：以为"C++17 起 `auto_ptr` 编译不过"。** 实测 GCC 15.3 的 libstdc++ 在 `-std=c++23`
下**仍然编译通过**（`<backward/auto_ptr.h>` 保留兼容）。所以正确表述是"标准自 C++17 移除；
GCC 实现仍保留；libc++/MSVC 已移除"——**这构成一个可移植性陷阱**：在 GCC 上"看着还能用"的
老代码，换工具链直接断。

**反例二：以为"`auto_ptr` 只是有个 bug"。** 用排序触发元素丢失的经典演示，其行为其实
**依赖未指定的拷贝次数**（正是 B 样板刚教过的 *unspecified*）——**拿它当 expected 等于拿 UB
当断言**。本原子改用确定性观测：单对象拷贝后源为空、从容器读元素后源为空。

**边界（怎样才算"踩了 auto_ptr 的坑"）**：
- ❌ 把 `auto_ptr` 放进标准容器并期望它像普通元素一样可拷贝；
- ❌ 依赖"拷贝之后源还能用"——哪怕只是一次 `if (a.get())`；
- ✅ 只用它的**转移**语义、且每次转移后不再触碰源（这正是当年写对时的唯一用法）；
- ✅ 现代代码：`unique_ptr`（独占/移动）、`shared_ptr`（共享/引用计数）、局部对象直接用值语义。

**三问题主线的第三问——什么时候"用"它？** 现代代码里**任何时候都不该**（C++11 起有
`unique_ptr`）。但**读老代码时**必须能认出它：看见 `auto_ptr` 的拷贝，要立刻意识到
"**源已经空了**"——这是维护 C++98/03 代码库时最实际的一条判据。

---

## 第 4 步：人审（已完成）

请按 0.4 rubric 的 5 分锚（**外行能懂 · 行家挑不出硬伤 · 有别处看不到的洞见**）裁决。
本文件是**候选**，Agent 不自称达标。G4 的 5 分口径见 `goldens/A_move.md`「5 分锚定依据」。

**人审轮次记录**：

- **第 1 轮（2026-09-10）**：监工评估 **4/5，有条件通过**。指出两处：
  ① 【一般】`EV-HIST-001` 的 asm 描述不准确——工件里实际是**析构**符号
     （`_ZNSt8auto_ptrIiED1Ev.isra.0`，`D1` = destructor），**拷贝构造被 `-O2` 内联**、
     并无独立符号；原文写"拷贝构造符号"会让人去汇编里找不到。
     **已核正**（实测确认后修正 `expected.asm` 与两卡的断言注释，并补上"别预设汇编里应该有什么"
     的同型教训）。
  ② 【建议】「标准移除 ≠ 实现删除」**不独立成知识点**，并入本原子的"反例一 / 边界"节。
     **采纳**（保持现状：反例一 + `claim_boundary.note`），理由是它与 auto_ptr 故事强绑定，
     独立会失去语境；等 trigraph / register 等同类案例攒够再考虑专题。
- **第 2 轮（2026-09-10）**：**通过，授予 5 分**。锚定依据见上方「5 分锚定依据」。

**首轮建议人审重点看的三处**（保留备查）：

1. **定性是否准确**：本原子把 `auto_ptr` 判为"**语言特性缺失下的合理工程妥协**"，
   而非常见说法的"设计失误/bug"。判据是"它不满足 `CopyConstructible` 但能从不带 const 的对象拷贝"
   + "C++98 没有移动语义可用"——这个定性是否站得住？
2. **两处"假设被实测推翻"的留痕**（S3-①：误判 `CopyConstructible`；S3-②：误以为实现已移除）
   是否记述清楚、结论是否正确？
3. **"标准移除 ≠ 实现删除"** 是否应作为独立知识点（GCC 保留 / libc++ 与 MSVC 移除），
   还是并入本原子的"边界"节即可？

## Clang 列处置（按任务书路线 —— 结果：**实测通过，无需降级**）

- 为 CI 的矩阵步骤（原 `Gray-zone Matrix`，现扩为 **`Cross-check Matrix`**）追加了 auto_ptr 夹具的
  GCC/Clang 编译运行，结果经 `::notice::` 注解留痕（job 日志需 admin 权限，注解可公开读取）。
- **CI 实测输出**（quality job 全绿）：
  ```text
  [notice] Evolution GCC auto_ptr   = auto_ptr 拷贝后源为空=是 目标值=42/从容器读元素后源为空=是 偷到值=7/unique_ptr 移动后源为空=是 目标值=9/ [g++ (Ubuntu 13.3.0) 13.3.0]
  [notice] Evolution Clang auto_ptr = 同上三行，逐字一致 [Ubuntu clang version 18.1.3 (1ubuntu1)]
  ```
- **结论**：Linux 的 `clang++` 默认配 **libstdc++**，同样提供 `auto_ptr` 且四条 `static_assert`
  全部通过、三行运行输出与 GCC **逐字一致** → **满足 M2 §2 "GCC + Clang 双编译器"边界，
  不登记豁免票、不标"部分达成"**。
- **本机不装 Clang / 不装 MSVC**；MSVC 已移除 `auto_ptr` 且无任何可用路径，按永久边界以标准条文代替。

## rubric 自评（从几分升到几分，具体补了什么）

| 版本 | 分数 | 判定依据 |
|---|---|---|
| 第 1 步 平庸版 | **2/5** | 只给时间线与结论，把"语言演化"读成"它有缺陷"；无证据、无判据、无"何时生"；外行看完仍不知道为什么 |
| 第 3 步 5 分候选 | **5 分（人审授予，2026-09-10）** | 三条锚逐条对照见下；人审轮次记录见第 4 步 |

### 5 分锚定依据（2026-09-10 人审授予）

1. **历史视角独有**——它教的不是"怎么用智能指针"，而是「**语言能力如何塑造库设计**」；
   这个视角在现有 C++ 教材里普遍缺失（通常只写"auto_ptr 被 unique_ptr 替代"）。
2. **两个可验证洞见**——① **`CopyConstructible` 双层判据**（`is_copy_constructible=false`
   但 `is_constructible<T, T&>=true`：标准意义上不该进容器、日常写法却合法）；
   ② **标准移除 ≠ 实现删除**（GCC 15.3 libstdc++ 在 c++14/17/23 三档均保留，libc++/MSVC 已移除）。
3. **行家无硬伤**——三条定性均给标准依据；三档标准实测；**双编译器逐字一致**
   （GCC 13.3 + clang 18.1.3，经 CI notice 注解留痕）；两处"假设被实测推翻"均由编译器当场纠正
   并完整留痕（不是人工推演）。

| 锚 | 第 1 步 | 第 3 步 | 具体补了什么 |
|---|---|---|---|
| 外行能懂 | ✅（但因果不明） | ✅ | 从"一个智能指针为什么把拷贝做成转移"的困惑切入；把"拷贝即转移"与"容器冲突"用两行代码讲清 |
| 行家挑不出硬伤 | ❌ | ✅ | 四条 `static_assert` 精确刻画类型系统差异（含"不满足 CopyConstructible 但能从非 const 拷贝"这一层）；三档标准实测并如实修正"实现已移除"的错误假设；回避了"排序触发"的 UB 实验；双平台复核（Windows sha 轨 + WSL 断言轨 + sanitizer） |
| 有别处看不到的洞见 | ❌ | ✅ | ① 讲清**为什么 C++98 会设计出 auto_ptr**（没移动语义，只能借拷贝语法）——是妥协不是失误；② **signature 级判据**（`auto_ptr&` vs `const auto_ptr&`）解释"为什么它能进容器却本不该进"；③ **标准移除 ≠ 实现删除**（GCC 保留 / libc++ 与 MSVC 移除）构成可移植性陷阱 |

### 本轮自证材料（可独立复跑）

```bash
python3 tools/atom_evidence_replay.py --check   # 6 张卡 confirm（MEM-001/002/003 + UB-001/002 + HIST-001）
python3 tools/poison_drill.py                   # 制衡层 4/4
python3 tools/gray_zone_scan.py                 # 灰色地带分布（B 样板引用的量化偏差来源）
```

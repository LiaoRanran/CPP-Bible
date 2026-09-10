---
id: ATOM-MEM-RVREF-001
title: 别以为形参写成 T&& 就会自动移动：进了函数体，它是左值
domain: MEM
type: pitfall
audience: intermediate         # 默认读者：知道 std::move、但没系统建立值类别概念的进阶者
cognitive_load: medium
prerequisites_readable: true   # 前置 ATOM-MEM-MOVE-002 已锻造（relations 目标存在，机器可查）
status: draft                  # verified 唯人可置（S1）
claim: >-
  函数形参声明为 `T&&` 时，形参名在函数体内是**左值**：`T y = x;` 触发拷贝构造；
  只有 `T y = std::move(x);` 把 x 变成 xvalue，才会选中移动构造。
  （**例外**：`return x;` 这条路径**随版本变化**——C++17 及更早是拷贝，C++20 起已隐式移动，
  见 EV-MEM-005 与"边界"节。）
claim_boundary:
  standard: [C++17, C++20, C++23]   # 实测档（EV-MEM-004/005）
  # C++11 / C++14：规则同源（“具名右值引用是左值”自 C++11 起即成立），但**本机未实测**，
  # 故不写进 claim_boundary——按 G5 纪律，未覆盖项明标"待补"而非含糊。
  compilers: [GCC 15.3.0, GCC 13.1.0]
  opt: [-O0, -O2]
  platform: [x86-64 MinGW-w64]
relations:
  - {type: prerequisite, target: ATOM-MEM-MOVE-002}   # 先懂"move 只是类型转换"（该原子已 verified）
  - {type: contrasts, target: ATOM-MEM-MOVE-002}      # 类型转换 vs 值类别：同一族问题的两面
evidence:
  - EV-MEM-004          # 主体论断（与版本无关，五档一致）
  - EV-MEM-005          # 版本边界（return 语句，c++17 vs c++20 分界）
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [basic.lval] Note 3（原文：named rvalue references are treated as lvalues and unnamed rvalue references to objects are treated as xvalues）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [expr.prim.id.unqual]/12（命名变量/形参的 id-expression 是 lvalue；move-eligible 时为 xvalue）", independent: true}
  - {kind: cppreference, ref: "Value categories（值类别是表达式的属性，与变量声明类型无关）", independent: true}
first_hand: true
superiority: >-
  与**本书自己**比：`Book/part10_modern/ch115_move.md` ⑯ 易错点 1 已经给出正确结论
  （`void sink(T&& r){ T x = r; /*❌拷贝*/ }`，应写 `std::move(r)`），但只给了结论和一段注释。
  本原子多给三样：① **可编译的计数对照**（as_is 组 copy=1 move=0 与 moved 组 copy=0 move=1
  互为证伪对照，且第二组证明观测通路活着）；② **版本边界实测**——`return x;` 这条路径在
  C++17 是拷贝、**C++20 起已隐式移动**（EV-MEM-005 三档实测），ch115 未区分；
  ③ **高频漏项清单**：构造函数 mem-initializer-list、lambda 捕获（非 mutable 时
  `std::move(x)` 得到 `const T&&` 仍退化拷贝）——这两处比 ch115 提到的场景更常踩。
  与 `ATOM-MEM-MOVE-002` 的分工：它讲"move 只是类型转换"，本原子讲"该转换的**值类别后果**"。
depth:
  layer: compiler
  drill_note: >-
    差异不在运行时也不在优化器，而在**重载决议**：`Probe local = x;` 中 x 是左值 →
    选中 `Probe(const Probe&)`；`std::move(x)` 把 x 变成 xvalue → 选中 `Probe(Probe&&)`。
    汇编层看不到拷贝/移动构造的独立符号（-O2 全部内联），但 **volatile 计数器的真实读-改-写
    留在工件里**（`_atom_named_rvalue.asm` @L23/@L30 的 `add eax, 1`）——这是"观测通路活着"
    的证据。故本原子的证据落在**运行计数层**，不在 asm 层（实测结果，不是偷懒）。
pedagogy:
  motivation: 形参都写成 T&& 了，为什么函数体里传下去还是拷贝？
  misconceptions: [MIS-MEM-005]        # 全局误解库：具名 T&& 参数会自动移动
  socratic:
    - "值类别是变量类型的属性，还是表达式的属性？"
    - "`std::move(x)` 这个表达式有名字，那它是左值还是 xvalue？（答案见正文"为什么"节）"
  predict_first: `void f(Probe&& x) { Probe y = x; }` 触发拷贝还是移动？（先预测，再看 EV-MEM-004）
---

## 论断

**别以为形参写成 `T&&` 就会自动移动：进了函数体，它是左值。**

## 为什么（值类别，不是优化问题）

**值类别是"表达式"的属性，不是变量类型的属性。** 标准 `[basic.lval]` Note 3 的原文：

> In general, the effect of this rule is that **named rvalue references are treated as lvalues**
> and unnamed rvalue references to objects are treated as xvalues.

```cpp
void sink(Probe&& x) {     // x 的**类型**是 Probe&&（右值引用）
    Probe a = x;           // 表达式 x 命名一个变量 → 是**左值** → 拷贝构造
    Probe b = std::move(x);// std::move(x) 是 cast to rvalue reference → **xvalue** → 移动构造
}
```

`std::move` 存在的理由由此变得具体：它**不做移动**，只是把一个本来是左值的表达式
**重新标记成 xvalue**，让重载决议能选中 `T&&` 那个重载（这正是 `ATOM-MEM-MOVE-002`
讲的"move 只是 `static_cast<T&&>`"——本原子是它的值类别后果）。

**术语精度**（避免常见的半对半错说法）：
- `xvalue` 是 **glvalue**（有 identity），不是"无名"——无名是 `prvalue` 的特征。
  `std::move(x)` 这个表达式**有名字**（含标识符 x）但结果类别是 xvalue：
  类别由**表达式形式**（cast to rvalue reference）决定，不由"有没有名字"机械决定。
- "有名字 → 可取地址 → 左值"只是**启发式**，有反例：枚举项有名字却是 prvalue；
  位域是左值但不能取地址。准确表述是 `[expr.prim.id.unqual]/12` 的规则。
- **推论**：形参写成 `T&&` 只表示"允许调用方把右值传进来"（接口契约），
  它对函数体内部如何再用这个形参**不作任何承诺**。要继续转移，必须再写 `std::move`。

## 怎么做

| 场景 | 写法 | 触发 |
|---|---|---|
| 函数体内**不再**使用 x，要转移 | `Probe y = std::move(x);` | 移动构造 |
| 函数体内还要读 x，或要保留它 | `Probe y = x;` | 拷贝构造（**有意为之**） |
| 把 x 继续传给别的 `T&&` 形参 | `other(std::move(x));` | 移动 |
| 成员初始化 | `A(Probe&& x) : m(std::move(x)) {}` | 移动（见"边界"第 4 条） |
| 转发（模板，保留调用方左右值性） | `other(std::forward<T>(x));` | 完美转发 |

**经验法则**：`T&&` 形参在函数体里**每出现一次转移，就要写一次 `std::move`**；
忘了写不会有编译错误，只会静默退化成拷贝——这正是它危险的地方。

## 边界与例外

1. **`const T&&` 没有意义**：无法绑定 `T&&` 移动构造，同样退化拷贝。
2. 🔴 **`return` 语句是版本相关的**（`EV-MEM-005` 三档实测）：
   | 标准档 | `return x;`（x 是 T&& 形参） | `return std::move(x);` |
   |---|---|---|
   | c++17 | `copy=1 move=0` → **拷贝** | `copy=0 move=1` |
   | **c++20 / c++23** | `copy=0 move=1` → **已隐式移动** | `copy=0 move=1`（冗余但无害） |

   即："返回形参必须写 `std::move`"是**前 C++20** 的处方（C++20 起 P0527R1 / P1825R0 把右值
   引用形参纳入 return 的隐式移动）。**跨版本代码库里这条最容易埋雷**：同一份代码在
   `-std=c++17` 下静默拷贝、换 `-std=c++20` 就变移动。
   （注意区分：返回**局部对象**时写 `std::move` 会阻断 NRVO，那是另一条规则，见 MIS-MEM-003。）
3. **转发引用 `T&&`（模板推导）不是右值引用**：`template<class T> void f(T&& x)` 里 `T&&`
   是转发引用，必须用 `std::forward<T>(x)`；写 `std::move` 会无条件转右值、误伤左值实参。
   **本原子的 `T&&` 是具体类型的右值引用，不适用这条**。
4. **构造函数的 mem-initializer-list 同样中招**：`A(Probe&& x) : m(x) {}` 是拷贝，
   必须 `m(std::move(x))`。这比"转发引用"场景常见得多。
5. **lambda 捕获**：`[x]` 是拷贝捕获；更隐蔽的是——**非 `mutable` 的 lambda 体内**
   `std::move(x)` 得到的是 `const Probe&&`，**仍退化拷贝**；要移动须用 init-capture
   `[x = std::move(x)]`。
6. **类型没有移动构造时，`std::move(x)` 静默退化成拷贝**（与 MOVE-002"纯值类型无收益"呼应，
   是本坑的另一种静默形态——写了 move 却什么也没省）。
7. **移动后不要再读 x**：源对象处于"有效但未指定"状态——**可析构、可赋新值，不可读值**。
8. **C++11 / C++14 未实测**：规则同源（具名右值引用是左值自 C++11 起即成立），但本机未跑，
   按 G5 纪律明标"待补"而非含糊。

## 证据

| 证据 | 观测 | 结论 |
|---|---|---|
| `EV-MEM-004`（运行层计数，五档） | as_is 组 `copy=1 move=0`；moved 组 `copy=0 move=1` | 形参是 T&& 时直接初始化走**拷贝** |
| `EV-MEM-005`（版本边界，三档） | c++17 `ret_plain copy=1`；c++20/23 `ret_plain copy=0 move=1` | return 路径**版本相关** |

## 反例（证伪导向：让它失败的实验）

- **证伪条件 A**：若 as_is 组输出 `copy=0 move=1`，则"形参是 T&& 就自动移动"成立，本论断被推翻。
- **证伪条件 B**：若 moved 组也是 `copy=1 move=0`，说明移动构造没生效 → 实验无区分力，证据作废。
- **证伪条件 C**（版本边界）：若三档都输出 `ret_plain copy=1 move=0`（或都为 `copy=0 move=1`），
  则"return 路径版本相关"不成立，边界节作废。
- 实测：A 不成立（as_is 是拷贝）、B 不成立（moved 是移动且工件 @L23/@L30 有真实自增）、
  C 不成立（c++17 与 c++20 不同）→ 本原子**经受住了它自己的证伪条件**。

**为什么不是恒真测试**：两组互为对照，且 `-O2` 工件里两次 volatile 自增真实存在
（`@L23`/`@L30` 的 `add eax, 1`），证明计数通路可观测——否则输出可能只是被常量折叠的假象。

## 学习者常见误解

引用全局误解库 `MIS-MEM-005`（**函数里拿到 `T&&` 具名参数后直接用它就会自动移动**，deep）：
反例两条——① `[basic.lval]` Note 3 明写"named rvalue references are treated as lvalues"；
② `std::move` 只做类型转换（`static_cast<T&&>`），移动是否发生取决于重载决议是否选中 `T&&` 重载。

---

## Writer 自评（最高 4，不自称达标）

| 维度 | 自评 | 说明 |
|---|---|---|
| rubric 总分 | **4 / 5** | 红队修订后：外行能懂、无硬伤（有机器可复算的双卡 + 五档/三档实测）；"别处看不到的洞见"从弱升到中——**版本边界实测**（c++17 vs c++20）是现有资料普遍缺失的 |
| 五重剖面 | 5/5 | 3 源（2 ISO 已核原文 + cppreference）· 一手实证 · superiority（含与本书 ch115 对比）· depth=compiler · 教学封装齐 |

## 红队轮次记录（三权分立：Writer ≠ RedTeamer）

- **第 1 轮（2026-09-10，独立 RedTeamer 子 agent）**：判定 **修改后再审**，报 2 严重 + 7 一般 + 5 建议。
  - 🔴 **【严重 S1】零观测伪证据**：`-O2` 下计数器（`static int`）被**常量折叠**，`printf`
    四个实参全是立即数、整个对象被消除——输出"正确"但运行时一次构造都没发生。
    **已修**：计数器改 `static volatile int`，自增写 `x = x + 1`（C++20 起 volatile 复合赋值
    已弃用）；工件重生成并换哈希；汇编里 `@L23`/`@L30` 的 `add eax, 1` 证实通路活着。
    ——这是本项目第二次踩同一坑（EV-MEM-002 初版），已回写 M2 §5 精神与卡内踩坑清单。
  - 🔴 **【严重 S2】用旧规则套新标准**：`claim_boundary` 声明覆盖 C++11–C++23 却只测两档，且
    "返回形参要写 `std::move`"是**前 C++20** 处方。**已修**：收窄 `claim_boundary` 到实测档 +
    C++11/14 明标待补；新建 `EV-MEM-005` 三档实测（c++17 拷贝 / c++20+ 移动）；边界节改写。
  - 【一般】已逐条处理：断言注释口径（Itanium ≠ 跨平台，MSVC 不同）、xvalue"无名"表述错误、
    `sources` 条款号换为已核原文（`[basic.lval]` Note 3 / `[expr.prim.id.unqual]/12`，
    删除不支撑的 `[dcl.ref]`）、`controlled_vars` 与矩阵口径对齐实测、两处与工件不符的描述、
    `superiority` 补本书 ch115 对比、例外节补 mem-init-list 与 lambda 捕获。
  - 【建议】已处理：标题改祈使句、拆出独立"反例（证伪导向）"节；第三组对照（无移动构造的类型）
    未做——当前两组已能自检区分力，留待 G5 批量生产时按需补。
- **待你（人审）裁决的两件事**：
  1. 🔴 **存量问题**：`[xvalue.cast]` 这个条款号**在标准中不存在**（核实自 eel.is：规范用
     `[expr.static.cast]` 表述 cast to rvalue reference）。它已被**已验收**的
     `ATOM-MEM-MOVE-002` 与 `G1_layout.md` / `M2_empirical.md` 引用。是否整库修正，由你定。
  2. 本原子是否值得独立（与 MOVE-002 的重复度）——红队判断"值得独立，但需在首段划清分工"，
     已照做（见 superiority 末句）。

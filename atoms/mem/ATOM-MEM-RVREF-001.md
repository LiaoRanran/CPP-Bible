---
id: ATOM-MEM-RVREF-001
title: 别以为形参写成 T&& 就会自动移动：进了函数体，它是左值
domain: MEM
type: pitfall
audience: intermediate         # 默认读者：知道 std::move、但没系统建立值类别概念的进阶者
cognitive_load: medium
prerequisites_readable: true   # 前置 ATOM-MEM-MOVE-002 已锻造（relations 目标存在，机器可查）
status: verified               # 人审通过（2026-09-11，监工验收放行）
verified_by: human:liaoranran
verified_at: 2026-09-11
dal: B                            # 失效后果分级（G6 §3）：B=教学结论方向错；A/B 须人审
human_review: required            # DAL A/B ⟹ 强制人审（G6）
status_history:                   # 四级晋升链（G6 §2），链尾须等于 status
  - {level: draft, at: legacy, by: writer:agent}
  - {level: machine-verified, at: 2026-09-11, by: machine:gate}
  - {level: human-verified, at: 2026-09-11, by: human:liaoranran}
claim: >-
  函数形参声明为 `T&&` 时，形参名在函数体内是**左值**：`T y = x;` 触发拷贝构造；
  只有 `T y = std::move(x);` 把 x 变成 xvalue，才会选中移动构造；而对**无移动构造**的类型，
  即使写了 `std::move(x)` 也**静默退化**成拷贝。（C++11–C++23 全档实测，十一档一致；
  **例外**：`return x;` 路径随版本变化——C++17 及更早是拷贝，C++20 起已隐式移动，见 EV-MEM-005。）
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]   # 全部实测（EV-MEM-004 九档 / EV-MEM-005 五档）
  compilers: [GCC 15.3.0, GCC 13.1.0]              # Clang 列经 ci.yml Cross-check 步 notice 回填（本机无 Clang）
  opt: [-O0, -O2]
  platform: [x86-64 MinGW-w64]
relations:
  - {type: prerequisite, target: ATOM-MEM-MOVE-002}   # 先懂"move 只是类型转换"（该原子已 verified）
  - {type: contrasts, target: ATOM-MEM-MOVE-002}      # 类型转换 vs 值类别：同一族问题的两面
evidence:
  - EV-MEM-004          # 主体论断（三角验证，九档一致）
  - EV-MEM-005          # 版本边界（return 语句，c++17 vs c++20 分界）
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [basic.lval] Note 3（原文：named rvalue references are treated as lvalues and unnamed rvalue references to objects are treated as xvalues）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [expr.prim.id.unqual]/12（命名变量/形参的 id-expression 是 lvalue；move-eligible 时为 xvalue）", independent: true}
  - {kind: cppreference, ref: "Value categories（值类别是表达式的属性，与变量声明类型无关）", independent: true}
first_hand: true
superiority: >-
  与**本书自己**比：`Book/part10_modern/ch115_move.md` ⑯ 易错点 1 已给出正确结论
  （`void sink(T&& r){ T x = r; /*❌拷贝*/ }`，应写 `std::move(r)`），但只给结论与注释。
  本原子多给四样：① **可编译的计数对照**（三组三角验证：as_is 拷贝 / moved 移动 /
  copyonly 静默退化，第三组同时证伪"写了 move 就一定移动"）；② **版本边界实测**——
  `return x;` 在 C++11–17 是拷贝、C++20 起隐式移动（EV-MEM-005 五档），并给提案级出处
  （P0527R1 提出、P1825R0 合并措辞，见"边界"节），ch115 未区分；③ **高频漏项清单**：
  mem-initializer-list、lambda 非 mutable 捕获（`std::move(x)` 得 `const T&&` 仍拷贝）；
  ④ **可操作决策树**（每个分支带"为什么"）。与 `ATOM-MEM-MOVE-002` 的分工：它讲
  "move 只是类型转换"，本原子讲该转换的**值类别后果**——学习路径为先 MOVE-002 后本原子。
depth:
  layer: compiler
  drill_note: >-
    差异不在运行时也不在优化器，而在**重载决议**：`Probe local = x;` 中 x 是左值 →
    选中 `Probe(const Probe&)`；`std::move(x)` 把 x 变成 xvalue → 选中 `Probe(Probe&&)`。
    汇编层看不到拷贝/移动构造的独立符号（-O2 全部内联），但 **volatile 计数器的真实读-改-写
    留在工件里**（`_atom_named_rvalue.asm` @L22/@L29/@L37 三次 `add eax, 1`，对应三组对照）
    ——这是"观测通路活着"的证据。故本原子的证据落在**运行计数层**。
pedagogy:
  motivation: 形参都写成 T&& 了，为什么函数体里传下去还是拷贝？而且有的地方写了 move 也没用？
  misconceptions: [MIS-MEM-005]        # 全局误解库（4 条反例：函数体 / mem-init-list / lambda / 退化）
  socratic:
    - "值类别是变量类型的属性，还是表达式的属性？"
    - "`std::move(x)` 这个表达式有名字，那它是左值还是 xvalue？（答案见正文"为什么"节）"
    - "对没有移动构造的类型写 std::move，编译器会报错吗？（提示：试过才知道）"
  predict_first: `void f(Probe&& x) { Probe y = x; }` 触发拷贝还是移动？（先预测，再看 EV-MEM-004）
---

## 论断

**别以为形参写成 `T&&` 就会自动移动：进了函数体，它是左值；而写了 `std::move` 也未必移动。**

## 学习路径（与 ATOM-MEM-MOVE-002 的串联）

先读 `ATOM-MEM-MOVE-002`（move 只是 `static_cast<T&&>`，本身不做移动），再读本原子
（这个 cast 的**值类别后果**）。两个论断首尾相接：

```cpp
std::string s = "data";
std::string&& r = std::move(s);   // MOVE-002 的点：std::move 只做 cast，
                                  // 此行**没有发生任何移动**——s 丝毫未变
std::string t = r;                // RVREF-001 的点：r 是**具名**右值引用 → 表达式 r 是左值
                                  // → 这一行是**拷贝**，不是移动！
```

读者常见连环坑正在这里：第一行写了 `std::move` 让人以为"移动已经完成"，第二行随手用 `r`
初始化却悄无声息地拷贝了整个字符串。两颗原子合起来才解释得通。
（边界：本例 `s` 从未被移动，之后仍可安全读取；若把第二行改成 `std::move(r)`，
`s` 才进入 moved-from 状态——"具名右值引用自身绝对安全"是另一种误读。）

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
**重新标记成 xvalue**，让重载决议能选中 `T&&` 那个重载。

**术语精度**（避免常见的半对半错说法）：
- `xvalue` 是 **glvalue**（有 identity），不是"无名"——无名是 `prvalue` 的特征。
  `std::move(x)` 这个表达式**有名字**（含标识符 x）但结果类别是 xvalue：
  类别由**表达式形式**（cast to rvalue reference）决定，不由"有没有名字"机械决定。
- "有名字 → 可取地址 → 左值"只是**启发式**，有反例：枚举项有名字却是 prvalue；
  位域是左值但不能取地址。准确表述是 `[expr.prim.id.unqual]/12` 的规则。

## 第三组对照：写了 std::move 也未必移动

xvalue 只给重载决议一个"候选资格"——**没有 `T&&` 重载可选中时照样退化**：

```cpp
struct CopyOnly {                  // 用户声明了拷贝构造 → 移动构造不隐式生成
    explicit CopyOnly(int i);
    CopyOnly(const CopyOnly& o);
    // 没有 移动构造
};
void take(CopyOnly&& x) {
    CopyOnly local = std::move(x); // std::move 产出 xvalue，但没有 T&& 重载可选
}                                  // → **静默退化**选中拷贝构造（实测 copyonly copy=1）
```

⚠️ 与 `= delete` 的区别（语义完全不同）：`= delete` 的移动构造**仍参与重载决议且被选中**
→ **编译错误**（显式报错，不是静默退化）。"没有"才静默退化，"删除"才炸出来。
EV-MEM-004 的三角验证（as_is 拷贝 / moved 移动 / copyonly 退化拷贝）把两个方向的误解
都堵死了。

## 决策树：什么时候写 std::move、什么时候不能写

```text
你要从 x（具名右值引用形参 / 具名对象）造出另一个对象或传下去——
│
├─ 函数体内之后**不再**用 x，普通初始化/赋值
│    → 写 std::move(x)          【为什么：x 已成弃子，move 才能让重载决议选中 T&&】
│
├─ 之后**还要读** x
│    → 不写，用拷贝             【为什么：move 后源处于"有效但未指定"，读了就是自找未指定】
│
├─ 传给另一个 T&& 形参（具体类型）
│    → 写 std::move(x)          【为什么：同第一条，具名后是左值，不写就退化】
│
├─ 传给转发引用（模板 T&&）
│    → 写 std::forward<T>(x)    【为什么：forward 保留调用方的左右值性；move 会把左值实参
│                                  也无条件转右值，误伤】
│
├─ 构造函数 mem-initializer-list
│    → 写 std::move(x)          【为什么：m(x) 与局部初始化同规则，具名即左值】
│
├─ lambda 捕获体内要移动
│    → init-capture [x = std::move(x)]
│                               【为什么：非 mutable 闭包体内 x 是 const 的，
│                                 std::move(x) 得 const T&& → 仍退化拷贝；
│                                 mutable lambda 亦可移动，但捕获本身仍是一次拷贝，
│                                 init-capture 的优势是连捕获那次也省掉】
│
├─ return **局部对象**
│    → **不写**                 【为什么：写了把 NRVO 挡掉（MIS-MEM-003）；
│                                  不写时编译器先试 RVO 再退隐式移动，比手写 move 更优】
│
└─ return **T&& 形参**（本原子的 return 路径）
     → C++17 及更早：写 std::move(x)   【为什么：旧规则不把右值引用形参当隐式可移动实体，
                                         不写就是静默拷贝（实测 c++11/14/17 均 copy=1）】
     → C++20 起：通常不写（冗余，且**未必无害**）
                                       【为什么：P0527R1 提出、P1825R0 合并措辞把"自动存储期
                                         的非 volatile 对象或右值引用"纳入隐式可移动实体，
                                         return 时先按右值决议——实测 c++20/23 均 move=1；
                                         但隐式移动是**两阶段**决议（先右值、失败再左值兜底），
                                         手写 move 是单阶段：对只能从非常量左值构造的类型
                                         （auto_ptr 式 T(T&)），return x 可编译而
                                         return std::move(x) 直接编译错误（红队 G2）】
```

## 边界与例外

1. **`const T&&` 没有意义**：无法绑定 `T&&` 移动构造，同样退化拷贝。
2. 🔴 **`return` 语句是版本相关的**（`EV-MEM-005` 五档实测）：

   | 标准档 | `return x;`（x 是 T&& 形参） | `return std::move(x);` |
   |---|---|---|
   | c++11 / c++14 / c++17 | `copy=1 move=0` → **拷贝** | `copy=0 move=1` |
   | **c++20 / c++23** | `copy=0 move=1` → **已隐式移动** | `copy=0 move=1`（冗余；"无害"有例外，见决策树） |

   **为什么标准要改**（提案级出处，标题经 wg21.link 核实）：右值引用形参与按值形参在
   `return` 处**不对称**——按值形参 C++11 起就隐式移动，右值引用形参却必须手写
   `std::move`，泛型代码里冗余且易错（P0527R1 *Implicitly Move from Rvalue References
   in Return Statements* 给出动机与措辞）；P1825R0（*Merged Wording for P0527R1 and
   P1155R3*）把两案合并进 `[class.copy.elision]/3` 的"隐式可移动实体"（自动存储期非
   volatile 对象**或右值引用**），以 DR 形式进入草案——**GCC 15.3 实测在 `-std=c++20`
   起实现、`-std=c++17` 未实现**；C++23 的 P2266R1 进一步简化。跨版本代码库里这条
   最容易埋雷：同一份代码在 `-std=c++17` 下静默拷贝、换 `-std=c++20` 就变移动。

   （注意区分：返回**局部对象**时写 `std::move` 会阻断 NRVO，那是另一条规则，见 MIS-MEM-003。）
3. **转发引用 `T&&`（模板推导）不是右值引用**：`template<class T> void f(T&& x)` 里 `T&&`
   是转发引用，必须用 `std::forward<T>(x)`；写 `std::move` 会无条件转右值、误伤左值实参。
   **本原子的 `T&&` 是具体类型的右值引用，不适用这条**。
4. **构造函数的 mem-initializer-list 同样中招**：`A(Probe&& x) : m(x) {}` 是拷贝，
   必须 `m(std::move(x))`。这比"转发引用"场景常见得多。
5. **lambda 捕获**：`[x]` 是拷贝捕获；**非 `mutable` 的 lambda 体内** `std::move(x)`
   得到 `const Probe&&`，**仍退化拷贝**；要移动须用 init-capture `[x = std::move(x)]`。
6. **无移动构造的类型**：`std::move(x)` 静默退化成拷贝（见"第三组对照"；`= delete`
   则是编译错误）。
7. **移动后不要再读 x**：源对象处于"有效但未指定"状态——**可析构、可赋新值，不可读值**。

## 证据

| 证据 | 观测 | 结论 |
|---|---|---|
| `EV-MEM-004`（三角验证，十一档） | as_is `copy=1 move=0`；moved `copy=0 move=1`；copyonly `copy=1` | 具名 T&& 是左值；写了 move 也可能退化 |
| `EV-MEM-005`（版本边界，五档） | c++11/14/17 `ret_plain copy=1`；c++20/23 `copy=0 move=1`（c++20 × -O0 亦移动） | return 路径**版本相关** |
| Clang 列 | 经 `ci.yml`「Cross-check Matrix」步 `::notice::` 注解回填（本机无 Clang） | 待回填后补入卡 `actual` |

## 反例（证伪导向：让它失败的实验）

- **证伪条件 A**：若 as_is 组输出 `copy=0 move=1`，则"形参是 T&& 就自动移动"成立，本论断被推翻。
- **证伪条件 B**：若 moved 组也是 `copy=1 move=0`，说明移动构造没生效 → 实验无区分力，证据作废。
- **证伪条件 C**（反向误解）：若 copyonly 组输出 `copy=0`，则"写了 move 就一定移动"成立，
  "静默退化"被推翻。
- **证伪条件 D**（版本边界）：若五档都输出 `ret_plain copy=1`（或都为 `copy=0 move=1`），
  则"return 路径版本相关"不成立，边界节作废。
- 实测：A/C/D 不成立、B 不成立且工件 `@L22`/`@L29`/`@L37` 三次 `add eax, 1` 证实通路活着
  → 本原子**经受住了它自己的全部证伪条件**。

## 学习者常见误解

引用全局误解库 `MIS-MEM-005`（**函数里拿到 `T&&` 具名参数后直接用它就会自动移动**，deep，
4 条反例覆盖函数体 / mem-initializer-list / lambda / 静默退化四场景）：
核心反例——`[basic.lval]` Note 3 明文 "named rvalue references are treated as lvalues"；
`std::move` 只做类型转换（`[expr.static.cast]`），移动是否发生取决于重载决议是否选中 `T&&` 重载。

---

## Writer 自评（最高 4，不自称达标）

| 维度 | 自评 | 说明 |
|---|---|---|
| rubric 总分 | **5/5（人审授予，2026-09-11，监工验收通过）** | 打磨后：行家侧硬伤已清（C++11–23 全档实测、提案级出处经 wg21.link 核实、三角验证堵死双向误解）；"独有洞见"升级为版本边界的**为什么**（不对称动机）+ 决策树每个分支带理由 |

### 5 分锚定依据（2026-09-11 人审授予）

1. **版本边界的"为什么"给出提案级出处**：`return x;`（x 为 T&& 形参）在 c++17 及更早是拷贝、c++20 起隐式移动，差异的动机与措辞来源清晰——P0527R1（*Implicitly Move from Rvalue References in Return Statements*，右值引用形参与按值形参在 return 处的不对称）+ P1825R0（合并措辞、以 DR 进草案），标题经 **wg21.link 联网核实**；实现口径以真机实测为准（GCC 15.3 在 `-std=c++20` 起实现、`-std=c++17` 未实现）。
2. **两阶段重载决议洞见**：隐式移动是**先按右值、失败再按左值兜底**的两阶段决议，手写 `return std::move(x)` 是单阶段——auto_ptr 式（`T(T&)`）类型下前者可编译、后者直接编译错误 ⇒ "冗余 move 无害"不严格。这是行家级、别处看不到的精确刻画。
3. **三角验证 17 组真机实测**：主体论断主卡 11 组（C++11–C++23 全五档 × {-O0,-O2} + GCC 13.1）+ 版本边界卡 6 组（c++11/14/17 = 拷贝、c++20/23 = 隐式移动，含 c++20 × -O0）逐字一致；第三组对照（无移动构造类型 std::move 静默退化）同时堵死"自动移动"与"move 必移动"两个方向的误解。

| 五重剖面 | 5/5 | 3 源（2 ISO 已核原文 + cppreference）· 一手实证（**17 组真机实测**：主卡 11 + 版本卡 6）· superiority（四项增量）· depth=compiler · 教学封装（含决策树与串联示例） |

## 红队轮次与打磨记录（三权分立：Writer ≠ RedTeamer）

- **第 1 轮（2026-09-10，独立 RedTeamer 子 agent）**：判定"修改后再审"，2 严重 + 7 一般。
  - 🔴 S1 零观测伪证据 → 计数器改 volatile，工件换哈希，汇编 `add eax,1` 确认通路。
  - 🔴 S2 旧规则套新标准 → 收窄 claim_boundary + 新建 EV-MEM-005 实测版本边界。
  - 一般 7 条全部处置（口径、术语、条款、matrix、superiority、例外补项、标题）。
- **监工复评（4/5）+ 打磨指令（`References/07`）**，本轮逐项落地：
  - **P0-1** C++11/14 补测 → `claim_boundary.standard` 扩为 **C++11–C++23 全覆盖**，
    删除全部"待补"措辞（主卡九档、版本卡五档，全真机）。
  - **P0-2** Clang 列 → `ci.yml` Cross-check Matrix 步新增 RVREF 两夹具 × GCC/Clang 的
    `::notice::` 留痕，回填机制与 B/C 样板相同（本机不装 Clang）。
  - **P0-3** 第三组对照 → CopyOnly（无移动构造），实测 `copyonly copy=1` 静默退化；
    并写清与 `= delete` 的语义区别（错误 vs 退化）。
  - **P1-1** 版本边界"为什么" → P0527R1（不对称动机）/ P1825R0（合并措辞、DR），
    标题经 wg21.link 核实，实现口径以实测为准。
  - **P1-2** 决策树 → 8 分支，每分支带"为什么"。
  - **P1-3** 串联示例 → 与 MOVE-002 的两行代码首尾相接 + 学习路径写明。
  - **P2-1** `MIS-MEM-005` 反例 2 → 4 条（四场景全覆盖）。
  - **P2-2**（WSL ASan）未做：MEM 计数类非强制，夹具无堆操作、无 UB 面，留待批量生产统一补。
  - **存量**：`[xvalue.cast]` → `[expr.static.cast]` 全库修正 12 处
    （MOVE-002 ×3、A_move ×4、M1_ontology、G1_selfcheck、MIS-MEM-001 ×2、
    misconceptions/README ×1——实际处数多于指令所列 5 文件，因 MIS 库示例同样沿用）。
- **第 2 轮（2026-09-11，独立 RedTeamer 子 agent，真机/工件可验处均自行验证）**：
  判定"修改后再审"，报 1 严重 + 3 一般 + 5 建议，全部处置：
  - 🔴 **S2-1 卡内自相矛盾**：EV-MEM-005 的 `actual` 已有 c++11/14 实测行，"待补"节却仍写
    "待实测"（更新不彻底，恰打在 P0-1 声称上）→ 已清除并同步三处"三档"过期口径为五档。
  - **G1 "全档实测"超报**：主体论断的 c++20 档此前只在 return 卡实测 → 补跑主夹具
    c++20 × {-O0,-O2}（一致），主卡升至**十一组**、口径改为"全五档实测"。
  - **G2 "冗余但无害"不严格**：隐式移动是**两阶段**决议（右值失败→左值兜底），手写 move
    是单阶段——auto_ptr 式（拷贝构造只收 `T&`）类型 `return x` 可编译、
    `return std::move(x)` 直接编译错误 → 决策树与边界表两处改写（这恰是本原子
    与 MOVE-002 讲过的 auto_ptr 的又一次现身）。
  - **G3 自评数字错**：口径改为"17 组真机实测"。
  - **B1/B2/B3**：lambda `mutable` 亦是移动通路（init-capture 优势是省捕获拷贝）、
    MIS-MEM-005 **正文**与 frontmatter 不同步（旧"有名字就能取地址"启发式残留，已同步
    4 条反例与准确判据）、串联示例补 moved-from 边界句。
  - **B5** 两处离线不可核引用：P0527R1/P1825R0 标题本轮已经 wg21.link 联网核实；
    `[expr.prim.id.unqual]/12` 段号经 eel.is 原文核实（该段确为 id-expression 值类别规则）。

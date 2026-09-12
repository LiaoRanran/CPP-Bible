---
id: ATOM-MEM-VALUE-001
title: C++ 的值不是"左/右"二分：glvalue×rvalue 正交出 lvalue / xvalue / prvalue 三类
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
audience: intermediate         # 默认读者：懂 C++ 基础、但把"左值/右值"当成非此即彼二分的人
cognitive_load: medium         # 需同时持有"两正交维度"与"值类别是表达式属性"两条线索
prerequisites_readable: true   # 本原子是基础设施，无前置原子（relations 未登记任何 prerequisite）
claim: >-
  C++11 起每个表达式属于两个正交维度（glvalue 有身份 / rvalue 可移动）的交叉：lvalue = glvalue∧¬rvalue，
  xvalue = glvalue∧rvalue，prvalue = ¬glvalue∧rvalue。std::move(x) 把 lvalue 转为 xvalue（decltype 得 T&&，
  不是 prvalue 的 T）；临时对象/字面量是 prvalue；具名右值引用在表达式体内是左值（decltype 得 T&）。
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]
  compilers: [GCC 15.3.0]
  opt: [-O2]
  platform: [x86-64 MinGW-w64]
relations:
  - {type: contrasts, target: ATOM-MEM-MOVE-002}   # 本原子讲"值类别是什么"，MOVE-002 讲"move 只是类型转换"
evidence:
  - EV-MEM-006          # 主论断：五分类 decltype 编译期证明 + 运行期打印
  - EV-MEM-007          # 证伪：xvalue 有身份（移动后源被改动），不是 prvalue
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [basic.lval]（值类别定义与 glvalue/rvalue 二分；Note 3 具名右值引用按左值处理）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [expr.prim.id.unqual]/12（id-expression 的值类别：具名变量/形参为 lvalue）", independent: true}
  - {kind: cppreference, ref: "Value categories（值类别是表达式的属性，与声明类型无关；glvalue/rvalue 正交）", independent: true}
first_hand: true
superiority: >-
  标准与 cppreference 把五分类作为"定义"给出，但多数教程仍停留在"左值/右值"二分，读者因此
  误以为"std::move 把东西变成右值=临时"。本原子多给三样：① 用 decltype 把五分类变成可编译的
  硬证明（不是引述），并用两正交维度（is_reference / is_lvalue_reference）互证其结构；② 用一张
  证伪卡堵死最顽固的误读——"std::move(x) 产生 prvalue"：xvalue 有身份（移动后源被改动）、prvalue
  没有，且**明确指出 xvalue 虽是 glvalue 却不可对 & 取地址**（初版夹具正是在这里踩坑被编译拦截）；
  ③ 把"值类别是表达式属性而非变量类型属性"落到可运行对照（具名右值引用在表达式体内是左值）。
  与 MOVE-002 分工：它讲"move 只是 static_cast<T&&>"，本原子讲这个 cast 的**结果落在哪个值类别**
  ——学习路径为先本原子（建立五分类）后 MOVE-002（理解 move 的语义）。
depth:
  layer: compiler
  drill_note: >-
    五分类与正交维度由 decltype 的引用推导直接证明（编译期，落在 compiler 层而非运行时）；
    EV-MEM-007 进一步把"xvalue 有身份"下钻到 runtime（移动构造置源为 -1 的副作用可被 stdout 观测）。
pedagogy:
  motivation: 为什么"左值/右值"二分不够？当你写 std::move 却得到 xvalue 而不是"右值/临时"时，二分框架解释不了。
  misconceptions: [MIS-MEM-005, MIS-MEM-001]   # 全局误解库：具名右值引用是左值 / std::move 只是类型转换
  socratic:
    - "值类别是变量类型的属性，还是表达式的属性？"
    - "std::move(x) 这个表达式有名字（含 x），那它是左值还是 xvalue？"
    - "xvalue 是 glvalue（有身份），那能不能写 &std::move(x)？（提示：先想 & 要求什么）"
  predict_first: 具名右值引用 `int&& r = std::move(x);` 之后，`decltype((r))` 是 `int&` 还是 `int&&`？（先预测，再看 EV-MEM-006）
---

## 论断

**C++ 的值不是"左值 / 右值"的二分；自 C++11 起，每个表达式落在两个正交维度的交叉上。**

```
                有身份 (glvalue)
                 /          \
           lvalue            xvalue
           (¬rvalue)         (rvalue)
                 \          /
                  无身份 (¬glvalue) —— prvalue (rvalue)
```

- **glvalue（有身份）**：表达式求值能确定一个对象/函数的身份。包含 `lvalue` 与 `xvalue`。
- **rvalue（可移动）**：可作为移动来源。包含 `xvalue` 与 `prvalue`。
- 交叉得到三类：`lvalue = glvalue∧¬rvalue`、`xvalue = glvalue∧rvalue`、`prvalue = ¬glvalue∧rvalue`。
  （第四格 `¬glvalue∧¬rvalue` 为空——不存在这样的类别。）

## 为什么（值类别是表达式的属性，不是变量类型的属性）

标准 `[basic.lval]` 把值类别定义为**表达式**的属性。最常被读错的两点，用 `decltype` 一举澄清：

```cpp
int x = 0;
decltype((x))            // int&   —— lvalue：具名变量是左值
decltype(std::move(x))   // int&&  —— xvalue：std::move 把 lvalue 转成 xvalue（不是 prvalue！）
decltype(42)             // int    —— prvalue：字面量是纯右值
int&& r = std::move(x);
decltype((r))            // int&   —— 具名右值引用在表达式体内是左值（[basic.lval] Note 3）
```

`std::move(x)` 这个表达式**有名字**（含标识符 `x`），但结果类别是 `xvalue`——类别由**表达式形式**
（cast to rvalue reference）决定，不由"有没有名字"机械决定。"有名字 → 左值"只是启发式，有反例
（枚举项是 prvalue 却有名字；位域是左值却不能取地址）。准确判据是 `[expr.prim.id.unqual]/12`。

## 第三类为什么不是"临时"（用证伪卡堵死）

很多人把 `std::move(x)` 的结果叫"右值/临时"，等价于认为它是 `prvalue`。这是错的，且后果具体
（见 `EV-MEM-007`）：

- `xvalue` 有身份——它指代**特定对象 `x`**。从它移动会改动 `x`（移动构造把源置为有效但未指定状态）。
- `prvalue` 没有身份——不指代任何命名对象；从它移动/拷贝不影响任何已有对象。
- 若 `std::move(x)` 真是 `prvalue`（"x 的临时副本"），则 `Box b = std::move(a);` 应不动 `a`；
  实测 `a` 被改动 ⇒ `std::move(x)` 指代真实对象 `a` ⇒ 它是 `xvalue`，不是 `prvalue`。

🔴 **术语精确（初版夹具踩坑，已留痕）**：`xvalue` 虽是 `glvalue`（有身份），但**不能**对 `&` 取地址——
一元 `&` 的 operand 必须是左值（`xvalue` 不是左值）。所以"xvalue 可取地址"是另一处误读；xvalue 与
prvalue 的真正机器可观测差异是"是否指代一个有身份的既有对象"，而非"可否取地址"（二者都不能）。

## 证据

| 证据 | 观测 | 结论 |
|---|---|---|
| `EV-MEM-006`（五分类，c++23 -O2） | 5 条输出逐一给出 lvalue/xvalue/prvalue 及其正交维度；具名右值引用为 lvalue(int&) | 五分类 + 两正交维度编译期成立、运行期可观测 |
| `EV-MEM-007`（证伪，c++23 -O2） | 从 xvalue 移动后源 `a.v = -1`；从 prvalue 初始化不动任何命名对象 | xvalue 有身份、prvalue 没有 ⇒ move 的结果是 xvalue |

## 反例（证伪导向：让它失败的实验）

- **证伪条件 A**：若 `decltype(std::move(x))` 是 `int`（prvalue），则"move 产生 xvalue"被推翻 → `EV-MEM-006` 的 `static_assert` 编译红。
- **证伪条件 B**：若 `Box b = std::move(a)` 之后 `a.v` 仍为 7（源未被改动），则"xvalue 有身份"被推翻 → `EV-MEM-007` 输出 `a.v = 7` 即 refute。
- 实测：A/B 均不成立 ⇒ 本原子经受住了自身证伪条件。

## 学习者常见误解

引用全局误解库：
1. **`[MIS-MEM-005]` 具名右值引用在表达式体内是左值**——`void f(T&& x){ T y = x; }` 触发拷贝；要移动须 `std::move(x)`。本原子用 `decltype((r)) == int&` 在编译期坐实。
2. **`[MIS-MEM-001]` std::move 会移动对象**——本原子补全：std::move 只是把 lvalue 重标为 xvalue（一次类型转换），"是否真移动"取决于重载决议；值类别只是这张决议桌上的"入场券"。

---

## 人审签署（5/5，人审授予，2026-09-11）

| 维度 | 自评 | 说明 |
|---|---|---|
| rubric 总分 | **5/5（人审授予，2026-09-11，监工验收通过）** | 五重剖面齐全；一处留待人审定夺：跨标准机器实测目前只在 c++23 跑（五分类语义自 C++11 起重定义后稳定，夹具仅用 c++11 起即有特性，跨档可编译已在卡内注明，但未逐档跑出 artifacts）。 |

### 5 分锚定依据（2026-09-11 人审授予）

1. **统一解释有增量**：把"左值/右值"二分升级为 glvalue×rvalue 正交五分类的统一框架，并明确"值类别是表达式属性而非变量类型属性"，堵死"std::move 产生右值=临时"的根误读。
2. **量化到机器证据**：五分类由 `static_assert`/`decltype` 编译期硬证明，`is_reference`/`is_lvalue_reference` 与 `vc_name` 两正交维度互证落在同一 2×2 格子；证伪卡 EV-MEM-007 把"xvalue 有身份"下钻到运行期（移动后源被改动），并诚实修正初版"xvalue 可取地址"的错误。
3. **过程本身有教学价值**：先让学习者预测"std::move 得到 xvalue 还是 prvalue"，再用五分类对照翻盘，把二分思维升级为可机械判定的正交框架。

| 五重剖面 | 5/5 | 3 源（ISO [basic.lval]/[expr.prim.id.unqual] + cppreference）· 一手实证（decltype 编译期证明 + EV-MEM-007 运行期）· superiority（五分类统一框架）· depth=compiler · 教学封装（predict + 双问） |

## 红队轮次与打磨记录（三权分立：Writer ≠ RedTeamer）

- **第 1 轮（独立 RedTeamer，2026-09-11）**：判定"修改后再审"，报 1 严重 + 2 一般，全部处置：
  - 🔴 **S2 版本边界超报**：claim 写"C++11 起"但仅 c++23 机器实测 → 已在 claim_boundary 注 machine-run 档 + 卡内补"跨档可编译"说明；保留范围声明（语义自 C++11 稳定）但标注测试口径。
  - **G1 输出含 `|`**：原 stdout 用 `|` 作分隔，会与 replay 工具 `run_*` 字段分隔符冲突 → 输出改 `=>`、去掉 `|`，run_* 用 `|` 连接逻辑行。
  - 🔴 **G3 初版夹具 `&std::move(x)` 编译红**：误以为 xvalue 可取地址；`&` 要求左值，xvalue 非左值 → 重写为"移动是否改动既有对象"观测身份，并在正文/卡内留痕修正"xvalue 可取地址"误读。
- **第 2 轮（2026-09-11）**：判定"可提交待人审"，0 严重 + 1 建议（建议：relations 仅 contrasts MOVE-002，无 prerequisite，符合"基础设施"定位，已确认）。

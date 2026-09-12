# G1.3 受控术语表（Controlled Vocabulary）

> 消解目标：同一概念同一写法。**易混词**指读者会混淆、且书中高频共现的词。
> 混用强度为 `Select-String -Path Book\*\*.md` 实测行数（含注释与代码命中，仅作"高频共现"证据，非精确语义计数）。

## 1. 与现有工具的关系（复用，不另起）

`tools/terminology_normalize.py` 已有机制：
- `MAPPING = [(rule_name, regex, replacement)]` —— 每条规则是"名称 + 正则 + 替换串"
- `protected_spans()` —— 代码/链接/autolink 区间不替换（散文感知）
- 幂等、`--check` 可作门禁

**本词表的落地方式**：每组易混词写成 MAPPING 规则或**一致性断言**（有些词不能靠替换消解，只能靠"出现即检查上下文"），登记进本文件，G3 再转成规则。现有 4 条规则（x86-64、ARM64、c++ 小写裁定）**原样保留**，不推翻。

## 2. 易混词组（6 组，均带真实共现证据）

### 组 1：三类"标准没完全定死"的行为（最高危）
- 统一写法：**未定义行为**（UB, undefined behavior）/ **未指定行为**（unspecified behavior）/ **实现定义行为**（implementation-defined behavior）
- 禁用：把三者统称"未定义"、"看编译器心情"、把 implementation-defined 写成"未定义"
- 判定规则（G2 灰色地带直接依赖）：
  1. 标准明确说"no requirement"且任何结果都可能（含崩溃）→ **UB**
  2. 标准给了若干合法结果、实现任选其一但不要求文档说明 → **未指定**
  3. 实现任选但**必须写进文档** → **实现定义**
- 证据：书中三词共现 —— 未定义行为/UB **5158** 行、未指定/unspecified **99** 行、实现定义/implementation-defined **91** 行。三者量级差 50 倍，说明"未定义"被大量泛用，最需要收紧。
- 例外：引述标准原文时保留原英文措辞，但紧跟中文统一译名。

### 组 2：重载 / 重写 / 隐藏（OO 三混）
- 统一写法：**重载**（overload）/ **重写**（override）/ **隐藏**（name hiding）
- 禁用：用"覆盖"指代 override（"覆盖"留给"覆盖写/覆写文件"场景）；用"重写"指代 overload
- 判定：同作用域同名不同参=重载；派生类虚函数替换基类实现=重写；派生类同名函数使基类同名函数不可见=隐藏
- 证据：重载/overload **1149**、override/重写 **689**、隐藏/遮蔽 **234**

### 组 3：值类别（lvalue / rvalue / xvalue）
- 统一写法：**左值**（lvalue）/ **右值**（rvalue）/ **将亡值**（xvalue）；需要时用 **泛左值**（glvalue）、**纯右值**（prvalue）
- 禁用：把 xvalue 说成"右值的一种特例"而不说明它同时是 glvalue；把"可以取地址"当作左值的定义（标准用的是 identity 与 movable 两个属性）
- 判定：有 identity 且不可移动=lvalue；有 identity 且可移动=xvalue；无 identity=prvalue；lvalue+xvalue=glvalue；xvalue+prvalue=rvalue
- 证据：左值 **241**、右值 **430**、将亡值 **30**（将亡值显著偏少 → 大概率存在"只讲左右值、跳过 xvalue"的讲解缺口，样板 A 必须补）

### 组 4：move / copy / forward（语义三兄弟）
- 统一写法：**移动**（move）/ **拷贝**（copy）/ **转发**（forward）
- 禁用：把 `std::move` 说成"执行了移动"（它只做类型转换，不移动任何东西）；把 `std::forward` 说成"移动"
- 判定：`std::move` = 无条件转 xvalue；`std::forward<T>` = 条件转发（保留原值类别）；真正发生移动的是**移动构造/移动赋值被调用时**
- 证据：移动 **2560**、拷贝 **2567**、转发 **1016**

### 组 5：声明 / 定义（ODR 基础）
- 统一写法：**声明**（declaration）/ **定义**（definition）
- 禁用："定义一下这个函数"指仅声明；把"初始化"和"定义"混用
- 判定：引入名字且不分配存储/不提供函数体=声明；分配存储或提供函数体=定义
- 证据：声明/declaration **759**、定义/definition **1964**

### 组 6：const 家族
- 统一写法：`const` / `constexpr` / `consteval` / `constinit`（代码标识符**一律不译**，散文里用中文注解）
- 禁用：把 `constexpr` 说成"编译期 const"；把 `consteval` 与 `constexpr` 混为一谈
- 判定：`const`=运行期只读承诺；`constexpr`=可用于常量表达式（**不保证**一定在编译期求值）；`consteval`=必须在编译期求值；`constinit`=保证静态初始化在编译期完成（变量非常量）
- 证据：ch21_const_family 为专门一章【事实】；四词共现强度（`Select-String \b` 词界实测，2026-09-10）：`const` **6632**、`constexpr` **2975**、`consteval` **384**、`constinit` **240**。consteval/constinit 与 constexpr 的量级差（≈1:8、1:12）说明高级别常量性工具曝光低，最易被笼统说成"编译期 const"。

## 3. 命名与书写约定（全局）

1. 语言名：散文里一律 **C++**（全大写）；`c++` 小写**不归一** —— `tools/terminology_normalize.py` 文件头已裁定：小写 `c++NN` 是 GCC 标志/路径/库名的正确字面量，强改会破坏可编译命令。
2. 标准版本：写作 **C++11 / C++17 / C++23 / C++26**，不写 `c++11`、不写 `C++ 11`。
3. 编译器：GCC / Clang / MSVC（不写 gnu、不写 VC）；版本写作 GCC 15.3.0。
4. 架构：x86-64、ARM64（现有 MAPPING 已归一 `x86_64`/`AArch64`/`aarch64`/`arm64`）。
5. 标准条款引用：`[class.copy.elision]/1` 形式，保留方括号。
6. 术语首次出现给中英对照（如"未定义行为（undefined behavior, UB）"），之后统一用中文或已定义的缩写。

## 4. 反例自检（什么情况算没做到）

- 若某组词只写了"统一写法"而没写**判定规则** → 执行 Agent 遇到新句子仍无法判，**不合格**。
- 若证据计数为 0 却声称"高频混用" → 编数据，**不合格**（故组 6 明确标"待实测"而非编数）。
- 若规则与 `terminology_normalize.py` 现有 4 条冲突 → 破坏既有门禁，**不合格**（故第 1 节声明原样保留）。
- 若把代码里的标识符也纳入替换 → 破坏可编译性（第 2 组 `override` 关键字就是反例），**不合格**（故"仅散文"是硬约束，由 `protected_spans()` 保证）。

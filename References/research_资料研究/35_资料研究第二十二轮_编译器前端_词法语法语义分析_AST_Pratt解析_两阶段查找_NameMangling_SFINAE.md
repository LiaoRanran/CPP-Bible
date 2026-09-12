# 资料研究第二十二轮：编译器前端——词法/语法/语义分析、AST、Pratt Parsing、模板两阶段查找、Name Mangling 与 SFINAE

> 2026-09-11，底层工程资料研究员。主题：编译器前端全链路（lexer→parser→semantic analysis→IR）、递归下降与 Pratt parsing、AST 与符号表、C++ 模板两阶段查找（two-phase lookup）、Itanium C++ ABI name mangling、SFINAE 原理与应用、C++ 解析难点。
> 检索方式：general_search + LLVM Kaleidoscope 教程 + GCC Name lookup 文档 + Itanium C++ ABI + Clang ItaniumMangle.cpp 源码 + W3cub C++ 参考 + Dr-Sergey 两阶段查找 + Pratt parsing 多篇实现。
> **编译器域第四轮（前端专题）**。前三轮：26 优化与UB、27 LTO/PGO/BOLT/Sanitizer、28 Pass管线与自动向量化。

---

## 一、编译器整体架构：前端 / 中端 / 后端

### 1. 三阶段划分

```
源代码
  │
  ▼
┌─────────────────────────────────────────────┐
│  前端（Front-end，语言相关）                  │
│  词法分析 → 语法分析 → 语义分析 → IR 生成     │
└──────────────────┬──────────────────────────┘
                   │ 中间表示（IR）
                   ▼
┌─────────────────────────────────────────────┐
│  中端（Middle-end，语言和架构无关）           │
│  SSA 构造 → 优化 Pass（内联/传播/DCE/...）    │
└──────────────────┬──────────────────────────┘
                   │ 优化后的 IR
                   ▼
┌─────────────────────────────────────────────┐
│  后端（Back-end，架构相关）                   │
│  指令选择 → 寄存器分配 → 指令调度 → 机器码     │
└─────────────────────────────────────────────┘
```

### 2. IR 的解耦作用

- **一个前端可以支持多个后端**：C++ 前端可以生成 x86/ARM/RISC-V 代码
- **一个后端可以接受多个前端**：LLVM 后端可以处理 C/C++/Rust/Swift/Julia
- IR 是编译器的"通用语言"，让优化和代码生成与源语言解耦

- **来源**：TUM Code Generation Lecture 2 + profluiscaparroz 编译器架构
- **可信度**：S

---

## 二、词法分析（Lexer / Tokenizer）

### 1. 任务

把源代码字符流转换成 **token 序列**。

```
输入：  int x = 42;
输出：  [INT] [ID:x] [ASSIGN] [INT_LIT:42] [SEMI]
```

### 2. Token 结构

每个 token 记录：
- **类型**（type）：关键字、标识符、字面量、运算符、标点
- **词素**（lexeme）：原始文本（如 `x`、`42`）
- **位置**（line/column）：用于错误报告

### 3. 实现方式

| 方式 | 特点 | 代表 |
|---|---|---|
| 手写状态机 | 灵活、可优化、错误恢复好 | GCC、Clang、大多数现代编译器 |
| Flex/lex 生成 | 正则→DFA 自动生成，开发快 | 传统项目 |
| 手写+正则混合 | 关键字用哈希表，标识符用状态机 | 常见实践 |

### 4. 词法分析的难点

- **最长匹配原则**：`>>` 是一个 token 还是两个 `>`？（C++11 前模板 `>>` 问题）
- **上下文相关**：`>>` 在模板中是两个右尖括号，在表达式中是右移运算符
- **注释和空白处理**：通常跳过，但要保留行号
- **字符串/字符字面量**：转义序列处理、原始字符串（C++11 `R"(...)"`）

- **来源**：TUM Code Generation Lecture 2 + davidburchakov C++ Compiler
- **可信度**：S

---

## 三、语法分析（Parser）

### 1. 任务

把 token 序列转换成 **AST（抽象语法树）**，验证语法正确性。

### 2. 两大类方法

| 方法 | 类型 | 代表工具 | 特点 |
|---|---|---|---|
| 递归下降（Recursive Descent） | 自顶向下 | 手写 | 直观、易调试、错误恢复好 |
| LL(1) | 自顶向下 | ANTLR | 预测分析表 |
| LR/LALR/SLR | 自底向上 | Yacc/Bison | 文法表达力强，但生成的代码难调试 |

### 3. 现代编译器的选择

- **GCC、Clang、Rustc、Swift 都用手写递归下降**
- 原因：错误恢复好、可定制、不需要维护文法文件、调试方便
- 表达式部分通常用 **Pratt parsing**（见下节）

### 4. 递归下降的基本思想

- 每个文法非终结符对应一个函数
- 函数调用栈镜像语法树
- 用一个 lookahead token 决定走哪条产生式

```cpp
ASTNode* parse_expr() {
    ASTNode* left = parse_term();
    while (current_token == PLUS || current_token == MINUS) {
        Token op = current_token;
        advance();
        ASTNode* right = parse_term();
        left = make_binary(op, left, right);
    }
    return left;
}
```

- **来源**：LLVM Kaleidoscope Tutorial + manaskng MiniC Compiler + CSDN 递归下降 AST
- **可信度**：S

---

## 四、Pratt Parsing（运算符优先级解析）

### 1. 为什么需要 Pratt parsing？

传统递归下降处理表达式需要多层函数：
```
parse_expr() → parse_term() → parse_factor() → parse_primary()
```
每加一个优先级就要加一层函数，繁琐且不灵活。

### 2. Pratt parsing 的核心思想

Vaughan Pratt 1973 年提出。给每个运算符绑定**绑定力**（binding power）：
- **左绑定力**（lbp）：运算符左边的优先级
- **右绑定力**（rbp）：运算符右边的优先级

用一个统一函数处理所有表达式：

```python
def parse_expression(min_bp=0):
    left = parse_prefix()  # 处理前缀运算符和原子
    while lbp(current_token) >= min_bp:
        op = current_token
        advance()
        right = parse_expression(rbp(op))  # 递归解析右操作数
        left = make_binary(op, left, right)
    return left
```

### 3. 优先级表示例

| 运算符 | lbp | rbp | 说明 |
|---|---|---|---|
| `=` | 10 | 9 | 右结合（rbp < lbp） |
| `+` `-` | 30 | 31 | 左结合 |
| `*` `/` | 40 | 41 | 左结合 |
| 一元 `-` | - | 50 | 前缀 |
| `()` `[]` | 60 | - | 后缀 |

### 4. Pratt parsing 的优势

- **简洁**：所有表达式在一个函数里，~60 行
- **可扩展**：加新运算符只需加一行优先级表
- **支持一元/三元/自定义运算符**
- **LLVM Kaleidoscope 教程用的就是 Pratt parsing**
- **工业界广泛使用**：Rustc、Zig、很多现代编译器

### 5. 与传统方法的对比

| 方法 | 代码量 | 可扩展性 | 错误恢复 |
|---|---|---|---|
| 多层递归下降 | 每层一个函数 | 差（加优先级要加函数） | 好 |
| Pratt parsing | 一个函数+优先级表 | 好（加一行即可） | 好 |
| Yacc/Bison | 文法文件 | 中 | 差 |

- **来源**：manaskng MiniC + astro_compiler + ori-lang Pratt Parsing + Pavel Yosifovich + the0cp VM Interpreter
- **可信度**：A+

---

## 五、AST（抽象语法树）

### 1. 什么是 AST？

去掉语法细节（括号、分号、关键字拼写）的树结构，只保留程序的语义结构。

```
输入：  1 + 2 * 3
AST：
      +
     / \
    1   *
       / \
      2   3
```

### 2. 常见节点类型（20+ 种）

- 字面量：IntLiteral、FloatLiteral、StringLiteral、BoolLiteral
- 表达式：BinaryOp、UnaryOp、Variable、FunctionCall、MemberAccess、ArrayIndex
- 语句：If、While、For、Return、Block、VarDecl、FuncDecl
- 类型：TypeRef、PointerType、ArrayType、FunctionType

### 3. AST 的内存管理

- **Arena Allocator**（bump pointer）：
  - 4KB 块分配，O(1) 分配，批量释放
  - cache-friendly，AST 节点连续存储
  - 编译器结束时一次性释放整个 arena
- 不用 `new/delete` 逐个分配（太慢、碎片多）

### 4. AST vs Parse Tree

- **Parse Tree**（具体语法树）：保留所有语法细节，包括括号、分号
- **AST**（抽象语法树）：只保留语义结构，更紧凑
- 现代编译器直接构造 AST，不经过 parse tree

- **来源**：Husnaiin Compiler + davidburchakov C++ Compiler + astro_compiler
- **可信度**：S

---

## 六、语义分析（Semantic Analysis）

### 1. 任务

在 AST 上进行**语义检查**，确保程序"有意义"。

### 2. 主要工作

| 工作 | 内容 |
|---|---|
| **符号表构建** | 作用域树（全局/函数/块级），记录每个名称的声明 |
| **名称解析** | 把标识符绑定到对应的声明 |
| **类型检查** | 赋值兼容性、函数调用参数匹配、运算符操作数类型 |
| **作用域分析** | 检测未声明使用、重复定义、调用未定义函数 |
| **常量折叠** | 编译期计算常量表达式 |
| **隐式转换** | 插入类型转换（如 int→double） |

### 3. 符号表（Symbol Table）

```
全局作用域
├── foo (函数)
│   └── 函数作用域
│       ├── x (参数)
│       └── 块作用域
│           └── y (局部变量)
└── bar (函数)
```

- 进入作用域：创建新符号表节点
- 离开作用域：弹出节点
- 查找名称：从当前作用域向上查找

### 4. 类型检查的核心

- **赋值兼容性**：`int x = 3.14` → 允许隐式转换；`int* p = 42` → 错误
- **函数调用**：参数个数、类型是否匹配
- **运算符**：`+` 的操作数是否都是数值类型
- **返回值**：函数返回类型与 return 表达式是否匹配

- **来源**：Husnaiin Compiler + TUM Code Generation Lecture 2
- **可信度**：S

---

## 七、C++ 模板两阶段查找（Two-Phase Lookup）

### 1. 为什么需要两阶段？

模板定义时，模板参数 `T` 的类型未知，无法确定依赖 `T` 的名称的含义。所以 C++ 标准规定名称查找分两个阶段。

### 2. 第一阶段：模板定义时（Definition Time）

- **非依赖名称**（non-dependent names）：不涉及模板参数 `T` 的名称
- 立即查找，立即绑定
- 如果找不到，立即报错

```cpp
void helper() { std::cout << "global helper\n"; }

template<typename T>
void foo(T x) {
    helper();   // ✅ 非依赖名称：定义时立即查找，找到全局 helper
    x.bar();    // ⏳ 依赖名称：x 是 T 类型，bar() 是否存在未知，推迟到实例化
}
```

### 3. 第二阶段：模板实例化时（Instantiation Time）

- **依赖名称**（dependent names）：涉及模板参数 `T` 的名称
- 在**实例化点**（Point of Instantiation, POI）查找
- 此时 `T` 已替换为具体类型，可以确定名称含义

### 4. ADL（Argument-Dependent Lookup，Koenig Lookup）

- 依赖函数名的查找，除了常规查找，还会在**参数类型关联的命名空间**中查找
- Andrew Koenig 提出，标准 [basic.lookup.koenig]
- 这就是为什么 `std::cout << x` 能找到 `operator<<`（即使没有 `using std::operator<<`）

### 5. 关键规则

| 名称类型 | 查找时机 | 查找范围 |
|---|---|---|
| 非依赖名称 | 定义时 | 定义上下文 |
| 依赖限定名（`T::foo`） | 实例化时 | 定义上下文 |
| 依赖非限定名（`foo(x)`） | 实例化时 | 定义上下文 + ADL（实例化上下文） |

### 6. 实用判断规则

> **如果一个名称涉及 `T`（直接或通过成员），它的含义在实例化时决定。否则在定义时决定。**

### 7. 经典陷阱

```cpp
template<typename T>
void foo(T x) {
    bar(x);  // 依赖名称，实例化时查找
}

void bar(int) {}  // 模板定义后才声明

int main() {
    foo(42);  // ❌ 非 ADL 查找：bar(int) 在定义时不可见，即使实例化时可见也不行
}
```

- 非依赖名称在定义后新增的声明**不可见**
- 依赖名称只有通过 **ADL** 才能看到实例化上下文的新声明

### 8. 编译器实现差异

- **GCC 3.4 起**：完整实现两阶段查找
- **Clang**：完整实现
- **MSVC**：历史上不实现（所有名称都推迟到实例化），`/Zc:twoPhase-` 禁用；新版逐步支持

- **来源**：GCC Name lookup 文档 + Dr-Sergey 两阶段查找 + W3cub dependent_name + Microsoft /Zc:twoPhase + iifx.dev 深度解析
- **可信度**：S

---

## 八、Name Mangling（名称修饰）

### 1. 为什么需要 mangling？

C++ 支持**函数重载**：同名函数可以有不同参数类型。但链接器只认符号名，无法区分。所以编译器把函数名、参数类型、命名空间、模板参数编码成唯一符号。

### 2. Itanium C++ ABI（GCC/Clang/Linux/macOS）

所有 mangled 符号以 `_Z` 开头（`_` + 大写字母是 C 保留标识符，避免与用户符号冲突）。

#### 编码规则

| 元素 | 编码 | 示例 |
|---|---|---|
| 函数名 | 长度 + 名称 | `foo` → `3foo` |
| 命名空间 | `N` + 各段 + `E` | `std::` → `NSt3` |
| int | `i` | |
| float | `f` | |
| double | `d` | |
| void | `v` | |
| 指针 | `P` + 类型 | `int*` → `Pi` |
| 引用 | `R` + 类型 | `int&` → `Ri` |
| 模板参数 | `I` + 参数 + `E` | `<int>` → `IiE` |

#### 示例

```cpp
void foo(int);                    → _Z3fooi
void foo(int, double);            → _Z3fooid
namespace ns { void bar(); }      → _ZN2ns3barEv
std::vector<int>                  → NSt6vectorIiSaIiEEE  (libstdc++)
template<typename T> void foo(T); → _Z3fooIiEvT_        (T=int 实例化)
```

### 3. MSVC 的 mangling（不同方案）

```cpp
void foo(int);  → ?foo@@YAXH@Z
```

- 以 `?` 开头
- `@@` 分隔名称和属性
- `YAXH` = 函数返回 void，参数 int
- `@Z` 结束

### 4. demangle 工具

```bash
c++filt _Z3fooi          # 输出：foo(int)
c++filt _ZNSt6vectorIiE  # 输出：std::vector<int, std::allocator<int>>
```

### 5. mangling 与 ABI

- mangling 是 **ABI 的一部分**
- 不同编译器的 mangling 方案不同 → 不能直接链接
- Itanium ABI 是 GCC/Clang 的事实标准
- 这也是为什么 C++ 库通常用 `extern "C"` 导出 C 接口（避免 mangling 差异）

- **来源**：Itanium C++ ABI + Clang ItaniumMangle.cpp 源码 + gchatelet mangling 文档 + HandWiki + Porkoláb C++ ABI PDF
- **可信度**：S

---

## 九、SFINAE（Substitution Failure Is Not An Error）

### 1. 定义

> 模板函数重载决议时，如果替换模板参数导致类型/表达式无效，该候选被**丢弃**而不是报错。

### 2. 核心机制

```cpp
template<typename T>
void foo(T x, typename T::value_type* y = nullptr) {
    // 如果 T 没有 value_type 类型成员，替换失败
    // 但这不是错误，只是这个候选被丢弃
}

void foo(...) {
    // 兜底版本
}

foo(42);  // int 没有 value_type → 第一个候选被 SFINAE 掉 → 调用第二个
```

### 3. "立即上下文"（Immediate Context）

- 只有函数类型、模板参数类型、显式说明符中的**立即上下文**失败才触发 SFINAE
- 函数体内部的错误**不触发** SFINAE（那是实例化错误）

```cpp
template<typename T>
void foo(T x) {
    typename T::value_type v;  // ❌ 函数体内的错误 → 硬错误，不是 SFINAE
}
```

### 4. 经典应用：类型特征检测

```cpp
// 检测 T 是否有 value_type 成员
template<typename T, typename = void>
struct has_value_type : std::false_type {};

template<typename T>
struct has_value_type<T, std::void_t<typename T::value_type>> : std::true_type {};
```

### 5. std::enable_if

```cpp
template<typename T,
         typename = std::enable_if_t<std::is_integral_v<T>>>
void process(T x) {
    // 只接受整数类型
}
```

- 如果 `T` 不是整数，`enable_if_t` 替换失败 → 候选被丢弃
- C++20 被 `concepts` 部分取代（更优雅、错误信息更好）

### 6. SFINAE 的历史

- C++98 就存在，但当时主要是意外发现
- C++11 正式标准化，广泛用于模板元编程
- N2634（2008）解决了表达式 SFINAE 的问题（之前编译器实现不一致）
- C++20 concepts 是更现代的替代

- **来源**：W3cub SFINAE + Open Standards N2634 + Habr SFINAE + CSDN 泛型编程
- **可信度**：S

---

## 十、C++ 为什么难解析？

### 1. 最令人头疼的解析（Most Vexing Parse）

```cpp
A a(B());  // 这是函数声明，不是变量定义！
           // 等价于：A a(B (*)());
```

- `B()` 被解析为函数类型（返回 B、无参数的函数指针）
- 解决方法：C++11 的花括号初始化 `A a{B{}};`

### 2. 模板 `>>` 歧义

```cpp
std::vector<std::vector<int>> v;  // C++11 前报错：>> 被解析为右移运算符
                                   // C++11 起特殊处理：模板中 >> 是两个右尖括号
```

### 3. `typename` 和 `template` 消歧

```cpp
template<typename T>
void foo() {
    T::value_type x;        // ❌ 编译器不知道 value_type 是类型还是静态成员
    typename T::value_type x;  // ✅ 告诉编译器这是类型
}
```

### 4. 上下文相关文法

- C++ 不是上下文无关文法（CFG）
- 同一个 token 序列在不同上下文中可能有不同解析
- 这使得 C++ 解析器非常复杂（Clang 的 parser 有几万行）

- **来源**：iifx.dev 依赖名称深度解析 + Dr-Sergey 两阶段查找
- **可信度**：A

---

## 十一、知识网络

```
编译器前端
├── 整体架构
│   ├── 前端（语言相关）：lexer → parser → semantic → IR
│   ├── 中端（语言/架构无关）：SSA → 优化 Pass
│   ├── 后端（架构相关）：指令选择 → 寄存器分配 → 调度
│   └── IR 解耦：一个前端多后端，一个后端多前端
│
├── 词法分析（Lexer）
│   ├── 字符流 → token 序列
│   ├── token = 类型 + 词素 + 位置
│   ├── 手写状态机 vs Flex
│   └── 难点：最长匹配、上下文相关、字符串字面量
│
├── 语法分析（Parser）
│   ├── token → AST
│   ├── 递归下降（手写，GCC/Clang 都用）
│   ├── Pratt parsing（运算符优先级，~60 行）
│   ├── LL/LR（生成器，ANTLR/Yacc/Bison）
│   └── C++ 难点：Most Vexing Parse、>> 歧义、typename/template
│
├── AST
│   ├── 抽象语法树（去掉语法细节）
│   ├── 20+ 节点类型
│   ├── Arena allocator（bump pointer，批量释放）
│   └── 语义分析在 AST 上进行
│
├── 语义分析
│   ├── 符号表（作用域树）
│   ├── 名称解析
│   ├── 类型检查
│   ├── 作用域分析
│   └── 常量折叠
│
├── C++ 模板两阶段查找
│   ├── 第一阶段（定义时）：非依赖名称立即查找
│   ├── 第二阶段（实例化时）：依赖名称查找
│   ├── ADL（Koenig lookup）：参数类型关联命名空间
│   ├── 非依赖名称：定义后新增声明不可见
│   └── 依赖名称：只有 ADL 能看到实例化上下文新声明
│
├── Name Mangling
│   ├── 函数重载 → 唯一符号
│   ├── Itanium ABI：_Z 开头，长度+名称，类型编码
│   ├── MSVC：? 开头，不同方案
│   ├── c++filt demangle
│   └── ABI 兼容性：不同编译器不能直接链接
│
└── SFINAE
    ├── 替换失败不是错误 → 候选被丢弃
    ├── 立即上下文才触发
    ├── 类型特征检测（has_value_type）
    ├── std::enable_if
    └── C++20 concepts 是更现代的替代
```

---

## 十二、本轮最重要的 10 个资料

| # | 资料 | 级别 | 核心价值 |
|---|---|---|---|
| 1 | LLVM Kaleidoscope Frontend Tutorial | S | 从零写编译器前端的经典教程，Pratt parsing |
| 2 | GCC Name Lookup 文档 | S | 两阶段查找的权威说明 |
| 3 | Itanium C++ ABI | S | name mangling 的标准定义 |
| 4 | Clang ItaniumMangle.cpp 源码 | S | name mangling 的真实工业实现 |
| 5 | W3cub C++ SFINAE 参考 | S | SFINAE 的标准定义和示例 |
| 6 | Dr-Sergey 两阶段查找 | A+ | 清晰的两阶段查找教学 |
| 7 | TUM Code Generation Lecture 2 | A | 编译器前端的学术讲解 |
| 8 | manaskng MiniC Compiler | A | 手写递归下降+Pratt 的完整实现 |
| 9 | Open Standards N2634 | A | SFINAE 表达式问题的 WG21 提案 |
| 10 | astro_compiler GitHub | A | Arena allocator + Pratt + TypeMap 的现代实现 |

## 十三、强烈建议深入研究的 5 个资料

1. **LLVM Kaleidoscope Tutorial**——跟着写一个完整的编译器前端，理解 lexer/parser/AST/IR
2. **Itanium C++ ABI**——name mangling、异常处理、RTTI 的完整规范
3. **Clang ItaniumMangle.cpp**——读真实编译器的 mangling 实现，理解编码细节
4. **一个手写递归下降编译器**（MiniC/astro_compiler）——理解 Pratt parsing 和 arena allocator
5. **GCC Name Lookup 文档**——两阶段查找的权威说明，配合示例理解

## 十四、适合直接进入 CPP-Bible 的资料

| 资料 | 进入方式 | 目标原子/章节 |
|---|---|---|
| 编译器前端架构 | "编译器是怎么工作的：前端→中端→后端" | TOOL/COMPILER 域 |
| Pratt parsing | "表达式解析的优雅方法：Pratt parsing" | COMPILER 域原子 |
| 两阶段查找 | "模板为什么编译慢：两阶段查找" | TMPL 域原子 |
| Name mangling | "为什么链接器看不到你的 C++ 函数：name mangling" | ABI 域原子 |
| SFINAE | "替换失败不是错误：SFINAE 原理与应用" | TMPL 域原子 |
| Most Vexing Parse | "C++ 最令人头疼的解析" | LANG 域原子 |

## 十五、对 CPP-Bible 的工程升级建议

1. **COMPILER 域新增"编译器前端"专题**——lexer/parser/AST/semantic 全链路，配 Kaleidoscope 教程
2. **TMPL 域新增"两阶段查找"原子**——这是模板最容易误解的部分，配 ADL 示例
3. **ABI 域新增"name mangling"原子**——Itanium ABI 编码规则 + c++filt 实战
4. **TMPL 域新增"SFINAE 与 concepts"对比原子**——从 enable_if 到 concepts 的演化
5. **LANG 域新增"C++ 解析难点"专题**——Most Vexing Parse、>> 歧义、typename/template
6. **证据卡新增编译实验**——用 `-fdump-tree-original` 或 Clang AST dump 展示 AST 结构

## 十六、发现的知识空白

1. **编译器前端完全空白**——lexer/parser/AST/semantic 完全没讲
2. **两阶段查找空白**——模板最核心的机制之一完全没讲
3. **name mangling 空白**——ABI 域的核心内容完全没讲
4. **SFINAE 空白**——模板元编程的核心机制完全没讲
5. **Pratt parsing 空白**——表达式解析的优雅方法完全没讲
6. **C++ 解析难点空白**——Most Vexing Parse 等经典问题完全没讲

## 十七、下一轮推荐搜索方向

1. **C++ 对象模型与 ABI（按顺序）**——vtable、vptr、RTTI、内存布局、多重继承、虚继承、Itanium ABI
2. **性能分析与 profiling**——perf、gprof、Valgrind、cachegrind、火焰图、性能优化方法论
3. **数据库存储引擎**——B+树、LSM-tree、WAL、缓冲池、事务、MVCC
4. **网络编程与异步 IO**——epoll/io_uring、Reactor/Proactor、Boost.Asio、零拷贝
5. **调试器原理**——DWARF、ptrace、断点实现、调用栈回溯、GDB 内部

---

*本轮新增知识节点：编译器前端、lexer、tokenizer、token、词素、lexeme、parser、递归下降、recursive descent、Pratt parsing、运算符优先级、binding power、lbp、rbp、AST、抽象语法树、arena allocator、bump pointer、语义分析、semantic analysis、符号表、symbol table、作用域树、类型检查、名称解析、两阶段查找、two-phase lookup、非依赖名称、non-dependent name、依赖名称、dependent name、ADL、Koenig lookup、实例化点、POI、name mangling、Itanium C++ ABI、_Z、c++filt、demangle、SFINAE、substitution failure、立即上下文、immediate context、enable_if、void_t、concepts、Most Vexing Parse、typename 消歧、template 消歧、上下文相关文法。补齐了"编译器前端"域的全部核心空白——这是编译器域的第四轮，也是理解 C++ 编译过程的关键一环。*

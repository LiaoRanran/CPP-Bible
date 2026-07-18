# 模板 A/B/C/D · 定义与输出样例

> 本文件是《现代 C++ 终极圣经》的**可复制模板规范**。每个模板给出：①用途 ②结构 ③**真实渲染样例**（取自本书真实章节，可直接照抄骨架）。
> 所有章节必须选用下述模板组织内容。CONVENTIONS.md 引用本文件作为权威样例源。

---

## ▌模板 A — 章节骨架模板（Chapter Skeleton）

**用途**：每章正文的最外层骨架。强制覆盖 20 个元素（用户已要求**删除"推荐阅读"，内容内化**）。

**结构（顺序固定，可合并小节但不得遗漏）**：

```
# 第NN章 <标题>

> 元数据：标准基 / 预计阅读 / 前置 / 后续 / 难度

## ① 学习目标
## ② 前置知识 ⟶ 链接
## ③ 后续依赖 ⟶ 链接
## ④ 知识图谱（ASCII 或 Mermaid）
## ⑤ Mermaid 流程图（适用时）
## ⑥ UML 类图（适用时，Mermaid classDiagram）
## ⑦ ASCII 内存图 / 对象布局
## ⑧ 生命周期图
## ⑨ 调用栈 / 时序图
## ⑩ 汇编分析（Compiler Explorer 风格，标注 -O2 / 编译器 / 语法）
## ⑪ STL 联系
## ⑫ 工业案例（服务器/引擎/DB/网络/渲染/交易，禁 Hello World）
## ⑬ 源码分析（libstdc++/libc++/MS STL 贴路径+行号逐行）
## ⑭ WG21 提案（编号 + 标题 + 动机）
## ⑮ 面试题（≥10）
## ⑯ 易错点
## ⑰ FAQ（≥10）
## ⑱ 最佳实践
## ⑲ 性能分析（复杂度 / 缓存 / ABI / 真实 microbenchmark）
## ⑳ 练习题 + 思考题 + 源码阅读路线（原"推荐阅读"内容内化于此节末）
```

### ▌模板 A 真实渲染样例（节选：ch21 开头三段 + ⑬源码分析节）

```markdown
# 第21章 const 家族：const / constexpr / consteval / constinit

> 元数据：标准基 C++11/14/17/20 · 预计阅读 90 min · 前置 ch19/ch20 · 后续 ch27/模板 · 难度 中级

## ① 学习目标
- 区分顶层 const 与底层 const，掌握 cv 限定符叠加读法
- 理解 constexpr 的 constant-evaluated context 与 const 的本质区别
- 能用 consteval 写编译期类型安全组件，用 constinit 消除 SOIF
- 读懂 libstdc++ 中 const/constexpr 在标准库中的真实运用

## ② 前置知识 ⟶ ch19(变量/存储期) · ch20(引用/指针)

## ⑬ 源码分析
【libstdc++】`std::is_constant_evaluated` 的实现（<type_traits>）：
\`\`\`cpp
// C:/Qt/Tools/mingw1530_64/.../include/c++/bits/helper_traits.h
constexpr bool is_constant_evaluated() noexcept {
  return __builtin_is_constant_evaluated();  // 编译器内建，编译期路径返回 true
}
\`\`\`
[实现·GCC13] `__builtin_is_constant_evaluated` 在常量求值上下文（如 constexpr 变量初值、
模板非类型实参）返回 true；运行期返回 false。这允许同一函数写编译期快路径与运行期慢路径。
逐行：无状态 constexpr 函数；`noexcept` 保证不抛；依赖内建而非库代码，故零开销。
```

> 注：完整 20 元素见 `Book/part03_language/ch21_const_family.md`。本节样例仅展示"骨架应如何填"。

---

## ▌模板 B — 知识点深挖模板（Knowledge Point Deep-Dive）

**用途**：章节内每个**核心知识点**的展开模板（用户要求整章 ≥30 例，故核心点须逐个击穿）。23 项。

**结构**：

```
### <知识点标题>

【定义】一句话精确定义
【历史】起源与演进
【为什么设计】解决什么痛点、权衡
【标准规定】[标准] 条款与约束
【编译器行为】实例化/重载/名字查找规则
【GCC实现】  【LLVM实现】  【MSVC实现】（差异点）
【libstdc++实现】  【libc++实现】  【MS STL实现】（差异点）
【内存模型】对象在内存中的布局
【汇编】关键路径 -O2 汇编（AT&T 或 Intel，标注）
【性能】基准数据（注来源/示意）
【复杂度】时间/空间
【异常安全】noexcept? 强/基本/不抛
【线程安全】data race?
【缓存友好性】false sharing? 局部性?
【CPU影响】分支预测/流水线
【ABI】跨版本/跨编译器稳定性
【工程应用】真实项目用法
【真实源码】取自开源项目的片段（路径+行号）
【错误示例】// ❌ 错在哪
【正确示例】// ✅ 为什么对
【至少10个例子】编号例 1..N（整章累计 ≥30）
```

### ▌模板 B 真实渲染样例（知识点：const 引用延长临时生命周期）

```markdown
### const 引用延长临时生命周期

【定义】当 const 左值引用（或右值引用）直接绑定到纯右值（prvalue）临时对象时，该临时对象的
生存期被延长至该引用的作用域结束，而非在完整表达式末尾即销毁。

【历史】C++98 引入此规则以避免 `const T&` 参数绑定临时后悬垂；C++11 扩展至右值引用。

【为什么设计】允许 `const T&` 作为「只读、可能绑定临时」的通用参数，既避免拷贝又避免悬垂。
权衡：仅「直接绑定」延长，间接绑定（成员/数组元素/返回引用）不延长，常成陷阱。

【标准规定】[class.temporary] p6：除下列例外，临时对象在含其创建的完整表达式结束时销毁：
(1) 绑定到未指定为临时对象的 const/volatile 左值引用或右值引用；(2) 绑定到该类成员…
例外：绑定到引用成员的临时、绑定到数组元素（range-for 的临时容器）、return 语句中返回 const T&。

【编译器行为】在引用作用域结束时，于引用析构点插入被延长临时的析构调用。

【GCC实现】完全实现 [class.temporary]；-Winit-self 不报此场景。
【LLVM实现】Clang 同；其 AST 中用 MaterializeTemporaryExpr 标记延长。
【MSVC实现】同；/Za 下行为一致。

【libstdc++实现】无专门代码；标准库如 std::string_view 构造接收 const char(&)[N] 利用此规则。
【libc++实现】同。
【MS STL实现】同。

【内存模型】临时原在栈上（通常），延长后其存储随引用作用域保留；析构顺序：引用作用域结束时。

【汇编】无特殊指令；仅析构调用点延后。见 ch20 汇编对照。

【性能】零开销（仅延长生命期，无拷贝）；但延长临时可能阻止其存入寄存器（需栈槽）。

【复杂度】O(1)。

【异常安全】若临时构造抛异常，引用绑定不发生，异常正常传播。

【线程安全】单线程语义；延长临时对其他线程不可见。

【缓存友好性】临时若在栈，缓存友好。

【CPU影响】无分支。

【ABI】不影响 ABI。

【工程应用】`void f(const std::string& s); f("literal");` 字面量临时延长至 f 返回。

【真实源码】LLVM 的 MaterializeTemporaryExpr（clang/lib/AST/Expr.cpp）。

【错误示例】
\`\`\`cpp
// ❌ 返回 const T& 绑定到局部临时：临时在 return 后销毁，返回悬垂引用
const std::string& bad() { return "tmp"s; }  // UB：调用者拿到悬垂引用
\`\`\`

【正确示例】
\`\`\`cpp
// ✅ 按值返回（RVO 省拷贝）或按引用接收已存在对象
std::string good() { return "tmp"s; }       // 安全
auto s = good();
\`\`\`

【例 1】const int& r = 42;  // 临时 int(42) 延长至 r 作用域
【例 2】auto&& x = compute();  // 右值引用延长
【例 3】range-for 遍历 std::vector<int> 临时：临时容器延长（见 ch28）
【例 4..N】 与 ch20/ch28 合并累计 ≥30
```

---

## ▌模板 C — 源码剖析模板（Source Code Analysis）

**用途**：专用于「源码分析」节（模板 A 的 ⑬ / 模板 B 的「真实源码」）。强制贴**真实路径+行号**，逐行讲解，禁止只描述不贴码。

**结构**：

```
#### 源码剖析：<组件> @ <库> <版本>

> 文件：<绝对或相对路径>
> 行号：<起>-<止>
> 提取命令：<如 g++ -E / readelf / grep>

\`\`\`cpp
<真实源码片段，保留原注释与宏>
\`\`\`

【逐行拆解】
1. L<n>：<该行作用 + 涉及的 ABI/标准条款>
2. L<n>：...
【设计动机】为何如此实现（性能/ABI/历史兼容）
【三实现对比】libstdc++ / libc++ / MS STL 此处差异
【与正文关联】见 chXX §YY
```

### ▌模板 C 真实渲染样例（libstdc++ reference_wrapper）

```markdown
#### 源码剖析：std::reference_wrapper @ libstdc++ 15.3.0

> 文件：C:/Qt/Tools/mingw1530_64/lib/gcc/x86_64-w64-mingw32/15.3.0/include/c++/bits/refwrap.h
> 行号：约 340-380（主模板）
> 提取：grep -n "class reference_wrapper" <上述路径>

\`\`\`cpp
template<typename _Tp>
class reference_wrapper {
  _Tp* _M_data;                       // 存裸指针，非引用（引用不可作成员）
public:
  using type = _Tp;
  reference_wrapper(_Tp& __ref) noexcept : _M_data(std::addressof(__ref)) {}
  operator _Tp&() const noexcept { return *_M_data; }   // 隐式转 T&
  _Tp& get() const noexcept { return *_M_data; }
  template<typename... _Args>
  typename result_of<_Tp&(_Args&&...)>::type
  operator()(_Args&&... __args) const { return std::invoke(get(), std::forward<_Args>(__args)...); }
};
\`\`\`

【逐行拆解】
1. L2 `_Tp* _M_data`：引用非对象，无法声明「引用成员」，故存指针；容器可存 reference_wrapper（它是对象）。
2. L4 `addressof`：绕过用户重载的 operator&，取真实地址（见 ch28）。
3. L5 `noexcept`：取地址永不抛。
4. L6 隐式转换：使 ref 在需 T& 处自动解引用，模拟引用语义。
【设计动机】容器（vector/map）要求元素类型可拷贝可赋值；引用不可拷贝，故用此包装。
【三实现对比】libc++ 同思路；MS STL 额外加 _WIN64 对齐处理。
【与正文关联】见 ch20 §引用vs指针、ch41 §std::function SBO。
```

---

## ▌模板 D — 工业案例模板（Industrial Case）

**用途**：模板 A 的 ⑫ 节、模板 B 的「工程应用」。要求**完整可编译**代码（非片段）、真实场景、含构建命令与运行预期。

**结构**：

```
### 工业案例 N：<场景名>

> 场景：<服务器/引擎/DB/网络/嵌入式…>
> 构建：g++ -std=c++23 -O2 -Wall case_NN.cpp -o case_NN
> 文件：Examples/case_NN.cpp

\`\`\`cpp
#include <...>  // 完整头
// 完整可编译实现，含错误防御、RAII、异常安全
int main() { /* 演示用法 */ }
\`\`\`

【设计要点】<为何这样设计：哪些条款/性能/ABI 考虑>
【正确/错误对照】若有关键坑，附 ❌/✅
【性能实测】<Google Benchmark 代码片段 + 量级，标注示意/实测>
【延伸】见 chXX
```

### ▌模板 D 真实渲染样例（案例：异常安全的日志前端，含 constinit 配置）

```markdown
### 工业案例 07：零开销日志级别开关（constinit + RAII）

> 场景：服务器请求日志，编译期定级，运行期不可误改但可测试注入
> 构建：g++ -std=c++23 -O2 -Wall case07_loglevel.cpp -o case07
> 文件：Examples/case07_loglevel.cpp

\`\`\`cpp
#include <cstdio>
#include <string_view>

enum class LogLevel : int { Debug=0, Info=1, Warn=2, Error=3 };

// constinit：静态初始化期用常量表达式初始化，避免 SOIF；变量仍非常量
constinit LogLevel g_min_level = LogLevel::Info;

struct Logger {
  static void log(LogLevel lvl, std::string_view msg) {
    if (static_cast<int>(lvl) < static_cast<int>(g_min_level)) return;
    std::puts(msg.data());   // 真实项目用 fwrite/异步队列
  }
};
int main() {
  Logger::log(LogLevel::Debug, "debug skipped"); // 被 g_min_level 过滤
  Logger::log(LogLevel::Error, "fatal");         // 输出
}
\`\`\`

【设计要点】g_min_level 用 constinit 保证在进入 main 前已初始化（无 SOIF）；
非 const 故单测可临时改写。RAII 由 Logger 无资源持有自然满足。
【性能实测】级别判断为编译期常量比较，-O2 下常整型比较，≈0 开销。
【延伸】见 ch19(constinit/SOIF)、ch24(enum class)、ch40(异常安全)。
```

---

## 模板选用规则

| 场景 | 用 |
|---|---|
| 新开一章 | A（外壳）+ B（核心知识点逐个展开） |
| 章节含标准库源码解读 | C（嵌入 A-⑬ 或 B-真实源码） |
| 章节需可运行示例/项目 | D（嵌入 A-⑫ 或 B-工程应用） |
| 面试/误区/FAQ 库条目 | 直接写入 Interview/MISCONCEPTIONS/FAQ 对应 .md，并交叉引用章节 |

## 一致性自检（每章收尾）

- [ ] 使用了模板 A 的 20 元素（无"推荐阅读"独立节）
- [ ] 核心知识点用模板 B，整章累计示例 ≥30
- [ ] 源码节用模板 C（有真实路径+行号+逐行）
- [ ] 工业案例用模板 D（可编译+构建命令）
- [ ] 立场分层标签 [标准]/[实现]/[平台]/[经验] 正确
- [ ] 新术语已入 glossary.json，章节已登记 INDEX.md

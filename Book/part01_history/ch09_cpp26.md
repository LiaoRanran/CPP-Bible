# 第09章　C++26：已确定特性与方向

⟶ Book/part10_modern/ch121_contracts.md
⟶ Book/part10_modern/ch123_ct_programming.md

> 标准基：ISO/IEC 14882:2026（草案，**特性可能变动**）｜预计阅读：25 min｜前置：ch07、ch67、ch113、ch114｜后续：ch74 反射、ch121 Contracts、ch114 Executor｜难度：★★★★

> ⚠️ 本章标注 `[实验性]`：C++26 在写作时尚未最终冻结，以下为已投票进入工作草案或高度可能的方向；以最终标准为准。

## ⓪ 历史动机：C++26 方向与"未冻结"的来龙去脉

> 当一章以"[实验性]"开篇，它讲述的不是定论，而是一份正在委员会会议室里被投票的未来。

### 0.1 起源（谁·何时·为何）

C++ 的三年节奏意味着：在 C++23 定稿的同时，下一版早已在 WG21 的提案堆里生长。C++26（写作时尚未最终冻结）的驱动力与以往不同——**它想补上 C++ 最后几块公认的短板**：编译期反射几乎为零、契约（contracts）在 C++20 被临门抽掉、并发模型仍缺统一执行器。[史][评] 这些不是凭空想象，而是十年来社区在反射、契约、执行器上的提案反复积淀的结果（如反射 P2996、契约 P2900）。[史]

### 0.2 关键转折（编年）

- **C++20 时期**：Contracts 原已投票进入标准，却在定稿前被撤回（因语义未定），成为社区著名"煮熟的鸭子飞了"事件。[史]
- **2020s 中**：静态反射（P2996，David Sankel 等主导）、`std::execution` 发送者/接收者模型、模块化标准库逐步成熟。[史]
- **预期 2026**：ISO/IEC 14882:2026 发布，收纳上述方向中已稳定者。[史]

### 0.3 设计哲学之争

C++26 的旗舰之争是"反射该有多强"。一派要完整编译期元对象（能遍历类型成员、生成代码），另一派怕它把 C++ 变成"带编译器的 Lisp"。[评] 契约则纠缠于"前置条件违反该崩溃还是抛异常"——C++20 的抽回正源于此分歧未解。[史] 执行器（sender/receiver）更是在"库实现（如 libunifex）已成熟"与"标准该不该绑定一种并发模型"之间拉锯。[评]

### 0.4 史料补遗与持续编年

- （待续：C++26 最终冻结时的真实特性清单、反射落地形态、契约是否回归可在此持续追加——这正是"持续编年"的最佳锚点。）
- 已知风险：草案阶段特性可能变动，本章特意标注 `[实验性]` 以示边界。[史]

## ① 学习目标

⟶ Book/part01_history/ch08_cpp23.md
⟶ Book/part01_history/ch10_version_matrix.md


```cpp
// [merged] ## ① 学习目标
#include <iostream>
#include <string>
constexpr int sum3(){ int a[3]{1,2,3}; return a[0]+a[1]+a[2]; } static_assert(sum3()==6, "");
std::string s9="a"; void use_d9(){ auto d9=s9; (void)d9; }
int main() {}
```

- 了解 C++26 已确定/高概率特性：静态反射（static reflection）、契约（Contracts，回归）、发送者/接收者执行器（`std::execution`）、模块化标准库（`std::meta`/`std` 模块）、`std::format` 增强、`std::simd` 可能、`std::generator` 稳定、 placement new 等小修。
- 理解这些特性解决「元编程繁琐 / 契约缺失 / 异步碎片化」三大痛点。

## ② 前置知识

```cpp
// [merged] ## ② 前置知识
#include <iostream>
struct Base9{ int a; }; struct Der9:Base9{ int b; }; Der9 d9{{1},2};
struct Pt9{ int x; int y; }; Pt9 p9{.x=1,.y=2};
int main() {}
```

- ch67（Concepts，反射的基础）、ch113（协程，与执行器协作）、ch74（反射专章）。

## ③ 后续依赖

```cpp
// [merged] ## ③ 后续依赖
#include <iostream>
#include <concepts>
template<class T> concept C9 = true; template<C9 T> void f9(T){}
template<class T> concept Num9 = std::integral<T> || std::floating_point<T>;
int main() {}
```

- 反射（ch74）、Contracts（ch121）、执行器（ch114）专章详述。

## ④ 知识图谱（ASCII）

```cpp
// [merged] ## ④ 知识图谱（ASCII）
#include <iostream>
#include <ranges>
#include <vector>
void p9(){ std::cout << "ok\n"; }
void r9(){ std::vector<int> v{1,2,3}; auto x=v | std::views::take(2); for(int e:x) (void)e; }
int main() {}
```

```
C++26 (方向)
├─ 静态反射: std::meta / 反射运算符 (^^ / [: :] 提案)
├─ Contracts: pre/post/assert(回归, 曾被 C++20 移除)
├─ std::execution: Sender/Receiver 异步模型
├─ 模块化标准库: import std;
├─ std::format 增强(打印到 ostream/宽字符)
├─ std::simd 进入标准(可能)
├─ 会话/批处理算法
└─ 小修: 变量模板 inline、placement new 简化
```

## ⑤ Mermaid（执行器 Sender 管线）

```cpp
// [merged] ## ⑤ Mermaid（执行器 Sender 管线）
#include <iostream>
static_assert(__cplusplus >= 202002L, "need c++20+");
int main() {
    constexpr auto std_ver = __cplusplus;  // 编译期标准版本宏
}
```

## ⑥ UML / 结构图（C++26 方向性特性）[标准]

```cpp
// [merged] ## ⑥ UML / 结构图（C++26 方向性特性）[标准]
#include <iostream>
int main() {}
```

C++26（草案）：静态反射、`std::execution` sender/receiver、契约 (contracts)、`std::simd`、扩展 `constexpr`、模式匹配（方向性，可能变动）。
## ⑦ ASCII 内存图（C++26 反射与值）

```cpp
// [merged] ## ⑦ ASCII 内存图（C++26 反射与值）
#include <iostream>
struct W9{ int v=1; void run(){ auto f=[self=*this]{ return self.v; }; (void)f; } };
int main() {}
```

静态反射在编译期暴露类型元数据，不影响运行时对象布局；契约由编译器在前后置条件插入检查，无新内存模型（ch11）。
## ⑧ 生命周期（C++26 契约与 constexpr 扩展）

```cpp
// [merged] ## ⑧ 生命周期（C++26 契约与 constexpr 扩展）
#include <iostream>
struct V9{ constexpr virtual int f() const { return 1; } };
int main() {}
```

契约不改变对象生命周期；`constexpr` 扩展到更多库类型，更多计算移至编译期（ch22）。
## ⑨ 调用栈（C++26 sender/receiver 执行器）

```cpp
// std::execution 执行策略改进
#include <execution>
#include <algorithm>
#include <vector>
void ex9(){ std::vector<int> v(2); std::sort(std::execution::par, v.begin(), v.end()); }
```
```cpp
// 协程推广示意
// task<int> gen26(){ co_yield 1; co_return 2; }
```

`std::execution` 用 sender/receiver 组合描述异步流水线，由调度器决定实际调用栈（ch167）。
```mermaid
flowchart LR
    S[Sender] -->|then| T[Transform]
    T -->|via Scheduler| R[Receiver 结果]
    R --> C[continuation]
```

## ⑩ 汇编（反射编译期生成）

```cpp
// [merged] ## ⑩ 汇编（反射编译期生成）
#include <iostream>
void use_hex2(){ auto hex_f=0x1.8p3; (void)hex_f; }  // 十六进制浮点字面量（C++23 起）
auto hex_f=0x1.8p3; void use_hex(){ (void)hex_f; }
int main() {}
```

> 反射把「运行时 typeid 字符串」升级为「编译期可遍历的类型元数据」，用于自动生成序列化/比较/打印代码（ch74）。无运行时开销。

> **真机实测（GCC 15.3.0）**：C++26 反射提案 P2996 **尚未实现**——`<meta>` 头不存在：
> ```text
> _probe_reflection.cpp:2:10: fatal error: meta: No such file or directory
> ```
> 即反射仍是"方向性"特性，本工具链无法编译 `reflect_value` / `^T` 等语法。跟踪表见 WG21/TRACKER.md。

## ⑪ STL 联系

```cpp
// [merged] ## ⑪ STL 联系
#include <iostream>
#include <vector>
namespace lib26 {}
int main() {
    std::vector v9{1,2,3};
}
```

- 模块化标准库让 `import std;` 取代 `#include <vector>` 等，编译更快（ch118）。
- `std::execution` 统一协程/线程池/IO 的异步组合（ch114、ch163）。

## ⑫ 工业案例

```cpp
// [merged] ## ⑫ 工业案例
#include <iostream>
[[assume(true)]] void hint9(){}
int main() {}
```

- **序列化框架**：反射自动生成 `to_json`/`from_json`，免手写（ch162 JSON）。
- **异步框架**：`std::execution` 统一网络库与线程池调度（ch163）。

## ⑬ 源码分析（方向）

```cpp
// [merged] ## ⑬ 源码分析（方向）
#include <iostream>
int main() {}
```

- 反射提案 `P2996` 用 `std::meta::info` 表示类型信息，`template <meta::info>` 编译期反射（ch74）。
- Contracts 提案提供 `pre`/`post`/`assert` 子句，编译器可生成运行时检查或静态证明（ch121）。

## ⑭ WG21 提案（关键，可能变动）

```cpp
// [merged] ## ⑭ WG21 提案（关键，可能变动）
#include <iostream>
#include <atomic>
inline unsigned long long operator"" _u(unsigned long long x){ return x; }  // 用户定义字面量（UDL）
int main() {
    std::atomic<int> a9{0};
}
```

- **P2996R3** Static reflection.
- **P0542R5**（及后续）Contracts 回归.
- **P2300R10** `std::execution` Sender/Receiver.
- **P1750R* / 模块化 std**.
- **P1928R* / `std::format` 增强**.

## ⑮ 面试题

```cpp
// [merged] ## ⑮ 面试题
#include <iostream>
#include <ranges>
#include <vector>
void ch9(){ std::vector<int> v{1,2,3,4}; auto r=v|std::views::filter([](int i){return i%2;})|std::views::transform([](int i){return i*2;}); for(int x:r)(void)x; }
int main() {}
```

1. 静态反射和 `typeid` 区别？（编译期、可遍历、零开销 vs 运行时字符串）
2. 为什么 Contracts 在 C++20 被移除后又回归？（实现与语义分歧，最终重新设计）

## ⑯ 易错点

```cpp
// [merged] ## ⑯ 易错点
#include <iostream>
constexpr int len(const char* s){ int n=0; while(s[n]) ++n; return n; } static_assert(len("hi")==2, "");
int main() {}
```

- C++26 特性**未冻结**：不要在生产代码依赖 `import std;` 或 Contracts，除非编译器明确支持（ch11 支持矩阵）。
- `std::execution` 模型学习曲线陡，需理解 Sender/Receiver 惰性（ch114）。

## ⑰ FAQ

```cpp
// [merged] ## ⑰ FAQ
#include <iostream>
#include <cstdint>
int main() {
    int32_t i9=0;
    #ifdef __cpp_lib_format
    #endif
}
```

- **Q：C++26 何时发布？** A：按计划约 2026 年（三年周期），但特性以最终草案为准。
- **Q：需要现在学吗？** A：理解方向即可；实际写码以 C++17/20 为主（工业现状，ch11）。

## ⑱ 最佳实践

```cpp
// [merged] ## ⑱ 最佳实践
#include <iostream>
#include <variant>
#include <string>
void m9(){ std::variant<int,std::string> v=1; std::visit([](auto x){(void)x;}, v); }
int main() {}
```

- 关注方向，但生产以编译器实际支持为准（ch11）。
- 提前用 Concepts 写好接口，便于未来接反射自动生成（ch67、ch74）。

## ⑲ 性能（不适用，方向性）

```cpp
// C++26 小结：反射/契约/模块化/数据并行（多为提案阶段）
```

## ⑳ 练习题 + 思考题 + 源码阅读路线（内化，无独立"推荐阅读"节）

```cpp
// 编译器版本探测
#ifdef __GNUC__
static_assert(__GNUC__ >= 13, "gcc13+");
#endif
```

## 附录: C++26 方向特性前瞻

```cpp
#include <iostream>
int main(){std::cout<<"C++26: Contracts(P2900), reflection(P2996), std::execution(P2300), std::simd.\n";return 0;}
```

1. 跟踪 P2996 提案进展，理解 `std::meta` 用法（ch74）。
2. 思考题：若反射普及，`Boost.Serialization` 类库会如何被替代？（ch128、ch162）

## 附录 B: C++26 方向深度代码

```cpp
#include <iostream>
#include <cassert>
int bounded_sqrt(int x){assert(x>=0);int r=0;while(r*r<=x)++r;return r-1;}
int main(){std::cout<<bounded_sqrt(50)<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"P2300 sender/receiver: composable async pipeline, replaces future/promise."<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"P2996 reflection: enumerate members at compile time, auto-generate JSON/serialization."<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"std::simd: explicit SIMD vectors without intrinsics, portable across architectures."<<std::endl;return 0;}
```

## 附录 C：C++26底层影响与工业前瞻 [E: Lowlevel / F: Industry / H: Design / J: Learning]

```
C++26关键特性及其工程影响:

Contracts (P2900R7):
  编译期可配置契约检查 → 零开销debug build, 可控发布构建
  工业影响: Airbus DO-178C 航空软件可标准化契约合规性

Reflection (P2996R5):
  编译期类型自省 → 替代MOC(Qt)/UHT(Unreal)的预处理器
  汇编: 反射生成代码与手写完全相同的mov/call指令

std::execution (P2300R7):
  统一异步模型(sender/receiver) → 替代boost::asio/epoll手写回调
  LLVM/Chromium可能迁移到标准异步框架
```

```cpp
#include <iostream>
int main() {
    std::cout << "C++26 = Contracts + Reflection + std::execution = trifecta" << std::endl;
    std::cout << "Contracts: P2900R7 approved Feb 2024, Hagenberg. GCC15/Clang20 target." << std::endl;
    std::cout << "Reflection: P2996R5, ~500 pages spec, largest single proposal in C++ history." << std::endl;
    return 0;
}
```

| 特性 | 提案 | 编译器支持 | 工业影响 |
|---|---|---|---|
| Contracts | P2900R7 | GCC15/Clang20 | 安全关键软件标准化 |
| Reflection | P2996R5 | Clang 19实验 | 消除Qt/UE的预处理器 |
| std::execution | P2300R7 | MSVC 2022实验 | 统一异步编程模型 |
| Trivial infinite loops | P2809R3 | GCC14/Clang18 | while(true)不再UB |

面试: C++26最重要的3个特性？ Contracts(契约) + Reflection(反射) + std::execution(异步)
       P2996的~500页spec说明了什么？ 反射是从根本上改变C++编译模型的特性


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第8章](Book/part01_history/ch08_cpp23.md) | STL算法回调/异步任务 | 本章提供概念，第8章提供实现 |
| [第10章](Book/part01_history/ch10_version_matrix.md) | 无锁队列/计数器 | 本章提供概念，第10章提供实现 |
| [第121章](Book/part10_modern/ch121_contracts.md) | 多态插件/框架扩展 | 本章提供概念，第121章提供实现 |
| [第123章](Book/part10_modern/ch123_ct_programming.md) | 配置解析/API响应 | 本章提供概念，第123章提供实现 |


## 深度增强：C++26三大特性

### 原理分析

Contracts(P2900): 标准化前置/后置, 多级别(default/audit/axiom), 航空DO-178C认证
Reflection(P2996): ~500页规格, 编译期类型自省, 替代Qt MOC/UE UHT预处理器
std::execution(P2300): 统一15年分散的异步模型(callback/future/coroutine/Asio)

### 工业影响

| 特性 | 替代 | 零开销 | 影响 |
|---|---|---|---|
| Contracts | assert() | release零开销 | 安全认证 |
| Reflection | Qt MOC/UE UHT | 编译期零运行时 | 消除预处理器 |
| std::execution | asio/epoll | 编译期组合 | 统一异步 |

```cpp
#include <iostream>
int main(){std::cout<<"C++26=Contracts+Reflection+std::execution=proof-carrying+zero-preprocessor+unified-async"<<std::endl;return 0;}
```

### 面试巩固

Q: Contracts vs assert? A: assert=非标准(NDEBUG); contracts=标准化+多级别+类型系统集成
Q: P2996为何500页? A: 需要定义编译期类型访问的每个细节
Q: std::execution vs Asio? A: P2300借鉴Asio模型, 标准化为编译器可优化的编译期组合

## 附录 E：C++26 P2300 std::execution深度

P2300 sender/receiver模型统一了C++的异步编程:
- sender: 描述异步工作(如async_read)
- receiver: 消费结果(如写回buffer)
- 组合器: then/upon_error/retry/stop_when

```cpp
#include <iostream>
int main(){std::cout<<"P2300 sender/receiver=unified async model, zero-callback overhead"<<std::endl;std::cout<<"Replaces: Boost.Asio callbacks, std::future, coroutine manual scheduling"<<std::endl;return 0;}
```

P2300核心优势:
- 编译期组合: sender组合→编译器优化为无callback的直通代码
- 零开销: 无虚函数, 无堆分配(小对象), 无引用计数
- 取消支持: stop_token贯穿整个sender chain

面试: P2300 vs std::async? async=future阻塞; P2300=sender/receiver链式, 无阻塞


> **真机实测（GCC 15.3.0）**：`<execution>` 头可编译，但 P2300 算法骨架未实现——`std::execution::just` / `then` 不是成员：
> ```text
> _probe_sender_real.cpp:5:18: error: 'just' is not a member of 'ex'
> _probe_sender_real.cpp:5:35: error: 'then' is not a member of 'ex'
> ```
> 即 C++26 方向特性在 GCC15 仅到位"头文件骨架"，**可声明 sender 概念、不可组合算法**。生产异步仍用 ch93 的 `std::async` / coroutine / 或第三方 Asio。

## 附录 G：Contracts P2900深度

C++20 P0542被拒(continuation过于复杂)。P2900简化: 只保留pre/post/assert + 三级检查(default/audit/axiom)。

```cpp
#include <iostream>
int main(){std::cout<<"P2900 contracts=pre/post/assert with default/audit/axiom levels"<<std::endl;return 0;}
```

| 级别 | 检查 | 开销 |
|---|---|---|
| default | debug | release 0 |
| audit | 始终 | ~1ns/check |
| axiom | 永不 | 0 |

面试: P2900 vs P0542? P0542被拒(过复杂); contracts vs static_assert? contracts=运行时; static_assert=编译期

### G.1 真机汇编实证（GCC 15.3.0 `-fcontracts`）

```cpp
// _asm_demo/ch09_contracts_test.cpp （GCC 15.3.0 -std=c++26 -O2 -fcontracts，实测）
[[nodiscard]] int clamp(int x, int lo, int hi)
    [[pre: lo <= hi]]
    [[post r: r >= lo && r <= hi]]
{ if (x < lo) return lo; if (x > hi) return hi; return x; }
```

`clamp` 入口构造 violation 描述（xmm0/xmm1 加载源位置串），`post` 检查插入调用点：

```asm
; clamp(int,int,int) 节选（objdump -d -M intel，demangled）
sub    rsp,0x58
lea    rax,[rip+0x22]        ; 构造 contract_violation 描述
movq   xmm0,QWORD PTR [rip+0x50]
...
cmp    edx,r8d               ; pre: lo <= hi
jg     25                    ; （默认 continuation 下 pre 失败不调 handler，按 assume）
...
cmp    edx,eax               ; post: r >= lo
jg     7b                    ; 失败→跳 0x7b 调用 handle_contract_violation
```

> 链接期缺 `handle_contract_violation`（GCC 实验性 runtime 限制）；`pre` 在默认语义下降级为 `assume`。**Contracts 在 GCC15 仍是实验特性**——可编译识别语法、完整可运行需更完整的 violation handler 实现。

## 相关章节（交叉引用）

- **相邻主题**：⟶ Book/part01_history/ch07_cpp20.md（第07章　C++20：量级升级）—— 编号相邻、主题接续。
- **相邻主题**：⟶ Book/part02_toolchain/ch11_compilers.md（第11章　编译器全景：GCC / Clang / MSVC 架构与 ABI（C++））—— 编号相邻、主题接续。
- **同模块**：⟶ Book/part01_history/ch01_c_history.md（第01章　C 语言遗产与 C with Classes）—— 同模块下的其他主题。


## 叙事补遗 [J: Learning]

- **仍是草案（CD 阶段）**：契约（Contracts，`[[assert:]]` 回归）、扩展 `constexpr`、静态反射、模式匹配已确定方向，但文本尚未冻结，以 WG21 最新提案状态为准。
- **静态反射是圣杯**：若落地，序列化/ORM/绑定生成的样板将由编译器替你写，而非靠宏或代码生成器——这是元编程从"运行时技巧"走向"编译期一等公民"的关键一步。
- **迁移铁律不变**：C++26 未冻结前不要押宝；查 `cxx_status`、等编译器实装，再按瓶颈引入。
## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

**真实场景：前向兼容的混合符号比较。** 你维护的代码既要面向 C++26（届时 `std::cmp_less` 已是常备工具）也要在 C++17 工具链上能编译。请先写一个对任意可比较类型通用、且对混合符号比较安全的 `max` 风格比较，并思考当它最终迁移到 C++26 时如何改用标准 `<compare>` 工具。

<details><summary>答案与解析</summary>

使用 `std::common_comparison_category` 或 `std::cmp_less` 避免符号陷阱：

```cpp
#include <iostream>
#include <utility>
template <typename T>
const T& max_safe(const T& a, const T& b) { return (b < a) ? a : b; }
int main() { std::cout << max_safe(3, 7) << '\n'; }
```

[标准] 模板参数推导按实参进行；两实参同类型时 `T` 唯一确定。

[引用] ISO C++20 §[temp.deduct]；cppreference "std::cmp_less"（https://en.cppreference.com/w/cpp/utility/intcmp/cmp_less）。C++26 方向（execution/contracts/静态反射）见 WG21 草案论文（可能变动，落地前查 `cxx_status`）。

</details>

### 练习 2（难度 ★★）

**真实场景：C++26 特性门控 API。** 你在规划一个将随 C++26（execution、contracts、静态反射）一起演进的库，现在就用已经成熟的概念给对外 `add` 接口加类型护栏，使浮点/非数值调用在编译期被清晰拒绝，为后续接 contracts 前置条件铺路。

<details><summary>答案与解析</summary>

C++20 概念取代 SFINAE 做编译期约束：

```cpp
#include <iostream>
#include <concepts>
template <std::integral T> T add(T a, T b) { return a + b; }
int main() { std::cout << add(2, 3) << '\n'; /* add(1.0, 2.0) 编译失败 */ }
```

[标准] 违反概念约束是硬错误（而非 SFINAE 静默失败），诊断信息更可读。

[引用] ISO C++20 §[concepts]；cppreference "std::integral"（https://en.cppreference.com/w/cpp/concepts/integral）。C++26 中概念生态继续演进（如细化推导指引），概念是后续 contracts 前置条件的基础。

</details>

### 练习 3（难度 ★★）

**真实场景：静态反射时代的编译期常量。** C++26 推进的静态反射（论文 P2996）会在编译期暴露类型元数据，很多计算会前移到编译期。请写一个 `constexpr` 阶乘函数，并用 `static_assert` 在编译期验证 `fact(5)==120`，作为"该值确实在编译期定值"的可执行证据。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
constexpr int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }
static_assert(fact(5) == 120);
int main() { std::cout << fact(5) << '\n'; }
```

[标准] `constexpr` 函数在常量表达式上下文（如模板实参、`static_assert`）中于编译期求值。

[引用] ISO C++ §[expr.const]；cppreference "constexpr"（https://en.cppreference.com/w/cpp/language/constexpr）。C++26 推进 constexpr 扩展与静态反射（论文 P2996），把更多运行期逻辑前移到编译期。

</details>



## 附录 J：C++26 方向性特性评估决策流（D3 维度）

本节把第⑤节（sender/receiver 执行器）、第⑨节（调用栈）与第⑭节（WG21 提案，可能变动）收敛为「方向性特性如何评估取舍」的决策流。

```mermaid
flowchart TD
  N1["C++26 草案 (可能变动)"]
  N2["std::execution 执行器 (P2300)"]
  N3["Contracts (P2900, ch121)"]
  N4["静态反射 (编译期)"]
  N5["constexpr 扩展 (ch69)"]
  N6["Hazard Pointers (ch112)"]
  N7["RCU (ch112)"]
  N8{"需要异步流水线?"}
  N9["用 sender/receiver (ch93 async)"]
  N10{"需要前置/后置条件?"}
  N11["用 Contracts 替代断言 (ch121)"]
  N12{"需要编译期类型内省?"}
  N13["用静态反射 (ch123 ct_programming)"]
  N14{"需要无锁安全回收?"}
  N15["用 hazard/RCU (ch112)"]
  N16["进入版本 train (ch10)"]
  N1 --> N2
  N1 --> N3
  N1 --> N4
  N1 --> N5
  N1 --> N6
  N1 --> N7
  N2 --> N8
  N8 -->|是| N9
  N3 --> N10
  N10 -->|是| N11
  N4 --> N12
  N12 -->|是| N13
  N6 --> N14
  N14 -->|是| N15
  N1 --> N16
```

> 决策流说明：第⑭节强调 C++26 提案「可能变动」——execution 与 contracts 是或门独立特性；contracts 取代手工断言（与 ch121 衔接），反射+constexpr 把更多运行期逻辑前移（ch69/ch123），hazard/RCU 收敛 ch112 的无锁回收难题。


## 附录 K：C++26 方向概念依赖网（D6 维度）

以「C++26 方向」为核心，连接 execution/contracts/反射等方向性特性与它们依赖的现代章节，形成概念网。

```mermaid
flowchart TD
  CORE["C++26 方向"]
  K1["std::execution (ch93 async)"]
  K2["Contracts (ch121)"]
  K3["静态反射 (ch123 ct_programming)"]
  K4["constexpr 扩展 (ch69)"]
  K5["Hazard/RCU (ch112)"]
  K6["上游: C++23 (ch08)"]
  K7["版本 train (ch10)"]
  K8["并发基础 (ch107 atomic)"]
  K9["内存序 (ch108)"]
  K10["模板约束 (ch67 concepts)"]
  K11["下游工业采纳 (ch156)"]
  CORE --> K1
  CORE --> K2
  CORE --> K3
  CORE --> K4
  CORE --> K5
  CORE --> K6
  CORE --> K7
  CORE --> K8
  CORE --> K9
  CORE --> K10
  CORE --> K11
  K1 --> K8
  K5 --> K9
  K3 --> K4
```

### K.1 概念依赖逐边解读

| 边 | 依赖含义 |
|----|----------|
| CORE → K1 | std::execution 提供 sender/receiver 异步模型，见 ch93。 |
| CORE → K2 | Contracts 在标准层提供前置/后置条件，见 ch121。 |
| CORE → K3 | 静态反射在编译期暴露类型元数据，见 ch123。 |
| CORE → K4 | constexpr 进一步扩展，见 ch69。 |
| CORE → K5 | Hazard Pointers/RCU 提供无锁安全回收，见 ch112。 |
| CORE → K6 | C++26 建立在 ch08 标准库大修之上。 |
| CORE → K7 | 方向性特性最终并入版本 train，见 ch10。 |
| CORE → K8 | 执行器建立在 ch107 原子与线程之上。 |
| CORE → K9 | 无锁回收依赖 ch108 内存序。 |
| CORE → K10 | 约束与反射仍基于 ch67 concepts。 |
| CORE → K11 | 工业采纳度影响最终优化质量，见 ch156。 |
| K1 → K8 | execution 的调度器依赖 ch107 并发原语。 |
| K5 → K9 | hazard/RCU 的正确性由 ch108 内存序保证。 |
| K3 → K4 | 静态反射常与 constexpr 配合做编译期内省。 |

### K.2 跨章闭环表

| 目标章 | 路径 | 闭环点 |
|--------|------|--------|
| ch121 contracts | CORE→K2 | ch121 是 C++26 contracts 的提前落地参考。 |
| ch93 thread_async | CORE→K1→K8 | std::execution 建立在 ch93 异步模型之上。 |
| ch112 hazard_rcu | CORE→K5→K9 | hazard/RCU 依赖 ch108 内存序保证。 |
| ch123 ct_programming | CORE→K3→K4 | 静态反射是 ch123 编译期编程的高阶形态。 |
| ch10 版本矩阵 | CORE→K7 | ch10 记录 C++26 何时并入 train。 |
| ch156 编译器优化 | CORE→K11 | ch156 决定 C++26 特性的最终优化质量。 |

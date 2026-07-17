# 第10章　版本特性全景对照表与迁移指南

⟶ Book/part01_history/ch04_cpp11.md
⟶ Book/part01_history/ch07_cpp20.md
⟶ Book/part16_reading/ch165_roadmap.md

> 标准基：C++98 → C++26｜预计阅读：20 min｜前置：ch03–ch09｜后续：全书｜难度：★★

## ① 学习目标

⟶ Book/part01_history/ch09_cpp26.md


```cpp
// [merged] ## ① 学习目标
#include <iostream>
void show_ver(){ std::cout << __cplusplus; }
static_assert(__cpp_concepts >= 201707L, "");
int main() {
    #ifdef __cpp_concepts
    #endif
}
```

- 一张表纵览各版本关键特性、动机、提案、对你代码的影响。
- 掌握「从 C++98/11 项目迁移到现代标准」的实操路径。

## ② 前置知识

```cpp
// [merged] ## ② 前置知识
#include <iostream>
int main() {
    #ifdef __cpp_modules
    #endif
    #ifdef __cpp_lib_ranges
    #endif
}
```

- ch03–ch09 各版本章。

## ③ 后续依赖

```cpp
// [merged] ## ③ 后续依赖
#include <iostream>
int main() {
    #ifdef __cpp_lib_format
    #endif
    #ifdef __cpp_lib_three_way_comparison
    #endif
}
```

- 作为速查表，后续每章可回查「该特性属于哪版」。

## ④ 对照总表

```cpp
// [merged] ## ④ 对照总表
#include <iostream>
int main() {
    #ifdef __cpp_impl_coroutine
    #endif
    #ifdef __cpp_structured_bindings
    #endif
}
```

| 版本 | 标志特性 | 关键提案 | 解决痛点 | 工业影响 |
|---|---|---|---|---|
| C++98 | 模板/异常/RTTI/STL/string/iostream | ARM 蓝本 | 首个 ISO 标准 | 工业 C++ 奠基 |
| C++03 | 值初始化修复 | — | 修 98 缺陷 | ≈98 |
| C++11 | auto/range-for/lambda/move/智能指针/constexpr/thread/unordered | N3337 | 资源管理+泛型革命 | 现代 C++ 起点 |
| C++14 | 泛型 lambda/返回推导/make_unique/放宽 constexpr | N4140 | 11 补全 | 平滑过渡 |
| C++17 | 结构化绑定/if-init/string_view/optional/variant/filesystem/并行算法/折叠 | N4659 | 生产力 | 广泛可用 |
| C++20 | Concepts/Modules/Coroutines/Ranges/<=>/span/jthread/format | N4861 | 模板可用、模块化、异步 | 量级升级 |
| C++23 | expected/flat_map/print/stacktrace/mdspan/ranges 适配 | N4950 | 库大修 | 库现代化 |
| C++26 | 反射/Contracts/执行器/模块化 std（方向） | 进行中 | 元编程/契约/异步统一 | 预览 |

## ⑤ 迁移指南

```cpp
// [merged] ## ⑤ 迁移指南
#include <iostream>
int main() {
    #ifdef __cpp_if_constexpr
    #endif
    #if __cplusplus >= 201103L
    #endif
}
```

### 从 C++98 → C++11/14
1. 把裸 `new`/`delete` 换成智能指针（ch48）。
2. 用 `auto` + 范围 for 替换手写迭代器循环（ch22、ch90）。
3. 用 `nullptr` 替换 `NULL`/`0`（ch19）。
4. 用 `enum class` 替换裸 `enum`（ch25）。
5. 用 `override`/`final` 标注虚函数（ch52）。

### 从 C++11/14 → C++17
1. 函数字符串参数用 `string_view`（ch82）。
2. 返回「可能无值」用 `optional`（ch88）。
3. 多类型字段用 `variant`+`visit`（ch26、ch138）。
4. 文件操作用 `std::filesystem`（ch91）。
5. 并行算法加 `execution::par`（ch99）。

### 从 C++17 → C++20
1. 模板约束用 Concepts（ch67）。
2. 数据管道用 Ranges（ch90）。
3. 新项目用 Modules（ch118）。
4. 异步用 Coroutines / jthread（ch113、ch94）。
5. 格式化用 `std::format`（ch131）。

### 从 C++20 → C++23
1. 可恢复错误用 `expected`（ch88）。
2. 读多写少映射用 `flat_map`（ch83）。
3. 输出用 `std::print`（ch131）。
4. 诊断用 `std::stacktrace`（ch14）。

## ⑥ 编译器支持矩阵（要点，详见 ch11）

```cpp
// [merged] ## ⑥ 编译器支持矩阵（要点，详见 ch11）
#include <iostream>
int main() {
    #if __cplusplus >= 201402L
    #endif
    #if __cplusplus >= 201703L
    #endif
}
```

- GCC：C++17 自 7 起较全，C++20 自 10/11 逐步，C++23 持续补全。
- Clang：与 GCC 接近，modules/concepts 支持早。
- MSVC：C++20 支持度高，modules 较成熟；部分 C++23 滞后。
> 生产选型：以「团队编译器最低版本」决定可用标准（ch11）。

## ⑦ 版本演进 Mermaid

```cpp
// [merged] ## ⑦ 版本演进 Mermaid
#include <iostream>
int main() {
    #if __cplusplus >= 202002L
    #endif
    #if __cplusplus >= 202302L
    #endif
}
```

## ⑧ 生命周期（版本矩阵本身无生命周期语义）

```cpp
// [merged] ## ⑧ 生命周期（版本矩阵本身无生命周期语义）
#include <iostream>
#include <version>
int main() {
    #ifdef __GNUC__
    int gcc_major = __GNUC__;
    #endif
}
```

各标准版本的对象生命周期规则见对应章（ch19 存储期、ch39 RAII、ch47 析构）；本章只横向对照版本差异。
## ⑨ 调用栈 / ABI（见 ch11、ch47）

```cpp
// [merged] ## ⑨ 调用栈 / ABI（见 ch11、ch47）
#include <iostream>
int main() {
    #ifdef _MSC_VER
    int msc = _MSC_VER;
    #endif
    #ifdef __GLIBCXX__
    int libstdcxx = __GLIBCXX__;
    #endif
}
```

调用约定与 ABI 由各编译器与平台决定，标准仅规定行为；版本迁移时重点关注 ABI 兼容性。
```mermaid
flowchart LR
    98 --> 03 --> 11 --> 14 --> 17 --> 20 --> 23 --> 26
```

## ⑩ 自检（每版一条）

```cpp
// 平台宏 _WIN32 / __linux__
#ifdef _WIN32
#endif
#ifdef __linux__
#endif
```
```cpp
// 检测 64 位平台
static_assert(sizeof(void*)==8, "64-bit");
```

## ⑪ STL 联系（各版标准库演进）

```cpp
// [merged] ## ⑪ STL 联系（各版标准库演进）
#include <iostream>
int main() {
    #if defined(__cpp_concepts) && defined(__cpp_lib_ranges)
    #endif
}
```

C++11 起 STL 大幅扩展（智能指针、区间、并发）；C++17/20 加入 `string_view`/`<filesystem>`/Ranges；演进全貌见 ch76–ch110。
## ⑫ 工业案例（编译器/库对标准的跟进节奏）

```cpp
// [merged] ## ⑫ 工业案例（编译器/库对标准的跟进节奏）
#include <iostream>
#include <ranges>
int main() {
    #if __cplusplus >= 202002L
    #endif
}
```

GCC/Clang/MSVC 与 libc++/libstdc++/MS STL 对新课标的支持普遍滞后 1–3 年，直接影响代码可移植性与上线节奏。
## ⑬ 源码分析（标准文本即规范源码）

```cpp
// [merged] ## ⑬ 源码分析（标准文本即规范源码）
#include <iostream>
int main() {
    #ifndef __cpp_concepts
    #error "need concepts"
    #endif
    #ifdef __cpp_modules
    #endif
}
```

C++ 标准文本（ISO/IEC 14882）与 WG21 提案、编译器前端实现共同构成「规范级源码」；研读草案比二手博客更可靠。
## ⑭ WG21 提案背景 [标准]

```cpp
// [merged] ## ⑭ WG21 提案背景 [标准]
#include <iostream>
int main() {
    #ifdef __cpp_impl_coroutine
    #endif
    #ifdef __cpp_lib_reflection
    #endif
}
```

标准由提案（Proposal）驱动，约每三年发布一版；提案状态、投票记录公开于 open-std.org，可追溯到每条特性的来龙去脉。
- 98：模板/异常/STL ✓
- 11：move/lambda/smartptr ✓
- 14：generic lambda ✓
- 17：string_view/optional/variant/filesystem ✓
- 20：concepts/modules/ranges/coroutine ✓
- 23：expected/print/flat_map ✓
- 26：reflection/contracts(方向) ✓

## ⑮ 面试题

```cpp
// [merged] ## ⑮ 面试题
#include <iostream>
#include <string_view>
int main() {
    std::string_view v10{"c++"};
}
```

## ⑯ 易错点（版本混用陷阱）

```cpp
// [merged] ## ⑯ 易错点（版本混用陷阱）
#include <iostream>
#include <string>
std::string stdlib_ver();
void noex10() noexcept {}
int main() {}
```

混用不同 `-std=` 编译单元可能导致 ODR 违规与 ABI 不一致；NDK/MSVC 对新课标支持常滞后，切勿假设「写 C++20 就能编」。
## ⑰ FAQ（迁移必读）

```cpp
// [merged] ## ⑰ FAQ（迁移必读）
#include <iostream>
int main() {
    #ifdef __cpp_lib_reflection
    #endif
}
```

- **Q：能否随意升到 `-std=c++23`？** A：需确认工具链与所有依赖库均已支持，否则链接期或运行期失败。
- **Q：如何写跨版本代码？** A：用特性测试宏 `__cpp_*` 做条件编译，而非硬编码版本号。
## ⑱ 最佳实践（版本治理）

```cpp
// 特性宏 __cpp_explicit_this_parameter（C++23 deducing this，GCC 15.3 实测 202110）
// 注意：标准宏名是 __cpp_explicit_this_parameter，非直觉的 __cpp_deducing_this（后者不存在）
#ifdef __cpp_explicit_this_parameter
#endif
```

项目显式固定 `-std=` 与编译器最低版本；用 `__cpp_*` 特性宏隔离新特性；CI 矩阵覆盖目标工具链组合。
## ⑲ 性能（标准版本 ≠ 性能）

```cpp
// 特性宏 __cpp_multidimensional_subscript（C++23）
#ifdef __cpp_multidimensional_subscript
#endif
```

性能取决于编译器实现与优化等级，与标准版本无直接因果；新特性多为零开销抽象（如 `string_view`、`<ranges>`），见 ch14/ch153。
1. 你的项目该用哪个标准？（看编译器支持 + 团队熟悉度 + 依赖库，ch11）
2. 为什么很多大厂仍锁 C++17？（生态/ABI 稳定/工具链成熟）
## ⑳ 练习题 + 思考题 + 源码阅读路线（内化，无独立"推荐阅读"节）

```cpp
// 编译期 if 检测平台
#ifdef _WIN32
const char* plat="win";
#else
const char* plat="other";
#endif
```

## 附录: 版本特性速查

```cpp
#include <iostream>
int main(){std::cout<<"C++11: move,auto,lambda,smart_ptr,constexpr,noexcept,thread\n";return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"C++17: structured_binding,if_constexpr,optional,variant,string_view,filesystem\n";return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"C++20: concepts,coroutines,ranges,modules,span,<=>\n";return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"C++23: expected,print,flat_map,views::zip,deducing_this\n";return 0;}
```

1. 评估你当前项目：列出可升级到 C++17/20 的 5 个具体改造点（依上表）。
2. 用 Compiler Explorer 对比同一函数在不同 `-std=` 下的汇编（ch157）。

## 附录 B: 版本选择决策树

```cpp
#include <iostream>
int main(){std::cout<<"New project? Start C++17 minimum. Can target C++20? Use concepts/coroutines. Embedded? C++11+ with RTOS."<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){
    std::cout<<"Decision matrix:"<<std::endl;
    std::cout<<"ABI stability required -> C++11/14 (longest support)"<<std::endl;
    std::cout<<"Modern codebase -> C++17 (sweet spot, widespread)"<<std::endl;
    std::cout<<"Cutting edge -> C++20/23 (check compiler support first)"<<std::endl;
    return 0;
}
```

```cpp
#include <iostream>
int main(){std::cout<<"Feature macro names: __cpp_lib_*, __cpp_*. Check with #if. Portable detection without version guessing."<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"GCC 13 C++23 support: ~90%. MSVC 17.8: ~95%. Clang 17: ~85%. Check cppreference for details."<<std::endl;return 0;}
```

## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第9章](Book/part01_history/ch09_cpp26.md) | 键值查找/缓存 | 本章提供概念，第9章提供实现 |
| [第7章](Book/part01_history/ch07_cpp20.md) | STL算法回调/异步任务 | 本章提供概念，第7章提供实现 |
| [第4章](Book/part01_history/ch04_cpp11.md) | 文件扫描/配置加载 | 本章提供概念，第4章提供实现 |

## 附录 E：版本选择工业与面试

C++版本选择决策树:
新项目(2024+): C++20 (concepts/ranges/coroutines已成熟)
LTS/企业: C++17 (GCC8/Clang6/MSVC2019, RHEL8)
嵌入式: C++11/14 (arm-none-eabi-gcc 9+)
安全关键: C++14 (DO-178C certified compilers)

```cpp
#include <iostream>
int main(){std::cout<<"C++11->14=minor, 14->17=productivity, 17->20=paradigm"<<std::endl;return 0;}
```

| 版本 | 编译器 | 场景 |
|---|---|---|
| C++11 | GCC 4.8+ | 嵌入式/遗产 |
| C++14 | GCC 5+ | LTS基线(Qt5.12/UE4.27) |
| C++17 | GCC 8+ | 新项目最低 |
| C++20 | GCC 10+ | 现代项目推荐 |
| C++23 | GCC 13+ | 前沿项目 |

面试: 新项目选C++17(最低)或C++20(推荐); 普及周期~3年

## 附录 G：版本升级设计权衡 [H: Design]

| 升级决策 | 收益 | 风险 | 建议 |
|---|---|---|---|
| C++11→14 | auto返回,generic lambda | 极低 | 必须 |
| C++14→17 | optional,variant,filesystem | 低(string_view) | 推荐 |
| C++17→20 | concepts,ranges,coroutines | 中(SFINAE→concepts重写) | 新项目推荐 |

```cpp
#include <iostream>
int main(){std::cout<<"Upgrade decisively: C++17 is the new minimum for new C++ projects."<<std::endl;return 0;}
```


## 深度增强：C++版本迁移成本与真实案例

### 原理分析

C++版本选择的本质是"编译器支持+库生态+团队能力+上线时间"四维约束。

WG21 train model每3年1版:
- C++11: 革命性(移动语义) → 必须升级
- C++14: 修正版 → 零成本升级
- C++17: 增量版 → 低风险(新特性可选)
- C++20: 范式版(concepts) → 中风险(SFINAE重写)

### 真实迁移案例

| 项目 | 迁移 | 成本 | 收益 |
|---|---|---|---|
| LLVM | C++14→C++17(2019) | ~50人月 | 编译快5% |
| Chromium | C++11→C++14(2018) | ~30人月 | 编译快10% |
| Google | C++14→C++17(2021) | 渐进式 | 开发者生产力 |

### 汇编验证

```asm
; C++14: 返回值=call copy_ctor → cost ~2ns
; C++17: guaranteed elision=直接构造在返回地址 → cost ~0ns
```

```cpp
#include <iostream>
#include <optional>
std::optional<int> make(){return 42;}
int main(){auto x=make();std::cout<<*x<<std::endl;return 0;}
```

### 面试巩固

Q: 新项目C++版本? A: C++17(最低)→团队有C++20经验→选C++20
Q: Google为什么不升C++20? A: 20亿行代码,需5年规划
Q: 版本迁移最大风险? A: ABI断裂(GCC5.1)和SFINAE→concepts重写


## 相关章节（交叉引用）

- **相邻主题**：⟶ Book/part02_toolchain/ch11_compilers.md（第11章　编译器全景：GCC / Clang / MSVC 架构与 ABI（C++））—— 编号相邻、主题接续。
- **相邻主题**：⟶ Book/part01_history/ch08_cpp23.md（第08章　C++23：标准库大修）—— 编号相邻、主题接续。
- **相邻主题**：⟶ Book/part02_toolchain/ch12_buildsystems.md（第12章　构建系统：Make / Ninja / CMake（C++））—— 编号相邻、主题接续。
- **同模块**：⟶ Book/part01_history/ch01_c_history.md（第01章　C 语言遗产与 C with Classes）—— 同模块下的其他主题。

## 附录 H：版本矩阵工业实践与源码对照

编译器特性支持与最低版本策略在真实项目中的落地：

| 项目/库 | 技术/模式 | 使用场景 | 源码/链接 |
|---------|----------|---------|----------|
| **Boost**（github.com/boostorg/config） | Boost.Config 用 `BOOST_CXX_*` 预处理器宏探测编译器特性 | 编译期特性探测 | `boost/config/compiler/gcc.hpp` |
| **Google/Abseil**（github.com/abseil/abseil-cpp） | 年份版本政策：明确最低 C++14/17/20 并随编译器季度升级 | 版本策略 | `absl/base/config.h` |
| **Chromium**（chromium.googlesource.com/chromium/src） | 当前最低 C++17，规划迁移 C++20，含特性灰度清单 | 项目政策 | `build/config/compiler/BUILD.gn` |
| **Qt**（code.qt.io） | Qt 6 强制最低 C++17，Qt 5 维持 C++11 | 框架基线 | `qtbase/cmake` |
| **Google** C++ Style Guide | 规定项目最低标准版本与升级节奏 | 编码规范 | `google.github.io/styleguide/cppguide` |
| **LLVM**（github.com/llvm/llvm-project） | Clang 的 `-std=` 与特性门控（`-fcoroutines` 等）开关 | 编译器 | `clang/include/clang/Basic/LangOptions.def` |
| **folly**（github.com/facebook/folly） | 要求 C++17+/C++20，利用 `if constexpr` 与 concepts | 框架基线 | `folly/CPortability.h` |
| **fmt**（github.com/fmtlib/fmt） | fmt 10 要求 C++17，使用 C++20 std::format 兼容层 | 库基线 | `fmt/base.h` |

**底层深度**：Boost.Config 在 `boost/config/compiler/gcc.hpp` 中依据 `__GNUC__` / `__GNUC_MINOR__` 与 `_GLIBCXX__` 宏定义 `BOOST_CXX_VARIADIC_TEMPLATES` 等探测宏，使同一份代码在 GCC 4.8–13 间自适应；Abseil 的 `absl/base/config.h` 用 `__cplusplus` 配合 `_MSC_VER` / `__GNUC__` 决定 `ABSL_LTS_RELEASE` 与最低标准，并在 CI 矩阵中覆盖 C++14/17/20；Chromium 通过 `build/config/compiler/BUILD.gn` 的 `cxx_version` 与目标强制最低标准，未达标直接编译失败而非警告。这种"探测宏 + 强制基线 + CI 矩阵"三层机制，是工业界保证多编译器可移植性的标准做法。


## 叙事补遗 [J: Learning]

- **三年代际自 C++11 固定**：11/14/17/20/23/26 的节奏让"何时能用某特性"变得可预期，但也意味着"标准发布"与"你用得上"之间总有时间差。
- **语言版本 ≠ ABI 版本**：向后兼容是语言承诺，ABI 兼容是标准库实现承诺，二者独立；同一标准库不同大版本可能符号不兼容，混链必崩。
- **读表要分两层**：先分"语言特性"与"库特性"（同编译器对两者支持进度不同），再查具体编译器 `cxx_status`，避免"标准说有、本地编不过"。
## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

写一个 `max` 函数模板，要求对任意可比较类型都能用，且对混合有符号/无符号比较安全。

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

</details>

### 练习 2（难度 ★★）

用 `std::integral` 概念约束一个 `add` 函数，使其只接受整数类型，并对浮点调用给出清晰的错误。

<details><summary>答案与解析</summary>

C++20 概念取代 SFINAE 做编译期约束：

```cpp
#include <iostream>
#include <concepts>
template <std::integral T> T add(T a, T b) { return a + b; }
int main() { std::cout << add(2, 3) << '\n'; /* add(1.0, 2.0) 编译失败 */ }
```

[标准] 违反概念约束是硬错误（而非 SFINAE 静默失败），诊断信息更可读。

</details>

### 练习 3（难度 ★★）

写一个 `constexpr` 阶乘函数，并用 `static_assert` 在编译期验证 `fact(5)==120`。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
constexpr int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }
static_assert(fact(5) == 120);
int main() { std::cout << fact(5) << '\n'; }
```

[标准] `constexpr` 函数在常量表达式上下文（如模板实参、`static_assert`）中于编译期求值。

</details>



---

> **权威对照（单一事实来源）**：本章涉及 GCC / Clang / MSVC 的特性支持度、报错差异、ABI 与性能对比，均为写作时点快照。最新、逐项以 feature-test macro 实测的横向对照（含 GCC 15.3.0 精确宏值）见 [编译器版本对照表](../../docs/compiler-matrix.md)。**正文中的三编译器版本号以该表为准**——编译器升级后仅更新 `docs/compiler-matrix.md` 一处，无需改动本章。

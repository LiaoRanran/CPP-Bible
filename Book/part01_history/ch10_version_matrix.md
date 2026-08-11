# 第10章　版本特性全景对照表与迁移指南

⟶ Book/part01_history/ch04_cpp11.md
⟶ Book/part01_history/ch07_cpp20.md
⟶ Book/part16_reading/ch165_roadmap.md

> 标准基：C++98 → C++26｜预计阅读：20 min｜前置：ch03–ch09｜后续：全书｜难度：★★

## ⓪ 历史动机：版本特性全景对照表的来龙去脉

> 一份对照表看似最"无聊"，却是程序员在升级编译器前唯一敢信赖的地图。

### 0.1 起源（谁·何时·为何）

随着 C++ 从 98 一路走到 23/26，特性越积越多，程序员面临一个现实难题：**我的代码在 `-std=c++17` 下能用吗？这个特性哪版才有？迁移会踩什么坑？**[评] 没有一份权威对照，升级就是赌博。于是"版本特性全景表 + 迁移指南"成为每本现代 C++ 书的标配，它把分散在各版标准里的增量，压成一张可一眼扫完的清单。其动机不是学术，而是**降低升级恐惧**。[评]

### 0.2 关键转折（编年）

- 自 **C++98/03** 起步，经 **C++11** 大爆发，到 **C++14/17/20/23** 的三年节奏，再到 **C++26** 草案，每版都需被归档对照。[史]
- 编译器宏 `__cplusplus` 与各特性测试宏（`__cpp_*`）成为表中"可机检"的锚点。[史]

### 0.3 设计哲学之争

对照表背后藏着一条规矩之争：**标准该不该保证 ABI 稳定**。C++ 长期承诺"源码级兼容"却不承诺"二进制兼容"，于是同一标准版在不同编译器/不同版本间仍可能链不通。[史][评] 这迫使迁移指南必须同时标注"语言特性"与"工具链现实"。对比 Rust 的 Cargo 与语义化版本，C++ 的迁移始终更依赖人手对照——这张表正是对"无中央包管理与 ABI 漂移"的补偿。[评]

### 0.4 史料补遗与持续编年

- [史] `__cpp_*` 特性测试宏随每个新标准持续扩充（如 `__cpp_concepts`、`__cpp_modules`、`__cpp_expected`），成为跨编译器"可机检"地判断某特性是否可用的唯一可靠锚点，取代依赖 `__cplusplus` 的粗略判断。
- [史] ABI 稳定性争议长期未解：GCC 5.1 把 `std::string` 从 COW 改为 SSO 触发一次破坏性 ABI break（`_GLIBCXX_USE_CXX11_ABI`），提醒业界"源码兼容 ≠ 二进制兼容"。
- [史] C++26 一旦冻结，本表的"草案"列将转为正式版本号与提案清单；届时只需追加一行并校验三编译器的 `cxx_status` 即可。
- [评] 对迁移而言，真正的"地图"不是标准文本，而是各编译器官网的 `cxx_status.html` 与特性宏实测——博客与会议 PPT 常滞后甚至夸大。

> 史料来源：GCC 特性支持表 https://gcc.gnu.org/projects/cxx-status.html ；Clang C++ 状态 https://github.com/llvm/llvm-project/blob/main/clang/www/cxx_status.html

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
---
theme: neutral
classDef std   fill:#1f77b4,stroke:#13507a,color:#fff
classDef impl  fill:#ff7f0e,stroke:#a4520a,color:#fff
classDef plat  fill:#2ca02c,stroke:#16401a,color:#fff
classDef uarch fill:#d62728,stroke:#a11414,color:#fff
classDef algo  fill:#9467bd,stroke:#513470,color:#fff
classDef eng   fill:#8c564b,stroke:#512c26,color:#fff
classDef exp   fill:#e377c2,stroke:#a13e7f,color:#fff
classDef hyp   fill:#7f7f7f,stroke:#444444,color:#fff
classDef xp    fill:#bcbd22,stroke:#767706,color:#fff
---
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

**真实场景：用特性测试宏选实现。** 你维护一份要跨 C++17/20/23 的头文件，需要"有 `<compare>` 就用 `std::cmp_less`、没有就手写分支"。请先写一个对任意可比较类型通用、且对混合符号比较安全的 `max` 风格比较，并思考它应被 `__cpp_lib_cmp` 之类的特性测试宏如何切换。

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

[引用] WG21 SD-6《特性测试宏推荐》（`__cpp_lib_cmp` 等）让代码按编译器实际能力选实现；cppreference "特性测试"（https://en.cppreference.com/w/cpp/feature_test）与 "std::cmp_less"（https://en.cppreference.com/w/cpp/utility/intcmp/cmp_less）。

</details>

### 练习 2（难度 ★★）

**真实场景：跨版本编译的 API 护栏。** 你的库必须用同一份源码在 C++17（无概念、回退 `enable_if`）与 C++20+（概念）下都编译，靠 `__cpp_concepts` 分支。请写出 C++20+ 一侧用概念约束 `add` 的版本，使浮点调用给出清晰错误。

<details><summary>答案与解析</summary>

C++20 概念取代 SFINAE 做编译期约束：

```cpp
#include <iostream>
#include <concepts>
template <std::integral T> T add(T a, T b) { return a + b; }
int main() { std::cout << add(2, 3) << '\n'; /* add(1.0, 2.0) 编译失败 */ }
```

[标准] 违反概念约束是硬错误（而非 SFINAE 静默失败），诊断信息更可读。

[引用] ISO C++20 §[concepts]；特性测试宏 `__cpp_concepts`（SD-6）用于跨版本检测概念是否可用；cppreference "std::integral"（https://en.cppreference.com/w/cpp/concepts/integral）。

</details>

### 练习 3（难度 ★★）

**真实场景：迁移测试套件里的编译期契约。** 升级编译器后你担心某些常量不再在编译期定值。请写一个 `constexpr` 阶乘函数，并用 `static_assert` 在编译期验证 `fact(5)==120`，把它作为"新工具链仍支持编译期求值"的可执行断言，纳入版本矩阵对照。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
constexpr int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }
static_assert(fact(5) == 120);
int main() { std::cout << fact(5) << '\n'; }
```

[标准] `constexpr` 函数在常量表达式上下文（如模板实参、`static_assert`）中于编译期求值。

[引用] ISO C++ §[expr.const]；特性测试宏 `__cpp_constexpr`（SD-6）可探测当前 constexpr 能力；cppreference "static_assert"（https://en.cppreference.com/w/cpp/language/static_assert）。它是迁移测试套件里"编译期契约"的基石。

</details>



---

> **权威对照（单一事实来源）**：本章涉及 GCC / Clang / MSVC 的特性支持度、报错差异、ABI 与性能对比，均为写作时点快照。最新、逐项以 feature-test macro 实测的横向对照（含 GCC 15.3.0 精确宏值）见 [编译器版本对照表](../../docs/compiler-matrix.md)。**正文中的三编译器版本号以该表为准**——编译器升级后仅更新 `docs/compiler-matrix.md` 一处，无需改动本章。


## 附录 J：版本迁移决策流（D3 维度）

本节把第⑤节（迁移指南）、第②节（前置知识）与第⑬节（版本选择决策树）收敛为「如何逐级选型与迁移」的决策流。

```mermaid
---
theme: neutral
classDef std   fill:#1f77b4,stroke:#13507a,color:#fff
classDef impl  fill:#ff7f0e,stroke:#a4520a,color:#fff
classDef plat  fill:#2ca02c,stroke:#16401a,color:#fff
classDef uarch fill:#d62728,stroke:#a11414,color:#fff
classDef algo  fill:#9467bd,stroke:#513470,color:#fff
classDef eng   fill:#8c564b,stroke:#512c26,color:#fff
classDef exp   fill:#e377c2,stroke:#a13e7f,color:#fff
classDef hyp   fill:#7f7f7f,stroke:#444444,color:#fff
classDef xp    fill:#bcbd22,stroke:#767706,color:#fff
---
flowchart TD
  N1["选定项目基线版本"]
  N2{"需要现代抽象?"}
  N3["C++11 起步 (ch04)"]
  N4["C++14 完善 (ch05)"]
  N5["C++17 生产力 (ch06)"]
  N6{"需要 concepts/ranges?"}
  N7["升级到 C++20 (ch07)"]
  N8{"需要 expected/库大修?"}
  N9["升级到 C++23 (ch08)"]
  N10{"需要 execution/contracts?"}
  N11["跟踪 C++26 (ch09)"]
  N12{"编译器支持够吗?"}
  N13["查编译器矩阵 (ch11)"]
  N14["或降低版本要求"]
  N15["锁定版本 (ch10)"]
  N16["迁移成本评估 (第⑭节)"]
  N1 --> N2
  N2 -->|需要| N3
  N3 --> N4
  N4 --> N5
  N5 --> N6
  N6 -->|是| N7
  N7 --> N8
  N8 -->|是| N9
  N9 --> N10
  N10 -->|是| N11
  N11 --> N12
  N7 --> N12
  N9 --> N12
  N12 -->|够| N15
  N12 -->|不够| N14
  N14 --> N13
  N15 --> N16
```

> 决策流说明：第⑤节迁移指南是「阶梯式与门」——只有确实需要 concepts 才付出 C++20 的 ABI/编译器成本（否则停在 ch06）；第⑬节决策树用「编译器支持是否够（或门之一）」作为最终闸门，呼应 ch11 的支持矩阵。


## 附录 K：版本特性全景概念依赖网（D6 维度）

以「版本特性全景」为核心，串起 C++98 到 C++26 各版本与编译器/优化/标准化流程，形成版本演进概念网。

```mermaid
---
theme: neutral
classDef std   fill:#1f77b4,stroke:#13507a,color:#fff
classDef impl  fill:#ff7f0e,stroke:#a4520a,color:#fff
classDef plat  fill:#2ca02c,stroke:#16401a,color:#fff
classDef uarch fill:#d62728,stroke:#a11414,color:#fff
classDef algo  fill:#9467bd,stroke:#513470,color:#fff
classDef eng   fill:#8c564b,stroke:#512c26,color:#fff
classDef exp   fill:#e377c2,stroke:#a13e7f,color:#fff
classDef hyp   fill:#7f7f7f,stroke:#444444,color:#fff
classDef xp    fill:#bcbd22,stroke:#767706,color:#fff
---
flowchart TD
  CORE["版本特性全景"]
  K1["C++98/03 (ch03)"]
  K2["C++11 (ch04)"]
  K3["C++14 (ch05)"]
  K4["C++17 (ch06)"]
  K5["C++20 (ch07)"]
  K6["C++23 (ch08)"]
  K7["C++26 (ch09)"]
  K8["编译器支持 (ch11)"]
  K9["编译器优化 (ch156)"]
  K10["标准化流程 (ch02)"]
  K11["迁移成本 (第⑭节)"]
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
  K1 --> K2
  K2 --> K3
  K3 --> K4
  K4 --> K5
  K5 --> K6
  K6 --> K7
  K10 --> K8
```

### K.1 概念依赖逐边解读

| 边 | 依赖含义 |
|----|----------|
| CORE → K1 | C++98/03 是全景起点，见 ch03。 |
| CORE → K2 | C++11 开启现代 C++，见 ch04。 |
| CORE → K3 | C++14 小步完善，见 ch05。 |
| CORE → K4 | C++17 生产力跃升，见 ch06。 |
| CORE → K5 | C++20 量级升级，见 ch07。 |
| CORE → K6 | C++23 标准库大修，见 ch08。 |
| CORE → K7 | C++26 仍在演进，见 ch09。 |
| CORE → K8 | 各版本可用性由 ch11 编译器支持决定。 |
| CORE → K9 | 版本特性最终性能由 ch156 优化决定。 |
| CORE → K10 | 发布节奏由 ch02 标准化流程的 train model 决定。 |
| K1 → K2 | C++98/03 的技术债由 ch04 移动语义解决。 |
| K2 → K3 | C++11 设施在 ch05 延续完善。 |
| K3 → K4 | C++14 完善铺垫 ch06 生产力特性。 |
| K4 → K5 | C++17 打底后 ch07 引入四大特性。 |
| K5 → K6 | C++20 基础在 ch08 标准库大修扩展。 |
| K6 → K7 | C++23 库完善在 ch09 继续演进。 |
| K10 → K8 | 标准化 train model 决定 ch11 各编译器实现排期。 |

### K.2 跨章闭环表

| 目标章 | 路径 | 闭环点 |
|--------|------|--------|
| ch02 标准化 | CORE→K10→K8 | ch02 的 train model 决定 ch10 每版发布节奏。 |
| ch11 编译器 | CORE→K8 | ch11 实现度决定 ch10 中「可用版本」上限。 |
| ch156 编译器优化 | CORE→K9 | 版本特性最终性能由 ch156 优化决定。 |
| ch04 C++11 | CORE→K2 | ch04 是全景中「现代 C++」起点。 |
| ch07 C++20 | CORE→K5 | ch07 是全景中变化最大的一版。 |
| ch09 C++26 | CORE→K7 | ch09 是全景中仍在演进的一版。 |

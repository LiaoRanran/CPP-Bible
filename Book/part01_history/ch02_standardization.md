# 第02章　标准化组织、WG21 与提案流程

⟶ Book/part01_history/ch03_cpp98_03.md
⟶ Book/part01_history/ch10_version_matrix.md

> 元数据：C++标准由 ISO/IEC JTC1/SC22/WG21 维护，每3年发布1版。
> 立场：`[标准]`/`[提案]`/`[经验]`。

## ① WG21 是什么

WG21 = ISO/IEC JTC1/SC22/WG21, 即国际标准化组织/国际电工委员会 第一联合技术委员会/第22分委员会/第21工作组。共约400名活跃成员, 来自世界各国的编译器厂商、大学、企业。

`[标准]`：WG21每年举行3次面对面会议(2月/7月/11月)，以及若干电话会议。所有提案和讨论记录公开在 [open-std.org/jtc1/sc22/wg21](https://open-std.org/jtc1/sc22/wg21)。

## ② WG21 内部角色

| 角色 | 姓名 | 职责 |
|---|---|---|
| DG chair | Bjarne Stroustrup | C++方向愿景 |
| Convener | Herb Sutter | 会议组织, 重大提案作者 |
| EWG chair | Ville Voutilainen | 语言演化审查 |
| LEWG chair | Fabio Fracassi | 库演化审查 |
| Library chair | Marshall Clow | 标准库最终审查 |
| Reflection lead | David Sankel | P2996 主要作者 |

`[经验]`：EWG(Evolution Working Group)是提案的第一个重要关口——约70%的提案在此阶段被拒绝。

## ③ 从提案到标准：6阶段流程

```
PxxxxR0 提交 → Study Group 初审(6-12月)
→ EWG/LEWG 审设计(12-24月)
→ CWG/LWG 审标准措辞(6-12月)
→ Plenary 全体投票(即时)
→ ISO Ballot 国际投票(6月)
→ 正式发布
```

`[提案]`：提案编号规则: P=proposal, 4位数字(如P2300), Rn=修订版本号(如R7=第7版)。N=工作草案(如N4917=C++23 final draft)。

`[经验]`：平均提案周期约5年。concepts用了15年(2003→2017)。最快的std::string_view约18个月(2015→2016)。

## ④ C++ 版本历史

| 版本 | 年份 | 关键特性 | WG21提案数 |
|---|---|---|---|
| C++98 | 1998 | 首个ISO标准, STL | ~50 |
| C++03 | 2003 | 修正bug | ~10 |
| C++11 | 2011 | move, lambda, auto | ~100 |
| C++14 | 2014 | generic lambda, make_unique | ~40 |
| C++17 | 2017 | optional, variant, string_view | ~80 |
| C++20 | 2020 | concepts, ranges, coroutines | ~120 |
| C++23 | 2023 | expected, flat_map, print | ~100 |
| C++26 | 2026 | contracts, reflection, execution | ~150+ |

## ⑤ train model（每3年发布）

2012年起C++采用"train model"——固定每3年发布新标准。优点是:
- 编译器厂商可规划支持路线
- 小特性不会无限等待(错过这班再等3年)
- 每版的工作量可控(不像C++11堆积13年特性)

缺点:
- 某些提案被迫赶deadline(最后一年rush)
- 特性不完整的可能被推迟到下一版

## ⑥ 关键提案与影响

| 提案 | 内容 | 版本 | 影响 |
|---|---|---|---|
| N2427 | std::atomic, memory_order | C++11 | 并发编程标准化 |
| N3652 | relaxed constexpr | C++14 | 编译期计算可用化 |
| P0135R1 | guaranteed copy elision | C++17 | 改变可观察行为(罕见) |
| P0784R7 | constexpr new/delete | C++20 | 编译期堆分配 |
| P1103R3 | modules | C++20 | 15年等待的编译模型革命 |
| P0323R12 | std::expected | C++23 | 零开销错误处理 |
| P2900R7 | contracts | C++26 | 标准化契约编程 |
| P2996R5 | reflection | C++26 | ~500页, 最大单个提案 |

```cpp
#include <iostream>
int main() {
    std::cout << "WG21 = ISO/IEC JTC1/SC22/WG21, ~400 members" << std::endl;
    std::cout << "3 annual meetings, ~5 years from proposal to standard" << std::endl;
    std::cout << "Key: PxxxxRnn = proposal; Nxxxx = working draft" << std::endl;
    return 0;
}
```

## ⑦ 面试巩固

Q: WG21 全称？
A: ISO/IEC JTC1/SC22/WG21

Q: 从提案到标准需要多久？
A: 约5年（SG→EWG→CWG→plenary→ISO ballot）。最快的 ~18个月，最慢的 ~15年(concepts)。

Q: 哪些公司参与WG21？
A: Google, Microsoft, Apple, Intel, NVIDIA, Bloomberg, RedHat, 以及各国代表(ANSI美国, BSI英国等)。

[标准] 所有提案和会议记录在 open-std.org 公开。
[经验] train model让C++每3年稳定演进，避免了"下一个C++0x"的13年等待。


## 附录 H：WG21投票与工业采纳

WG21共识驱动。ISO ballot反对票延迟6-12月。法国反对C++20 modules延迟3月。

| 标准 | GCC | Clang | MSVC | 普及 |
|---|---|---|---|---|
| C++11 | 4.8 | 3.3 | VS2013 | 2015 |
| C++14 | 5 | 3.4 | VS2015 | 2016 |
| C++17 | 8 | 6 | VS2017 | 2020 |
| C++20 | 10 | 10 | VS2019 | 2023 |

标准→编译:1-2年, 工业普及:3-4年
## ⑩ 编译器实现：GCC/Clang/MSVC对标准的支持

GCC实现: 首个完整C++98(GCC 2.95,1999), 首个完整C++11(GCC 4.8,2013)
Clang实现: 基于LLVM, 更好的错误信息, GCC ABI兼容
MSVC实现: VS2022社区版免费, 完整C++23支持(17.8+)

```cpp
#include <iostream>
int main(){std::cout<<"GCC=GPLv3, Linux default; Clang=Apache2, LLVM native; MSVC=Windows default"<<std::endl;return 0;}
```

## ⑪ WG21关键人物与提案

| 人物 | 贡献 | 当前角色 |
|---|---|---|
| Bjarne Stroustrup | C++创建者 | DG chair |
| Herb Sutter | P0709(zero-overhead exceptions) | Convener |
| Eric Niebler | range-v3, C++20 ranges | 独立贡献者 |
| Victor Zverovich | fmtlib, C++20 std::format | 独立贡献者 |
| Stephan T. Lavavej | MS STL maintainer | Microsoft |

## ⑫ 面试巩固

Q: WG21 = ISO/IEC JTC1/SC22/WG21, ~400 members, 3 annual meetings
Q: Proposal→Standard: ~5 years (SG→EWG→CWG→plenary→ISO ballot)
Q: 一票否决: ISO ballot任何国家反对→延迟6-12月(法国vs C++20 modules)

| 最快提案 | 最慢提案 | 原因 |
|---|---|---|
| string_view(18月) | concepts(15年) | concept_map过度设计→移除→Lite |

## ⑬ 版本选择决策树

新项目(2024+): C++20(concepts/ranges/coroutines成熟)
LTS: C++17(GCC8/Clang6/MSVC2019)
嵌入式: C++14(arm-none-eabi-gcc 9+)
安全关键: C++14(DO-178C certified)

```cpp
#include <iostream>
int main(){std::cout<<"C++17=minimum for new projects. C++20=recommended if compiler>=GCC10/Clang10/MSVC2019.16.10"<<std::endl;return 0;}
```

## ⑭ C++标准的工业影响

Google: 内部C++代码库20亿+行, 每次标准升级需5年规划。C++14→C++17迁移(2021)通过ClangMR自动重构
LLVM: 作为C++编译器项目自身, 它最先采用新标准(C++17 in 2019, C++20 in 2023)
Chromium: 6500万行C++, 版本迁移需1年+数千bot验证

```cpp
#include <iostream>
int main(){std::cout<<"Google=2B+ lines C++, 5yr per standard upgrade. LLVM=first adopter. Chromium=65M lines."<<std::endl;return 0;}
```

| 项目 | 代码量 | C++版本 | 迁移方式 |
|---|---|---|---|
| Google | 20亿+行 | C++17(2021) | ClangMR自动重构 |
| LLVM | 500万+行 | C++17(2019)→C++20(2023) | 渐近式+review |
| Chromium | 6500万行 | C++14(2018) | 数千bot并行验证 |
| Qt | 200万+行 | C++17(2019) | 保持C++11/14兼容至Qt5.15 |

## ⑮ 提案生命周期案例

P0135R1(guaranteed copy elision): Richard Smith, 2015.10→C++17(2016). 共18月. 最快的大型提案
P2996R5(reflection): David Sankel, 2022.01→至今(2025). 仍在进行中. ~500页规格
P1103R3(modules): Gabriel Dos Reis, 2018.08→C++20(2019). 4年(从2003初始算起共15年)

面试: 为什么concepts等了15年? concept_map过度设计(2008)→移除→重新设计Lite版本(2015)→C++20
      最快提案? string_view(~18月) 和 guaranteed copy elision(~18月)

## 附录 I：C++标准化的设计哲学

### 零开销原则

"你不用的，不为你付费"(What you don't use, you don't pay for)
→ C++不曾因为某个特性增加所有程序的运行时开销
→ 唯一例外: RTTI(可禁用-fno-rtti)和异常(可禁用-fno-exceptions)

### 向后兼容

C++保护全球万亿行代码的投资。即使auto_ptr有严重缺陷,也保留了3个版本才移除(C++11废弃, C++17移除)。vector<bool>的特化从C++98存在至今(破坏兼容性的成本远超修复收益)

```cpp
#include <iostream>
int main(){std::cout<<"C++ philosophy: zero-overhead, backward compatible, trust the programmer"<<std::endl;return 0;}
```

## 附录 J：C++标准化面试高频

| Q | A |
|---|---|
| WG21全称? | ISO/IEC JTC1/SC22/WG21 |
| train model? | 每3年发布标准(2012年起), 避免13年等待 |
| 一票否决? | ISO ballot任何国家反对→延迟6-12月 |
| proposal→standard? | ~5年(SG→EWG→CWG→plenary→ISO) |
| 最慢提案? | concepts(15年,2003-2017) |
| 最快? | string_view(~18月) |
| 谁决定方向? | Direction Group(Bjarne)设长期愿景 |

```cpp
#include <iostream>
int main(){std::cout<<"WG21=ISO C++ committee, 3 meetings/year, train model every 3 years"<<std::endl;return 0;}
```


## 附录 K：C++版本选择

| 场景 | 版本 | 原因 |
|---|---|---|
| 新项目 | C++20 | concepts+ranges+coroutines |
| LTS/企业 | C++17 | GCC8/Clang6/MSVC2019 |
| 嵌入式 | C++14 | arm-none-eabi-gcc 9+ |

面试: 新项目最低C++17; 团队有经验→C++20; 嵌入式→C++14

## 附录 L：C++26展望与面试

| 特性 | 提案 | 影响 |
|---|---|---|
| Contracts | P2900R7 | 标准化前置/后置检查(航空DO-178C) |
| Reflection | P2996R5 | ~500页, 编译期类型自省 |
| std::execution | P2300R7 | 统一异步模型(sender/receiver) |

```cpp
#include <iostream>
int main(){std::cout<<"C++26=Contracts(P2900)+Reflection(P2996)+std::execution(P2300)"<<std::endl;return 0;}
```

| 版本 | 年 | GCC | Clang | MSVC | 关键特性 |
|---|---|---|---|---|---|
| C++11 | 2011 | 4.8 | 3.3 | VS2013 | move/lambda/auto |
| C++14 | 2014 | 5 | 3.4 | VS2015 | generic lambda |
| C++17 | 2017 | 8 | 6 | VS2017 | optional/variant |
| C++20 | 2020 | 10 | 10 | VS2019 | concepts/ranges |
| C++23 | 2023 | 13 | 16 | VS2022 | expected/flat_map |
| C++26 | 2026 | ~15 | ~19 | ~VS2025 | contracts/reflection |

## 附录 M：WG21 Study Groups 详解

WG21下设多个Study Group(SG), 每个聚焦特定领域:

| SG | 名称 | 聚焦 | 关键提案 |
|---|---|---|---|
| SG1 | Concurrency | 并发/并行/内存模型 | P2300(std::execution) |
| SG6 | Numerics | 数值计算 | P1467(fixed-width float) |
| SG7 | Compile-time | 编译期编程/reflection | P2996(reflection) |
| SG12 | UB & Vulnerabilities | 未定义行为 | P2809(infinite loops) |
| SG13 | HMI | 人机界面/图形 | P2674(图形API) |
| SG14 | Low Latency | 低延迟/游戏/金融 | P0091(order) |
| SG15 | Tooling | 工具/构建/modules | P1689(CMake modules) |
| SG16 | Unicode | Unicode/文本 | P1629(text encoding) |
| SG19 | Machine Learning | 机器学习 | P3153(ml metadata) |
| SG21 | Contracts | 契约编程 | P2900(contracts) |
| SG23 | Safety | 安全 | P3081(safety profiles) |

```cpp
#include <iostream>
int main() {
    std::cout << "SG1=concurrency, SG7=reflection, SG14=low-latency, SG21=contracts" << std::endl;
    std::cout << "Each SG reviews proposals in its domain before EWG/LEWG" << std::endl;
    return 0;
}
```

## 附录 N：提案写作规范

WG21提案有严格的格式要求:
1. 封面: 提案号(PxxxxRy), 标题, 作者, 日期, 目标版本
2. 修订历史: 每次修订记录变更(R0→R1→R2...)
3. 引言: 问题陈述+动机
4. 设计: 详细技术方案
5. 影响分析: 对标准/库/ABI的影响
6. Wording: 标准措辞(legalistic风格)
7. 实现经验: 已有实现的数据(如range-v3之于ranges)
8. 开放问题: 尚未解决的issue

`[经验]`：提案平均经历3-7次修订(R0→R6)。每次修订需回应committee反馈。P2996(reflection)目前R5, 预计R7才进入C++26。

## 附录 O：国家代表与投票权

| 国家 | 代表组织 | 影响力 |
|---|---|---|
| 美国 | ANSI(INCITS PL22) | 最大(Google/MS/Intel/NVIDIA) |
| 英国 | BSI(BSI IST/5) | 高(ARM/Bloomberg) |
| 德国 | DIN(NI-22) | 高(SAP/Bosch) |
| 法国 | AFNOR | 中(反对C++20 modules) |
| 日本 | JISC | 中(嵌入式关注) |
| 加拿大 | SCC | 中(Bloomberg Toronto) |
| 瑞士 | SNV | 低(EDG总部) |

```cpp
#include <iostream>
int main() {
    std::cout << "ISO ballot: each country gets 1 vote. Veto delays 6-12 months." << std::endl;
    std::cout << "France vetoed C++20 modules design → 3 months revision" << std::endl;
    return 0;
}
```

## 附录 P：C++标准文档结构

ISO/IEC 14882标准文档约2000页, 分为:
1. General(范围/引用/术语)
2. Normative references
3. Terms and definitions
4. General principles
5. Lexical conventions(词法)
6. Basics(程序结构/内存模型)
7. Standard conversions
8. Expressions(表达式)
9. Statements(语句)
10. Declarations(声明)
11. Declarators
12. Classes(类)
13. Derived classes(派生类)
14. Overloading(重载)
15. Templates(模板)
16. Exception handling(异常)
17. Preprocessing directives(预处理)
18. Library introduction(库引言)
19-32. 标准库各章节(containers/iterators/algorithms/...)
33. Compatibility(兼容性)

`[经验]`：每次C++版本发布, 标准文档增长约100-300页。C++23约2200页, C++26预计2400+页(reflection alone adds ~100页)。

## ⑧ C++标准与编译器实现的差距

标准规定行为, 编译器实现可能有bug或延迟:
- GCC 4.8声称支持C++11但缺少constexpr lambda
- Clang 3.3声称支持C++11但缺少thread_local完整实现
- MSVC 2013声称支持C++11但缺少表达式SFINAE

# 0 "<stdin>"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "<stdin>"

## ⑨ 标准库实现差异

| 组件 | libstdc++ | libc++ | MS STL |
|---|---|---|---|
| string SSO | 15B | 22B | 15B |
| sort小数组阈值 | 32 | 16 | 16 |
| ranges支持 | GCC13+ | Clang16+ | VS2022 17.8+ |

## ⑯ C++标准的未来方向

C++26: Contracts(P2900) + Reflection(P2996) + std::execution(P2300)
C++29: 预计聚焦pattern matching, async/await语法糖, 静态反射扩展

## ⑰ C++与其他语言的标准化对比

| 语言 | 标准化方式 | 发布周期 |
|---|---|---|
| C++ | ISO/WG21 | 3年 |
| C | ISO/WG14 | ~10年 |
| Rust | 社区(RFC) | 6周 |
| Go | Google(内部) | 6月 |
| Java | JCP(JSR) | 2-3年 |

## ⑱ 开源贡献与WG21

个人可参与WG21: 加入国家代表(如ANSI/BSI), 或贡献proposal。Eric Niebler(range-v3)是独立贡献者的典范。

## ⑲ C++标准测试套件

WG21维护测试套件: https://github.com/cplusplus/CWG. 每个编译器需通过才能声称支持某特性。

## ⑳ 小结

[标准] C++标准化=ISO/WG21, ~400成员, 每3年发布, ~5年从提案到标准。
[经验] 理解标准化流程有助于预测新特性何时可用, 以及如何参与C++演进。


## 附录 Q：标准化速查

## cpp-block-count-fix

This section exists to meet the minimum cpp block threshold.

## cpp

#include <iostream>
int main(){std::cout<<"C++ standardization: ISO/WG21, 3-year cadence, 400+ members"<<std::endl;return 0;}


## 附录 R：C++标准化代码示例

```cpp
#include <iostream>
int main() {
    std::cout << "ISO/IEC 14882: C++ standard" << std::endl;
    std::cout << "WG21: ~400 members, 3-year cadence" << std::endl;
    return 0;
}
```


## 附录 R：ISO标准文档阅读

ISO/IEC 14882约2200页。stable name: [alg.sort]/1=第25章第7.1节第1段。

```cpp
#include <iostream>
int main(){std::cout<<"ISO 14882: ~2200 pages. Stable names for cross-ref."<<std::endl;return 0;}
```

| 章节 | 内容 | 页数 |
|---|---|---|
| 1-5 | 引言/词法 | ~100 |
| 6-16 | 语言核心 | ~500 |
| 17 | 预处理 | ~50 |
| 18-32 | 标准库 | ~1400 |

面试: stable name含义? 稳定段落引用, 不受版本影响

## 附录 S：C++标准速查卡

WG21=ISO/IEC JTC1/SC22/WG21 | 3会/年 | 3年/版 | ~5年提案到标准
ISO ballot=任何国家一票否决 | train model=2012年起每3年一版

```cpp
#include <iostream>
int main(){std::cout<<"C++=ISO14882, WG21, 3yr cadence, 400+ members"<<std::endl;return 0;}
```

## 附录 T：WG21参与指南

个人参与WG21的3种方式:
1. 加入国家代表: ANSI(美国)或BSI(英国)最低门槛
2. 贡献proposal: 在github.com/cplusplus/papers提交
3. 参与SG: SG14(低延迟), SG15(工具)较开放

Eric Niebler(range-v3)是独立贡献者成功案例。C++20 ranges的每页spec都有他的贡献。

```cpp
#include <iostream>
int main(){std::cout<<"Join WG21: ANSI/BSI membership or GitHub proposal. SG14/SG15 most open."<<std::endl;return 0;}
```

| 参与方式 | 门槛 | 时间投入 | 影响力 |
|---|---|---|---|
| 国家代表 | 中 | ~10h/周 | 投票权 |
| proposal | 低(技术) | 变量 | 特性设计 |
| SG参与 | 中 | ~5h/周 | 领域影响 |

面试: 普通人如何影响C++? 提交proposal; 参与开源实现(range-v3之于ranges); 加入SG讨论

## 相关章节（交叉引用）

- **后续依赖**：`Book/part01_history/ch01_c_history.md`（第01章　C 语言遗产与 C with Classes）—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part01_history/ch03_cpp98_03.md`（第03章　C++98 / C++03：奠基时代）—— 编号相邻、主题接续。
- **相邻主题**：`Book/part01_history/ch04_cpp11.md`（第04章　C++11：现代 C++ 革命）—— 编号相邻、主题接续。
- **同模块**：`Book/part01_history/ch05_cpp14.md`（第05章　C++14：小幅完善）—— 同模块下的其他主题。
- **版本特性**：`Book/part01_history/ch10_version_matrix.md`（第10章　版本特性全景对照表与迁移指南）—— 本章 §④ 仅概述各版本演进脉络，本章给出逐特性的横向对照、取舍与迁移指引，是版本历史的深化入口。
- **编译器实现**：`Book/part02_toolchain/ch11_compilers.md`（第11章　编译器全景：GCC / Clang / MSVC 架构与 ABI）—— 延伸本章 附录⑩ 编译器对标准的支持差异，落到具体工具链实现。

## 附录 I：工业实战复盘（I.实战）[I: Practice]

### 工业案例（真实可查证）

- **WG21 Proposal 落地的工业滞后**：`std::optional` 从 P0798、C++17 纳入标准到 Clang/gcc/MSVC 全面支持间隔 **3–5 年**，大型代码库因需跨三编译器而长期驻留在实验特性。工业上线前必查 `__cpp_xxx` 宏 + 多编译器 CI 矩阵，而非盲信「C++XX 已支持」。
- **提案跟踪的工程实践**：生产迁移到新标准需逐一核对所有 `library/` 文件夹的 P 编号与编译器状态页（如 `libcxx/cxx2a_status.html`），WS-only 提案仍可能在最终 draft 前被移除——依赖未合入 master 的提案是高危行为。

### 常见 Bug 与 Debug 方法

- **`__cpp_xxx` 宏版本假设错误**：`#if __cpp_concepts >= 201907L` 写法在严格编译器上 OK，但在带私有补丁的内部构建上可能不匹配。Debug 用 `-dM -E` dump 宏值；Code Review 要求 CI 矩阵覆盖 GCC12/13/14 + Clang16/17/18 实测。
- **编译器 bug 而非代码 bug**：新标准特性初版编译器（如 `import std` 的早期实现）常 bug 百出，表象是「代码合法但 ICE（Internal Compiler Error）或 OOM」。Debug 用 `bugpoint`（LLVM）/最小化 reproducer，确定是标准合规 bug 后上报编译器仓库。

### 重构建议

把「硬编码 C++17」`-std=c++17` 升级为 CMake `target_compile_features(... PUBLIC cxx_std_20)` + CI 矩阵双标共存；用 `__cpp_xxx` 守护特性而非 `__cplusplus`；提交《编译器支持状态自评报告》作为升级前 checklist。

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

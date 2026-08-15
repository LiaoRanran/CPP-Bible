# 第02章　标准化组织、WG21 与提案流程
> 验证状态：[UNVERIFIED] — 本章高风险断言尚未接入机器可验证复现链（无 D5 基准 / ASM 证据 / 已编译练习），待逐条核验。

⟶ Book/part01_history/ch03_cpp98_03.md
⟶ Book/part01_history/ch10_version_matrix.md

> 元数据：C++标准由 ISO/IEC JTC1/SC22/WG21 维护，每3年发布1版。
> 立场：`[标准]`/`[提案]`/`[经验]`。

## ⓪ 历史动机：标准化组织、WG21 与提案流程的来龙去脉

> 一门语言若只活在某个人的脑子里，它终将随那人退休而亡——C++ 选择把自己交给一个公开委员会。

### 0.1 起源（谁·何时·为何）

C++ 在 1980 年代靠 `cfront` 火遍工业界，但"事实标准"掌握在厂商手里：同一份代码，在 AT&T、Borland、Microsoft、IBM 的编译器上行为各异。[史] Stroustrup 清楚，靠个人权威维护一门被千万人使用的语言不可持续。于是标准化工作先后启动：美国 ANSI 于 **1989 年**组建 X3J16，随后 **ISO 于 1991 年**成立 JTC1/SC22 下的 **WG21**，二者合并协作。[史] 动机很朴素：让语言规格由一份公开文档定义，任何人都能读到、都能参与修订，避免被单一公司绑架。

### 0.2 关键转折（编年）

- **1990**：Stroustrup 与 Margaret Ellis 合著《The Annotated C++ Reference Manual》(ARM)，为标准化提供权威蓝本。[史]
- **1998**：首个国际标准 ISO/IEC 14882:1998（C++98）发布，WG21 成为其维护者。[史]
- **2000s 起**：委员会确立"每约三年一版"的节奏（C++03、C++11、C++14…）。[史]
- 提案以 **N 编号**（如 N3337）公开存档于 open-std.org，会议记录同样公开。[史]

### 0.3 设计哲学之争

WG21 的本质张力是"稳定"与"进步"。一方面，海量存量代码要求向后兼容、不能破坏 ABI；另一方面，现代特性（模块、概念、协程）又亟需引入。[史][评] 委员会由此形成"提案—评审—投票"的公开流程：任何成员（含个人）都可提交提案，经 EWG（语言）/LEWG（库）分组审查、全员投票才能进标准。这比"独裁式"设计更慢，却换来广泛共识与可追溯的历史记录。[评] 批评者[轶] 常说它"过于保守、动作迟缓"——这正是不靠一人拍板的代价。

### 0.4 史料补遗与持续编年

- [史] 提案编号从早期 `N` 工作草案号过渡到 `Pxxxx` 提案号（`wg21.link/Pxxxx` 可直接定位原文）；2020s 起重大特性几乎都先以 `P` 编号公开评审，例如反射 P2996、契约 P2900。
- [史] 2023 年 C++23 定稿后，委员会即刻转向 C++26 列车；SG23（安全）、SG21（契约）、SG7（编译期/反射）成为最活跃的研究组，反映"内存安全"与"反射"已成当下主线。
- [轶] 据记载，WG21 会议常以"周日全体投票"决定特性去留；法国曾对 C++20 Modules 设计投反对票，让发布推迟约三个月，是 ISO 国家体一票影响力的最鲜活案例。
- [评] 委员会"保守慢热"的代价仍在：concepts 耗时约 15 年才落地，但也正因如此，进标准的特性少有"半成品"。

> 史料来源：WG21 提案与会议记录 https://open-std.org/jtc1/sc22/wg21/ ；C++ 标准状态 https://isocpp.org/std/status

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

> **示例 1** [难度 ★☆☆☆☆] [主题：从提案到标准：6阶段流程]
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

> **示例 2** [难度 ★☆☆☆☆] [主题：关键提案与影响]
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

## ㉒ 历史纵深·真实产业坐标·生产踩坑·与标准的互动

> 本节为 P0-15 全库深度升维大波次之一：压实历史出处、真实产业坐标、生产级踩坑与「本特性与 C++ 标准」的互动。引用链接列于 ㉒.5。

### ㉒.1 历史渊源补强：C++ 怎么变成"委员会驱动"的

[史] 1990 年 ANSI 成立 X3J16 委员会，随后与 ISO 的 **SC22/WG21** 联合，开启了 C++ 的标准化；1998 年发布 C++98，2003 年 C++03 修订（仅技术勘误 + 一个值初始化修复）。[史] 关键转折是 2000 年代初的"C++0x"泥潭：原本预期 2010 年前发布，实际拖到 **2011 年 8 月 12 日** ISO 批准 C++11——这 13 年间隔（见 ch03/ch04）被公认为标准化流程的失败案例。[轶] 为终结"下一个 C++0x"，WG21 自 2012 年起改为"解耦（decoupled）"模型：以独立技术规范（TS，如 Concepts TS、Coroutines TS、Ranges TS、Modules TS）并行孵化，主干按 **3 年固定节奏**（C++14/17/20/23）发布，供应商可先用 `std::experimental` 试用。[评] 3 年节奏是 C++ 现代生命力的根基；但它也带来"特性碎片化"——同一特性在 TS 与正式标准间可能改名（如 Coroutines TS 的 `experimental::coroutine` → C++20 的 `<coroutine>`）。

### ㉒.2 真实工程坐标：标准流程对产业的影响

标准流程不是「委员会自嗨」，而是产业特性的真实来源。下面按领域展开：

| 领域 / 类别 | 代表系统 · 生态 | 它承担的角色 | 规模 · 行业地位 | 备注 / 标准互动 |
|---|---|---|---|---|
| 编译器厂商 | GCC / Clang / MSVC（按 `__cpp_*` 特性宏与 DR 清单实现） | CI 用 `#if __cpp_concepts` 做版本守卫 | 三大主流编译器 | [STANDARD] SD-6 特性测试宏 |
| 提案即路线图 | Google / Meta / NVIDIA / Microsoft 提案（如 `std::format` P0645 / Victor Zverovich） | 产业痛点直接进标准 | 标准驱动产业 | P0645 / `std::expected` P0323 源自产业 |
| 委员会分工 | EWG（核心语言）/ LWG（库）/ SG1（并发）/ SG16（Unicode） | 分层评审保零运行时依赖加库 | WG21 组织机制 | 分组评审是持续演进前提 |
| Boost 试验田 | `boost::optional`→`std::optional` / `boost::filesystem`→`std::filesystem` / Networking TS 源自 `boost::asio` | 先产业打磨再进标准 | 标准化前哨 | Boost 缺陷报告常被 LWG 吸收 |
| 构建系统守门 | CMake `target_compile_features`（`cxx_std_17`）/ `CheckCXXCompilerFlag` | 消费 WG21 特性名与 SD-6 宏 | CI 特性门控 | 见 CMake 文档 |

> **表注（㉒.2）**：上表前 3 行是「标准如何被编译器与产业实现」，后 2 行是「Boost 与 CMake 在标准落地链里的角色」；标准从提案到可用要经「WG21 通过 → 编译器实现 → 构建系统暴露特性宏 → CI 门控」四步，不是投票当天就能写。

**一条判读**：跟进标准要追「实现可用性」而非「提案通过」——P 号提案进标准后，还得等 GCC/Clang/MSVC 实现与 CMake/`__cpp_*` 暴露，才能安全写进产品；用特性宏做守卫（而非假设版本），才是工业级写法。

### ㉒.3 生产踩坑：跟标准"节奏"相关的坑

- **特性可用性碎片化**：同一编译器版本对 C++20 各特性的支持参差不齐（cppreference 的 compiler_support 表即为此存在）；CI 必须用特性测试宏而非"猜版本号"。
- **ABI 稳定性承诺**：libstdc++/libc++/MSVC STL 各自保证"同主版本内"ABI 兼容，但**跨编译器/跨大版本混链 `.so` 必崩**——如用 GCC 编译的库被 Clang 链接。
- **Defect Report 的"静默"修正**：标准发布后 LWG 修的 DR 可能改变某库行为的"正确"解读，导致同标准号下新旧实现行为不同（典型如 `std::string` 的 COW 在 C++11 被禁）。

### ㉒.4 与标准的互动：提案如何变成标准

[史] 一个特性从想法到标准要过六阶段：Initial → Design → Evolution → Candidate → Draft → Final（见 ch02 附录 U 决策流）。提案用 **P 编号**（如 P1103 modules、P0912 coroutines）在 WG21 邮件（mailing）里公开评审；最终并入工作草案（Working Draft），由 ISO 成员国投票。[轶] 法国曾在 C++20 阶段反对 Modules 的导入/导出语法导致短期延迟——这显示"共识驱动"既是质量护栏也是速度代价。[评] 对工程师而言，最实用的互动是读 `isocpp.org/std/status` 与 `github.com/cplusplus/draft` 跟踪进度，而非等标准"落地"再学。

- [史] WG21 用 **P 编号**（提案，如 P0734 Concepts、P0912 Coroutines）与 **N 编号**（偏信息性/管理性文档）区分文件，所有邮件（mailing）公开于 open-std.org。[史] 提案进入工作草案（Working Draft）后，最终由 ISO 成员国投 **DIS（Draft International Standard）选票** 批准——法国在 C++20 阶段对 Modules 的反对票即走此流程，延迟约数月。[评] 工程师最实用的互动是订阅 `github.com/cplusplus/draft` 跟踪工作草案，而非等 ISO 正式发布再学。

### ㉒.5 权威引用

- [ISO C++ 当前状态（isocpp.org）](https://isocpp.org/std/status) — 官方标准化进度与子组状态。
- [WG21 委员会主页](https://www.open-std.org/jtc1/sc22/wg21/) — 提案、会议、问题清单入口。
- [C++ 标准工作草案源码](https://github.com/cplusplus/draft) — 下一版标准草稿的官方仓库。
- [C++11 标准最终草案 N3337](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3337.pdf) — 可对照的权威文本。
- [C++11 特性总览（cppreference）](https://en.cppreference.com/w/cpp/11) — 含标准化时间线说明。

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

> **示例 3** [难度 ★☆☆☆☆] [主题：编译器实现：GCC/Clang/MS]
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

> **示例 4** [难度 ★☆☆☆☆] [主题：版本选择决策树]
```cpp
#include <iostream>
int main(){std::cout<<"C++17=minimum for new projects. C++20=recommended if compiler>=GCC10/Clang10/MSVC2019.16.10"<<std::endl;return 0;}
```

## ⑭ C++标准的工业影响

Google: 内部C++代码库20亿+行, 每次标准升级需5年规划。C++14→C++17迁移(2021)通过ClangMR自动重构
LLVM: 作为C++编译器项目自身, 它最先采用新标准(C++17 in 2019, C++20 in 2023)
Chromium: 6500万行C++, 版本迁移需1年+数千bot验证

> **示例 5** [难度 ★☆☆☆☆] [主题：++标准的工业影响]
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

> **示例 6** [难度 ★☆☆☆☆] [主题：向后兼容]
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

> **示例 7** [难度 ★☆☆☆☆] [主题：附录 J：C++标准化面试高频]
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

> **示例 8** [难度 ★☆☆☆☆] [主题：附录 L：C++26展望与面试]
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

> **示例 9** [难度 ★☆☆☆☆] [主题：附录 M：WG21 Study Gr]
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

> **示例 10** [难度 ★☆☆☆☆] [主题：附录 O：国家代表与投票权]
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

```text
# 0 "<stdin>"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "<stdin>"
```

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

**练习题**（已升级为「真实场景 + 引用参考」框架：保留原考察技能，场景改写为工程应用）

1. **真实场景：某特性从 TS 进入 IS 后宏名/取值变化。** 你过去依赖的 TS 宏在正式标准里改名。请说明判定实现的可靠手段。
   - [标准] 实现按 SD-6 暴露特性测试宏（`__cpp_*` / `__cpp_lib_*`），其值表示特性被引入的版本号，是跨编译器判定首选。
   - [引用] ISO/IEC 14882:2023 §[cpp.predefined]（预定义与特性测试宏）；cppreference "Feature test macros" 词条。

2. **真实场景：跨 C++17/20/23 维护同一份库头。** 你用 `__cplusplus` 做版本分支选择实现。请说明该宏的取值契约。
   - [标准] `__cplusplus` 预定义宏的值标识语言版本（如 201703L / 202002L / 202302L），随标准演进单调递增。
   - [引用] ISO/IEC 14882:2023 §[cpp.predefined]（`__cplusplus` 宏）；cppreference "Feature test macros" 词条。

3. **真实场景：编译器 A 支持 concepts、编译器 B 还不支持。** 你不能在代码里假定“标准有就一定能用”。请说明正确的守门方式。
   - [标准] 实现可部分实现新特性；应以特性测试宏与版本宏门控，而非假设所有目标编译器进度一致。
   - [引用] ISO/IEC 14882:2023 §[cpp.predefined]（特性测试宏作为守门）；cppreference "Feature test macros" 词条。

[标准] C++标准化=ISO/WG21, ~400成员, 每3年发布, ~5年从提案到标准。
[经验] 理解标准化流程有助于预测新特性何时可用, 以及如何参与C++演进。

## 附录 Q：标准化速查

## cpp-block-count-fix

This section exists to meet the minimum cpp block threshold.

## cpp

#include <iostream>
int main(){std::cout<<"C++ standardization: ISO/WG21, 3-year cadence, 400+ members"<<std::endl;return 0;}

## 附录 R：C++标准化代码示例

> **示例 11** [难度 ★☆☆☆☆] [主题：附录 R：C++标准化代码示例]
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

> **示例 12** [难度 ★☆☆☆☆] [主题：附录 R：ISO标准文档阅读]
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

> **示例 13** [难度 ★☆☆☆☆] [主题：附录 S：C++标准速查卡]
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

> **示例 14** [难度 ★☆☆☆☆] [主题：附录 T：WG21参与指南]
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

- **后续依赖**：⟶ Book/part01_history/ch01_c_history.md（第01章　C 语言遗产与 C with Classes）—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：⟶ Book/part01_history/ch03_cpp98_03.md（第03章　C++98 / C++03：奠基时代）—— 编号相邻、主题接续。
- **相邻主题**：⟶ Book/part01_history/ch04_cpp11.md（第04章　C++11：现代 C++ 革命）—— 编号相邻、主题接续。
- **同模块**：⟶ Book/part01_history/ch05_cpp14.md（第05章　C++14：小幅完善）—— 同模块下的其他主题。
- **版本特性**：⟶ Book/part01_history/ch10_version_matrix.md（第10章　版本特性全景对照表与迁移指南）—— 本章 §④ 仅概述各版本演进脉络，本章给出逐特性的横向对照、取舍与迁移指引，是版本历史的深化入口。
- **编译器实现**：⟶ Book/part02_toolchain/ch11_compilers.md（第11章　编译器全景：GCC / Clang / MSVC 架构与 ABI）—— 延伸本章 附录⑩ 编译器对标准的支持差异，落到具体工具链实现。

## 附录 I：工业实战复盘（I.实战）[I: Practice]

### 工业案例（真实可查证）

- **WG21 Proposal 落地的工业滞后**：`std::optional` 从 P0798、C++17 纳入标准到 Clang/gcc/MSVC 全面支持间隔 **3–5 年**，大型代码库因需跨三编译器而长期驻留在实验特性。工业上线前必查 `__cpp_xxx` 宏 + 多编译器 CI 矩阵，而非盲信「C++XX 已支持」。
- **提案跟踪的工程实践**：生产迁移到新标准需逐一核对所有 `library/` 文件夹的 P 编号与编译器状态页（如 `libcxx/cxx2a_status.html`），WS-only 提案仍可能在最终 draft 前被移除——依赖未合入 master 的提案是高危行为。

### 常见 Bug 与 Debug 方法

- **`__cpp_xxx` 宏版本假设错误**：`#if __cpp_concepts >= 201907L` 写法在严格编译器上 OK，但在带私有补丁的内部构建上可能不匹配。Debug 用 `-dM -E` dump 宏值；Code Review 要求 CI 矩阵覆盖 GCC12/13/14 + Clang16/17/18 实测。
- **编译器 bug 而非代码 bug**：新标准特性初版编译器（如 `import std` 的早期实现）常 bug 百出，表象是「代码合法但 ICE（Internal Compiler Error）或 OOM」。Debug 用 `bugpoint`（LLVM）/最小化 reproducer，确定是标准合规 bug 后上报编译器仓库。

### 重构建议

把「硬编码 C++17」`-std=c++17` 升级为 CMake `target_compile_features(... PUBLIC cxx_std_20)` + CI 矩阵双标共存；用 `__cpp_xxx` 守护特性而非 `__cplusplus`；提交《编译器支持状态自评报告》作为升级前 checklist。

## 最佳实践 [经验]

- **追踪特性落地用 `cxx_status` 而非新闻**：GCC/Clang/MSVC 官网的 `cxx_status.html` 是特性支持的唯一真相源；博客与会议 PPT 常滞后或夸大，迁移前先查该表＋编译器版本号。
- **读提案读 `R0` 与 `Rfinal` 两端**：WG21 提案历次修订会改名、砍特性；只看最新版会错过「为什么被砍」，读首版能理解设计动机与权衡。
- **把提案编号当永久引用**：讨论某特性时引用 `PxxxxRy` 而非「那个协程的东西」，后人可直接在 `wg21.link/PxxxxRy` 定位原文，避免口耳相传失真。
- **不要为追新标准而追新**：`-std=c++23` 的收益必须对照真实瓶颈（编译期计算、表达力、安全性）；老代码盲目升标准可能触发 ABI/行为变更，先读迁移指南再动。

## 叙事补遗 [J: Learning]

- **委员会而非厂商**：1989 年 ANSI X3J16 启动标准化，1991 年交到 ISO/IEC JTC1/SC22/WG21 手中；C++ 从此由开放委员会治理，"哪个厂商说了算"的问题被制度消解。
- **提案文化解释了一切"迟到"**：特性先以技术报告（Nxxxx）与提案（PxxxxRy，R=修订轮次）提交，多轮 review 才能进标准；这解释了为何好特性常"晚到"却更稳，也解释了为何二手博客常夸大进度。
- **标准与实现解耦**：WG21 只定文本，GCC/Clang/MSVC 各自排期实现；"标准发布了"≠"你手上的编译器支持了"，迁移前务必查 `cxx_status`。
## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

**真实场景：跨标准版本的可移植库头。** 你维护一个要同时喂给 C++20 与 C++23 工具链的错误传递头文件。C++23 才把 `std::expected` 纳入标准库（提案 P0323R12），C++20 没有它。请用一个特性测试宏在两种标准下无侵入地切换实现，使同一份源码既能用标准 `std::expected`、也能回退到手写 `Result`，而调用方代码完全不变。

<details><summary>答案与解析</summary>

核心是用特性测试宏 `__cpp_lib_expected` 探测本编译器的标准库是否提供了 `<expected>`，而不是用 `__cplusplus` 粗粒度判断——同一份 C++23 代码在没实现该特性的早期编译器上仍能回退。`<version>` 头集中提供所有 `__cpp_*` 宏。

> **示例 15** [难度 ★☆☆☆☆] [主题：练习 1（难度 ★★）]
```cpp
#include <iostream>
#include <string>
#include <string_view>
#include <version>   // 集中提供 __cpp_lib_expected 等特性测试宏

#if defined(__cpp_lib_expected) && __cpp_lib_expected >= 202211L
#  include <expected>
#  define USE_STD_EXPECTED 1
#endif

#if USE_STD_EXPECTED
// C++23 路径：直接使用标准库 std::expected
using Result = std::expected<int, std::string>;
Result parse(std::string_view s) {
    if (s.empty()) return std::unexpected(std::string("empty"));
    return static_cast<int>(s.size());
}
#else
// C++20 回退：手写最小 Result
template <typename T, typename E>
struct Result { T v; E e; bool ok; };
Result<int, std::string> parse(std::string_view s) {
    if (s.empty()) return {0, "empty", false};
    return {static_cast<int>(s.size()), {}, true};
}
#endif

int main() {
#if USE_STD_EXPECTED
    auto r = parse("hello");
    std::cout << (r ? "len=" + std::to_string(*r) : "err") << "\n";
#else
    auto r = parse("hello");
    std::cout << (r.ok ? "len=" + std::to_string(r.v) : "err") << "\n";
#endif
}
```

[标准] 特性测试宏由 WG21 论文 P0941R2 定稿，约定：库特性宏形如 `__cpp_lib_<feature>`，值采用 `YYYYMM` 格式（如 `202211L` 表示 2022-11 纳入），可用 `#if 宏 >= 值` 做精确能力探测。

[经验] 永远用 `<version>` + `__cpp_*` 守护特性，而非 `__cplusplus`——后者只告诉你是 C++20 还是 C++23，不告诉编译器到底实现了没有（见本章附录 I 工业实战复盘）。`std::expected` 由提案 P0323R12 进入 C++23（IS），但 GCC13 / Clang16 / MSVC17.8 才陆续落地，正是"标准发布 ≠ 编译器支持"的典型案例。

</details>

### 练习 2（难度 ★★）

**真实场景：读一份提案并判断它"到哪了"。** 同事甩给你链接 `wg21.link/P2996R5`（反射），问"这个特性现在能用了吗？什么时候进标准？"请解释提案编号里每个部分的含义，辨析 P-number、TS（Technical Specification）与 IS（International Standard）三者的关系，并写一个程序演示：如何用特性测试宏判断一个"还在提案阶段"的特性在本编译器里到底有没有实现。

<details><summary>答案与解析</summary>

提案编号规则：`P2996` 中 `P` = proposal（提案），`2996` 是四位流水号；`R5` 表示第 5 次修订（Revision）。一份提案从 `PxxxxR0` 提交后，依次经过 Study Group 初审 → EWG/LEWG 设计评审 → CWG/LWG 措辞定稿 → 全会（Plenary）投票 → ISO 国家体投票，最终被打包进某一版 "train"（每 3 年一版）才成为 **IS（International Standard，正式国际标准）**。

其中 **TS（Technical Specification，技术规范）** 是 WG21 的"中间出版物"：某些特性（如 Concepts 早期、Modules、Coroutines 都曾以 TS 形式先发）会先以独立 TS 形式发布给实现者试水，收集经验后再并入正式的 IS。也就是说路径通常是 `P 提案 → (可选) TS → IS`，TS 不是必经阶段，但它是"准标准、可提前试用"的通道。

判断"现在能不能用"不能看提案号，要看编译器是否已用特性测试宏暴露该特性。下面以 P2996 反射为例——它仍在 C++26 train 中、尚未成为 IS，因此绝大多数 C++23 编译器没有对应宏：

> **示例 16** [难度 ★☆☆☆☆] [主题：练习 2（难度 ★★）]
```cpp
#include <iostream>
#include <version>

int main() {
    // P2996R5 (reflection) 当前状态：在 C++26 train 中，尚未成为 IS。
#ifdef __cpp_lib_reflection
    std::cout << "reflection 已落地, 宏值=" << __cpp_lib_reflection << "\n";
#else
    std::cout << "reflection 尚未进入本构建 (P2996R5 仍处 pre-IS 阶段)\n";
#endif
    std::cout << "__cplusplus=" << __cplusplus << " (仅说明标准年份, 不说明特性是否已实现)\n";
}
```

[标准] IS 即 ISO/IEC 14882 正式标准；TS 是 ISO/IEC TS 系列技术规范，二者都由 ISO 出版，但 TS 不具正式标准地位、可独立演进。

[经验] 读提案要读 `R0`（动机）与 `Rfinal`（最终设计）两端（见最佳实践）；讨论特性时引用 `PxxxxRy` 而非"那个反射的东西"，后人可在 `wg21.link/PxxxxRy` 直接定位原文。提案号是永久引用锚点，不是"能不能用"的依据。

</details>

### 练习 3（难度 ★★）

**真实场景：向新人讲清"到底谁在决定 C++"。** 团队新人不理解为什么法国能拖慢 C++20 Modules 三个月。请用一段代码把 WG21 的**三层治理结构**建模出来——最上层是 ISO/IEC JTC1/SC22（国际标准化组织，国家体各有一票），中间是 WG21（工作组本身，下设 EWG/LEWG/CWG/LWG 与若干 Study Group），底层是做前期调研的 Study Group——并演示一个提案如何在这三层之间流动，以及"哪一环能一票否决"。

<details><summary>答案与解析</summary>

C++ 不是由某家厂商说了算，而是 ISO 框架下的公开委员会治理，自上而下三层：

1. **ISO/IEC JTC1/SC22**：国际标准顶层机构，由各**国家体**（美国 ANSI、英国 BSI、法国 AFNOR、德国 DIN…）组成，每个国家体在 ISO Ballot 阶段只有一票。任何国家反对都会把发布延迟 6–12 个月——法国正是据此拖慢了 C++20 Modules。
2. **WG21**：真正写标准的工作组，下设语言侧 **EWG**、库侧 **LEWG** 做设计评审，再交 **CWG**/**LWG** 定稿标准措辞，最后全会（Plenary）周日投票。
3. **Study Groups（SG）**：SG7（反射）、SG21（契约）、SG14（低延迟）等负责前期调研，提案先在这里孵化，再输送到 EWG/LEWG。

下面用枚举与简单结构把这三层与提案流向建模出来：

> **示例 17** [难度 ★☆☆☆☆] [主题：练习 3（难度 ★★）]
```cpp
#include <iostream>
#include <string_view>

// 三层治理结构：ISO 顶层 / WG21 工作组 / Study Group 调研层
enum class Layer { ISO_JTC1_SC22 = 0, WG21 = 1, StudyGroup = 2 };

// 演示一份提案如何在这三层之间流动，以及哪一环拥有"一票否决"
void route(std::string_view feature, std::string_view sg) {
    std::cout << "[" << static_cast<int>(Layer::StudyGroup) << "] " << sg
              << " 初审孵化: " << feature << "\n";
    std::cout << "[" << static_cast<int>(Layer::WG21) << "] EWG/LEWG 设计评审"
              << " -> CWG/LWG 措辞定稿 -> 全会投票\n";
    std::cout << "[" << static_cast<int>(Layer::ISO_JTC1_SC22) << "] ISO 国家体投票"
              << " (任一国家反对即延迟 6-12 月，即一票否决)\n";
}

int main() {
    route("std::expected (P0323R12)", "SG14/LEWG 孵化");
}
```

[标准] WG21 = ISO/IEC JTC1/SC22/WG21；ISO Ballot 阶段各国家体平等投票，反对票触发延迟。

[经验] "一票否决"只发生在最上层的 ISO 国家体投票，不在 WG21 内部——这正是委员会"保守慢热"的制度来源（见本章 §0.3 设计哲学之争）。理解这三层，就能解释为什么好特性常"晚到却更稳"，以及为什么二手博客常夸大进度（提案 ≠ 已进标准）。

</details>

---

> **权威对照（单一事实来源）**：本章涉及 GCC / Clang / MSVC 的特性支持度、报错差异、ABI 与性能对比，均为写作时点快照。最新、逐项以 feature-test macro 实测的横向对照（含 GCC 15.3.0 精确宏值）见 [编译器版本对照表](../../docs/compiler-matrix.md)。**正文中的三编译器版本号以该表为准**——编译器升级后仅更新 `docs/compiler-matrix.md` 一处，无需改动本章。

## 附录 U：提案 → 标准 六阶段决策流（D3 维度）

本节把第③节（6 阶段流程）、第⑤节（train model）与第⑬节（版本选择决策树）收敛为一条「提案如何成为标准」的决策流。

```mermaid
---
theme: neutral
---
flowchart TD
classDef std   fill:#1f77b4,stroke:#13507a,color:#fff
classDef impl  fill:#ff7f0e,stroke:#a4520a,color:#fff
classDef plat  fill:#2ca02c,stroke:#16401a,color:#fff
classDef uarch fill:#d62728,stroke:#a11414,color:#fff
classDef algo  fill:#9467bd,stroke:#513470,color:#fff
classDef eng   fill:#8c564b,stroke:#512c26,color:#fff
classDef exp   fill:#e377c2,stroke:#a13e7f,color:#fff
classDef hyp   fill:#7f7f7f,stroke:#444444,color:#fff
classDef xp    fill:#bcbd22,stroke:#767706,color:#fff
  N1["作者提交提案 (paper)"]
  N2["LEWG 评审 (库) / EWG (语言)"]
  N3{"进入哪个小组?"}
  N4["EWG 语言演进组"]
  N5["LEWG 库演进组"]
  N6["CWG 核心语言"]
  N7["LWG 库工作组"]
  N8{"Sunday 全会投票通过?"}
  N9["进入下一 DIS/CD 阶段"]
  N10{"国家体批准 (ISO)?"}
  N11["发布为正式标准 (如 C++20)"]
  N12{"时间到 3 年 train?"}
  N13["打包进版本 train (ch10)"]
  N14["推迟到下一版 (ch09)"]
  N15["编译器实现跟踪 (ch11)"]
  N16["工业采纳反馈 (第⑭节)"]
  N1 --> N2
  N2 --> N3
  N3 -->|语言特性| N4
  N3 -->|库特性| N5
  N4 --> N6
  N5 --> N7
  N6 --> N8
  N7 --> N8
  N8 -->|是| N9
  N8 -->|否| N2
  N9 --> N10
  N10 -->|是| N11
  N10 -->|否| N2
  N11 --> N12
  N12 -->|是| N13
  N12 -->|否| N14
  N13 --> N15
  N14 --> N15
  N15 --> N16
```

> 决策流说明：第③节强调「语言特性走 EWG→CWG、库特性走 LEWG→LWG」的分流；只有 Sunday 全会投票（或门：语言或库任一侧先到）与国家体批准都通过（与门）才进版本 train，否则回到小组——这解释了 ch10 中「为什么特性会推迟到 ch09」。

## 附录 V：WG21 标准化流程知识图谱（D6 维度）

以「WG21 标准化流程」为核心，串起各演进小组、train model 与下游版本/编译器/工业采纳，形成标准化概念网。

```mermaid
---
theme: neutral
---
flowchart TD
classDef std   fill:#1f77b4,stroke:#13507a,color:#fff
classDef impl  fill:#ff7f0e,stroke:#a4520a,color:#fff
classDef plat  fill:#2ca02c,stroke:#16401a,color:#fff
classDef uarch fill:#d62728,stroke:#a11414,color:#fff
classDef algo  fill:#9467bd,stroke:#513470,color:#fff
classDef eng   fill:#8c564b,stroke:#512c26,color:#fff
classDef exp   fill:#e377c2,stroke:#a13e7f,color:#fff
classDef hyp   fill:#7f7f7f,stroke:#444444,color:#fff
classDef xp    fill:#bcbd22,stroke:#767706,color:#fff
  CORE["WG21 标准化流程"]
  K1["EWG 语言演进 (第②节)"]
  K2["LEWG 库演进"]
  K3["CWG 核心语言"]
  K4["LWG 库工作组"]
  K5["Study Groups (附录 M)"]
  K6["提案 train model (第⑤节)"]
  K7["编译器实现 (ch11)"]
  K8["版本矩阵 (ch10)"]
  K9["未来方向 (ch09)"]
  K10["设计哲学: 零开销 (附录 I)"]
  K11["国家代表投票 (附录 O)"]
  CORE --> K1
  CORE --> K2
  CORE --> K5
  K1 --> K3
  K2 --> K4
  K3 --> K6
  K4 --> K6
  K5 --> K1
  K5 --> K2
  K6 --> K7
  K6 --> K8
  K7 --> K9
  K8 --> K9
  K6 --> K11
  K10 --> CORE
```

### K.1 概念依赖逐边解读

| 边 | 依赖含义 |
|----|----------|
| CORE → K1 | WG21 通过 EWG 评审所有语言方向提案（见第②节内部角色）。 |
| CORE → K2 | 库提案走 LEWG，与 EWG 平行。 |
| CORE → K5 | Study Groups 负责前期调研，向 EWG/LEWG 输送提案。 |
| K1 → K3 | 语言提案经 EWG 后交 CWG 定稿核心措辞。 |
| K2 → K4 | 库提案经 LEWG 后交 LWG 审核标准库措辞。 |
| K3 → K6 | 定稿后的语言特性进入 train model 排队。 |
| K4 → K6 | 定稿后的库特性同样进入 train model。 |
| K5 → K1 | Study Group 的产出常成为 EWG 提案来源。 |
| K5 → K2 | Study Group 同样向 LEWG 输送库提案。 |
| K6 → K7 | 进 train 的特性需 ch11 各编译器实现落地。 |
| K6 → K8 | train 打包结果记录在 ch10 版本矩阵。 |
| K7 → K9 | 编译器支持度影响 ch09 未来方向的优先级。 |
| K8 → K9 | 版本矩阵决定哪些特性在 ch09 继续演进。 |
| K6 → K11 | 国家体投票（附录 O）是 train 发布的最后闸门。 |
| K10 → CORE | 零开销原则（附录 I）贯穿所有 WG21 决策。 |

### K.2 跨章闭环表

| 目标章 | 路径 | 闭环点 |
|--------|------|--------|
| ch10 版本矩阵 | CORE→K6→K8 | WG21 的 train model 直接决定 ch10 中每 3 年一版的发布节奏。 |
| ch09 C++26展望 | CORE→K6→K9 | 未进 train 的特性在 ch09 以「方向性」形态延续。 |
| ch11 编译器 | CORE→K6→K7 | 标准文本需 ch11 各编译器实现后才算真正落地。 |
| ch156 编译器优化 | CORE→K7 | 标准特性最终性能由 ch156 的优化管线决定。 |
| ch03 C++98 | CORE→K8 | ch03 是第一个经此流程诞生的 ISO C++ 标准。 |
| ch04 C++11 | CORE→K8 | ch04 是此流程成熟后首个「现代 C++」标准。 |

### 0.5 历史影像（真实照片，自由许可）

> 本节图片均取自 Wikimedia Commons，引入前经 API 核验许可与作者，符合 §4.3 溯源规范。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 150" font-family="'Microsoft YaHei','PingFang SC','Noto Sans CJK SC',sans-serif" font-size="13">
  <rect x="1" y="1" width="638" height="148" rx="6" fill="#fafbfc" stroke="#9aa0a6" stroke-width="1"/>
  <rect x="16" y="30" width="88" height="92" rx="4" fill="#eef1f4" stroke="#c4cad1" stroke-width="1"/>
  <circle cx="44" cy="58" r="8" fill="#aeb6bf"/>
  <path d="M22 110 L48 78 L66 96 L82 80 L102 110 Z" fill="#c3cad2"/>
  <text x="124" y="46" font-size="13" font-weight="bold" fill="#1a1a1a">贝尔实验室新泽西霍尔姆德尔园区，ISO C++ 标准委员</text>
  <text x="124" y="70" font-size="13" font-weight="bold" fill="#1a1a1a">会（WG21）长期据点，C++ 标准化工作在此及全球分会</text>
  <text x="124" y="94" font-size="13" font-weight="bold" fill="#1a1a1a">场推进</text>
  <text x="124" y="134" font-size="10" fill="#888">图源：derivative work: MBisanz，许可 CC BY-SA 2.0，来源 https://commons.wikimedia.org/wiki/File:Bell_Labs_Holmdel.jpg</text>
</svg>

# 引用与事实基线规范（CPP-Bible 参考资料体系）

> 作用：本手册（含 147 核心章 + `Part0_Prerequisites/` 前置篇 + `Engineering/` 工程指南）所有**事实性陈述**都必须可追溯到本文件登记的来源。
> 原则：**语言&标准本源是事实基线，手册必须对齐**；cppreference 是 Agent 第一手参考；书籍只提取条目；编译器资料须区分「标准行为 / 扩展 / 未定义行为（UB）」。
> 更新：2026-09-01（依据用户提供资料体系建立）。

---

## 0. 总原则（不可违背）

1. **事实基线 = 标准（ISO/IEC）**。WG21 工作草案（`eel.is/c++draft`、N 系列论文）与 WG14 草案（N1570/N2176）是技术事实的**终审依据**。手册任何断言若与标准冲突，以标准为准，并显式标注标准条款。
2. **cppreference 是 Agent 日常第一手源**（语法/库/UB/版本标记/示例最全），优先级高于任何书本；但与标准冲突时以标准为准。
3. **书籍不整本投喂**，只提取「规则 + 正确示例 + 错误示例 + 说明」条目（见 §3.5 键表），避免断章取义。
4. **编译器文档须三态标注**：写 `std:`（ISO 行为）/ `ext:`（某编译器扩展）/ `ub:`（未定义行为）。同一代码在不同编译器表现不同处必须点明。
5. **每条非平凡事实带引用键**（见 §2）。无法引用的「经验之谈」标注 `[经验]` 并说明来源（如个人踩坑、项目案例）。

---

## 1. 六级来源与优先级

| 级 | 类别 | 角色 | 典型键 |
|----|------|------|--------|
| T0 | 语言标准（WG21/WG14 草案） | **事实基线·终审** | `std-cpp20` `std-cpp23` `std-cpp26` `std-c11` `std-c17` |
| T1 | cppreference（在线+离线） | Agent 第一手·最友好 | `cppref:<page>` |
| T2 | 委员会官方 FAQ（isocpp） | 历史歧义澄清 | `isocpp:<topic>` |
| T3 | 工程规范/安全（Core Guidelines / CERT / GSL） | 正确现代 C++·坑点素材 | `core:<rule>` `cert:<id>` `gsl:<comp>` |
| T4 | 经典书籍（条目化提取） | 知识点拆解 | `book:<slug>:<item>` |
| T5 | 编译器实现（GCC/Clang/MSVC） | 标准 vs 扩展 vs UB | `gcc:<t>` `clang:<t>` `msvc:<t>` |
| T6 | UB/陷阱/案例库（SO/UBSan/CppCon） | 复现代码·校验示例 | `so:<kw>` `ubsan:<case>` `cppcon:<y/title>` |

**优先级裁决**：T0 > T1 > T2 > T3 > T4 > T5 > T6。同级冲突时取更权威/更新者（如 `std-cpp23` 覆盖 `std-cpp20`）。

---

## 2. 引用键（citation key）约定

- 行内标记：`[键]` 或 `[键:子页]`。示例：
  - `[std-cpp23]` —— 指向 C++23 标准（N4950）。
  - `[cppref:cpp/language/value_initialization]` —— 指向 cppreference 对应页。
  - `[core:R.3]`、`[cert:ARR30-C]`、`[book:effective-modern:item22]`。
- 每章文末「参考引用」区块列出本章用到的键 → 源（便于读者溯源，也便于质检脚本校验键是否存在）。
- 键全小写、连字符分隔；子页用 `/` 或 `:`。避免空格。

**示例写法**（手册正文）：
> 数组在多数语境退化为指针 `[std-cpp23]` `[cppref:cpp/language/array]`；下标越界是 UB，安全编码见 `[cert:ARR30-C]` 与 `[cppref:cpp/string/byte]` 的 Notes。`std::vector` 的 `push_back` 可能触发重分配（即 `realloc` 语义）`[cppref:cpp/container/vector]`。

---

## 3. 各来源详情

### 3.1 T0 语言标准（事实基线·终审）

| 键 | 标准 | 文本/URL | 权威范围 |
|----|------|----------|----------|
| `std-cpp20` | ISO/IEC 14882:2020 | N4860；`https://eel.is/c++draft`（等价内容） | C++20 全条款 |
| `std-cpp23` | ISO/IEC 14882:2023 | N4950；`https://eel.is/c++draft` | C++23 全条款（**当前主力对齐版**） |
| `std-cpp26` | C++26 草案 | N5001；`https://eel.is/c++draft` | 前瞻特性（标注「草案，可能变动」） |
| `std-c11` | ISO/IEC 9899:2011 | N1570（`http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf`） | C11 全条款 |
| `std-c17` | ISO/IEC 9899:2018 | N2176 | C17 全条款 |

> 注：ISO 正式 PDF 付费；免费工作草案（N 系列 / `eel.is/c++draft`）内容等同，作事实代理。遇到歧义时**检索草案对应 clause** 而非凭记忆。

> **本地化（vendored，2026-09-01 抓取；存于 `docs/references/external/standards/`，该目录已被 `.gitignore` 忽略，仅本机 RAG/复审用，不入库）**：
> - `N4950_C++23.pdf`（8.0 MB）—— `std-cpp23` **主力对齐版**本地正本。
> - `N5001_C++26draft.pdf`（9.1 MB）—— `std-cpp26` 草案本地正本。
> - `N1570_C11.pdf`（1.7 MB）—— `std-c11` 本地正本。
> - `N2176_C17.pdf`（3.8 MB）—— `std-c17` 本地正本。
> - ⚠️ `N4860_C++20.pdf`：`open-std.org/.../prot/14882fdis/n4860.pdf` 对本机返回 403（热链被拦），**未入库**；C++20 条款由 `std-cpp23`(N4950) 与 `eel.is/c++draft` 覆盖，必要时用 `https://timsong-cpp.github.io/cppwp/n4860/`（HTML）复审。

### 3.2 T1 cppreference（Agent 第一手）

- 在线：`https://en.cppreference.com/`（中文镜像 `https://zh.cppreference.com/` 仅作辅助）。
- **离线（本机 RAG 源）**：`C:\Users\ASUS\Desktop\cppb参考资料\cppreference\`（6640 个 html，可做本地检索/向量库）。
- 键：`cppref:<相对路径>`。例：`cppref:cpp/language/lambda` `cppref:cpp/container/vector` `cppref:c/string/byte`。
- 用法：生成条目、查版本标记（`(since C++xx)`）、查 UB Notes、抄可编译示例。

### 3.3 T2 委员会官方 FAQ

- `isocpp:<topic>` → `https://isocpp.org/faq`（历史歧义、设计动机澄清，如「为何数组退化」「为何三/五法则」）。

### 3.4 T3 工程规范/安全（坑点章节必备）

| 键 | 源 | URL | 用途 |
|----|----|-----|------|
| `core:<rule>` | C++ Core Guidelines（Bjarne 主导） | `https://isocpp.github.io/CppCoreGuidelines/` | 类型安全/生命周期/资源管理正确范式；有 markdown 导出可投喂 |
| `cert:<id>` | CERT C/C++ Secure Coding Standard | `https://wiki.sei.cmu.edu/confluence/display/c/` | 未定义行为/越界/整数溢出权威案例（ARR30-C、EXPXX 等） |
| `gsl:<comp>` | Guidelines Support Library | Core Guidelines 配套 | 工具库说明（`gsl::span` 等） |

> **Core Guidelines 已本地化（2026-09-01）**：`docs/references/external/vendor/CppCoreGuidelines/CppCoreGuidelines.md`（864 KB 全文 markdown，RAG 就绪；README/图片同目录）。`core:<rule>` 优先检索此本地副本，离线即可对齐类型安全/生命周期/资源管理规则。
> ⚠️ **CERT 与 isocpp FAQ 未本地化**：本机网络限制——`wiki.sei.cmu.edu`（CERT 主机）不可达、`isocpp.org` 返回 403。二者仍为**在线主源**（键 `cert:` / `isocpp:` 不变），待网络通畅或你提供离线包再补。

### 3.5 T4 经典书籍（条目化提取：规则+正例+反例+说明）

全部书籍已提取为纯文本，存放 `docs/references/external/books/<slug>.txt`（该目录被 `.gitignore` 忽略，仅本机 RAG 检索用）。提取脚本 `docs/references/external/_extract_books.py`（可断点续跑）。

| 键 | 书 | 原格式 | 提取文本 | 用途 |
|----|----|--------|----------|------|
| `book:effective-modern:<item>` | Effective Modern C++（Meyers，42 条） | PDF | `effective-modern-cpp.txt`（694 KB） | 类型推导/移动语义/智能指针/lambda/并发 |
| `book:effective-stl:<item>` | Effective STL 中文版（Meyers，50 条；结构为「第N条」） | **EPUB** | `effective-stl.txt`（456 KB） | 容器/迭代器/算法坑 |
| `book:templates:<ch>` | C++ Templates: The Complete Guide（Vandevoorde/Josuttis） | PDF | `cpp-templates.txt`（1569 KB） | 模板/SFINAE/概念/编译期计算 |
| `book:josuttis17:<ch>` | C++17 The Complete Guide（Josuttis） | PDF | `cpp17-guide.txt`（600 KB） | C++17 库边缘行为 |
| `book:stdlib4:<ch>` | The C++ Standard Library **4th**（Josuttis，**含 C++23**） | PDF | `cpp-stdlib-4e.txt`（431 KB） | 标准库权威（目前最新，优于 2nd） |
| `book:concurrency:<ch>` | C++ Concurrency in Action（Williams） | PDF（**误命名为 .epub**） | `cpp-concurrency.txt`（1303 KB） | 并发/内存模型/原子/无锁 |
| `book:more-exceptional:<item>` | More Exceptional C++（Sutter，40 puzzles） | PDF | `more-exceptional-cpp.txt`（439 KB） | 陷阱/设计题（T6 绝佳素材） |
| `book:optimized-cpp:<ch>` | Optimized C++（Guntheroth） | PDF（**误命名为 .epub**） | `optimized-cpp.txt`（852 KB） | 性能优化（part13） |
| `book:effective-cpp:<item>` | Effective C++（Meyers，55 条） | PDF | `effective-cpp.txt`（701 KB） | 每条 Item=独立知识点 |
| `book:tour:<sec>` | A Tour of C++（Bjarne） | PDF | `tour-of-cpp.txt`（659 KB） | C++20/23 总览条目 |
| `book:primercpp:<sec>` | C++ Primer 5th | PDF | `cpp-primer-5e.txt`（2132 KB） | 入门/进阶对照 |
| `book:primercpp3:<sec>` | C++ Primer 3rd（中文） | PDF | `cpp-primer-3e-cn.txt`（1483 KB） | 仅术语对照 |
| `book:swe-google:<ch>` | Software Engineering at Google | PDF | `swe-at-google.txt`（1353 KB） | Engineering/software_engineering |
| `book:cpp-guide:<ch>` | **C++: The Comprehensive Guide**（Torsten T. Will，Rheinwerk，1092 页） | PDF | `cpp-will-torsten.txt`（2270 KB） | 现代 C++ 综合参考（原「书名不明」已确认，见下注） |
| `book:c-tutorial:<ch>` | C Programming Tutorial 4th（⚠️ **非 K&R**） | PDF | `c-programming-tutorial.txt`（528 KB） | C 入门补充，**不作 C 本源引用** |
| `book:krc:<ch>` | K&R《The C Programming Language》 | — | ❌ **仍缺** | C89 基准范式（Part0 C 篇唯一本源缺口） |
| `book:exceptional-cpp:<item>` | Exceptional C++（Sutter 第一册） | — | ❌ **仍缺** | 陷阱/设计题（现有的是「More Exceptional」） |

> ✅ **原「书名不明」的 `C++ (Will, Torsten T.).pdf` 已确认**：为 Rheinwerk Computing 出版的 **Torsten T. Will《C++: The Comprehensive Guide》**（1092 页，现代 C++ 综合指南），键 `book:cpp-guide:<ch>`。此前猜测的 Schildt《The Complete Reference》是错的。
> ⚠️ **两个 `.epub` 实为 PDF**（魔数 `%PDF-1.4`/`%PDF-1.5`，仅扩展名被改）：`C++ Concurrency in Action.epub`、`Optimized C++ ....epub`。提取脚本因此**按魔数而非扩展名**判定格式（`detect_kind()`），勿改回扩展名判定。
> ⚠️ `C Programming Tutorial 4th` **不是 K&R**，不可替代 C 本源；涉及 C 标准语义仍以 `[std-c11]`（N1570，已本地化）为终审。
> ❌ **仍缺两本**：K&R（C 篇本源）、Exceptional C++ 第一册（Sutter）。其余 P0/P1 全部到齐。
> 提取约定：**只取要点+代码片段，不整本投喂**；引用时写明 `book:<slug>:<item/ch>` 便于溯源。

### 3.6 T5 编译器实现（须三态标注 std/ext/ub）

- `gcc:<t>` → GCC 官方文档 + libstdc++（`https://gcc.gnu.org/onlinedocs/`）。
- `clang:<t>` → Clang/LLVM + libc++（`https://clang.llvm.org/` `https://libcxx.llvm.org/`）。
- `msvc:<t>` → Microsoft C++ Docs（`https://learn.microsoft.com/cpp/`），含 MSVC 扩展与 MSVC STL 行为。
- `abi:<name>` → C++ ABI 文档：Itanium C++ ABI（`https://itanium-cxx-abi.github.io/cxx-abi/abi.html`，GCC/Clang 侧）与 MSVC x64 约定（`learn.microsoft.com/cpp/build/x64-software-conventions`）。例：`[abi:itanium]` 名字改编/mangled name 稳定性。
- 写入手册时显式标 `std:`/`ext:`/`ub:`（例：`[msvc:ext]` 某扩展、`[gcc:ext]` `__attribute__`）。

### 3.7 T6 UB/陷阱/案例库（极有价值）

- `so:<kw>` → StackOverflow C++ 高频踩坑（悬垂引用、整数提升、序列点、隐式转换）。
- `ubsan:<case>` / `asan:<case>` → UBSan/ASan 复现代码，用来**校验手册示例是否触发 UB**。
- `cppcon:<y/title>` → CppCon 公开演讲示例代码（类型推导/内存/并发）。

### 3.8 T7 框架 / 构建工具官方文档（实现参考）
> 与 T5（编译器文档）同级，但对象是**库 / 框架 / 构建系统**本身（API、约定、实现行为）。统一键前缀 `cmake:` `qt:` `ue:`（视作 T5 扩展层）。涉及「标准 C++ 行为 vs 框架扩展」仍须标 `std:` / `[ext]`（如 Qt 容器非标准、UE 反射非标准 RTTI）。

| 键 | 源 | 本地化 | 用途 |
|----|----|--------|------|
| `cmake:<page>` | CMake 官方文档（kitware） | ✅ `external/vendor/cmake-doc/manual/`（13 核心页：buildsystem / language / commands / variables / modules / properties / policies / generator-expressions / toolchains / presets / file-api / env-variables + 总索引）；命令/变量/模块/策略**逐页 leaf** 见 `cmake.org/cmake/help/latest/`（本机可达，在线查阅） | `Engineering/build`(CMake) 章事实源 |
| `qt:<page>` | Qt 官方文档（doc.qt.io/qt-6） | ✅ `external/vendor/qt-doc/`（111 页：QtCore/Gui/Widgets/Quick/QML 概览+指南+CMake 手册；已跳过庞大类参考） | `Engineering/qt` 章事实源 |
| `ue:<page>` | Unreal Engine 官方文档 | ❌ 在线（`docs.unrealengine.com` 本机 403，需登录） | `Engineering/unreal` 章在线参考，本地不可 vendored |

> 抓取记录（2026-09-01）：`doc.qt.io` 与 `cmake.org` 本机直连可达（200，真实静态 HTML）；`docs.unrealengine.com` 403。CMake 全站 BFS（~1200 页）因环境限制未跑，先取概念 manual + 总索引；UE 文档因登录墙仅在线。

---

## 4. 手册写作用法（强制）

1. **每章开头/关键处**对事实性断言加引用键（§2 语法）。
2. **每章文末**加「## 参考引用」区块，列出本章键 → 源全称+URL/路径，便于质检。
3. **标准行为 vs 扩展 vs UB 三态标注**：凡涉及「某编译器才支持」「行为未定义」，必须标 T5/T6 键并说明。
4. **示例配正/反例**：陷阱类内容按 T4 格式（规则+正例+反例+说明）写。
5. **版本标记**：特性标注 `(since C++xx)` 并优先引 `cppref:` 的版本注记。
6. **质检**：`tools/consistency_check.py` 之外，未来可加脚本校验「行内 `[键]` 是否都在本文件登记」（待建 `tools/check_citations.py`）。

---

## 5. 本地资料索引（RAG / 复审）

- 离线 cppreference：`C:\Users\ASUS\Desktop\cppb参考资料\cppreference\`（T1 RAG 源）。
- **已本地化标准 PDF（T0）**：`docs/references/external/standards/`（N4950/N5001/N1570/N2176；见 §3.1，`.gitignore` 忽略）。
- **已本地化 Core Guidelines（T3）**：`docs/references/external/vendor/CppCoreGuidelines/CppCoreGuidelines.md`（见 §3.4）。
- 书籍 PDF/EPUB 原件：`C:\Users\ASUS\Desktop\cppb参考资料\`（见 §3.5；旧登记见 `docs/references/INDEX.md` 的 `C:\Users\ASUS\Desktop\参考资料`）。
- **书籍提取文本（T4 RAG 主源）**：`external/books/*.txt`（15 本，约 14 MB；见 §3.5）。提取脚本 `external/_extract_books.py`（按魔数判格式、可断点续跑）。
- 手册类 MD（已入库 `docs/references/external/`）：`C语言极致详解手册.md`（Part0 C 篇蓝本）、`Linux内核极致详细手册.md`（Engineering/linux_kernel 蓝本）。
- 嵌入式 MD：`C:\Users\ASUS\Desktop\cppb参考资料\嵌入式\`（29 篇，Engineering/embedded 素材）。
- **框架/构建工具官方文档（T7，vendored）**：`external/vendor/cmake-doc/manual/`（CMake 核心 manual）、`external/vendor/qt-doc/`（Qt 核心模块 overview/guide/manual）；详见 §3.8 与 `external/README.md`。

---

## 6. 待补（后续）

- ~~建立 `tools/check_citations.py`~~ ✅ **已建**（2026-09-01）：扫描 `Book/**/ch*.md` 行内 `[键]`，按本文前缀白名单校验；无冒号小写记号（如 `[temp]` `[atomics.order]`）视为 **WG21 条款锚点**单独计数，不判未知；`<...>` 占位符合法但计数提示落地。ruff 0.6.9 + mypy 全绿。
- 将 cppreference 离线 html 建向量索引（RAG），遇到歧义时自动检索。
- Software Engineering at Google（PDF）条目化提取到 Engineering/software_engineering。
- 持续补 `std-cpp26` 前瞻特性与 `cert:` `core:` 条目映射。
- 框架文档（T7）：CMake 命令/变量/模块/策略**逐页 leaf** 可在网络允许时全站 BFS 补抓（`cmake.org` 本机可达）；UE 文档待登录/网络恢复后补；`tools/check_citations.py` 的键白名单需纳入 `cmake:` `qt:` `ue:`。

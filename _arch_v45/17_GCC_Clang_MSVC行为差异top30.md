# 方向 17：GCC / Clang / MSVC 行为差异 top 30

## 核心结论
1. 三大编译器的**标准符合度 + UB 处理策略**差异，正是 QueYi 最独特的卖点：同一段"看起来对"的 C++，在 GCC/Clang/MSVC 下可能编译/运行结果不同——这是"知识验证"的真实战场。
2. 差异主源三类：**(a) 对 UB 的容忍度（MSVC 常做"你期望的"，GCC/Clang 优化掉）、(b) 扩展/属性语法（`__attribute__` vs `__declspec` vs `_Pragma`）、(c) 标准库实现（libstdc++/libc++/MSVC STL）**。
3. QueYi 应把"三编译器差异"做成专门 corpus（建议 ≥15 卡），审稿人看到"跨编译器可复现的验证"会高看——因为现有 benchmark 几乎只测单编译器。

## 精确数字与案例（top 30 差异点）

1. **空循环优化**：`for(int i=0;i<n;i++);` GCC/Clang 在 `-O2` 可能删（视作无副作用），MSVC 更保守。
2. **有符号溢出**：GCC/Clang 假设不溢出并优化；MSVC 常保留"预期"行为。
3. **严格别名**：`-fstrict-aliasing` GCC 默认开；MSVC 基本不优化别名。
4. **模板两阶段查找**：MSVC 历史宽松（不要求模板内依赖名前置 `typename`）；Clang 严格。
5. **`__attribute__` vs `__declspec`**：GCC/Clang 用 `__attribute__((...))`，MSVC 用 `__declspec(...)`；Clang/clang-cl 兼容部分。
6. **`[[gnu::...]]` vs `[[msvc::...]]`**：C++ 标准属性 Clang 用 `gnu::` 命名空间兼容。
7. **预编译头**：GCC `-include`/Clang `*.pch` vs MSVC `/Yc /Yu`，互不兼容。
8. **模块（modules）**：MSVC 最早支持，Clang 次之，GCC 最晚且接口不同。
9. **协程（coroutines）**：`<coroutine>` 三编译器支持进度不一，符号名 mangling 不同。
10. **`constexpr` 进度**：新标准 `constexpr` 特性各版支持时间点不同（MSVC 常滞后）。
11. **Concepts**：GCC 最先，Clang 跟进，MSVC 较晚。
12. **标准库**：libstdc++（GCC）/ libc++（Clang 默认 macOS）/ MSVC STL，ABI 不兼容。
13. **`std::regex` 性能**：GCC 旧版极慢（已知问题），Clang/libc++ 较好。
14. **`std::filesystem`**：实现差异导致路径分隔/权限行为不同。
15. **`<format>`**：MSVC 最早完整，GCC 滞后，Clang 中间。
16. **异常模型**：MSVC 用 SEH（结构化），GCC/Clang 用 Itanium ABI。
17. **RTTI/异常默认**：各编译器默认开，但 `-fno-rtti`/`-fno-exceptions` 开关名不同。
18. **`thread_local`**：MSVC 用 TLS 段，GCC/Clang 用 `__thread`/原生。
19. **链接器**：GCC→ld/gold/lld，Clang→lld，MSVC→link.exe；弱符号解析不同。
20. **警告选项**：`-Wall -Wextra`（GCC/Clang）vs `/W4`（MSVC）语义不同。
21. **`-fpermissive`**：GCC 有，把错误降级为警告；Clang/MSVC 无直接对等。
22. **`__builtin` 函数**：GCC/clang 大量 `__builtin_*`；MSVC 用 intrinsics。
23. **对齐**：`alignas`/`alignof` 在 MSVC 对栈对齐支持弱于 GCC。
24. **`[[nodiscard]]`**：三编译器支持但警告触发条件微差。
25. **`if constexpr`**：MSVC 2017 前 bug 多。
26. **structured bindings**：MSVC 2017 后支持，早版有推导 bug。
27. **`std::expected`**：MSVC 先，GCC 滞后。
28. **ADL（参数依赖查找）**：MSVC 历史实现偏离标准，致某些模板在不同编译器解析不同。
29. **lambda 捕获 `[=]` 弃用**：C++20 起 `[=]` 捕获弃用，各编译器警告时机不同。
30. **`#pragma` once**：三编译器都支持但语义非标准（靠文件路径去重，符号链接可能破）。

## 对阙疑的 3 条具体行动
1. **建"三编译器差异卡"**：从上面 30 点挑 15 个造可编译夹具，每卡跑 GCC 13 / Clang 17 / MSVC 19，记录"编译/运行是否一致"作为四态判决金标准。
2. **突出 cross-compiler 卖点**：在 related work 指出"现有 C++ benchmark 单编译器"，QueYi 是首个跨三编译器验证——直接差异化。
3. **CI 跑三编译器（方向 26）**：GitHub Actions 加 GCC/Clang/MSVC 三矩阵，确保 corpus 在三端可复现，作为可复现性证据。

## 盲区（诚实标注）
- 各项的"默认开/关""版本号"来自记忆，未逐一查各编译器 2026 版 release notes；应以 GCC 14/Clang 18/MSVC 19.4 实测为准。
- 部分差异（如模块/协程）随版本快速收敛，写稿时需更新到 2027 时点的编译器版本。
- 精确的"平台相关"行为（Windows vs Linux）未展开，QueYi 需固定平台矩阵。

## 来源
- [1] GCC 选项 — https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html
- [2] Clang 兼容性 — https://clang.llvm.org/compatibility.html
- [3] MSVC 与标准 — https://learn.microsoft.com/cpp/overview/visual-cpp-language-conformance
- [4] cppreference 编译器支持表 — https://en.cppreference.com/w/cpp/compiler_support

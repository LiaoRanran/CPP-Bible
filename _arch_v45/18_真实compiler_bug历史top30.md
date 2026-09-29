# 方向 18：真实 compiler bug 历史 top 30

## 核心结论
1. 编译器自身有 bug，意味着"编译通过 ≠ 正确"——这是 QueYi 存在的根本理由之一：LLM 生成的代码可能因编译器 bug 或 UB 优化而行为异常，人/模型都难发现。
2. 真实 compiler bug 多分布在：**错误优化（UB 触发错误代码删除）、模板/constexpr 崩溃、ABI/链接错、标准库实现缺陷**。每类都能成为 QueYi 的"缺陷夹具"灵感源。
3. 引用真实 bug 报告（GCC Bugzilla / LLVM GitHub Issues / MSVC Developer Community）能极大增强 QueYi 稿的可信度与新颖性——这是现有 benchmark 很少做的"来自真实编译器缺陷"的 corpus。

## 精确数字与案例（30 类真实 bug 主题）
> 注：以下为真实存在的 bug 类别与代表性报告方向；具体 bug ID 需在你写稿时抓官方 tracker 核实（盲点见下）。

1. **GCC 空循环/无限循环误删（UB 优化）**：`for(...);` 被删。
2. **GCC 有符号溢出错误优化**：`if(x+1>x)` 被恒真优化掉。
3. **GCC 移除"看似不可达"的 `abort()`/`__builtin_unreachable` 误用**导致后续删代码。
4. **Clang `-O2` 下 memcpy 折叠破坏严格别名假设**。
5. **Clang 模板 SFINAE 在复杂递归下崩溃（ICE）**。
6. **Clang `constexpr` 求值越界未报错**。
7. **MSVC 2015 `constexpr` 大段不支持（已知落后）**。
8. **MSVC lambda 泛型捕获 `[=]` 推导错误（旧版）**。
9. **MSVC `/O2` 下浮点 fused multiply-add 与标准不符**。
10. **GCC `std::regex`  catastrophic backtracking / 极慢（已知多年）**。
11. **libstdc++ `std::string` 小字符串优化 ABI 变更致崩溃**。
12. **libc++ 某版 `std::vector` 调试模式越界漏检**。
13. **MSVC STL `<format>` 早期实现崩溃**。
14. **GCC 协程帧布局 bug（早期 `<coroutine>`）**。
15. **Clang 模块（modules）循环依赖死锁**。
16. **GCC LTO（链接时优化）跨 TU 内联错误**。
17. **Clang ThinLTO 错误去虚拟化**。
18. **MSVC 增量链接（/INCREMENTAL）符号错**。
19. **GCC `-fprofile` 插桩数值错**。
20. **Clang UBSan 误报 `alignment` 在某些平台**。
21. **GCC 对 `volatile` 访问的错误重排**。
22. **MSVC `std::atomic` 在 ARM64 内存序 bug**。
23. **GCC `std::filesystem::copy` 符号链接处理错**。
24. **Clang `[[no_unique_address]]` 布局错**。
25. **GCC `if constexpr` 嵌套模板实例化错**。
26. **MSVC `std::expected` 移动语义 bug（早版）**。
27. **GCC `std::ranges` 某算法复杂度/正确性问题**。
28. **Clang `std::simd`/向量化错误生成**。
29. **MSVC `/permissive-` 下旧代码大量报错（兼容倒退）**。
30. **跨编译器 `std::thread` 析构时 join/detach 行为差异致 UB**。

## 对阙疑的 3 条具体行动
1. **抓官方 tracker 做 corpus**：从 GCC Bugzilla / LLVM issues / MSVC Developer Community 各挑 5 个"已确认+有最小复现"的 bug，写成 QueYi 的"真实缺陷夹具"（区别于你已有的 15 条重注入夹具）。
2. **建"编译器缺陷→UB 类"映射**：把 bug 18 主题对回方向 16 的 15 类 UB，证明 QueYi taxonomy 覆盖现实缺陷源。
3. **在稿里引用 bug ID**：related work 列 10 个真实 bug 编号 + 链接，展示"我们的 corpus 来自一线编译器缺陷"，强差异化。

## 盲区（诚实标注）
- **具体 bug 编号（如 gcc bug 85491 类）我未逐一核实**，上述为真实存在的 bug 类别与方向，写稿前必须抓官方 tracker 拿到准确 ID 与状态（已确认/已修复/仍开）。
- "真实缺陷夹具"若直接复制 bug 的最小复现，需注意许可（tracker 代码通常可引用，但应注明来源）。
- 编译器版本敏感：某 bug 在 GCC 13 修复不代表 GCC 11 也修；QueYi 需固定测试编译器版本矩阵。

## 来源
- [1] GCC Bugzilla — https://gcc.gnu.org/bugzilla/
- [2] LLVM GitHub Issues — https://github.com/llvm/llvm-project/issues
- [3] MSVC Developer Community — https://developercommunity.visualstudio.com/cpp
- [4] Compiler Explorer (godbolt) 验证差异 — https://godbolt.org/

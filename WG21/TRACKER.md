# WG21 提案 → 编译器实现进度跟踪表 · TRACKER

> 提案号 → 特性 → feature-test macro → GCC / Clang / MSVC 最低支持版本 → 备注。
> **GCC 列 = 本机实测**（GCC 15.3.0 / MinGW-w64 MSVCRT，`__cpp_*` 宏真实探测，见 `_cpp_probe_gcc.json`）。
> **Clang / MSVC 列 = 官方文档快照**（cppreference compiler support，标 `[DOC]`），无本机验证。
> 自动检测当前工具链：`python3 tools/generate_wg21_tracker.py`。

**图例**：✅ 已支持 / 🚧 部分 / ❌ 未支持 / `[DOC]` 文档来源未本机验证
**实测环境锚点**：GCC 15.3.0，`-std=c++23`，51/64 探测宏已定义。

---

## C++20 语言特性

| 提案 | 特性 | feature-test macro | GCC | Clang [DOC] | MSVC [DOC] | 备注 | 章节 |
|------|------|-------------------|:---:|:---:|:---:|------|------|
| P0734 | Concepts | `__cpp_concepts` | ✅ 202002 | ✅ 10 | ✅ 19.30 | GCC 实测 202002 | ch67 |
| P1103 | Modules | `__cpp_modules` | 🚧 需 `-fmodules` | 🚧 16 | ✅ 19.28 | **GCC 默认 UNDEF**，加 `-fmodules-ts`/`-fmodules` 才 201810 | ch118 |
| P0912 | Coroutines | `__cpp_impl_coroutine` | ✅ 201902 | ✅ 14 | ✅ 19.28 | GCC 实测 201902 | ch113 |
| P0515 | 三路比较 `<=>` | `__cpp_impl_three_way_comparison` | ✅ 201907 | ✅ 10 | ✅ 19.20 | | ch24 |
| P1073 | `consteval` | `__cpp_consteval` | ✅ 201811 | ✅ 14 | ✅ 19.28 | | ch69 |
| P0692 | 聚合初始化扩展 | `__cpp_aggregate_paren_init` | ✅ 201902 | ✅ 16 | ✅ 19.29 | | ch32 |

## C++20 库特性

| 提案 | 特性 | feature-test macro | GCC | Clang [DOC] | MSVC [DOC] | 备注 | 章节 |
|------|------|-------------------|:---:|:---:|:---:|------|------|
| P0896 | Ranges | `__cpp_lib_ranges` | ✅ 202302 | ✅ 15 | ✅ 19.29 | GCC 实测 202302（含后续 DR） | ch90、ch119 |
| P0645 | `std::format` | `__cpp_lib_format` | ✅ 202304 | ✅ 17 | ✅ 19.29 | GCC 实测 202304 | ch131 |
| P0122 | `std::span` | `__cpp_lib_span` | ✅ 202002 | ✅ 7 | ✅ 19.26 | | ch82 |
| P1135 | `std::jthread`/`stop_token` | `__cpp_lib_jthread` | ✅ 201911 | ✅ 18 | ✅ 19.28 | Clang 长期缺失，18 才补 | ch94、ch103 |
| P0019 | `std::atomic_ref` | `__cpp_lib_atomic_ref` | ✅ 201806 | ✅ 19 | ✅ 19.28 | | ch107 |

## C++23 语言特性

| 提案 | 特性 | feature-test macro | GCC | Clang [DOC] | MSVC [DOC] | 备注 | 章节 |
|------|------|-------------------|:---:|:---:|:---:|------|------|
| P1938 | `if consteval` | `__cpp_if_consteval` | ✅ 202106 | ✅ 17 | ✅ 19.32 | GCC 实测 202106 | ch69 |
| P0847 | Deducing `this` | `__cpp_explicit_this_parameter` | ✅ 202110 | ✅ 18 | ✅ 19.32 | GCC 15.3 **实测已支持** 202110（注意宏名是 `__cpp_explicit_this_parameter`，非 `__cpp_deducing_this`） | ch57 |
| P2128 | 多维下标 `[]` | `__cpp_multidimensional_subscript` | ✅ 202211 | ✅ 17 | 🚧 | | ch77 |
| P2242 | 非平凡在 constexpr | `__cpp_constexpr` | ✅ 202306 | ✅ 17 | ✅ 19.33 | GCC 实测放宽版 | ch69 |
| P1102 | 省略 lambda `()` | — | ✅ | ✅ 13 | ✅ 19.33 | | ch27 |

## C++23 库特性

| 提案 | 特性 | feature-test macro | GCC | Clang [DOC] | MSVC [DOC] | 备注 | 章节 |
|------|------|-------------------|:---:|:---:|:---:|------|------|
| P0323 | `std::expected` | `__cpp_lib_expected` | ✅ 202211 | ✅ 16 | ✅ 19.33 | GCC 实测 202211 | ch88 |
| P2502 | `std::generator` | `__cpp_lib_generator` | ✅ 202207 | 🚧 | ✅ 19.43 | GCC 实测 202207，Clang 迟 | ch113 |
| P2093 | `std::print` | `__cpp_lib_print` | 🚧 宏 202211 / **链接失败** | ✅ 18 | ✅ 19.37 | GCC 实测宏已定义 202211，但本 MinGW 构建 libstdc++ 未导出 `__open_terminal`，链接失败（undefined reference）；`std::format` 等价替代。详见 ch08 附录 G | ch08、ch131 |
| P0881 | `std::stacktrace` | `__cpp_lib_stacktrace` | ❌ `<undef>` | 🚧 | ✅ 19.34 | **GCC/MinGW 无 libstdc++ backtrace**（实测 UNDEF） | ch158 |
| P0429 | `std::flat_map`/`flat_set` | `__cpp_lib_flat_map` | ✅ 202207 | 🚧 | ✅ 19.42 | GCC 15.3 实测已定义 202207 | ch85 |
| P1899 | `std::mdspan` | `__cpp_lib_mdspan` | ❌ 头缺失 | ✅ 18 | ✅ 19.39 | GCC 15.3 实测 `<mdspan>` 头不存在（fatal error: mdspan: No such file）；宏 UNDEF 同源。详见 ch08 附录 G | ch08、ch82 |

## C++26 关键提案（进行中，随标准演进变动）

| 提案 | 特性 | feature-test macro | GCC | Clang [DOC] | MSVC [DOC] | 备注 | 章节 |
|------|------|-------------------|:---:|:---:|:---:|------|------|
| P2996 | 静态反射（reflection） | `__cpp_reflection` | ❌ `<meta>` 缺失 | 🚧 实验 | ❌ | GCC15 无 `<meta>` 头（fatal error: meta: No such file），无法编译 `reflect_value`/`^T`；里程碑特性，编译器均在起步。详见 ch09 ⑩ 汇编 | ch09、ch74 |
| P2300 | `std::execution`（Sender/Receiver） | 未定名 | 🚧 头有/算法无 | 🚧 | ❌ | GCC15 `<execution>` 头可编译，但 `just`/`then` 算法未实现（'not a member of ex'）；参考实现 stdexec。注意 `__cpp_lib_execution`（实测 201902）是 **C++17 并行算法执行策略**，与 P2300 无关。详见 ch09 附录 E | ch09、ch93、ch114 |
| P2632 | `std::hive`（原 colony） | — | ❌ | ❌ | ❌ | 提案阶段 | ch85 |
| P0843 | `std::inplace_vector` | `__cpp_lib_inplace_vector` | ❌ `<undef>` | 🚧 | 🚧 | GCC 15.3 实测 UNDEF；无堆容器标准化，嵌入式关键（见 Interview E1） | ch77 |
| P2786 | Trivial relocatability | `__cpp_trivial_relocatability`（拟） | ❌ | 🚧 | ❌ | 移动优化，容器提速 | ch115 |
| P1385 | `std::linalg`（BLAS 接口） | — | ❌ | ❌ | 🚧 | mdspan 之上的线性代数 | ch82 |
| P2900 | Contracts（合约） | `__cpp_contracts`（拟） | 🚧 -fcontracts 可编译 | 🚧 实验 | ❌ | GCC15 加 `-fcontracts` 可识别 `[[pre]]/[[post]]` 语法，但链接缺 `handle_contract_violation`（实验 runtime 限制），pre 默认降级为 assume。详见 ch09 附录 G（含真机汇编） | ch09、ch121 |

---

## 关键实测结论（GCC 15.3.0 本机）

以下为本机探测中**与直觉不符、面试/工程易踩坑**的点（`__cpp_*` 实测，非文档推测）：

1. **`__cpp_modules` 默认 UNDEF**：GCC 只有加 `-fmodules`/`-fmodules-ts` 才定义（值 201810）。仅凭默认宏判断会误判「不支持模块」。
2. **Deducing `this`（P0847）宏名陷阱**：正确的 feature-test macro 是 `__cpp_explicit_this_parameter`（GCC 15.3 实测 **202110 已支持**），而非直觉的 `__cpp_deducing_this`（该名不存在，探测必得 UNDEF → 易误判为「不支持」）。判断特性支持务必用标准规定的宏名。
3. **`std::stacktrace`（P0881）MinGW 不可用**：`__cpp_lib_stacktrace` UNDEF，libstdc++ 的 backtrace 后端在 MinGW 上缺失。异常诊断类代码需条件编译降级。
4. **`std::generator`（P2502）GCC 领先 Clang**：GCC 15.3 实测 202207，Clang 迟迟未完整——协程库特性上 GCC 反而更超前。
5. **`__cpp_lib_execution` 语义陷阱**：该宏（实测 201902）指 **C++17 并行算法执行策略**，与 C++26 P2300 `std::execution`（Sender/Receiver）**完全无关**，勿因宏已定义误判 P2300 已实现。
6. **`std::print` 宏支持 ≠ 可链接运行**：`__cpp_lib_print` 实测 202211 已定义（宏层面"支持"），但本 MinGW libstdc++ 未导出 `__open_terminal`/`__write_to_terminal`，**链接失败**。特性支持须区分"宏定义 / 头存在 / 可编译链接运行"三层——仅凭宏判断会高估可用性（详见 ch08 附录 G）。
7. **Contracts 在 GCC15 是实验半成品**：`-fcontracts` 下语法可编译、生成 violation 描述与 post 检查分支，但缺 violation handler 链接符号，pre 默认按 assume；不可作为生产契约依赖（详见 ch09 附录 G 真机汇编）。

## 季度同步流程（B3.4）

每季度执行一次，保持矩阵表与真实工具链同步：

```bash
# 1. 重新探测当前工具链 __cpp_* 支持度（P0-2.4）
python3 tools/verify_compiler_features.py --gcc <path-to-g++> --out _cpp_probe_gcc.json

# 2. 生成 WG21 跟踪表差异报告（B3.3），对比 TRACKER.md 声称值
python3 tools/generate_wg21_tracker.py --probe _cpp_probe_gcc.json --tracker WG21/TRACKER.md

# 3. 若有差异（编译器升级新增/回退特性），更新本表 GCC 列 + docs/compiler-matrix.md
# 4. Clang/MSVC 列对照 cppreference compiler support 页面手动更新（标 [DOC]）
```

**同步锚点**：本表 GCC 列锚定 GCC 15.3.0（2026-07 探测）。工具链升级后须重跑步骤 1-2。

---
*Clang/MSVC 版本以 cppreference「Compiler support」页面为准，非本机验证；GCC 列均为本机 `__cpp_*` 实测。提案随 WG21 进程变动。*

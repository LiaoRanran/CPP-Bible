# 编译器版本对照矩阵 — Compiler Feature Matrix

> **本文件是「三编译器对比」的单一事实来源（single source of truth）。**
> 正文（Book/）中所有「GCC / Clang / MSVC 支持度」对比**不应写死版本号**，
> 一律通过交叉引用指向本表，例如：
> `详见 [编译器版本对照表](../docs/compiler-matrix.md#语言特性支持度)`。
>
> **设计动机**：编译器升级后只需改本文件一处，正文零改动；且支持度用
> feature-test macro 实测值表达，避免"某时间点快照"随时间失真。

---

## 0. 数据来源与可信度

| 列 | 来源 | 可信度标记 | 含义 |
|----|------|:---------:|------|
| **GCC** | `tools/verify_compiler_features.py` 本机实测 | **VERIFIED** | 宏值精确，探测日期见下 |
| **Clang** | cppreference 特性支持表（2026-Q2 快照） | **DOC** | 非本机实测，季度复验时更新 |
| **MSVC** | cppreference / MSVC 发布说明（2026-Q2 快照） | **DOC** | 非本机实测，季度复验时更新 |

**环境锚点（GCC 实测基准）**

| 项 | 值 |
|----|----|
| 编译器 | `g++.exe (MinGW-w64 x86_64-msvcrt-posix-seh, built by Brecht Sanders)` **15.3.0** |
| 探测命令 | `-std=c++23 -O0`（Modules 需额外 `-fmodules`，见备注）|
| OS | Windows 10/11（Git Bash，winlibs 发行版）|
| 探测日期 | **2026-07-15** |
| 宏定义总数 | 64 项中 **51 项已定义**（默认 flag 下）|

> ⚠️ **GCC 模块支持的特殊性（实测）**：`__cpp_modules` 在默认 `-std=c++23` 下
> **未定义（UNDEF）**，必须显式加 `-fmodules` 才定义（值 `201810`）。这与 MSVC /
> Clang 默认即定义不同，是 GCC 工具链的真实边界，跨编译器代码务必用
> `#ifdef __cpp_modules` 守卫而非假定"上了 C++20 就有模块"。

---

## 1. 语言特性支持度（Language Features）

符号：`✓` = 已定义（括号内为 **GCC 实测宏值**）；`—` = 未定义；`N/A` = 不适用。

| 特性 | feature-test macro | GCC 15.3 | Clang (DOC) | MSVC (DOC) | 首次标准 | 备注 |
|------|-------------------|:--------:|:-----------:|:----------:|---------|------|
| Concepts | `__cpp_concepts` | ✓ 202002 | ✓ ≥10 | ✓ ≥19.3 | C++20 | GCC/Clang 概念报错精确到原子约束 |
| Modules | `__cpp_modules` | — (需 `-fmodules`) | ✓ ≥16 | ✓ ≥19.5 | C++20 | **GCC 需 `-fmodules`（实测 201810）** |
| Coroutines | `__cpp_coroutines` | — | ✓ ≥14 | ✓ ≥19.10 | C++20 | GCC 经 `__cpp_impl_coroutine=201902` 提供能力 |
| Coroutine impl | `__cpp_impl_coroutine` | ✓ 201902 | ✓ | ✓ | C++20 | GCC 实测值 |
| constexpr 扩展 | `__cpp_constexpr` | ✓ 202211 | ✓ | ✓ | C++23 | GCC 实测 |
| if consteval | `__cpp_if_consteval` | ✓ 202106 | ✓ ≥14 | ✓ ≥19.3 | C++23 | GCC 实测 |
| static operator() | `__cpp_static_call_operator` | ✓ 202207 | ✓ ≥13 | ✓ ≥19.4 | C++23 | GCC 实测 |
| **deducing this** | `__cpp_explicit_this_parameter` | ✓ 202110 | ✓ ≥18 | ✓ ≥19.4 | C++23 | **GCC 15.3 实测已支持 202110**（正确宏名带 `_parameter`；`__cpp_deducing_this` 是错误名，探测必得 UNDEF） |
| 多维下标 | `__cpp_multidimensional_subscript` | ✓ 202211 | ✓ ≥15 | ✓ ≥19.3 | C++23 | GCC 实测 |
| `size_t` 后缀 `zu` | `__cpp_size_t_suffix` | ✓ 202011 | ✓ ≥13 | ✓ ≥19.3 | C++23 | GCC 实测 |
| 命名转义 `\o{}` | `__cpp_named_character_escapes` | ✓ 202207 | ✓ ≥17 | ✓ ≥19.4 | C++23 | GCC 实测 |
| 标准库模块 | `__cpp_lib_modules` | — | ✓ ≥17 (`std`/`std.compat`) | ✓ ≥19.5 | C++23 | GCC 未提供 `std` 模块（实测 UNDEF） |
| `*this` 捕获 | `__cpp_capture_star_this` | ✓ 201603 | ✓ | ✓ | C++17 | GCC 实测 |
| generic lambda | `__cpp_generic_lambdas` | ✓ 201707 | ✓ ≥14 | ✓ | C++14 | GCC 实测 |
| init-capture | `__cpp_init_captures` | ✓ 201803 | ✓ ≥14 | ✓ | C++14 | GCC 实测 |
| lambda `[=, this]` | `__cpp_lambda_capture` | — | ✓ ≥16 | ✓ | C++20 | GCC 15.3 仍未弃用旧式捕获（实测 UNDEF） |
| structured bindings | `__cpp_structured_bindings` | ✓ 201606 | ✓ ≥14 | ✓ ≥19.1 | C++17 | GCC 实测 |
| if constexpr | `__cpp_if_constexpr` | ✓ 201606 | ✓ ≥14 | ✓ ≥19.1 | C++17 | GCC 实测 |
| fold expressions | `__cpp_fold_expressions` | ✓ 201603 | ✓ ≥14 | ✓ ≥19.1 | C++17 | GCC 实测 |
| CTAD | `__cpp_deduction_guides` | ✓ 202207 | ✓ ≥14 | ✓ ≥19.1 | C++17 | GCC 实测（值 202207 含 C++20 扩展） |
| variadic using | `__cpp_variadic_using` | ✓ 201611 | ✓ ≥14 | ✓ ≥19.1 | C++17 | GCC 实测 |
| aggregate NSDMI | `__cpp_aggregate_nsdmi` | ✓ 201304 | ✓ ≥14 | ✓ ≥19.1 | C++14 | GCC 实测 |
| NTTP 扩展 | `__cpp_nontype_template_args` | ✓ 201911 | ✓ ≥14 | ✓ ≥19.1 | C++20 | GCC 实测 |
| rvalue refs | `__cpp_rvalue_references` | ✓ 200610 | ✓ | ✓ | C++11 | GCC 实测 |
| decltype | `__cpp_decltype` | ✓ 200707 | ✓ | ✓ | C++11 | GCC 实测 |
| lambdas | `__cpp_lambdas` | ✓ 200907 | ✓ | ✓ | C++11 | GCC 实测 |
| alias templates | `__cpp_alias_templates` | ✓ 200704 | ✓ | ✓ | C++11 | GCC 实测 |
| variadic templates | `__cpp_variadic_templates` | ✓ 200704 | ✓ | ✓ | C++11 | GCC 实测 |
| raw strings | `__cpp_raw_strings` | ✓ 200710 | ✓ | ✓ | C++11 | GCC 实测 |
| UDL | `__cpp_user_defined_literals` | ✓ 200809 | ✓ | ✓ | C++11 | GCC 实测 |

---

## 2. 标准库特性支持度（Library Features）

| 特性 | feature-test macro | GCC 15.3 | Clang (DOC) | MSVC (DOC) | 首次标准 | 备注 |
|------|-------------------|:--------:|:-----------:|:----------:|---------|------|
| `std::format` | `__cpp_lib_format` | ✓ 202304 | ✓ ≥14 | ✓ ≥19.32 | C++20 | GCC 实测 |
| `std::print` | `__cpp_lib_print` | ✓ 202211 | ✓ ≥18 | ✓ ≥19.38 | C++23 | GCC 实测；Clang 需 libc++ 18 |
| `std::ranges` | `__cpp_lib_ranges` | ✓ 202302 | ✓ ≥16 | ✓ ≥19.30 | C++20 | GCC 实测（值 202302 含 C++23 扩展）|
| `std::span` | `__cpp_lib_span` | ✓ 202002 | ✓ ≥14 | ✓ ≥19.2 | C++20 | GCC 实测 |
| `std::jthread` | `__cpp_lib_jthread` | ✓ 201911 | ✓ ≥14 | ✓ ≥19.28 | C++20 | GCC 实测 |
| atomic wait/notify | `__cpp_lib_atomic_wait` | ✓ 201907 | ✓ ≥11 | ✓ ≥19.2 | C++20 | GCC 实测 |
| `std::barrier` | `__cpp_lib_barrier` | ✓ 201907 | ✓ ≥11 | ✓ ≥19.2 | C++20 | GCC 实测 |
| `std::latch` | `__cpp_lib_latch` | ✓ 201907 | ✓ ≥11 | ✓ ≥19.2 | C++20 | GCC 实测 |
| `std::counting_semaphore` | `__cpp_lib_semaphore` | ✓ 201907 | ✓ ≥11 | ✓ ≥19.2 | C++20 | GCC 实测 |
| `<coroutine>` | `__cpp_lib_coroutine` | ✓ 201902 | ✓ ≥14 | ✓ ≥19.10 | C++20 | GCC 实测 |
| concepts 库 | `__cpp_lib_concepts` | ✓ 202002 | ✓ ≥10 | ✓ ≥19.3 | C++20 | GCC 实测 |
| `std::pmr` | `__cpp_lib_memory_resource` | ✓ 201603 | ✓ ≥14 | ✓ ≥19.1 | C++17 | GCC 实测 |
| `std::filesystem` | `__cpp_lib_filesystem` | ✓ 201703 | ✓ ≥14 | ✓ ≥19.1 | C++17 | GCC 实测 |
| `std::string_view` | `__cpp_lib_string_view` | ✓ 201803 | ✓ ≥14 | ✓ ≥19.1 | C++17 | GCC 实测 |
| `std::optional` | `__cpp_lib_optional` | ✓ 202110 | ✓ ≥14 | ✓ ≥19.1 | C++17 | GCC 实测（值含 C++20 扩展）|
| `std::variant` | `__cpp_lib_variant` | ✓ 202106 | ✓ ≥14 | ✓ ≥19.1 | C++17 | GCC 实测 |
| `std::any` | `__cpp_lib_any` | ✓ 201606 | ✓ ≥14 | ✓ ≥19.1 | C++17 | GCC 实测 |
| `std::shared_mutex` | `__cpp_lib_shared_mutex` | ✓ 201505 | ✓ ≥14 | ✓ ≥19.1 | C++17 | GCC 实测 |
| `std::atomic_ref` | `__cpp_lib_atomic_ref` | ✓ 201806 | ✓ ≥14 | ✓ ≥19.1 | C++20 | GCC 实测 |
| `std::to_chars` | `__cpp_lib_to_chars` | ✓ 201611 | ✓ ≥14 | ✓ ≥19.1 | C++17 | GCC 实测 |
| bit ops | `__cpp_lib_bitops` | ✓ 201907 | ✓ ≥14 | ✓ ≥19.2 | C++20 | GCC 实测 |
| `std::endian` | `__cpp_lib_endian` | ✓ 201907 | ✓ ≥14 | ✓ ≥19.2 | C++20 | GCC 实测 |
| `std::source_location` | `__cpp_lib_source_location` | ✓ 201907 | ✓ ≥14 | ✓ ≥19.2 | C++20 | GCC 实测 |
| `std::expected` | `__cpp_lib_expected` | ✓ 202211 | ✓ ≥16 | ✓ ≥19.34 | C++23 | GCC 实测 |
| `std::generator` | `__cpp_lib_generator` | ✓ 202207 | ✓ ≥17 | ✓ ≥19.38 | C++23 | GCC 实测 |
| `smart_ptr_for_overwrite` | `__cpp_lib_smart_ptr_for_overwrite` | — | ✓ ≥20 | ✓ ≥19.38 | C++20 | GCC 15.3 实测 UNDEF |
| `std::move_only_function` | `__cpp_lib_move_only_function` | — | ✓ ≥17 | ✓ ≥19.37 | C++23 | GCC 15.3 实测 UNDEF |
| `std::stacktrace` | `__cpp_lib_stacktrace` | — | ✓ ≥18 | ✓ ≥19.38 | C++23 | GCC 15.3 实测 UNDEF |
| `std::simd` | `__cpp_lib_simd` | — | — | — | C++23 | 三编译器均**未实现**（P1928 候选）|
| `<stdatomic.h>` | `__cpp_lib_stdatomic_h` | — | — | — | C++23 | GCC 15.3 实测 UNDEF |
| `std::hazard_pointer` | `__cpp_lib_hazard_pointer` | — | — | — | C++26 | 候选，均未实现 |
| `std::rcu` | `__cpp_lib_rcu` | — | — | — | C++26 | 候选，均未实现 |

---

## 3. 已知差异（诊断 / ABI / 性能）

### 3.1 诊断差异（Diagnostics）
- **概念（Concepts）报错精度**：GCC（`cp/constraint.cc`）与 Clang（`Sema::CheckConceptCheckArgs`）
  均能将约束失败定位到原子约束层面；MSVC 在 19.3 之前仅给出整条 `requires` 失败。
- **模板报错可读性**：Clang 默认 `-fdiagnostics-show-template-tree` 折叠深层嵌套；GCC 需显式开启。
- **Modules 报错**：Clang 模块错误定位到 `.ixx`/`.cppm` 行；MSVC 经 `IfcOutput` 的 `.ifc` 元数据，
  GCC 模块报错信息在 15.x 仍不如 Clang 友好（实测观察，非宏可测）。

### 3.2 ABI 差异（不可二进制兼容）
- **名称修饰（name mangling）**：GCC / Clang 用 **Itanium C++ ABI**（`_Z1fi`）；
  MSVC 用 **MSVC mangling**（`?f@@YAXH@Z`）。跨编译器链接同一目标文件**必然失败**。
- **标准库 ABI**：GCC→`libstdc++`、Clang→`libc++`（可切 libstdc++）、MSVC→**MS STL**。
  三者 `std::string`/`std::list` 布局不同，动态库跨编译器传递 STL 对象**未定义行为**。
- **异常模型**：GCC/Clang 用 Itanium 零成本异常（DWARF）；MSVC 用 SEH-based 异常。
- **结论**：同一二进制产品必须**单一工具链 + 单一标准库**编译；跨 DLL 边界传递 C++ 对象
  须用 C 接口或稳定 ABI 类型（POD / 句柄）。

### 3.3 性能差异（编译 / 运行）
- **编译速度**：Clang 前端解析快于 GCC；MSVC 单 TU 较慢但并行 `/MP` 成熟。
- **Modules 加速**：Clang / MSVC 模块化构建显著降低头文件重解析；GCC 因 `-fmodules` 成熟度，
  大项目模块化收益不稳定（实测观察）。
- **优化质量**：`-O2` 下三者生成代码质量接近；`-O3` 向量化 GCC/Clang 略优于 MSVC；
  **禁止编造数字**——具体 benchmark 见 `Benchmarks/`（P0-1 实测化任务）。

---

## 4. 定期复验流程（P0-2.5）

> 编译器每半年一大版本。为避免矩阵失真，建立季度复验：

```bash
# 1. 重新探测当前 GCC（MinGW 15.3 → 未来 16.x）特性支持
python3 tools/verify_compiler_features.py --check

# 2. diff 落盘 JSON 与上表 GCC 列，记录新增/移除的宏
diff <(python3 -c "import json;d=json.load(open('_cpp_probe_gcc.json'));\
      print('\n'.join(f'{k}={v[\"gcc_value\"]}' for k,v in d.items()))") \
     <(grep -oE '__cpp_[a-z_]+ \| (✓ [0-9]+|—)' docs/compiler-matrix.md)

# 3. 更新 Clang / MSVC 列：核对 cppreference 特性支持表（DOC 来源）
# 4. 在 ROADMAP / CHANGELOG 记录本次复验日期与变化
```

**复验记录（CHANGELOG 锚）**

| 日期 | GCC 版本 | 变化 |
|------|---------|------|
| 2026-07-15 | 15.3.0 | 基线建立：51/64 宏已定义；deducing this 已支持（`__cpp_explicit_this_parameter`=202110，早前误用 `__cpp_deducing_this` 得 UNDEF）；stacktrace / simd 仍 UNDEF |

---

_本表由 `tools/verify_compiler_features.py` 生成 GCC 列，人工补 Clang/MSVC DOC 列。
正文引用一律指向本表，禁止在 Book/ 正文写死三编译器版本号。_

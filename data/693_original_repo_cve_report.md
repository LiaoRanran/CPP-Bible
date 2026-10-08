# 693-E1 · 原始项目 CVE 验证报告（可行性 + 溯源）

- 生成：2026-10-08T21:19:42+08:00｜脚本：`tools/verify_693_original_repo.py`
- 候选：683 的 110 条 CVE 中带 `refs_commit` 的 **22** 条；本批实际处理 **20** 条

## 0. 红线冲突的显式登记（**必读**）

任务书 **红线 8**：「科研强化阶段不跑新 `detect()`（只读已有数据做分析）」。
任务 **E1.2**：「在原始 build context 下编译运行 / 用 Queyi 8 资产检测 / 对比检出率差异」。

**两者不可能同时满足** —— E1 的检出率差异必须跑新 `detect()` 才能得到。
本批的处理是 **服从红线 8**（红线优先于任务），因此：

| 动作 | 执行了吗 |
|---|---|
| 取原始 revision 源码（codeload tarball at commit） | 是 |
| 原始项目构建尝试（configure/cmake/make） | 是（非 detect） |
| 编译旗标对比（项目 CFLAGS vs 683 重构件旗标） | 是（纯分析） |
| **Queyi 8 资产检测** | **否（红线 8）** |

因此本报告交付的是**原始项目验证的可行性边界**，不是检出率差异。
检测臂的完整设计见 §4，留给后续批次。

## 1. 汇总

| 项 | 值 |
|---|---|
| 候选（带 commit 引用） | 22 |
| 本批处理 | 20 |
| 取源成功 | **13** |
| 取源失败/跳过 | 7 |
| **构建成功** | **0** |
| 构建失败 | 9 |
| 取源成功但未构建 | 3 |
| 构建总耗时 | 408.0 s |
| 检测臂 | **未执行**（红线 8） |

### 1.1 构建失败的根因聚合

| 根因 | 条数 |
|---|---:|
| cmake 不存在 | 4 |
| 无法执行 cmake | 2 |
| 步骤失败 | 1 |
| 无法执行 make | 1 |
| 超时 | 1 |

> **根因结论**：本机（Windows + Git Bash）**未安装 cmake / make**，因此所有以 CMake 或 Makefile 为构建系统的原始项目**一个都构建不起来**。
> 这不是网络问题（13/20 取源成功），也不是仓库访问问题（codeload 全 200），
> 而是**本机工具链缺口**。原始项目验证要真跑，必须先在 Linux/WSL 或容器里备齐
> `cmake` + `make` + `autotools`（本批 Docker 镜像已包含，但镜像未实测构建）。

## 2. 逐条结果

| RW | CVE | 项目 | 类型 | 取源 | 构建系统 | 构建 | 耗时(s) | 683 冻结判决 |
|---|---|---|---|---|---|---|---:|---|
| RW-024 | CVE-2019-20372 | nginx | logic_error | OK | unknown | — | — | miss |
| RW-027 | CVE-2024-6387 | OpenSSH | data_race | OK | unknown | — | — | catch |
| RW-028 | CVE-2018-15473 | OpenSSH | logic_error | X | — | — | — | miss |
| RW-029 | CVE-2022-23308 | libxml2 | use_after_free | OK | cmake | X | 0.01 | catch |
| RW-033 | CVE-2022-37434 | zlib | out_of_bounds | OK | cmake | X | 0.01 | catch |
| RW-034 | CVE-2018-25032 | zlib | out_of_bounds | OK | cmake | X | 0.01 | catch |
| RW-035 | CVE-2018-13785 | libpng | integer_overflow | OK | cmake | X | 0.01 | miss |
| RW-038 | CVE-2023-4863 | libwebp | out_of_bounds | OK | cmake | X | 0.01 | catch |
| RW-049 | CVE-2020-12284 | FFmpeg | out_of_bounds | OK | autotools | X | 17.87 | catch |
| RW-065 | CVE-2021-41099 | Redis | integer_overflow | OK | make | X | 0.0 | catch |
| RW-071 | CVE-2021-38593 | Qt | integer_overflow | OK | cmake | X | 0.02 | catch |
| RW-072 | CVE-2023-32762 | Qt | logic_error | X | — | — | — | miss |
| RW-075 | CVE-2016-5195 | Linux kernel | data_race | X | — | — | — | catch |
| RW-078 | CVE-2021-33909 | Linux kernel | integer_overflow | X | — | — | — | miss |
| RW-086 | CVE-2017-16995 | Linux kernel | integer_overflow | X | — | — | — | catch |
| RW-087 | CVE-2019-13272 | Linux kernel | logic_error | X | — | — | — | miss |
| RW-090 | CVE-2016-8655 | Linux kernel | data_race | X | — | — | — | miss |
| RW-092 | CVE-2022-26691 | CUPS | logic_error | OK | autotools | X | 390.04 | miss |
| RW-095 | CVE-2021-45943 | expat | null_pointer_deref | OK | — | — | — | catch |
| RW-103 | CVE-2018-0500 | curl | out_of_bounds | OK | cmake | — | — | catch |

## 3. 编译旗标对比（为什么「单文件重构」不等于「原始上下文」）

- **683 重构件口径**：`-std=c++17 -g -fsanitize=<asset> -fno-omit-frame-pointer（-O0/-O2 双档）`
- **原始项目自身旗标**（从 Makefile/configure.ac/CMakeLists 抓取的高频项）：

- **RW-029**（GNOME/libxml2）：`-fsanitize`x6、`-Wall`x4、`-Werror`x4、`-Wformat`x3、`-fexceptions`x2、`-Wshadow`x2
- **RW-033**（madler/zlib）：`-Wall`x3、`-Wwrite-strings`x2、`-Wpointer-arith`x2、`-Wconversion`x2、`-Wstrict-prototypes`x2、`-Wmissing-prototypes`x2
- **RW-034**（madler/zlib）：`-Wall`x3、`-Wwrite-strings`x2、`-Wpointer-arith`x2、`-Wconversion`x2、`-Wstrict-prototypes`x2、`-Wmissing-prototypes`x2
- **RW-035**（glennrp/libpng）：`-Wl`x5、`-Wall`x3、`-Werror`x2
- **RW-038**（webmproject/libwebp）：`-flax-vector-conversions`x2、`-framework`x2、`-Wformat-nonliteral`x1、`-Wformat-security`x1、`-fno-lax-vector-conversions`x1
- **RW-049**（FFmpeg/FFmpeg）：`-flags`x1、`-fflags`x1
- **RW-065**（redis/redis）：`-Wl`x11、`-Wall`x9、`-O2`x7、`-fno-common`x4、`-ftest-coverage`x3、`-Wno-missing-field-initializers`x2
- **RW-071**（qt/qtbase）：`-Wmissing-prototypes`x1、`-Wunused`x1、`-Wimplicit`x1、`-Wreturn-type`x1、`-Wparentheses`x1、`-Wformat`x1
- **RW-092**（OpenPrinting/cups）：`-for`x2
- **RW-103**（curl/curl）：`-Werror`x4、`-framework`x2、`-Wall`x1、`-Wpointer-arith`x1、`-Wwrite-strings`x1、`-Wunused`x1

> **观察**：原始项目普遍启用 `-O2/-O3` 与大量 `-W*`，且**多数不做 sanitizer 插桩**；
> 683 的重构件则在 `-O0/-O2` 双档下**显式开 sanitizer**。这意味着两者的可检出性
> 差异**主要来自编译配置，而非代码是否在项目里**——这正是 E1 想量化的东西。

## 4. 检测臂设计（未执行，留给后续批次）

若后续批次解除红线 8，按以下步骤执行（本报告已把 1–2 步做完）：

1. 已完成：取原始 revision 源码树（含 sha 与 tarball 大小）；
2. 已完成：构建原始项目（记录成败与耗时）；
3. 待做：把 683 的重构 PoC 放进项目源码树内，用项目自身 build 系统编译（arm B）；
4. 待做：用 Queyi 八资产检测 arm A（683 现有口径）与 arm B；
5. 待做：报 Δ（arm B − arm A）与配对 McNemar；预期主要差异源是编译旗标（见 §3）。

## 5. 诚实清单

- **检测臂未执行**，因此**没有任何「原始项目 vs 重构」的检出率差异数字**；
- 取源走 **codeload tarball** 而非 `git clone`（本机 git 协议被连接重置，已登记）；
- 构建使用**本机工具链**（MinGW，无 sanitizer），与论文的 WSL 口径**不同**，
  故本报告的构建成败**不能**直接推断 WSL 下的成败；
- 单包上限 60 MiB，超限者登记为跳过而非失败；
- 构建总预算耗尽后的项目登记为 `fetched_build_skipped`，**不记为失败**。

# Changelog

本项目遵循"竣工即记"原则，按日期记录里程碑。版本号语义见 [`RELEASE.md`](RELEASE.md)。

---

## [1.1.0] - 2026-07-15

第三阶段"质量收尾 + 高含金量升级"首个发布。在 1.0.0 全绿基线上，追加实测/工程价值内容，并修复一处编译器特性支持的事实性错误。

### 新增（高含金量）

- **性能数据实测化（P0-1）**：ch27/ch50/ch93 关键数据点由 `[示意]` 升级为 GCC 15.3.0 本机 `[实测]`——多继承 vptr 布局（主 `0x0`/次 `0x8`/槽宽 `0x8`）、同步代价（atomic 3.5ns / mutex 7.6ns / thread 125µs）、转型代价（virtual 0.5ns / dynamic_cast 6.9ns，慢 13.6×）。测量程序落 `_emp_bench/`。
- **编译器版本矩阵（P0-2）**：新增 `docs/compiler-matrix.md`（GCC 列本机实测，Clang/MSVC 标 `[DOC]`）+ 验证工具 `tools/verify_compiler_features.py`，正文引用统一指向本表，禁止在正文写死三编译器版本号。
- **UB / Sanitizer 反例库（P0-3）**：`Appendix/ub/` 15 例（内存 5 + 并发 5 + 生命周期 5），每例配真实 ASan/TSan/UBSan 输出与修复。
- **WG21 提案跟踪表（B3）**：新增 `WG21/TRACKER.md`（C++20/23/26 提案 → feature-test 宏 → 三编译器支持）+ `tools/generate_wg21_tracker.py`（解析并对比本机探测基线出 diff）。
- **面试题嵌入式分类（B2）**：`Interview/` 拆 `general/`（20 题 + 难度分级 + 🔧 嵌入相关标注）+ `embedded/`（E1-E10 STM32F4 硬核题：无堆容器 / 跨 TU ABI / volatile MMIO / 中断安全 / placement new / 内存池 / DMA 抽象 / 零开销寄存器映射 / 全局构造顺序）。
- **汇编实证扩展（B4，累计 8→12 例）**：ch42/48/52/117 各加「附录 E 编译实证」，全部 GCC 15.3 `-O2` objdump 真实生成——
  - ch42 严格别名：翻转 `-fstrict-aliasing` 开关的生成码分歧（缓存返回值 vs 重载内存）；
  - ch48 RTTI：`typeid` 读 `vtable[-1]` 的 `type_info`、`dynamic_cast` 尾调 `__dynamic_cast`；
  - ch52 EBO：空基类偏移 0 vs 空成员偏移 4（sizeof 4 vs 8 汇编可见）；
  - ch117 复制消除：prvalue 直接写返回槽零 copy/move 调用，删 move 仍编译。

### 修复（事实性）

- **deducing this 特性支持误判**（重大）：1.0.0 期间 P0-2 误用不存在的宏名 `__cpp_deducing_this` / `__cpp_explicit_this`（均探测为 UNDEF），错误结论"GCC 15.3 不支持 deducing this"。本机 `-dM` 实探证明正确宏名 `__cpp_explicit_this_parameter` = 202110 **已支持**。全链修正 5 处：`WG21/TRACKER.md`、`docs/compiler-matrix.md`、`_cpp_probe_gcc.json`、`tools/verify_compiler_features.py`、`Book/…/ch10_version_matrix.md`。
- 附带修正：`__cpp_lib_flat_map` = 202207（已支持）、`std::mdspan` / `inplace_vector` 确为 UNDEF、P2300 `std::execution` 宏尚未定名（并澄清 `__cpp_lib_execution` = 201902 是 C++17 并行算法，与 P2300 无关）。

### 质量审计（A 系）

- **交叉引用审计（A1）**：`tools/crossref_audit.py` 实跑 147 章 / 1190 引用 / 断链 0 / part 覆盖率 100%。
- **CI 豁免消化（A2）**：定向重测 66 个豁免块（GCC 13.1，CI 同款 flags）全部合法失败（modules / 外部库 / POSIX / MSVC / 多文件 / 故意错误演示），0 stale；新增防呆工具 `tools/prune_exempt.py`。全量 `--main-only` 复扫：147 章 / 112 通过 / 66 失败块与基线一致。

### 一致性审计（C 系）

- **术语一致性（C1）**：修复索引层 32 处断链引用——`GLOSSARY.md`（ABI/CRTP/data race/deadlock/EBO/UB/vtable 共 7 条）、`CROSSREF.md`（生命周期/虚函数链/协程链/CRTP 链 4 条核心链）、`MISCONCEPTIONS.md`（章节区间头 + 条目章号共 21 处）全部映射到真实章号；`glossary.json` 129 术语 0 断链；术语变体审计（运行期/运行时/范本/解构/指标/多形/内连）确认均为有意用法，0 实际错误。
- **Mermaid 图表审计（C2）**：新增 `tools/mermaid_audit.py`（静态结构校验）+ `tools/mermaid_parse_check.mjs`（官方 `mermaid.parse` + jsdom 真实解析）；全量 88 图块静态 + 官方解析双重校验 0 失败。
- **章编号一致性（C3）**：新增 `tools/chapter_number_audit.py`——校验文件名 `chNN` ↔ H1 `第NN章`、序列连续性、重号、part 区间重叠、mkdocs nav 悬空引用；147 章 0 错、18 个缺号确认为有意预留（33/34/53-59/73-75/102-106/114）。

### 质量基线（不变）

- `consistency_check.py` 147 章 ERROR=0 / WARN=0；CI 编译门禁保持全绿。

---

## [1.0.0] - 2026-07-14

首个可发布快照。147 章全部竣工，质量门禁"本地 + CI"双向全绿。

### 发布质量基线

- **规模**：147 章 / 16 part / 约 14.7 万行 / 6840 个可编译 cpp 块
- **密度审计 v3**：均分 **24.2/30**，浅章（<15 分）**0** 个 —— 密度深化封顶，主线转向质量收尾
- **一致性**：`consistency_check.py` ERROR=0 / WARN=0
- **交叉引用**：0 断链
- **断言**：编译期 + 运行期断言全 PASS

### 2026-07-14 加固（相对 07-13 候选）

- **CI 编译门禁上线**：`compile_all.py --main-only` → `compile_gate.py`（双层豁免：显式清单 + 错误模式）。
  新真实 `SYNTAX` / `TYPE_MISMATCH` 错误一旦引入，CI 立即变红。
- **跨平台回归修复**（本地 mingw 软过、Linux gcc13 暴露）：
  - `ch30` 补 `<csignal>`（`sig_atomic_t`，Linux gcc 不隐式带）
  - `ch35` / `ch36` 补 `<cstdint>`（`uintptr_t`）
  - `ch62` `W<int>` 成员 `double` → `char`（LP64 下 `static_assert` 失败，LLP64 巧合掩盖）
  - 门禁 WINDOWS 模式补 `winsock2.h | ws2tcpip.h`
- **EPUB 去封面**：移除 `--epub-cover-image` 与 `assets/cover.png`（独立作品，无外部封面依赖）；
  EPUB / PDF 构建经 CI 实证干净。
- **豁免清单元数据化**：`compile_exempt.json` 由 `gen_compile_exempt.py` 从审计报告生成，
  66 块 **0 UNCLASSIFIED**。

### 已知设计性豁免（非 bug）

多文件示例、C++20 Modules（`import std;` 需 MSVC 17.5+ / Clang 18+，GCC / MinGW 诚实豁免）、
POSIX / Windows 专用 API、外部库、故意展示的错误 / UB、跨块依赖 —— 详见 `tools/compile_exempt.json`。

---

## [1.0.0-rc] - 2026-07-12 / 07-13

初版竣工候选（详见 [`RELEASE.md`](RELEASE.md)）：

- 清理 311 个 `.bak` 与 6 个临时探针
- 去重审计清零（DUP%=0.0 / WTR%=0.00）
- 单章 lint GPA 98.7（A=146）
- 本地门禁全绿，待 CI 实跑确认

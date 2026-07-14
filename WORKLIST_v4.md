# WORKLIST v4.1 — 质量收尾 + 高含金量升级（2026-07-14 重构）

> **前置状态**（2026-07-14 终检）：
> - 密度 v3：avg combined=24.9/30, shallow=0, min=23, max=30, A-J 十维全非零 → 竣工
> - I 维度：62/62 全收口（13 批 / ~1,700 行纯散文）→ 竣工
> - 方向 1 汇编实证：核心机制全满 8 例 → 竣工
> - 编译门禁：112/147 通过（35 豁免），5 真实 bug 已修复
> - 一致性：30 次连续 100/100
>
> **本版新增**：5 条用户提议升级轴（2026-07-14），按价值重新排入 P0/P1 层。

---

## Phase 0：高含金量升级（P0 — 用户指定优先）

### P0-1. 性能数据"实测化"——替换 353 处 [示意]

**背景**：全书 `[示意]` 标记 353 处，集中在 ch12 构建系统(32)、ch43 缓存局部性(16)、ch163 网络(14) 等性能章。现有 Benchmarks/ 目录仅有手动 `steady_clock` 测时，未接入 Google Benchmark 框架。

**目标**：用真实 Google Benchmark 数据替换所有 [示意] 性能数字，附机器型号/编译器版本/编译 flag/多次运行取中位数。

| 子任务 | 内容 | 状态 |
|--------|------|------|
| P0-1.1 | 安装 Google Benchmark (vcpkg 或源码编译)，验证 GCC15 -O2 链路 | ⬜ |
| P0-1.2 | 写 `tools/scan_illustrative.py`：扫描 353 处 [示意]，按章节/主题分组，输出优先级矩阵 | ⬜ |
| P0-1.3 | 第一批（高价值章 10 章）：ch43 cache / ch77 vector / ch93 thread / ch40 exception / ch115 move / ch51 CRTP / ch27 cast / ch47 vtable / ch41 unique_ptr / ch107 atomic —— 每章 2-5 个 benchmark，用 Google Benchmark 重写 | ⬜ |
| P0-1.4 | 第二批（中价值章 15 章）：ch152 perf / ch154 cache / ch156 compiler_opt / ch163 net 等剩余绩效章 | ⬜ |
| P0-1.5 | 写 `tools/inject_bench_results.py`：将 benchmark JSON 输出自动替换对应的 `[示意]` 文本 | ⬜ |
| P0-1.6 | 建立 `Benchmarks/MACHINE_SPEC.md`：记录本机硬件/OS/编译器信息作为基准确认锚 | ⬜ |

**预期增量**：~200 个 .cpp benchmark 文件，~50 处 [示意]→真数据的章节替换。

### P0-2. 编译器版本矩阵表 + 定期复验机制

**背景**：全书 218 处三编译器对比提及，分散在 ch02/08/09/10/11 等标准化章。当前数据是"某个时间点的快照"——GCC15/Clang19/MSVC 2025 行为与 GCC13 时期已有差异（特别是 concepts 报错信息、modules 实现度）。

**目标**：建立 `docs/compiler-matrix.md` 集中版本对照表，正文中对比引用指向此表（不写死版本号）。

| 子任务 | 内容 | 状态 |
|--------|------|------|
| P0-2.1 | 扫描 218 处编译器对比提及，分类为「特性支持度」「报错信息」「性能差异」「ABI 差异」四类 | ⬜ |
| P0-2.2 | 创建 `docs/compiler-matrix.md`：特性→GCC版本/Clang版本/MSVC版本 + 首次支持日期 | ⬜ |
| P0-2.3 | 正文中高价值章的版本号引用改为指向矩阵表（如 `详见 [编译器版本对照表](../docs/compiler-matrix.md#concepts)`）| ⬜ |
| P0-2.4 | 写 `tools/verify_compiler_features.py`：编译期检测 __cpp_* feature-test macros，自动验证矩阵表正确性 | ⬜ |
| P0-2.5 | 建立定期复验流程：每季度跑一次 P0-2.4，diff 输出变化 | ⬜ |

**关键设计原则**：正文不写死版本号，全部通过矩阵表间接引用。编译器升级后只改一个文件。

### P0-3. 反例/UB 库 + Sanitizer 实测输出

**背景**：全书 693 处 UB 提及，但仅 273 处涉及 sanitizer——多数 UB 是理论描述，缺少 "真实 crash/sanitizer 报错" 的可视化证据。本书最大缺失：**UB 的理论描述与工程冲击之间的落差**。

**目标**：建立跨章节反例合集，每条 UB：真实代码→编译器行为→ASan/UBSan/TSan 输出→根因分析。

| 子任务 | 内容 | 状态 |
|--------|------|------|
| P0-3.1 | 创建 `Book/appendix_ub/` 目录结构：`chXX_use_after_free.md`、`chXX_data_race.md` 等，按 UB 类型组织 | ⬜ |
| P0-3.2 | 第一批（内存 UB 5 例）：use-after-free / double-free / stack-use-after-scope / alignment violation / strict-aliasing violation —— 全部附 ASan/UBSan 真实输出 | ⬜ |
| P0-3.3 | 第二批（并发 UB 5 例）：data-race / lock-order-inversion / non-atomic signal handler / thread-sanitizer 误报识别 / false-sharing 实测性能崩塌 | ⬜ |
| P0-3.4 | 第三批（生命周期 UB 5 例）：dangling reference / iterator invalidation / vptr corruption / ODR violation / const_cast mutation of const object | ⬜ |
| P0-3.5 | 写 `tools/run_sanitizer_suite.py`：一键编译+运行所有 UB 示例，收集 sanitizer 输出为 Markdown | ⬜ |
| P0-3.6 | 正文高价值章（ch28 lifetime / ch36 stack-heap / ch42 aliasing / ch93 thread / ch107 atomic）追加交叉引用到 UB 库 | ⬜ |

**产出**：`Book/appendix_ub/` 目录 ~15 个 .md 文件，每条含真实 sanitizer 输出截图/日志 + 根因分析。

---

## Phase A：质量加固（P0 — 排雷优先）

### A1. 交叉引用审计

**目标**：147 章所有 `[chNN](...)` 交叉引用不指向死链接。

| 子任务 | 内容 | 状态 |
|--------|------|------|
| A1.1 | 写脚本扫描所有 `[ch数字]` 引用，验证目标 .md 文件存在 | ⬜ |
| A1.2 | 写脚本扫描所有 `[#锚点](#...)` 内部锚点，验证目标标题存在 | ⬜ |
| A1.3 | 修复断裂引用（预估 5-15 处） | ⬜ |
| A1.4 | 补充缺失的交叉引用（核心依赖链：如 ch26 lambda → ch69 constexpr 应互引）| ⬜ |

### A2. CI 豁免消化

**目标**：减少 `compile_exempt.json` 中的可修项，提升真实门禁覆盖。

| 子任务 | 内容 | 状态 |
|--------|------|------|
| A2.1 | 审计 35 项豁免，分类为「可修」「需重构」「真豁免」| ⬜ |
| A2.2 | 修复可修项（预估 5-10 块：缺头文件/简单语法错误）| ⬜ |
| A2.3 | 标注真豁免项（平台/外部库/MSVC 专有）为永久豁免 | ⬜ |
| A2.4 | 更新豁免清单，目标 110+/147 通过 | ⬜ |

---

## Phase B：发布提升（P1 — 可见成果）

### B1. v1.1.0 发布

| 子任务 | 内容 | 状态 |
|--------|------|------|
| B1.1 | 更新 CHANGELOG.md（I 收口 + 8 例汇编 + 门禁里程碑 + Phase 0 三项）| ⬜ |
| B1.2 | 打 tag `v1.1.0` | ⬜ |
| B1.3 | 创建 GitHub Release（描述 + CHANGELOG 链接）| ⬜ |

### B2. Interview 按方向重新分类（嵌入式/系统向）

**背景**：现有 `Interview/INTERVIEW.md` 20 道通用 C++ 题，未按方向分类。用户走嵌入式/驱动方向，需独立子集。

| 子任务 | 内容 | 状态 |
|--------|------|------|
| B2.1 | 从现有 20 题中标记嵌入式相关（内存对齐/ABI/无堆环境），估约 8-10 题 | ⬜ |
| B2.2 | 新增嵌入式专属题 10 道：no-heap 容器替代、跨编译单元 ABI、volatile 在 MMIO 的正确用法、中断安全设计、placement new 在固定地址构造、constexpr 替代宏、内存池在资源受限环境、DMA 缓冲区的 C++ 抽象、硬件寄存器映射的零开销抽象、linker script 与 C++ 全局构造顺序 | ⬜ |
| B2.3 | 建立 `Interview/` 子目录：`general/`（通用 C++）+ `embedded/`（嵌入式/系统向）| ⬜ |
| B2.4 | 每道题标注对应 Book 章节、难度、公司频次 | ⬜ |

### B3. WG21 提案→编译器实现进度跟踪表

**背景**：现有 `WG21/PROPOSALS.md` 已有 C++11-20 提案索引（~30 条），但缺少 C++23/26 提案和编译器实现进度。

| 子任务 | 内容 | 状态 |
|--------|------|------|
| B3.1 | 扩展 PROPOSALS.md 覆盖 C++23/26 关键提案（~15 条元） | ⬜ |
| B3.2 | 建 `WG21/TRACKER.md`：提案号→特性→GCC/Clang/MSVC 实现版本→feature-test macro→备注 | ⬜ |
| B3.3 | 写 `tools/generate_wg21_tracker.py`：从 __cpp_* macro 自动检测当前工具链支持度，对比 TRACKER.md 标注差异 | ⬜ |
| B3.4 | 建定期同步流程：每季度跑一次 P0-2.4（编译器特征）+ B3.3（WG21 提案），diff 输出变化，更新矩阵表 | ⬜ |

### B4. 方向 1 汇编实证扩展

| 优先级 | 候选章 | 价值 |
|--------|--------|------|
| ★★★ | ch117 copy_elision | NRVO 与 RVO 的区别：NRVO 编译器拒绝时的汇编差异 |
| ★★★ | ch42 strict_aliasing | `-fstrict-aliasing` 对 load/store 指令的实际影响 |
| ★★ | ch48 rtti | `typeid` vs `dynamic_cast` 的真实指令对比 |
| ★★ | ch52 ebo | 空基类优化在 sizeof 中的实际汇编体现 |

### B5. PDF/EPUB 全量构建

| 子任务 | 内容 | 状态 |
|--------|------|------|
| B5.1 | 修复 Mermaid 图表→静态图片渲染（epub/PDF 不支持动态 SVG）| ⬜ |
| B5.2 | 跑 PDF 全量构建脚本 | ⬜ |
| B5.3 | PDF 质量检查（目录/页码/图表/代码块/中文字体）| ⬜ |

---

## Phase C：体验优化（P2 — 锦上添花）

### C1. 术语一致性

| 子任务 | 内容 | 状态 |
|--------|------|------|
| C1.1 | 建立术语映射表（约 50 个核心术语） | ⬜ |
| C1.2 | grep 扫描高频混用，逐章统一 | ⬜ |

### C2. Mermaid 图表审计

| 子任务 | 内容 | 状态 |
|--------|------|------|
| C2.1 | 全量 Mermaid 语法验证（`_mermaid_validate.mjs` 已有基础设施）| ⬜ |
| C2.2 | 修复渲染失败的图表（预估 3-8 处） | ⬜ |

### C3. 章编号一致性

| 子任务 | 内容 | 状态 |
|--------|------|------|
| C3.1 | 扫描所有 `第N章` 声明与文件名 chN 的一致性 | ⬜ |
| C3.2 | 修复编号不一致（预估 0-3 处） | ⬜ |

---

## 不纳入项（P2-，已评估）

- **C++ 嵌入式驱动适用边界专题**：评估后不纳入。C++ 在内核态基本不用，用户态驱动/BSP 工具链场景受限，独立专题容易牵强。相关内容融入 P0-3（UB 库的内存相关反例）和 B2（Interview 嵌入式题）即可覆盖核心价值。

---

## 执行约定

1. 所有改动后跑 `consistency_check.py`（必须 0/0）
2. 涉及 .cpp 块变化后跑编译门禁
3. Book/*.md 正文保持最简洁（写作风格红线）
4. 每完成一个子项 → commit + push + 记忆日志
5. ROADMAP_v3.md 跟着每批同步回填

---

## 进度总览

| Phase | 名称 | 子项数 | 完成 | 进度 |
|-------|------|--------|------|------|
| P0 | 高含金量升级（实测化 / 矩阵表 / UB库） | 17 | 0 | 0% |
| A | 质量加固（交叉引用 / CI豁免） | 8 | 0 | 0% |
| B | 发布提升（v1.1.0 / Interview / WG21 / 汇编扩展 / PDF） | 14 | 0 | 0% |
| C | 体验优化（术语 / Mermaid / 编号） | 6 | 0 | 0% |
| **合计** | | **45** | **0** | **0%** |

---

_本文件与 ROADMAP_v3.md 互补：ROADMAP 记录历史，WORKLIST 指导未来。_

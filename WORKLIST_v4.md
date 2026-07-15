# WORKLIST v4.2 — 质量收尾 + 高含金量升级（2026-07-14 重构 → 2026-07-15 全项完成 + Phase4/5 汇编矩阵并入 → 批 G/H/I/J/K 实证续扩至 45 例）

> **前置状态**（2026-07-14 终检）：
> - 密度 v3：avg combined=24.9/30, shallow=0, min=23, max=30, A-J 十维全非零 → 竣工
> - I 维度：62/62 全收口（13 批 / ~1,700 行纯散文）→ 竣工
> - 方向 1 汇编实证：核心机制全满 8 例 → 竣工；Phase 4/5 扩展至 31 例（真机 GCC 15.3.0 实证矩阵）；批 G/H 续扩至 **37 例**
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
| P0-1.1 | 安装 Google Benchmark (vcpkg 或源码编译)，验证 GCC15 -O2 链路 | ✅ |
| P0-1.2 | 写 `tools/scan_illustrative.py`：扫描 353 处 [示意]，按章节/主题分组，输出优先级矩阵 | ✅ |
| P0-1.3 | 第一批（高价值章 10 章）：ch43 cache / ch77 vector / ch93 thread / ch40 exception / ch115 move / ch51 CRTP / ch27 cast / ch47 vtable / ch41 unique_ptr / ch107 atomic —— 每章 2-5 个 benchmark，用 Google Benchmark 重写 | ✅ |
| P0-1.4 | 第二批（中价值章 15 章）：ch152 perf / ch154 cache / ch156 compiler_opt / ch163 net 等剩余绩效章 | ✅ |
| P0-1.5 | 写 `tools/inject_bench_results.py`：将 benchmark JSON 输出自动替换对应的 `[示意]` 文本 | ✅ |
| P0-1.6 | 建立 `Benchmarks/MACHINE_SPEC.md`：记录本机硬件/OS/编译器信息作为基准确认锚 | ✅ |

**预期增量**：~200 个 .cpp benchmark 文件，~50 处 [示意]→真数据的章节替换。

### P0-2. 编译器版本矩阵表 + 定期复验机制

**背景**：全书 218 处三编译器对比提及，分散在 ch02/08/09/10/11 等标准化章。当前数据是"某个时间点的快照"——GCC15/Clang19/MSVC 2025 行为与 GCC13 时期已有差异（特别是 concepts 报错信息、modules 实现度）。

**目标**：建立 `docs/compiler-matrix.md` 集中版本对照表，正文中对比引用指向此表（不写死版本号）。

| 子任务 | 内容 | 状态 |
|--------|------|------|
| P0-2.1 | 扫描 218 处编译器对比提及，分类为「特性支持度」「报错信息」「性能差异」「ABI 差异」四类 | ✅ |
| P0-2.2 | 创建 `docs/compiler-matrix.md`：特性→GCC版本/Clang版本/MSVC版本 + 首次支持日期 | ✅ |
| P0-2.3 | 正文中高价值章的版本号引用改为指向矩阵表（如 `详见 [编译器版本对照表](../docs/compiler-matrix.md#concepts)`）| ✅ |
| P0-2.4 | 写 `tools/verify_compiler_features.py`：编译期检测 __cpp_* feature-test macros，自动验证矩阵表正确性 | ✅ |
| P0-2.5 | 建立定期复验流程：每季度跑一次 P0-2.4，diff 输出变化 | ✅ |

**关键设计原则**：正文不写死版本号，全部通过矩阵表间接引用。编译器升级后只改一个文件。

### P0-3. 反例/UB 库 + Sanitizer 实测输出

**背景**：全书 693 处 UB 提及，但仅 273 处涉及 sanitizer——多数 UB 是理论描述，缺少 "真实 crash/sanitizer 报错" 的可视化证据。本书最大缺失：**UB 的理论描述与工程冲击之间的落差**。

**目标**：建立跨章节反例合集，每条 UB：真实代码→编译器行为→ASan/UBSan/TSan 输出→根因分析。

| 子任务 | 内容 | 状态 |
|--------|------|------|
| P0-3.1 | 创建 `Book/appendix_ub/` 目录结构：`chXX_use_after_free.md`、`chXX_data_race.md` 等，按 UB 类型组织 | ✅ |
| P0-3.2 | 第一批（内存 UB 5 例）：use-after-free / double-free / stack-use-after-scope / alignment violation / strict-aliasing violation —— 全部附 ASan/UBSan 真实输出 | ✅ |
| P0-3.3 | 第二批（并发 UB 5 例）：data-race / lock-order-inversion / non-atomic signal handler / thread-sanitizer 误报识别 / false-sharing 实测性能崩塌 | ✅ |
| P0-3.4 | 第三批（生命周期 UB 5 例）：dangling reference / iterator invalidation / vptr corruption / ODR violation / const_cast mutation of const object | ✅ |
| P0-3.5 | 写 `tools/run_sanitizer_suite.py`：一键编译+运行所有 UB 示例，收集 sanitizer 输出为 Markdown | ✅ |
| P0-3.6 | 正文高价值章（ch28 lifetime / ch36 stack-heap / ch42 aliasing / ch93 thread / ch107 atomic）追加交叉引用到 UB 库 | ✅ |

**产出**：`Book/appendix_ub/` 目录 ~15 个 .md 文件，每条含真实 sanitizer 输出截图/日志 + 根因分析。

---

## Phase A：质量加固（P0 — 排雷优先）

### A1. 交叉引用审计

**目标**：147 章所有 `[chNN](...)` 交叉引用不指向死链接。

| 子任务 | 内容 | 状态 |
|--------|------|------|
| A1.1 | 写脚本扫描所有 `[ch数字]` 引用，验证目标 .md 文件存在 | ✅ |
| A1.2 | 写脚本扫描所有 `[#锚点](#...)` 内部锚点，验证目标标题存在 | ✅ |
| A1.3 | 修复断裂引用（预估 5-15 处） | ✅ |
| A1.4 | 补充缺失的交叉引用（核心依赖链：如 ch26 lambda → ch69 constexpr 应互引）| ✅ |

### A2. CI 豁免消化

**目标**：减少 `compile_exempt.json` 中的可修项，提升真实门禁覆盖。

| 子任务 | 内容 | 状态 |
|--------|------|------|
| A2.1 | 审计 35 项豁免，分类为「可修」「需重构」「真豁免」| ✅ |
| A2.2 | 修复可修项（预估 5-10 块：缺头文件/简单语法错误）| ✅ |
| A2.3 | 标注真豁免项（平台/外部库/MSVC 专有）为永久豁免 | ✅ |
| A2.4 | 更新豁免清单，目标 110+/147 通过 | ✅ |

---

## Phase B：发布提升（P1 — 可见成果）

### B1. v1.1.0 发布

| 子任务 | 内容 | 状态 |
|--------|------|------|
| B1.1 | 更新 CHANGELOG.md（I 收口 + 8 例汇编 + 门禁里程碑 + Phase 0 三项）| ✅ |
| B1.2 | 打 tag `v1.1.0` | ✅ |
| B1.3 | 创建 GitHub Release（描述 + CHANGELOG 链接）| ✅ |

### B2. Interview 按方向重新分类（嵌入式/系统向）

**背景**：现有 `Interview/INTERVIEW.md` 20 道通用 C++ 题，未按方向分类。用户走嵌入式/驱动方向，需独立子集。

| 子任务 | 内容 | 状态 |
|--------|------|------|
| B2.1 | 从现有 20 题中标记嵌入式相关（内存对齐/ABI/无堆环境），估约 8-10 题 | ✅ |
| B2.2 | 新增嵌入式专属题 10 道：no-heap 容器替代、跨编译单元 ABI、volatile 在 MMIO 的正确用法、中断安全设计、placement new 在固定地址构造、constexpr 替代宏、内存池在资源受限环境、DMA 缓冲区的 C++ 抽象、硬件寄存器映射的零开销抽象、linker script 与 C++ 全局构造顺序 | ✅ |
| B2.3 | 建立 `Interview/` 子目录：`general/`（通用 C++）+ `embedded/`（嵌入式/系统向）| ✅ |
| B2.4 | 每道题标注对应 Book 章节、难度、公司频次 | ✅ |

### B3. WG21 提案→编译器实现进度跟踪表

**背景**：现有 `WG21/PROPOSALS.md` 已有 C++11-20 提案索引（~30 条），但缺少 C++23/26 提案和编译器实现进度。

| 子任务 | 内容 | 状态 |
|--------|------|------|
| B3.1 | 扩展 PROPOSALS.md 覆盖 C++23/26 关键提案（~15 条元） | ✅ |
| B3.2 | 建 `WG21/TRACKER.md`：提案号→特性→GCC/Clang/MSVC 实现版本→feature-test macro→备注 | ✅ |
| B3.3 | 写 `tools/generate_wg21_tracker.py`：从 __cpp_* macro 自动检测当前工具链支持度，对比 TRACKER.md 标注差异 | ✅ |
| B3.4 | 建定期同步流程：每季度跑一次 P0-2.4（编译器特征）+ B3.3（WG21 提案），diff 输出变化，更新矩阵表 | ✅ |

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
| B5.1 | 修复 Mermaid 图表→静态图片渲染（epub/PDF 不支持动态 SVG）| ✅ |
| B5.2 | 跑 PDF 全量构建脚本 | ✅ |
| B5.3 | PDF 质量检查（目录/页码/图表/代码块/中文字体）| ✅ |

---

## Phase C：体验优化（P2 — 锦上添花）

### C1. 术语一致性

| 子任务 | 内容 | 状态 |
|--------|------|------|
| C1.1 | 建立术语映射表（约 50 个核心术语） | ✅ |
| C1.2 | grep 扫描高频混用，逐章统一 | ✅ |

### C2. Mermaid 图表审计

| 子任务 | 内容 | 状态 |
|--------|------|------|
| C2.1 | 全量 Mermaid 语法验证（`_mermaid_validate.mjs` 已有基础设施）| ✅ |
| C2.2 | 修复渲染失败的图表（预估 3-8 处） | ✅ |

### C3. 章编号一致性

| 子任务 | 内容 | 状态 |
|--------|------|------|
| C3.1 | 扫描所有 `第N章` 声明与文件名 chN 的一致性 | ✅ |
| C3.2 | 修复编号不一致（预估 0-3 处） | ✅ |

---


---

## Phase D：真机汇编实证矩阵（ASM MATRIX，Phase 4/5 扩展轴）

> 与 ROADMAP_v3.md §10.5、_asm_demo/INDEX.md 互补。本阶段把"每个 C++ 抽象在 GCC 15.3.0 下到底生成什么代码"系统化，累计 31 例真机实证（全部真实编译 + 真实 `objdump`，绝不伪造）。

| 子任务 | 内容 | 状态 |
|--------|------|------|
| P4-1 | ch08 C++23 真机实证（expected/generator/format/opt/ranges） | ✅ |
| P4-2 | ch09 C++26 真机实证（contracts/-fcontracts；mdspan/print/reflection 诚实标注不可用） | ✅ |
| P4-3 | WG21 TRACKER 真机对齐（5 行 GCC 列对齐实测结论） | ✅ |
| P4-4 | 门禁复验 + 提交 + 推送 + 收尾 | ✅ |
| P4-5-1~4 | ch08 优化等级对比 + ranges 零成本 + 附录 G.4/G.5 + TRACKER P0896 链接 | ✅ |
| P5-1~3 | 批 A：原子内存序屏障 / shared_ptr 引用计数 / 批 A 收尾 | ✅ |
| P5-4~5 | 批 A 续：atomic_rmw(lock xadd/cmpxchg) / fence(lock or 全屏障) | ✅ |
| P5-6~8 | 批 B：constexpr 零痕迹 / perfect_fwd 引用折叠 / nrvo 拷贝省略 | ✅ |
| P5-9~10 | 批 C：string SSO / vector 扩容三连 | ✅ |
| P5-11~12 | 批 D：虚调用 vs CRTP / variant+visit 索引分派 | ✅ |
| P5-13~14 | 批 E/F：pmr 分配路径 / std::function 类型擦除 | ✅ |

**产出**：`_asm_demo/` 下 31 组 `.cpp`+`.s`（`.o`/`.exe` 被 gitignore）；每例嵌入目标章"附录"小节（正文最简洁）；`STATE.json` `assembly_empirical_examples=31`；一致性门禁 31 次连续 100/100。

---

## Phase E：批 G 高相关非显然实证（ASM MATRIX 扩展续，2026-07-15）

> 承接 Phase D 的 31 例真机矩阵，补 3 例**嵌入式/系统向高相关、且直觉易错**的抽象：lambda 捕获的指令代价与闭包布局、虚继承的 this 调整 thunk、noexcept 对异常处理元数据体积的影响。全部 GCC 15.3.0 真机 `objdump`/`-h`，绝不伪造；SEH/ELF 差异已显式区分。

| 子任务 | 内容 | 状态 |
|--------|------|------|
| G1 | ASM-26-lambda-capture：ch26 附录H。无捕获 1B / 按值捕获值 4B（调用点寄存器搬运 0 访存）/ 按引用捕获 8B（调用点经指针二次解引用）；目标可证明不变时 GCC 折叠引用捕获为零开销，实时读取才显式二次解引用 | ✅ |
| G2 | ASM-50-vi：ch50 新增[实现]节。虚继承 `virtual thunk to D::f()`（`_ZTv0_n24_N1D1fEv`）经 vbtable 运行时查虚基类偏移（`add rcx,[rax-0x18]`）调整 this，非固定 `sub`；成员访问也走 vbptr 间接，比非虚 MI thunk 更贵 | ✅ |
| G3 | ASM-40-noexcept：ch40 新增实战实证节。MinGW/Win64 SEH 下 `may_throw` EH 元数据 100B vs `no_throw` 32B（−68%）；`.xdata.unlikely`（LSDA 块）整体消失，`.text.unlikely` 抛异常冷路径消除；等价 ELF `.gcc_except_table` 消失 | ✅ |

**产出**：`_asm_demo/` 累计 **34 组**实证（31+3）；`STATE.json` `assembly_empirical_examples=34`；一致性门禁维持 100/100；INDEX.md 已建"批 G"小节并单列三例。

## Phase E 续：批 H 零成本词汇类型（ASM MATRIX 扩展续，2026-07-15）

> 承接批 G，补 3 例**零成本抽象直觉易错**的词汇类型：std::optional 空间膨胀却访问零间接、std::span 仅 {ptr,size} 且 operator[] 不查边界、std::tuple get<N>/结构化绑定为编译期偏移访问。全部 GCC 15.3.0 真机 objdump，绝不伪造。

| 子任务 | 内容 | 状态 |
|--------|------|------|
| H1 | ASM-88-optional：ch88 附录。访问零额外间接（值单条 mov，engaged 标志@offset4）；空间代价真实：optional<int> 8B / optional<long long> 16B / optional<char> 2B（vs int 4B） | ✅ |
| H2 | ASM-82-span：ch82 附录。遍历与裸 ptr+len 逐字节同码；operator[] 无运行时边界检查（越界静默 UB）；sizeof=16（ptr+size_t） | ✅ |
| H3 | ASM-89-tuple：ch89 附录。get<N> 编译期偏移访问（无索引计算）；结构化绑定与裸 struct 成员访问逐字节相同；libstdc++ 递归继承致末参在最底地址（get<2>@0/get<1>@8/get<0>@16），sizeof=24 | ✅ |

**产出**：`_asm_demo/` 累计 **37 组**实证（34+3）；`STATE.json` `assembly_empirical_examples=37`；一致性门禁维持 100/100；INDEX.md 已建"批 H"小节并单列三例。

## Phase F：批 I/J/K 零成本词汇/容器/类型实证（ASM MATRIX 扩展续，2026-07-15）

> 承接批 H，补 8 例**零成本抽象直觉易错、且嵌入式高频**的机制：std::array 与裸数组同码、string_view 布局反直觉（len 在前）、initializer_list 寿命陷阱、bitset 边界检查代价、<bit> 默认软件 popcount、enum class 强类型零开销、map/unordered_map 的真实指针追逐与整数除法。全部 GCC 15.3.0 真机 objdump，绝不伪造。

| 子任务 | 内容 | 状态 |
|--------|------|------|
| I1 | ASM-80-array：ch80 附录。`std::array` 与裸数组逐字节同布局（均 32B）；`operator[]`=`mov eax,[rcx+rdx*4]` 无边界检查；`at()`=`cmp rdx,0x7`+`ja` throw；`data()`=`mov rax,rcx`；按值整段 32B 拷贝 | ✅ |
| I2 | ASM-81-string_view：ch81 附录（接 SSO）。`string_view`={len@0,ptr@8}、16B；`sv_substr` 零 call O(1)；`str_substr` 含 `_M_create/_M_copy` 调用 O(n)；`sv_at`=`add rdx,[rcx+8]`+`movzx` 无检查 | ✅ |
| I3 | ASM-32-init_list：ch32 附录。`initializer_list`={ptr@0,len@8}；range-for 退化为指针自增循环；`dangling_il()` 触发 `-Winit-list-lifetime` 告警；字面量提升为 .rdata 非常量悬垂 | ✅ |
| J1 | ASM-87-bitset：ch87 附录。`bitset_flip`=`not`；`bitset_set/test` 移位+位运算带 `cmp i,0x3f` 边界检查；`bitset_count` 拆低/高 32 位各 call 一次 popcount 运行库 | ✅ |
| J2 | ASM-87-bit：ch87 附录（接 bitset）。`popcnt_u` 默认走运行库 SWAR；`bswap_u`=`bswap`；`to_float`=`movd`；`is_pow2`=`(x-1)<(x^(x-1))`；`-mpopcnt` 后 `popcnt eax,ecx` 单指令 | ✅ |
| J3 | ASM-24-enum：ch24 附录。`use_enum`=`movzx`+`add`+越界`cmovae`；`use_plain`=`lea [rcx+1]` 隐式转换零成本；`enum_underlying`=`mov eax,ecx` | ✅ |
| K1 | ASM-83-map：ch83 附录。`build()` 三次 `call _M_emplace_hint_unique`（每元素 `operator new` 节点）；`find_it` 沿 `+0x10`左/`+0x18`右指针追逐比较键`@0x20`，O(log n) | ✅ |
| K2 | ASM-85-unordered：ch85 附录。`build()` 节点堆分配+桶数组（`max_load_factor=0x3f800000`）；`find_it` 先 `div r11` 取桶索引再沿 `+0x00` next 单链表比较键`@0x08` | ✅ |

**产出**：`_asm_demo/` 累计 **45 组**实证（37+8）；`STATE.json` `assembly_empirical_examples=45`；一致性门禁维持 100/100；INDEX.md 已建"批 I/J/K"小节并单列八例。

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
| P0 | 高含金量升级（实测化 / 矩阵表 / UB库） | 17 | 17 | 100% |
| A | 质量加固（交叉引用 / CI豁免） | 8 | 8 | 100% |
| B | 发布提升（v1.1.0 / Interview / WG21 / 汇编扩展 / PDF） | 14 | 14 | 100% |
| C | 体验优化（术语 / Mermaid / 编号） | 6 | 6 | 100% |
| E | 批 G 高相关非显然实证（lambda 捕获 / 虚继承 / noexcept 元数据） | 3 | 3 | 100% |
| E2 | 批 H 零成本词汇类型（optional / span / tuple） | 3 | 3 | 100% |
| F-I | 批 I 零成本词汇/容器（array / string_view / init_list） | 3 | 3 | 100% |
| F-J | 批 J 零成本工具与强类型（bitset / <bit> / enum） | 3 | 3 | 100% |
| F-K | 批 K 关联容器（map / unordered_map） | 2 | 2 | 100% |
| **合计** | | **59** | **59** | **100%** |

---

_本文件与 ROADMAP_v3.md 互补：ROADMAP 记录历史，WORKLIST 指导未来。_

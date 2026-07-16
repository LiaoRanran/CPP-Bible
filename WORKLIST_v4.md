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

**产出**：`_asm_demo/` 累计 **53 组**实证（37+3+11）；`STATE.json` `assembly_empirical_examples=53`；一致性门禁维持 100/100；INDEX.md 已建"批 I/J/K/L"小节。

## Phase G：批 L STL 容器真实成本实证（ASM MATRIX 容器收尾，2026-07-15）

> 批 L 补 8 例**容器级别的非显然底层代价**——deque 双间接 vs vector 单间接、list/forward_list 每元素堆分配 vs 缓存局部性、set 红黑树指针追逐 vs unordered_set 整数除桶、适配器编译期委托零开销、any SBO 边界超 16B 即堆。全部 GCC 15.3.0 `-O2` 链接 exe 后 objdump，附录注入 6 个目标章（ch78/79/84/85/86/89）。

| 子任务 | 内容 | 状态 |
|--------|------|------|
| L1 | ASM-78-deque：ch78 附录。分块大小=0x200(512B=128×int)；`operator[]`=`sar rdx,0x7`块索引→map查表→`lea rdx,[rdx+r9*4]`元素偏移双间接；push_back 越块 operator new(0x200) |  ✅ |
| L2 | ASM-79-list：ch79 附录。每元素 operator new 24B 节点(prev+next+value)；遍历=`mov rax,[rax+0x8]` next追逐无缓存局部性 | ✅ |
| L3 | ASM-79-fwdlist：ch79 附录（与 list 同章）。无 size 成员 O(n) distance；before_begin 哨兵；insert_after 仅改写 2 next 指针；节点 16B（比 list 省 8B） | ✅ |
| L4 | ASM-84-set：ch84 附录。每节点 operator new(0x28=40B)；find 比较键@0x20 追逐左@0x10/右@0x18；键即值均存 0x20 | ✅ |
| L5 | ASM-85-uset：ch85 附录。find div 取桶→next 链比较值@0x08；节点 16B；rehash O(n) 全量桶重建 | ✅ |
| L6 | ASM-86-pq：ch86 附录。push=push_back+push_heap 上浮环(sar除2+cmp+swap)；top=c.front() 单 load；零开销 | ✅ |
| L7 | ASM-86-adapters：ch86 附录（与 pq 同章）。stack.top()=deque.back()；queue.front() 直接读 deque._M_start 首元素无函数调用；queue.back()=deque.back()；全编译期委托 | ✅ |
| L8 | ASM-89-any：ch89 附录。≤16B 走 _Manager_internal SBO 内联（零 operator new）；>16B 走 _Manager_external+operator new；any_cast 内联 typeid 校验 | ✅ |


## Phase APP：应用层增强（习题重写 / 工业深挖 / 用法演绎，2026-07-15 启动）

> 诊断（2026-07-15）：全书机制层深度足够（密度 avg 24.9/30，53 组真机实证），但**应用层偏薄**——
> (1) 全部章节的 `## 自测练习` 为同一套与主题无关的模板题（max 模板 / concept add / constexpr fact，全 ★★）；
> (2) 仅 ~8/147 章有 step-by-step「用法演绎」；
> (3) 部分工业附录为"开源链接列表"而缺逐行代码解读。
> 用户明确要求："还得多点习题，工业例子，用法演示演绎"。不增章、不扩写正文（实证/演示入附录）。

**三条工作线**
- **APP-A 习题重写**：把模板题替换为章主题对齐的难度阶梯（★★→★★★→★★★★），含可编译答案与 `[标准]` 标注。
- **APP-B 工业深挖**：将"链接列表"式工业附录升级为真实开源代码段的逐行解读 + 取舍对照。
- **APP-C 用法演绎**：为关键章追加 `## 附录：用法演绎` step-by-step 场景推导（选型→错误→修复→结论）。

**Batch APP1（已完成，2026-07-15）**：8 章首批全覆盖 APP-A + APP-C

| 子任务 | 章 | 内容 |
|--------|:---:|------|
| APP1 | ch20 引用指针 | 习题：引用别名零开销 / optional_ref 实现 / 返回引用vs指针；演绎：返回引用还是指针 |
| APP1 | ch27 类型转换 | 习题：static_cast 窄化 / reinterpret_cast MMIO / dynamic_cast 虚继承；演绎：类型双关正确姿势 |
| APP1 | ch41 智能指针 | 习题：unique vs shared / 循环引用 weak_ptr / make_shared+deleter；演绎：裸指针→unique_ptr 迁移 |
| APP1 | ch47 虚函数 | 习题：多态分发 / 构造期虚调用 / CRTP vs 虚函数；演绎：可扩展插件系统设计 |
| APP1 | ch77 vector | 习题：reserve 复杂度 / 迭代器失效 / erase_remove_if+vector<bool>；演绎：百万构建性能对决 |
| APP1 | ch78 deque | 习题：头部插入 / 双间接常数 / 单调队列；演绎：双端缓冲选型 |
| APP1 | ch93 线程异步 | 习题：thread join/detach / async 阻塞析构 / 数据竞争 atomic；演绎：并行求和竞争现场 |
| APP1 | ch96 排序 | 习题：stable_sort / introsort / nth_element top-k；演绎：top-k 与中位数正确打开方式 |

> 一致性门禁：147 章 ERROR=0 / WARN=0 = 100/100（注入后复验通过）。APP-A/H-C 覆盖 8/147 章。

**Batch APP2（已完成，2026-07-15）**：第二批 8 章全覆盖 APP-A + APP-C（其中 ch42/ch50 含既有真机 ASM 附录，脚本仅替换习题块并在 EOF 追加演绎，ASM 零破坏）

| 子任务 | 章 | 内容 |
|--------|:---:|------|
| APP2 | ch21 const 家族 | 习题：const 重载 / constexpr vs const / constinit+consteval；演绎：const 的层层含义 |
| APP2 | ch31 运算符重载 | 习题：operator+<< / <=> 三路比较 / rule of 5+noexcept 移动；演绎：rule of 3→5 安全字符串类 |
| APP2 | ch39 RAII | 习题：RAII 资源守卫 / ScopeGuard / copy-and-swap 强异常安全；演绎：10 处 open/close → 0 泄漏 |
| APP2 | ch42 严格别名 | 习题：reinterpret_cast UB / byte* 万能别名 / __restrict 向量化；演绎：严格别名如何悄悄改结果（保留附录E ASM） |
| APP2 | ch43 缓存局部性 | 习题：行/列优先遍历 / false sharing / AOS vs SOA；演绎：矩阵遍历 10× 加速 |
| APP2 | ch44 内存池 | 习题：固定块池 / pmr 接入 STL / 碎片对比；演绎：实时系统 new→内存池 |
| APP2 | ch50 多重继承 | 习题：非虚 MI 两份基类 / 菱形二义 / virtual 继承代价；演绎：菱形继承要不要 virtual（保留[实现] ASM） |
| APP2 | ch51 CRTP | 习题：CRTP 静态多态 / Barton-Nackman / CRTP vs 虚函数；演绎：虚函数→零成本静态分发 |

> 一致性门禁（APP3 注入后）：147 章 ERROR=0 / WARN=0 = 100/100；5 章新注入 cpp 块编译校验通过（GCC15.3 -O2 -Wall -Wextra，ch27 2516B / ch41 882B / ch96 1076B / ch110 844B / ch133 自包含块）。APP-A/APP-C 累计覆盖 21/147 章。

**Batch APP4（已完成，2026-07-16）**：模板核心簇 8 章全覆盖 APP-A + APP-C（习题重写 + 用法演绎附录）

| 子任务 | 章 | 内容 |
|--------|:---:|------|
| APP4 | ch60 模板基础 | 习题：clamp 默认模板参数 / Matrix 非类型参数 / pi+Vec 变量+别名模板；演绎：默认参数位置 + 非类型参数编译期常量 |
| APP4 | ch62 特化 | 习题：PointHash 自定义哈希器(可编译) / 类模板序列化特化 / is_ptr_like 偏特化；演绎：MyHash 特化签名匹配 + 偏序歧义 |
| APP4 | ch63 变参 | 习题：递归 print_all / fold 重写 / make_array(index_sequence)；演绎：base case + 包展开运算符 |
| APP4 | ch64 折叠 | 习题：sum/product 折叠方向 / all/any 短路 / for_each 逗号折叠；演绎：`-`/`/` 方向 + 空包语义 |
| APP4 | ch65 类型萃取 | 习题：手写 my_is_pointer / enable_if to_string / void_t has_serialize；演绎：enable_if 位置 + void_t 探测 callable |
| APP4 | ch66 SFINAE | 习题：enable_if load / void_t has_iterator / tag dispatch foo；演绎：SFINAE 软失败 vs 硬错误 + 条件互补 |
| APP4 | ch67 concepts | 习题：integral add / requires Addable/Printable/Reportable / concept to_string 重写；演绎：requires 分号 + 诊断优势 |
| APP4 | ch68 TMP | 习题：Fact 元函数 / TypeList / if constexpr process；演绎：终止特化 + if constexpr 编译期常量条件 |

> 一致性门禁：147 章 ERROR=0 / WARN=0 = 100/100（注入后复验通过）。靶向编译校验：40 注入块 GCC 13.1 -O2 -Wall -Wextra 0 fail（ch60/62/63/64/65/66/67/68）。4 处真实缺陷修复：std::clamp C++20 四参 ADL 歧义 / std::hash 特化须位于 std 命名空间（改用自定义哈希器）/ enable_if 返回类型 size_t 后误 .length()。APP-A/APP-C 累计覆盖 29/147 章。

**Batch APP5（已完成，2026-07-16）**：模板/编译期簇尾章 5 章全覆盖 APP-A + APP-C（习题重写 + 用法演绎附录）

| 子任务 | 章 | 内容 |
|--------|:---:|------|
| APP5 | ch61 模板重载 | 习题：max 双类型重载 / 区间模板 + SFINAE / 模板友元；演绎：重载决议 + 非推导语境 |
| APP5 | ch69 constexpr | 习题：constexpr 字符串长度 / 编译期斐波那契 / if constexpr 分发；演绎：constexpr 求值边界 + 编译期 vs 运行期 |
| APP5 | ch70 标签分发 | 习题：标签分发 dispatch / 迭代器 category 重载 / enum 标签；演绎：标签类空类型 + 重载决议优先级 |
| APP5 | ch71 策略类 | 习题：策略模板参数 / 运行时策略选择 / 特征萃取策略；演绎：策略注入点 + 编译期组合 |
| APP5 | ch72 表达式模板 | 习题：惰性代理求值 / 悬垂代理陷阱 / 物化安全写法；演绎：惰性代理单次遍历 + 寿命约束 |

> 一致性门禁：147 章 ERROR=0 / WARN=0 = 100/100（注入后复验通过）。靶向编译校验：30 注入块 GCC 13.1 -O2 -Wall -Wextra 0 fail（ch61/69/70/71/72）。1 处真实缺陷修复：ch72 演绎1 最小化 Vec 缺 `Vec(const VecAdd&)` 转换构造，导致 `Vec ab = a + b` 因 VecAdd→Vec 无可行转换失败（演绎2/练习3 已有该构造故通过），补转换构造后编译通过。APP-A/APP-C 累计覆盖 34/147 章。

**Batch APP6（已完成，2026-07-16）**：内存管理簇 5 章全覆盖 APP-A + APP-C（习题重写 + 用法演绎附录）

| 子任务 | 章 | 内容 |
|--------|:---:|------|
| APP6 | ch35 内存布局 | 习题：offsetof 字段偏移 / 对齐填充 sizeof / 栈堆增长方向；演绎：地址空间段布局 + 对齐陷阱 |
| APP6 | ch36 栈与堆 | 习题：栈对象生命周期 / RAII 异常安全 / 堆分配开销计时；演绎：悬垂引用 + 运行时缓冲选型 |
| APP6 | ch37 new/delete | 习题：类域 operator new 计数 / placement new 重建 / 对象池；演绎：空闲链表 node 池化降碎片 |
| APP6 | ch38 分配器 | 习题：pmr monotonic_buffer_resource / 计数资源 / reserve 扩容；演绎：资源生命周期陷阱 + 池化降延迟 |
| APP6 | ch40 异常安全 | 习题：copy-and-swap / 栈展开 / 事务式提交；演绎：dtor noexcept + noexcept 移动保证强异常安全 |

> 一致性门禁：147 章 ERROR=0 / WARN=0 = 100/100（注入后复验通过）。靶向编译校验：25 注入块 GCC 13.1 -O2 -Wall -Wextra 0 fail（ch35/36/37/38/40；其中 ch37 的 3 个 operator-new 块命中 OPERATOR_REPLACE_RE 被门禁跳过，经 `_verify_ch37_manual.py` 独立 TU 编译 0 fail 确认可编译）。1 处真实缺陷修复：ch38 演绎2 `std::pmr::vector<int> v(std::pmr::polymorphic_allocator<int>(&res));` 触发 most-vexing-parse（被解析为函数声明，`v.push_back` 报 "non-class type"），改为先命名 allocator 变量 `std::pmr::polymorphic_allocator<int> pa(&res);` 再 `std::pmr::vector<int> v(pa);` 修复。APP-A/APP-C 累计覆盖 39/147 章。

**Batch APP7（已完成，2026-07-16）**：语言基础簇 5 章全覆盖 APP-A + APP-C（习题重写 + 用法演绎附录）

| 子任务 | 章 | 内容 |
|--------|:---:|------|
| APP7 | ch19 变量与存储期 | 习题：static 局部状态/inline 变量跨 TU / SOIF 的 Meyers 单例；演绎：跨 TU 共享配置 + SOIF 兜底 |
| APP7 | ch22 auto/decltype | 习题：auto& 遍历 / decltype(auto) 保引用 / vector<bool> 代理陷阱；演绎：auto 隐藏返回类型 + decltype(auto) 转发保真 |
| APP7 | ch23 命名空间/ADL | 习题：ADL 发现 operator<< / std::swap 惯用法 / inline namespace ABI；演绎：ADL 让 << 可发现 + swap 异常安全 |
| APP7 | ch25 union/variant | 习题：variant 安全访问 / visit+overload O(1) / valueless_by_exception；演绎：variant 替代 union+tag + monostate 默认构造 |
| APP7 | ch28 生命周期/UB | 习题：返回局部引用悬垂 / string_view 绑临时悬垂 / launder 重建；演绎：返回值而非 const& + string_view 生命周期 |

> 一致性门禁：147 章 ERROR=0 / WARN=0 = 100/100（注入后复验通过）。靶向编译校验：25 注入块 GCC 13.1 -O2 -Wall -Wextra 0 fail（ch19/22/23/25/28；其中 ch19 的 1 块命中 CROSSBLOCK_INC_RE 被跳过）。2 处真实缺陷修复：ch22 练习2 原三元 `ref?f_ref():f_val()` 把 int& 与 int 统一为右值 int 致 decltype(auto) 推导为 int 而非 int&，改为 `return (g)` vs `return g` 直接演示 decltype((x)) 保引用；ch23 演绎2 `Handle` 因用户声明拷贝构造抑制默认构造，`Handle a,b;` 报 no matching ctor，加 `Handle()=default;` 修复。APP-A/APP-C 累计覆盖 44/147 章。

**Batch APP8（已完成，2026-07-16）**：算法簇 5 章全覆盖 APP-A + APP-C（习题重写 + 用法演绎附录）

| 子任务 | 章 | 内容 |
|--------|:---:|------|
| APP8 | ch95 算法总览 | 习题：count_if+par 并行统计 / 严格弱序降序 / for_each_n+erase-remove；演绎：二分 vs 线性查找 + 并行数据竞争 |
| APP8 | ch97 查找 | 习题：lower/upper 计数 / equal_range / search 子序列；演绎：binary_search 判存在 + 二分前置已排序 |
| APP8 | ch98 堆 | 习题：make_heap+sort_heap / 动态优先队列 / 最小堆 Top-K；演绎：priority_queue 动态极值 + 堆不变量 |
| APP8 | ch99 数值 | 习题：accumulate 求和拼接 / inner_product 点积 / transform_reduce 并行平方和；演绎：reduce 并行规约 + 初值类型 |
| APP8 | ch100 ranges | 习题：ranges::sort 投影 / views 惰性管道 / ranges::find 投影；演绎：views 替代多步 copy_if + 悬垂视图 |

> 一致性门禁：147 章 ERROR=0 / WARN=0 = 100/100（注入后复验通过）。靶向编译校验：35 注入块 GCC 13.1 -O2 -Wall -Wextra 全链接 0 fail（ch95/97/98/99/100；含 `std::execution::par` 算法实测可链接运行）。关键修复：门禁初报 9 处「常见错误」反例块失败（引用未定义变量），将运行时/逻辑类反例改为自包含可编译反例程序，编译错误类（ch99 演绎1 `accumulate` 无执行策略重载）改为纯注释块，复验 0 fail。注入块均显式写全 `#include`（CI 的 `compile_all.py` 不带 PRELUDE，防止缺头文件回归）。APP-A/APP-C 累计覆盖 49/147 章。

**后续批次（规划中）**
- **APP9+**：滚动覆盖剩余章节（part09_concurrency / part10_modern / part11_lowlevel / part12_network / part13_dsa / part14_perf 等剩余章，及 part03_language 的 ch24/26/29/30/32 需注意 preserve 模式保尾随 ASM 附录），直至 147 章习题全部主题对齐。

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
| G-L | 批 L STL 容器真实成本实证（deque/list/fwdlist/set/uset/pq/adapters/any） | 8 | 8 | 100% |
| APP1 | Phase APP 应用层增强首批（8 章习题重写+用法演绎） | 8 | 8 | 100% |
| APP2 | Phase APP 应用层增强第二批（8 章习题重写+用法演绎） | 8 | 8 | 100% |
| APP3 | Phase APP 工业深挖首批（5 章上游源码逐行+可编译范式） | 5 | 5 | 100% |
| APP4 | Phase APP 应用层增强第四批（模板核心簇 8 章习题重写+用法演绎） | 8 | 8 | 100% |
| APP5 | Phase APP 应用层增强第五批（模板/编译期簇尾章 5 章习题重写+用法演绎） | 5 | 5 | 100% |
| APP6 | Phase APP 应用层增强第六批（内存管理簇 5 章习题重写+用法演绎） | 5 | 5 | 100% |
| APP7 | Phase APP 应用层增强第七批（语言基础簇 5 章习题重写+用法演绎） | 5 | 5 | 100% |
| APP8 | Phase APP 应用层增强第八批（算法簇 5 章习题重写+用法演绎） | 5 | 5 | 100% |
| **合计** | | **116** | **116** | **100%** |

---

_本文件与 ROADMAP_v3.md 互补：ROADMAP 记录历史，WORKLIST 指导未来。_

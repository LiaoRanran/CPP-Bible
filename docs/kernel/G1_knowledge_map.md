# G1.1 知识覆盖地图（Knowledge Coverage Map）

> 本文件是**已查证事实 + 本设计决策**的混合体，凡结论均标注来源。
> 统计脚本：`_g1_map.py`（一次性，G1 验收后删除），口径 = 按 ```` ```cpp ```` 围栏计数。

## 1. 这张地图解决什么

现有 `Book/` 用 16 个 `part*` 目录组织，那是**出版顺序**（先讲历史、再讲工具链、再讲语言……），不是**知识结构**。出版顺序的问题是：同一主题被拆散在多个 part（例如"移动语义"在 part10、而它依赖的"值类别/对象生命周期"在 part03 与 part04），原子化后无法表达"哪些原子构成一条学习路径"。

所以本地图自顶向下重建一层**知识域（domain）**：它是原子的命名空间、是 ID 中段、也是优先级调度单位。`part*` 保留为**出版视图**（L4），域是**知识视图**（L1），两者是两条正交的轴。

## 2. 域骨架（16 域，ID 中段用大写缩写）

| 域 ID | 中文名 | 英文 | 判据（什么内容归此域） |
|---|---|---|---|
| `HIST` | 语言演化与版本 | history & versions | 讲"标准怎么变成这样"：版本特性、提案、时间线 |
| `TOOL` | 工具链 | toolchain | 编译器、构建系统、打包、调试、剖析、IDE、交叉编译、构建配置 |
| `LANG` | 语言基础与类型系统 | core language | 变量/引用指针/const 家族/auto/命名空间/enum/union/lambda/转型/初始化/运算符重载/friend |
| `UB` | 未定义行为与语义边界 | UB & semantic boundary | 生命周期 UB、volatile、严格别名、求值顺序、契约——**横切域**，按"是否 pending 标准判定"归类 |
| `MEM` | 对象模型与内存 | object model & memory | 布局、栈堆、new/delete、allocator、RAII、异常安全、智能指针、缓存局部性、内存池、OO 对象模型、继承/虚/CRTP/EBO、**值语义三兄弟（move / perfect forwarding / copy elision）** |
| `TMPL` | 模板与泛型 | templates & generics | 模板基础/重载/特化/变参/fold/traits/SFINAE/concepts/TMP/constexpr/tag dispatch/policy/表达式模板 |
| `STL` | 标准库 | standard library | 容器、string、span、ranges、filesystem、chrono、optional/variant、tuple/any |
| `ALGO` | 算法 | algorithms | 算法总览、排序、查找、堆、数值、范围算法 |
| `CONC` | 并发与内存模型 | concurrency | 原子、内存序、fence、无锁、ABA、hazard/RCU、协程、thread/async、stop_token |
| `MOD` | 现代特性 | modern features | modules、ranges 深水、协程应用、contracts、pmr、编译期编程 |
| `ABI` | 编译链接与生态库 | ABI & ecosystem | libstdc++/libc++/MS STL 实现、LLVM、Boost、Qt、Chromium/Abseil、fmt/spdlog、LevelDB/RocksDB、ClickHouse/Redis、Unreal |
| `PAT` | 模式与惯用法 | patterns & idioms | GoF 三组、CRTP 模式、policy 模式、DI、ECS、DOD |
| `ENG` | 工程实践 | engineering | 风格、命名与 API、错误处理、代码评审、GitFlow、CI/CD、测试、基准 |
| `PERF` | 性能与硬件 | performance | 性能模型、CPU 微架构、缓存优化、SIMD、编译器优化、Compiler Explorer、性能反模式 |
| `CASE` | 综合案例 | case studies | 线程池、内存池、日志、JSON、网络、框架 |
| `READ` | 阅读与路线 | reading roadmap | 延伸阅读路线（仅 ch165） |

**与 part 的差异（3 处关键重归类，本设计决策）**：
1. `ch115_move` / `ch116_perfect_forwarding` / `ch117_copy_elision` 从 part10(MOD) 归入 **MEM**——值语义三兄弟的知识依赖是"对象生命周期 + 值类别"，不是"现代特性"。样板 A（移动语义）据此落在 MEM 域。
2. `ch28_lifetime_ub` / `ch30_volatile` / `ch42_strict_aliasing` 从 part03/part04 抽出入 **UB** 横切域——样板 B（灰色地带）据此落在 UB 域。
3. `ch93_thread_async` / `ch94_stop_token` 在 part07(STL) 目录内，但按主题归 **CONC**。

## 3. 真实统计（脚本实测，非估算）

| 域 | 章数 | cpp 块 | 含 main | 纯注释块 | VERIFIED | UNVERIFIED |
|---|---|---|---|---|---|---|
| MEM | 20 | 1108 | 720 | 12 | 29 | 55 |
| STL | 17 | 828 | 742 | 8 | 3 | **89** |
| TMPL | 13 | 774 | 376 | 10 | 25 | 44 |
| LANG | 12 | 708 | 532 | 1 | 12 | 2 |
| ABI | 11 | 619 | 274 | 35 | 6 | 5 |
| CONC | 9 | 442 | 241 | 5 | 40 | **45** |
| PAT | 9 | 425 | 196 | 14 | 9 | 4 |
| ENG | 8 | 410 | 168 | 9 | 5 | 6 |
| TOOL | 8 | 406 | 219 | 8 | 7 | 1 |
| ALGO | 7 | 403 | 121 | 6 | 7 | 0 |
| HIST | 10 | 351 | 328 | 3 | 8 | 11 |
| PERF | 7 | 323 | 244 | 1 | 0 | **31** |
| MOD | 6 | 276 | 206 | 5 | 7 | 0 |
| CASE | 6 | 264 | 103 | 12 | 5 | 1 |
| UB | 3 | 175 | 153 | 1 | 2 | 3 |
| READ | 1 | 60 | 20 | 9 | 0 | 1 |
| **合计** | **147** | **7572** | **4643** | **139** | **165** | **298** |

**交叉验证（可信度锚）**：本脚本的 VERIFIED=165 / UNVERIFIED=298 与 `build/metrics.json:content.verification` 的 `{"verified":165,"unverified":298,"needs_verify":0}` **完全一致**，两套独立口径吻合，说明映射与统计可靠。

**口径差已定死（2026-09-10 复查，非待确认）**：本表 7572 vs `metrics.json` 7515，差 57，根因是**两套围栏识别规则不同**——
- 本工具沿用 `comment_blocks.parse`（= `compile_all.extract_blocks` = **CI 编译报告口径**）：开栏允许**缩进**（`^\s*```cpp`）。实测 10 个差异文件中缩进 cpp 开栏 51 个 + 边界连锁 6 个（ch22 独占 22，均为缩进块）。
- `metrics_snapshot` 只认**顶格**围栏（`^(`{3,})`），缩进块不进 `blocks.cpp` 真值（7515）。
- **决策：D（缺口密度）的分母 = 7572 口径**，理由：原子化要验证的正是"CI 会编译的块"，UNVERIFIED 标记也锚在这些块上；用 7515 会让 57 个真实编译块的验证缺口从分母消失。
- 移交项（非 G1）：`metrics_snapshot` 的缩进围栏盲区（57 块 ≈ 0.75%）应在后续工具修复波统一（联动 7515 真值与 README 回填，不在本轮动）。

## 4. 逐章映射（覆盖率）

**覆盖率 = 147 / 147 = 100%，未映射 0 章**（脚本输出 `未映射 0`）。完整逐章归属见下表，章名后 `[P]` 标记表示"该章在 part 目录中的位置与域不一致"（即上面 3 处重归类）。

| 域 | 章节 |
|---|---|
| HIST | ch01_c_history, ch02_standardization, ch03_cpp98_03, ch04_cpp11, ch05_cpp14, ch06_cpp17, ch07_cpp20, ch08_cpp23, ch09_cpp26, ch10_version_matrix |
| TOOL | ch11_compilers, ch12_buildsystems, ch13_packaging, ch14_debugging, ch15_profiling, ch16_ide, ch17_crosscompile, ch18_buildconfig |
| LANG | ch19_variables, ch20_reference_pointer, ch21_const_family, ch22_auto_decltype, ch23_namespace_adl, ch24_enum, ch25_union_variant, ch26_lambda, ch27_cast, ch29_friend, ch31_operator_overloading, ch32_initialization |
| UB | ch28_lifetime_ub `[P]`, ch30_volatile `[P]`, ch42_strict_aliasing `[P]` |
| MEM | ch35_memory_layout, ch36_stack_heap, ch37_new_delete, ch38_allocator, ch39_raii_rule, ch40_exception_safety, ch41_smart_pointers, ch43_cache_locality, ch44_memory_pool, ch45_oop_object_model, ch46_encapsulation_inheritance, ch47_virtual_functions, ch48_rtti, ch49_virtual_inheritance, ch50_multiple_inheritance, ch51_crtp, ch52_ebo, ch115_move `[P]`, ch116_perfect_forwarding `[P]`, ch117_copy_elision `[P]` |
| TMPL | ch60_template_basics, ch61_template_overload, ch62_specialization, ch63_variadic, ch64_fold, ch65_type_traits, ch66_sfinae, ch67_concepts, ch68_tmp, ch69_constexpr, ch70_tag_dispatch, ch71_policy, ch72_expression_templates |
| STL | ch76_stl_arch, ch77_vector, ch78_deque, ch79_list, ch80_array, ch81_string, ch82_span, ch83_map, ch84_set, ch85_unordered, ch86_adapters, ch87_bitset, ch88_optional_variant, ch89_tuple_any, ch90_ranges, ch91_filesystem, ch92_chrono |
| ALGO | ch95_algo_overview, ch96_sorting, ch97_search, ch98_heap, ch99_numeric, ch100_ranges_algo, ch101_algo_theory |
| CONC | ch107_atomic, ch108_memory_order, ch109_fence, ch110_lockfree, ch111_aba, ch112_hazard_rcu, ch113_coroutine, ch93_thread_async `[P]`, ch94_stop_token `[P]` |
| MOD | ch118_modules, ch119_ranges_deep, ch120_coroutine_app, ch121_contracts, ch122_pmr, ch123_ct_programming |
| ABI | ch124_libstdcxx, ch125_libcxx, ch126_msstl, ch127_llvm, ch128_boost, ch129_qt, ch130_chromium_abseil, ch131_fmt_spdlog, ch132_leveldb_rocksdb, ch133_clickhouse_redis, ch134_unreal |
| PAT | ch135_patterns_intro, ch136_creational, ch137_structural, ch138_behavioral, ch139_crtp_pattern, ch140_policy_pattern, ch141_di, ch142_ecs, ch143_dod |
| ENG | ch144_style, ch145_naming_api, ch146_error_handling, ch147_code_review, ch148_gitflow, ch149_ci_cd, ch150_testing, ch151_benchmark |
| PERF | ch152_perf_model, ch153_cpu_micro, ch154_cache_opt, ch155_simd, ch156_compiler_opt, ch157_compiler_explorer, ch158_perf_antipatterns |
| CASE | ch159_threadpool, ch160_mempool, ch161_logger, ch162_json, ch163_net, ch164_framework |
| READ | ch165_roadmap |

> 编号洞（ch33/34、ch53-59、ch73-75、ch105/106、ch114 等缺失）是历史合并/删除的结果，按"禁增章"铁律保留不动，映射时跳过。

## 5. 原子化优先级（可算规则，非拍脑袋）

按用户 DRQ-4 定调"最薄弱优先"，我用两个**可算**信号定级：

- **验证缺口密度** `D = UNVERIFIED / cpp块`
- **体量占比** `S = 域 cpp 块 / 7572`

规则（阈值锚定，非拍脑袋）：
- 全书平均缺口密度 D̄ = 298/7572 = **3.94%**。
- **P0** = G4 样板依赖域（MEM / UB / HIST）∪ `D ≥ 2×D̄ ≈ 8%`（语义：缺口密度显著高于全书平均一倍的域）。
  验证稳健性：STL 10.7% / CONC 10.2% / PERF 9.6% 全部 >8% 入 P0，TMPL 5.7% <8% 不入——定级与初版 9% 阈值完全一致，结论对阈值不敏感。
- **P1** = `S ≥ 9%`（体量大，影响面广）且不在 P0
- **P2** = 其余核心域
- **P3** = 派生/综述域（CASE / READ，内容多为组装，原子化收益低）

实测定级：

| 优先级 | 域 | 判据 |
|---|---|---|
| **P0** | MEM | 样板 A（移动语义）+ 样板 C（auto_ptr→unique_ptr 演化）落此域；D=5.0% |
| **P0** | UB | 样板 B（灰色地带）落此域 |
| **P0** | STL | D = 89/828 = **10.7%**（全书最薄弱） |
| **P0** | CONC | D = 45/442 = **10.2%** |
| **P0** | PERF | D = 31/323 = **9.6%**，且 VERIFIED=0（该域**零**已验证标记） |
| **P0** | HIST | 样板 C 的版本演化证据链依赖 |
| P1 | TMPL | S=10.2%，D=5.7% |
| P1 | LANG | S=9.3% |
| P2 | ABI / PAT / TOOL / ALGO / MOD / ENG | 核心但当前缺口较低 |
| P3 | CASE / READ | 组装型内容，最后做 |

**我的判断**：PERF 域 VERIFIED=0、UNVERIFIED=31，是全书唯一"零已验证"的核心域——它讲性能却没有一条被标记验证的论断，这与"未验证不入正文"的冲突最刺眼。按最薄弱优先，它该和 STL 一起进 P0，虽然 G4 样板没点它的名。这是我加的一条，不是用户原始指令。

## 6. 反例自检（什么情况算没做到）

- 若有任一 `.md` 章节未出现在上表 → 覆盖率 ≠100%，**不合格**。
- 若优先级可用"我觉得"解释而不用 `D`/`S` 算出 → 规则失效，**不合格**。
- 若某域只有域名没有"判据（什么内容归此域）"→ 无法判定新原子归属，**不合格**。
- 若 3 处重归类没写理由 → 后续执行 Agent 会按 part 目录机械归类，样板 A/B/C 会落错域，**不合格**。

# 630 A1 · 自身免疫率口径差异诊断（22 张口径级 warn 逐卡）

> 工具：`tools/autoimmune_diagnose_630.py`（纯标准库，**只读，零写入**；分类判据写死在源码里供人复核）
> 实测：**107 条 warn** 分布在 **23 张卡**上

## 一、分类统计

| 分类 | 条数 | 判据 |
|---|---|---|
| 字段缺失型 | 0 | 命题里没有该键，或值为空 |
| 字段值不符型 | 98 | 键在、结构合规，但取值不被规则接受 |
| 格式型 | 9 | 键在但结构不合规（如 object 是句子） |

| 规则 | 条数 | 要求字段 |
|---|---|---|
| `ATOM-CLAIM-CONCEPT-NORMALIZED` | 65 | object ∈ 规范概念集（概念短语，不是句子） |
| `OBSERVATION-LIVENESS` | 42 | `liveness: {kind: fixture_symbol, symbol: <夹具特有符号>}` |

- **auto 可自动补**（能从既有数据推断）：**42 条**
- **human 必须人填**：**65 条**（超过 5 条 ⇒ 触发任务书 §十.3「需人审批量处理」）

## 二、逐卡逐条诊断

| # | 卡 ID | 命题 | 规则 | 要求字段 | 当前值 | 分类 | 可自动 |
|---|---|---|---|---|---|---|---|
| 1 | `ATOM-CONC-FENCE-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 编译器屏障 compiler barrier | 格式型 | human |
| 2 | `ATOM-CONC-FENCE-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | fence 与 happens-before 内存序同步 | 格式型 | human |
| 3 | `ATOM-CONC-FENCE-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 4 | `ATOM-CONC-LOCK-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | mutex vs atomic 性能 | 字段值不符型 | human |
| 5 | `ATOM-CONC-LOCK-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | mutex vs atomic 性能 | 字段值不符型 | human |
| 6 | `ATOM-CONC-LOCK-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 7 | `ATOM-CONC-RACE-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 数据竞争 UB | 字段值不符型 | human |
| 8 | `ATOM-CONC-RACE-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 数据竞争 UB | 字段值不符型 | human |
| 9 | `ATOM-CONC-RACE-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 动态数据竞争检测局限性 | 字段值不符型 | human |
| 10 | `ATOM-CONC-RACE-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 11 | `ATOM-HIST-AUTOPTR-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | auto_ptr 历史 | 字段值不符型 | human |
| 12 | `ATOM-HIST-AUTOPTR-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | auto_ptr 历史 | 字段值不符型 | human |
| 13 | `ATOM-HIST-AUTOPTR-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | auto_ptr 历史 | 字段值不符型 | human |
| 14 | `ATOM-HIST-AUTOPTR-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 15 | `ATOM-HIST-AUTOPTR-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 16 | `ATOM-HIST-AUTOPTR-001` | `prop-4` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 17 | `ATOM-MEM-ALIGN-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 内存对齐 | 字段值不符型 | human |
| 18 | `ATOM-MEM-ALIGN-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 内存对齐 | 字段值不符型 | human |
| 19 | `ATOM-MEM-ALIGN-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 对齐与严格别名规则 | 字段值不符型 | human |
| 20 | `ATOM-MEM-ALIGN-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 21 | `ATOM-MEM-ALIGN-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 22 | `ATOM-MEM-ALLOC-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | allocator 内存策略 | 字段值不符型 | human |
| 23 | `ATOM-MEM-ALLOC-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | allocator 内存策略 | 字段值不符型 | human |
| 24 | `ATOM-MEM-ALLOC-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | allocator 内存策略 | 字段值不符型 | human |
| 25 | `ATOM-MEM-ALLOC-001` | `prop-4` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | allocator 内存策略 | 字段值不符型 | human |
| 26 | `ATOM-MEM-ALLOC-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 27 | `ATOM-MEM-ALLOC-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 28 | `ATOM-MEM-ALLOC-001` | `prop-3` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 29 | `ATOM-MEM-LEAK-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 内存泄漏检测 | 字段值不符型 | human |
| 30 | `ATOM-MEM-LEAK-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 内存泄漏检测 | 字段值不符型 | human |
| 31 | `ATOM-MEM-LEAK-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 内存泄漏检测局限性 | 字段值不符型 | human |
| 32 | `ATOM-MEM-LEAK-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 33 | `ATOM-MEM-LEAK-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 34 | `ATOM-MEM-MOVE-002` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 移动构造 | 字段值不符型 | human |
| 35 | `ATOM-MEM-MOVE-002` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 移动构造 | 字段值不符型 | human |
| 36 | `ATOM-MEM-MOVE-002` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 类型转换语义 | 字段值不符型 | human |
| 37 | `ATOM-MEM-MOVE-002` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 38 | `ATOM-MEM-MOVE-002` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 39 | `ATOM-MEM-NEW-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | new/delete 配对 | 字段值不符型 | human |
| 40 | `ATOM-MEM-NEW-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | new/delete 配对 | 字段值不符型 | human |
| 41 | `ATOM-MEM-NEW-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | new/delete 配对 | 字段值不符型 | human |
| 42 | `ATOM-MEM-NEW-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 43 | `ATOM-MEM-NEW-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 44 | `ATOM-MEM-PERF-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 小对象移动性能 | 字段值不符型 | human |
| 45 | `ATOM-MEM-PERF-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 小对象移动性能 | 字段值不符型 | human |
| 46 | `ATOM-MEM-PERF-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 47 | `ATOM-MEM-PERF-002` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | string SSO 小字符串优化 | 字段值不符型 | human |
| 48 | `ATOM-MEM-PERF-002` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | string SSO 小字符串优化 | 字段值不符型 | human |
| 49 | `ATOM-MEM-PERF-002` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 50 | `ATOM-MEM-PERF-003` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | string 实现差异 libstdc++ vs libc++ | 格式型 | human |
| 51 | `ATOM-MEM-PERF-003` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | string 实现差异 libstdc++ vs libc++ | 格式型 | human |
| 52 | `ATOM-MEM-PERF-003` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 性能结论的可移植性 | 字段值不符型 | human |
| 53 | `ATOM-MEM-PERF-003` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 54 | `ATOM-MEM-RAII-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | RAII 资源生命周期 | 字段值不符型 | human |
| 55 | `ATOM-MEM-RAII-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | C++ 对象析构顺序 | 字段值不符型 | human |
| 56 | `ATOM-MEM-RAII-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | RAII 资源生命周期 | 字段值不符型 | human |
| 57 | `ATOM-MEM-RAII-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 58 | `ATOM-MEM-RAII-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 59 | `ATOM-MEM-RAII-002` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | Rule of 0/3/5 | 字段值不符型 | human |
| 60 | `ATOM-MEM-RAII-002` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 资源所有权与特殊成员函数 | 字段值不符型 | human |
| 61 | `ATOM-MEM-RAII-002` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | noexcept move 与容器迁移 | 字段值不符型 | human |
| 62 | `ATOM-MEM-RAII-002` | `prop-4` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 规则背诵与语义理解 | 字段值不符型 | human |
| 63 | `ATOM-MEM-RAII-002` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 64 | `ATOM-MEM-RAII-002` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 65 | `ATOM-MEM-RAII-002` | `prop-3` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 66 | `ATOM-MEM-RVREF-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 右值引用 + std::move | 字段值不符型 | human |
| 67 | `ATOM-MEM-RVREF-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 右值引用 + std::move | 字段值不符型 | human |
| 68 | `ATOM-MEM-RVREF-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 右值引用 + std::move | 字段值不符型 | human |
| 69 | `ATOM-MEM-RVREF-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 70 | `ATOM-MEM-RVREF-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 71 | `ATOM-MEM-SHARED-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | shared_ptr 循环引用 | 字段值不符型 | human |
| 72 | `ATOM-MEM-SHARED-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | shared_ptr 循环引用 | 字段值不符型 | human |
| 73 | `ATOM-MEM-SHARED-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | shared_ptr 循环引用 | 字段值不符型 | human |
| 74 | `ATOM-MEM-SHARED-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 75 | `ATOM-MEM-SHARED-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 76 | `ATOM-MEM-SHARED-002` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | shared_ptr 对象布局与引用计数 | 字段值不符型 | human |
| 77 | `ATOM-MEM-SHARED-002` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | shared_ptr 引用计数同步 | 字段值不符型 | human |
| 78 | `ATOM-MEM-SHARED-002` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | shared_ptr 并发语义 | 字段值不符型 | human |
| 79 | `ATOM-MEM-SHARED-002` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 80 | `ATOM-MEM-SHARED-002` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 81 | `ATOM-MEM-UNIQUE-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | unique_ptr 对象表示与大小 | 字段值不符型 | human |
| 82 | `ATOM-MEM-UNIQUE-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | unique_ptr 移动语义 | 字段值不符型 | human |
| 83 | `ATOM-MEM-UNIQUE-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | unique_ptr 所有权模型与开销 | 字段值不符型 | human |
| 84 | `ATOM-MEM-UNIQUE-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 85 | `ATOM-MEM-UNIQUE-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 86 | `ATOM-MEM-UNIQUE-002` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | unique_ptr 删除器 | 字段值不符型 | human |
| 87 | `ATOM-MEM-UNIQUE-002` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | unique_ptr 删除器 | 字段值不符型 | human |
| 88 | `ATOM-MEM-UNIQUE-002` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | unique_ptr 布局的实现依赖 | 字段值不符型 | human |
| 89 | `ATOM-MEM-UNIQUE-002` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 90 | `ATOM-MEM-UNIQUE-002` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 91 | `ATOM-MEM-VALUE-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 值类别 lvalue/xvalue/prvalue | 格式型 | human |
| 92 | `ATOM-MEM-VALUE-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 移动后的对象状态 | 字段值不符型 | human |
| 93 | `ATOM-MEM-VALUE-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 值类别 lvalue/xvalue/prvalue | 格式型 | human |
| 94 | `ATOM-MEM-VALUE-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 95 | `ATOM-MEM-VALUE-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 96 | `ATOM-MEM-VALUE-002` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 引用折叠 + perfect forwarding | 格式型 | human |
| 97 | `ATOM-MEM-VALUE-002` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 引用折叠 + perfect forwarding | 格式型 | human |
| 98 | `ATOM-MEM-VALUE-002` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 引用折叠 + perfect forwarding | 格式型 | human |
| 99 | `ATOM-MEM-VALUE-002` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 100 | `ATOM-MEM-VALUE-002` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 101 | `ATOM-MEM-WEAK-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | weak_ptr | 字段值不符型 | human |
| 102 | `ATOM-MEM-WEAK-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | weak_ptr | 字段值不符型 | human |
| 103 | `ATOM-MEM-WEAK-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | weak_ptr | 字段值不符型 | human |
| 104 | `ATOM-MEM-WEAK-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 105 | `ATOM-MEM-WEAK-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |
| 106 | `ATOM-UB-GRAY-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 未定义行为与求值顺序 | 字段值不符型 | human |
| 107 | `ATOM-UB-GRAY-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | {'kind': 'fixture_symbol', 'symb | 字段值不符型 | auto |

## 三、修复建议（三选一，本批不执行）

1. **补字段**：`OBSERVATION-LIVENESS` 的 `liveness` 在**能定位到夹具特有符号**时可自动推断（取本命题引用卡 `artifact_assert` 里的非通用符号）；其余字段需人填（尤其 `signed_by`，机器永不代签，§零.3）。
2. **改规则**：三条规则都是 526/530 为**新卡**设计的命题级放权闸；若对老卡豁免（按 `created_at`/`meta_version` 分流），blast radius 覆盖**全库 27 张原子卡 + 未来所有卡**，且会让「命题级放权」在存量上失效 ⇒ 风险高，见 A2 方案乙。
3. **豁免**：把 22 张卡登记进既有豁免治理（有哈希链、可审计），代价是**债被固化**。

## 四、关键诚实

- **这不是「gate 误杀」的直接证据**：三条规则都要求「命题级」字段，而老卡的命题只挂证据卡 id（卡级活性条件）⇒ 属**规则口径与存量形态的错配**；
- 分类（缺失/值不符/格式）是**人工判据的机器实现**，边界情形（如「短语 vs 短句」）存在解释空间，逐条表格已列出当前值供人复核；
- 本工具**不修改任何卡**（自检断言 `git diff --quiet -- atoms` 为空）。

# 631 B2 · human 90 条字段清单（**只出清单，不代填**）

> §零.3：不代签人审、机器不做语义判断。本清单给出**候选值供人确认**，一个字段都不代填。

## 一、总览

| 优先级 | 条数 |
|---|---|
| 高 | 4 |
| 中 | 61 |
| 低 | 0 |
| **合计** | **65** |

| 字段 | 条数 |
|---|---|
| `object` | 65 |

> `signed_by` 全部为**高**：机器永不代签（§零.3），且填错会把 warn 升格为 block。

## 二、逐条清单（按优先级）

| # | 优先级 | 卡 | 命题 | 字段 | 当前值 | 建议候选 | 为什么不能 auto |
|---|---|---|---|---|---|---|---|
| 1 | **高** | `ATOM-CONC-FENCE-001` | prop-1 | `object` | 编译器屏障 compiler barrier | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 2 | **高** | `ATOM-MEM-MOVE-002` | prop-3 | `object` | 类型转换语义 | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 3 | **高** | `ATOM-MEM-PERF-003` | prop-3 | `object` | 性能结论的可移植性 | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 4 | **高** | `ATOM-MEM-RAII-002` | prop-4 | `object` | 规则背诵与语义理解 | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 5 | **中** | `ATOM-CONC-FENCE-001` | prop-2 | `object` | fence 与 happens-before 内存序同步 | happens-before | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 6 | **中** | `ATOM-CONC-LOCK-001` | prop-1 | `object` | mutex vs atomic 性能 | std::move 的性能收益 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 7 | **中** | `ATOM-CONC-LOCK-001` | prop-2 | `object` | mutex vs atomic 性能 | std::move 的性能收益 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 8 | **中** | `ATOM-CONC-RACE-001` | prop-1 | `object` | 数据竞争 UB | 数据竞争 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 9 | **中** | `ATOM-CONC-RACE-001` | prop-2 | `object` | 数据竞争 UB | 数据竞争 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 10 | **中** | `ATOM-CONC-RACE-001` | prop-3 | `object` | 动态数据竞争检测局限性 | 数据竞争 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 11 | **中** | `ATOM-HIST-AUTOPTR-001` | prop-1 | `object` | auto_ptr 历史 | auto_ptr 的历史定位 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 12 | **中** | `ATOM-HIST-AUTOPTR-001` | prop-2 | `object` | auto_ptr 历史 | auto_ptr 的历史定位 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 13 | **中** | `ATOM-HIST-AUTOPTR-001` | prop-3 | `object` | auto_ptr 历史 | auto_ptr 的历史定位 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 14 | **中** | `ATOM-MEM-ALIGN-001` | prop-1 | `object` | 内存对齐 | 内存序 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 15 | **中** | `ATOM-MEM-ALIGN-001` | prop-2 | `object` | 内存对齐 | 内存序 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 16 | **中** | `ATOM-MEM-ALIGN-001` | prop-3 | `object` | 对齐与严格别名规则 | 未测序修改与严格别名 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 17 | **中** | `ATOM-MEM-ALLOC-001` | prop-1 | `object` | allocator 内存策略 | allocator | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 18 | **中** | `ATOM-MEM-ALLOC-001` | prop-2 | `object` | allocator 内存策略 | allocator | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 19 | **中** | `ATOM-MEM-ALLOC-001` | prop-3 | `object` | allocator 内存策略 | allocator | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 20 | **中** | `ATOM-MEM-ALLOC-001` | prop-4 | `object` | allocator 内存策略 | allocator | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 21 | **中** | `ATOM-MEM-LEAK-001` | prop-1 | `object` | 内存泄漏检测 | 内存序 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 22 | **中** | `ATOM-MEM-LEAK-001` | prop-2 | `object` | 内存泄漏检测 | 内存序 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 23 | **中** | `ATOM-MEM-LEAK-001` | prop-3 | `object` | 内存泄漏检测局限性 | 内存序 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 24 | **中** | `ATOM-MEM-MOVE-002` | prop-1 | `object` | 移动构造 | 移动转移与析构次数 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 25 | **中** | `ATOM-MEM-MOVE-002` | prop-2 | `object` | 移动构造 | 移动转移与析构次数 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 26 | **中** | `ATOM-MEM-NEW-001` | prop-1 | `object` | new/delete 配对 | new / delete 表达式 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 27 | **中** | `ATOM-MEM-NEW-001` | prop-2 | `object` | new/delete 配对 | new / delete 表达式 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 28 | **中** | `ATOM-MEM-NEW-001` | prop-3 | `object` | new/delete 配对 | new / delete 表达式 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 29 | **中** | `ATOM-MEM-PERF-001` | prop-1 | `object` | 小对象移动性能 | 小对象分配策略的快慢 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 30 | **中** | `ATOM-MEM-PERF-001` | prop-2 | `object` | 小对象移动性能 | 小对象分配策略的快慢 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 31 | **中** | `ATOM-MEM-PERF-002` | prop-1 | `object` | string SSO 小字符串优化 | libstdc++ 侧的 string 布局 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 32 | **中** | `ATOM-MEM-PERF-002` | prop-2 | `object` | string SSO 小字符串优化 | libstdc++ 侧的 string 布局 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 33 | **中** | `ATOM-MEM-PERF-003` | prop-1 | `object` | string 实现差异 libstdc++ vs lib | libstdc++ 侧的 string 布局 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 34 | **中** | `ATOM-MEM-PERF-003` | prop-2 | `object` | string 实现差异 libstdc++ vs lib | libstdc++ 侧的 string 布局 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 35 | **中** | `ATOM-MEM-RAII-001` | prop-1 | `object` | RAII 资源生命周期 | RAII 的异常安全性 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 36 | **中** | `ATOM-MEM-RAII-001` | prop-2 | `object` | C++ 对象析构顺序 | 作用域内对象的析构顺序 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 37 | **中** | `ATOM-MEM-RAII-001` | prop-3 | `object` | RAII 资源生命周期 | RAII 的异常安全性 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 38 | **中** | `ATOM-MEM-RAII-002` | prop-1 | `object` | Rule of 0/3/5 | Rule of Zero 的隐式特殊成员 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 39 | **中** | `ATOM-MEM-RAII-002` | prop-2 | `object` | 资源所有权与特殊成员函数 | 特殊成员函数的取舍 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 40 | **中** | `ATOM-MEM-RAII-002` | prop-3 | `object` | noexcept move 与容器迁移 | 移动构造的 noexcept | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 41 | **中** | `ATOM-MEM-RVREF-001` | prop-1 | `object` | 右值引用 + std::move | std::move 的作用 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 42 | **中** | `ATOM-MEM-RVREF-001` | prop-2 | `object` | 右值引用 + std::move | std::move 的作用 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 43 | **中** | `ATOM-MEM-RVREF-001` | prop-3 | `object` | 右值引用 + std::move | std::move 的作用 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 44 | **中** | `ATOM-MEM-SHARED-001` | prop-1 | `object` | shared_ptr 循环引用 | shared_ptr 的引用计数与析构 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 45 | **中** | `ATOM-MEM-SHARED-001` | prop-2 | `object` | shared_ptr 循环引用 | shared_ptr 的引用计数与析构 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 46 | **中** | `ATOM-MEM-SHARED-001` | prop-3 | `object` | shared_ptr 循环引用 | shared_ptr 的引用计数与析构 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 47 | **中** | `ATOM-MEM-SHARED-002` | prop-1 | `object` | shared_ptr 对象布局与引用计数 | shared_ptr 的引用计数与析构 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 48 | **中** | `ATOM-MEM-SHARED-002` | prop-2 | `object` | shared_ptr 引用计数同步 | shared_ptr 的引用计数与析构 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 49 | **中** | `ATOM-MEM-SHARED-002` | prop-3 | `object` | shared_ptr 并发语义 | shared_ptr 的删除器 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 50 | **中** | `ATOM-MEM-UNIQUE-001` | prop-1 | `object` | unique_ptr 对象表示与大小 | unique_ptr 的大小 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 51 | **中** | `ATOM-MEM-UNIQUE-001` | prop-2 | `object` | unique_ptr 移动语义 | unique_ptr 的所有权语义 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 52 | **中** | `ATOM-MEM-UNIQUE-001` | prop-3 | `object` | unique_ptr 所有权模型与开销 | unique_ptr 的所有权语义 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 53 | **中** | `ATOM-MEM-UNIQUE-002` | prop-1 | `object` | unique_ptr 删除器 | unique_ptr 的删除器 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 54 | **中** | `ATOM-MEM-UNIQUE-002` | prop-2 | `object` | unique_ptr 删除器 | unique_ptr 的删除器 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 55 | **中** | `ATOM-MEM-UNIQUE-002` | prop-3 | `object` | unique_ptr 布局的实现依赖 | unique_ptr 的大小 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 56 | **中** | `ATOM-MEM-VALUE-001` | prop-1 | `object` | 值类别 lvalue/xvalue/prvalue | 从 xvalue 移动后的源与目标 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 57 | **中** | `ATOM-MEM-VALUE-001` | prop-2 | `object` | 移动后的对象状态 | 移动收益的有无 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 58 | **中** | `ATOM-MEM-VALUE-001` | prop-3 | `object` | 值类别 lvalue/xvalue/prvalue | 从 xvalue 移动后的源与目标 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 59 | **中** | `ATOM-MEM-VALUE-002` | prop-1 | `object` | 引用折叠 + perfect forwarding | 转发链里有无 std::forward | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 60 | **中** | `ATOM-MEM-VALUE-002` | prop-2 | `object` | 引用折叠 + perfect forwarding | 转发链里有无 std::forward | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 61 | **中** | `ATOM-MEM-VALUE-002` | prop-3 | `object` | 引用折叠 + perfect forwarding | 转发链里有无 std::forward | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 62 | **中** | `ATOM-MEM-WEAK-001` | prop-1 | `object` | weak_ptr | weak_ptr 的语义 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 63 | **中** | `ATOM-MEM-WEAK-001` | prop-2 | `object` | weak_ptr | weak_ptr 的语义 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 64 | **中** | `ATOM-MEM-WEAK-001` | prop-3 | `object` | weak_ptr | weak_ptr 的语义 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 65 | **中** | `ATOM-UB-GRAY-001` | prop-2 | `object` | 未定义行为与求值顺序 | 函数实参的求值顺序 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |

## 三、机器可读输出

- JSONL：`data/autoimmune_human_queue_631.jsonl`（65 行，每行一条，字段含 card_id/prop_id/field/suggest/priority/why_not_auto）

## 四、诚实登记

1. **建议候选来自规范集相似度**（630 A2 `suggest_object`），**不是语义正确性保证**；人可拒绝候选并选择「改 claim_type」或「补概念条目」；
2. `signed_by` 的建议值写作 `human:<在册实名>`——**不是让机器填**，而是提醒：该字段只能由**在册人**签；
3. 优先级规则是**人定**的（见本文件 `PRIORITY_RULES`），可审可改；若人认为 `object` 应先于 `signed_by`，改这张表即可重排；
4. 本工具**不写任何卡**（只读 630 方案 + 输出清单文件）。

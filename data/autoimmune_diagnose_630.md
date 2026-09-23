# 630 A1 · 自身免疫率口径差异诊断（22 张口径级 warn 逐卡）

> 工具：`tools/autoimmune_diagnose_630.py`（纯标准库，**只读，零写入**；分类判据写死在源码里供人复核）
> 实测：**132 条 warn** 分布在 **23 张卡**上

## 一、分类统计

| 分类 | 条数 | 判据 |
|---|---|---|
| 字段缺失型 | 67 | 命题里没有该键，或值为空 |
| 字段值不符型 | 2 | 键在、结构合规，但取值不被规则接受 |
| 格式型 | 63 | 键在但结构不合规（如 object 是句子） |

| 规则 | 条数 | 要求字段 |
|---|---|---|
| `ATOM-CLAIM-CONCEPT-NORMALIZED` | 65 | object ∈ 规范概念集（概念短语，不是句子） |
| `OBSERVATION-LIVENESS` | 42 | `liveness: {kind: fixture_symbol, symbol: <夹具特有符号>}` |
| `INFERENCE-NOT-MACHINE-VERIFIED` | 25 | `signed_by: human:<在册实名>`（命题级人签） |

- **auto 可自动补**（能从既有数据推断）：**42 条**
- **human 必须人填**：**90 条**（超过 5 条 ⇒ 触发任务书 §十.3「需人审批量处理」）

## 二、逐卡逐条诊断

| # | 卡 ID | 命题 | 规则 | 要求字段 | 当前值 | 分类 | 可自动 |
|---|---|---|---|---|---|---|---|
| 1 | `ATOM-CONC-FENCE-001` | `prop-2` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 2 | `ATOM-CONC-FENCE-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 阻止编译器消除该循环 | 字段值不符型 | human |
| 3 | `ATOM-CONC-FENCE-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 数据竞争原子性/不建立happens-before | 格式型 | human |
| 4 | `ATOM-CONC-FENCE-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 5 | `ATOM-CONC-LOCK-001` | `prop-2` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 6 | `ATOM-CONC-LOCK-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | single_result=200000；mutex/atomi | 格式型 | human |
| 7 | `ATOM-CONC-LOCK-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 高竞争下 CAS 的原子 RMW 代价可能超过 mutex，≤2 | 格式型 | human |
| 8 | `ATOM-CONC-LOCK-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 9 | `ATOM-CONC-RACE-001` | `prop-2` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 10 | `ATOM-CONC-RACE-001` | `prop-3` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 11 | `ATOM-CONC-RACE-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | single_total=100000、race_ops_tot | 格式型 | human |
| 12 | `ATOM-CONC-RACE-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | C++ 未定义行为（不是"结果偶尔算错"），编译器可据此做激进优 | 格式型 | human |
| 13 | `ATOM-CONC-RACE-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 安全证明（插桩盲区 / 必须全量插桩 / 时序偶发 ⇒ 存在漏报 | 格式型 | human |
| 14 | `ATOM-CONC-RACE-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 15 | `ATOM-HIST-AUTOPTR-001` | `prop-3` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 16 | `ATOM-HIST-AUTOPTR-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 转移而非拷贝（拷贝后源为空、目标值=42；从容器读元素后源为空、 | 格式型 | human |
| 17 | `ATOM-HIST-AUTOPTR-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | auto_ptr is_copy_constructible=f | 格式型 | human |
| 18 | `ATOM-HIST-AUTOPTR-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | C++98 缺少移动语义时的工程妥协（C++11 depreca | 格式型 | human |
| 19 | `ATOM-HIST-AUTOPTR-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 20 | `ATOM-HIST-AUTOPTR-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 21 | `ATOM-HIST-AUTOPTR-001` | `prop-4` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 22 | `ATOM-MEM-ALIGN-001` | `prop-3` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 23 | `ATOM-MEM-ALIGN-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | sizeof(Padded)=8（大于成员大小之和）、offse | 格式型 | human |
| 24 | `ATOM-MEM-ALIGN-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | alignof(Aligned)=16 / sizeof(Ali | 格式型 | human |
| 25 | `ATOM-MEM-ALIGN-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 未定义行为（strict aliasing 与对齐要求） | 格式型 | human |
| 26 | `ATOM-MEM-ALIGN-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 27 | `ATOM-MEM-ALIGN-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 28 | `ATOM-MEM-ALLOC-001` | `prop-4` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 29 | `ATOM-MEM-ALLOC-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | allocate 路径 allocs=1 / ctors=0；c | 格式型 | human |
| 30 | `ATOM-MEM-ALLOC-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | calls=5 / bytes=124 / heap_new=0 | 格式型 | human |
| 31 | `ATOM-MEM-ALLOC-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | upstream_allocs=0（全程不触碰上游）；deleg | 格式型 | human |
| 32 | `ATOM-MEM-ALLOC-001` | `prop-4` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 内存策略抽象（容器只经 allocator_traits 要内存 | 格式型 | human |
| 33 | `ATOM-MEM-ALLOC-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 34 | `ATOM-MEM-ALLOC-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 35 | `ATOM-MEM-ALLOC-001` | `prop-3` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 36 | `ATOM-MEM-LEAK-001` | `prop-3` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 37 | `ATOM-MEM-LEAK-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | constructed=3、destroyed after sc | 格式型 | human |
| 38 | `ATOM-MEM-LEAK-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | root use_count=3、constructed=3、d | 格式型 | human |
| 39 | `ATOM-MEM-LEAK-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 因此"没被报"不能推出"没泄漏" | 字段值不符型 | human |
| 40 | `ATOM-MEM-LEAK-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 41 | `ATOM-MEM-LEAK-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 42 | `ATOM-MEM-MOVE-002` | `prop-3` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 43 | `ATOM-MEM-MOVE-002` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 构造分配=1、拷贝分配=1、移动分配=0；证伪对照（假移动）分配 | 格式型 | human |
| 44 | `ATOM-MEM-MOVE-002` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | HeapBuf 移动分配=0 且源被掏空=是；FixedBuf  | 格式型 | human |
| 45 | `ATOM-MEM-MOVE-002` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 一次类型转换（与 static_cast 明文等价），自身不分配 | 格式型 | human |
| 46 | `ATOM-MEM-MOVE-002` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 47 | `ATOM-MEM-MOVE-002` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 48 | `ATOM-MEM-NEW-001` | `prop-3` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 49 | `ATOM-MEM-NEW-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | after new alloc=1 ctor=1；after d | 格式型 | human |
| 50 | `ATOM-MEM-NEW-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | new[] calls=1 / delete[] calls=1 | 格式型 | human |
| 51 | `ATOM-MEM-NEW-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 未定义行为（数组与非数组形式必须各自配对） | 格式型 | human |
| 52 | `ATOM-MEM-NEW-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 53 | `ATOM-MEM-NEW-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 54 | `ATOM-MEM-PERF-001` | `prop-2` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 55 | `ATOM-MEM-PERF-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | Value32 sizeof=32 时 move_eq_copy | 格式型 | human |
| 56 | `ATOM-MEM-PERF-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 掏空源对象（无可掏空资源时移动退化为拷贝，无收益） | 格式型 | human |
| 57 | `ATOM-MEM-PERF-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 58 | `ATOM-MEM-PERF-002` | `prop-2` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 59 | `ATOM-MEM-PERF-002` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | max_zero_alloc_len=15 / first_he | 格式型 | human |
| 60 | `ATOM-MEM-PERF-002` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 实现内建（标准不要求），阈值不可移植 | 格式型 | human |
| 61 | `ATOM-MEM-PERF-002` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 62 | `ATOM-MEM-PERF-003` | `prop-2` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 63 | `ATOM-MEM-PERF-003` | `prop-3` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 64 | `ATOM-MEM-PERF-003` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | sizeof_string=32、sso_capacity=15 | 格式型 | human |
| 65 | `ATOM-MEM-PERF-003` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 不可移植（同判据同驱动下 libstdc++ 32/15 与 l | 格式型 | human |
| 66 | `ATOM-MEM-PERF-003` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 「池/单调缓冲更快」不是可移植结论（可移植的是因果链与「必须实测 | 格式型 | human |
| 67 | `ATOM-MEM-PERF-003` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 68 | `ATOM-MEM-RAII-001` | `prop-3` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 69 | `ATOM-MEM-RAII-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | RAII 路径后 g_live=0；裸 new/delete 路 | 格式型 | human |
| 70 | `ATOM-MEM-RAII-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 按构造逆序（ctor A|B|C ⇒ dtor C|B|A） | 格式型 | human |
| 71 | `ATOM-MEM-RAII-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 资源生命周期绑定到对象生命周期（栈展开时作用域内对象逆序析构） | 格式型 | human |
| 72 | `ATOM-MEM-RAII-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 73 | `ATOM-MEM-RAII-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 74 | `ATOM-MEM-RAII-002` | `prop-4` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 75 | `ATOM-MEM-RAII-002` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | unique_ptr 成员拷贝被删除（copy_construc | 格式型 | human |
| 76 | `ATOM-MEM-RAII-002` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 同一缓冲被两次析构（buggy 路径 same_ptr=1 /  | 格式型 | human |
| 77 | `ATOM-MEM-RAII-002` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 标 noexcept ⇒ copies=0 moves=4；未标 | 格式型 | human |
| 78 | `ATOM-MEM-RAII-002` | `prop-4` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 而非记忆 Rule of 0/3/5 口诀 | 格式型 | human |
| 79 | `ATOM-MEM-RAII-002` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 80 | `ATOM-MEM-RAII-002` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 81 | `ATOM-MEM-RAII-002` | `prop-3` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 82 | `ATOM-MEM-RVREF-001` | `prop-3` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 83 | `ATOM-MEM-RVREF-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 直接用（as_is）copy=1 move=0；std::mov | 格式型 | human |
| 84 | `ATOM-MEM-RVREF-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | C++11/14/17 下 ret_plain copy=1 m | 格式型 | human |
| 85 | `ATOM-MEM-RVREF-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 与变量声明类型无关（命名右值引用是左值，须 std::move  | 格式型 | human |
| 86 | `ATOM-MEM-RVREF-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 87 | `ATOM-MEM-RVREF-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 88 | `ATOM-MEM-SHARED-001` | `prop-3` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 89 | `ATOM-MEM-SHARED-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | make 后 use_count=1、copy 后=2、作用域内 | 格式型 | human |
| 90 | `ATOM-MEM-SHARED-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | a use_count=2、b use_count=2、node | 格式型 | human |
| 91 | `ATOM-MEM-SHARED-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | weak_ptr 打破（shared_ptr 自身不处理环） | 格式型 | human |
| 92 | `ATOM-MEM-SHARED-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 93 | `ATOM-MEM-SHARED-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 94 | `ATOM-MEM-SHARED-002` | `prop-3` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 95 | `ATOM-MEM-SHARED-002` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | sizeof(shared_ptr)=16、copy 后 use | 格式型 | human |
| 96 | `ATOM-MEM-SHARED-002` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 带 lock 前缀的原子 RMW 指令（lock add / l | 格式型 | human |
| 97 | `ATOM-MEM-SHARED-002` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 控制块计数（被指对象与同一 shared_ptr 实例都不受保护 | 格式型 | human |
| 98 | `ATOM-MEM-SHARED-002` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 99 | `ATOM-MEM-SHARED-002` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 100 | `ATOM-MEM-UNIQUE-001` | `prop-3` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 101 | `ATOM-MEM-UNIQUE-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 裸指针（sizeof(unique_ptr<Big>)=8、si | 格式型 | human |
| 102 | `ATOM-MEM-UNIQUE-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 移动后源为空（a empty=1）、目标可用（b->v=7）、b | 格式型 | human |
| 103 | `ATOM-MEM-UNIQUE-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 运行时零开销；不可共享，需要共享才升级到 shared_ptr | 格式型 | human |
| 104 | `ATOM-MEM-UNIQUE-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 105 | `ATOM-MEM-UNIQUE-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 106 | `ATOM-MEM-UNIQUE-002` | `prop-3` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 107 | `ATOM-MEM-UNIQUE-002` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | default=8、stateless=8（EBO 吸收）、st | 格式型 | human |
| 108 | `ATOM-MEM-UNIQUE-002` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | default=16、带状态删除器仍=16（sizes equa | 格式型 | human |
| 109 | `ATOM-MEM-UNIQUE-002` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 实现边界而非语言保证（final 反例实测 16） | 格式型 | human |
| 110 | `ATOM-MEM-UNIQUE-002` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 111 | `ATOM-MEM-UNIQUE-002` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 112 | `ATOM-MEM-VALUE-001` | `prop-3` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 113 | `ATOM-MEM-VALUE-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | decltype((x))⇒lvalue（glvalue ∧ ¬ | 格式型 | human |
| 114 | `ATOM-MEM-VALUE-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 源 a.v=-1（被掏空的哨兵值）、b.v=7、c.v=7 | 格式型 | human |
| 115 | `ATOM-MEM-VALUE-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | glvalue（有身份）× rvalue（可移动）⇒ lvalu | 格式型 | human |
| 116 | `ATOM-MEM-VALUE-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 117 | `ATOM-MEM-VALUE-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 118 | `ATOM-MEM-VALUE-002` | `prop-3` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 119 | `ATOM-MEM-VALUE-002` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | T& &⇒int&、T& &&⇒int&、T&& &⇒int&、 | 格式型 | human |
| 120 | `ATOM-MEM-VALUE-002` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | forward 右值 copies=0 moves=1；forw | 格式型 | human |
| 121 | `ATOM-MEM-VALUE-002` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | T&& 传左值时推 T=int& 并折叠回左值引用；const  | 格式型 | human |
| 122 | `ATOM-MEM-VALUE-002` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 123 | `ATOM-MEM-VALUE-002` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 124 | `ATOM-MEM-WEAK-001` | `prop-3` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 125 | `ATOM-MEM-WEAK-001` | `prop-1` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 有 weak 时 use_count=1（不增计数）、expir | 格式型 | human |
| 126 | `ATOM-MEM-WEAK-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | a use_count=1、b use_count=2、node | 格式型 | human |
| 127 | `ATOM-MEM-WEAK-001` | `prop-3` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 非拥有观察者（不增加强引用计数），lock() 提升为 shar | 格式型 | human |
| 128 | `ATOM-MEM-WEAK-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 129 | `ATOM-MEM-WEAK-001` | `prop-2` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |
| 130 | `ATOM-UB-GRAY-001` | `prop-2` | `INFERENCE-NOT-MACHINE-VERIFIED` | `signed_by` | （缺失） | 字段缺失型 | human |
| 131 | `ATOM-UB-GRAY-001` | `prop-2` | `ATOM-CLAIM-CONCEPT-NORMALIZED` | `object` | 未定义行为（优化器可据此删除访问）；而实参 f(i++, i++ | 格式型 | human |
| 132 | `ATOM-UB-GRAY-001` | `prop-1` | `OBSERVATION-LIVENESS` | `liveness` | （缺失） | 字段缺失型 | auto |

## 三、修复建议（三选一，本批不执行）

1. **补字段**：`OBSERVATION-LIVENESS` 的 `liveness` 在**能定位到夹具特有符号**时可自动推断（取本命题引用卡 `artifact_assert` 里的非通用符号）；其余字段需人填（尤其 `signed_by`，机器永不代签，§零.3）。
2. **改规则**：三条规则都是 526/530 为**新卡**设计的命题级放权闸；若对老卡豁免（按 `created_at`/`meta_version` 分流），blast radius 覆盖**全库 27 张原子卡 + 未来所有卡**，且会让「命题级放权」在存量上失效 ⇒ 风险高，见 A2 方案乙。
3. **豁免**：把 22 张卡登记进既有豁免治理（有哈希链、可审计），代价是**债被固化**。

## 四、关键诚实

- **这不是「gate 误杀」的直接证据**：三条规则都要求「命题级」字段，而老卡的命题只挂证据卡 id（卡级活性条件）⇒ 属**规则口径与存量形态的错配**；
- 分类（缺失/值不符/格式）是**人工判据的机器实现**，边界情形（如「短语 vs 短句」）存在解释空间，逐条表格已列出当前值供人复核；
- 本工具**不修改任何卡**（自检断言 `git diff --quiet -- atoms` 为空）。

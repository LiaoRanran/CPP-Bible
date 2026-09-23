# 631 B2 · human 90 条字段清单（**只出清单，不代填**）

> §零.3：不代签人审、机器不做语义判断。本清单给出**候选值供人确认**，一个字段都不代填。

## 一、总览

| 优先级 | 条数 |
|---|---|
| 高 | 76 |
| 中 | 14 |
| 低 | 0 |
| **合计** | **90** |

| 字段 | 条数 |
|---|---|
| `object` | 65 |
| `signed_by` | 25 |

> `signed_by` 全部为**高**：机器永不代签（§零.3），且填错会把 warn 升格为 block。

## 二、逐条清单（按优先级）

| # | 优先级 | 卡 | 命题 | 字段 | 当前值 | 建议候选 | 为什么不能 auto |
|---|---|---|---|---|---|---|---|
| 1 | **高** | `ATOM-CONC-FENCE-001` | prop-1 | `object` | 阻止编译器消除该循环 | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 2 | **高** | `ATOM-CONC-FENCE-001` | prop-2 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 3 | **高** | `ATOM-CONC-LOCK-001` | prop-1 | `object` | single_result=200000；mutex/a | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 4 | **高** | `ATOM-CONC-LOCK-001` | prop-2 | `object` | 高竞争下 CAS 的原子 RMW 代价可能超过 mute | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 5 | **高** | `ATOM-CONC-LOCK-001` | prop-2 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 6 | **高** | `ATOM-CONC-RACE-001` | prop-1 | `object` | single_total=100000、race_ops | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 7 | **高** | `ATOM-CONC-RACE-001` | prop-2 | `object` | C++ 未定义行为（不是"结果偶尔算错"），编译器可据此 | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 8 | **高** | `ATOM-CONC-RACE-001` | prop-2 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 9 | **高** | `ATOM-CONC-RACE-001` | prop-3 | `object` | 安全证明（插桩盲区 / 必须全量插桩 / 时序偶发 ⇒  | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 10 | **高** | `ATOM-CONC-RACE-001` | prop-3 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 11 | **高** | `ATOM-HIST-AUTOPTR-001` | prop-1 | `object` | 转移而非拷贝（拷贝后源为空、目标值=42；从容器读元素后 | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 12 | **高** | `ATOM-HIST-AUTOPTR-001` | prop-2 | `object` | auto_ptr is_copy_constructib | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 13 | **高** | `ATOM-HIST-AUTOPTR-001` | prop-3 | `object` | C++98 缺少移动语义时的工程妥协（C++11 dep | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 14 | **高** | `ATOM-HIST-AUTOPTR-001` | prop-3 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 15 | **高** | `ATOM-MEM-ALIGN-001` | prop-1 | `object` | sizeof(Padded)=8（大于成员大小之和）、o | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 16 | **高** | `ATOM-MEM-ALIGN-001` | prop-2 | `object` | alignof(Aligned)=16 / sizeof | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 17 | **高** | `ATOM-MEM-ALIGN-001` | prop-3 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 18 | **高** | `ATOM-MEM-ALLOC-001` | prop-1 | `object` | allocate 路径 allocs=1 / ctors | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 19 | **高** | `ATOM-MEM-ALLOC-001` | prop-2 | `object` | calls=5 / bytes=124 / heap_n | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 20 | **高** | `ATOM-MEM-ALLOC-001` | prop-3 | `object` | upstream_allocs=0（全程不触碰上游）；d | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 21 | **高** | `ATOM-MEM-ALLOC-001` | prop-4 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 22 | **高** | `ATOM-MEM-LEAK-001` | prop-1 | `object` | constructed=3、destroyed afte | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 23 | **高** | `ATOM-MEM-LEAK-001` | prop-2 | `object` | root use_count=3、constructed | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 24 | **高** | `ATOM-MEM-LEAK-001` | prop-3 | `object` | 因此"没被报"不能推出"没泄漏" | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 25 | **高** | `ATOM-MEM-LEAK-001` | prop-3 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 26 | **高** | `ATOM-MEM-MOVE-002` | prop-1 | `object` | 构造分配=1、拷贝分配=1、移动分配=0；证伪对照（假移 | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 27 | **高** | `ATOM-MEM-MOVE-002` | prop-2 | `object` | HeapBuf 移动分配=0 且源被掏空=是；Fixed | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 28 | **高** | `ATOM-MEM-MOVE-002` | prop-3 | `object` | 一次类型转换（与 static_cast 明文等价），自 | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 29 | **高** | `ATOM-MEM-MOVE-002` | prop-3 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 30 | **高** | `ATOM-MEM-NEW-001` | prop-3 | `object` | 未定义行为（数组与非数组形式必须各自配对） | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 31 | **高** | `ATOM-MEM-NEW-001` | prop-3 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 32 | **高** | `ATOM-MEM-PERF-001` | prop-1 | `object` | Value32 sizeof=32 时 move_eq_ | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 33 | **高** | `ATOM-MEM-PERF-001` | prop-2 | `object` | 掏空源对象（无可掏空资源时移动退化为拷贝，无收益） | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 34 | **高** | `ATOM-MEM-PERF-001` | prop-2 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 35 | **高** | `ATOM-MEM-PERF-002` | prop-1 | `object` | max_zero_alloc_len=15 / firs | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 36 | **高** | `ATOM-MEM-PERF-002` | prop-2 | `object` | 实现内建（标准不要求），阈值不可移植 | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 37 | **高** | `ATOM-MEM-PERF-002` | prop-2 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 38 | **高** | `ATOM-MEM-PERF-003` | prop-1 | `object` | sizeof_string=32、sso_capacit | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 39 | **高** | `ATOM-MEM-PERF-003` | prop-2 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 40 | **高** | `ATOM-MEM-PERF-003` | prop-3 | `object` | 「池/单调缓冲更快」不是可移植结论（可移植的是因果链与「 | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 41 | **高** | `ATOM-MEM-PERF-003` | prop-3 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 42 | **高** | `ATOM-MEM-RAII-001` | prop-2 | `object` | 按构造逆序（ctor A\|B\|C ⇒ dtor C\ | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 43 | **高** | `ATOM-MEM-RAII-001` | prop-3 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 44 | **高** | `ATOM-MEM-RAII-002` | prop-1 | `object` | unique_ptr 成员拷贝被删除（copy_cons | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 45 | **高** | `ATOM-MEM-RAII-002` | prop-2 | `object` | 同一缓冲被两次析构（buggy 路径 same_ptr= | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 46 | **高** | `ATOM-MEM-RAII-002` | prop-3 | `object` | 标 noexcept ⇒ copies=0 moves= | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 47 | **高** | `ATOM-MEM-RAII-002` | prop-4 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 48 | **高** | `ATOM-MEM-RVREF-001` | prop-1 | `object` | 直接用（as_is）copy=1 move=0；std: | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 49 | **高** | `ATOM-MEM-RVREF-001` | prop-2 | `object` | C++11/14/17 下 ret_plain copy | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 50 | **高** | `ATOM-MEM-RVREF-001` | prop-3 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 51 | **高** | `ATOM-MEM-SHARED-001` | prop-1 | `object` | make 后 use_count=1、copy 后=2、 | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 52 | **高** | `ATOM-MEM-SHARED-001` | prop-2 | `object` | a use_count=2、b use_count=2、 | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 53 | **高** | `ATOM-MEM-SHARED-001` | prop-3 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 54 | **高** | `ATOM-MEM-SHARED-002` | prop-1 | `object` | sizeof(shared_ptr)=16、copy 后 | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 55 | **高** | `ATOM-MEM-SHARED-002` | prop-2 | `object` | 带 lock 前缀的原子 RMW 指令（lock add | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 56 | **高** | `ATOM-MEM-SHARED-002` | prop-3 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 57 | **高** | `ATOM-MEM-UNIQUE-001` | prop-1 | `object` | 裸指针（sizeof(unique_ptr<Big>)= | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 58 | **高** | `ATOM-MEM-UNIQUE-001` | prop-2 | `object` | 移动后源为空（a empty=1）、目标可用（b->v= | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 59 | **高** | `ATOM-MEM-UNIQUE-001` | prop-3 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 60 | **高** | `ATOM-MEM-UNIQUE-002` | prop-1 | `object` | default=8、stateless=8（EBO 吸收 | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 61 | **高** | `ATOM-MEM-UNIQUE-002` | prop-2 | `object` | default=16、带状态删除器仍=16（sizes  | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 62 | **高** | `ATOM-MEM-UNIQUE-002` | prop-3 | `object` | 实现边界而非语言保证（final 反例实测 16） | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 63 | **高** | `ATOM-MEM-UNIQUE-002` | prop-3 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 64 | **高** | `ATOM-MEM-VALUE-001` | prop-1 | `object` | decltype((x))⇒lvalue（glvalue | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 65 | **高** | `ATOM-MEM-VALUE-001` | prop-2 | `object` | 源 a.v=-1（被掏空的哨兵值）、b.v=7、c.v= | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 66 | **高** | `ATOM-MEM-VALUE-001` | prop-3 | `object` | glvalue（有身份）× rvalue（可移动）⇒ l | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 67 | **高** | `ATOM-MEM-VALUE-001` | prop-3 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 68 | **高** | `ATOM-MEM-VALUE-002` | prop-1 | `object` | T& &⇒int&、T& &&⇒int&、T&& &⇒i | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 69 | **高** | `ATOM-MEM-VALUE-002` | prop-2 | `object` | forward 右值 copies=0 moves=1； | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 70 | **高** | `ATOM-MEM-VALUE-002` | prop-3 | `object` | T&& 传左值时推 T=int& 并折叠回左值引用；co | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 71 | **高** | `ATOM-MEM-VALUE-002` | prop-3 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 72 | **高** | `ATOM-MEM-WEAK-001` | prop-1 | `object` | 有 weak 时 use_count=1（不增计数）、e | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 73 | **高** | `ATOM-MEM-WEAK-001` | prop-2 | `object` | a use_count=1、b use_count=2、 | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 74 | **高** | `ATOM-MEM-WEAK-001` | prop-3 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 75 | **高** | `ATOM-UB-GRAY-001` | prop-2 | `object` | 未定义行为（优化器可据此删除访问）；而实参 f(i++, | — | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 76 | **高** | `ATOM-UB-GRAY-001` | prop-2 | `signed_by` | （缺失） | — | §零.3：机器永不代签人审；且填不规范会从 warn 升 block |
| 77 | **中** | `ATOM-CONC-FENCE-001` | prop-2 | `object` | 数据竞争原子性/不建立happens-before | happens-before | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 78 | **中** | `ATOM-MEM-ALIGN-001` | prop-3 | `object` | 未定义行为（strict aliasing 与对齐要求） | alignas 与按字节搬运 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 79 | **中** | `ATOM-MEM-ALLOC-001` | prop-4 | `object` | 内存策略抽象（容器只经 allocator_traits | allocator | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 80 | **中** | `ATOM-MEM-NEW-001` | prop-1 | `object` | after new alloc=1 ctor=1；aft | new / delete 表达式 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 81 | **中** | `ATOM-MEM-NEW-001` | prop-2 | `object` | new[] calls=1 / delete[] cal | new[] / delete[] 混用 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 82 | **中** | `ATOM-MEM-PERF-003` | prop-2 | `object` | 不可移植（同判据同驱动下 libstdc++ 32/15 | libstdc++ 侧的 string 布局 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 83 | **中** | `ATOM-MEM-RAII-001` | prop-1 | `object` | RAII 路径后 g_live=0；裸 new/dele | new / delete 表达式 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 84 | **中** | `ATOM-MEM-RAII-001` | prop-3 | `object` | 资源生命周期绑定到对象生命周期（栈展开时作用域内对象逆序 | 作用域内对象的析构顺序 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 85 | **中** | `ATOM-MEM-RAII-002` | prop-4 | `object` | 而非记忆 Rule of 0/3/5 口诀 | Rule of Zero 的隐式特殊成员 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 86 | **中** | `ATOM-MEM-RVREF-001` | prop-3 | `object` | 与变量声明类型无关（命名右值引用是左值，须 std::m | std::move 的作用 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 87 | **中** | `ATOM-MEM-SHARED-001` | prop-3 | `object` | weak_ptr 打破（shared_ptr 自身不处理 | shared_ptr 的删除器 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 88 | **中** | `ATOM-MEM-SHARED-002` | prop-3 | `object` | 控制块计数（被指对象与同一 shared_ptr 实例都 | shared_ptr 的删除器 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 89 | **中** | `ATOM-MEM-UNIQUE-001` | prop-3 | `object` | 运行时零开销；不可共享，需要共享才升级到 shared_ | shared_ptr 的删除器 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |
| 90 | **中** | `ATOM-MEM-WEAK-001` | prop-3 | `object` | 非拥有观察者（不增加强引用计数），lock() 提升为  | shared_ptr 的删除器 | object 是语义判断，机器不改；给出规范集内最相似候选供人确认，若无合适候选 |

## 三、机器可读输出

- JSONL：`data/autoimmune_human_queue_631.jsonl`（90 行，每行一条，字段含 card_id/prop_id/field/suggest/priority/why_not_auto）

## 四、诚实登记

1. **建议候选来自规范集相似度**（630 A2 `suggest_object`），**不是语义正确性保证**；人可拒绝候选并选择「改 claim_type」或「补概念条目」；
2. `signed_by` 的建议值写作 `human:<在册实名>`——**不是让机器填**，而是提醒：该字段只能由**在册人**签；
3. 优先级规则是**人定**的（见本文件 `PRIORITY_RULES`），可审可改；若人认为 `object` 应先于 `signed_by`，改这张表即可重排；
4. 本工具**不写任何卡**（只读 630 方案 + 输出清单文件）。

# 611 D2 · 命题活性锚补全计划（只读 · 不补字段）

> 仅生成「补全计划」：把每条缺锚 observation 命题、它的 evidence、以及**建议**的 `fixture_symbol` 列出。是否采用、补哪个符号是**人审权力**。

## 一、总览

- 缺锚 observation 命题 **50** 条（607 实测 50，已锁定）；
- 建议符号取自该命题 `evidence` 里第一个工件引用（ATOM-/EV-/example-）；evidence 空 ⇒ 待人裁定；

## 二、补全计划明细

| 卡 | 命题 id | 状态 | 建议 fixture_symbol | 证据 | 内容（截断） |
|---|---|---|---|---|---|
| `ATOM-CONC-FENCE-001` | `prop-1` | 缺 `liveness` | `EV-CONC-001` | EV-CONC-001 EV-CONC-002 | 屏障落在循环体内（含零机器指令的 atomic_signal_fence）即阻止… |
| `ATOM-CONC-LOCK-001` | `prop-1` | 缺 `liveness` | `EV-CONC-003` | EV-CONC-003 EV-CONC-004 | 同夹具四路对照的机器读数（EV-CONC-003/004 共享 `Example… |
| `ATOM-CONC-RACE-001` | `prop-1` | 缺 `liveness` | `EV-CONC-005` | EV-CONC-005 EV-CONC-006 | 三场景（single|race|safe）在 kIters=100000 下的机… |
| `ATOM-HIST-AUTOPTR-001` | `prop-1` | 缺 `liveness` | `EV-HIST-001` | EV-HIST-001 EV-MEM-003 | 实测（GCC 15.3.0、-std=c++14 -O2）：auto_ptr 拷… |
| `ATOM-HIST-AUTOPTR-001` | `prop-2` | 缺 `liveness` | `EV-HIST-001` | EV-HIST-001 EV-MEM-003 | 编译期判定（四条 static_assert 全部通过）：auto_ptr 不满… |
| `ATOM-HIST-AUTOPTR-001` | `prop-4` | 缺 `liveness` | `EV-HIST-001` | EV-HIST-001 | 实现层事实（EV-HIST-001 的 impl_ 读数）：同一夹具在 -std… |
| `ATOM-LANG-INLINE-001` | `prop-1` | 缺 `liveness` | `EV-LANG-001` | EV-LANG-001 EV-LANG-002 | 两个 TU 给出不同定义的 inline 函数，其可观测行为由链接顺序与优化档共… |
| `ATOM-LANG-INLINE-001` | `prop-2` | 缺 `liveness` | `EV-LANG-001` | EV-LANG-001 EV-LANG-002 | 当各 TU 的定义由相同 token 序列构成时行为稳定：stable 组在 a… |
| `ATOM-MEM-ALIGN-001` | `prop-1` | 缺 `liveness` | `EV-MEM-019` | EV-MEM-019 | 编译器在成员间与末尾插入 padding 使每个成员与整体满足对齐：实测 siz… |
| `ATOM-MEM-ALIGN-001` | `prop-2` | 缺 `liveness` | `EV-MEM-020` | EV-MEM-020 | 对齐可控且按字节搬运保真：实测 alignof(Aligned)=16、size… |
| `ATOM-MEM-ALLOC-001` | `prop-1` | 缺 `liveness` | `EV-MEM-026` | EV-MEM-026 | 分配与对象构造是两个独立动作：实测 allocate 路径 allocs=1 而… |
| `ATOM-MEM-ALLOC-001` | `prop-2` | 缺 `liveness` | `EV-MEM-027` | EV-MEM-027 | 策略可整体替换：自定义 arena 分配器接入 vector 后，16 次 pu… |
| `ATOM-MEM-ALLOC-001` | `prop-3` | 缺 `liveness` | `EV-MEM-028` | EV-MEM-028 | std::pmr（C++17）把分配策略变成运行时多态：monotonic_bu… |
| `ATOM-MEM-ALLOC-002` | `prop-1` | 缺 `liveness` | `EV-MEM-040` | EV-MEM-040 EV-MEM-041 | 同一 workload（1000 次 24B 分配、-O2）下三种小对象策略的元… |
| `ATOM-MEM-ALLOC-002` | `prop-2` | 缺 `liveness` | `EV-MEM-040` | EV-MEM-040 EV-MEM-041 | bitmap 的 bookkeeping 是 1 bit/块、pool 是 8B… |
| `ATOM-MEM-LEAK-001` | `prop-1` | 缺 `liveness` | `EV-MEM-036` | EV-MEM-036 | 父用 weak_ptr 上行的无环树：实测 root children=2、pa… |
| `ATOM-MEM-LEAK-001` | `prop-2` | 缺 `liveness` | `EV-MEM-037` | EV-MEM-037 | 仅把上行改为 shared_ptr（与 EV-MEM-036 构成唯一变量对照）… |
| `ATOM-MEM-LEAK-002` | `prop-1` | 缺 `liveness` | `EV-MEM-042` | EV-MEM-042 EV-MEM-043 | 循环引用夹具上的零依赖观测（构造/析构计数、存活对象数）读出：cycle_all… |
| `ATOM-MEM-LEAK-002` | `prop-2` | 缺 `liveness` | `EV-MEM-042` | EV-MEM-042 EV-MEM-043 | 同一循环引用夹具、同一编译器与档位（-O1 -g -fsanitize=addr… |
| `ATOM-MEM-MOVE-002` | `prop-1` | 缺 `liveness` | `EV-MEM-001` | EV-MEM-001 | 移动不分配：六组组合（GCC 15.3/13.1/8.1 × -O0/-O2）读… |
| `ATOM-MEM-MOVE-002` | `prop-2` | 缺 `liveness` | `EV-MEM-002` | EV-MEM-002 | 收益来自掏空源：持堆的 HeapBuf 拷贝分配=1、移动分配=0、移动后源被掏… |
| `ATOM-MEM-NEW-001` | `prop-1` | 缺 `liveness` | `EV-MEM-017` | EV-MEM-017 | new 表达式先分配再构造、delete 表达式先析构再释放，两层各自独立发生一… |
| `ATOM-MEM-NEW-001` | `prop-2` | 缺 `liveness` | `EV-MEM-018` | EV-MEM-018 | 数组与 nothrow 的实测：array new[] calls=1、arra… |
| `ATOM-MEM-PERF-001` | `prop-1` | 缺 `liveness` | `EV-MEM-008` | EV-MEM-008 | 实测（-O0/-O2 一致）：无动态资源的 Value32（sizeof=32）… |
| `ATOM-MEM-PERF-002` | `prop-1` | 缺 `liveness` | `EV-MEM-029` | EV-MEM-029 | 本机 libstdc++（GCC 15.3.0）上 SSO 阈值为 15 字符：… |
| `ATOM-MEM-PERF-003` | `prop-1` | 缺 `liveness` | `EV-MEM-038` | EV-MEM-038 | libstdc++ 侧实测（cxx23 -O2 与 cxx17 -O0 一致）：… |
| `ATOM-MEM-PERF-004` | `prop-1` | 缺 `liveness` | `EV-MEM-044` | EV-MEM-044 EV-MEM-045 | 相邻布局两计数器落在同一缓存行（tight_offset_bytes=8、tig… |
| `ATOM-MEM-PERF-004` | `prop-2` | 缺 `liveness` | `EV-MEM-044` | EV-MEM-044 EV-MEM-045 | 4 线程各累加 1e7 次、7 轮下共享缓存行明显更慢：sharing_is_s… |
| `ATOM-MEM-RAII-001` | `prop-1` | 缺 `liveness` | `EV-MEM-009` | EV-MEM-009 | 同夹具两条路径的对照读数：RAII 路径（safe_path）结束后 g_liv… |
| `ATOM-MEM-RAII-001` | `prop-2` | 缺 `liveness` | `EV-MEM-010` | EV-MEM-010 | 多个 RAII 对象在同一作用域时，析构按构造的逆序自动发生：实测输出为 cto… |
| `ATOM-MEM-RAII-002` | `prop-1` | 缺 `liveness` | `EV-MEM-023` | EV-MEM-023 | 成员全是 RAII 类型（unique_ptr/vector/string）时一… |
| `ATOM-MEM-RAII-002` | `prop-2` | 缺 `liveness` | `EV-MEM-024` | EV-MEM-024 | 管理裸资源时只写析构会得到隐式浅拷贝：实测 buggy 路径 allocs=1、… |
| `ATOM-MEM-RAII-002` | `prop-3` | 缺 `liveness` | `EV-MEM-025` | EV-MEM-025 | vector 扩容搬迁走移动还是退化拷贝取决于移动构造是否标 noexcept：… |
| `ATOM-MEM-RVREF-001` | `prop-1` | 缺 `liveness` | `EV-MEM-004` | EV-MEM-004 | 形参声明为 T&& 时，形参名在函数体内表现为左值：十一档组合读数一致——原样使… |
| `ATOM-MEM-RVREF-001` | `prop-2` | 缺 `liveness` | `EV-MEM-005` | EV-MEM-005 | 例外路径（return x;）随版本变化：cxx11、cxx14、cxx17 下… |
| `ATOM-MEM-SHARED-001` | `prop-1` | 缺 `liveness` | `EV-MEM-013` | EV-MEM-013 | 共享所有权的计数与释放：make 后 use_count=1、拷贝后=2、作用域… |
| `ATOM-MEM-SHARED-001` | `prop-2` | 缺 `liveness` | `EV-MEM-014` | EV-MEM-014 | 两个对象互相用 shared_ptr 持有时：a 与 b 的 use_count… |
| `ATOM-MEM-SHARED-002` | `prop-1` | 缺 `liveness` | `EV-MEM-034` | EV-MEM-034 | 四线程各持副本并发拷贝：-O0/-O2 一致——sizeof(shared_pt… |
| `ATOM-MEM-SHARED-002` | `prop-2` | 缺 `liveness` | `EV-MEM-034` | EV-MEM-034 | 控制块计数用原子 RMW 修改：工件断言在 `_Sp_counted_base:… |
| `ATOM-MEM-UNIQUE-001` | `prop-1` | 缺 `liveness` | `EV-MEM-011` | EV-MEM-011 | 零开销的第一个证据：实测 sizeof(unique_ptr<Big>)=8、s… |
| `ATOM-MEM-UNIQUE-001` | `prop-2` | 缺 `liveness` | `EV-MEM-012` | EV-MEM-012 | 所有权转移与释放：移动后源被置空（a empty=1）、目标持有对象（b->v=… |
| `ATOM-MEM-UNIQUE-002` | `prop-1` | 缺 `liveness` | `EV-MEM-032` | EV-MEM-032 | 删除器是 unique_ptr 类型的一部分，对象大小随之变化（-O0/-O2 … |
| `ATOM-MEM-UNIQUE-002` | `prop-2` | 缺 `liveness` | `EV-MEM-033` | EV-MEM-033 | 删除器经类型擦除由控制块持有，与类型无关：sizeof(shared_ptr) … |
| `ATOM-MEM-VALUE-001` | `prop-1` | 缺 `liveness` | `EV-MEM-006` | EV-MEM-006 | 三类值类别的机器判定：decltype((x)) 得 lvalue（有身份、不可… |
| `ATOM-MEM-VALUE-001` | `prop-2` | 缺 `liveness` | `EV-MEM-007` | EV-MEM-007 | 从 xvalue 移动（std::move(a)）后：源对象被标记为已掏空（a.… |
| `ATOM-MEM-VALUE-002` | `prop-1` | 缺 `liveness` | `EV-MEM-021` | EV-MEM-021 | 四条折叠规则的实测：T& &⇒int&、T& &&⇒int&、T&& &⇒int… |
| `ATOM-MEM-VALUE-002` | `prop-2` | 缺 `liveness` | `EV-MEM-022` | EV-MEM-022 | 转发链对照：forward 右值实参时 copies=0、moves=1；for… |
| `ATOM-MEM-WEAK-001` | `prop-1` | 缺 `liveness` | `EV-MEM-015` | EV-MEM-015 | 非拥有观察者的实测：持有 weak 时 use_count 仍为 1（不增加强引… |
| `ATOM-MEM-WEAK-001` | `prop-2` | 缺 `liveness` | `EV-MEM-016` | EV-MEM-016 | 把反向引用改为 weak 后：a use_count=1、b use_count… |
| `ATOM-UB-GRAY-001` | `prop-1` | 缺 `liveness` | `EV-UB-001` | EV-UB-001 | f(g(), h()) 的实参求值顺序实测：四组组合（GCC 15.3.0 与 … |

## 三、口径与边界

- 复用 607 `proposition_liveness_audit.audit` 的判定（同源、不重实现）；
- `needs_review`（external_basis）不进本计划（那类由人决定改标 inference 或补夹具锚）；
- 绝不写命题卡、绝不自动补 `liveness`；本文件只是人审工作台。

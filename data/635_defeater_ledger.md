# 635 1.5 · 种子击败器台账 + taint 标记

- verified 卡：**23**；覆盖率：**100.0%**（每卡 ≥1 击败器）
- 类型分布：{'rebutting': 0, 'undercutting': 23}
- `taint_propagation=true`（引用于 ≥3 条下游卡）：**8** 张

## 一、击败器清单

| 卡 | 类型 | taint | 引用数 | 击败器内容 |
|---|---|---|---|---|
| `ATOM-CONC-FENCE-001` | undercutting | false | 2 | 若「屏障落在循环体内（含零机器指令的 atomic_signal_fence）即阻止编译器删除该循环；移到体外则与无屏障同形、整段被消除。」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-CONC-LOCK-001` | undercutting | false | 0 | 若「同夹具四路对照的机器读数（EV-CONC-003/004 共享 `Examples/atoms/_atom_lock_cost.out`）：nproc=32、s」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-CONC-RACE-001` | undercutting | false | 0 | 若「三场景（single|race|safe）在 kIters=100000 下的机器读数：single_total=100000、race_ops_total=2」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-HIST-AUTOPTR-001` | undercutting | false | 0 | 若「实测（GCC 15.3.0、-std=c++14 -O2）：auto_ptr 拷贝后源为空=是、目标值=42；从容器读元素后源为空=是、偷到值=7；unique」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-MEM-ALIGN-001` | undercutting | false | 0 | 若「编译器在成员间与末尾插入 padding 使每个成员与整体满足对齐：实测 sizeof(Padded)=8、offsetof a=0、offsetof b=4，」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-MEM-ALLOC-001` | undercutting | true | 3 | 若「分配与对象构造是两个独立动作：实测 allocate 路径 allocs=1 而 ctors=0（只分配不构造），separate construct 路径 c」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-MEM-LEAK-001` | undercutting | false | 1 | 若「父用 weak_ptr 上行的无环树：实测 root children=2、parent reachable=1、constructed=3、destroyed」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-MEM-MOVE-002` | undercutting | true | 6 | 若「移动不分配：六组组合（GCC 15.3/13.1/8.1 × -O0/-O2）读数一致——构造分配=1、拷贝分配=1、移动分配=0，证伪对照（假移动）分配=1；」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-MEM-NEW-001` | undercutting | true | 3 | 若「new 表达式先分配再构造、delete 表达式先析构再释放，两层各自独立发生一次：实测 after new 时 alloc=1、ctor=1，after de」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-MEM-PERF-001` | undercutting | true | 4 | 若「实测（-O0/-O2 一致）：无动态资源的 Value32（sizeof=32）移动与拷贝搬运字节数相同且源保持完好（value move source int」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-MEM-PERF-002` | undercutting | false | 2 | 若「本机 libstdc++（GCC 15.3.0）上 SSO 阈值为 15 字符：实测 len=0/14/15 时 allocs=0，len=16 起 alloc」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-MEM-PERF-003` | undercutting | false | 2 | 若「libstdc++ 侧实测（cxx23 -O2 与 cxx17 -O0 一致）：sizeof_string=32、sizeof_size_t=8、capacit」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-MEM-RAII-001` | undercutting | true | 4 | 若「同夹具两条路径的对照读数：RAII 路径（safe_path）结束后 g_live=0（无存活资源），裸 new/delete 路径（leak_path）异常跳」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-MEM-RAII-002` | undercutting | false | 0 | 若「成员全是 RAII 类型（unique_ptr/vector/string）时一个特殊成员都不写也正确：实测 move_constructible=1、copy」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-MEM-RVREF-001` | undercutting | false | 1 | 若「形参声明为 T&& 时，形参名在函数体内表现为左值：十一档组合读数一致——原样使用（as_is）copy=1、move=0；std::move(x) 后 cop」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-MEM-SHARED-001` | undercutting | true | 6 | 若「共享所有权的计数与释放：make 后 use_count=1、拷贝后=2、作用域内=3、离开作用域后=2，且 box destroyed count=1（计数归」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-MEM-SHARED-002` | undercutting | false | 1 | 若「四线程各持副本并发拷贝：-O0/-O2 一致——sizeof(shared_ptr)=16、shared_ptr copyable=1 而 unique_ptr」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-MEM-UNIQUE-001` | undercutting | true | 3 | 若「零开销的第一个证据：实测 sizeof(unique_ptr<Big>)=8、sizeof(Big*)=8、equal=1（两者相等，没有额外字段）。」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-MEM-UNIQUE-002` | undercutting | false | 1 | 若「删除器是 unique_ptr 类型的一部分，对象大小随之变化（-O0/-O2 一致）：default=8、stateless=8（空且非 final 被空基类」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-MEM-VALUE-001` | undercutting | false | 2 | 若「三类值类别的机器判定：decltype((x)) 得 lvalue（有身份、不可移动）、decltype(std::move(x)) 得 xvalue（有身份、」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-MEM-VALUE-002` | undercutting | false | 0 | 若「四条折叠规则的实测：T& &⇒int&、T& &&⇒int&、T&& &⇒int&、T&& &&⇒int&&（唯一保持右值引用的是"右值引用的右值引用"）；au」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-MEM-WEAK-001` | undercutting | true | 5 | 若「非拥有观察者的实测：持有 weak 时 use_count 仍为 1（不增加强引用）、expired before=0；.lock() 后 use_count=」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |
| `ATOM-UB-GRAY-001` | undercutting | false | 2 | 若「f(g(), h()) 的实参求值顺序实测：四组组合（GCC 15.3.0 与 GCC 13.1.0、-O0 与 -O2、c++17）输出均为 h 先于 g、最」所依赖的实验/产物在新编译器或平台上得到相反观测（或该证据的 artifact_sha256 失效），则本卡的**理由被削弱**。 |

## 二、taint=true 高风险卡清单

- `ATOM-MEM-ALLOC-001`
- `ATOM-MEM-MOVE-002`
- `ATOM-MEM-NEW-001`
- `ATOM-MEM-PERF-001`
- `ATOM-MEM-RAII-001`
- `ATOM-MEM-SHARED-001`
- `ATOM-MEM-UNIQUE-001`
- `ATOM-MEM-WEAK-001`

## 诚实登记

1. 击败器内容为**模板 + 卡内 prop 摘要**生成（非人工逐条撰写），真实可用但需人审润色；
2. `taint_propagation` 按**跨卡引用计数 ≥3** 判定（启发式）；
3. 本工具**只读**，不改任何卡与判决。

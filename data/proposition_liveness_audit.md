# 命题活性锚审计（607 任务 2 · 只读）

> 生成时间：2026-09-19T21:41:13 ｜ 扫描面：`atoms` ｜ 命令：`python tools/proposition_liveness_audit.py --check`
>
> **本报告是人审清单，不是自动判决**：工具只按 gate `OBSERVATION-LIVENESS` 的判据（observation 命题须有 `liveness.kind=fixture_symbol` 且 `symbol` 非空）列清单，**不自动补字段**、**不改任何卡**、不做语义判断。

## 1 · 总览

| 指标 | 数量 |
|---|---|
| 命题总数 | **79** |
| └ observation | **50** |
| └ inference | **29** |
| └ 其它/未知 `claim_type` | 0 |
| 含 `liveness` 字段的命题 | **0** |
| 不含 `liveness` 的命题 | 79 |

**observation 命题的状态分布**（`ok` 之外都是待办/待审）：

| 状态 | 数量 | 含义 |
|---|---|---|
| `ok` | **0** | `kind: fixture_symbol` 且 `symbol` 非空（gate 不报 warn） |
| `missing` | **50** | 无 `liveness` ⇒ gate 报 warn |
| `missing_symbol` | 0 | `kind: fixture_symbol` 但 `symbol` 空 ⇒ gate 同样报 warn |
| `unknown_kind` | 0 | `kind` 不在 `fixture_symbol` / `external_basis` 内 ⇒ 人审该填什么 |
| `needs_review` | **0** | `kind: external_basis` 的 observation（见 §3） |

## 2 · 已有 `liveness` 的命题（按 kind 分组）

**0 条**：全库没有任何命题填过 `liveness`（因此下面的清单 = 全部 observation）。

## 3 · `needs_review` 清单（`kind: external_basis` 的 observation，共 0 条）

含义：该命题的活性来自**外部标准/权威源**背书，而非**单一工件** ⇒ replay 无法证伪它，任务书要求单列，供人审决定「改标 inference」或「补夹具级锚」。

（空）

## 4 · 缺 liveness 清单（按卡分组，共 50 条 / 27 卡）

> 字段说明：本仓命题卡**没有 `brief` 字段**（任务书写的 `brief` 在本仓对应 `statement`），故此处取 `statement` 前 60 字；JSON 输出里有全文。

### `ATOM-CONC-FENCE-001`（1 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-CONC-001, EV-CONC-002 | 屏障落在循环体内（含零机器指令的 atomic_signal_fence）即阻止编译器删除该循环；移到体外则与无屏障同形… |

### `ATOM-CONC-LOCK-001`（1 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-CONC-003, EV-CONC-004 | 同夹具四路对照的机器读数（EV-CONC-003/004 共享 `Examples/atoms/_atom_lock_c… |

### `ATOM-CONC-RACE-001`（1 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-CONC-005, EV-CONC-006 | 三场景（single|race|safe）在 kIters=100000 下的机器读数：single_total=100… |

### `ATOM-HIST-AUTOPTR-001`（3 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-HIST-001, EV-MEM-003 | 实测（GCC 15.3.0、-std=c++14 -O2）：auto_ptr 拷贝后源为空=是、目标值=42；从容器读元… |
| `prop-2` | 缺 `liveness` | EV-HIST-001, EV-MEM-003 | 编译期判定（四条 static_assert 全部通过）：auto_ptr 不满足 CopyConstructible（… |
| `prop-4` | 缺 `liveness` | EV-HIST-001 | 实现层事实（EV-HIST-001 的 impl_ 读数）：同一夹具在 -std=c++17 与 -std=c++23 … |

### `ATOM-LANG-INLINE-001`（2 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-LANG-001, EV-LANG-002 | 两个 TU 给出不同定义的 inline 函数，其可观测行为由链接顺序与优化档共同决定：-O0（未内联）链接顺序 a→b… |
| `prop-2` | 缺 `liveness` | EV-LANG-001, EV-LANG-002 | 当各 TU 的定义由相同 token 序列构成时行为稳定：stable 组在 ab/ba/o2/o2b 四种链接与优化组… |

### `ATOM-MEM-ALIGN-001`（2 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-019 | 编译器在成员间与末尾插入 padding 使每个成员与整体满足对齐：实测 sizeof(Padded)=8、offset… |
| `prop-2` | 缺 `liveness` | EV-MEM-020 | 对齐可控且按字节搬运保真：实测 alignof(Aligned)=16、sizeof(Aligned)=16，且 mem… |

### `ATOM-MEM-ALLOC-001`（3 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-026 | 分配与对象构造是两个独立动作：实测 allocate 路径 allocs=1 而 ctors=0（只分配不构造），sep… |
| `prop-2` | 缺 `liveness` | EV-MEM-027 | 策略可整体替换：自定义 arena 分配器接入 vector 后，16 次 push_back 期间 calls=5、b… |
| `prop-3` | 缺 `liveness` | EV-MEM-028 | std::pmr（C++17）把分配策略变成运行时多态：monotonic_buffer_resource 用栈缓冲伺候… |

### `ATOM-MEM-ALLOC-002`（2 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-040, EV-MEM-041 | 同一 workload（1000 次 24B 分配、-O2）下三种小对象策略的元数据可用统一口径（struct_byte… |
| `prop-2` | 缺 `liveness` | EV-MEM-040, EV-MEM-041 | bitmap 的 bookkeeping 是 1 bit/块、pool 是 8B/块指针，故元数据随块数线性增长：块数由… |

### `ATOM-MEM-LEAK-001`（2 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-036 | 父用 weak_ptr 上行的无环树：实测 root children=2、parent reachable=1、con… |
| `prop-2` | 缺 `liveness` | EV-MEM-037 | 仅把上行改为 shared_ptr（与 EV-MEM-036 构成唯一变量对照）即成环：实测 root children… |

### `ATOM-MEM-LEAK-002`（2 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-042, EV-MEM-043 | 循环引用夹具上的零依赖观测（构造/析构计数、存活对象数）读出：cycle_allocated=2、cycle_destr… |
| `prop-2` | 缺 `liveness` | EV-MEM-042, EV-MEM-043 | 同一循环引用夹具、同一编译器与档位（-O1 -g -fsanitize=address,undefined）下，仅给 N… |

### `ATOM-MEM-MOVE-002`（2 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-001 | 移动不分配：六组组合（GCC 15.3/13.1/8.1 × -O0/-O2）读数一致——构造分配=1、拷贝分配=1、移… |
| `prop-2` | 缺 `liveness` | EV-MEM-002 | 收益来自掏空源：持堆的 HeapBuf 拷贝分配=1、移动分配=0、移动后源被掏空=是；无可掏空间接资源的 FixedB… |

### `ATOM-MEM-NEW-001`（2 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-017 | new 表达式先分配再构造、delete 表达式先析构再释放，两层各自独立发生一次：实测 after new 时 all… |
| `prop-2` | 缺 `liveness` | EV-MEM-018 | 数组与 nothrow 的实测：array new[] calls=1、array delete[] calls=1（必… |

### `ATOM-MEM-PERF-001`（1 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-008 | 实测（-O0/-O2 一致）：无动态资源的 Value32（sizeof=32）移动与拷贝搬运字节数相同且源保持完好（v… |

### `ATOM-MEM-PERF-002`（1 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-029 | 本机 libstdc++（GCC 15.3.0）上 SSO 阈值为 15 字符：实测 len=0/14/15 时 all… |

### `ATOM-MEM-PERF-003`（1 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-038 | libstdc++ 侧实测（cxx23 -O2 与 cxx17 -O0 一致）：sizeof_string=32、siz… |

### `ATOM-MEM-PERF-004`（2 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-044, EV-MEM-045 | 相邻布局两计数器落在同一缓存行（tight_offset_bytes=8、tight_same_line=1），alig… |
| `prop-2` | 缺 `liveness` | EV-MEM-044, EV-MEM-045 | 4 线程各累加 1e7 次、7 轮下共享缓存行明显更慢：sharing_is_slower=1 且 counters_a… |

### `ATOM-MEM-RAII-001`（2 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-009 | 同夹具两条路径的对照读数：RAII 路径（safe_path）结束后 g_live=0（无存活资源），裸 new/del… |
| `prop-2` | 缺 `liveness` | EV-MEM-010 | 多个 RAII 对象在同一作用域时，析构按构造的逆序自动发生：实测输出为 ctor A、ctor B、ctor C，随后… |

### `ATOM-MEM-RAII-002`（3 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-023 | 成员全是 RAII 类型（unique_ptr/vector/string）时一个特殊成员都不写也正确：实测 move_… |
| `prop-2` | 缺 `liveness` | EV-MEM-024 | 管理裸资源时只写析构会得到隐式浅拷贝：实测 buggy 路径 allocs=1、same_ptr=1、dtor_runs… |
| `prop-3` | 缺 `liveness` | EV-MEM-025 | vector 扩容搬迁走移动还是退化拷贝取决于移动构造是否标 noexcept：实测 noexcept move 路径 … |

### `ATOM-MEM-RVREF-001`（2 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-004 | 形参声明为 T&& 时，形参名在函数体内表现为左值：十一档组合读数一致——原样使用（as_is）copy=1、move=… |
| `prop-2` | 缺 `liveness` | EV-MEM-005 | 例外路径（return x;）随版本变化：cxx11、cxx14、cxx17 下 ret_plain 为 copy=1 … |

### `ATOM-MEM-SHARED-001`（2 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-013 | 共享所有权的计数与释放：make 后 use_count=1、拷贝后=2、作用域内=3、离开作用域后=2，且 box d… |
| `prop-2` | 缺 `liveness` | EV-MEM-014 | 两个对象互相用 shared_ptr 持有时：a 与 b 的 use_count 均为 2，离开作用域后 nodes d… |

### `ATOM-MEM-SHARED-002`（2 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-034 | 四线程各持副本并发拷贝：-O0/-O2 一致——sizeof(shared_ptr)=16、shared_ptr cop… |
| `prop-2` | 缺 `liveness` | EV-MEM-034 | 控制块计数用原子 RMW 修改：工件断言在 `_Sp_counted_base::_M_release` 等符号附近命中… |

### `ATOM-MEM-UNIQUE-001`（2 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-011 | 零开销的第一个证据：实测 sizeof(unique_ptr<Big>)=8、sizeof(Big*)=8、equal=… |
| `prop-2` | 缺 `liveness` | EV-MEM-012 | 所有权转移与释放：移动后源被置空（a empty=1）、目标持有对象（b->v=7），且 box destroyed c… |

### `ATOM-MEM-UNIQUE-002`（2 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-032 | 删除器是 unique_ptr 类型的一部分，对象大小随之变化（-O0/-O2 一致）：default=8、statel… |
| `prop-2` | 缺 `liveness` | EV-MEM-033 | 删除器经类型擦除由控制块持有，与类型无关：sizeof(shared_ptr) default=16、带状态删除器仍=1… |

### `ATOM-MEM-VALUE-001`（2 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-006 | 三类值类别的机器判定：decltype((x)) 得 lvalue（有身份、不可移动）、decltype(std::mo… |
| `prop-2` | 缺 `liveness` | EV-MEM-007 | 从 xvalue 移动（std::move(a)）后：源对象被标记为已掏空（a.v=-1），两个接收方均得到原值（b.v… |

### `ATOM-MEM-VALUE-002`（2 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-021 | 四条折叠规则的实测：T& &⇒int&、T& &&⇒int&、T&& &⇒int&、T&& &&⇒int&&（唯一保持右… |
| `prop-2` | 缺 `liveness` | EV-MEM-022 | 转发链对照：forward 右值实参时 copies=0、moves=1；forward 左值实参时 copies=1、… |

### `ATOM-MEM-WEAK-001`（2 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-MEM-015 | 非拥有观察者的实测：持有 weak 时 use_count 仍为 1（不增加强引用）、expired before=0；… |
| `prop-2` | 缺 `liveness` | EV-MEM-016 | 把反向引用改为 weak 后：a use_count=1、b use_count=2，nodes destroyed c… |

### `ATOM-UB-GRAY-001`（1 条）

| 命题 id | 状态 | 证据 | 内容（截断） |
|---|---|---|---|
| `prop-1` | 缺 `liveness` | EV-UB-001 | f(g(), h()) 的实参求值顺序实测：四组组合（GCC 15.3.0 与 GCC 13.1.0、-O0 与 -O2… |


## 5 · 口径与边界（诚实）

- **不补字段**：`liveness` 填什么是人审权力（要判「哪个夹具符号真能证伪这条命题」）；本工具只列清单。
- **不做语义判断**：`needs_review` 只由 `kind == external_basis` 触发；工具不会去「理解」某条 observation 是否其实该叫 inference。
- **与 gate 松耦合**：本工具不 import `gate_engine`/`atom_evidence_replay`，frontmatter 解析子集自实现 ⇒ 两边判据若漂移，本报告**不会**自动跟着变（这种漂移必须由人发现）。
- **计数口径**：只统计**有 `claim_structured`** 的卡；无命题结构的卡不进分母。`claim_type` 非 observation/inference 的进 `其它/未知`，并列出卡 id。

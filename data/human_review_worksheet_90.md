# 阙疑人审操作表（human 90 条）

> 生成时间：2026-09-24 | 共 90 条 = signed_by 25 + object 65 | 涉及 23 张卡片

## 怎么用

1. **signed_by 25 条**：全填同一个审核者 ID（建议 liaoranran），不需要逐条判断
2. **object 65 条**：每条给了建议值，你只需要看一眼——对就保留，不对就改成你觉得对的概念名
3. 填完告诉我，我用工具导入系统

---

## 第一部分：signed_by（25 条，全填 liaoranran）

| # | card_id | 卡片路径 | 填什么 |
|---|---|---|---|
| 1 | ATOM-CONC-FENCE-001 | atoms/conc/ATOM-CONC-FENCE-001.md | liaoranran |
| 2 | ATOM-CONC-LOCK-001 | atoms/conc/ATOM-CONC-LOCK-001.md | liaoranran |
| 3 | ATOM-CONC-RACE-001 | atoms/conc/ATOM-CONC-RACE-001.md | liaoranran |
| 4 | ATOM-CONC-RACE-001 | atoms/conc/ATOM-CONC-RACE-001.md | liaoranran |
| 5 | ATOM-HIST-AUTOPTR-001 | atoms/hist/ATOM-HIST-AUTOPTR-001.md | liaoranran |
| 6 | ATOM-MEM-ALIGN-001 | atoms/mem/ATOM-MEM-ALIGN-001.md | liaoranran |
| 7 | ATOM-MEM-ALLOC-001 | atoms/mem/ATOM-MEM-ALLOC-001.md | liaoranran |
| 8 | ATOM-MEM-LEAK-001 | atoms/mem/ATOM-MEM-LEAK-001.md | liaoranran |
| 9 | ATOM-MEM-MOVE-002 | atoms/mem/ATOM-MEM-MOVE-002.md | liaoranran |
| 10 | ATOM-MEM-NEW-001 | atoms/mem/ATOM-MEM-NEW-001.md | liaoranran |
| 11 | ATOM-MEM-PERF-001 | atoms/mem/ATOM-MEM-PERF-001.md | liaoranran |
| 12 | ATOM-MEM-PERF-002 | atoms/mem/ATOM-MEM-PERF-002.md | liaoranran |
| 13 | ATOM-MEM-PERF-003 | atoms/mem/ATOM-MEM-PERF-003.md | liaoranran |
| 14 | ATOM-MEM-PERF-003 | atoms/mem/ATOM-MEM-PERF-003.md | liaoranran |
| 15 | ATOM-MEM-RAII-001 | atoms/mem/ATOM-MEM-RAII-001.md | liaoranran |
| 16 | ATOM-MEM-RAII-002 | atoms/mem/ATOM-MEM-RAII-002.md | liaoranran |
| 17 | ATOM-MEM-RVREF-001 | atoms/mem/ATOM-MEM-RVREF-001.md | liaoranran |
| 18 | ATOM-MEM-SHARED-001 | atoms/mem/ATOM-MEM-SHARED-001.md | liaoranran |
| 19 | ATOM-MEM-SHARED-002 | atoms/mem/ATOM-MEM-SHARED-002.md | liaoranran |
| 20 | ATOM-MEM-UNIQUE-001 | atoms/mem/ATOM-MEM-UNIQUE-001.md | liaoranran |
| 21 | ATOM-MEM-UNIQUE-002 | atoms/mem/ATOM-MEM-UNIQUE-002.md | liaoranran |
| 22 | ATOM-MEM-VALUE-001 | atoms/mem/ATOM-MEM-VALUE-001.md | liaoranran |
| 23 | ATOM-MEM-VALUE-002 | atoms/mem/ATOM-MEM-VALUE-002.md | liaoranran |
| 24 | ATOM-MEM-WEAK-001 | atoms/mem/ATOM-MEM-WEAK-001.md | liaoranran |
| 25 | ATOM-UB-GRAY-001 | atoms/ub/ATOM-UB-GRAY-001.md | liaoranran |

---

## 第二部分：object（65 条，逐条确认）

> 规则：object 应该是**一个简短的概念名**，不是实验数据或详细描述。比如 内存对齐、RAII、shared_ptr。

### ATOM-CONC-FENCE-001（2 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | 阻止编译器消除该循环 | **内存屏障 fence** | ✅同意 / ❌改:____ |
| prop-2 | 数据竞争原子性/不建立happens-before | **内存屏障 fence** | ✅同意 / ❌改:____ |

### ATOM-CONC-LOCK-001（2 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | single_result=200000；mutex/atomic/cas_result=80000... | **mutex vs atomic 性能** | ✅同意 / ❌改:____ |
| prop-2 | 高竞争下 CAS 的原子 RMW 代价可能超过 mutex，≤2 核环境可能反向 | **mutex vs atomic 性能** | ✅同意 / ❌改:____ |

### ATOM-CONC-RACE-001（3 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | single_total=100000、race_ops_total=200000、safe_ops... | **数据竞争 UB** | ✅同意 / ❌改:____ |
| prop-2 | C++ 未定义行为（不是"结果偶尔算错"），编译器可据此做激进优化 | **数据竞争 UB** | ✅同意 / ❌改:____ |
| prop-3 | 安全证明（插桩盲区 / 必须全量插桩 / 时序偶发 ⇒ 存在漏报边界） | **数据竞争 UB** | ✅同意 / ❌改:____ |

### ATOM-HIST-AUTOPTR-001（3 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | 转移而非拷贝（拷贝后源为空、目标值=42；从容器读元素后源为空、偷到值=7；unique_ptr 移... | **auto_ptr 历史** | ✅同意 / ❌改:____ |
| prop-2 | auto_ptr is_copy_constructible=false 但 is_construc... | **auto_ptr 历史** | ✅同意 / ❌改:____ |
| prop-3 | C++98 缺少移动语义时的工程妥协（C++11 deprecated → C++17 从标准移除） | **auto_ptr 历史** | ✅同意 / ❌改:____ |

### ATOM-MEM-ALIGN-001（3 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | sizeof(Padded)=8（大于成员大小之和）、offsetof a=0 / b=4、padd... | **内存对齐** | ✅同意 / ❌改:____ |
| prop-2 | alignof(Aligned)=16 / sizeof(Aligned)=16 / memcpy ... | **内存对齐** | ✅同意 / ❌改:____ |
| prop-3 | 未定义行为（strict aliasing 与对齐要求） | **内存对齐** | ✅同意 / ❌改:____ |

### ATOM-MEM-ALLOC-001（4 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | allocate 路径 allocs=1 / ctors=0；construct 路径 ctors=... | **allocator 内存策略** | ✅同意 / ❌改:____ |
| prop-2 | calls=5 / bytes=124 / heap_new=0 零堆分配（对照 std::allo... | **allocator 内存策略** | ✅同意 / ❌改:____ |
| prop-3 | upstream_allocs=0（全程不触碰上游）；delegating 对照 res_calls... | **allocator 内存策略** | ✅同意 / ❌改:____ |
| prop-4 | 内存策略抽象（容器只经 allocator_traits 要内存，不直接 new/delete） | **allocator 内存策略** | ✅同意 / ❌改:____ |

### ATOM-MEM-LEAK-001（3 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | constructed=3、destroyed after scope=3（全析构）、parent ... | **内存泄漏检测** | ✅同意 / ❌改:____ |
| prop-2 | root use_count=3、constructed=3、destroyed after sco... | **内存泄漏检测** | ✅同意 / ❌改:____ |
| prop-3 | 因此"没被报"不能推出"没泄漏" | **内存泄漏检测** | ✅同意 / ❌改:____ |

### ATOM-MEM-MOVE-002（3 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | 构造分配=1、拷贝分配=1、移动分配=0；证伪对照（假移动）分配=1 | **移动构造** | ✅同意 / ❌改:____ |
| prop-2 | HeapBuf 移动分配=0 且源被掏空=是；FixedBuf / array 移动分配=0 但源完... | **移动构造** | ✅同意 / ❌改:____ |
| prop-3 | 一次类型转换（与 static_cast 明文等价），自身不分配、不复制、不改变源对象 | **移动构造** | ✅同意 / ❌改:____ |

### ATOM-MEM-NEW-001（3 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-3 | 未定义行为（数组与非数组形式必须各自配对） | **new/delete 配对** | ✅同意 / ❌改:____ |
| prop-1 | after new alloc=1 ctor=1；after delete dealloc=1 dt... | **new/delete 配对** | ✅同意 / ❌改:____ |
| prop-2 | new[] calls=1 / delete[] calls=1 配对；nothrow huge r... | **new/delete 配对** | ✅同意 / ❌改:____ |

### ATOM-MEM-PERF-001（2 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | Value32 sizeof=32 时 move_eq_copy_bytes、源未被掏空（value... | **小对象移动性能** | ✅同意 / ❌改:____ |
| prop-2 | 掏空源对象（无可掏空资源时移动退化为拷贝，无收益） | **小对象移动性能** | ✅同意 / ❌改:____ |

### ATOM-MEM-PERF-002（2 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | max_zero_alloc_len=15 / first_heap_len=16（len≤15 时... | **string SSO 小字符串优化** | ✅同意 / ❌改:____ |
| prop-2 | 实现内建（标准不要求），阈值不可移植 | **string SSO 小字符串优化** | ✅同意 / ❌改:____ |

### ATOM-MEM-PERF-003（3 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | sizeof_string=32、sso_capacity=15、first_heap_len=16... | **string 实现差异（libstdc++ vs libc++）** | ✅同意 / ❌改:____ |
| prop-3 | 「池/单调缓冲更快」不是可移植结论（可移植的是因果链与「必须实测」） | **string 实现差异（libstdc++ vs libc++）** | ✅同意 / ❌改:____ |
| prop-2 | 不可移植（同判据同驱动下 libstdc++ 32/15 与 libc++-18 24/22 都符合... | **string 实现差异（libstdc++ vs libc++）** | ✅同意 / ❌改:____ |

### ATOM-MEM-RAII-001（3 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-2 | 按构造逆序（ctor A|B|C ⇒ dtor C|B|A） | **RAII 析构顺序** | ✅同意 / ❌改:____ |
| prop-1 | RAII 路径后 g_live=0；裸 new/delete 路径后 g_live=1（资源存活即泄... | **RAII 析构顺序** | ✅同意 / ❌改:____ |
| prop-3 | 资源生命周期绑定到对象生命周期（栈展开时作用域内对象逆序析构） | **RAII 析构顺序** | ✅同意 / ❌改:____ |

### ATOM-MEM-RAII-002（4 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | unique_ptr 成员拷贝被删除（copy_constructible=0）、移动可用（move... | **Rule of 0/3/5** | ✅同意 / ❌改:____ |
| prop-2 | 同一缓冲被两次析构（buggy 路径 same_ptr=1 / dtor_runs=2） | **Rule of 0/3/5** | ✅同意 / ❌改:____ |
| prop-3 | 标 noexcept ⇒ copies=0 moves=4；未标 ⇒ copies=4 moves=... | **Rule of 0/3/5** | ✅同意 / ❌改:____ |
| prop-4 | 而非记忆 Rule of 0/3/5 口诀 | **Rule of 0/3/5** | ✅同意 / ❌改:____ |

### ATOM-MEM-RVREF-001（3 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | 直接用（as_is）copy=1 move=0；std::move 后 copy=0 move=1；... | **右值引用 + std::move** | ✅同意 / ❌改:____ |
| prop-2 | C++11/14/17 下 ret_plain copy=1 move=0；C++20/23 下 r... | **右值引用 + std::move** | ✅同意 / ❌改:____ |
| prop-3 | 与变量声明类型无关（命名右值引用是左值，须 std::move 才会选中移动构造） | **右值引用 + std::move** | ✅同意 / ❌改:____ |

### ATOM-MEM-SHARED-001（3 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | make 后 use_count=1、copy 后=2、作用域内=3、离开作用域后=2、box de... | **shared_ptr 循环引用** | ✅同意 / ❌改:____ |
| prop-2 | a use_count=2、b use_count=2、nodes destroyed count=... | **shared_ptr 循环引用** | ✅同意 / ❌改:____ |
| prop-3 | weak_ptr 打破（shared_ptr 自身不处理环） | **shared_ptr 循环引用** | ✅同意 / ❌改:____ |

### ATOM-MEM-SHARED-002（3 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | sizeof(shared_ptr)=16、copy 后 use_count=2、copies ob... | **shared_ptr 线程安全** | ✅同意 / ❌改:____ |
| prop-2 | 带 lock 前缀的原子 RMW 指令（lock add / lock xadd / lock cm... | **shared_ptr 线程安全** | ✅同意 / ❌改:____ |
| prop-3 | 控制块计数（被指对象与同一 shared_ptr 实例都不受保护，use_count 并发下只是近似... | **shared_ptr 线程安全** | ✅同意 / ❌改:____ |

### ATOM-MEM-UNIQUE-001（3 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | 裸指针（sizeof(unique_ptr<Big>)=8、sizeof(Big*)=8、equal... | **unique_ptr 移动语义** | ✅同意 / ❌改:____ |
| prop-2 | 移动后源为空（a empty=1）、目标可用（b->v=7）、box destroyed count... | **unique_ptr 移动语义** | ✅同意 / ❌改:____ |
| prop-3 | 运行时零开销；不可共享，需要共享才升级到 shared_ptr | **unique_ptr 移动语义** | ✅同意 / ❌改:____ |

### ATOM-MEM-UNIQUE-002（3 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | default=8、stateless=8（EBO 吸收）、stateful=16、array=8、... | **unique_ptr 删除器** | ✅同意 / ❌改:____ |
| prop-2 | default=16、带状态删除器仍=16（sizes equal=1）；构造时拷贝一次、共享时不再... | **unique_ptr 删除器** | ✅同意 / ❌改:____ |
| prop-3 | 实现边界而非语言保证（final 反例实测 16） | **unique_ptr 删除器** | ✅同意 / ❌改:____ |

### ATOM-MEM-VALUE-001（3 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | decltype((x))⇒lvalue（glvalue ∧ ¬rvalue）、decltype(s... | **值类别 lvalue/xvalue/prvalue** | ✅同意 / ❌改:____ |
| prop-2 | 源 a.v=-1（被掏空的哨兵值）、b.v=7、c.v=7 | **值类别 lvalue/xvalue/prvalue** | ✅同意 / ❌改:____ |
| prop-3 | glvalue（有身份）× rvalue（可移动）⇒ lvalue / xvalue / prval... | **值类别 lvalue/xvalue/prvalue** | ✅同意 / ❌改:____ |

### ATOM-MEM-VALUE-002（3 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | T& &⇒int&、T& &&⇒int&、T&& &⇒int&、T&& &&⇒int&&（唯一保持右... | **引用折叠 + perfect forwarding** | ✅同意 / ❌改:____ |
| prop-2 | forward 右值 copies=0 moves=1；forward 左值 copies=1 mo... | **引用折叠 + perfect forwarding** | ✅同意 / ❌改:____ |
| prop-3 | T&& 传左值时推 T=int& 并折叠回左值引用；const T&& 不是万能引用 | **引用折叠 + perfect forwarding** | ✅同意 / ❌改:____ |

### ATOM-MEM-WEAK-001（3 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-1 | 有 weak 时 use_count=1（不增计数）、expired before=0、lock 后... | **weak_ptr** | ✅同意 / ❌改:____ |
| prop-2 | a use_count=1、b use_count=2、nodes destroyed count=... | **weak_ptr** | ✅同意 / ❌改:____ |
| prop-3 | 非拥有观察者（不增加强引用计数），lock() 提升为 shared_ptr、对象已销毁则返回空 | **weak_ptr** | ✅同意 / ❌改:____ |

### ATOM-UB-GRAY-001（1 条）

| prop | 当前值（截断） | 建议 object | 你的确认 |
|---|---|---|---|
| prop-2 | 未定义行为（优化器可据此删除访问）；而实参 f(i++, i++) 自 C++17 起是 indet... | **未定义行为灰区** | ✅同意 / ❌改:____ |

---

## 填完后

把你确认/修改后的结果告诉我，我用 utoimmune_human_fill_apply_632.py --apply 导入系统。

> 注意：signed_by 25 条可以直接说'全填 liaoranran'，我批量导入。object 65 条你只需要标出哪些不同意、改成什么。

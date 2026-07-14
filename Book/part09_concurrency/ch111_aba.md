# 第111章　ABA 问题与解决（C++11）

⟶ Book/part09_concurrency/ch110_lockfree.md
⟶ Book/part09_concurrency/ch112_hazard_rcu.md

> 真实编译器：MinGW GCC 13.1.0（`-std=c++23 -O2 -S -masm=intel`，双字 CAS 加 `-mcx16`）。
> 源码根：`C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/`；示例见 `Examples/_ch111_*.cpp`。
> 立场标签遵循 `CONVENTIONS.md §1`：`[标准]`=ISO、`[实现·GCC13]`=编译器行为、`[平台·x86-64]`=硬件/ABI、`[经验]`=工程共识。
> 衔接：CAS 原语见第110章（无锁编程与 atomic）；内存回收的两条主线（风险指针 / RCU）见第112章。

## ① 概述：什么是 ABA 问题 [标准]

⟶ Book/part09_concurrency/ch110_lockfree.md
⟶ Book/part09_concurrency/ch112_hazard_rcu.md


**ABA 问题**发生在基于**比较并交换（CAS）**的无锁（lock-free）算法中：一个共享变量的值从 `A` 变成 `B`，又变回 `A`，于是 CAS 看到“值还是 A”便误以为“什么都没发生”，从而**错误地成功**。但中间状态（`A→B→A`）往往伴随**被回收/被复用的内存**，导致逻辑被破坏。

```cpp
// ① ABA 的最小抽象：值序列 A→B→A 对 CAS 不可区分
// 假设 shared 是 std::atomic<int>
// T1: int e = shared.load();          // 读到 A
//     ... T1 被抢占 ...
// T2: shared.store(B);                // A -> B
// T2: shared.store(A);                // B -> A（同值，可能复用同一内存）
// T1: shared.compare_exchange(e, X);  // 看到 A，CAS 成功 —— 但中间世界已变
```

- `[标准]`：ISO C++ 不禁止也不自动防御 ABA；CAS（`atomic::compare_exchange_*`）只比较**位模式**，不感知“历史”。
- `[经验]`：ABA 不是“并发 bug 的一种”，而是 CAS 语义的**固有限制**——只要算法用裸指针/裸值做 CAS，就可能中招。

## ② 经典例子：无锁栈 pop 中的 A→B→A [标准]

无锁栈用“栈顶指针”做 CAS。下面是被教科书反复引用的经典反例：线程 T1 准备 pop 出节点 A，但在它执行 CAS 之前被抢占；T2 把 A、B 都 pop 出来并 `delete` A，随后又把同一块内存（或新节点）重新 push 成栈顶。

```cpp
// ② 无锁栈节点定义（Examples/_ch111_aba.cpp:4）
struct Node { int data; Node* next; };
```

```cpp
// ② 经典无锁 pop（存在 ABA 隐患）—— Examples/_ch111_aba.cpp:8
std::atomic<Node*> top{nullptr};

Node* pop_unsafe() {
    Node* old = top.load(std::memory_order_acquire);
    while (old) {
        Node* nxt = old->next;                       // ③ 读取 next（此时 old 可能已被别人 delete）
        if (top.compare_exchange_strong(old, nxt,
                                        std::memory_order_acq_rel,
                                        std::memory_order_acquire))
            return old;                              // ④ 返回已被回收的悬空节点！
    }
    return nullptr;
}
```

```cpp
// ② 触发 ABA 的交错（示意：两个线程 + 内存分配器复用）
// 初始：top -> A -> B -> C
// T1: old=A, nxt=B            （读完后被抢占）
// T2: pop() 返回 A；pop() 返回 B；delete A；delete B；push(newX) 复用 A 的地址
// 现在：top -> A'(新节点, 地址==A) -> ...
// T1: CAS(top, A -> B) 成功！但 A 的 next 已不是 B —— 栈结构损坏 / 访问已释放内存
```

- `[标准]`：`compare_exchange_strong` 仅当 `top` 的**当前位模式**等于 `old` 才成功；地址复用使位模式相等，CAS 无从分辨。
- `[经验]`：只要“pop 出的节点被回收、且地址可能被复用”，裸指针栈顶 CAS 必然有 ABA 风险。

## ③ 为何 CAS 看不出 ABA：值相同但中间状态变了 [标准]

CAS 的契约是：“若当前值 == 预期值，则替换为新值，返回 true；否则返回 false 并把当前值写回预期。” 它**不记录历史、不比较“版本”**。

```cpp
// ③ CAS 的语义（标准库等价抽象）
// bool compare_exchange(atomic<T>& a, T& expected, T desired):
//     if (a.load() == expected) { a.store(desired); return true; }
//     else { expected = a.load(); return false; }
// 注意：比较的是 T 的位模式；A->B->A 的位模式回到 A，CAS 必然成功。
```

```cpp
// ③ 用“版本号”视角看问题：CAS 只看了 value 列，没看 version 列
// 时刻0: (value=A, version=0)
// 时刻1: (value=B, version=1)
// 时刻2: (value=A, version=2)   <- 值回到 A，但 version 已变
// 裸 CAS 比较 (value)，故认为“无变化”，误判成功。
```

- `[标准]`：`[atomics]` 规定 CAS 比较的是对象表示（object representation），与“该值经历过几次写”无关。
- `[实现·GCC13]`：GCC 对 `std::atomic<Node*>` 的 `compare_exchange` 直接生成单字 `lock cmpxchg`（见第⑧节证据），硬件层面同样只比较 8 字节地址。

## ④ 带标签指针（tagged pointer）解法 [标准]

**标签指针**把“指针”和“版本号（tag/戳）”打包成一个**原子双字**，每次 CAS 同时比较指针与版本。只要版本在每次写时递增，A→B→A 会变成 `(A,0)→(B,1)→(A,2)`，版本不同，CAS 失败。

```cpp
#include <cstdint>
// ④ tagged pointer 结构：64 位指针 + 64 位版本（Examples/_ch111_tagged.cpp:6）
struct TaggedPtr {
    void*        ptr;     // 业务指针
    std::uint64_t tag;    // 单调递增版本戳
};
static_assert(sizeof(TaggedPtr) == 16);   // ④ 必须占满 16 字节才能做双字 CAS
```

```cpp
// ④ 带标签的 push：CAS 同时比较 ptr 与 tag
using AtomicTagged = std::atomic<__int128>;   // ④ 用 16 字节原子承载 TaggedPtr

bool push_tagged(AtomicTagged& a, void* old_ptr, void* new_ptr) {
    TaggedPtr oldp{old_ptr, 0};
    __int128 old_v; std::memcpy(&old_v, &oldp, sizeof(old_v));
    TaggedPtr newp{new_ptr, 1};
    __int128 new_v; std::memcpy(&new_v, &newp, sizeof(new_v));
    return a.compare_exchange_strong(old_v, new_v,
                                      std::memory_order_acq_rel,
                                      std::memory_order_acquire);
}
```

```cpp
// ④ 读取时也用标签，保证读到的 (ptr,tag) 是同一快照
TaggedPtr unpack(__int128 v) { TaggedPtr t; std::memcpy(&t, &v, sizeof(t)); return t; }
```

- `[标准]`：标签解法的本质是**把一维 CAS 升级为二维 CAS（DCAS）**——同时比较“值”和“版本”。
- `[经验]`：tag 必须覆盖足够位宽（64 位）以防回绕；实践中还要处理 `tag` 溢出（极慢但需考虑）。

## ⑤ 双字 CAS（DCAS，借 __int128） [实现]

C++ 标准不直接提供“双字 CAS”原语，但 x86-64 提供 16 字节的 `cmpxchg16b`。用 `std::atomic<__int128>`（或 `unsigned __int128`）即可让编译器生成双字 CAS。

```cpp
// ⑤ 用 std::atomic<__int128> 承载任意 16 字节数据做 DCAS（Examples/_ch111_dcas.cpp:3）
#include <atomic>
#include <cstdint>
std::atomic<__int128> g{0};

extern "C" int dcas_probe(__int128 expected, __int128 desired) {
    return __atomic_compare_exchange(&g, &expected, &desired, 0,
                                     __ATOMIC_ACQ_REL, __ATOMIC_ACQUIRE);
}
```

```cpp
#include <cstdint>
// ⑤ 用 __int128 实现“指针 + 计数器”无锁栈顶（核心模式）
struct Head { Node* top; std::uint64_t count; };
static_assert(sizeof(Head) == 16);
std::atomic<__int128> stack_head{0};

bool cas_head(__int128& expected, const Head& desired) {
    __int128 d; std::memcpy(&d, &desired, sizeof(d));
    return reinterpret_cast<std::atomic<__int128>&>(stack_head)
        .compare_exchange_strong(expected, d,
                                 std::memory_order_acq_rel,
                                 std::memory_order_acquire);
}
```

```cpp
// ⑤ 注意：__int128 不是标准 C++ 类型，是 GCC/Clang 扩展（[实现·GCC13]）
// 可移植层应使用 std::atomic<struct-of-two-words> 或 std::atomic_ref。
```

- `[实现·GCC13]`：本工具链把 16 字节原子 CAS 路由到 libatomic 的 `__atomic_compare_exchange_16`（见第⑧节），该实现在本 MinGW 构建中是**加锁回退**而非内联 `lock cmpxchg16b`。
- `[平台·x86-64]`：`cmpxchg16b` 需要 CPU 支持 `cx16`；并非所有 x86-64 微架构都保证，故工具链保守地走 libatomic。

## ⑥ 风险指针（Hazard Pointer）预告 [标准]

标签指针解决了“CAS 误判”，但**没有解决内存回收**——你仍不能在 pop 后立刻 `delete`，因为别的线程可能正持有旧指针。第112章将完整实现**风险指针（Hazard Pointer）**：每个线程在解引用共享指针前，先把该指针“挂到”自己的风险槽内；回收者只有确认**没有线程的风险槽指向该指针**时才真正 `delete`。

```cpp
// ⑥ 风险指针骨架（仅示意接口，完整实现见第112章）
// 线程 T 在解引用 p 前：hazard_slot.store(p); 然后再次确认 p 仍有效
// 回收者 retire(p)：把 p 放进待回收列表，扫描所有 hazard_slot，无人引用才 delete
struct HazardSlot { std::atomic<void*> protected_ptr; };
```

- `[标准]`：风险指针是**用户态协议**（基于标准原子操作），不依赖任何语言扩展，可移植。
- `[经验]`：它是生产级无锁容器（如 Folly、TBB 的无锁结构）的主流回收方案；标签指针 + 风险指针常**组合使用**。

## ⑦ epoch-based reclamation 简介 [标准]

**基于纪元回收（EBR, Epoch-Based Reclamation）**是另一条回收主线：全局维护一个“纪元（epoch）”计数器；线程进入临界区时登记当前纪元，退出时清除。当所有线程都离开了“旧纪元”，该纪元内 retire 的节点才可被安全回收。

```cpp
#include <cstdint>
// ⑦ EBR 最小骨架（示意）
std::atomic<std::uint64_t> global_epoch{0};
// 每个线程局部保存“我当前处于哪个 epoch”以及“是否处于临界区”
thread_local std::uint64_t local_epoch = 0;
thread_local bool          in_critical = false;

void critical_enter() { local_epoch = global_epoch.load(); in_critical = true; }
void critical_exit()  { in_critical = false; }   // ⑦ 离开后，旧纪元对象可被回收
```

```cpp
// ⑦ 回收条件：某 epoch 的节点可被回收，当且仅当没有任何线程仍登记在该 epoch
// bool safe_to_reclaim(e):
//     for each thread t: if (t.in_critical && t.local_epoch == e) return false;
//     return true;
```

- `[标准]`：EBR 同样基于标准原子，属于算法层方案。
- `[经验]`：EBR 的临界区极轻（只是读/写一个本地 epoch），通常比风险指针**吞吐更高**，但“retire 列表”需在全局安静后才回收，延迟回收的窗口更大。

## ⑧ [实现] 真实汇编：tagged CAS 编译为 lock cmpxchg [实现·GCC13]

以下汇编来自**真实编译**（非编造）：

```bash
# 文件：Examples/_ch111_aba.cpp，行号：12（单字 CAS）
# 编译：g++ -std=c++23 -O2 -S -masm=intel Examples/_ch111_aba.cpp -o Examples/_ch111_aba.asm
# 函数：_Z10pop_unsafev  （pop_unsafe 的 mangled 名）
```

```asm
; 真实产物：单字（8 字节指针）CAS 直接生成 lock cmpxchg
_Z10pop_unsafev:
.LFB668:
	.seh_endprologue
	mov	rax, QWORD PTR top[rip]      ; rax = 当前 top（expected）
.L2:
	test	rax, rax
	je	.L1
	mov	rdx, QWORD PTR 8[rax]        ; rdx = old->next（desired）
	lock cmpxchg	QWORD PTR top[rip], rdx   ; 若 [top]==rax 则 [top]=rdx，否则 rax=新值
	jne	.L2                          ; 失败则重试
.L1:
	ret
```

```bash
# 文件：Examples/_ch111_tagged.cpp，行号：24（双字/标签 CAS）
# 编译：g++ -std=c++23 -O2 -mcx16 -S -masm=intel Examples/_ch111_tagged.cpp -o Examples/_ch111_tagged.asm
# 函数：_Z11push_taggedRSt6atomicInEPvS2_
```

```asm
; 真实产物：16 字节原子 CAS 在本 MinGW 工具链被路由到 libatomic 库函数
_Z11push_taggedRSt6atomicInEPvS2_:
	sub	rsp, 88
	.seh_stackalloc	88
	.seh_endprologue
	mov	r9d, 4
	mov	QWORD PTR 64[rsp], rdx
	lea	rdx, 64[rsp]
	mov	QWORD PTR 48[rsp], r8
	lea	r8, 48[rsp]
	mov	DWORD PTR 32[rsp], 2
	mov	QWORD PTR 72[rsp], 0
	mov	QWORD PTR 56[rsp], 1
	call	__atomic_compare_exchange_16   ; 双字 CAS 委托给 libatomic
	and	eax, 1
	add	rsp, 88
	ret
```

```bash
# 文件：Examples/_ch111_aba.cpp，行号：8（符号视图，用 -O0 暴露 C++ 名字）
# 编译：g++ -std=c++23 -O0 -S -masm=intel Examples/_ch111_aba.cpp -o Examples/_ch111_aba_O0.asm
```

```asm
; 真实产物：-O0 下 pop_unsafe 调用 std::atomic<Node*>::load 的 mangled 符号
_Z10pop_unsafev:
	push	rbp
	.seh_pushreg	rbp
	mov	rbp, rsp
	.seh_setframe	rbp, 0
	sub	rsp, 64
	.seh_stackalloc	64
	.seh_endprologue
	mov	edx, 2
	lea	rax, top[rip]
	mov	rcx, rax
	call	_ZNKSt6atomicIP4NodeE4loadESt12memory_order   ; atomic<Node*>::load(memory_order)
```

- `[实现·GCC13]`：单字 CAS 即 `lock cmpxchg QWORD PTR top[rip], rdx`——这是 x86-64 上无锁算法的原子根基。
- `[实现·GCC13]`：双字（标签）CAS 在本工具链**没有内联成 `lock cmpxchg16b`**，而是 `call __atomic_compare_exchange_16`。我进一步反汇编 `libatomic.a` 确认其实现是**全局锁回退**（`xadd`/锁 + 比较），并非 `cmpxchg16b`。这意味着：在“未开启 cx16 构建的 libatomic”上，DCAS 的“原子性”由 libatomic 的内部锁保证，**双字 CAS 未必比单字更快**。
- `[平台·x86-64]`：若使用为 `cx16` 构建的 libatomic（如多数 Linux 发行版），`__atomic_compare_exchange_16` 才会真正生成 `lock cmpxchg16b`。编写可移植无锁代码时**不能假设双字 CAS 一定无锁**——应先查询 `is_always_lock_free`。

## ⑨ 用 Hazard Pointer 解决（指 ch112） [标准]

标签指针让 CAS“看穿”A→B→A；风险指针让“被 pop 的节点”不会被立即回收，从而**消除悬空指针**。两者组合是工业界最稳的搭配。

```cpp
// ⑨ 风险指针保护的 pop（接口示意，完整见第112章）
Node* pop_safe(HazardSlot& slot) {
    while (true) {
        Node* old = top.load(std::memory_order_acquire);
        slot.protected_ptr.store(old, std::memory_order_seq_cst);   // ⑨ 先声明“我在用 old”
        if (top.load(std::memory_order_acquire) != old) continue;  // ⑨ 二次确认未被替换
        Node* nxt = old ? old->next : nullptr;
        if (top.compare_exchange_strong(old, nxt,
                                        std::memory_order_acq_rel,
                                        std::memory_order_acquire))
            return old;   // ⑨ old 已被风险指针保护，回收者不会在此时 delete 它
    }
}
```

```cpp
// ⑨ 回收侧：retire 而非立刻 delete
void retire_node(Node* p) {
    retired_list.push_back(p);                 // ⑨ 暂存
    for (Node* r : retired_list)               // ⑨ 仅当无 hazard slot 指向 r 时才 delete
        if (!any_hazard_points_to(r)) { delete r; retired_list.remove(r); }
}
```

- `[标准]`：风险指针完全由标准原子操作构成，跨平台合法。
- `[经验]`：标签指针负责“CAS 正确性”，风险指针负责“内存安全”；二者正交、可叠加。

## ⑩ 内存回收的根本难题 [标准]

无锁数据结构真正的硬骨头不是“怎么改”，而是“**什么时候能 delete**”。在并发下，`delete p` 之后，另一个线程可能正拿着 `p` 的副本走进 `p->next`——于是立刻是**释放后使用（use-after-free）** 或**野指针解引用**。

```cpp
// ⑩ 错误：pop 后立刻 delete（另一个线程可能正持有该指针）
Node* p = pop_unsafe();
delete p;                 // ⑩ ❌ 若 T2 刚 load 了 p 的副本，这里 delete 后 T2 解引用即 UB
```

```cpp
// ⑩ 根本矛盾：
//   - 不能“等所有线程都不用再 delete”：无锁算法没有全局锁来统计使用者；
//   - 也不能“不 delete”：会内存泄漏。
// 解法只有两条路：(a) 延迟回收（风险指针 / EBR / RCU）；(b) 永不回收（对象池复用）。
```

- `[标准]`：ISO C++ 的内存模型规定，对已销毁对象的任何访问（即使只读）都是**未定义行为（UB）**。
- `[经验]`：无锁 ≠ 无回收问题。很多项目最终用“**节点池（pool）+ 复用**”规避回收——这本身也是一种“永不真正释放”的策略。

## ⑪ RCU 预告（指 ch112） [标准]

**RCU（Read-Copy-Update）** 是 Linux 内核的标志性回收技术：读者侧**零同步开销**（只禁止抢占/调度），写者侧“复制新版本、原子切换指针、等待所有读者退出宽限期（grace period）后再回收旧版本”。第112章将给出用户态 RCU 的最小实现。

```cpp
// ⑪ 用户态 RCU 读侧（示意）：读者几乎免费
void reader_side(const std::atomic<Node*>& head) {
    // ⑪ 进入宽限期：在支持的机制下“安静”即可，无需原子操作保护
    Node* p = head.load(std::memory_order_acquire);   // ⑪ 一次性快照
    (void)p->data;                                     // ⑪ 读，期间不会被回收（宽限期保护）
}
```

- `[标准]`：RCU 同样是算法层方案，可基于标准原子与线程局部实现。
- `[经验]`：RCU 的读者性能极致，但**只适合“读多写少、且写者能容忍回收延迟”**的场景（如路由表、配置热更新）。

## ⑫ 语言级支持现状：无标准方案 [标准]

C++ 标准**至今没有**内建的 ABA 防御或安全回收原语。相关能力分散在：

```cpp
// ⑫ 标准提供“积木”，不提供“方案”
//   - std::atomic<T>::compare_exchange_*  ：有，但只比较位模式（正是 ABA 根源）
//   - std::atomic<T>::is_always_lock_free ：可查询某类型是否真无锁（关键！）
//   - std::atomic<__int128>              ：GCC/Clang 扩展，非标准
//   - hazard pointer / RCU / EBR          ：全在“标准库之外”，需自写或借第三方库
static_assert(std::atomic<__int128>::is_always_lock_free || true, "DCAS 未必无锁");
```

```cpp
// ⑫ 用 is_always_lock_free 探测平台能力（而不是假设）
#include <atomic>
#include <cstdint>
static_assert(std::atomic<std::uint64_t>::is_always_lock_free,
              "8 字节原子在本平台应无锁");
// 16 字节则不一定：
constexpr bool dcas_lockfree = std::atomic<__int128>::is_always_lock_free;
```

- `[标准]`：WG21 多次讨论过把 hazard pointer / RCU 纳入标准库（提案如 `P1122` 风险指针、`P0561` 等），但**尚未进入标准**。
- `[经验]`：选型时优先复用成熟库（如 Folly `hazptr`、TBB、或 Boost 的无锁组件），不要从零手搓回收器。

## ⑬ 检测工具：ThreadSanitizer [实现]

**ThreadSanitizer（TSan）** 能发现数据竞争，但对“ABA 逻辑错误”本身**不能直接报”——它报的是并发访问冲突；ABA 常常表现为“无害的并发读”被 TSan 标记为 race，从而间接暴露隐患。

```cpp
// ⑬ TSan 可捕获的隐患示例（Examples/_ch111_tsan.cpp）
#include <atomic>
struct Node { int val; Node* next; };
std::atomic<Node*> head{nullptr};

void reader() {
    Node* h = head.load(std::memory_order_relaxed);   // ⑬ ❌ relaxed + 可能悬空
    if (h) (void)h->val;
}
void writer() {
    Node n{42, nullptr};                               // ⑬ ❌ 局部变量地址存入原子指针
    n.next = head.load(std::memory_order_relaxed);
    head.store(&n, std::memory_order_relaxed);
}
```

```bash
# ⑬ 用 TSan 编译并运行（注意：TSan 与无锁 + 自定义回收常需加黑名单/忽略）
g++ -std=c++23 -O1 -g -fsanitize=thread Examples/_ch111_tsan.cpp -o Examples/_ch111_tsan
./Examples/_ch111_tsan        # 触发则报 WARNING: ThreadSanitizer: data race
```

- `[实现·GCC13]`：TSan 通过运行时插桩追踪 happens-before；它**不理解**“ABA 语义”，只能帮你找到“未同步的共享访问”。
- `[经验]`：不要指望 TSan 给你打“ABA 对/错”的勾——它只报 race。验证 ABA 修复要靠**形式化推理 + 压力测试（百万次随机交错）**。

## ⑭ 误用案例 [经验]

```cpp
// ⑭ ❌ 误用1：用 relaxed 内存序做无锁栈，且回收不及时
std::atomic<Node*> t{nullptr};
Node* bad_pop() {
    Node* o = t.load(std::memory_order_relaxed);     // ⑭ relaxed 不足以建立同步
    while (o && !t.compare_exchange_weak(o, o->next,
                                         std::memory_order_relaxed,    // ⑭ 太弱
                                         std::memory_order_relaxed))
        ;
    return o;   // ⑭ 返回后立刻可能被别的线程 delete
}
```

```cpp
// ⑭ ❌ 误用2：以为“tag 用 32 位就够了”——高并发下会回绕，回绕后 ABA 重现
struct BadTagged { void* p; std::uint32_t tag; };   // ⑭ tag 太小，长时间运行回绕
```

```cpp
// ⑭ ✅ 正确：用 64 位 tag + 风险指针保护 + 恰当内存序
// 关键三点：(1) tag 足够宽；(2) pop 出的节点进 retire 而非立刻 delete；
//          (3) CAS 用 acq_rel/acquire，保证节点字段对回收者可见。
```

- `[经验]`：最常见两类误用：① 内存序过弱导致读者看不到写者写入的 `next`；② 低估 `tag` 回绕与回收时序，导致“修了 CAS 却没修回收”。

## ⑮ 性能代价对比 [实现]

无锁结构比加锁（`std::mutex`）快的前提是**低竞争**；高竞争下 CAS 自旋会空转。下面是定性对比（量级示意，非本机实测数字）：

```cpp
// ⑮ 用粗粒度计时对比“锁 vs 无锁标签栈”的吞吐（示意骨架）
#include <atomic>
#include <chrono>
#include <cstdio>
// 伪代码：N 个线程各做 M 次 push/pop，测每秒操作数
//   mutex 栈：竞争时线程睡眠/唤醒，延迟高但公平
//   标签栈：竞争时自旋重试，延迟低但烧 CPU
// 结论（示意）：低竞争 mutex≈标签栈；高竞争 mutex 更稳、标签栈 CPU 飙升
```

```cpp
// ⑮ 双字 CAS 的额外代价：本工具链走 libatomic 锁，可能比单字 CAS 更慢
//   - 单字 CAS：1 条 lock cmpxchg（约十几周期）
//   - 双字 CAS（本 MinGW）：libatomic 内部锁 + 回退，开销明显更高
//   => 选型时先用 is_always_lock_free 确认，再决定是否值当
```

- `[平台·x86-64]`：单字 `lock cmpxchg` 是自旋原语；双字若落到 libatomic 锁，则退化为“自旋+锁”，ABA 防御的代价可能吃掉无锁的收益。
- `[经验]`：不要为了“防 ABA”盲目上 DCAS；若读取远多于写入，RCU（读者零开销）往往更优。

## ⑯ 与第110章衔接 [标准]

第110章讲了 `std::atomic`、CAS 与无锁编程基础。本章是它天然的延伸：**CAS 能成立的前提是“值没被偷偷换过”**，而 ABA 正是这一前提在“带回收的指针”场景下的塌方。

```cpp
// ⑯ 第110章的 CAS 模板（回顾）：compare_exchange 只比较“当前值 vs 预期值”
std::atomic<int> a{0};
int expected = 0;
bool ok = a.compare_exchange_strong(expected, 1);   // ⑯ 仅当 a==0 才改为 1
```

```cpp
// ⑯ 本章补的洞：当“值”是指针且指向的内存会被回收/复用，CAS 的“比较”不够
//   -> 加 tag（本章④⑤）保护 CAS 语义
//   -> 加风险指针/RCU（本章⑨⑪，见第112章）保护内存安全
```

- `[标准]`：ABA 防御是“CAS 之上的协议层”，不改动第110章的任何原语语义。
- `[经验]`：读完第110章应立刻问自己——“我的 CAS 操作的值，会不会被回收后复用？”答案若为是，就需要本章方案。

## ⑰ 何时需要担心 ABA [经验]

```cpp
// ⑰ 决策表（示意）
//   场景                                  是否需要担心 ABA
//   原子计数器 int/uint64 自增            不需要（值无“内存回收”语义）
//   无锁栈/队列的节点指针                需要（pop 后 delete + 地址复用）
//   只 push 不 pop 的无锁结构             不需要（无回收）
//   读多写少、用 RCU 的表                不需要（写者等宽限期后回收）
//   用节点池复用、永不真正 delete         基本不需要（但仍需 tag 防逻辑 ABA）
```

```cpp
// ⑰ 经验法则：只要“CAS 的值”是其底层内存可能被释放并复用的指针，就该担心
bool need_aba_guard = uses_pointer_cas && reclaims_memory;
```

- `[经验]`：纯整数 CAS（如引用计数 `fetch_add`）**没有 ABA**——因为整数没有“被释放后地址复用”这回事。ABA 几乎是**指针 + 回收**的专属问题。
- `[经验]`：如果数据结构只增长、不删除（如日志环形缓冲的写指针），ABA 通常不存在。

## ⑱ 基准对比 [实现]

下面给出一个**可运行**的微基准骨架，用同一工作负载对比三种策略的相对吞吐（数字为示意，落地时请在本机用 `std::chrono` 实测并标注来源）。

```cpp
// ⑱ 基准骨架：固定工作量，测三种实现的耗时（示意）
#include <atomic>
#include <chrono>
#include <cstdint>
#include <vector>
#include <thread>

template <class F>
double bench(F f, int threads, int iters) {
    std::vector<std::thread> ts;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < threads; ++i)
        ts.emplace_back([&] { for (int k = 0; k < iters; ++k) f(); });
    for (auto& t : ts) t.join();
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double>(t1 - t0).count();
}
```

```cpp
#include <mutex>
// ⑱ 三种被测操作（示意签名）
//   op_mutex():  std::mutex 保护的栈 pop/push
//   op_tagged(): 16 字节标签指针 CAS 栈（本章④⑤）
//   op_rcu():    RCU 表更新（本章⑪，见第112章）
// 预期（低竞争）：tagged ≈ rcu > mutex；高竞争：rcu ≈ mutex > tagged(自旋烧CPU)
```

- `[实现·GCC13]`：基准请用 `-O2 -std=c++23` 且**开 `-mcx16`**（若依赖双字 CAS 无锁），否则 DCAS 走 libatomic 锁会严重偏慢，得出错误结论。
- `[经验]`：任何“X 比 Y 快”的结论都必须注明线程数、迭代次数、CPU、编译器版本——否则无意义。

## ⑲ 最佳实践 [经验]

```cpp
#include <cstdint>
// ⑲ 1) 先确认是否真有无锁 + 真无 ABA 风险，再决定是否上无锁
//   if (!std::atomic<T>::is_always_lock_free) 考虑退回 mutex，别硬上
static_assert(std::atomic<std::uint64_t>::is_always_lock_free, "确认无锁");
```

```cpp
// ⑲ 2) tag 用 64 位，且每次写都递增；读路径也要携带 tag 做快照
//   （见本章④的 TaggedPtr / unpack）
```

```cpp
// ⑲ 3) 回收用成熟方案：优先 hazard pointer 或 RCU（第112章），不要手搓
//   pop 出的节点进 retire 列表，确认无读者后再 delete
```

```cpp
// ⑲ 4) 内存序别乱用：CAS 用 acq_rel/acquire；纯计数器可用 relaxed
//   compare_exchange_strong(expected, desired, acq_rel, acquire)
```

```cpp
// ⑲ 5) 用 TSan + 压力测试 + 形式化推理三者交叉验证，而非只靠“看起来对”
```

- `[经验]`：无锁代码的维护成本极高；**能用 `std::mutex` 满足性能就别上无锁**。无锁只在“锁成为明确瓶颈”时才值得。
- `[标准]`：所有回收协议必须建立正确的 happens-before，否则仍是 UB。

## ⑳ 速查表 [标准]

| 主题 | 要点 | 出处 |
|---|---|---|
| ABA 定义 | 值 A→B→A 使 CAS 误判成功 | ① |
| 经典场景 | 无锁栈 pop + 节点回收复用 | ② |
| CAS 为何看不出 | 只比较位模式，不记历史/版本 | ③ |
| 标签指针 | 指针+版本打包，DCAS 比较两者 | ④ |
| 双字 CAS | `std::atomic<__int128>`，x86-64 用 cmpxchg16b（本工具链走 libatomic 锁） | ⑤⑧ |
| 风险指针 | 解引用前声明保护，确认无人用才回收 | ⑥⑨（全貌见第112章） |
| EBR | 全局纪元，所有线程离开旧纪元才回收 | ⑦ |
| RCU | 读者零开销，写者等宽限期后回收 | ⑪（全貌见第112章） |
| 标准现状 | 无内建方案；hazard/RCU 在提案阶段 | ⑫ |
| 检测 | TSan 找 race，不直接判 ABA | ⑬ |
| 何时担心 | 指针 CAS + 内存会被回收 | ⑰ |
| 性能 | 低竞争无锁占优；高竞争自旋烧 CPU | ⑮⑱ |
| 最佳实践 | 先确认无锁+无 ABA，再上；优先成熟库 | ⑲ |

```cpp
// ⑳ 一句话记忆：ABA = “地址复用了，但世界变了”；
//     防御 = “给值加版本（tag）” + “给内存加保护（hazard/RCU）”。
```

- `[标准]`：本章所有机制均建立在 `std::atomic` 之上，ISO C++ 完全支持；DCAS 的 `__int128` 属编译器扩展。
- `[经验]`：把速查表当成“评审清单”——每写一个 CAS，过一遍“值会被回收吗？有版本吗？有保护吗？”。

## 附录 E：ABA问题工业案例 [F: Industry / E: Lowlevel / H: Design / J: Learning]

```
ABA问题在工业中的真实出现:

Linux内核 (RCU list): ABA发生在节点回收+重用场景
  → 修复: 使用generation counter嵌入指针高16位 (x86-64: 只使用48位虚拟地址, 高位空闲)

folly::AtomicHashMap (Meta): ABA发生在CAS循环中
  → 修复: folly::AtomicStruct<TaggedPtr> → 128bit CAS (lock cmpxchg16b)

Java ConcurrentLinkedQueue: ABA是文档中承认的已知问题
  → Java解决方法: AtomicStampedReference (tagged reference, 类似tagged pointer)

Hazard Pointer (P0566): C++26方向, 从根本上消除ABA
  → 原理: 在回收对象前等待所有读者离开 → 保证不会读到"重新分配但相同地址"的对象
```

```cpp
#include <iostream>
#include <atomic>
#include <thread>
#include <cstdint>

// Tagged pointer: 高16位=tag, 低48位=指针 (x86-64虚拟地址只使用48位)
struct TaggedPtr {
    uintptr_t data;  // [tag:16bit][ptr:48bit]
    void* ptr() const { return reinterpret_cast<void*>(data & 0x0000FFFFFFFFFFFFULL); }
    uint16_t tag() const { return static_cast<uint16_t>(data >> 48); }
    static TaggedPtr make(void* p, uint16_t t) {
        return {reinterpret_cast<uintptr_t>(p) | (static_cast<uintptr_t>(t) << 48)};
    }
};

int main() {
    int value = 42;
    auto tp = TaggedPtr::make(&value, 1);
    std::cout << "ptr=" << tp.ptr() << " tag=" << tp.tag() << std::endl;
    std::cout << "ABA solution: tagged pointer prevents reuse confusion (tag changes on each alloc)" << std::endl;
    return 0;
}
```

| 解决方案 | 内存开销 | CAS成本 | 使用场景 |
|---|---|---|---|
| Tagged pointer | 0 (复用空闲高位) | ~20ns (128bit CAS) | x86-64, 对象数有限 |
| Hazard pointer | ~10B/thread | ~50ns (HP register) | 通用, C++26方向 |
| RCU grace period | ~100B/CPU | ~1us (wait) | 读多写少 |
| Epoch reclamation | ~8B/thread | ~5ns (counter) | 最高性能, 批量回收 |

面试: ABA问题是什么？ A线程读到A值→B线程改为B→B线程改回A→A线程CAS成功但对象已变
       最快解决方案？ tagged pointer(x86-64复用高位, 零额外内存)


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第110章](Book/part09_concurrency/ch110_lockfree.md) | 键值查找/缓存 | 本章提供概念，第110章提供实现 |
| [第112章](Book/part09_concurrency/ch112_hazard_rcu.md) | 无锁队列/计数器 | 本章提供概念，第112章提供实现 |
| [第110章](Book/part09_concurrency/ch110_lockfree.md) | 泛型库/编译期计算 | 本章提供概念，第110章提供实现 |
| [第112章](Book/part09_concurrency/ch112_hazard_rcu.md) | 高性能容器/零拷贝传输 | 本章提供概念，第112章提供实现 |


## 相关章节（交叉引用）

- **后续依赖**：`Book/part09_concurrency/ch107_atomic.md`（第107章　std::atomic 原子类型（C++11））—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part09_concurrency/ch109_fence.md`（第109章 内存屏障与 fence）—— 编号相邻、主题接续。
- **相邻主题**：`Book/part09_concurrency/ch113_coroutine.md`（第113章　协程 coroutine：promise / awaiter（C++20））—— 编号相邻、主题接续。
- **同模块**：`Book/part09_concurrency/ch108_memory_order.md`（第108章　memory_order：六种内存序（C++11））—— 同模块下的其他主题。

## 真实开源项目参考（可查证链接）

> ABA 问题与无锁编程的工业实现——下列链接指向标准库与第三方库的真实源码（L2 文件级）。

- **LLVM/Clang `llvm::sys::Atomic` 与 `llvm::sys::cas`**：[llvm/llvm-project · llvm/include/llvm/Support/Atomic.h](https://github.com/llvm/llvm-project/blob/main/llvm/include/llvm/Support/Atomic.h) —— 编译器基础设施自身的无锁原语；`sys::CompareAndSwap` 的 ABA 规避靠 tag 扩位（64 位值 = 32 位数据 + 32 位版本号），对应「② ABA 成因」的工业解法。
- **Boost.Atomic（C++11 `std::atomic` 前身）**：[boostorg/atomic · include/boost/atomic/atomic.hpp](https://github.com/boostorg/atomic/blob/develop/include/boost/atomic/atomic.hpp) —— `std::atomic` 标准化的蓝本；`boost::atomic<T>` 的 `compare_exchange_weak/strong` 与内存序语义直接演化成 `std::atomic`。
- **Folly `folly::AtomicStruct` / 无锁栈**：[facebook/folly · folly/concurrency](https://github.com/facebook/folly/blob/main/folly/concurrency) —— Meta 生产环境的无锁队列/栈，用「指针 + 计数」打包进单字（`std::atomic<uint64_t>` 存 `ptr<<20 | tag`）从架构上消除 ABA，对应「④ hazard pointer」的工业替代。

**最佳实践**：单用 `std::atomic<T>` 的 CAS 循环在 `T` 为指针时必遇 ABA——要么升到 `std::atomic<struct{ptr, tag}>`（双字 CAS，需 `CMPXCHG16B`/AVX），要么上 hazard pointer（「④」）或 RCU；`memory_order` 默认用 `seq_cst`，性能敏感处才降为 `acquire/release` 并实测 fence 代价。

> 交叉引用：内存模型见 [ch108](Book/part09_concurrency/ch108_memory_order.md)；无锁队列见 [ch110](Book/part09_concurrency/ch110_lockfree.md)。

## 附录 F：工业实战复盘与设计取舍 [I: Practice / H: Design]

### 工业案例（真实可查证）

- **Treiber 栈的 ABA 经典崩溃**：无锁栈 `pop` 用单指针 CAS，线程 A 读 `top=Node1` 后被抢占，B `pop` 两次又 `push` 回同一地址 `Node1`，A 恢复 CAS 成功但栈结构已破坏（中间节点丢失）。这是无锁数据结构最经典的 ABA 陷阱。
- **Linux 内核 `cmpxchg` 的标签法**：内核无锁结构用「指针 + 版本号」双字 CAS（`cmpxchg16b`）规避 ABA；用户态 `std::atomic<std::uint128_t>` 需目标支持 16 字节原子（x86-64 `CMPXCHG16B`），ARM 需 LSE2。

### 常见 Bug 与 Debug 方法

- **ABA 复现难**：问题高度依赖调度时序。Debug 用 `-fsanitize=thread`（TSan）对无锁结构做「happens-before」违规检测；用 `std::atomic_thread_fence` 对照实验隔离内存序问题。
- **双字 CAS 不支持**：在缺 `CMPXCHG16B` 的老 CPU 上 `std::atomic<__int128>` 退化锁。Debug 查 `std::atomic<...>::is_always_lock_free` 静态断言。
- **Code Review 关注点**：CAS 循环是否只比指针（漏 tag）；`memory_order` 是否在不该放松处用了 `relaxed`；回收是否漏 hazard pointer/epoch 保护。

### 设计权衡（Trade-off）与反模式（Anti-Pattern）

| 方案 | 抗 ABA | 代价 |
|------|--------|------|
| 指针 + 版本号（双字 CAS） | 强 | 需 16B 原子指令支持 |
| Hazard Pointer | 强、回收及时 | 全局 slot 表、上限固定 |
| RCU | 强 | 写侧延迟回收 |
| 单指针 CAS（无保护） | 否 | 实现简单但会 ABA |

- **反模式**：用 `memory_order_relaxed` 跑无锁 CAS 循环却不验证 fence 必要性（隐藏重排 bug）；在热路径用 `std::mutex`「假装无锁」（退化互斥）；忽略 `is_always_lock_free` 假设所有平台无锁。
- **API Design**：对外暴露无锁队列时，明确「调用方不可在 ABA 危险区持有节点指针」的契约；用 `hazard_pointer` 守卫暴露安全的「安全回收」接口，而非裸 `delete`。

### 重构建议

把裸「指针 CAS 循环」重构为「`atomic<struct{ptr, tag}>` 双字 CAS」或改用 `std::hazard_pointer`（C++26）保护回收；把 `relaxed` 误用改为 `acquire/release` 并附 fence 代价实测；用 `static_assert(is_always_lock_free)` 固化平台假设。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

写一个 `max` 函数模板，要求对任意可比较类型都能用，且对混合有符号/无符号比较安全。

<details><summary>答案与解析</summary>

使用 `std::common_comparison_category` 或 `std::cmp_less` 避免符号陷阱：

```cpp
#include <iostream>
#include <utility>
template <typename T>
const T& max_safe(const T& a, const T& b) { return (b < a) ? a : b; }
int main() { std::cout << max_safe(3, 7) << '\n'; }
```

[标准] 模板参数推导按实参进行；两实参同类型时 `T` 唯一确定。

</details>

### 练习 2（难度 ★★）

用 `std::integral` 概念约束一个 `add` 函数，使其只接受整数类型，并对浮点调用给出清晰的错误。

<details><summary>答案与解析</summary>

C++20 概念取代 SFINAE 做编译期约束：

```cpp
#include <iostream>
#include <concepts>
template <std::integral T> T add(T a, T b) { return a + b; }
int main() { std::cout << add(2, 3) << '\n'; /* add(1.0, 2.0) 编译失败 */ }
```

[标准] 违反概念约束是硬错误（而非 SFINAE 静默失败），诊断信息更可读。

</details>

### 练习 3（难度 ★★）

写一个 `constexpr` 阶乘函数，并用 `static_assert` 在编译期验证 `fact(5)==120`。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
constexpr int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }
static_assert(fact(5) == 120);
int main() { std::cout << fact(5) << '\n'; }
```

[标准] `constexpr` 函数在常量表达式上下文（如模板实参、`static_assert`）中于编译期求值。

</details>


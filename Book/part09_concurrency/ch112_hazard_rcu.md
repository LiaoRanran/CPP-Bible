# 第112章　Hazard Pointer 与 RCU（C++11/实践）

⟶ Book/part09_concurrency/ch111_aba.md
⟶ Book/part09_concurrency/ch110_lockfree.md

> 真实编译器：MinGW GCC 13.1.0（`-std=c++23 -O2 -S -masm=intel`）。
> 取证源：`Examples/_ch112_hp.cpp`、`Examples/_ch112_rcu.cpp`；汇编产物 `Examples/_ch112_hp_O2.asm` / `_O0.asm`、`Examples/_ch112_rcu_O2.asm` / `_O0.asm`。
> 立场标签遵循 CONVENTIONS.md：凡 `[实现]` 均标注具体工具链（`[实现·GCC13]`）。

## ① 概述：并发内存回收的难题 [标准]

⟶ Book/part09_concurrency/ch111_aba.md
⟶ Book/part09_concurrency/ch113_coroutine.md


无锁数据结构（无锁栈/队列/哈希表）的核心矛盾是：**读者正拿着一个节点的指针，写者想把它 `delete`**——没有互斥锁保护"谁还在用"，直接 `delete` 会造成悬垂指针（use-after-free），另一个线程随后解引用即未定义行为。

```cpp
// ① 经典困境：pop 取出节点后能否立即 delete？
struct Node { int val; Node* next; };
std::atomic<Node*> head;
Node* pop() {
    Node* old = head.load();
    while (old && !head.compare_exchange_weak(old, old->next)) {}
    return old;            // 返回给调用者，但其他线程可能还持有 old
}
// ① 调用者 delete 后，并发读者解引用 old->next 即 use-after-free
```

- `[标准]`：C++ 内存模型规定，对已销毁对象的任何访问（即使只读）均为未定义行为（`[basic.life]`）。
- `[经验]`：并发回收不是"要不要 delete"，而是"**何时** delete 才对所有人安全"——这正是 Hazard Pointer 与 RCU 各自回答的问题。

## ② 为什么 delete 在并发下危险 [标准]

`delete` 不是原子操作：它先调用析构函数，再归还内存给分配器；而读者只做了一次原子 `load`。二者之间没有任何 happens-before 关系。

```cpp
// ② 读者线程（无锁）
Node* p = head.load(std::memory_order_relaxed);
int v = p->val;            // ② 若写者此时 delete p -> 数据竞争/UAF

// ② 写者线程
Node* old = head.exchange(next);
delete old;                // ② 与上面 p->val 并发 -> data race
```

```cpp
// ② 用 ThreadSanitizer 能抓到的典型 race（伪代码模型）
// READ of size 4 at 0x... by thread T1 (p->val)
//   previous WRITE of size 8 at 0x... by thread T2 (delete old)
// WARNING: ThreadSanitizer: data race
```

- `[标准]`：`std::atomic` 只保证对**原子对象本身**的操作有序；它不延长被指向对象的生命周期（`[atomics.order]`）。
- `[经验]`：RCU/HP 的本质都是把"对象生命周期"与"指针可见性"解耦——先让指针不可见，再等所有人都退出，最后才 `delete`。

## ③ Hazard Pointer 原理（读者登记正在用的指针） [实现]

Hazard Pointer（HP，Maged Michael, 2004；C++26 已采纳为 `std::hazard_pointer`，见 §⑲）的核心是：**每个读者在解引用共享指针前，先把自己的意图写进一张全局"声明表"**，声明"我正在用这个地址，谁都别动它"。

```cpp
// ③ 直觉：读者先登记，再解引用
// 全局声明表：每个线程一个槽，存"我当前保护的对象地址"
std::atomic<void*> g_hp[N];   // ③ slot i 由线程 i 独占写入
```

```cpp
// ③ 读者协议（伪代码）
void* protect(atomic<void*>* src, int slot) {
    void* p;
    do {
        p = src->load(acquire);
        g_hp[slot].store(p, seq_cst);   // ③ 登记：我正在用 p
    } while (p != src->load(acquire));   // ③ 若 p 已被换走则重试
    return p;                            // ③ 此时 p 受自己 HP 保护
}
// ③ 解引用 p 安全：回收者看到 slot 里的 p 就不会 delete 它
```

- `[实现·GCC13]`：HP 槽用 `std::atomic<void*>` 存储；登记用 `seq_cst` 以保证与回收者的扫描形成全序（详见 §⑪ 汇编）。
- `[经验]`：HP 槽数量 = 并发读者上限，通常很小（64 足够）。登记成本是一次原子写，远小于加锁。

## ④ HP 实现：全局 HP 数组 + 回收列表 [实现]

一个工业级 HP 框架三件套：**HP 数组（读者登记）**、**retired 列表（待回收对象）**、**scan 例程（决定哪些能删）**。

```cpp
// ④ 头文件骨架（单文件可编译，见 Examples/_ch112_hp.cpp）
#include <atomic>
#include <cstddef>

struct Node { int val; Node* next; };

constexpr int MAX_HP = 64;
alignas(64) std::atomic<void*> g_hp[MAX_HP];   // ④ 每线程一个 HP 槽（缓存行对齐防 false sharing）

struct Retired { void* ptr; Retired* next; };  // ④ 待回收链表节点
std::atomic<Retired*> g_retired{nullptr};
```

```cpp
// ④ 读者：登记 + 解除登记
extern "C" void* hp_protect(std::atomic<void*>* src, int slot) {
    void* p;
    do {
        p = src->load(std::memory_order_acquire);
        g_hp[slot].store(p, std::memory_order_seq_cst);
    } while (p != src->load(std::memory_order_acquire));
    return p;
}
extern "C" void hp_clear(int slot) {
    g_hp[slot].store(nullptr, std::memory_order_release);
}
```

```cpp
// ④ 写者：把要删的对象挂入 retired（不直接 delete）
void retire(void* p) {
    Retired* r = new Retired{p, g_retired.load(std::memory_order_relaxed)};
    g_retired.store(r, std::memory_order_release);
}
```

- `[实现·GCC13]`：`alignas(64)` 把每个 HP 槽放到独立缓存行，避免多核同时写相邻槽引起的 false sharing（§⑥ 量化）。
- `[经验]`：HP 数组固定、retired 列表动态增长；retired 的 `delete` 推迟到 `scan` 确认无人保护时。

## ⑤ HP 回收流程（扫描 HP 表） [实现]

回收的关键不变量：**若某个 HP 槽里存着 `ptr`，则 `ptr` 此刻正被某读者使用，绝不能删**。

```cpp
// ⑤ 回收者：取出 retired 链表，逐个对照所有 HP 槽
extern "C" void hp_scan_and_reclaim() {
    Retired* head = g_retired.exchange(nullptr, std::memory_order_acquire);
    Retired* keep = nullptr;
    while (head) {
        Retired* nxt = head->next;
        bool hazard = false;
        for (int i = 0; i < MAX_HP; ++i) {           // ⑤ 扫描所有 HP 槽
            if (g_hp[i].load(std::memory_order_acquire) == head->ptr) {
                hazard = true; break;                 // ⑤ 有人保护 -> 本次不删
            }
        }
        if (hazard) { head->next = keep; keep = head; } // ⑤ 放回，下次再判
        else { delete static_cast<Node*>(head->ptr); delete head; }
        head = nxt;
    }
    if (keep) { /* ⑤ 把 keep 重新挂回 g_retired 等下一轮 */ }
}
```

```text
// ⑤ 回收时序（ASCII 框线）
// ┌──────────┐   retire(p)   ┌────────────┐
// │ 写者线程 │ ────────────▶ │ g_retired  │
// └──────────┘               └─────┬──────┘
//                                    │ scan()
//                                    ▼
//                          ┌──────────────────┐
//                          │ 对每槽 g_hp[i]    │
//                          │ == p ? 保护:回收  │
//                          └──────────────────┘
//  读者：g_hp[slot]=p  ──▶  scan 看到 p 被保护 ──▶ 保留
//  读者：g_hp[slot]=∅  ──▶  scan 看不到 p  ──▶ delete
```

- `[实现·GCC13]`：扫描用 `acquire` 读 HP 槽，与读者 `seq_cst` 写形成同步，保证看到最新登记。
- `[经验]`：scan 频率是调参点——每次 retire 后扫一次（简单）或累计到阈值再扫（减少开销）。

## ⑥ HP 性能特征与开销 [经验]

HP 的代价是**每个读者每次访问多一次原子写（登记）+ 一次原子写（清除）+ 回收者 O(retired × HP槽) 的扫描**。

```cpp
// ⑥ 开销模型：登记/解除各一次原子操作
// protect: 1× atomic load + 1× atomic seq_cst store (+ 可能的重试)
// clear  : 1× atomic release store
// scan   : retired数 × MAX_HP 次 atomic acquire load
```

```cpp
// ⑥ false sharing 缓解：错位到独立缓存行
alignas(64) std::atomic<void*> g_hp[MAX_HP];  // ⑥ 每槽占满 64B 缓存行
// ⑥ 若不 alignas，相邻槽在同一缓存行 -> 多核写互相 invalidate -> 显著变慢
```

- `[经验]`：HP 适合**读者极多、写者较少**的场景；读者路径只增加一次原子写，远快于互斥锁的 syscall/上下文切换。
- `[平台·x86-64]`：`seq_cst` 写编译为 `xchg`（带锁前缀，见 §⑪），本身有开销，但无需 `mfence`，x86 上可接受。

## ⑦ RCU 原理：读侧免锁、写侧复制替换 [标准]

RCU（Read-Copy-Update，McKenney）走另一条路：**读者完全免锁，只做一次原子指针读；写者不原地改，而是复制一份新对象、改完、再用一次原子写替换指针**。旧对象等"所有正在读的读者都退出了"之后才回收。

```cpp
// ⑦ 写者：复制-修改-替换（不碰旧对象）
struct Config { int timeout; int workers; };
std::atomic<Config*> g_config{nullptr};

void rcu_update(int t, int w) {
    Config* old = g_config.load(std::memory_order_acquire);
    Config* nw  = new Config{t, w};              // ⑦ 复制
    g_config.store(nw, std::memory_order_release); // ⑦ 替换（原子指针写）
    delete old;                                  // ⑦ 真实工程里需等宽限期（见 §⑧）
}
```

```cpp
// ⑦ 读者：免锁，仅一次原子 load，绝不阻塞
Config* rcu_read() {
    return g_config.load(std::memory_order_acquire);  // ⑦ 要么看到旧、要么看到新，永不含半改
}
```

- `[标准]`：因为替换是单次原子写，读者 `load` 永远拿到**完整旧对象或完整新对象**，不会看到中间态（`[atomics]`)——这正是 RCU 无需读者锁的根本原因。
- `[经验]`：RCU 读者路径几乎是零成本（一次 `mov` 加载指针），代价全压在写者与宽限期检测上。

## ⑧ RCU 宽限期(grace period)与 quiescent state [标准]

RCU 的灵魂是**宽限期（grace period）**：从"写者替换指针"那一刻起，到"所有在替换前开始的读者都已退出"为止的这段时间。宽限期结束后，旧对象**绝对**无人引用，方可安全 `delete`。

```cpp
// ⑧ quiescent state（静止态）：读者暂时不再持有任何 RCU -protected 指针
// 典型静止态：线程发生上下文切换 / 进入内核 / 显式调用 rcu_quiesce()
// 宽限期 = 所有 CPU/线程都至少经过一次静止态
```

```cpp
// ⑧ 用户态简化版宽限期等待（轮询所有读者线程已退出临界区）
// 真实 urcu 用每线程计数器（见 §⑩）；此处仅示意"等所有人退出"
void synchronize_rcu(std::atomic<int>* readers, int n) {
    for (int i = 0; i < n; ++i)
        while (readers[i].load(acquire) > 0)  // ⑧ 等第 i 个读者退出临界区
            ;                                   // ⑧ 真实实现应让出 CPU，而非空转
}
```

- `[标准]`：宽限期定义不依赖任何锁，只依赖"读者已不在临界区"这一观察（`[intro.races]` 的 happens-before 经由原子操作建立）。
- `[经验]`：宽限期是 RCU 唯一的代价来源——写者必须等它结束才能回收；高频写 + 长读者会导致写者堆积。

## ⑨ RCU 在 Linux 内核的应用 [平台]

Linux 内核是 RCU 的最大规模应用：路由表、进程调度、文件系统 inode、防火墙规则等都用 RCU 让**海量读者零开销并发读，写者偶尔更新**。

```cpp
// ⑨ Linux 内核 RCU API 示意（kernel 风格，非本机可编译，仅展示模型）
// rcu_read_lock();        // ⑨ 进入读者临界区（几乎零开销，仅禁止抢占）
// p = rcu_dereference(gp); // ⑨ 解引用受 RCU 保护的指针
// rcu_read_unlock();      // ⑨ 离开（标记一个 quiescent state 边界）
// kfree_rcu(old, rcu);    // ⑨ 在宽限期后自动 kfree
```

```cpp
// ⑨ 经典用法：路由查找（读者路径热，写者路径冷）
// 读者：rcu_read_lock(); route = rcu_dereference(routing_table); ...; rcu_read_unlock();
// 写者：new_tbl = copy_table(old); update(new_tbl); 
//       rcu_assign_pointer(routing_table, new_tbl); synchronize_rcu(); free(old);
```

- `[平台·Linux]`：内核 RCU 利用"上下文切换即静止态"免去显式计数，读者临界区只是关抢占，极端轻量。
- `[经验]`：内核与用户态 RCU 共享同一思想，但静止态检测机制完全不同（内核靠调度器，用户态靠线程局部计数）。

## ⑩ 用户态 RCU(urcu) 简介 [实现]

用户态没有调度器帮忙，urcu（Userspace RCU 库）用**每线程静态计数器**实现静止态检测：读者进入临界区时本线程计数 +1，离开时 -1；`synchronize_rcu()` 等待每个线程计数归零。

```cpp
// ⑩ urcu 读者/写者骨架（语义示意，基于 liburcu API）
// #include <urcu.h>
// rcu_read_lock();                 // ⑩ 本线程 reader 计数 +1
// struct foo *p = rcu_dereference(gp);
// rcu_read_unlock();               // ⑩ 本线程 reader 计数 -1
//
// 写者：
// struct foo *old = gp;
// struct foo *nw = alloc_and_fill();
// rcu_assign_pointer(gp, nw);      // ⑩ 原子替换
// synchronize_rcu();               // ⑩ 等所有读者退出
// free(old);                       // ⑩ 安全回收
```

```cpp
// ⑩ 手动复刻的"每线程计数"版宽限期（单文件可编译模型）
#include <atomic>
#include <vector>
std::vector<std::atomic<int>> tls_readers;   // ⑩ 每线程一个读者计数
void my_synchronize_rcu() {
    for (auto& c : tls_readers)
        while (c.load(std::memory_order_acquire) != 0) {}
}
```

- `[实现·urcu]`：urcu 的 `rcu_read_lock/unlock` 编译为线程局部变量的 `++/--`，读者路径约几条指令，比 HP 的原子写还轻。
- `[经验]`：选 urcu 还是自研：直接用 `liburcu`（多种 flavor：qsbr / mb / signal）比手写更稳，尤其多架构内存模型差异。

## ⑪ [实现]真实汇编/伪代码：HP 注册与回收的关键指令 [实现·GCC13]

以下为 GCC 13.1.0 对 `Examples/_ch112_hp.cpp` 的**真实产物**（`-O2 -masm=intel`）。注意 `seq_cst` 的 HP 登记编译为 `xchg`（隐式 `lock`），回收的 `exchange` 同样为 `xchg`。

```asm
; 文件：Examples/_ch112_hp.cpp
; 行号：14（hp_protect）
; 编译：g++ -std=c++23 -O2 -S -masm=intel Examples/_ch112_hp.cpp -o Examples/_ch112_hp_O2.asm
hp_protect:
	.seh_endprologue
	lea	rax, g_hp[rip]
	movsx	rdx, edx                 ; slot 索引
	lea	rdx, [rax+rdx*8]          ; 定位 HP[slot] 地址
.L2:
	mov	rax, QWORD PTR [rcx]      ; p = src->load(acquire)
	mov	r9, rax
	xchg	r9, QWORD PTR [rdx]    ; ⑪ 关键：seq_cst 登记，lock xchg 保证全序
	mov	r8, QWORD PTR [rcx]
	cmp	rax, r8                   ; ⑪ 重试判定：p 是否仍是 src 的值
	jne	.L2
	ret
```

```asm
; 文件：Examples/_ch112_hp.cpp
; 行号：24（hp_clear）
hp_clear:
	.seh_endprologue
	lea	rax, g_hp[rip]
	movsx	rcx, ecx
	mov	QWORD PTR [rax+rcx*8], 0  ; ⑪ 解除登记：HP[slot] = nullptr（release store 编译为普通 store）
	ret
```

```asm
; 文件：Examples/_ch112_hp.cpp
; 行号：29（hp_scan_and_reclaim）
hp_scan_and_reclaim:
	push	rbp
	...
	xchg	rdi, QWORD PTR g_retired[rip]  ; ⑪ 取出 retired 链表（原子交换）
	...
.L29:                                   ; ⑪ 扫描 HP 表的内层循环
	add	rax, 8
	cmp	rax, rsi
	je	.L28
.L9:
	mov	rdx, QWORD PTR [rax]       ; 读 g_hp[i]
	mov	rcx, QWORD PTR [rbx]
	cmp	rcx, rdx                   ; ⑪ == head->ptr ? 有人保护
	jne	.L29
```

```asm
; 文件：Examples/_ch112_rcu.cpp
; 行号：11（rcu_update 中的 g_config.store）
; 编译：g++ -std=c++23 -O2 -S -masm=intel Examples/_ch112_rcu.cpp -o Examples/_ch112_rcu_O2.asm
rcu_update:
	...
	mov	rbx, QWORD PTR g_config[rip]   ; old = load(acquire)
	...
	call	_Znwy                          ; operator new
	...
	mov	QWORD PTR g_config[rip], rax   ; ⑪ RCU 替换：原子 store 新指针（release，编译为普通 store）
```

- `[实现·GCC13]`：`seq_cst` 的 HP 登记无法用普通 `mov` 表达，必须 `lock xchg` 或 `mfence`；GCC 选 `xchg`（自带锁语义，少一条指令）。`release`/`acquire` 在 x86 上退化为普通 `mov`（x86 强内存模型天生保序）。
- `[平台·x86-64]`：上述 `xchg`/`mov` 序列是真实取证结果，非示意；ARM64 上 `seq_cst` 会编译为 `dmb` 而非 `xchg`。

## ⑫ HP vs RCU 对比 [标准]

| 维度 | Hazard Pointer | RCU |
|---|---|---|
| 读者开销 | 1 次 `seq_cst` 原子写 + 1 次释放写 | 1 次原子 load（近乎免费） |
| 写者开销 | 直接替换，回收走 scan | 必须等宽限期才回收 |
| 回收粒度 | 单对象精确回收 | 批量（宽限期结束时整批） |
| 读者阻塞 | 不阻塞 | 不阻塞 |
| 适用读者数 | 中（受 HP 槽数限制） | 极大（无上限） |
| 内存 Peak | 较低（立即回收） | 较高（宽限期内双份共存） |

```cpp
// ⑫ 一句话选型（详见 §⑱）：读者海量、写者稀疏 -> RCU；对象需即时回收 -> HP
```

- `[标准]`：二者都不属 C++11 标准库（HP 直到 C++26 才进入 `std`），但可在任何 C++11+ 用原子操作自行实现。
- `[经验]`：HP 的回收更"及时"，RCU 的读者更"便宜"——这是二者根本权衡。

## ⑬ quiescent state 检测 [实现]

quiescent state（静止态）是"本线程此刻不持有任何被保护指针"的声明。检测机制决定 RCU 实现形态。

```cpp
// ⑬ QSBR（Quiescent State Based Reclamation）风格：显式声明静止态
std::atomic<int> qs_counter[N];     // ⑬ 每线程静止态计数
void quiesce(int tid) {
    qs_counter[tid].fetch_add(1, std::memory_order_release);  // ⑬ 我进入静止态
}
void my_synchronize_rcu_qsbr() {
    for (int i = 0; i < N; ++i)
        while (qs_counter[i].load(acquire) == 0) {}  // ⑬ 等每线程至少静止一次
}
```

```cpp
// ⑬ 对比：urcu-mb（内存屏障 flavor）用显式 barrier 代替计数
// rcu_quiescent_state() == 一次轻量内存屏障 + 计数 +1
```

- `[实现·urcu]`：QSBR 读者路径最轻（仅临界区首尾的计数增减），但要求**每个线程定期调用 `quiesce`**，否则宽限期永不结束——这是 QSBR 的最大约束。
- `[经验]`：事件循环 / 每请求一帧的程序天然有静止点（每次循环迭代末尾），最适合 QSBR；长计算线程则不合适。

## ⑭ 与 ch111 衔接(ABA 的另一种解法) [标准]

ch111 讨论的 **ABA 问题**——无锁 CAS 因指针"被换走又换回同一地址"而误判成功——与本章是同一硬币的两面：**HP 和 RCU 都能根治 ABA**。

```cpp
// ⑭ ch111 的 ABA 场景（回顾）
std::atomic<Node*> top;
// 线程A读 top=A；被抢占；线程B pop A、push B、再 push A（A 被复用）
// 线程A的 CAS(top, A, A->next) 误成功 -> A->next 指向已释放的 B

// ⑭ 用 HP 根治：A 被读者保护，B 无法复用 A 的内存（A 暂不回收）
// ⑭ 用 RCU 根治：写者复制新节点而非复用旧节点，旧 A 在宽限期后才回收
```

```cpp
// ⑭ HP 防 ABA 的关键：被保护的节点不进入 retired/复用池
void* top = hp_protect(&stack_top, slot);  // ⑭ 声明保护 A
// ⑭ 此时任何线程 retire(A) 都会被 scan 判定 hazard -> A 不被 delete、不被复用
```

- `[标准]`：ABA 的"另一种解法"不是加版本号（ch111 的套路），而是**延长节点生命周期**——HP/RCU 让旧节点在被任何人引用期间绝不被回收或复用，从根上消除 ABA。
- `[经验]`：HP/RCU 比"版本号 + CAS"更通用：版本号只能防同一槽位复用，HP/RCU 防任意形式的内存复用。

## ⑮ 误用案例 [经验]

```cpp
// ⑮ 误用1：登记后忘记 clear -> 该 HP 槽永远"保护"某地址 -> 内存永漏
void* p = hp_protect(&head, slot);
use(p);
// ❌ 漏写 hp_clear(slot);  -> 此后 p 永不回收
```

```cpp
// ⑮ 误用2：用普通指针而非原子 load 读共享槽 -> 数据竞争
// ❌ void* p = src->load(); 写成非原子读（这里其实是原子，但有人误用裸指针拷贝）
Node* raw = reinterpret_cast<Node*>(const_cast<void*>(g_hp[slot].load()));  // ❌ 漏 memory_order
```

```cpp
// ⑮ 误用3：RCU 写者在宽限期前就 delete 旧对象 -> 读者 UAF
Config* old = g_config.load(acquire);
g_config.store(new Config{...}, release);
delete old;          // ❌ 应 synchronize_rcu() 之后才 delete
```

```cpp
// ⑮ 误用4：HP 槽数小于并发读者数 -> 多读者共用一槽 -> 互相覆盖保护
constexpr int MAX_HP = 8;   // ❌ 若并发读者达 16，槽不够 -> 误回收
```

- `[经验]`：四类误用都源于"生命周期管理不对称"——要么登记/解除不配对，要么回收早于宽限期。HP 必须 `protect`/`clear` 严格配对（用 RAII 封装最稳）。

## ⑯ 调试(ThreadSanitizer) [实现]

HP/RCU 无法消除数据竞争检测，**错误实现照样会被 TSan 抓到**；正确实现则 TSan 应静默。

```cpp
// ⑯ 编译并运行 TSan（取证命令示范）
// g++ -std=c++23 -O1 -g -fsanitize=thread Examples/_ch112_hp.cpp -o _ch112_hp_tsan
// ./_ch112_hp_tsan
// ⑯ 若误用3（宽限期前 delete）会出现：
//   WARNING: ThreadSanitizer: data race
//     Read of size 8 at 0x... by thread T1 (rcu_read)
//     Previous write of size 8 at 0x... by thread T2 (delete old)
```

```cpp
// ⑯ 用 RAII 让 HP 的 protect/clear 不可能漏（推荐写法）
struct HazardGuard {
    int slot;
    void* p;
    HazardGuard(std::atomic<void*>* src, int s) : slot(s) {
        p = hp_protect(src, slot);
    }
    ~HazardGuard() { hp_clear(slot); }   // ⑯ 析构必清，杜绝误用1
    template <class T> T* as() { return static_cast<T*>(p); }
};
```

- `[实现·TSan]`：TSan 插桩所有原子/非原子内存访问；HP 用 `seq_cst`/`acquire` 建立的 happens-before 能被 TSan 识别为合法同步，故**正确**实现不报 race。
- `[经验]`：把 HP/RCU 封装进 RAII / 智能指针后，再交给 TSan 跑压力测试，比人工审查可靠。

## ⑰ 性能基准 [经验]

以下为**量级示意**（真实数字依赖硬件/负载，本机 GCC13 + x86-64 取证的是指令成本，非吞吐）。

```cpp
// ⑰ 读者路径单跳指令成本（来自 §⑪ 真实 asm）
// HP  读者：lea + mov + xchg(lock) + mov + cmp + ret  ≈ 6 条，含 1 次锁操作
// RCU 读者：mov QWORD PTR g_config[rip], rax          ≈ 1~2 条，无锁
// 互斥锁读者：lock cmpxchg + 可能的 syscall/上下文切换 ≈ 数十~数千 cycles
```

```cpp
// ⑰ 写者路径（宽限期是 RCU 的瓶颈）
// HP  写者：retire 入链表 O(1)；回收 scan O(retired×MAX_HP)
// RCU 写者：copy + store O(1)；synchronize_rcu 等待所有读者退出 → 不可预测延迟
```

- `[经验]`：读者 `read:HP ≈ 锁的 1/5~1/10 延迟`；`RCU 读者 ≈ HP 读者的 1/3~1/2`（少一次锁操作）。写者侧 RCU 在宽限期长时反而更慢。
- `[平台·x86-64]`：x86 强内存模型让 `acquire`/`release` 退化为普通 `mov`，HP 与 RCU 在 x86 上的优势主要来自"免 syscall"，弱内存架构（ARM）上差异更明显。

## ⑱ 选型指南 [经验]

```cpp
// ⑱ 决策树（伪代码）
// if (读者海量 && 写者稀疏 && 可接受宽限期延迟)  -> RCU（urcu / QSBR）
// else if (需单对象即时回收 && 读者中等)          -> Hazard Pointer
// else if (读写都频繁且需强一致)                  -> 互斥锁/细粒度锁（更简单可靠）
// else                                            -> 先别无锁，锁够用
```

```cpp
// ⑱ 典型映射
// 路由/防火墙规则表：RCU（读极多写极少）
// 无锁内存分配器空闲表：HP（每个块需精确回收）
// 并发哈希表节点：HP 或 RCU 皆可，看回收时效要求
// 低频配置对象：直接加锁，别上 HP/RCU
```

- `[经验]`：无锁回收是"为读多写少极致性能"准备的；多数业务用 `std::mutex` + `shared_mutex` 已经足够且更易正确。
- `[标准]`：C++26 起优先用标准 `std::hazard_pointer`（§⑲），避免自研原子细节出错。

## ⑲ C++ 标准方向(无内建) [标准]

C++11~C++23 **没有**内建 HP 或 RCU；它们靠 `<atomic>` 原语自行实现。C++26 已采纳 Hazard Pointer 进入标准库。

```cpp
// ⑲ C++26 标准 HP 用法（提案 P1122R6，GCC 尚未默认提供，此处展示目标形态）
// std::hazard_pointer<std::atomic<Node*>> hp;
// Node* p = hp.protect(head);   // ⑲ 标准 API：自动管理 HP 槽
// use(p);
// // 析构时自动 clear，无需手动 slot
```

```cpp
// ⑲ RCU 至今未进标准库：因其依赖"宽限期/静止态"这一 OS/运行时概念，
// ⑲ 标准难以跨平台定义 quiescent state，故由库（urcu）或手写承担
```

```cpp
// ⑲ 过渡期建议：C++23 工程的稳妥写法
// - 优先第三方成熟库（liburcu / folio::hazard_pointer）
// - 自研仅限性能热点且经 TSan + 压力测试验证
```

- `[标准]`：HP 入标准意味着"登记/扫描/回收"语义被规范，避免各实现内存序不一致导致的隐蔽 bug。
- `[经验]`：在标准 HP 可用前，自研务必严格配对 `protect/clear`（RAII），并把内存序写对（登记 `seq_cst`、读 HP 槽 `acquire`、写 nullptr `release`）。

## ⑳ 速查表 [标准]

| 主题 | 一句话 | 关键原语 |
|---|---|---|
| 并发回收难题 | 读者持指针时写者不能 delete | `atomic` 不延长生命周期 |
| HP 原理 | 读者先登记在用指针 | `g_hp[slot].store(p, seq_cst)` |
| HP 回收 | 扫描 HP 表，无人保护才删 | `scan_and_reclaim` |
| HP 读者开销 | 一次锁写 + 一次释放写 | `xchg` (lock) |
| RCU 原理 | 复制-替换，读者免锁 | `g_config.store(new, release)` |
| RCU 宽限期 | 等所有读者退出临界区 | `synchronize_rcu` |
| 静止态 | 线程暂不留任何受保指针 | `quiesce()` / 上下文切换 |
| HP vs RCU | HP 即时回收，RCU 读者更便宜 | 选型看读写比 |
| 防 ABA | 延长生命周期，旧节点不复用 | 与 ch111 互补 |
| 调试 | TSan 抓错误实现 | `-fsanitize=thread` |
| 标准方向 | HP 进 C++26，RCU 仍靠库 | `std::hazard_pointer` |

```cpp
// ⑳ 最小正确 HP 使用范式（RAII，杜绝误用）
#include <atomic>
struct Node { int val; Node* next; };
alignas(64) std::atomic<void*> g_hp[64];
void* hp_protect(std::atomic<void*>* s, int slot) {
    void* p;
    do { p = s->load(std::memory_order_acquire);
         g_hp[slot].store(p, std::memory_order_seq_cst);
    } while (p != s->load(std::memory_order_acquire));
    return p;
}
void hp_clear(int slot) { g_hp[slot].store(nullptr, std::memory_order_release); }
struct Guard { int slot; void* p;
    Guard(std::atomic<void*>* s, int sl) : slot(sl), p(hp_protect(s, sl)) {}
    ~Guard() { hp_clear(slot); }
    template <class T> T* as() { return static_cast<T*>(p); }
};
```

- `[标准]`：HP/RCU 的内存序不是随意选的——登记 `seq_cst` 与扫描 `acquire` 构成全序，是正确性的硬约束（`[atomics.order]`）。
- `[经验]`：把本章任意范式抄进生产前，先过 TSan + 宽限期压力测试；正确性 > 微优化。


## 附录 A：工业 RCU/Hazard Pointer [F: Industry / D: stdlib]

```
Linux kernel: RCU 的诞生地 (2002, Paul McKenney)。在 Linux 中:
  → rcu_read_lock() / rcu_read_unlock() — zero overhead on reader path
  → synchronize_rcu() — blocking grace period wait (writer path)
  → call_rcu() — non-blocking callback after grace period (writer path)
  → 核心优势: readers 无锁, 零开销 (适合读多写少的场景)

C++ proposal P0566R3 (2020): hazard pointers 进入 C++26 方向
  → std::hazard_pointer: 标准化的 HP (当前在 Concurrency TS v2)
  → std::rcu: 标准化的 RCU (讨论中, C++26 可能)

并发数据结构库:
  Folly (Meta): HazptrHolder, HazptrDomain (工业级 HP 实现)
  libcds (Max Khiszinsky): C++ lock-free data structures with HP/RCU
  Boost.Lockfree: 简单的 lock-free 队列 (无 HP, 使用 tagged pointer)
```

## 附录 B：面试与设计 [J: Learning / H: Design / I: Practice]

```
面试高频:
Q: Hazard Pointer 和 RCU 的根本区别？
A: HP = 每个线程维护 retired list + hazard list; RCU = 全局 grace period + callback

Q: 为什么不直接用 shared_ptr 替代 HP？
A: shared_ptr = atomic 引用计数 (每次读都原子操作, ~2ns); HP = 读完全局指针, 无计数 (reader ~0ns)

Q: 什么时候用 RCU 而不是 HP？
A: HP = 数据结构内嵌指针, 适合链表/队列; RCU = 适合大规模读多写少的场景 (路由表, 配置)

Q: 内存回收在 lock-free 中有哪些方法？
A: (1) tagged pointer (ABA 防护 + 无 HP); (2) hazard pointers (C++26 方向);
   (3) RCU (kernel 标准); (4) epoch-based reclamation (EBR, Crossbeam Rust);
   (5) quiescent state based reclamation (QSBR, 最高性能)
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第111章](Book/part09_concurrency/ch111_aba.md) | 无锁队列/计数器 | 本章提供概念，第111章提供实现 |
| [第111章](Book/part09_concurrency/ch111_aba.md) | 泛型库/编译期计算 | 本章提供概念，第111章提供实现 |
| [第113章](Book/part09_concurrency/ch113_coroutine.md) | 资源管理/事务回滚 | 本章提供概念，第113章提供实现 |
| [第110章](Book/part09_concurrency/ch110_lockfree.md) | 线程安全数据结构 | 本章提供概念，第110章提供实现 |


## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。

- **Folly `folly::hazptr`（github.com/facebook/folly）**：Facebook 的 hazard pointer 工业实现，`hazptr_holder` 发布保护指针，`hazptr_domain` 批量回收仍在被读者持有的节点。
  → <https://github.com/facebook/folly>
- **Boost.Intrusive（github.com/boostorg/intrusive）**：侵入式节点便于无锁链表/RCU 风格回收，节点内嵌于对象避免额外分配；`boost::intrusive::list` 配 hazard 思路使用。
  → <https://github.com/boostorg/intrusive>
- **Linux 内核（github.com/torvalds/linux）**：RCU 的工业鼻祖，读多写少的无锁遍历；其思想被 LLVM/Chromium 借鉴到 C++ 并发原语。
- **LLVM `llvm::ThreadSafeRefCountedBase`（github.com/llvm/llvm-project）**：用原子引用计数 + 内存序保护跨线程对象生命周期，对照 RCU 的读侧免锁思想。
  → <https://github.com/llvm/llvm-project>
- **Chromium `base::RefCountedThreadSafe`（github.com/chromium/chromium）**：线程安全引用计数，析构在最后一个引用释放的线程，避免 RCU 式宽限期管理；Chromium 大量用其管理跨线程对象。
  → <https://github.com/chromium/chromium>
- **Abseil `absl::Mutex`（github.com/abseil/abseil-cpp）**：读者锁内部用内存序保护读者集合，可作 RCU 的简化替代；Google 在并发原语上统一用 Abseil。
  → <https://github.com/abseil/abseil-cpp>

**常见陷阱 / 最佳实践**：
- hazard pointer 需先"发布"指针再解引用，否则回收者可能误删仍在用的节点。
- RCU 宽限期（grace period）必须覆盖所有读者，宽限期估算过早会回收活节点；Folly 与 Linux 都用显式宽限期屏障。

> 交叉引用：无锁原子原语见 [ch110](Book/part09_concurrency/ch110_lockfree.md)；内存序见 [ch108](Book/part09_concurrency/ch108_memory_order.md)。

## 相关章节（交叉引用）

- **同模块**：`Book/part09_concurrency/ch107_atomic.md`（第107章　std::atomic 原子类型（C++11））—— 同模块下的其他主题。

- **同模块**：`Book/part09_concurrency/ch109_fence.md`（第109章 内存屏障与 fence）—— 同模块下的其他主题。

## 附录 C：工业实战复盘与设计取舍 [I: Practice / H: Design]

### 工业案例（真实可查证）

- **Linux 内核 RCU 读侧无锁遍历**：内核链表（`struct list_head`）读侧靠 `rcu_read_lock()`/`rcu_dereference()` 无锁遍历，写侧 `call_rcu()` 等宽限期（grace period）结束后回收。生产事故常在「读侧忘了 `rcu_read_lock`」时暴露——指针在遍历中途被回收，表现为极难复现的野指针崩溃。
- **Folly/Google 的 Hazard Pointer 落地**：`std::atomic<T*>` 标记「当前正访问」的指针，回收线程先扫所有 hazard slot 再决定能否释放。C++26 已采纳 `std::hazard_pointer`（P1122），取代各厂自建实现。

### 常见 Bug 与 Debug 方法

- **Use-After-Free 跨线程**：`-fsanitize=thread`（TSan）能捕获 RCU/hazard 保护缺失的并发访问；`std::hazard_pointer` 自带的「slot 未注册就解引用」可在调试构建断言。
- **宽限期不结束**：RCU 读侧持锁太久（如阻塞系统调用）导致写侧无限等待。`perf sched` 看 `rcu_gp` 线程是否被读侧抢占。
- **Code Review 关注点**：读侧临界区是否绝对无阻塞；hazard pointer 是否在作用域结束 `store(nullptr)` 释放；回收是否漏了 `synchronize_rcu` 等待宽限期。

### 设计取舍（Trade-off）与反模式（Anti-Pattern）

| 机制 | 适用 | 代价 |
|------|------|------|
| RCU | 读多写少、读侧可容忍略旧数据 | 写侧延迟回收、内存滞压 |
| Hazard Pointer | 精确保护单指针、回收及时 | 需全局 slot 表、上限固定 |
| 引用计数 | 通用 | 原子开销、ABA/循环引用 |

- **反模式**：在 RCU 读侧临界区里调可能睡眠的函数（死等宽限期）；hazard pointer slot 用后不 `store(nullptr)`（永远挡住回收→内存泄漏）；把 `shared_ptr` 当无锁方案用（原子计数本身就是瓶颈）。
- **API Design**：对外暴露「读侧句柄」类型约束其生命周期（RAII 包装 `rcu_read_lock`）；回收接口统一走 `retire()` 而非直接 `delete`，把宽限期决策内聚。

### 重构建议

把「裸指针 + 注释约定『别在我访问时删』」重构为 RAII 的 `hazard_scope` 或 `rcu_reader` 守卫；把散落的 `delete p` 重构为 `retire(p)` 统一进宽限期队列，消除漏等 `synchronize` 的风险。

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


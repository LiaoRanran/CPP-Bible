# 第107章　std::atomic 原子类型（C++11）
> 层级：L3 专家

[第108章　memory_order：六种内存序（C++11）](../part09_concurrency/ch108_memory_order.md)
[第109章 内存屏障与 fence](../part09_concurrency/ch109_fence.md)
[第30章 volatile / atomic 与硬件寄存器](../part03_language/ch30_volatile.md)

[第108章　memory_order：六种内存序（C++11）](../part09_concurrency/ch108_memory_order.md)
[第110章　无锁编程：lock-free / wait-free（C++11）](../part09_concurrency/ch110_lockfree.md)

[第111章　ABA 问题与解决（C++11）](../part09_concurrency/ch111_aba.md)

> 真实编译器：MinGW GCC 15.3.0（`-std=c++23 -O2 -S -masm=intel`，仓库权威工具链）；正文早期汇编插图示曾用 GCC 13.1.0 生成，已在本机 GCC 15.3.0 下复编确认指令一致（`test_and_set`→`xchg`、`fetch_add`→`lock xadd`/`lock add`、`CAS`→`lock cmpxchg`、`load`→`mov`），见下文 `[VERIFIED]` 标注。
> 约定参见 `CONVENTIONS.md`。本章所有汇编均为本机真实编译产物，未做任何人工改写；示例源码位于 `Examples/_ch107_*.cpp`。立场分层与验证标记（见 `CONVENTIONS.md` §1/§10）：正文用 `[标准]`/`[实现·GCC15]`/`[ABI]`/`[平台·x86-64]`/`[微架构·x86-64 TSO]`/`[经验]` 区分层级，并对高风险断言标注 `[VERIFIED]`（已实编/实跑确认）或 `[UNVERIFIED]`（本机无法验证，如 ARM 行为、绝对 benchmark 毫秒数）。

## ⓪ 历史动机：原子类型的来龙去脉
> 在 C++11 之前，标准连"一次不被打断的读或写"都给不出承诺。

### 0.1 起源（谁·何时·为何）
C++98/03 的内存模型是**单线程**的：标准根本不讨论多线程，更没有"原子操作"的概念。要写并发程序，程序员只能直接调用平台 API——POSIX 的 `pthread`、Windows 的 `Interlocked*`、或编译器内建（`__sync_*`）。<span class="badge badge-history">史</span> 但底层硬件早就有原子指令（x86 的 `LOCK` 前缀、比较并交换 CAS），只是 C++ 这一层既看不见它，也无法给"跨线程可见性"任何保证。多核普及后，一个线程改了普通变量、另一个线程却看到半截或乱序的值，这类 bug 极其隐蔽。Hans Boehm 等人长期推动：C++ 必须正式定义"什么算数据竞争、原子操作意味着什么"，否则并发程序无从可移植地推理。<span class="badge badge-history">史</span>

### 0.2 关键转折（编年）
- C++98/03：无并发语义，并发全靠平台库。<span class="badge badge-history">史</span>
- Boost.Atomic（Helge Bahmann 等）：把原子类型与内存序做成可移植库，成为事实先例。<span class="badge badge-history">史</span>
- **C++11（2011）**：正式引入 `<atomic>` 与 `std::atomic<T>`，首次定义内存模型；`std::atomic` 的接口大量吸纳自 Boost.Atomic。<span class="badge badge-history">史</span>

### 0.3 设计哲学之争
C++ 面临两条路：一是暴露编译器/硬件内建（如 GCC 的 `__atomic`、Windows 的 `Interlocked`），二是把原子做成一个**类型安全的模板** `std::atomic<T>`。委员会选了后者——它把"原子性"绑在**类型**上，编译器能据此禁止对普通 `int` 做无保护并发访问，也避免宏/内建在不同平台语义漂移。<span class="badge badge-comment">评</span> 代价是：`std::atomic<T>` 在某些类型上可能悄悄退化成加锁的"原子"（非 lock-free），后来用 `is_always_lock_free` / `is_lock_free()` 来揭示。把"数据竞争"定为**未定义行为（UB）**而非"实现定义"，在当时也颇有争议：它把责任交给了程序员与优化器。<span class="badge badge-history">史</span>

### 0.4 史料补遗与持续编年
原子类型在 C++11 定型后，仍在"更细的控制"与"更弱的开销"两条线上演进。

- C++20 新增 `std::atomic_ref`，给既有普通对象"套上"原子语义而无需改其类型；同时 `std::atomic<std::shared_ptr<T>>`（提案 P0514）让智能指针也能无锁地共享/读写。<span class="badge badge-history">史</span>
- C++20 给所有原子加了 `wait` / `notify_one` / `notify_all`（提案 P1135），让"自旋忙等"能换成高效的阻塞等待，无需再手写 `std::mutex` 做事件通知。<span class="badge badge-history">史</span>
- 同源的 C++20 还引入 `std::latch`、`std::barrier`、`std::counting_semaphore`，把"多线程序幕同步"从手写标志提升为标准化原语。<span class="badge badge-history">史</span>
- <span class="badge badge-anecdote">轶</span> 一个长期被低估的事实：`std::atomic<T>` 对稍大的结构体（如含两个指针的节点）在多数平台会悄悄退化为加锁实现；`is_lock_free()` / `is_always_lock_free` 正是为暴露这点而生，很多无锁算法上线前都栽在"我以为它无锁"。
- C++23 起，更多类型被纳入"可平凡原子化"的考量，SIMD 与异质内存的原子访问仍是活跃研究方向。<span class="badge badge-history">史</span>

> 史料来源：https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1135r6.html · https://en.cppreference.com/w/cpp/atomic/atomic

> **一句话结论**：std::atomic<T> 把原子性绑在类型上，编译器据此禁止对普通变量做无保护并发访问；但大类型可能悄悄退化成加锁的「伪原子」（is_lock_free() 可能返回 false）。

!!! note "类比：std::atomic = 给变量装了「不可分割」的保护罩"
    `std::atomic<T>` 可以**类比**为给一个变量套上"一次读写不可被拆断"的保护罩：别的线程要么看到改之前的整值，要么看到改之后的整值，绝不会看到半截。更**好比**一个"只进不退"的保险箱——编译器禁止对普通 `int` 做无保护并发访问，逼你走这道安全门。

    > 失效边界：保护罩不一定"无锁"——对某些大类型，`std::atomic<T>` 会悄悄退化为内部加锁的"伪原子"，`is_lock_free()` 可能返回 false。原子性只保证"单次读写不被撕裂"，不保证"多步操作的整体性"；`a++; b++` 两步之间仍可被别的线程插空，要整体原子得用 CAS 或把数据打包。

## ① 概述：为什么需要原子操作与 data race <span class="badge badge-std">标准</span>

[第108章　memory_order：六种内存序（C++11）](../part09_concurrency/ch108_memory_order.md)

多线程同时读写同一普通变量而缺乏同步，即构成**数据竞争（data race）**——这是 C++ 标准中未定义行为（UB），结果不可预测，且会被编译器优化彻底破坏。`std::atomic<T>` 提供**不可分割**的读写与读-改-写（RMW）操作，并附带**内存序（memory order）**约束，使并发访问既安全又可推理。

> **示例 1** <span class="badge badge-exp">难度 ★★★★☆</span> · 概述：为什么需要原子操作与 data race
```cpp
// ① 没有原子保护的计数器：data race（UB）
#include <thread>
int bad_counter = 0;                 // 普通 int，多写并发 = data race
void worker_bad() { for (int i = 0; i < 100000; ++i) ++bad_counter; }
```

> **示例 2** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 概述：为什么需要原子操作与 data race
```cpp
// ① 用原子类型消除 data race
#include <atomic>
#include <thread>
std::atomic<int> good_counter{0};    // 原子 int，RMW 不可分割
void worker_good() { for (int i = 0; i < 100000; ++i) good_counter.fetch_add(1); }
```

- `[标准]`：C++11 引入 `<atomic>`；对原子对象的无数据竞争访问保证确定性结果。
- `[经验]`：只要有一个线程在**写**，所有线程对该变量都必须走原子/互斥路径，否则仍是 data race。

## 架构与流程图示（Mermaid）

释放-获取同步：生产者以 release 写 flag，消费者以 acquire 读 flag；一旦观测到，之前的写入对消费者可见。

```mermaid
flowchart LR
    P["生产者线程<br/>data = 1 （relaxed）<br/>flag.store(true, 释放)"]
    F["原子变量 flag"]
    C["消费者线程<br/>if flag.load(获取) 为真<br/>则读到 data == 1"]
    P -->|"释放 建立同步"| F
    F -->|"获取 观测到"| C
```

## ② std::atomic 模板与特化（atomic<int>/bool/指针） <span class="badge badge-std">标准</span>

`std::atomic<T>` 是模板；标准对常见类型提供特化与完整（fully-specialized）别名，以保证 lock-free 与最优布局：

> **示例 3** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 模板与特化
```cpp
// ② 主模板与标准特化别名
#include <atomic>
std::atomic<int>           a_i{0};   // 对应 atomic_int
std::atomic<bool>          a_b{false};
std::atomic<long long>     a_ll{0};
std::atomic<unsigned>      a_u{1};
```

> **示例 4** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 模板与特化
```cpp
// ② 标准提供的 typedef 别名（与上面等价、可读性更佳）
#include <atomic>
#include <cstddef>
std::atomic_int            ai{0};     // atomic<int>
std::atomic_bool           ab{false}; // atomic<bool>
std::atomic_size_t         asz{0};    // atomic<size_t>
```

> **示例 5** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 模板与特化
```cpp
// ② 整型原子可做的运算远多于 bool：bool 仅支持 store/load/exchange/test
#include <atomic>
int main() {
    std::atomic<bool> b{false};
    b.store(true);
    bool was = b.exchange(false);     // 返回旧值
    (void)was;
    return (int)b.load();
}
```

- `[标准]`：原子特化均为 **POD-like**，平凡可构造/可析构；`is_trivially_copyable_v<atomic<T>>` 为真。
- `[经验]`：优先用 `atomic_int` / `atomic_size_t` 等别名，避免与 `volatile int` 混淆（见 ⑮）。

## ③ load/store 的内存可见性 <span class="badge badge-std">标准</span>

`load()` 读、`store()` 写是原子的基本操作。它们都接受 `memory_order` 参数，默认 `memory_order_seq_cst`（顺序一致，最严格也最慢）：

> **示例 6** [难度 ★★☆☆☆] [主题：的内存可见性 <span class="badge badge-std">标准</span>]
```cpp
// ③ 默认顺序一致的内存序
#include <atomic>
std::atomic<int> x{0};
int read_x() { return x.load(); }                 // = load(seq_cst)
void write_x(int v) { x.store(v); }               // = store(seq_cst, v)
```

> **示例 7** [难度 ★★☆☆☆] [主题：的内存可见性 <span class="badge badge-std">标准</span>]
```cpp
// ③ 放宽内存序：relaxed 只保证原子性，不保证其他内存的可见顺序
#include <atomic>
std::atomic<int> c{0};
void inc_relaxed() { c.fetch_add(1, std::memory_order_relaxed); }
int  read_relaxed() { return c.load(std::memory_order_relaxed); }
```

> **示例 8** [难度 ★★☆☆☆] [主题：的内存可见性 <span class="badge badge-std">标准</span>]
```cpp
// ③ 生产者-消费者用 acquire/release 配对传递"数据已就绪"信号
#include <atomic>
#include <thread>
int payload = 0;
std::atomic<bool> ready{false};
void producer() { payload = 42; ready.store(true, std::memory_order_release); }
void consumer() { while (!ready.load(std::memory_order_acquire)) ; int v = payload; (void)v; }
```

- `[标准]`：`seq_cst` 在所有原子操作间建立单一全序；`acquire`/`release` 仅同步"成对的"同步点。
- `[微架构·x86-64 TSO]`：在 x86-64 上，acquire/release 常编译为普通 `mov`（不插 fence），只有 RMW 才需 `lock` 前缀——这是 x86 强内存模型（TSO）带来的红利。

## ④ exchange <span class="badge badge-std">标准</span>

`exchange(desired, order)` 原子地"写入新值并返回旧值"，是一个不可分割的读-改-写，常用于**状态切换 / 所有权转移**：

> **示例 9** [难度 ★★☆☆☆] [主题：<span class="badge badge-std">标准</span>]
```cpp
// ④ exchange：写入新值、原子返回旧值
#include <atomic>
std::atomic<int> flag{0};
int take_old() { return flag.exchange(1, std::memory_order_acq_rel); }  // 返回 0，留下 1
```

> **示例 10** [难度 ★★☆☆☆] [主题：<span class="badge badge-std">标准</span>]
```cpp
// ④ 用 exchange 实现简单的"一次性触发"哨兵
#include <atomic>
std::atomic<bool> fired{false};
bool try_fire() { return !fired.exchange(true); }   // 仅第一个调用者得到 true
```

> **示例 11** [难度 ★★☆☆☆] [主题：<span class="badge badge-std">标准</span>]
```cpp
// ④ 与 store 的区别：store 丢弃旧值；exchange 暴露旧值
#include <atomic>
std::atomic<int> a{7};
int old = a.exchange(99);    // old == 7, a 现在为 99
```

- `[标准]`：`exchange` 是可移植的 RMW 原语，等价于"非原子的 `tmp=o; o=v; return tmp;`"但不可分割。
- `[经验]`：需要"读旧值+写新值一气呵成"时，永远用 `exchange`/`fetch_*`，不要用 `load` 后 `store`。

## ⑤ compare_exchange_weak / compare_exchange_strong <span class="badge badge-std">标准</span>

CAS（Compare-And-Swap）是几乎所有无锁算法的基石：`compare_exchange(expected, desired)` 在 `*this == expected` 时写入 `desired` 并返回 `true`，否则把真实值写回 `expected` 并返回 `false`。

> **示例 12** <span class="badge badge-exp">难度 ★★☆☆☆</span> · compare_exchange_weak / compare_exchange_strong
```cpp
// ⑤ compare_exchange_strong：成功才替换，失败回写实际值到 expected
#include <atomic>
std::atomic<int> v{10};
bool set_if(int old_val, int new_val) {
    int e = old_val;
    return v.compare_exchange_strong(e, new_val, std::memory_order_acq_rel);
}
```

> **示例 13** <span class="badge badge-exp">难度 ★★☆☆☆</span> · compare_exchange_weak / compare_exchange_strong
```cpp
// ⑤ compare_exchange_weak：可能在无竞争时也虚假失败，必须配合循环
#include <atomic>
std::atomic<int> w{0};
void add_using_cas(int delta) {
    int e = w.load(std::memory_order_relaxed);
    while (!w.compare_exchange_weak(e, e + delta,
             std::memory_order_release, std::memory_order_relaxed)) {
        // e 已被更新为当前值，循环重试
    }
}
```

> **示例 14** <span class="badge badge-exp">难度 ★★☆☆☆</span> · compare_exchange_weak / compare_exchange_strong
```cpp
// ⑤ 两内存序重载：成功用 acq_rel，失败用 relaxed（失败时未改值，弱序即可）
#include <atomic>
std::atomic<int> z{0};
bool bump() {
    int e = 0;
    return z.compare_exchange_weak(e, e + 1,
               std::memory_order_acq_rel, std::memory_order_relaxed);
}
```

- `[标准]`：`weak` 允许虚假失败（在 LL/SC 架构上更自然），`strong` 不虚假失败但可能更慢。
- `[经验]`：循环里用 `weak`（重试成本低）；单次尝试用 `strong`。CAS 失败时 `expected` 被改写，务必在循环里复用。

## ⑥ fetch_add 等 RMW 操作 <span class="badge badge-std">标准</span>

读-改-写（Read-Modify-Write）族提供"读旧值 + 写新值"不可分割组合：`fetch_add` / `fetch_sub` / `fetch_and` / `fetch_or` / `fetch_xor`，以及前缀自增 `++`/`--`（对原子整型即 `fetch_add(1)`）：

> **示例 15** [难度 ★★☆☆☆] [主题：add 等 RMW 操作 <span class="badge badge-std">标准</span>]
```cpp
// ⑥ fetch_add / fetch_sub：返回旧值
#include <atomic>
std::atomic<int> c{0};
int prev = c.fetch_add(5);     // prev == 0, c 现在为 5
int prev2 = c.fetch_sub(2);    // prev2 == 5, c 现在为 3
```

> **示例 16** [难度 ★★☆☆☆] [主题：add 等 RMW 操作 <span class="badge badge-std">标准</span>]
```cpp
// ⑥ 位运算 RMW：原子按位与/或/异或
#include <atomic>
std::atomic<unsigned> bits{0xFF};
void clear_bit3() { bits.fetch_and(~(1u << 3)); }
void set_bit5()   { bits.fetch_or(1u << 5); }
void flip_bit0()  { bits.fetch_xor(1u); }
```

> **示例 17** [难度 ★★☆☆☆] [主题：add 等 RMW 操作 <span class="badge badge-std">标准</span>]
```cpp
// ⑥ 前缀 ++/-- 等价于 fetch_add(1)/fetch_sub(1)，但返回的是"新值"
#include <atomic>
std::atomic<int> n{0};
void demo() {
    int a = ++n;   // a == 1（新值），n == 1
    int b = n++;   // b == 1（旧值），n == 2  —— 注意后缀返回旧值
}
```

> **示例 18** [难度 ★★☆☆☆] [主题：add 等 RMW 操作 <span class="badge badge-std">标准</span>]
```cpp
// ⑥ fetch_add 对浮点原子也支持（C++20 起）
#include <atomic>
std::atomic<double> acc{0.0};
void add_double(double d) { acc.fetch_add(d, std::memory_order_relaxed); }
```

- `[标准]`：整型、指针、浮点（C++20）、`shared_ptr`（C++20）原子均提供相应 RMW。
- `[经验]`：RMW 返回的"旧值"常是构建无锁算法中最有用的中间量（如取出队列头）。

## ⑦ is_lock_free 与对齐要求 <span class="badge badge-std">标准</span>

`std::atomic<T>::is_always_lock_free`（静态）和 `is_lock_free()`（运行期）揭示该原子是否真的无锁。硬件原子指令要求对象**自然对齐**：

> **示例 19** [难度 ★★★☆☆] [主题：lockfree 与对齐要求 <span class="badge badge-std">标准</span>
```cpp
// ⑦ 运行期与编译期 lock-free 查询（C++17 起 is_always_lock_free）
#include <atomic>
#include <iostream>
void probe() {
    std::atomic<int> a;
    std::cout << a.is_lock_free() << '\n';            // 运行期查询
    std::cout << std::atomic<int>::is_always_lock_free << '\n';
    std::cout << std::atomic<long long>::is_always_lock_free << '\n';
}
```

> **示例 20** [难度 ★★☆☆☆] [主题：lockfree 与对齐要求 <span class="badge badge-std">标准</span>
```cpp
// ⑦ 对齐要求：原子对象必须按 T 的自然对齐，否则退化为加锁实现
#include <atomic>
#include <cstddef>
struct Aligned { alignas(std::atomic<int>) std::atomic<int> a; };
static_assert(alignof(std::atomic<int>) == alignof(int), "atomic<int> 对齐 = int");
```

> **示例 21** [难度 ★★☆☆☆] [主题：lockfree 与对齐要求 <span class="badge badge-std">标准</span>
```cpp
// ⑦ 宽类型往往不是 lock-free（64 位平台上一半以上的字宽会加锁）
#include <atomic>
#include <iostream>
void wide() {
    std::atomic<__int128> big;     // 多数平台非 lock-free，内部加锁
    std::cout << big.is_lock_free() << '\n';
}
```

- `[标准]`：`is_always_lock_free` 为真表示**保证**无锁；仅 `is_lock_free()` 为真表示当前平台无锁（但可移植性弱）。
- `[经验]`：不要对超大结构体用 `atomic<BigStruct>`——它几乎一定加锁（见 ⑯），那还不如直接用 `std::mutex`。

## ⑧ atomic_flag 与无锁自旋 <span class="badge badge-std">标准</span>

`std::atomic_flag` 是最小原子类型：**只有** `test_and_set` 和 `clear`，且**保证 lock-free**。它常被当作无锁自旋锁/Token 的基石。本节附真实汇编。

> **示例 22** [难度 ★★★☆☆] [主题：flag 与无锁自旋 <span class="badge badge-std">标准</span>]
```cpp
// 文件：Examples/_ch107_atomic_flag.cpp
// 行号：6
#include <atomic>
std::atomic_flag f = ATOMIC_FLAG_INIT;   // 必须以此宏初始化为 clear 状态
void acquire() { while (f.test_and_set(std::memory_order_acquire)) { } }
void release() { f.clear(std::memory_order_release); }
```

```asm
; 节选自 Examples/_ch107_atomic_flag.asm
; 编译：g++ -std=c++23 -O2 -S -masm=intel Examples/_ch107_atomic_flag.cpp -o _ch107_atomic_flag.asm
; 文件：Examples/_ch107_atomic_flag.cpp
; 行号：16（xchg 自旋）/ 28（clear）
_Z7acquirev:
	mov	edx, 1
.L2:
	mov	eax, edx
	xchg	al, BYTE PTR f[rip]     ; xchg 隐含 LOCK：原子交换并测试
	test	al, al
	jne	.L2                      ; 非 0 表示已被占用，继续自旋
	ret
_Z7releasev:
	mov	BYTE PTR f[rip], 0        ; 普通写即可释放（release 语义由内存序保证）
	ret
```

- `[实现·GCC15] [VERIFIED]`：`test_and_set` 编译为 `xchg al, [f]`——x86 上 `xchg` 对内存操作隐式带 `LOCK` 前缀，是真正原子的自旋测试。
- `[平台·x86-64]`：`atomic_flag` 占 1 字节、必 lock-free，是构建自旋原语的最小构件。

## ⑨ 原子指针 <span class="badge badge-std">标准</span>

`std::atomic<T*>` 提供原子指针，RMW 以**字节**为单位（受对象大小影响），`fetch_add`/`fetch_sub` 按 `sizeof(T)` 步进，并支持 `+=`/`-=` 与 `++`/`--`：

> **示例 23** [难度 ★★☆☆☆] [主题：原子指针 <span class="badge badge-std">标准</span>]
```cpp
// ⑨ 原子指针：fetch_add 按元素大小步进
#include <atomic>
int arr[8];
std::atomic<int*> p{arr};
int* next_slot() { return p.fetch_add(1); }   // 返回旧指针，p 前进一个 int
```

> **示例 24** [难度 ★★☆☆☆] [主题：原子指针 <span class="badge badge-std">标准</span>]
```cpp
// ⑨ 原子指针的 += 与后缀 ++
#include <atomic>
int buf[4];
std::atomic<int*> q{buf};
void advance() {
    q += 2;                 // 前进 2 个 int（= 8 字节）
    int* cur = q++;         // 返回当前，再前进（与 fetch_add(1) 语义一致）
    (void)cur;
}
```

> **示例 25** [难度 ★★☆☆☆] [主题：原子指针 <span class="badge badge-std">标准</span>]
```cpp
// ⑨ 用原子指针实现无锁单生产者游标
#include <atomic>
struct Node { int v; Node* next; };
Node* head = nullptr;
std::atomic<Node*> top{nullptr};
Node* pop_one() {
    Node* old = top.load(std::memory_order_acquire);
    while (old && !top.compare_exchange_weak(old, old->next,
             std::memory_order_acq_rel, std::memory_order_relaxed)) { }
    return old;
}
```

- `[标准]`：指针原子的 `fetch_add(n)` 等价于 `reinterpret_cast<char*>(p) + n*sizeof(T)`，差异由类型自动处理。
- `[经验]`：原子指针是写无锁链表/队列的核心，但要警惕 ⑭ 的 ABA 问题。

## ⑩ 原子操作与 data race 的 UB 边界 <span class="badge badge-std">标准</span>

原子对象本身并发访问安全，但**混用原子与非原子视图**越过 UB 边界：

> **示例 26** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 原子操作与 data race 的
```cpp
// ⑩ 合法：所有访问都走原子
#include <atomic>
#include <thread>
std::atomic<int> x{0};
void t1() { x.store(1); }
void t2() { (void)x.load(); }
```

> **示例 27** <span class="badge badge-exp">难度 ★★★★☆</span> · 原子操作与 data race 的
```cpp
// ⑩ 非法（UB）：同一对象既以原子又以非原子方式访问且存在并发写
#include <atomic>
#include <cstdint>
std::atomic<int> a{0};
void ub_alias() {
    int* raw = reinterpret_cast<int*>(&a);   // 取非原子别名
    *raw = 5;                                 // data race + 违反严格别名/原子访问规则 => UB
}
```

> **示例 28** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 原子操作与 data race 的
```cpp
// ⑩ 合法但危险：memory_order_relaxed 仍原子，只是不排序其他内存
#include <atomic>
std::atomic<int> c{0};
void relaxed_only_count() { c.fetch_add(1, std::memory_order_relaxed); }
```

- `[标准]`：仅当**所有**对对象的操作都通过原子类型（或 `memcpy`/位cast 的有限例外）进行时，才免于 data race。
- `[经验]`：不要 `reinterpret_cast` 掉原子性；不要对"本应是原子"的变量用普通 `int` 读写来"碰运气"。

## ⑪ [实现·GCC15]真实汇编：atomic<int>::fetch_add 编译为 lock xadd [实现·GCC15] [VERIFIED]

这是本章核心证据。`fetch_add(1)` 在 x86 上对应**带 LOCK 前缀的原子 RMW**。`-O0` 生成经典 `lock xadd`；`-O2` 对"加 1"特例优化为更短的 `lock add`，二者都是不可分割的原子指令。

> **示例 29** <span class="badge badge-exp">难度 ★★★☆☆</span> · [实现·GCC15]真实汇编：atomic<int>::fetch_add 编译为 lock xadd [实现·GCC15] [VERIFIED]
```cpp
// 文件：Examples/_ch107_fetch_add.cpp
// 行号：6
#include <atomic>
std::atomic<int> g{0};
void add_one() {
    g.fetch_add(1, std::memory_order_relaxed);   // 不可被线程抢占拆分
}
int read() {
    return g.load(std::memory_order_relaxed);
}
```

```asm
; 节选自 Examples/_ch107_fetch_add.asm
; 编译：g++ -std=c++23 -O0 -S -masm=intel Examples/_ch107_mangled.cpp -o _ch107_mangled.asm
; 文件：Examples/_ch107_mangled.cpp
; 行号：26（lock xadd，来自 _ch107_mangled.cpp 的 -O0 产物）
_Z7add_onev:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16
	mov	DWORD PTR -4[rbp], 1
	mov	DWORD PTR -8[rbp], 0
	mov	edx, DWORD PTR -4[rbp]
	lea	rax, g[rip]
	lock xadd	DWORD PTR [rax], edx    ; ← 真正的原子 RMW：读-改-写一气呵成
	nop
	add	rsp, 16
	pop	rbp
	ret
```

```asm
; 节选自 Examples/_ch107_fetch_add.asm
; 编译：g++ -std=c++23 -O2 -S -masm=intel Examples/_ch107_fetch_add.cpp -o _ch107_fetch_add.asm
; 文件：Examples/_ch107_fetch_add.cpp
; 行号：11（lock add，O2 对 +1 的特化）
_Z7add_onev:
	.seh_endprologue
	lock add	DWORD PTR g[rip], 1      ; ← O2 把 +1 的 fetch_add 优化为 lock add
	ret
_Z4readv:
	mov	eax, DWORD PTR g[rip]        ; load 普通 mov（x86 强内存模型无需额外 fence）
	ret
```

- `[实现·GCC15] [VERIFIED]`：`-O0` 是 `lock xadd`（通用 RMW）；`-O2` 识别"加 1"用更紧凑的 `lock add`。`lock` 前缀令 CPU 在指令期间断言 LOCK# 信号，锁定总线/缓存行，保证整条指令原子。
- `[平台·x86-64]`：`lock` 前缀可修饰 `add`/`xadd`/`cmpxchg` 等，是 x86 原子性的硬件根基；`load` 在 x86 上无需 `lock`（TSO 保证对齐字长的普通读可见最新写）。
- `[标准]`：mangled 符号 `_Z7add_onev` 即 C++ 名字改编后的 `add_one()`（`7`=名字长度，`v`=无参），证明该函数是普通链接符号，仅指令带 `lock`。

## ⑫ 用 CAS 实现自旋锁 <span class="badge badge-std">标准</span>

CAS 可构造无锁（或自旋）互斥。下面 `spinlock` 用 `atomic<bool>` + `compare_exchange_weak` 实现；成功地把 `false` 改成 `true` 即获得锁。本节附真实汇编。

> **示例 30** [难度 ★★★☆☆] [主题：用 CAS 实现自旋锁 <span class="badge badge-std">标准</span>]
```cpp
// 文件：Examples/_ch107_spinlock.cpp
// 行号：7
#include <atomic>
std::atomic<bool> locked{false};
void lock() {
    bool expected = false;
    while (!locked.compare_exchange_weak(expected, true,
             std::memory_order_acquire, std::memory_order_relaxed)) {
        expected = false;        // 失败：expected 已回写为 true，需复位再试
    }
}
void unlock() { locked.store(false, std::memory_order_release); }
```

```asm
; 节选自 Examples/_ch107_spinlock.asm
; 编译：g++ -std=c++23 -O2 -S -masm=intel Examples/_ch107_spinlock.cpp -o _ch107_spinlock.asm
; 文件：Examples/_ch107_spinlock.cpp
; 行号：17（lock cmpxchg 自旋）
_Z4lockv:
	sub	rsp, 24
	mov	edx, 1
.L3:
	xor	eax, eax
	mov	BYTE PTR 15[rsp], 0
	lock cmpxchg	BYTE PTR locked[rip], dl   ; ← CAS 原子：若 locked==0 则置 1
	jne	.L3                                  ; 失败则跳回 .L3 重试（自旋）
	add	rsp, 24
	ret
_Z6unlockv:
	mov	BYTE PTR locked[rip], 0              ; 释放：store(false, release)
	ret
```

> **示例 31** [难度 ★★☆☆☆] [主题：用 CAS 实现自旋锁 <span class="badge badge-std">标准</span>]
```cpp
// ⑫ RAII 封装自旋锁，避免忘记 unlock
#include <atomic>
struct spinlock {
    std::atomic<bool>& lk;
    explicit spinlock(std::atomic<bool>& b) : lk(b) {
        bool e = false;
        while (!lk.compare_exchange_weak(e, true,
                 std::memory_order_acquire, std::memory_order_relaxed)) e = false;
    }
    ~spinlock() { lk.store(false, std::memory_order_release); }
};
```

- `[实现·GCC15] [VERIFIED]`：CAS 自旋编译为 `lock cmpxchg` + `jne` 回跳——这正是无锁栈/队列、引用计数的底层原语。
- `[经验]`：自旋锁适合**临界区极短**、不希望线程切上下文的场景；临界区长时换 `std::mutex`（会睡眠而非空转）。

## ⑬ 无锁栈雏形（push） <span class="badge badge-std">标准</span>

用 `atomic<Node*>` 头指针 + CAS 即可写出无锁 push：循环读取当前头，构造新节点指向头，再 CAS 把头换成新节点。

> **示例 32** [难度 ★★☆☆☆] [主题：无锁栈雏形（push） <span class="badge badge-std">标准</span>]
```cpp
// ⑬ 无锁栈 push（CAS 循环，注意仍受 ABA 限制，见 ⑭）
#include <atomic>
struct Node { int val; Node* next; };
std::atomic<Node*> head{nullptr};
void push(int v) {
    Node* n = new Node{v, nullptr};
    Node* old = head.load(std::memory_order_relaxed);
    do {
        n->next = old;
    } while (!head.compare_exchange_weak(old, n,
             std::memory_order_release, std::memory_order_relaxed));
}
```

> **示例 33** [难度 ★★☆☆☆] [主题：无锁栈雏形（push） <span class="badge badge-std">标准</span>]
```cpp
// ⑬ 配套的（可能不安全的）pop 雏形：演示 CAS 在链表上的用法
#include <atomic>
struct Node2 { int val; Node2* next; };
std::atomic<Node2*> top{nullptr};
int pop_unsafe() {
    Node2* old = top.load(std::memory_order_acquire);
    while (old && !top.compare_exchange_weak(old, old->next,
             std::memory_order_acq_rel, std::memory_order_relaxed)) { }
    int r = old ? old->val : -1;
    // 注意：真实实现需处理 ABA 与内存回收，此处仅演示 CAS 结构
    return r;
}
```

- `[标准]`：此 push 是无锁（lock-free）的——总有线程能推进；但它不是**无等待（wait-free）**。
- `[经验]`：无锁 ≠ 无 bug。pop 的"读 old->next 再用"在并发下会触发 ⑭ 的 ABA 问题，生产代码请用带标签指针或 hazard pointer。

## ⑭ ABA 问题预告 <span class="badge badge-std">标准</span>

CAS 只比较"值相等"，不感知"中间发生过什么"。若指针 `A→B→A`（被弹出又分配同地址），CAS 误以为无变化而成功，却带着失效的 `next` 链路——这就是 **ABA**。第111章（无锁编程进阶）会给出带**标签指针（tagged pointer）**、`hazard pointer`、RCU 等完整解法。本章先记住结论：

> **示例 34** [难度 ★★☆☆☆] [主题：问题预告 <span class="badge badge-std">标准</span>]
```cpp
// ⑭ ABA 示意：CAS 无法发现中间被改回"相同值"
#include <atomic>
struct N { int v; N* next; };
std::atomic<N*> head{nullptr};
void buggy_pop() {
    N* old = head.load();
    N* next = old->next;            // 假设此刻另一线程把它 A->B->A
    // 下面 CAS 看到 head 仍是 old(A)，成功——但 next 已是陈旧链路
    head.compare_exchange_strong(old, next);   // 危险！
}
```

- `[标准]`：CAS 语义仅保证"比较-交换"原子，不做"历史变更"追踪。
- `[经验]`：凡是链表无锁结构，必须正视 ABA；不要以为"用了 atomic 就万事大吉"（详见第111章）。

## ⑮ 与 volatile 的本质区别 <span class="badge badge-exp">经验</span>

`volatile` 只禁止编译器对该变量的重排/缓存，**不提供原子性、不生成 `lock`、不建立线程间 happens-before**。`volatile++` 在汇编里是普通 `mov/add/mov` 三条指令，可被线程抢占；`atomic++` 是单条 `lock add`。二者不可互换。

> **示例 35** <span class="badge badge-exp">难度 ★★★☆☆</span> · 与 volatile 的本质区别 [经验]
```cpp
// 文件：Examples/_ch107_volatile.cpp
// 行号：6
#include <atomic>
volatile int v = 0;
std::atomic<int> a{0};
void volatile_inc() { v++; }                       // 非原子！
void atomic_inc()  { a.fetch_add(1, std::memory_order_relaxed); }  // 原子
```

```asm
; 节选自 Examples/_ch107_volatile.asm
; 编译：g++ -std=c++23 -O2 -S -masm=intel Examples/_ch107_volatile.cpp -o _ch107_volatile.asm
; 文件：Examples/_ch107_volatile.cpp
; 行号：11（volatile 三指令，无 lock）/ 23（atomic 单条 lock add）
_Z12volatile_incv:
	mov	eax, DWORD PTR v[rip]      ; 1) 读
	add	eax, 1                     ; 2) 改
	mov	DWORD PTR v[rip], eax      ; 3) 写 —— 三步之间可被抢占 => 非原子
	ret
_Z10atomic_incv:
	lock add	DWORD PTR a[rip], 1   ; 单条原子 RMW，不可分割
	ret
```

- `[实现·GCC15] [VERIFIED]`：证据确凿——`volatile_inc` 编译为 `mov/add/mov` 三条独立指令，没有任何 `lock`；`atomic_inc` 编译为单条 `lock add`。
- `[经验]`：C++ 中 `volatile` **不能**用于线程同步（C++20 起 `volatile` 上的 `++` 已被弃用并告警）。跨线程同步只用 `std::atomic` 或 `std::mutex`。
- `[标准]`：`volatile` 的语义是"防止编译器优化掉对内存映射 I/O 的访问"，与并发原子性无关。

## ⑯ 常见误用（用 atomic 保护大结构体） <span class="badge badge-exp">经验</span>

`std::atomic<T>` 要求 `T` 是平凡可拷贝的；试图用原子"保护"大结构体，会得到加锁的、慢的、且易误用的实现——还不如直接 `std::mutex`。

> **示例 36** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 常见误用
```cpp
// ⑯ 误用：把大结构体塞进 atomic（往往加锁，且每次读写都是整块复制）
#include <atomic>
struct Big { char blob[256]; };
std::atomic<Big> shared;                 // 编译可通过，但多为 lock-based，慢
void wrong() { Big b = shared.load(); }  // 整块 256 字节原子复制，昂贵
```

> **示例 37** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 常见误用
```cpp
// ⑯ 正确：用互斥量保护大结构体，或只原子化其中真正需要同步的字段
#include <atomic>
#include <mutex>
struct State { int ready = 0; double result = 0.0; };
State g_state;
std::mutex g_mtx;
void correct_publish(double r) {
    std::lock_guard<std::mutex> lk(g_mtx);
    g_state.result = r;
    g_state.ready = 1;
}
// 用原子"标志位"发布，结构体本体由互斥保护
std::atomic<int> g_ready{0};
```

> **示例 38** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 常见误用
```cpp
// ⑯ 另一误用：忘记 compare_exchange 会改写 expected，循环外用旧值
#include <atomic>
std::atomic<int> x{0};
bool bug_cas() {
    int e = 0;
    bool ok = x.compare_exchange_strong(e, 1);
    // 若失败，e 已变；此处若再依赖 e==0 就错
    return ok;
}
```

- `[经验]`：原子适合"小、标量、高频"的同步点（计数器、标志、指针）；大对象用 `std::mutex`。
- `[实现·GCC15]`：当 `sizeof(T)` 超过平台 lock-free 阈值（常见 8/16 字节），`atomic<T>` 退化为内部加锁（可查 `is_lock_free()`）。

## ⑰ 性能注意：伪共享（false sharing）与 cache line padding [平台·x86-64]

两个不同原子变量落在**同一缓存行**时，不同核反复使对方缓存行失效，性能骤降——这叫**伪共享**。用 `alignas(std::hardware_destructive_interference_size)` 把它们隔开。

> **示例 39** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 性能注意：伪共享与 cache line padding
```cpp
// ⑰ 伪共享：相邻两个原子在线程间乒乓，互相 invalid 缓存行
#include <atomic>
std::atomic<int> a_shared{0};
std::atomic<int> b_shared{0};     // 很可能和 a 同缓存行 => false sharing
void writer_a() { for (int i=0;i<1000000;++i) a_shared.fetch_add(1); }
void writer_b() { for (int i=0;i<1000000;++i) b_shared.fetch_add(1); }
```

> **示例 40** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 性能注意：伪共享与 cache line padding
```cpp
// ⑰ 修复：按缓存行大小对齐，避免两个热点落同一行
#include <atomic>
#include <new>
struct Padded {
    alignas(std::hardware_destructive_interference_size) std::atomic<int> a{0};
    alignas(std::hardware_destructive_interference_size) std::atomic<int> b{0};
};
Padded g_p;
```

- `[平台·x86-64]`：`std::hardware_destructive_interference_size` 通常为 64（典型缓存行）。对齐后 `a` 与 `b` 各占独立缓存行，跨核写不再互相 invalid。
- `[经验]`：perf 火焰图看到大量 `lock` 指令却逻辑简单时，先怀疑伪共享；padding 是无锁高并发的常见提速点。

## ⑱ 宽原子与 __int128 <span class="badge badge-std">标准</span>

128 位整数 `__int128` 可作为 `std::atomic<__int128>` 使用，但在多数 64 位平台**不是 lock-free**（需内部加锁），除非目标支持 `cmpxchg16b` 双字 CAS。

> **示例 41** [难度 ★★☆☆☆] [主题：宽原子与 int128 <span class="badge badge-std">标准</span>]
```cpp
// ⑱ 128 位原子：可移植但多数平台非 lock-free
#include <atomic>
std::atomic<__int128> wide{0};
void set_wide(__int128 v) { wide.store(v, std::memory_order_release); }
__int128 get_wide() { return wide.load(std::memory_order_acquire); }
```

> **示例 42** [难度 ★★☆☆☆] [主题：宽原子与 int128 <span class="badge badge-std">标准</span>]
```cpp
// ⑱ 用 128 位原子做"序列号 + 数据"的带标签指针（缓解 ABA，见 ⑭）
#include <atomic>
#include <cstdint>
struct TaggedPtr {
    void* ptr;
    std::uint64_t tag;     // 每次 CAS 自增，地址复用也无法骗过比较
};
std::atomic<__int128> head_pair{0};   // 把 (ptr,tag) 打包进 128 位一次性 CAS
```

> **示例 43** [难度 ★★☆☆☆] [主题：宽原子与 int128 <span class="badge badge-std">标准</span>]
```cpp
// ⑱ 检查平台是否 lock-free
#include <atomic>
#include <iostream>
void probe_wide() {
    std::cout << std::atomic<__int128>::is_always_lock_free << '\n';
}
```

- `[标准]`：`std::atomic<__int128>` 是扩展类型，依赖编译器/平台；是否 lock-free 用 `is_lock_free()` 实测。
- `[经验]`：需要"双字原子 CAS"时优先查 `is_always_lock_free`；若不支持，退化为带互斥的 128 位组合或改用 hazard pointer。

## ⑲ 调试/验证手段（ThreadSanitizer） [平台·x86-64]

数据竞争难以靠肉眼发现。GCC/Clang 的 **ThreadSanitizer（tsan）** 在运行期插桩检测 data race，是无锁/并发代码的必备验证工具。

> **示例 44** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 调试/验证手段
```cpp
// ⑲ 被测代码：故意的 data race（用于演示 tsan 报告）
#include <thread>
int race = 0;                            // 普通 int，并发写
void bad() { for (int i=0;i<100000;++i) ++race; }
int main() {
    std::thread a(bad), b(bad);
    a.join(); b.join();
    return race;                          // tsan 会在此类访问上报 data race
}
```

> **示例 45** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 调试/验证手段
```cpp
// ⑲ 修复后：用原子，tsan 不再报竞争
#include <atomic>
#include <thread>
std::atomic<int> safe{0};
void good() { for (int i=0;i<100000;++i) safe.fetch_add(1); }
int main() {
    std::thread a(good), b(good);
    a.join(); b.join();
    return safe.load();
}
```

```bash
# ⑲ 编译并运行 tsan（GCC/Clang 均支持 -fsanitize=thread）
g++ -std=c++23 -O1 -g -fsanitize=thread _ch107_tsan_demo.cpp -o tsan_demo
./tsan_demo      # 竞争版本会打印 WARNING: ThreadSanitizer: data race
```

- `[平台·GCC13/Clang]`：`-fsanitize=thread` 注入race 检测；建议用 `-O1 -g` 兼顾速度与可读栈。
- `[经验]`：无锁算法写完**必须**跑 tsan + 压力测试；tsan 不保证发现所有问题，但能抓绝大多数真实 data race。

## ⑳ 速查表 <span class="badge badge-std">标准</span>

**练习题**（已升级为「真实场景 + 引用参考」框架：保留原考察技能，场景改写为工程应用）

1. **真实场景：用 `std::atomic<int>` 计数避免数据竞争。** 你多线程 `++` 不再丢更新。请说明保证。
   - <span class="badge badge-std">标准</span> 对原子对象的并发访问不产生数据竞争；RMW 操作整体原子完成。
   - <span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[atomics]（原子操作免数据竞争）；cppreference "std::atomic" 词条。

2. **真实场景：默认内存顺序是 `seq_cst`，可能比 필요 更慢。** 你确认单变量无需跨变量顺序。请说明默认。
   - <span class="badge badge-std">标准</span> 未指定 memory_order 时，原子操作按 `memory_order_seq_cst` 执行（全序、最安全但最贵）。
   - <span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[atomics.order]（seq_cst 默认）；cppreference "std::memory_order" 词条。

3. **真实场景：`fetch_add` 是原子读-改-写。** 你用它做无锁计数器。请说明。
   - <span class="badge badge-std">标准</span> fetch_add/exchange 等是原子 RMW；在多线程竞争下结果正确且单一。
   - <span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[atomics]（RMW 操作）；cppreference "std::atomic::fetch_add" 词条。

> **示例 46** [难度 ★★☆☆☆] [主题：速查表 <span class="badge badge-std">标准</span>]
```cpp
// ⑳ 最小可编译回顾：把本章要点串成一段代码
#include <atomic>
std::atomic<int>   cnt{0};
std::atomic<bool>  flag{false};
std::atomic_flag   f = ATOMIC_FLAG_INIT;
void quick() {
    cnt.fetch_add(1, std::memory_order_relaxed);   // RMW
    int old = cnt.exchange(0);                      // 读旧写新
    int e = 0;
    cnt.compare_exchange_weak(e, 1,                 // CAS
        std::memory_order_acq_rel, std::memory_order_relaxed);
    flag.store(true, std::memory_order_release);    // 发布
    (void)flag.load(std::memory_order_acquire);     // 获取
    while (f.test_and_set(std::memory_order_acquire)) { }  // 自旋
    f.clear(std::memory_order_release);
    (void)old;
}
```

| 操作 | 函数 | 是否 RMW | x86-64 典型指令 |
|---|---|---|---|
| 读 | `load` | 否 | `mov` |
| 写 | `store` | 否 | `mov` |
| 交换 | `exchange` | 是 | `xchg` |
| 加/减 | `fetch_add`/`fetch_sub` | 是 | `lock xadd` / `lock add` |
| 位运算 | `fetch_and`/`or`/`xor` | 是 | `lock and` 等 |
| 比较交换 | `compare_exchange` | 是 | `lock cmpxchg` |
| 测试置位 | `atomic_flag::test_and_set` | 是 | `xchg`（隐含 LOCK） |

- `[标准]`：所有原子操作默认 `seq_cst`；按需降级到 `acquire`/`release`/`relaxed` 可减 fence。
- `[经验]`：能用 `atomic_flag` 就不上互斥；临界区长用 `std::mutex`；写完无锁代码必跑 ThreadSanitizer（见 ⑲）。
- `[平台·x86-64]`：x86 是强内存模型，`load`/`store` 编译为普通 `mov`，只有 RMW 需要 `lock` 前缀——这是与弱内存架构（ARM）性能差异的根源。

> **示例 47** [难度 ★★☆☆☆] [主题：速查表 <span class="badge badge-std">标准</span>]
```
┌───────────────┬───────────────────────────┬──────────────────────┐
│ 同步手段       │ 适用场景                   │ 备注                  │
├───────────────┼───────────────────────────┼──────────────────────┤
│ atomic 标量    │ 计数器/标志/指针 CAS        │ lock-free，最快        │
│ atomic_flag    │ 自旋锁/Token              │ 必 lock-free          │
│ std::mutex     │ 长临界区/大对象           │ 会睡眠，安全简单       │
│ 无锁结构       │ 高并发链表/队列           │ 需处理 ABA（见 ⑭）     │
└───────────────┴───────────────────────────┴──────────────────────┘
```

## ㉒ 历史纵深·真实产业坐标·生产踩坑·与标准的互动

> 本节为 P0-15 全库深度升维大波次之一：压实历史出处、真实产业坐标、生产级踩坑与「本特性与 C++ 标准」的互动。引用链接列于 ㉒.5。

### ㉒.1 历史渊源补强：从硬件原子到 C++ 内存模型

<span class="badge badge-history">史</span> C++ 原子（`<atomic>`）随 **C++11** 进入标准，是 C++ 第一次把「原子类型 + 内存序」写进语言——此前多线程 C++ 处于「未定义行为」灰色地带，程序员只能靠编译器内建（`__sync_*`）或平台汇编。<span class="badge badge-history">史</span> 更底层：C++11 的内存模型与原子设计深受 **Hans Boehm、Sarita Adve、Mark Batty（x86/POWER/ARM 弱内存模型的形式化）** 影响，并由 **P0558R1（Fixing the C++ Memory Model，2017）** 修正了一批准许加宽/窄化破坏原子性的措辞缺陷；**C++20 的 P0020R6** 又补上**浮点原子（`atomic<float/double>` 的 `fetch_add` 等）**，服务 HPC 并行浮点累加。<span class="badge badge-anecdote">轶</span> 早期 C++11 还不允许对「普通 `int` 做原子访问」，直到 **C++20 `std::atomic_ref`（P0019）** 才允许把已存在的对象按原子方式访问，而不必把它声明成 `atomic<T>`。<span class="badge badge-comment">评</span> 原子是「无锁编程」的地基，但它**不保证无锁**——`is_lock_free()` 可能为 false（如某些平台对大于机器字的类型退化为内部锁）。

### ㉒.2 真实工程坐标：原子活在哪些产品里

下表把「原子」拉成「无锁并发的最小单元」。

| 领域/类别 | 代表系统·生态 | 它承担的角色 | 规模·行业地位 | 备注 / 标准互动 |
| --- | --- | --- | --- | --- |
| 操作系统 / 用户态库 | Linux 内核（`atomic_t`/`atomic64_t` 同源）/ `liburing` / DPDK | 无锁计数与标志位（内核用自有一套） | 一切并发软件地基 | 语义与 C++11 原子同源 |
| 编译器 / 运行时 | LLVM（`RefCountBase` 思路） | 引用计数 / 线程安全懒初始化标志 / 统计计数器 | 编译基础设施 | 原子用于内部并发 |
| 游戏引擎 | Unreal / Unity 原生侧 | 无锁任务队列 / 帧间标志·状态机（`atomic<bool/flag>`） | 实时系统 | 避互斥锁开销 |
| 高性能网络 | Seastar / folly | 无锁 ring buffer / 连接计数器 / hazard pointer 底层 | 低尾延迟标配 | 无锁结构皆依赖原子 |
| 汽车 / 安全攸关 | AUTOSAR Adaptive（ASIL-D 多核 ECU） | 核间免锁状态同步与看门狗握手 | ISO 26262 功能安全 | 原子是并发原语地基 |
| 数据库 / 存储 | RocksDB（`SequenceNumber`）/ ClickHouse | 原子递增 / memtable 引用计数 / 查询统计 | LSM 并发读支撑 | 引用计数靠原子 |

> **表注（㉒.2）**：上表把「原子」拉成「无锁并发的最小单元」。注意 Linux 内核一行：它不能用 `std::atomic`（那是用户态库），却用语义同源的 `atomic_t`/`atomic64_t`——说明原子是跨用户态 / 内核的通用并发原语，只是接口不同。AUTOSAR Adaptive 与 RocksDB / ClickHouse 两行则点出原子的两个极端用途：功能安全（规避锁的不可预测阻塞）与高并发（引用计数 / 序列号）。

**一条判读**：用 `std::atomic` 的判据是「有一个被多核并发读写的小状态（计数 / 标志 / 句柄），且不想付锁开销」。引用计数（LLVM / RocksDB）、标志位（游戏 / 网络）、序列号（存储）都符合 → 用原子拿无锁与确定性；但当操作变大（要保护一段临界区）或需要互斥语义时，原子不够，要 mutex / RCU（见 ch109–112）。规则：单变量并发 → 原子；多变量不变式 → 锁或更高层原语。

### ㉒.3 生产踩坑：原子的常见误用

- **误以为 `atomic` 一定无锁**：`atomic<LargeStruct>` 在多数平台会退化为内部加锁（`is_lock_free()==false`），并发写反而更慢且可能惊现「看似原子其实不是」的幻觉——超大类型请拆成可原生原子的小字段或用 seqlock。
- **滥用 `memory_order_relaxed` 导致看不到关联写**：把本该 `release/acquire` 的数据发布用 `relaxed` 做，会被编译器/CPU 重排，另一线程读到「指针已置位但数据还没写」——典型是并发栈/队列的无锁 bug。
- **`atomic` 上自旋忙等烧 CPU**：用 `while(flag.load()==0);` 自旋等待会占满核心；应配合 `std::this_thread::yield()`/`pause` 指令或改用条件变量/ futex。
- **混用原子与非原子访问同一变量**：对同一变量既用 `atomic<T>` 又用裸 `T` 访问，结果未定义；要么全原子，要么全非原子并由锁保护。

### ㉒.4 与标准的互动：原子与 C++ 标准的演进

<span class="badge badge-history">史</span> 原子随 **C++11** 引入，奠定内存模型；**C++17 的 P0558R1** 修复了内存模型措辞缺陷（影响所有原子操作的正确性基础）；**C++20** 是原子的大年——**P0020R6 引入浮点原子**（`fetch_add` 等，服务 HPC），**P0019 引入 `std::atomic_ref`**（对已存在对象做原子访问）；**C++26** 继续推进 hazard pointer/RCU 标准化（P1122/P2530），其底层亦建立在原子之上。与 WG21 方向一致：把「硬件原子 + 形式化内存模型」持续下沉为标准可移植抽象。

- <span class="badge badge-history">史</span> **浮点原子修订链**：**P0020** 历经 **R0（2015-10）→ R3 → R4 → R5 → R6（2017-11-10）**，由 H. Carter Edwards 等提案，最终随 C++20 采纳 `atomic<float/double>`（`fetch_add` 等），服务 HPC 并行浮点累加；可于 <https://wg21.link/p0020> 逐版追溯。
- <span class="badge badge-history">史</span> **`atomic_ref` 修订链**：**P0019** 从 **R0 → R3 → R7 → R8（2018）** 演进，最终进 C++20，提供对已存在对象做原子访问的能力（特性宏 `__cpp_lib_atomic_ref`=201806L）；<https://wg21.link/p0019>。

### ㉒.5 权威引用

- [cppreference: std::atomic](https://en.cppreference.com/w/cpp/atomic/atomic) — 原子类型的成员、内存序与 `is_lock_free` 语义。
- [WG21 P0558R1 — Fixing the C++ Memory Model（2017）](https://wg21.link/p0558) — 修正原子/内存模型的措辞缺陷，是 C++17 原子正确性的基础。
- [WG21 P0020R6 — Floating Point Atomic（C++20）](https://wg21.link/p0020) — 在 C++20 引入 `atomic<float/double>` 的提案。
- [cppreference: std::atomic_ref (C++20)](https://en.cppreference.com/w/cpp/atomic/atomic_ref) — C++20 对已有对象做原子访问的设施。

## 附录 A：WG21 提案与工业实现对比 [B: Principle / F: Industry]

atomic 从 TR1 (2005) 到 C++20 的 15 年演化，是并发编程从"平台相关"到"标准可移植"的缩影：

| 版本 | 关键内容 | 提案 |
|---|---|---|
| C++11 | std::atomic<T>, 6 memory_order, is_lock_free | N2427 (Boehm, 2007) |
| C++14 | atomic_init (废弃, 改用构造函数) | N3660 |
| C++17 | is_always_lock_free, atomic<T>::value_type | P0558R1 |
| C++20 | atomic_ref<T>, atomic<shared_ptr<T>>, atomic_flag::wait | P0019R8, P1643R1 |
| C++23 | 无重大 atomic 变更 | — |

> **示例 48** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 附录 A：WG21 提案与工业实现对
```cpp
#include <iostream>
#include <atomic>
int main() {
    std::cout << "Industrial atomic usage:\n";
    std::cout << "folly::AtomicHashMap: lock-free hash map, 10M ops/s on 16 cores\n";
    std::cout << "ClickHouse: atomic_flag for spinlock, skip mutex for sub-100ns sections\n";
    std::cout << "LLVM: atomic<unsigned> for reference counting (in LLVM 17+, migrated from manual atomics)\n";
    std::cout << "Chromium: base::AtomicRefCount uses atomic<int> with acq_rel semantics\n";
    std::cout << "Linux kernel: atomic_t (C) is the API that inspired C++ std::atomic design\n";
    return 0;
}
```

## 附录 B：底层汇编与性能证据 [E: Low-level / G: Performance]

> **示例 49** <span class="badge badge-exp">难度 ★★★☆☆</span> · 附录 B：底层汇编与性能证据 [E: Low-level / G: Performance]
```cpp
// GCC -O2 x86-64 atomic 操作的汇编对比
#include <atomic>
#include <iostream>

std::atomic<int> x{0};

void atomic_store() { x.store(42, std::memory_order_relaxed); }
// asm: mov DWORD PTR [x], 42  (普通 mov，x86 上对齐的 int store 天然原子)

void atomic_fetch_add() { x.fetch_add(1, std::memory_order_seq_cst); }
// asm: lock add DWORD PTR [x], 1 (LOCK prefix 保证多核原子性)

void atomic_cas() { int expected = 0; x.compare_exchange_strong(expected, 1); }
// asm: mov eax, 0; lock cmpxchg DWORD PTR [x], 1

int main() {
    atomic_store();
    atomic_fetch_add();
    atomic_cas();
    std::cout << "x86 atomic costs (approximate):\n";
    std::cout << "relaxed store:  ~1ns (plain mov)\n";
    std::cout << "seq_cst RMW:    ~20ns (LOCK prefix + mfence)\n";
    std::cout << "CAS loop:       ~30-50ns per iteration (LOCK cmpxchg + branch)\n";
    std::cout << "ARM: LDREX/STREX for RMW, ~5-10ns; x86 LOCK prefix is ~10-20ns\n";
    std::cout << "Key: x86's TSO (Total Store Order) makes acquire=free, release=free.\n";
    return 0;
}
```

## 附录 D：面试与设计权衡 [J: Learning / H: Design]

> **示例 50** <span class="badge badge-exp">难度 ★★★★☆</span> · 附录 D：面试与设计权衡 [J: Learning / H: Design]
```
面试高频:
Q: std::atomic<int> 一定能做到 lock-free 吗？
A: 标准不保证，但实际: GCC/Clang/MSVC 在 x86/ARM 上对齐的 int 都是 lock-free。
   用 is_lock_free() 或 is_always_lock_free 编译期检查。

Q: atomic 和 volatile 的本质区别？
A: atomic = thread-safe (原子性 + happens-before); volatile = optimizer bypass (仅禁止寄存器缓存)。
   两者正交：可以同时使用 atomic<volatile int>。

Q: 为什么 CAS 循环 (compare_exchange_weak) 比锁好？
A: CAS 是用户态原子操作(~20ns)；mutex 涉及系统调用 + 上下文切换(~1-10us)。
   但 CAS 循环在高竞争下退化 (spin 浪费 CPU)，此时 mutex 更好 (让出 CPU)。

设计权衡:
- lock-free 保证至少一个线程推进; wait-free 保证每个线程都推进
- 无锁队列: MPMC (多生产者多消费者) 比 MPSC/SPSC 复杂 10×
- is_lock_free: 检查当前硬件是否支持，但编译器可能降级为互斥锁
```

## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第108章](../part09_concurrency/ch108_memory_order.md) | 键值查找/缓存 | 本章提供概念，第108章提供实现 |
| [第108章](../part09_concurrency/ch108_memory_order.md) | 无锁队列/计数器 | 本章提供概念，第108章提供实现 |
| [第108章](../part09_concurrency/ch108_memory_order.md) | 资源管理/事务回滚 | 本章提供概念，第108章提供实现 |
| [第109章](../part09_concurrency/ch109_fence.md) | 线程安全数据结构 | 本章提供概念，第109章提供实现 |
| [第110章](../part09_concurrency/ch110_lockfree.md) | 共享所有权/图结构 | 本章提供概念，第110章提供实现 |

## 相关章节（交叉引用）

- **同模块兄弟（part09 并发）**：[第108章　memory_order：六种内存序（C++11）](../part09_concurrency/ch108_memory_order.md)）
- **同模块兄弟（part09 并发）**：[第109章 内存屏障与 fence](../part09_concurrency/ch109_fence.md)
- **同模块兄弟（part09 并发）**：[第110章　无锁编程：lock-free / wait-free（C++11）](../part09_concurrency/ch110_lockfree.md)）
- **同模块兄弟（part09 并发）**：[第111章　ABA 问题与解决（C++11）](../part09_concurrency/ch111_aba.md)）
- **同模块兄弟（part09 并发）**：[第112章　Hazard Pointer 与 RCU（C++11/实践）](../part09_concurrency/ch112_hazard_rcu.md)）
- **同模块兄弟（part09 并发）**：[第113章　协程 coroutine：promise / awaiter（C++20）](../part09_concurrency/ch113_coroutine.md)）
- **硬件底座（part03）**：[第30章 volatile / atomic 与硬件寄存器](../part03_language/ch30_volatile.md)—— volatile/atomic 与硬件寄存器的内存可见性语义，是原子操作的语言层地基
- **多线程落地（part07）**：[第93章　线程与异步：thread / future / async](../part07_stl/ch93_thread_async.md)—— 原子操作在线程/异步同步中的典型用法

## 附录 G：工业原子操作与 lock-free 数据结构

| 库/项目 | 数据结构 | 原子序 | 典型场景 | 源码 |
|---------|---------|--------|---------|------|
| **folly**（github.com/facebook/folly） | `MPMCQueue<T>` | 多生产者多消费者无锁队列（CAS） | Meta 服务间通信、日志管线（百万 msg/s） | `folly/MPMCQueue.h` — `std::atomic<Slot>` + `compare_exchange_strong` |
| **Boost.Lockfree**（github.com/boostorg/lockfree） | `spsc_queue<T>` | 单生产者单消费者环形缓冲 | 音视频流、事件驱动（零锁，纯原子序） | `include/boost/lockfree/spsc_queue.hpp` |
| **DPDK**（github.com/DPDK/dpdk） | `rte_ring` | 多生产者多消费者无锁环 | 网络包处理（千万 PPS），L2/L3 转发 | `lib/ring/rte_ring.h` — CAS + 精细 `memory_order` |
| **Google `absl::Mutex`**（github.com/abseil/abseil-cpp） | 混合锁 | `futex` 内核睡眠 + `atomic` 用户态快速路径 | 低竞争时零系统调用（仅 `compare_exchange_weak` 自旋） | `absl/synchronization/mutex.h` |
| **Linux RCU**（kernel.org） | `rcu_read_lock()` / `rcu_dereference()` | 读端零原子操作（仅编译器屏障） | 内核路由表、文件系统 VFS、网络协议栈 | `include/linux/rcupdate.h` |

**底层深度**：x86 强序模型（TSO）使 `memory_order_seq_cst` 的代价远高于 ARM/Power。x86 上 `seq_cst store` → `mov` + `mfence`（≈33–50 周期），而 `release store` → 仅 `mov`（x86 store 自带 release 语义）。ARMv8 上 `seq_cst` → `stlr` + `dmb ish`（全屏障，≈10–20 周期），`release` → `stlr`（仅 store-release）。在 lock-free 队列的热路径上，将 `seq_cst` 降为 `acquire/release` 可将吞吐从 ~50M ops/s 提升至 ~300M ops/s（folly MPMCQueue 基准）。

## 附录 I：工业实战复盘（I.实战）[I: Practice]

### 工业案例（真实可查证）

- **`is_lock_free` 的跨平台假象**：`std::atomic<std::shared_ptr>` 在 x86-64 Glibc 上是无锁的，在 ARM32/MIPS 上内部用 `std::mutex` 保护——`is_always_lock_free` 为 `false`，却无编译警告。生产上加 `static_assert(is_always_lock_free)` 在目标平台 CI 矩阵上提前暴露。
- **`atomic<T>` 的对齐及伪分享**：两个 `atomic<int>` 若落在同一 64B 缓存行，线程各自写时 cache line 反复失效→串行化吞吐量。用 `alignas(64)` 根据 `std::hardware_destructive_interference_size` 分离。

### 常见 Bug 与 Debug 方法

- **`memory_order_relaxed` 标志丢失（详见 ch108）**：store(relaxed)/load(relaxed) 无 synchronizes-with，ARM 弱内存模型下可见性延迟。TSan 抓 happens-before 违规。
- **`compare_exchange_weak` 的伪失败循环**：`while(!val.compare_exchange_weak(expected,desired))` 是正确写法；`compare_exchange_strong` 无伪失败但更多 fence。强平台（x86）两者等价、弱平台选 weak。
- **Code Review 关注点**：`is_lock_free` 是否被 `static_assert`；相邻 `atomic` 是否有伪分享风险；CAS 循环是否用 weak + while。

### 重构建议

对所有 `atomic<T>` 加上 `static_assert(is_always_lock_free)` 编译期断言；相邻高频 atomic 变量用 `alignas(64)` 分离消除伪分享；CAS 循环用 `compare_exchange_weak` + while 循环最小化 fence 开销。

## 附录 J：GCC 15.3.0 真机汇编实证（ASM-107-atomic_rmw）[E: Low-level]

> 工具链：`g++.exe (MinGW-W64 x86_64-msvcrt-posix-seh, Brecht Sanders r1) 15.3.0`，`-std=c++26 -O2 -c`，`objdump -d -M intel -C`。证据源码 `_asm_demo/ch107_atomic_rmw_test.cpp`、汇编 `_asm_demo/ch107_atomic_rmw_test.s`。各函数加 `[[gnu::noinline]]` 以隔离对比。

### 真机指令（节选）

```asm
; fetch_add_relaxed() 与 fetch_add_seqcst() —— 二者逐字节相同
        mov     eax,0x1
        lock xadd DWORD PTR [rip+g32],eax   ; 返回旧值于 eax；relaxed/seq_cst 指令无差别
        ret
; fetch_add64()  (uint64_t)
        mov     eax,0x1
        lock xadd QWORD PTR [rip+g64],rax   ; 64 位形式，rax 承载旧值
        ret
; exchange_seqcst()
        mov     eax,0x63                     ; 0x63 = 99
        xchg    DWORD PTR [rip+g32],eax      ; xchg 对内存操作数隐式 LOCK#，天然原子（无需显式 f0 前缀）
        ret
; cas_inc()  —— canonical CAS 重试环（compare_exchange_weak + while）
        mov     eax,DWORD PTR [rip+g32]      ; expected = load()
        lea     edx,[rax+0x1]                ; desired = expected + 1
.loop:  lock cmpxchg DWORD PTR [rip+g32],edx ; 若 [mem]==eax→写 edx 且 ZF=1；否则 [mem]→eax（刷新 expected）
        jne     .loop                        ; ZF=0（失败）→ 用新 eax 重试
        ret
```

### 非显然事实

1. **`fetch_add` 的 relaxed 与 seq_cst 生成逐字节相同的 `lock xadd`。** 原因：x86 的 `lock` 前缀本身就是全屏障（sequentially consistent），不存在"更弱"的 RMW 指令；内存序差异不是体现在 RMW 指令上，而是体现在编译器对**周围其他访存**的重排约束上。换言之，单看一条原子 RMW，你无法从指令区分 relaxed 与 seq_cst。
2. **`exchange` 用 `xchg` 而非 `lock xchg`。** x86 ISA 规定 `xchg` 一旦带内存操作数就**隐式断言 LOCK# 总线锁**（无论是否写 `f0` 前缀字节），因此无条件 swap 天然原子、零额外前缀开销。
3. **`compare_exchange_weak` 在 x86 上编译为 `lock cmpxchg` + `jne` 重试环；weak 与 strong 逐字节相同。** x86 的 `cmpxchg` 是真实硬件 CAS，GCC **不模拟"伪失败"**——所谓 spurious failure 只发生在无法用单条指令表达 CAS 的平台（编译器被迫注入重试）。这也解释了 ch107 正文"弱平台才需 weak、x86 上两者等价"的结论：硬件层面根本没有差别。
4. **64 位 RMW 为 `lock xadd QWORD ... ,rax`**，与 32 位完全同构，仅操作数宽度与累加器（rax vs eax）不同。

### 跨平台警示（呼应 ch108）

以上 `lock` 前缀行为仅在 x86-64 TSO 成立。ARM/ARM64 上 `fetch_add`/`exchange` 通常编译为 `ldadd`/`swp`（Armv8.1 LSE 原子指令）或 `ldrex`/`strex` 独占监视对，CAS 用 `ldxr`/`stxr` 循环。**`lock` 前缀是 x86 专属**，把 x86 上"一条带锁指令"的心智模型照搬到 ARM MCU 会误判原子性与性能——ARM 弱内存还需配 `dmb` 屏障才获得等价顺序保证。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

**真实场景**：高并发服务里统计 QPS、命中数、错误数等指标是写多读少的典型场景——若每次加锁（`std::mutex`）开销过大，无锁原子计数器是默认首选。请用 `std::atomic<long>` 实现一个线程安全计数器，让 8 个线程各自 `+100000`，最终总和必须恰好 `800000`。说明为何 `counter = counter + 1;` 形式是错的，而 `fetch_add` 是对的——`atomic` 保证的是"单个操作"原子，不是"涉及该变量的任意表达式"原子。

<details><summary>答案与解析</summary>

`atomic<T>::fetch_add` 是单条**读-改-写（RMW）**原子操作，中途不可被打断；而 `counter = counter + 1` 展开为「原子 load → 普通加 → 原子 store」三步，两次 RMW 之间可插入其它线程的更新，导致丢失更新。

> **示例 51** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 练习 1（难度 ★★）
```cpp
#include <atomic>
#include <thread>
#include <vector>
#include <iostream>
int main() {
    std::atomic<long> counter{0};
    auto work = [&]{ for (int i = 0; i < 100000; ++i) counter.fetch_add(1, std::memory_order_relaxed); };
    std::vector<std::thread> ts;
    for (int i = 0; i < 8; ++i) ts.emplace_back(work);
    for (auto& t : ts) t.join();
    std::cout << counter.load() << '\n';   // 恰好 800000
    return counter.load() == 800000 ? 0 : 1;
}
```

<span class="badge badge-std">标准</span> 纯计数无跨变量依赖，用 `memory_order_relaxed` 即可保证原子性与最终一致，且是最快选项（`[atomics.order]`）。

<span class="badge badge-ref">引用</span> cppreference `std::atomic::fetch_add`：`https://en.cppreference.com/w/cpp/atomic/atomic/fetch_add`。原子操作与内存序规范见 ISO §32.5（[atomics]）。

</details>

### 练习 2（难度 ★★★）

**真实场景**：并发监控里常要"无锁地维护一个全局最大延迟/最大水位线"——标准库没有 `fetch_max`，但任何读-改-写都可以用 CAS 循环表达。请用 `compare_exchange_weak` 自己实现一个无锁的「原子取最大值」`atomic_fetch_max`，使多线程写入不同值后，原子变量保存全局最大值。为什么用 `compare_exchange_weak` 而非 `strong`？CAS 失败时为什么 `cur` 会被自动刷新为最新值？

<details><summary>答案与解析</summary>

CAS 循环是实现任意 RMW 的通用范式：读当前值 → 本地算新值 → CAS 提交，失败则用被刷新的期望值重试。`compare_exchange_weak` 允许伪失败但在循环里代价更低。

> **示例 52** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 练习 2（难度 ★★★）
```cpp
#include <atomic>
#include <thread>
#include <vector>
#include <iostream>
long atomic_fetch_max(std::atomic<long>& a, long v) {
    long cur = a.load(std::memory_order_relaxed);
    while (v > cur && !a.compare_exchange_weak(cur, v,
               std::memory_order_release, std::memory_order_relaxed)) {}
    return cur;   // cur 被 CAS 失败时自动刷新为最新值
}
int main() {
    std::atomic<long> m{0};
    std::vector<std::thread> ts;
    for (long i = 1; i <= 8; ++i) ts.emplace_back([&, i]{ atomic_fetch_max(m, i * 1000); });
    for (auto& t : ts) t.join();
    std::cout << m.load() << '\n';   // 8000
    return m.load() == 8000 ? 0 : 1;
}
```

<span class="badge badge-std">标准</span> CAS 失败时 `cur` 被写入内存现值，无需手动重载——这是 `compare_exchange` 的关键约定。

<span class="badge badge-ref">引用</span> cppreference `std::atomic::compare_exchange_weak`：`https://en.cppreference.com/w/cpp/atomic/atomic/compare_exchange`。CAS 循环范式见 ISO §32.5（[atomics]）及 M. Herlihy, *Wait-Free Synchronization*, 1991。

</details>

### 练习 3（难度 ★★★★）

**真实场景**：极短临界区（如更新一个标志、改一个计数器）下，自旋锁比互斥量更轻——`std::atomic_flag` 是标准保证"必然无锁"的最小原子类型，正是实现自旋锁/无锁栈标记位的基石。请用 `std::atomic_flag` 实现一个最小自旋锁 `SpinLock`（`lock`/`unlock`），并说明为何 `test_and_set` 用 `acquire`、`clear` 用 `release`。用它保护一个普通 `int` 累加，验证无数据竞争。生产环境为什么还应在自旋体里加 `std::this_thread::yield()`？

<details><summary>答案与解析</summary>

`atomic_flag` 是标准保证**无锁**的最小原子类型。`lock` 用 `test_and_set(acquire)` 保证临界区读写不会被重排到加锁之前；`unlock` 用 `clear(release)` 保证临界区写在释放锁前对下一个持有者可见——构成 release/acquire 同步对。

> **示例 53** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 练习 3（难度 ★★★★）
```cpp
#include <atomic>
#include <thread>
#include <vector>
#include <iostream>
struct SpinLock {
    std::atomic_flag f = ATOMIC_FLAG_INIT;
    void lock()   { while (f.test_and_set(std::memory_order_acquire)) { /* spin */ } }
    void unlock() { f.clear(std::memory_order_release); }
};
int main() {
    SpinLock sl;
    int shared = 0;                       // 普通 int，靠锁保护
    auto work = [&]{ for (int i = 0; i < 100000; ++i) { sl.lock(); ++shared; sl.unlock(); } };
    std::vector<std::thread> ts;
    for (int i = 0; i < 4; ++i) ts.emplace_back(work);
    for (auto& t : ts) t.join();
    std::cout << shared << '\n';           // 400000
    return shared == 400000 ? 0 : 1;
}
```

<span class="badge badge-exp">经验</span> 生产环境的自旋锁还应在自旋体内加 `_mm_pause()`/`std::this_thread::yield()` 降低总线争用与功耗；纯 busy-loop 仅用于极短临界区。

<span class="badge badge-ref">引用</span> cppreference `std::atomic_flag`：`https://en.cppreference.com/w/cpp/atomic/atomic_flag`；`std::atomic_flag::test_and_set`：`https://en.cppreference.com/w/cpp/atomic/atomic_flag/test_and_set`。

### 练习 4（难度 ★★★）

**真实场景：指标采集的"取出并清零"必须原子。** 监控系统周期性收集计数器的批次值、随后清零重计——若把"读当前值 + 清零"写成两条语句，两个采集线程可能一个丢批、一个漏数。`std::atomic::exchange(new)` 原子地完成"返回旧值并写入新值"，是"取批并归零"的唯一正确表达。请用 `exchange` 实现周期采集，说明为什么 `load` + `store` 拆开会丢更新。

<details><summary>答案与解析</summary>

`exchange(desired)` 是一个读-改-写（RMW）原子操作：返回**旧值**、写入 `desired`，两者在同一临界点完成。它等价于"`old = load(); store(desired); return old;`"但整段不可被打断——任何别的线程的写入要么发生在 exchange 之前（被计入旧值）、要么之后（留在新计数周期），绝不会丢失。而拆开的 `load()` 与 `store(0)` 之间可能插入另一个线程的 `fetch_add`，导致那次累加既不在本次批次、也不在下个周期。

标准依据：`exchange` 的语义见 ISO §32.5.5（[atomics.types.operations]）；RMW 操作只接受 `memory_order_relaxed`/`consume`/`acquire`/`release`/`acq_rel`/`seq_cst`。对纯计数且无跨变量发布需求，`relaxed` 足够——`exchange` 自身仍保证"取旧写新"的原子性。

边界条件与失效场景：生产线程在 `exchange(0)` 完成瞬间的并发 `fetch_add` 会落到新周期——这是"按周期切分"的语义边界，业务应明确接受。若还需知道"哪一次 `fetch_add` 落在哪个批次"，exchange 满足不了，需 epoch/版本号（见 ch111 tagged pointer 思想）。高频路径上 `exchange` 与 `fetch_add` 同为单条 `lock xchg`/`lock xadd`，无额外代价。

> **示例 59** <span class="badge badge-exp">难度 ★★★☆☆</span> · 练习 4（难度 ★★★）
```cpp
#include <atomic>
#include <thread>
#include <vector>
#include <iostream>
int main() {
    std::atomic<long> counter{0};
    std::vector<std::thread> ps;
    for (int i = 0; i < 4; ++i)
        ps.emplace_back([&]{ for (int j = 0; j < 25000; ++j)
                                counter.fetch_add(1, std::memory_order_relaxed); });
    for (auto& t : ps) t.join();
    // 采集：原子地"取出并清零"——load+store 拆开会丢更新
    long batch = counter.exchange(0, std::memory_order_relaxed);
    std::cout << "batch=" << batch << ", now=" << counter.load() << '\n';
    return batch == 100000 && counter.load() == 0 ? 0 : 1;
}
```

<span class="badge badge-std">标准</span> `exchange` 是 RMW 原子操作，返回值与写新值不可分割（[atomics.types.operations]）；"读批 + 清零"语义用 exchange 表达，拆成 `load`+`store` 会引入竞态窗口。

<span class="badge badge-exp">经验</span> 指标采集"取批归零"用 `exchange(0)`；"只读快照"用 `load`；"累加"用 `fetch_add`——三种诉求对应三种原子原语，别混用。多周期时序敏感时把 epoch 与批次值打包成 `uint64_t` 一次 exchange 取回。

</details>

### 练习 5（难度 ★★★）

**真实场景：忙等太费，让线程睡到"标志变化"再醒。** 工作线程等待"任务就绪"信号时，`while(!flag.load()){}` 忙等空转烧 CPU；C++20 的 `std::atomic::wait`/`notify_*` 把"阻塞到值变化"做成库原语。请用 `atomic<bool>::wait` 阻塞主线程直至 worker 置位并 `notify_one`，说明 `wait` 的"值比较 + 阻塞"为何是原子判定、以及伪唤醒（spurious wakeup）如何处理。

<details><summary>答案与解析</summary>

`wait(old, order)` 先以 `order` 读值：若等于 `old` 则阻塞，直到被 `notify_one()`/`notify_all()` 唤醒或发生伪唤醒后重新检查——它内部是"读到 old 才睡"的原子判定，`load` 与"决定阻塞"之间没有竞态窗口。生产者 `store(true)` 后 `notify_one()` 把恰好阻塞中的线程唤醒；若通知先于 wait，则 wait 首次读值已 != old、直接不阻塞。

标准依据：`wait`/`notify_one`/`notify_all` 是 C++20 原子类型新增成员（见 ISO §32.5.3），其"公平性不做保证、允许伪唤醒"由实现决定——调用方必须在循环里用 `wait` 或结合 `while` 条件防御伪唤醒。与 `std::condition_variable` 不同，`atomic::wait` 不需要互斥量配套，也没有 `predicate` 重载。

边界条件与失效场景：`wait` 只保证"被通知或伪唤醒时返回"，不保证"值已变化"——正确姿势是 `while (val.load(acquire) != expected) val.wait(expected);` 循环或检查后重试。`notify_one` 只唤醒一个线程；多等待者广播用 `notify_all`。若目标值在阻塞期间变化后又变回 `old`，wait 可能错过通知但仍会在未来被其它通知/伪唤醒唤醒——高频翻转场景慎用。

> **示例 60** <span class="badge badge-exp">难度 ★★★☆☆</span> · 练习 5（难度 ★★★）
```cpp
#include <atomic>
#include <thread>
#include <iostream>
int main() {
    std::atomic<bool> ready{false};
    std::atomic<int> data{0};
    std::thread worker([&]{
        data.store(42, std::memory_order_release);
        ready.store(true, std::memory_order_release);
        ready.notify_one();                            // 唤醒阻塞中的等待者
    });
    // 阻塞直到 ready 变为 true（可配循环防御伪唤醒）
    while (!ready.load(std::memory_order_acquire))
        ready.wait(false, std::memory_order_acquire);
    std::cout << "data=" << data.load(std::memory_order_acquire) << '\n';   // 42
    worker.join();
    return 0;
}
```

<span class="badge badge-std">标准</span> `atomic::wait(old, order)` 语义是"读值等于 `old` 才阻塞"（[atomics.wait]）；release/acquire 配对让 `data` 的写在 `ready` 通知链上对等待者可见。

<span class="badge badge-exp">经验</span> 单个标志/计数器的等待用 `atomic::wait` 最轻（无锁、无内核对象）；多个条件或多个线程配互斥量的场景仍属 `condition_variable` 的领地。伪唤醒是标准允许行为，工业代码一律 `while` 包裹，别写裸 `if`。

</details>

## 附录：用法演绎（从选型到落地）

> 本节把本章原子原语放进真实决策链：**选型场景 → 常见错误 → 修复代码 → 工程结论**。

### 演绎 1：计数器该用 mutex、atomic 还是分片计数？

**选型场景**：高频统计计数（如 QPS、命中数），写远多于读，无跨变量依赖。

- `std::mutex + int`：正确但每次加锁有系统调用/争用开销，高频下成为瓶颈。
- `std::atomic<long>` + `fetch_add(relaxed)`：单条 `lock xadd`，无锁、最省心，是**默认首选**。
- 分片计数（每线程一个 cache-line 对齐的计数器，读时求和）：写零争用，但读需遍历、占内存——仅在 `fetch_add` 也成为热点时才上。

**常见错误**：把「读改写」写成两步，误以为 `atomic` 就万事大吉。

> **示例 54** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 演绎 1：计数器该用 mutex、a
```cpp
#include <atomic>
#include <thread>
#include <vector>
#include <iostream>
int main() {
    std::atomic<long> c{0};
    // 错误：c = c + 1 是 load + 普通加 + store，两次 RMW 间会丢更新
    auto bad = [&]{ for (int i = 0; i < 100000; ++i) c = c + 1; };
    std::vector<std::thread> ts;
    for (int i = 0; i < 8; ++i) ts.emplace_back(bad);
    for (auto& t : ts) t.join();
    std::cout << "bad total = " << c.load() << " (通常 < 800000)\n";  // 丢更新
    return 0;   // 编译通过，运行期结果错误——典型「原子变量非原子使用」
}
```

**修复**：改为 `c.fetch_add(1, std::memory_order_relaxed);`（见练习 1），结果恒为 `800000`。

**结论**：`atomic` 保证的是**单个操作**原子，不是「涉及该变量的任意表达式」原子。凡「读→算→写」必须落到一条 RMW（`fetch_add`/`fetch_or`/`compare_exchange`）。

### 演绎 2：`atomic<BigStruct>` 为什么悄悄退化成带锁？

**选型场景**：想把一个 24 字节的配置结构体做成原子快照，多线程读、偶尔整体替换。

**常见错误**：直接 `std::atomic<Config>`，以为拿到无锁快照。

> **示例 55** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 演绎 2：atomic<BigStr
```cpp
#include <atomic>
#include <iostream>
struct Config { long a, b, c; };          // 24 字节，超过硬件宽 CAS（16 字节）
int main() {
    std::atomic<Config> cfg{};
    std::cout << "is_lock_free = " << cfg.is_lock_free() << '\n';  // 多半为 0：内部用锁
    Config c = cfg.load();                 // 语法合法，但退化为「加锁 memcpy」
    (void)c;
    return 0;
}
```

对象超过平台宽 CAS 宽度（x86-64 上 `cmpxchg16b` 管 16 字节）时，`std::atomic<T>` 会退化为「内部锁 + memcpy」，`is_lock_free()` 返回 0，失去无锁初衷，还可能在信号处理中不安全。

**修复**：改为**原子指针发布不可变快照**（RCU 式），读侧只读一个 8 字节原子指针：

> **示例 56** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 演绎 2：atomic<BigStr
```cpp
#include <atomic>
#include <memory>
#include <iostream>
struct Config { long a, b, c; };
int main() {
    auto p = std::make_shared<const Config>(Config{1, 2, 3});
    std::atomic<std::shared_ptr<const Config>> cur{p};   // C++20 原子 shared_ptr
    auto snap = cur.load();                                // 8 字节原子读，读侧无锁
    std::cout << snap->a << ' ' << snap->b << ' ' << snap->c << '\n';
    cur.store(std::make_shared<const Config>(Config{4, 5, 6}));  // 整体替换
    return 0;
}
```

**结论**：宽对象不要硬塞 `atomic<T>`。用「原子指针 + 不可变对象」发布快照：读侧一条原子指针 load，替换是一次指针 CAS，天然无锁且信号安全。真正的回收安全见 ch112（HP/RCU）。

---

> **UB 实证库（并发）**：数据竞争（非原子并发写）与伪共享（缓存行弹跳）的**真实基准/运行证据** + `std::atomic` 修复，见 [附录 UB 反例库](../../Appendix/ub/README.md)（C1/C5）。

---

## 附录 K：真实并发基准——计数器实现的扩展性对决 [G: Performance]

> 本附录把本章「演绎 1：计数器该用 mutex、atomic 还是分片计数？」的**定性选型**变成**可量化实证**，并呼应 ⑪ 真实汇编（`fetch_add` → `lock xadd`）与 ⑰ 伪共享。
> 基准程序 `_bench_atomic.cpp`（已留库根，可复现）：GCC 15.3.0 `-O2 -std=c++20 -pthread -static`，总增量固定 `N=50,000,000`，用原子 `start` 旗隔离线程创建开销，末态和校验恒等于 `N`（防数据竞争/优化失真）。分片用 `std::atomic_ref<long>` 落在每线程 `alignas(64)` 私有槽——**避免编译器把裸累加循环强度削减成单条赋值**（微基准经典坑，详见下文方法学注）。

### K.1 四种实现与实测吞吐（M/s = 百万次增量/秒）

| 线程数 T | `std::mutex`+`long` | `atomic` seq_cst | `atomic` relaxed | 分片(每线程槽) |
|---|---|---|---|---|
| 1 | 60.8 | 356.5 | 356.3 | 386.5 |
| 2 | 36.5 | 80.2 | 95.5 | 391.9 |
| 4 | 14.6 | 61.6 | 69.8 | 783.5 |
| 8 | 12.5 | 54.8 | 48.7 | **1564.9** |

### K.2 三个非显然结论

**① 单线程：mutex 比 atomic 慢 5.9×**（60.8 vs 356.5 M/s）。`std::mutex` 每次加锁/解锁都有 futex/系统调用与内存屏障开销；单条 `lock xadd` 只是一次原子 RMW。→ 单写或低争用场景，永远优先 `atomic` 而非 `mutex`。

**② 高争用下，共享 atomic / mutex 都「负扩展」**：
- mutex：60.8 → 12.5 M/s（8 线程反而慢 **4.9×**）——所有线程在**同一把锁**上排队，线程越多越串行。
- atomic seq_cst：356.5 → 54.8 M/s（**6.5× 慢**）——所有线程抢**同一个缓存行**的独占权，MESI 在核间反复弹跳（coherence traffic）。
- 这与「atomic 无锁就快」的直觉相反：无锁 ≠ 无争用。锁消除的是「互斥等待」，没消除「共享写变量→缓存行乒乓」。

**③ 分片计数近线性扩展，且碾压一切**（386.5 → 1564.9 M/s，8 线程 **4.05× 加速**；比同线程 atomic 快 **28.6×**，比 mutex 快 **125×**）。每线程写自己的 `alignas(64)` 槽，**零缓存行争用**，写之间完全独立 → 完美随核数扩展。代价仅是「读时需遍历求和 + 占 T 条缓存行内存」（见 ⑰ 伪共享的对称面）。

> **关键反直觉点**：`relaxed` 在争用下与 `seq_cst` 几乎相同（8 线程 48.7 vs 54.8 M/s）。原因见 ⑪：`fetch_add` 无论 memory_order 都编译成 `lock xadd`，而 `lock` 前缀**强制独占缓存行**——瓶颈是「拿不到 Exclusive 行」，不是「内存屏障多严」。`relaxed` 省掉的只是 x86 上本就便宜的 `mfence`，在争用场景中占比极小。**结论：靠 `memory_order_relaxed` 救不了高争用计数器的吞吐，靠分片（消除共享写）才行。**

### K.3 选型决策（实证后的精确版）

```mermaid
flowchart TD
    Q["高频共享计数器?"] --> S{"写线程数 / 争用强度"}
    S -- "单写 或 低争用" --> A["std::atomic&lt;long&gt;::fetch_add(relaxed) 默认首选&lt;br/&gt;实测 356 M/s, 比 mutex 快 5.9x"]
    S -- "多写高争用 且 必须单变量" --> B["shared atomic 吞吐塌缩&lt;br/&gt;实测 8线程仅 55 M/s, 比1线程慢 6.5x"]
    S -- "多写高争用 且 可接受最终汇总" --> C["分片计数: 每线程 alignas(64) 槽, 读时求和&lt;br/&gt;实测 8线程 1565 M/s, 近线性扩展"]
    B --> D["瓶颈 = 缓存行独占权(MESI 弹跳),&lt;br/&gt;relaxed 救不了, 须消除共享写"]
    C --> E["比同线程 atomic 快 28.6x, 比 mutex 快 125x"]
    A --> F["lock xadd 单 RMW, 无锁开销"]
```

### K.4 与本书其他章的交叉引用

- **演绎 1（本章）**：本附录是其量化版——演绎 1 说「默认首选 `atomic`、分片仅在 fetch_add 也成热点的上进」，本基准给出了「热点」的**精确阈值**（共享 atomic 约 55 M/s 量级即触顶，分片可再提 28×）。
- **⑰ 伪共享**：分片用 `alignas(64)` 把每槽钉在不同缓存行，正是 ⑰「消除伪共享」的正向应用；⑰ 讲「共享写变慢」，本附录讲「分而治之变快」，是同一机制的阴阳两面。
- **ch108 内存序**：K.2③ 解释了为何 x86 上 relaxed/seq_cst 在争用下无差——x86 TSO 下 store 自带 release，`mfence` 才是 seq_cst 额外代价，但相对 `lock` 行独占可忽略。
- **ch41 `shared_ptr`**：其控制块的引用计数本身就是一个 `std::atomic`——本附录的「共享 atomic 负扩展」同样适用于 `shared_ptr` 拷贝风暴；高频拷贝 `shared_ptr` 时，分片/本地化引用计数同样是解药。

### K.5 方法学注（D5 可复现要点）

- **编译**：`-O2 -std=c++20`（分片用 `std::atomic_ref`，C++20 起可用）+ `-pthread -static`。
- **防循环被优化**：分片若用裸 `long l; for(...) l+=1;` 再回写，`-O2` 会把循环强度削减为 `l = N/T` 单条赋值，吞吐虚高几个数量级（首版即踩此坑，虚报 38 万 M/s）。改用 `std::atomic_ref<long>` 落每线程私有槽，既是真实内存 RMW（不可消除），又无跨线程争用，公平代表「分片」本质。
- **隔离线程创建开销**：用 `std::atomic<bool> start` 旗，所有线程自旋等待同一时刻释放再计时，避免 `std::thread` 构造/销毁时间混入并行段。
- **正确性校验**：每种策略末态和必须恒等于 `N=50,000,000`，否则说明有数据竞争或被优化掉；本基准四策略均通过。

---

### D5.5 汇编实证 (GCC 15.3.0)

> 以下 disassembly 由 `g++ -O2 -std=c++23 -masm=intel _bench_d5_107_atomic.cpp` 真实生成（节选 `bench_atomic_relaxed` / `bench_mutex` 的**工作线程**热循环）。原子路径是单条 `lock add`、互斥路径每次迭代要两次 `pthread_mutex_*` 系统调用再配一条普通 `add`——这正解释了 D5.2「mutex 慢在系统调用+阻塞、atomic 是纯 RMW」的非显然结论。

```asm
; bench_atomic_relaxed 工作线程（节选热循环）—— 单条 lock xadd，无系统调用、无阻塞
;   _ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ20bench_atomic_relaxediEUlvE_EEEEE6_M_runEv (节选)
        mov     eax, 2000000
        xor     edx, edx
        idiv    DWORD PTR 16[rcx]      ; per = N / nthreads
        test    eax, eax
        jle     .L
        cdqe
        xor     edx, edx
        mov     r8, QWORD PTR 8[rcx]
        lock add        QWORD PTR [r8], 1   ; ← 原子 RMW：单条带 LOCK# 自增，纯用户态，无系统调用
        add     rdx, 1
        cmp     rax, rdx
        jne     .L
        ret
; bench_mutex 工作线程（节选热循环）—— 每次迭代两次系统调用 + 一条普通自增
;   _ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ11bench_mutexiEUlvE_EEEEE6_M_runEv (节选)
        mov     rbx, QWORD PTR 8[rcx]
        mov     rcx, rsi
        call    pthread_mutex_lock      ; ← 加锁：futex 系统调用 + 内存屏障
        test    eax, eax
        jne     .L
        mov     rdx, QWORD PTR 24[rdi]
        mov     rcx, rsi
        add     rbx, 1
        add     QWORD PTR [rdx], 1      ; 受互斥保护的普通自增（原子性来自锁，而非指令本身）
        call    pthread_mutex_unlock    ; ← 解锁：第二次系统调用（可能陷入内核睡眠/唤醒）
        cmp     rbp, rbx
        jne     .L
```

> 注意：两条路径的「计数器自增」本身都是一次 `+1`，差异全在周围——`atomic` 用 CPU 的 `lock` 前缀把 RMW 变成不可分割的原子操作；`mutex` 则把临界区交给内核 futex 串行化，单次最慢、高争用下还坠入上下文切换。这与 D5.2 第①、②条一致：**绝对毫秒随机器而变，加速比（约 1.6–2.1×）才是可移植信号**。

## 附录 L：原子操作知识图谱（D6 知识连接） [J: Learning / H: Design / G: Performance]

> 本附录把本章散落的「重排 / memory_order / RMW / 缓存 / 锁 / 无锁 / ABA」串成一张**概念依赖图**，回答三个 D6 问题：① 这些概念谁依赖谁？② 一条 `std::atomic` 写到底牵动哪些硬件/编译器机制？③ 与本书哪些章构成知识闭环？
> 它不是装饰图——每条边都带**依赖方向**（A → B 表示「B 的成立依赖 A 的约束/支撑」），下文逐边解读。图与 ch108 内存序总论、⑰ 伪共享、附录 K 基准互为表里。

```mermaid
flowchart TD
    REORD["编译器重排 / CPU 重排<br/>(乱序执行 · store 缓冲 · 写合并)"] -->|"被 memory_order 约束"| MO["memory_order<br/>relaxed / acq-rel / seq_cst"]
    MO -->|"决定可见性强度"| AT["std::atomic&lt;T&gt;<br/>(RMW: lock xadd / lock cmpxchg)"]
    AT -->|"acquire/release 配对建立"| SW["synchronizes-with<br/>(跨线程同步关系)"]
    SW -->|"推导"| HB["happens-before<br/>(跨线程偏序保证)"]
    AT -->|"运行于硬件之上"| MESI["cache 一致性 (MESI)<br/>独占行弹跳 = 争用成本"]
    MO -->|"可由显式屏障表达"| FENCE["atomic_thread_fence<br/>(批量刷新可见性)"]
    MUTEX["std::mutex / 锁<br/>(互斥 + 隐含 acq/rel)"] -->|"提供更强 synchronizes-with"| HB
    AT -->|"CAS/RMW 支撑"| LF["lock-free / wait-free<br/>(无阻塞进度保证)"]
    LF -->|"依赖 CAS 实现"| CAS["compare_exchange<br/>(无锁算法原语)"]
    CAS -->|"固有陷阱"| ABA["ABA 问题<br/>(指针复用致 CAS 误判)"]
    AT -.->|"共享写触发"| FS["伪共享 (false sharing)<br/>⑰ / ch154: 缓存行乒乓"]
    MESI -.->|"争用放大"| FS
```

### L.1 逐边解读（依赖方向为何成立）

1. **重排 → memory_order**：`memory_order` 存在的唯一理由就是约束编译器与 CPU 的重排自由度。relaxed 允许任意重排（只保原子性），acq-rel 约束临界区边界，seq_cst 加全局顺序。没有重排，memory_order 无意义——这也解释了 ch30 ⑮「volatile 不建立 happens-before」：volatile 只挡编译器重排，**完全不挡 CPU 重排**，更不约束可见性。
2. **memory_order → atomic**：同一原子对象，用不同 memory_order 读写作出的**可见性承诺**不同。例：单生产者单消费者队列用 `store(release)` + `load(acquire)` 即可，无需 seq_cst 的全局开销——这是「按需付费」原则。
3. **atomic → synchronizes-with**：只有 **release/acquire/seq_cst** 配对才建立 synchronizes-with；relaxed 的 RMW 不建立任何同步。这正是 ⑮/附录 J 里 `fetch_add` 无论 memory_order 都编译成 `lock xadd`，但**可见性语义**随 memory_order 而变的原因。
4. **synchronizes-with → happens-before**：synchronizes-with 是 happens-before 的主要来源之一。一旦 A 线程 release、B 线程 acquire 到同一原子，A 在 release 前的所有写对 B 在 acquire 后可见——数据竞争 UB（⑩）由此被消除。
5. **atomic → MESI（硬件 substrate）**：任何原子 RMW 最终落到硬件原子指令（x86 `lock` 前缀 / ARM `ldaxr`+`stlxr`）。`lock` 强制独占缓存行，于是「争用」在硬件层表现为 MESI 在核间反复弹跳——这是附录 K 中「共享 atomic 8 线程仅 55 M/s、比 1 线程慢 6.5×」的**物理根源**，而非算法问题。
6. **memory_order → fence**：`atomic_thread_fence` 是 memory_order 的「区间/批量」形式——一条 fence 刷新一批操作，而非逐个标 memory_order。批量边界清晰时用 fence 更省标注成本（注意：x86 TSO 下 fence 收益有限，见附录 K 关键反直觉点）。
7. **mutex → happens-before**：`std::mutex` 的 lock/unlock 隐含 acquire/release，且**额外提供互斥**（同一时刻仅一线程进临界区）。所以 mutex 给出的 synchronizes-with 比 atomic 更强——代价是可能阻塞（附录 K 单线程慢 5.9× 的由来）。
8. **atomic → lock-free**：`is_lock_free()` 的进度保证来自 RMW 指令；`compare_exchange` 是无锁算法基石。⑬ 无锁栈、无锁队列都建在这条边上。
9. **CAS → ABA**：基于 CAS 的无锁结构（⑬ 无锁栈）会踩 ABA——指针被复用（A→B→A）使 CAS 误判「没变」。解法：hazard pointer / 带版本标签的原子 / 改用风险指针（见 ⑭ ABA 预告）。
10. **atomic → 伪共享**：多个原子落在同一缓存行会被 MESI 弹跳拖慢——即 ⑰ 伪共享，也是附录 K 分片计数用 `alignas(64)` 拆槽的直接动机。

### L.2 跨章知识闭环（D6 连接方向）

| 本图谱节点 | 连接章 | 关系 |
|---|---|---|
| memory_order / synchronizes-with / happens-before | **ch108 内存序（总论）** | 三角的 WG21 来源与成本量化在 ch108 附录 A/B；本图谱是其「概念层」，ch108 是其「证据层」 |
| MESI / 伪共享 | **ch154 缓存优化**、**⑰ 伪共享** | 三方印证：ch154 附录 I 给 `hardware_interference_size` 源码 + 伪共享 5.66× 基准；本图谱给机制位置 |
| mutex → happens-before | **ch41 智能指针**、**ch40 异常安全** | `shared_ptr` 控制块引用计数是 atomic（附录 K 负扩展同样适用）；锁与异常安全的回滚语义强相关 |
| CAS / ABA | **⑬ 无锁栈**、**ch95 内省排序** | 无锁数据结构与无锁原语的工程落点 |
| 重排起点 | **ch30 volatile（⑮）** | volatile 只挡编译器重排、不建立 happens-before——图谱起点反衬 atomic 的必要性 |
| is_lock_free / 进度保证 | **ch115 移动语义**、**ch122 pmr** | 无锁数据结构要求移动/析构 `noexcept`（异常安全）；pmr 多态分配器与原子协同做无锁内存池 |
| RMW 指令 | **附录 J 真机汇编** | 图谱中 `lock xadd/cmpxchg` 的逐指令实证在附录 J；本图谱是「为什么」、附录 J 是「长什么样」 |

## 附录 D4：libstdc++ 15.3.0 源码解析 — std::atomic 原子操作内建映射

> 以下源码摘自 libstdc++ 15.3.0（GCC 15.3.0 附带），文件 `bits/atomic_base.h` 与 `atomic`。

### D4.1 __atomic_base 存储成员与对齐

```text
// bits/atomic_base.h  L337-358  (libstdc++ 15.3.0)
  template<typename _ITp>
    struct __atomic_base
    {
    private:
      typedef _ITp __int_type;

      static constexpr int _S_alignment =
	sizeof(_ITp) > alignof(_ITp) ? sizeof(_ITp) : alignof(_ITp);

      alignas(_S_alignment) __int_type _M_i _GLIBCXX20_INIT(0);
```

### D4.2 is_lock_free() — 运行时无锁判定

```text
// bits/atomic_base.h  L452-460  (libstdc++ 15.3.0)
      bool
      is_lock_free() const noexcept
      {
	return __atomic_is_lock_free(sizeof(_M_i),
	    reinterpret_cast<void *>(-_S_alignment));
      }
```

### D4.3 load() / store() — 转发到 GCC 内建函数

```text
// bits/atomic_base.h  L468-491  store
      void
      store(__int_type __i, memory_order __m = memory_order_seq_cst) noexcept
      {
	__atomic_store_n(&_M_i, __i, int(__m));
      }

// bits/atomic_base.h  L493-513  load
      __int_type
      load(memory_order __m = memory_order_seq_cst) const noexcept
      {
	return __atomic_load_n(&_M_i, int(__m));
      }
```

### D4.4 compare_exchange — weak vs strong

```text
// bits/atomic_base.h  L530-565  weak（第4参数=1，允许伪失败）
      bool
      compare_exchange_weak(__int_type& __i1, __int_type __i2,
			    memory_order __m1, memory_order __m2) noexcept
      {
	return __atomic_compare_exchange_n(&_M_i, &__i1, __i2, 1,
					   int(__m1), int(__m2));
      }

// bits/atomic_base.h  L567-602  strong（第4参数=0，不允许伪失败）
      bool
      compare_exchange_strong(__int_type& __i1, __int_type __i2,
			      memory_order __m1, memory_order __m2) noexcept
      {
	return __atomic_compare_exchange_n(&_M_i, &__i1, __i2, 0,
					   int(__m1), int(__m2));
      }
```

### D4.5 atomic<T> 通用主模板 — 通用内建函数

```text
// atomic  L198-230  (libstdc++ 15.3.0)
  template<typename _Tp>
    struct atomic
    {
    private:
      static constexpr int _S_min_alignment
	= (sizeof(_Tp) & (sizeof(_Tp) - 1)) || sizeof(_Tp) > 16
	? 0 : sizeof(_Tp);

      static constexpr int _S_alignment
        = _S_min_alignment > alignof(_Tp) ? _S_min_alignment : alignof(_Tp);

      alignas(_S_alignment) _Tp _M_i;
```

### D4.6 设计动机

| 设计选择 | 动机 |
|---------|------|
| `alignas(_S_alignment)` | 确保原子变量对齐到 `sizeof(T)`，硬件可直接 CAS → 无锁 |
| `__atomic_*_n` 内建函数 | 编译器映射到最优机器指令（x86 LOCK CMPXCHG / ARM LDREX-STREX） |
| weak vs strong 分离 | CAS 循环中用 weak 省去重试开销（伪失败可接受）；单次 CAS 用 strong |
| 通用 `atomic<T>` 用非 `_n` 内建 | 处理可能有 padding 的自定义类型（`__atomic_load` vs `__atomic_load_n`） |

### D4.7 跨实现对比

| 实现 | 整型特化 | 通用 T | 内建函数 |
|------|---------|--------|---------|
| libstdc++ 15.3.0 | `__atomic_base<T>` 公有继承 | `alignas _M_i` | GCC `__atomic_*` |
| libc++ (LLVM) | `__atomic_base<T>` | `__cxx_atomic<T>` | Clang `__atomic_*` |
| MSVC STL | `_Atomic_impl<T>` | `_Atomic_storage<T>` | MSVC intrinsics |

三大实现均依赖编译器内建函数映射到硬件原子指令，API 层面一致。

### D4.8 编译验证

> **示例 57** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 编译验证
```cpp
#include <atomic>
#include <iostream>
#include <thread>
#include <vector>
int main() {
    std::atomic<int> counter{0};

    std::cout << "is_lock_free=" << counter.is_lock_free() << std::endl;  // 1
    std::cout << "is_always_lock_free=" << std::atomic<int>::is_always_lock_free << std::endl;  // 1

    counter.store(10);
    std::cout << "after store=" << counter.load() << std::endl;  // 10

    int expected = 10;
    bool ok = counter.compare_exchange_strong(expected, 20);
    std::cout << "cas(10->20)=" << ok << " val=" << counter.load() << std::endl;  // 1 20

    expected = 99;  // wrong expected
    ok = counter.compare_exchange_strong(expected, 30);
    std::cout << "cas(99->30)=" << ok << " val=" << counter.load() << std::endl;  // 0 20

    counter.fetch_add(5);
    std::cout << "after fetch_add(5)=" << counter.load() << std::endl;  // 25

    // multi-thread increment
    std::vector<std::thread> threads;
    for (int i = 0; i < 4; ++i) {
        threads.emplace_back([&counter]() {
            for (int j = 0; j < 1000; ++j) counter.fetch_add(1, std::memory_order_relaxed);
        });
    }
    for (auto& t : threads) t.join();
    std::cout << "after 4x1000 increment=" << counter.load() << std::endl;  // 4025
    return 0;
}
```

## 附录 U：原子类型与无锁选型决策流（D3 维度）

```mermaid
flowchart TD
    A["多线程共享变量需要同步"] --> B{"单变量原子操作就够?"}
    B -->|"是 单变量"| C{"类型 trivially copyable 且 <= 机器字?"}
    B -->|"否 多变量事务"| D["用 mutex / 自旋锁 保护临界区"]
    C -->|"是 小字"| C1["std::atomic<T> (通常 lock-free)"]
    C -->|"否 大字"| C2["atomic<T> 可能加锁 -> 拆分/用指针"]
    C1 --> E{"需要无锁进度保证?"}
    E -->|"是"| F{"is_lock_free() 为真?"}
    F -->|"是"| F1["CAS 循环 (compare_exchange_weak)"]
    F -->|"否"| F2["退化为锁 / 改设计"]
    E -->|"否"| G["直接用 load/store/exchange"]
    A --> H{"需要自定义内存序?"}
    H -->|"是"| H1["memory_order_acquire/release/seq_cst"]
    H -->|"否"| H2["默认 seq_cst 安全"]
    C1 --> X["落地: 选原子操作并守内存序/无锁前提"]
    C2 --> X
    D --> X
    F1 --> X
    F2 --> X
    G --> X
    H1 --> X
    H2 --> X
```

> 决策流说明：原子选型第一问是「单变量还是多变量事务」——单变量用 `std::atomic<T>`，多变量必须上锁（原子无法跨变量保持一致性）。对单变量再看类型大小：`is_lock_free()` 为假时 `atomic<T>` 内部加锁，大结构应拆成机器字字段或改用指针。需要无锁进度保证时用 CAS 循环，但务必处理 ABA 与 `compare_exchange` 的自旋；内存序默认 `seq_cst` 最安全，只在已论证热点处放宽到 acquire/release。

## 附录 V：原子操作知识图谱（D6 维度）

```mermaid
flowchart TD
    LF["is_lock_free()"] --> AT["std::atomic<T>"]
    CAS["compare_exchange / CAS 循环"] --> AT
    RMW["fetch_add / exchange (RMW)"] --> AT
    FLAG["atomic_flag (无锁保证)"] --> AT
    MO["memory_order"] --> SW["synchronizes-with / happens-before"]
    SW --> AT
    CAS --> ABA["ABA 问题"]
    FALSE["伪共享"] --> CACHE["缓存行 / MESI"]
    CACHE --> CH154["缓存优化 ch154"]
    MUTEX["mutex (退化路径)"] --> AT
    RMW --> CH108["内存序总论 ch108"]
    AT --> CH41["智能指针 ch41"]
    MO --> CH108
```

### V.1 概念依赖逐边解读

| 上游概念 | 下游概念 | 依赖含义 |
|---|---|---|
| is_lock_free() | std::atomic<T> | 无锁判定决定 atomic 是否真无锁还是内部加锁 |
| compare_exchange / CAS 循环 | std::atomic<T> | CAS 是无锁更新的核心原语 |
| fetch_add / exchange (RMW) | std::atomic<T> | RMW 是原子读-改-写操作族 |
| atomic_flag (无锁保证) | std::atomic<T> | atomic_flag 是唯一标准保证无锁的原子布尔 |
| memory_order | synchronizes-with / happens-before | 内存序建立同步与先行关系 |
| synchronizes-with / happens-before | std::atomic<T> | 原子操作通过这些关系提供跨线程可见性 |
| compare_exchange / CAS 循环 | ABA 问题 | CAS 循环在复用节点时可能受 ABA 干扰 |
| 伪共享 | 缓存行 / MESI | 伪共享源于多核竞争同一缓存行 |
| 缓存行 / MESI | 缓存优化 ch154 | 缓存行/伪共享的实证在 ch154 |
| mutex (退化路径) | std::atomic<T> | is_lock_free 为假时原子内部退化为锁 |
| fetch_add / exchange (RMW) | 内存序总论 ch108 | RMW 指令的语义成本在 ch108 量化 |
| std::atomic<T> | 智能指针 ch41 | shared_ptr 控制块引用计数即 atomic |
| memory_order | 内存序总论 ch108 | memory_order 三角的 WG21 来源在 ch108 |

### V.2 章节闭环表

| 上游章 | 下游章 | 传递的知识 |
|---|---|---|
| ch108（内存序总论） | ch107（原子） | memory_order 三角的 WG21 来源与成本量化在 ch108 |
| ch154（缓存优化） | ch107 | 伪共享/缓存行在 ch154 附录 I 实证 |
| ch41（智能指针） | ch107 | shared_ptr 控制块引用计数是 atomic（附录 K 负扩展同样适用） |
| ch40（异常安全） | ch107 | 锁与异常安全的回滚语义强相关 |
| ch30（volatile） | ch107 | volatile 只挡编译器重排、不建立 happens-before，反衬 atomic 必要 |
| ch95（内省排序） | ch107 | 无锁原语的工程落点在本书算法章 |
| ch115（移动语义） | ch107 | 无锁数据结构要求移动/析构 noexcept，与 pmr 协同做无锁内存池 |

## 附录 D5：真实基准与性能分析 — std::atomic 内存序与互斥锁对比 (GCC 15.3.0)

> 测试环境：AMD Ryzen 9 7940HX（16C/32T）；本机 MinGW-W64 GCC 15.3.0；`g++ -O2 -std=c++17`；`std::chrono::steady_clock` 计时，5 轮取中位；`volatile` sink 防死代码消除。本附录目的：对比 `std::atomic`（relaxed RMW）与 `std::mutex` 保护计数器在各线程数下的真实开销，并给出非显然根因。**绝对毫秒随机器而变，加速比才是可移植信号。**

### D5.1 基准结果

| 场景 | 耗时 ms | 相对 |
|---|---|---|
| 1 线程 — atomic relaxed / std::mutex | 6.78 / 14.33 | atomic **2.11×** 快 |
| 4 线程 — atomic relaxed / std::mutex | 22.39 / 34.83 | atomic **1.56×** 快 |
| 8 线程 — atomic relaxed / std::mutex | 29.33 / 55.43 | atomic **1.89×** 快 |

#### 可视化速读（D5.1 数据图）

<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="图：8 线程 atomic relaxed vs std::mutex 累加耗时">
  <text x="340" y="26" text-anchor="middle" font-size="14.5" font-family="Georgia, 'Times New Roman', serif" font-weight="bold">图：8 线程 atomic relaxed vs std::mutex 累加耗时</text>
  <line x1="80" y1="300" x2="640" y2="300" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300" x2="80" y2="52" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300.0" x2="640" y2="300.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="303.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">0</text>
  <line x1="80" y1="238.0" x2="640" y2="238.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="241.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">25</text>
  <line x1="80" y1="176.0" x2="640" y2="176.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="179.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">50</text>
  <line x1="80" y1="114.0" x2="640" y2="114.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="117.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">75</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="55.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">100</text>
  <text x="20" y="176" text-anchor="middle" font-size="12" font-family="Georgia, serif" transform="rotate(-90 20 176)">耗时 (ms)</text>
  <line x1="80" y1="162.5" x2="640" y2="162.5" stroke="#C44E52" stroke-width="1.2" stroke-dasharray="5 4"/>
  <text x="640" y="158.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif" fill="#C44E52">1.00× 基线 (std::mutex)</text>
  <rect x="188.0" y="162.5" width="64.0" height="137.5" fill="#9A9A9A"/>
  <text x="220.0" y="156.5" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#9A9A9A">55.43ms (1.00×)</text>
  <text x="220.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 220.0 314.0)">std::mutex</text>
  <rect x="468.0" y="227.3" width="64.0" height="72.7" fill="#C44E52"/>
  <text x="500.0" y="221.3" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#C44E52">29.33ms (1.89×快)</text>
  <text x="500.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 500.0 314.0)">atomic relaxed</text>
</svg>

> 图注：8 线程下 `atomic relaxed` 累加 29.33ms，比 `std::mutex` 55.43ms **快 1.89×**；1/4 线程结果同样利好原子（2.11× / 1.56×）。机制：lock-free 原子操作避开了 mutex 的系统调用与串行化等待。

### D5.2 非显然结论

1. **`std::mutex` 慢的根因是系统调用 + 线程阻塞/唤醒 + 可能的上下文切换 + 临界区串行化。** 每次 `++c` 都要经过 `lock_guard` 的加锁/解锁，低争用时也至少是一次 futex 往返与内存屏障开销。

2. **`std::atomic`（relaxed）只是一条 `lock xadd` 前缀原子指令，无系统调用、无阻塞。** 它是纯 RMW，编译为单条带 `LOCK#` 的原子加，因此各线程数下都比 `std::mutex` 快一个数量级附近（见 ⑪、附录 J 的 `lock xadd` 实证）。

3. **线程数增多时 mutex 的争用与休眠成本被放大（14.33 → 55.43 ms），atomic 优势更稳（6.78 → 29.33 ms）。** 注意 `memory_order_relaxed` 不保序，仅适用于纯计数器这类**无需同步其他内存**的场合；一旦要发布数据，需改 `acquire`/`release` 或 `seq_cst`（见 ch108）。

### D5.3 可复现 demo

> **示例 58** <span class="badge badge-exp">难度 ★★★☆☆</span> · 可复现 demo
```cpp
#include <iostream>
#include <thread>
#include <atomic>
#include <mutex>
#include <cassert>

int main() {
    constexpr int iterations = 1 << 20;   // 1,048,576

    std::atomic<int> atomic_counter{0};
    std::mutex mtx;
    int mutex_counter = 0;

    auto work = [&]() {
        for (int i = 0; i < iterations; ++i) {
            atomic_counter.fetch_add(1, std::memory_order_relaxed);
            {
                std::lock_guard<std::mutex> lk(mtx);
                ++mutex_counter;
            }
        }
    };

    std::thread t1(work);
    std::thread t2(work);
    t1.join();
    t2.join();

    std::cout << "atomic_counter = " << atomic_counter.load() << std::endl;
    std::cout << "mutex_counter  = " << mutex_counter << std::endl;

    // 功能正确性断言（绝不断言时间 / 倍数 / 精确 sizeof）
    assert(atomic_counter.load() == 2 * iterations);
    assert(mutex_counter == 2 * iterations);
    return 0;
}
```

### D5.4 方法学注

基准源码见库根 `_bench_d5_107_atomic.cpp`。
- 计时取 5 轮中位数，规避调度抖动与冷热启动偏差。
- `volatile` sink 防 DCE；末态和恒等于 `N` 作为正确性校验，防止数据竞争或循环被优化掉。
- 加速比（如 2.11× / 1.56× / 1.89×）是可移植信号；绝对毫秒随 CPU、内存、编译器版本而变，请勿跨机器直接比较毫秒。
- 复现旗标：`g++ -O2 -std=c++17`。demo 仅断言功能正确性（两种计数器末态都等于 `2 * iterations`），未对时间或倍数做任何断言。

## 参考引用

- `[std-cpp23]`（T0·终审）ISO/IEC 14882:2023（C++23） —— 本地 `docs/references/external/standards/N4950_C++23.pdf`
- `[cppref:cpp/atomic]`（T1）cppreference `cpp/atomic` —— 离线 `C:\Users\ASUS\Desktop\cppb参考资料\cppreference\`
- `[book:effective-modern:item40]`（T4）Effective Modern C++（Meyers，42 条） · Item 40：Use std::atomic for concurrency, volatile for special memory. —— 提取文本 `docs/references/external/books/effective-modern-cpp.txt`
- `[book:concurrency:ch5]`（T4）C++ Concurrency in Action（Williams） · ch5 —— 提取文本 `docs/references/external/books/cpp-concurrency.txt`

> 键的含义与全部来源见 `docs/references/SOURCING.md`；写作时只取要点，不整本投喂。

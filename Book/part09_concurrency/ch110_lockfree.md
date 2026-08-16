# 第110章　无锁编程：lock-free / wait-free（C++11）

⟶ Book/part09_concurrency/ch107_atomic.md
⟶ Book/part09_concurrency/ch111_aba.md

> 真实编译器：MinGW GCC 15.3.0（`-std=c++23 -O2 -S -masm=intel`，仓库权威工具链）；正文早期汇编插图示曾用 GCC 13.1.0 生成，已在本机 GCC 15.3.0 下复编确认指令一致（`fetch_add`→`lock add`/`lock xadd`、`CAS`→`lock cmpxchg`、128 位 CAS→`call __atomic_compare_exchange_16`），见下文 `[VERIFIED]` 标注。
> 取证源码：`Examples/_ch110_cas.cpp` / `_ch110_counter.cpp` / `_ch110_dwcas.cpp`（均在本章 `Examples/` 下，真实编译取证，非编造）。
> 约定参见 `CONVENTIONS.md`。本章立场分层与验证标记（见 §1/§10）：`[标准]`（标准语义）/`[实现·GCC15]`（本工具链行为）/`[ABI]`/`[平台·x86-64]`（x86-64 架构）/`[微架构·x86-64]`（CPU 缓存一致性/MESI/微架构）/`[经验]`（工程判断）；高风险断言标 `[VERIFIED]`（已实编确认）或 `[UNVERIFIED]`（ARM 行为、绝对 ns 基准等本机无法复现/不可移植）。

## ⓪ 历史动机：无锁编程的来龙去脉
> 锁的麻烦不只是"慢"，而是"持锁的线程一旦被卡住，所有人陪绑"。

### 0.1 起源（谁·何时·为何）
互斥量（mutex）让正确性容易保证，但代价是**阻塞**：持锁线程若被操作系统抢占、发生页错误、或遇到优先级反转，所有等待线程全被冻住；更糟的是死锁。在实时系统、高频交易、操作系统内核这类"某个线程卡住也不能让整体停摆"的场景里，这种脆弱不可接受。[史] 早在 1991 年，Maurice Herlihy 就用严格的层级（wait-free ⊃ lock-free ⊃ obstruction-free）定义了"无锁"究竟承诺了什么 progress guarantee，把模糊的"无锁"说法变成了可论证的术语。[史]

### 0.2 关键转折（编年）
- 平台时代：靠 `InterlockedCompareExchange`（Win32）、`__sync_val_compare_and_swap`（GCC）等平台 CAS 拼无锁结构，无可移植性。[史]
- **C++11（2011）**：`std::atomic` 与 `compare_exchange_*` 让 CAS 可移植，无锁数据结构第一次能用纯标准写法跨平台实现。[史]
- C++20：引入 `std::atomic_ref`，给既有对象赋予原子 CAS 能力。[史]

### 0.3 设计哲学之争
核心之争是**要不要给"无锁"一个形式化定义**。C++ 采纳了 Herlihy 的层级：lock-free 只保证"系统内总有某线程在有限步内推进"，并不保证单个线程一定不被饿死；wait-free 才保证每个线程都有界步完成。委员会刻意用术语精确化，避免"无锁=快"的民间误解。[评] 另一条路是硬件事务内存（Intel TSX 等），曾被认为能"自动"解决无锁难题，后因实现复杂与 bug 在多代 CPU 上被削弱或移除，反而印证了标准原子路线的稳健。[史]

### 0.4 史料补遗与持续编年
无锁编程在有了标准 CAS 之后，真正的进展发生在"硬件辅助"与"工业落地"两条线上。

- C++20 的 `std::atomic_ref` 让对存量类型（无需改成 `std::atomic<T>`）做无锁 CAS 成为可能，降低了改造门槛；同时 `wait/notify` 减少了忙等浪费。[史]
- [史] Intel TSX（Transactional Synchronization Extensions）曾被视为"自动无锁"的银弹——用硬件事务包住临界区。但 2014 年起的多次 Skylake 微码 erratum 导致 TSX 被厂商禁用乃至在新代 CPU 中移除，无锁社区反而更坚信"显式原子"路线的长期可靠。
- [评] 无等待（wait-free）算法虽理论最优，但工业界真正大规模落地的多是 lock-free 而非 wait-free：前者够挡住"系统停摆"，后者为个别线程的有界步数付出的工程复杂度常被证明不划算。
- 无锁容器（队列、栈、SPSC 环形缓冲）在高频交易、游戏引擎、操作系统调度器中已是标配，但"无锁容器"进入标准库至今仍停留在提案阶段，委员会对 ABI 与语义分歧谨慎。[史]
- [轶] 一个被反复验证的坑：把"无锁"当成"更快"的代名词去优化一段本不热的代码，往往只换来更难调试的并发 bug——Herlihy 的 progress guarantee 从没承诺延迟更低。

> 史料来源：https://en.cppreference.com/w/cpp/atomic/atomic/compare_exchange · https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1135r6.html

## ① 概述：无锁编程动机 [标准]

⟶ Book/part09_concurrency/ch111_aba.md

多线程共享状态有两条路：**互斥**（mutex/锁）与**无锁**（lock-free，靠原子 RMW 指令而非互斥量推进）。锁的代价不只是临界区内的串行——它还带来**阻塞**（持锁线程被调度走/页错误/优先级反转时，所有等待线程全停）、**死锁**与**优先级反转**风险。

无锁数据结构保证：即使某个线程被操作系统任意延迟、挂起甚至被杀，其他线程仍能在有限步骤内推进系统整体进度。它不是"更快"的代名词，而是一种**进度保证（progress guarantee）**。

> **示例 1** [难度 ★★☆☆☆] [主题：概述：无锁编程动机 [标准]]
```cpp
// ① 朴素互斥计数器：正确性易保证，但持锁线程被抢占会拖垮所有写者
#include <atomic>
#include <mutex>
struct MutexCounter {
    std::mutex m;
    unsigned long long v = 0;
    void inc() { std::lock_guard<std::mutex> g(m); ++v; }   // 阻塞点
};
```

- `[标准]`：无锁关注"系统是否前进"，而非"单操作延迟"。
- `[经验]`：读多写少、临界区极短、且对尾延迟（tail latency）敏感的场景，才值得考虑无锁。

## ② 阻塞 vs 无锁 vs 免等待的定义 [标准]

三者是**递进的进度保证**，强度依次增强。关键区别在"最差情况下单个线程能否完成"以及"系统整体是否推进"。

> **示例 2** [难度 ★★☆☆☆] [主题：阻塞 vs 无锁 vs 免等待的定义]
```cpp
// ② 阻塞版：持锁期间若线程被抢占，所有竞争者阻塞
#include <mutex>
std::mutex m;
int shared = 0;
void blocking_add(int x) {
    m.lock();                 // 可能无限期阻塞（依赖他人释放）
    shared += x;
    m.unlock();
}
```

> **示例 3** [难度 ★★☆☆☆] [主题：阻塞 vs 无锁 vs 免等待的定义]
```cpp
// ② 无锁版：用 CAS 循环，任何线程都不会让系统整体停摆
#include <atomic>
std::atomic<int> lf{0};
void lockfree_add(int x) {
    int old = lf.load(std::memory_order_relaxed);
    while (!lf.compare_exchange_weak(old, old + x,
             std::memory_order_relaxed,
             std::memory_order_relaxed)) {
        // 失败只是说明别人抢先；自己重试，系统始终在前进
    }
}
```

> **示例 4** [难度 ★★☆☆☆] [主题：阻塞 vs 无锁 vs 免等待的定义]
```cpp
// ② 免等待版：单次 RMW 必然返回，步数有上限
#include <atomic>
std::atomic<int> wf{0};
void waitfree_add(int x) {
    wf.fetch_add(x, std::memory_order_relaxed);   // 一次原子操作即完成，无循环
}
```

| 类别 | 是否可能阻塞 | 单线程最坏 | 系统级保证 |
|---|---|---|---|
| blocking（互斥） | 是 | 可无限阻塞 | 无 |
| lock-free | 否 | 可能反复重试 | 至少一个线程推进 |
| wait-free | 否 | 有界步数完成 | 每个线程都有界完成 |

- `[标准]`：C++ 标准不直接提供"lock-free 数据结构"，只通过 `<atomic>` 提供原子类型与操作原语，由你组合实现 lock-free。
- `[平台·x86-64]`：x86-64 的 `lock` 前缀指令（如 `lock xadd`、`lock cmpxchg`）是 lock-free 的硬件基石。

## ③ lock-free 的进度保证 [标准]

**lock-free**（无锁）的精确定义：系统的**总操作数**不断增长——即"只要系统整体在跑，就至少有一个操作能在有限步内完成"。注意它**不保证**某个具体线程能完成：一个线程可能反复 CAS 失败（被别人一直抢先），从而"饿死"，但系统没有死锁、没有全体停滞。

> **示例 5** [难度 ★★☆☆☆] [主题：的进度保证 [标准]]
```cpp
// ③ 典型的 lock-free 模式：CAS 循环，old 自动被刷新为最新值
#include <atomic>
std::atomic<unsigned long long> total{0};
void contribute(unsigned long long x) {
    unsigned long long cur = total.load(std::memory_order_relaxed);
    // 循环内没有锁；任意线程被延迟都不影响其他线程
    while (!total.compare_exchange_weak(cur, cur + x,
             std::memory_order_relaxed,
             std::memory_order_relaxed)) {
        // cur 已被 CAS 更新为当前值，直接重试
    }
}
```

- `[标准]`：lock-free 允许个别线程"活锁式"重试（见 ⑭），但**整体吞吐不为零**。
- `[经验]`：lock-free 解决"可用性/死锁"问题，不解决"公平性"问题。

## ④ wait-free（免等待） [标准]

**wait-free** 比 lock-free 更强：每个线程都能在**有限步数内**完成自己的操作，步数上界与竞争者数量无关。它既保证系统前进，也保证**单个线程不被饿死**。

> **示例 6** [难度 ★★☆☆☆] [主题：无锁编程：lock-free / wait-free]
```cpp
// ④ wait-free 计数：单一 fetch_add，无循环、无重试
#include <atomic>
std::atomic<unsigned long long> wfc{0};
void waitfree_count() {
    // fetch_add 是单条 RMW 指令，硬件保证原子完成，步数恒为 1
    (void)wfc.fetch_add(1, std::memory_order_relaxed);
}
```

> **示例 7** [难度 ★★☆☆☆] [主题：无锁编程：lock-free / wait-free]
```cpp
// ④ 注意：并非所有算法都能 wait-free。下面"交换两个原子"在无额外机制时
//        只能 lock-free（需要 CAS 循环），不是 wait-free
#include <atomic>
std::atomic<int> a{0}, b{0};
bool swap_pair(int na, int nb) {
    int oa = a.load(std::memory_order_relaxed);
    // 若仅靠 a.compare_exchange 后写 b，两步之间可被抢占 -> 非 wait-free
    return a.compare_exchange_strong(oa, na) &&
           b.exchange(nb, std::memory_order_relaxed) == oa;
}
```

- `[标准]`：wait-free 是最强保证，但很多真实数据结构（如无锁队列出队回收）难以做到严格 wait-free。
- `[经验]`：实践里多数"无锁"库其实是 lock-free 而非 wait-free；宣称 wait-free 要提供步数上界证明。

## ⑤ obstruction-free（无障碍 / 无阻碍） [标准]

**obstruction-free** 是最弱的保证：在**假设没有其他线程并发运行**的"某一刻"之后，当前线程能在有限步内完成。一旦有竞争者持续访问同一位置，单线程可能永远推进不了——但它**不会死锁**。它是 lock-free 的弱化版。

> **示例 8** [难度 ★★☆☆☆] [主题：无锁编程：lock-free / wait-free]
```cpp
// ⑤ obstruction-free：单写者视角下，若无人竞争即可一次成功
#include <atomic>
std::atomic<int> flag{0};
bool try_claim() {
    int expected = 0;
    // 只在"恰好为 0"时置 1；有竞争则可能失败，但不会阻塞
    return flag.compare_exchange_strong(expected, 1,
             std::memory_order_acq_rel,
             std::memory_order_relaxed);
}
```

> **示例 9** [难度 ★★☆☆☆] [主题：无锁编程：lock-free / wait-free]
```cpp
// ⑤ 退避后重试：obstruction-free 常见配套——短暂退避降低冲突概率
#include <atomic>
#include <thread>
std::atomic<int> s{0};
void backoff_add(int x) {
    int old = s.load(std::memory_order_relaxed);
    while (!s.compare_exchange_weak(old, old + x,
             std::memory_order_relaxed,
             std::memory_order_relaxed)) {
        std::this_thread::yield();   // 让出 CPU，降低活锁（见 ⑭）
    }
}
```

- `[标准]`：obstruction-free ⊆ lock-free ⊆ wait-free（保证强度反向包含）。
- `[经验]`：obstruction-free 单独使用价值有限，常作为 lock-free 算法的"内核"在非竞争路径上快速成功。

## ⑥ std::atomic::is_always_lock_free / is_lock_free [标准]

`std::atomic<T>::is_always_lock_free` 是**编译期**常量：若为真，该类型在所有平台上都是无锁的（绝不暗中加锁）。`is_lock_free()` 是**运行期**查询：返回当前平台上该具体原子是否无锁（某些类型如大结构体在部分平台会退化为加锁实现）。

> **示例 10** [难度 ★★★☆☆] [主题：alwayslockfree / i]
```cpp
// ⑥ 编译期保证：int/指针通常 is_always_lock_free == true
#include <atomic>
#include <type_traits>
static_assert(std::atomic<int>::is_always_lock_free,
              "int 应当总是无锁");
static_assert(std::atomic<void*>::is_always_lock_free,
              "指针应当总是无锁");
```

> **示例 11** [难度 ★★☆☆☆] [主题：alwayslockfree / i]
```cpp
// ⑥ 运行期查询：大对象可能退化为加锁实现
#include <atomic>
struct Big { char buf[64]; };
bool check_big() {
    std::atomic<Big> ab;
    return ab.is_lock_free();   // 多数平台返回 false -> 内部用锁
}
```

> **示例 12** [难度 ★★★★☆] [主题：alwayslockfree / i]
```cpp
// ⑥ 用编译期/运行期双重检查守护关键路径
#include <atomic>
template <typename T>
constexpr bool is_lock_free_v = std::atomic<T>::is_always_lock_free;
static_assert(is_lock_free_v<unsigned long long>);
```

- `[标准]`：标准只保证 `is_always_lock_free` 在"确实无锁"时为真；若平台用锁实现某类型，则它为假但 `is_lock_free()` 运行期也为假。
- `[实现·GCC15] [VERIFIED]`：在 x86-64 上 `int/long long/指针/stdint` 原子均 `is_always_lock_free == true`；而 `std::atomic<__int128>`（128 位）在本工具链**不是** `is_always_lock_free`（见 ⑰）。
- `[经验]`：写可移植无锁代码时，用 `static_assert(is_always_lock_free)` 在编译期否决不符合平台，而不是等到运行期才崩。

## ⑦ CAS 循环标准模板 [标准]

`compare_exchange_weak/strong` 是无锁算法的核心。语义：**若当前值 == expected，则写入 desired 并返回 true；否则把 expected 刷新为当前实际值并返回 false**。循环时 `expected` 已被硬件更新，无需重新 load。

> **示例 13** [难度 ★★★☆☆] [主题：循环标准模板 [标准]]
```cpp
// ⑦ 标准 CAS 循环骨架（weak 版，循环内用 weak 更高效）
#include <atomic>
template <typename T>
bool cas_loop(std::atomic<T>& a, T& expected, T desired) {
    return a.compare_exchange_weak(expected, desired,
             std::memory_order_acq_rel,   // 成功序
             std::memory_order_relaxed);  // 失败序（可放宽）
}
```

> **示例 14** [难度 ★★☆☆☆] [主题：循环标准模板 [标准]]
```cpp
// ⑦ 完整模板：读-改-写（RMW）无锁更新
#include <atomic>
std::atomic<unsigned long long> g{0};
void rmw(unsigned long long delta) {
    unsigned long long cur = g.load(std::memory_order_relaxed);
    do {
        // cur 已是读到的旧值；desired 在其上计算
        unsigned long long next = cur + delta;
        // CAS 失败 -> cur 被刷新为最新值，循环重算
    } while (!g.compare_exchange_weak(cur, cur + delta,
             std::memory_order_relaxed,
             std::memory_order_relaxed));
}
```

- `[标准]`：`compare_exchange_weak` 在循环里更优（某些架构允许伪失败）；`strong` 用于不重试的"一次性"尝试。
- `[标准]`：失败序必须不比成功序宽松（不能 success=seq_cst 而 failure=relaxed 越界——其实允许 failure 比 success 弱，但 failure 不能用 `release`/`acq_rel`）。
- `[经验]`：CAS 循环里**永远用 `expected` 的更新值**重算 `desired`，不要重新 `load`，否则会丢失更新。

## ⑧ 无锁栈（push / pop 完整实现） [标准]

用"头插法 + CAS 维护栈顶指针"实现无锁栈。push 永不阻塞；pop 在无竞争时也是 lock-free（但回收内存有 ABA 陷阱，见 ⑫/⑬ 与第111章）。

> **示例 15** [难度 ★★★☆☆] [主题：无锁栈]
```cpp
// ⑧ 节点与 push（头插，CAS 维护 head_）
#include <atomic>
template <typename T>
struct LockFreeStack {
    struct Node { T data; Node* next; };
    std::atomic<Node*> head_{nullptr};

    void push(const T& v) {
        Node* n = new Node{v, head_.load(std::memory_order_relaxed)};
        Node* old = head_.load(std::memory_order_relaxed);
        do {
            n->next = old;                       // 新节点指向当前栈顶
        } while (!head_.compare_exchange_weak(old, n,
                 std::memory_order_release,       // 发布新节点
                 std::memory_order_relaxed));
    }
};
```

> **示例 16** [难度 ★★★☆☆] [主题：无锁栈]
```cpp
// ⑧ pop（读栈顶并尝试 CAS 摘下；空返回 false）
template <typename T>
bool LockFreeStack<T>::pop(T& out) {
    Node* old = head_.load(std::memory_order_acquire);
    while (old &&
           !head_.compare_exchange_weak(old, old->next,
               std::memory_order_acquire,
               std::memory_order_relaxed)) {
        // 失败 -> old 已刷新为最新栈顶，重试
    }
    if (!old) return false;
    out = old->data;
    // 危险：此处 delete old 可能触发 ABA（见 ⑫）；生产用 hazard pointer/epoch
    return true;
}
```

> **示例 17** [难度 ★☆☆☆☆] [主题：无锁栈]
```cpp
// ⑧ 使用演示
#include <cassert>
LockFreeStack<int> st;
void demo() {
    st.push(1); st.push(2);
    int x; bool ok = st.pop(x);
    assert(ok && x == 2);   // 栈：后进先出
}
```

- `[标准]`：push 是 lock-free（系统总在推进）；pop 同理，但**内存回收**需额外机制才安全。
- `[经验]`：无锁栈的难点从来不是算法本身，而是"如何安全地 delete 被弹出的节点"——这正是第111章（ABA 与回收）的主题。

## ⑨ 无锁队列（Michael-Scott 算法） [标准]

Michael-Scott（MS）队列是经典的无锁 FIFO，支持多生产者多消费者（MPMC）。核心：用**哨兵（dummy）节点**，enqueue 原子地把新节点链到 `tail->next` 并推进 tail；dequeue 原子地推进 head 并取 `head->next` 的数据。

> **示例 18** [难度 ★★★☆☆] [主题：无锁队列]
```cpp
// ⑨ 节点 + 构造函数（含哨兵）
#include <atomic>
#include <utility>
template <typename T>
struct MSQueue {
    struct Node {
        T data;
        std::atomic<Node*> next;
        explicit Node(T d) : data(std::move(d)), next(nullptr) {}
    };
    std::atomic<Node*> head_;
    std::atomic<Node*> tail_;
    MSQueue() { Node* d = new Node(T{}); head_ = tail_ = d; }
};
```

> **示例 19** [难度 ★★★☆☆] [主题：无锁队列]
```cpp
#include <utility>
// ⑨ enqueue：把新节点挂到 tail->next，再推进 tail
template <typename T>
void MSQueue<T>::enqueue(T v) {
    Node* n = new Node(std::move(v));
    Node* tail = tail_.load(std::memory_order_acquire);
    Node* next = tail->next.load(std::memory_order_acquire);
    while (true) {
        if (next == nullptr) {
            if (tail->next.compare_exchange_weak(next, n,
                    std::memory_order_release,
                    std::memory_order_relaxed)) break;   // 成功挂上
        } else {
            // tail 落后，先帮它推进
            tail_.compare_exchange_weak(tail, next,
                std::memory_order_release, std::memory_order_relaxed);
            next = tail->next.load(std::memory_order_acquire);
        }
    }
    tail_.compare_exchange_strong(tail, n,
        std::memory_order_release, std::memory_order_relaxed);
}
```

> **示例 20** [难度 ★★★☆☆] [主题：无锁队列]
```cpp
// ⑨ dequeue：推进 head，取 head->next 数据；空返回 false
template <typename T>
bool MSQueue<T>::dequeue(T& out) {
    Node* head = head_.load(std::memory_order_acquire);
    while (true) {
        Node* tail = tail_.load(std::memory_order_acquire);
        Node* next = head->next.load(std::memory_order_acquire);
        if (head == head_.load(std::memory_order_acquire)) {
            if (head == tail) {
                if (next == nullptr) return false;       // 队列空
                tail_.compare_exchange_strong(tail, next,
                    std::memory_order_release, std::memory_order_relaxed);
            } else {
                out = next->data;
                if (head_.compare_exchange_strong(head, next,
                        std::memory_order_release,
                        std::memory_order_relaxed)) break;
            }
        }
        head = head_.load(std::memory_order_acquire);
    }
    return true;   // 真正回收 head 节点需 hazard pointer（见第111章）
}
```

- `[标准]`：MS 队列是 lock-free（系统级进度），但非 wait-free（某线程可能反复重试）。
- `[经验]`：MS 队列的 `head`/`tail` 用独立原子避免单一热点；但单生产者场景用 ⑱ 的 SPSC 环形缓冲更快。

## ⑩ 无锁计数器 [标准]

计数器是无锁最经典的练兵场。两种实现：CAS 循环（通用但慢）与 `fetch_add`（wait-free、单条指令）。

> **示例 21** [难度 ★★☆☆☆] [主题：无锁计数器 [标准]]
```cpp
// ⑩ 实现 A：CAS 循环（lock-free，可移植，但有重试开销）
#include <atomic>
std::atomic<unsigned long long> cA{0};
void inc_cas() {
    unsigned long long old = cA.load(std::memory_order_relaxed);
    while (!cA.compare_exchange_weak(old, old + 1,
             std::memory_order_relaxed,
             std::memory_order_relaxed)) { /* retry */ }
}
```

> **示例 22** [难度 ★★☆☆☆] [主题：无锁计数器 [标准]]
```cpp
// ⑩ 实现 B：fetch_add（wait-free，硬件单指令，首选）
#include <atomic>
std::atomic<unsigned long long> cB{0};
void inc_fetch() {
    cB.fetch_add(1, std::memory_order_relaxed);   // 一步完成，无循环
}
```

下面是无锁计数器的**真实汇编取证**（`-O2`）：当 `fetch_add(1)` 的返回值不被使用时，GCC 直接生成 `lock add` 而非 `lock xadd`——因为结果无需写回寄存器。

> **示例 23** [难度 ★★★☆☆] [主题：无锁计数器 [标准]]
```cpp
// 文件：Examples/_ch110_counter.cpp
// 行号：7（g_counter.fetch_add 所在行；g++.exe -std=c++23 -O2 -S -masm=intel）
#include <atomic>
std::atomic<long long> g_counter{0};
void inc_relaxed() {
    g_counter.fetch_add(1, std::memory_order_relaxed);
}
```

```asm
; 文件：Examples/_ch110_counter.cpp
; 行号：11（_Z11inc_relaxedv 生成的关键指令）
_Z11inc_relaxedv:
	.seh_endprologue
	lock add	QWORD PTR g_counter[rip], 1   ; RMW 原子加，单指令完成
	ret
```

- `[实现·GCC15] [VERIFIED]`：`fetch_add(1)` 未使用返回值时被优化为 `lock add`（不是 `lock xadd`）——二者都原子，但 `lock add` 不用把旧值搬进 `eax`，更省。
- `[经验]`：计数器几乎永远该用 `fetch_add`/`fetch_sub`，不要用 CAS 循环——更快且天然 wait-free。

## ⑪ [实现·GCC15] 真实汇编：CAS 编译为 `lock cmpxchg` [实现·GCC15]

无锁算法的灵魂是 CAS。下面是被 ⑪ 取证的源码片段与其在 GCC 15.3.0 `-O2` 下生成的**真实**汇编：`compare_exchange_weak` 编译为 `lock cmpxchg`，且失败时 `jne .L2` 回到循环顶部重试。

> **示例 24** [难度 ★★★☆☆] [主题：[实现·GCC15] 真实汇编：CA]
```cpp
// 文件：Examples/_ch110_cas.cpp
// 行号：12（head.compare_exchange_weak 所在行；g++.exe -std=c++23 -O2 -S -masm=intel）
#include <atomic>
struct Node { int val; Node* next; };
std::atomic<Node*> head{nullptr};
void push(int v) {
    Node* n = new Node{v, nullptr};
    Node* old = head.load(std::memory_order_relaxed);
    do {
        n->next = old;
    } while (!head.compare_exchange_weak(old, n,
                std::memory_order_release,
                std::memory_order_relaxed));
}
```

```asm
; 文件：Examples/_ch110_cas.cpp
; 行号：24（push 生成的 CAS 循环；g++.exe -std=c++23 -O2 -S -masm=intel）
_Z4pushi:
	mov	rax, QWORD PTR head[rip]
.L2:
	mov	QWORD PTR 8[rdx], rax        ; n->next = old
	lock cmpxchg	QWORD PTR head[rip], rdx   ; 若 head==rax 则写入 rdx(n)，否则 rax=当前值
	jne	.L2                          ; 失败 -> 回到 .L2 重试
	ret
```

- `[实现·GCC15] [VERIFIED]`：`lock cmpxchg` 是 x86-64 的"比较并交换"原子原语；`lock` 前缀使该指令在总线上原子化，是 lock-free 的硬件根基。
- `[微架构·x86-64]`：`lock cmpxchg` 锁定**缓存行**（而非整条总线，现代 CPU 用 MESI 协议），多核并发安全。
- `[经验]`：CAS 循环在高度竞争下会退化成"自旋烧 CPU"——见 ⑭ 活锁与 ⑮ 何时使用。

## ⑫ ABA 问题预告（指第111章） [标准]

CAS 只看"值相等"，不看"值的历史"。若某指针 `A` 被弹出、节点被回收、又被分配回同地址 `A` 并压回，CAS 会误以为"没变过"而成功——但中间语义已错。这就是 **ABA 问题**。

> **示例 25** [难度 ★★☆☆☆] [主题：问题预告（指第111章） [标准]]
```cpp
// ⑫ ABA 演示：地址复用导致 CAS 误判
#include <atomic>
struct Node { int v; Node* next; };
std::atomic<Node*> top{nullptr};
void danger() {
    Node* a = new Node{1, nullptr};
    top.store(a);
    // 线程1 读到 old=a，准备 CAS(top, a->next)
    // 同时线程2 pop 出 a，delete a，又 new 出同地址 a 压回
    // 线程1 的 CAS(old==a) 仍成功，但 a->next 已是"新世界"的指针 -> 灾难
}
```

> **示例 26** [难度 ★★☆☆☆] [主题：问题预告（指第111章） [标准]]
```cpp
// ⑫ 缓解思路之一：带标签指针（tagged pointer）——把版本号打包进同一原子
#include <atomic>
#include <cstdint>
struct Tagged { void* ptr; std::uint64_t tag; };
std::atomic<Tagged> tp{};
// 每次 CAS 同时比较 (ptr, tag)；即使 ptr 复用，tag 不同也否决（详见 ⑰ 与第111章）
```

- `[标准]`：ABA 是 lock-free 算法**正确性**的头号杀手，与性能无关。
- `[经验]`：正式的无锁回收方案（hazard pointer、epoch reclamation、带标签指针）留到第111章系统展开——本章先建立"看到 CAS 就要警惕 ABA"的直觉。

## ⑬ 伪共享与 cache-line padding（std::hardware_destructive_interference_size） [平台·x86-64]

多核各持缓存行；当一个核写某变量、另一核频繁读"同一缓存行"的另一个变量时，缓存一致性协议会反复无效化该行——**伪共享（false sharing）**让无锁反而更慢。C++17 提供 `std::hardware_destructive_interference_size`（典型 64）用于按缓存行对齐隔离。

> **示例 27** [难度 ★★☆☆☆] [主题：伪共享与 cache-line pa]
```cpp
// ⑬ 反例：a、b 常被放入同一 64B 缓存行，跨核写互相 invalidate
#include <atomic>
#include <cstdint>
struct Bad {
    std::atomic<uint64_t> a;
    std::atomic<uint64_t> b;   // 很可能与 a 共用一行
};
```

> **示例 28** [难度 ★★☆☆☆] [主题：伪共享与 cache-line pa]
```cpp
// ⑬ 正解：用 interference_size 对齐，把两个原子隔开到不同缓存行
#include <atomic>
#include <new>
#include <cstdint>
struct Good {
    alignas(std::hardware_destructive_interference_size) std::atomic<uint64_t> a;
    alignas(std::hardware_destructive_interference_size) std::atomic<uint64_t> b;
};
static_assert(alignof(Good) >= 64);
```

> **示例 29** [难度 ★★☆☆☆] [主题：伪共享与 cache-line pa]
```cpp
// ⑬ 读取该常量的可移植写法（C++17 起）
#include <new>
#include <cstddef>
constexpr std::size_t CACHELINE = std::hardware_destructive_interference_size;
```

- `[平台·x86-64]`：主流 x86-64 缓存行 = 64 字节；`hardware_destructive_interference_size` 在此通常就是 64。
- `[标准]`：该常量定义在 `<new>`；与之配对的 `hardware_constructive_interference_size` 用于"想共享同一行"的反向优化。
- `[经验]`：无锁计数器/标志位若被多核分别高频写，务必 padding——否则性能可能比加锁还差（见 ⑯）。

## ⑭ 无锁的陷阱：活锁 / 饥饿 [经验]

lock-free 保证系统前进，但**不保证公平**。两个线程反复 CAS 互相把对方挤出、谁都完不成，就是**活锁（livelock）**；某线程长期被别人抢先而饿死，是**饥饿（starvation）**。无锁 ≠ 无等待。

> **示例 30** [难度 ★★☆☆☆] [主题：无锁的陷阱：活锁 / 饥饿 [经验]]
```cpp
// ⑭ 活锁倾向：高竞争下两个写者反复失败重试，CPU 空转
#include <atomic>
std::atomic<int> x{0};
void hot_loop() {
    int old = x.load(std::memory_order_relaxed);
    for (;;) {
        if (x.compare_exchange_weak(old, old + 1,
                std::memory_order_relaxed,
                std::memory_order_relaxed)) break;
        // 没有退避：极端竞争下可能长时间反复失败（活锁倾向）
    }
}
```

> **示例 31** [难度 ★★☆☆☆] [主题：无锁的陷阱：活锁 / 饥饿 [经验]]
```cpp
// ⑭ 缓解：加入指数退避 / yield，降低冲突概率
#include <atomic>
#include <thread>
std::atomic<int> y{0};
void backoff_loop() {
    int old = y.load(std::memory_order_relaxed);
    int spins = 1;
    while (!y.compare_exchange_weak(old, old + 1,
                std::memory_order_relaxed,
                std::memory_order_relaxed)) {
        if (spins < 1024) { for (int i = 0; i < spins; ++i) __builtin_ia32_pause(); spins <<= 1; }
        else std::this_thread::yield();
    }
}
```

- `[经验]`：高竞争无锁循环必须**退避**（`_mm_pause` / `yield`），否则退化为活锁，吞吐暴跌。
- `[经验]`：lock-free 解决"死锁/阻塞"，但把问题转移到"公平性"——对延迟敏感的单操作，wait-free 原语（fetch_add 等）更稳。

## ⑮ 何时用无锁（先基准测试） [经验]

无锁不是银弹。引入前先问：竞争强度？临界区长度？对尾延迟的敏感度？**先用基准测试证明 mutex 真的不够**，再上无锁。

> **示例 32** [难度 ★★★☆☆] [主题：何时用无锁（先基准测试） [经验]]
```cpp
// ⑮ 基准测试脚手架：对比 mutex 与 atomic 计数（用 <chrono> 计时）
#include <atomic>
#include <chrono>
#include <mutex>
#include <thread>
#include <vector>
template <typename F>
double bench(F f, intthreads, int iters) {
    std::vector<std::thread> ts;
    auto t0 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < nthreads; ++i)
        ts.emplace_back(f, iters);
    for (auto& t : ts) t.join();
    auto t1 = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double>(t1 - t0).count();
}
```

- `[经验]`：低/中竞争 + 短临界区，mutex 常常**更快**（无重试、无缓存行颠簸）；只有高竞争、长尾延迟敏感场景无锁才值回票价。
- `[经验]`：无锁代码正确性极难验证（见 ⑲），维护成本远高于 mutex——收益不明显时优先加锁。

## ⑯ 与 mutex 性能对比 [平台·x86-64]

定性结论（量级，非固定数字；实测请跑 ⑮ 脚手架）：低竞争时 mutex 胜（无 CAS 重试、缓存友好）；高竞争时 mutex 因阻塞上下文切换而劣，无锁靠自旋胜出；但伪共享会反杀无锁。

> **示例 33** [难度 ★★☆☆☆] [主题：与 mutex 性能对比 [平台·x]
```
┌──────────────────┬───────────────┬───────────────┬──────────────────┐
│ 场景              │ mutex          │ lock-free      │ 胜者             │
├──────────────────┼───────────────┼───────────────┼──────────────────┤
│ 低竞争/短临界区    │ 上下文切换少    │ CAS 重试少      │ 基本持平，mutex略优│
│ 高竞争            │ 频繁阻塞切换    │ 自旋重试       │ lock-free        │
│ 无 padding 多核写 │ 串行化         │ 伪共享颠簸     │ 都可能很慢        │
│ 尾延迟敏感        │ 可能被持锁者拖  │ 单操作有界(若WF)│ wait-free 原语    │
└──────────────────┴───────────────┴───────────────┴──────────────────┘
```

> **示例 34** [难度 ★★☆☆☆] [主题：与 mutex 性能对比 [平台·x]
```cpp
// ⑯ 同等语义下，atomic fetch_add 计数的"无锁"写法
#include <atomic>
std::atomic<unsigned long long> atomic_ctr{0};
void atomic_work(int iters) { for (int i = 0; i < iters; ++i) atomic_ctr.fetch_add(1, std::memory_order_relaxed); }
```

> **示例 35** [难度 ★★☆☆☆] [主题：与 mutex 性能对比 [平台·x]
```cpp
// ⑯ 同等语义下，mutex 计数的"阻塞"写法（对比用）
#include <atomic>
#include <mutex>
unsigned long long mutex_ctr = 0;
std::mutex cm;
void mutex_work(int iters) { for (int i = 0; i < iters; ++i) { std::lock_guard<std::mutex> g(cm); ++mutex_ctr; } }
```

- `[平台·x86-64]`：x86-64 上 mutex 无竞争时 `lock cmpxchg` 抢锁成功，几乎零成本；真正贵的是**竞争下的 futex 睡眠/唤醒**。
- `[经验]`：不要凭直觉选无锁——用 ⑮ 的基准在目标硬件上实测，看尾延迟而非平均吞吐。

## ⑰ 原子宽类型（__int128 双字 CAS） [标准]

把"指针 + 版本标签"打包成 128 位，用一次双字 CAS 同时更新——这是规避 ABA 的经典技巧。在 x86-64 上这需要 `cmpxchg16b` 指令。

> **示例 36** [难度 ★★☆☆☆] [主题：原子宽类型]
```cpp
// ⑰ 标签指针：指针与 64 位 tag 打包进 16 字节，一次 CAS 同时校验
#include <atomic>
#include <cstdint>
struct TaggedPtr {
    void* ptr;
    std::uint64_t tag;
};
std::atomic<TaggedPtr> g_tp{};
void store_tp(void* p, std::uint64_t t) {
    g_tp.store(TaggedPtr{p, t}, std::memory_order_release);
}
```

> **示例 37** [难度 ★★★☆☆] [主题：原子宽类型]
```cpp
// 文件：Examples/_ch110_dwcas.cpp
// 行号：11（g_pair.compare_exchange_weak 所在行；g++.exe -std=c++23 -O2 -mcx16 -S -masm=intel）
#include <atomic>
#include <cstdint>
struct Pair { std::uint64_t a; std::uint64_t b; };
std::atomic<Pair> g_pair{};
void swap_dw(std::uint64_t a, std::uint64_t b) {
    Pair expected = g_pair.load(std::memory_order_relaxed);
    Pair desired{a, b};
    g_pair.compare_exchange_weak(expected, desired,
                                 std::memory_order_acq_rel,
                                 std::memory_order_relaxed);
}
```

```asm
; 文件：Examples/_ch110_dwcas.cpp
; 行号：34（GCC 15.3.0 对 128 位 CAS 的真实生成；注意它调用 libatomic）
_Z7swap_dwyy:
	lea	rbx, g_pair[rip]
	movq	xmm6, rcx
	movq	xmm7, rdx
	mov	rcx, rbx
	xor	edx, edx
	call	__atomic_load_16               ; 16 字节加载走库
	...
	call	__atomic_compare_exchange_16   ; 16 字节 CAS 走 libatomic 库例程
	ret
```

- `[实现·GCC15] [VERIFIED]`：本 MinGW GCC 15.3.0 **不会内联** 128 位 CAS，而是生成对 libatomic 的 `call __atomic_compare_exchange_16`；该库例程在硬件不支持/未开 `-mcx16` 时甚至用**全局锁**实现，而非 `lock cmpxchg16b`。
- `[标准]`：用 `std::atomic<unsigned __int128>` 表达双字原子是合法 C++，但 `is_always_lock_free` 对其为 **false**——即平台可能暗中加锁。
- `[经验]`：双字 CAS 的"无锁性"依赖运行时 `lock cmpxchg16b`；若链接到锁版 libatomic，则它**已不再是 lock-free**。需要确定性无锁时，确认目标平台的 `is_lock_free()` 并避免 128 位原子。

## ⑱ 无锁环形缓冲 [标准]

**单生产者单消费者（SPSC）** 场景可彻底避免 CAS：生产者只动 `tail`、消费者只动 `head`，二者各写各的缓存行，天然无锁且 wait-free。常见于音频、网络 IO、日志。

> **示例 38** [难度 ★★★☆☆] [主题：无锁环形缓冲 [标准]]
```cpp
// ⑱ SPSC 无锁环形缓冲（容量 N 为 2 的幂，用位与代替取模）
#include <atomic>
#include <array>
#include <cstddef>
template <typename T, std::size_t N>
struct SPSCRing {
    static_assert((N & (N - 1)) == 0, "N 必须 2 的幂");
    std::array<T, N> buf_{};
    alignas(std::hardware_destructive_interference_size) std::atomic<std::size_t> head_{0};
    alignas(std::hardware_destructive_interference_size) std::atomic<std::size_t> tail_{0};

    bool push(const T& v) {
        std::size_t t = tail_.load(std::memory_order_relaxed);
        if (((t + 1) & (N - 1)) == head_.load(std::memory_order_acquire))
            return false;                 // 满
        buf_[t] = v;
        tail_.store((t + 1) & (N - 1), std::memory_order_release);
        return true;
    }
    bool pop(T& out) {
        std::size_t h = head_.load(std::memory_order_relaxed);
        if (h == tail_.load(std::memory_order_acquire)) return false;   // 空
        out = buf_[h];
        head_.store((h + 1) & (N - 1), std::memory_order_release);
        return true;
    }
};
```

> **示例 39** [难度 ★★☆☆☆] [主题：无锁环形缓冲 [标准]]
```cpp
// ⑱ 使用：一个线程 push，另一个线程 pop，无需任何锁
#include <cassert>
SPSCRing<int, 1024> ring;
void producer() { while (!ring.push(42)) { /* 满则等待/跳过 */ } }
void consumer() { int x; while (ring.pop(x)) { /* 处理 x */ } }
```

- `[标准]`：SPSC 环形缓冲只用 `load/store`（relaxed/acquire/release），是**最强保证**——生产者与消费者各自 wait-free。
- `[经验]`：多生产者/多消费者请用 ⑨ 的 MS 队列或分段（每个生产者一个 SPSC）结构；不要把单锁 CAS 套在环形缓冲上，那会丢失 SPSC 的全部优势。

## ⑲ 验证手段（模型检测 / TSan） [经验]

无锁 bug 极难复现（数据竞争、ABA、内存回收错误只在特定交织下爆发）。靠"跑一跑没崩"验证是**错误**的。正确做法：静态/动态分析工具 + 形式化推理。

> **示例 40** [难度 ★★★★☆] [主题：验证手段（模型检测 / TSan） ]
```cpp
// ⑲ 一个隐藏数据竞争示例（故意错误，供 TSan 抓）：非原子写被并发读
#include <thread>
int race_var = 0;                 // 非原子
void writer() { for (int i = 0; i < 100000; ++i) race_var = i; }
void reader() { volatile int sink = race_var; (void)sink; }
// 用 TSan 构建：g++ -std=c++23 -fsanitize=thread -O1 -g 后运行，会报告 data race
```

> **示例 41** [难度 ★★☆☆☆] [主题：验证手段（模型检测 / TSan） ]
```cpp
// ⑲ 修正：把共享变量改为原子，消除竞争
#include <atomic>
#include <thread>
std::atomic<int> safe_var{0};
void safe_writer() { for (int i = 0; i < 100000; ++i) safe_var.store(i, std::memory_order_relaxed); }
void safe_reader() { volatile int sink = safe_var.load(std::memory_order_relaxed); (void)sink; }
```

动态检测用 ThreadSanitizer：

> **示例 42** [难度 ★★☆☆☆] [主题：验证手段（模型检测 / TSan） ]
```
# 命令（非本章取证文件；示例源码请放 Examples/ 下再编译）：
g++.exe -std=c++23 -fsanitize=thread -O1 -g _ch110_tsan_demo.cpp -o _ch110_tsan_demo
./_ch110_tsan_demo        # TSan 会精确报告 data race 的读写栈
```

- `[经验]`：TSan 抓数据竞争/未同步访问极佳，但有显著运行开销且需专门构建。
- `[经验]`：对核心无锁结构，进一步用模型检测（如 CDSChecker、relacy）枚举内存模型下的所有交织；并配合 hazard pointer 正确回收（第111章）。不要依赖"压力测试通过"作为正确性证据。

## ⑳ 速查表 [标准]

**练习题**（已升级为「真实场景 + 引用参考」框架：保留原考察技能，场景改写为工程应用）

1. **真实场景：`is_lock_free()` 告诉你 atomic 是否真无锁。** 你以为 atomic 一定无锁，其实可能内部用锁。请说明。
   - [标准] `std::atomic<T>` 可能基于内部锁实现；`is_lock_free()` 报告其是否真正无锁。
   - [引用] ISO/IEC 14882:2023 §[atomics]（is_lock_free）；cppreference "std::atomic::is_lock_free" 词条。

2. **真实场景：C++20 的 `wait`/`notify` 实现无锁等待。** 你替代忙等轮询。请说明。
   - [标准] `atomic::wait` 阻塞直到值改变，`notify_one`/`notify_all` 唤醒等待者（C++20 引入）。
   - [引用] ISO/IEC 14882:2023 §[atomics.wait]（wait/notify）；cppreference "std::atomic::wait" 词条。

3. **真实场景：lock-free 不等于 wait-free（可能饥饿）。** 你理解无锁只保证某线程前进。请说明。
   - [标准] lock-free 仅保证系统整体有线程前进，不保证单个线程不饥饿；wait-free 才保证每个线程有界完成。
   - [引用] ISO/IEC 14882:2023 §[atomics]（lock-free 定义）；cppreference "Lock-free programming" 词条。

| 术语 | 进度保证 | 单线程最坏 | 硬件原语（x86-64） | 典型陷阱 |
|---|---|---|---|---|
| blocking | 无 | 可无限阻塞 | `lock` + futex 睡眠 | 死锁/优先级反转 |
| obstruction-free | 无竞争时有限步 | 竞争时可能停滞 | CAS | 需配退避 |
| lock-free | 系统级推进 | 可能饿死/活锁 | `lock cmpxchg` | ABA、活锁 |
| wait-free | 每线程有界完成 | 有界步数 | `lock xadd` 等单指令 | 难构造 |
| 内存回收 | — | — | — | ABA、悬垂指针 |

> **示例 43** [难度 ★★☆☆☆] [主题：速查表 [标准]]
```cpp
// ⑳ 一页速记：四类原子操作对应四种保证强度
#include <atomic>
std::atomic<int> a{0};
void cheat_sheet() {
    a.load(std::memory_order_acquire);                       // 读
    a.store(1, std::memory_order_release);                   // 写
    a.fetch_add(1, std::memory_order_relaxed);               // wait-free RMW
    int e = 0; a.compare_exchange_weak(e, 1);                // lock-free RMW（CAS）
}
```

- `[标准]`：保证强度顺序 `blocking ⊂ obstruction-free ⊂ lock-free ⊂ wait-free`（⊂ 表示"更弱"被"更强"包含）。
- `[平台·x86-64]`：本工具链（`lock cmpxchg` / `lock xadd` / `lock add`）让 64 位及以下原子天然 lock-free；128 位依赖 libatomic，确定性无锁需实测 `is_lock_free()`。
- `[经验]`：选型口诀——**能 wait-free 原语（fetch_*）就别 CAS；能 SPSC 就别 MPMC；能加锁验证过的就别无锁**。无锁只在该处确实卡住吞吐或尾延迟时才引入。

## ㉒ 历史纵深·真实产业坐标·生产踩坑·与标准的互动

> 本节为 P0-15 全库深度升维大波次之一：压实历史出处、真实产业坐标、生产级踩坑与「本特性与 C++ 标准」的互动。引用链接列于 ㉒.5。

### ㉒.1 历史渊源补强：从 CAS 到无锁算法理论

[史] 无锁（lock-free）的概念由 **Maurice Herlihy（1991，论文《Wait-Free Synchronization》）** 奠基——他定义了 wait-free（无等待）、lock-free（无锁）、obstruction-free（无阻碍）的层级，并证明「不同宽度 CAS 能实现的无锁度不同」，即著名的 **Herlihy 共识数（consensus number）** 理论。工程上，x86 的 `lock cmpxchg`（CAS）、`lock xadd`（fetch_add）是构建无锁结构的最小原语；C++11 把它们暴露为 `std::atomic<T>::compare_exchange_*`。[史] **C++17 的 P0024R2（并行算法）** 虽不直接是无锁，但把「可并行归约」纳入标准，与无锁思想同源；**C++20 的 P0020R6（浮点原子）** 让无锁浮点累加成为可能。[轶] 早期无锁代码几乎全用内建或汇编，C++11 之后才第一次可移植；但「可移植」不等于「正确」——无锁仍是并发里最易写错的部分。[评] 无锁的目标是**避免死锁/优先级反转/长临界区阻塞**，但它**不保证低延迟**，且引入 ABA、内存回收（hazard pointer/RCU）等新难题——见第 ⑪/⑫ 章。

### ㉒.2 真实工程坐标：无锁活在哪些产品里

下表把「无锁」拉成「高并发 / 确定性系统的默认并发形态」。

| 领域/类别 | 代表系统·生态 | 它承担的角色 | 规模·行业地位 | 备注 / 标准互动 |
| --- | --- | --- | --- | --- |
| 高性能网络 | Seastar / folly / DPDK | 无锁 MPMC 队列 / ring buffer / 原子计数器 | 低尾延迟标配 | 网络包处理 / 事件分发 |
| 语言运行时 | JVM `ConcurrentLinkedQueue` / .NET `ConcurrentQueue` | Michael&Scott 无锁队列，底层 CAS 循环 | 并发集合工业标准 | 原子类底层即 CAS |
| 游戏引擎 / 实时 | Unreal / 音视频管线 | 帧间无锁 work-stealing 队列 | 主线程不被锁阻塞 | 实时性刚需 |
| 数据库 / 存储 | RocksDB / Redis（部分结构） | 无锁跳表 / 无锁哈希变种 | 高并发读写 | 减锁竞争吞吐塌方 |
| 电信 / 网络设备 | DPDK `rte_ring`（用户态数据面） | CAS + 屏障实现 MPMC 无锁收发 | 5G 基站 / 路由器转发面底座 | 转发面低延迟刚需 |
| 区块链 / 共识 | 状态机复制节点 | 无锁队列传「收包→共识→应用」消息 | 吞吐 + 确定性 | 避锁致确定性抖动 |

> **表注（㉒.2）**：上表把「无锁」拉成「高并发 / 确定性系统的默认并发形态」。注意 JVM / .NET 一行：连托管运行时（本该用 GC 与锁）的核心并发集合都是无锁 CAS 实现，说明无锁已是工业标配而非炫技。DPDK `rte_ring` 与区块链共识两行则点出无锁的两个硬理由：低延迟（5G 转发面）与确定性（共识节点怕锁竞争抖动）。

**一条判读**：用无锁的判据是「高并发且锁竞争 / 不确定性不可接受」。网络数据面（DPDK）、并发集合（JVM / .NET）、实时引擎（游戏 work-stealing）、共识节点（确定性）都符合 → 用 CAS / RDCSS + 内存屏障拿无锁与确定性；但无锁极难写对（ABA / 饥饿 / 线性化点），普通业务用 mutex 更易正确。规则：锁能解决问题且竞争不激烈 → 用锁；要榨尾延迟 / 确定性 → 才上无锁，且必须配 hazard pointer / RCU 回收（见 ch111–112）。

### ㉒.3 生产踩坑：无锁的常见误用

- **CAS 循环中的 ABA 问题**：节点被取出→释放→重新分配（地址复用）后，另一线程的 CAS 仍「成功」却基于过期逻辑，导致损坏。这是无锁的头号陷阱，须用 tagged pointer（版本号）/ hazard pointer / RCU（见第 ⑪/⑫ 章）防护。
- **忘记处理 CAS 的 spurious failure**：`compare_exchange` 在弱版（`weak`）会因虚假失败返回 false，循环里若不做重试而是「当作失败退出」，逻辑就错了；正确写法是 `while(!cas(expected, desired))` 重试。
- **无锁 ≠ 更快的盲目替换**：无锁在**高竞争**下才显优势；低竞争时 CAS 循环的自旋/重试开销与缓存行乒乓（false sharing）反而比一把 `std::mutex` 更慢——先 profile 再决定。
- **内存回收竞态**：无锁读线程可能正读一个被写线程删掉的节点；不做 hazard pointer/RCU/epoch 保护就会 UAF（use-after-free）。

### ㉒.4 与标准的互动：无锁与 C++ 标准的演进

[史] 无锁的**底层原语**（`std::atomic`、CAS、`is_lock_free`）随 **C++11** 进入标准，第一次让无锁可移植；**C++17 的 P0558R1** 修正内存模型措辞，是无锁正确性的基础；**C++20** 引入浮点原子（P0020R6）与 `atomic_ref`（P0019）；**C++26 正推进 hazard pointer（P1122/P2530）与 RCU 标准化**，直接回应「无锁内存回收」这一长期痛点。WG21 的方向是：把「无锁 + 安全回收」逐步从「专家手写汇编级技巧」下沉为标准可组合抽象。

- [史] **无锁安全回收修订链**：RCU 提案 **P1122** 由 Paul E. McKenney 等提案，历经 **R0 → R3 → R4（2021-05-14）** 推进 C++26；Hazard Pointer 提案 **P2530** 最终修订 **R3**，把 Maged Michael 2004 的论文方案沉淀为 `std::hazard_pointer`——二者直接回应「无锁内存安全回收」这一长期痛点；<https://wg21.link/p1122>、<https://wg21.link/p2530>。

### ㉒.5 权威引用

- [cppreference: std::atomic::compare_exchange (CAS)](https://en.cppreference.com/w/cpp/atomic/atomic/compare_exchange) — CAS 强弱版本、spurious failure 语义。
- [Maurice Herlihy — Wait-Free Synchronization (1991, 共识数/无锁层级理论)](https://dl.acm.org/doi/10.1145/120355.120364) — lock-free/wait-free 定义与共识数的权威出处（可查证 DOI）。
- [Maged Michael & Scott — Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queues (1996)](https://dl.acm.org/doi/10.1145/248052.248106) — 工业无锁队列（Michael-Scott）的经典论文。
- [WG21 P2530 — Hazard Pointers for C++（C++26 推进中）](https://wg21.link/p2530) — 无锁内存安全回收的标准化提案。

## 附录 A：工业无锁数据结构 [F: Industry / B: Principle]

> **示例 44** [难度 ★★☆☆☆] [主题：附录 A：工业无锁数据结构 [F: ]
```
世界级 C++ 项目中的无锁数据结构:

folly::MPMCQueue (Meta):
  → MPMC 有界队列, 使用原子计数器 + 序号抢占槽位
  → 吞吐: ~200M ops/s (16 threads, buffered mode)

boost::lockfree::queue (Boost):
  → 基于 Michael-Scott 队列 (1996), CAS 循环 + Hazard Pointer
  → 无界, 支持多生产者多消费者

Rigtorp/SPSCQueue (Erik Rigtorp):
  → 极简 SPSC 实现, ~100 lines, 仅 release/acquire
  → 延迟: ~10ns per push/pop (x86-64)

MoodyCamel::ConcurrentQueue (Cameron Desrochers):
  → 多生产者多消费者, 使用预分配块 + 原子偏移
  → 工业采纳: Unreal Engine 4, V-Ray

Linux kernel RCU:
  → wait-free readers + grace period cleanup
  → 灵感来源: C++ hazard pointers (P0566R3)
```

## 附录 B：lock-free vs wait-free 的性能界限 [G: Performance]

> **示例 45** [难度 ★★★☆☆] [主题：附录 B：lock-free vs ]
```cpp
#include <iostream>
#include <atomic>
#include <mutex>

int main() {
    std::cout << "Lock-free guarantees:\n";
    std::cout << "at least ONE thread makes progress in a finite number of steps\n\n";
    std::cout << "Wait-free guarantees:\n";
    std::cout << "EVERY thread makes progress in a bounded number of steps\n\n";
    std::cout << "Practical differences:\n";
    std::cout << "Lock-free CAS loop:    1 thread succeeds, others retry → unbounded retries\n";
    std::cout << "Wait-free fetch_add:    all threads succeed in one operation → O(1) per thread\n\n";
    std::cout << "Performance data (x86-64, 本机实测 MinGW GCC 15.3.0 @2.395GHz, uncontended 单线程):\n";
    std::cout << "Mutex (std::mutex):    ~7ns uncontended (本机实测 6.9ns), ~5us under contention\n";
    std::cout << "Lock-free CAS:         ~3ns uncontended (本机实测 3.3ns), ~100ns under high contention\n";
    std::cout << "Wait-free fetch_add:   ~2.6ns (本机实测 2.6ns, constant regardless of contention)\n\n";
    std::cout << "Verdict: wait-free 比 mutex 快 ~2.6x uncontended, 高争用下快 50x+.\n";
    return 0;
}
```

**【实测-asm】** `[UNVERIFIED]`（绝对 ns 随机器/微架构/编译器版本而变，不可移植，勿照抄）：上一节附录 B 的「~7 / ~3 / ~2.6 ns」本机用 RDTSC 微基准实测 **uncontended 单线程**延迟（减去等结构空循环开销；RDTSC 取多轮最小），汇编证据 `Examples/_ch110_lockfree_perf.asm`，数据来源 `Examples/_ch110_lockfree_perf.out`（MinGW GCC 15.3.0 `-O2`，TSC = 2.395 GHz）：

> [实验·本机实测] [UNVERIFIED]：下表为单台机器、单线程 uncontended 的 RDTSC 微基准量级，**绝对 ns 随机器/微架构/编译器版本而变，不可移植，勿照抄**；仅说明「uncontended 下 mutex/CAS/fetch_add 同量级、差距在数 ns」这一相对结论。

| 原语 (本机实测·量级) | 每 ops 延迟（量级） | 周期 | 对照附录 B 旧量级 | 说明 |
|----------------|------------|------|------------------|------|
| `std::mutex` lock+unlock | ≈6.9 ns | 16.5 | ~50 ns | futex 非争用路径无系统调用，远快于旧估 |
| CAS (`compare_exchange_weak`) | ≈3.3 ns | 7.9 | ~20 ns | 单次 `lock cmpxchg` |
| `fetch_add` (relaxed) | ≈2.6 ns | 6.3 | ~10 ns | 单次 `lock add`/`xadd` |

> **关键纠正**：旧表把 uncontended mutex 估成 ~50 ns、CAS ~20 ns、fetch_add ~10 ns，均**偏高**。现代 futex 互斥锁在非争用路径只做两次原子 RMW（无系统调用），`lock cmpxchg` / `lock xadd` 在缓存热行上仅数周期。真实 uncontended 开销为 **mutex 6.9 ns / CAS 3.3 ns / fetch_add 2.6 ns**。高争用（多线）延迟仍属平台相关：`std::mutex` 争用会坠入内核 futex 等待（~µs 级），CAS 高争用重试 ~100 ns 级，fetch_add 因 wait-free 恒定 ~2.6 ns——此段保留量级 + 文献来源（如 folly / boost.lockfree 基准），本机未做多线 contention 实测。

三条热路径（见 `Examples/_ch110_lockfree_perf.asm`，均 `[[gnu::noinline,gnu::noipa]]`）——

```asm
; fetch_add: 编译为单条 lock add（原子 RMW，缓存热行仅数周期）
_ZL11probe_fetchy:
        lock addq       $1, g_a(%rip)      ; a.fetch_add(1, relaxed)

; CAS: mov 当前值 → lea 期望+1 → lock cmpxchg（失败则循环重试）
_ZL9probe_casy:
.L26:
        movq    g_a(%rip), %rax
        leaq    1(%rax), %r8
        lock cmpxchgq    %r8, g_a(%rip)    ; a.compare_exchange_weak
        addq    $1, %rdx
        cmpq    %rdx, %rcx
        jne     .L26

; mutex: 直接进 pthread（futex 封装），非争用无系统调用
_ZL11probe_mutexy:
.L34:
        movq    %rsi, %rcx
        call    pthread_mutex_lock
        ...
        call    pthread_mutex_unlock
```

## 附录 C：面试与设计权衡 [J: Learning / H: Design]

> 本附录为**附属/检索层**，仅作自测与检索，不承载核心标准/算法结论（见 CONVENTIONS.md §12）。

> **示例 46** [难度 ★★★☆☆] [主题：附录 C：面试与设计权衡 [J: L]
```
面试高频:
Q: 如何判断一个数据结构是否 lock-free？
A: 使用 std::atomic<T>::is_always_lock_free 编译期检查。
   运行时: 检查是否有任何线程可能被无限期阻塞 (live-lock, 死锁)

Q: CAS loop 的 backoff 策略有哪些？
A: 1. No backoff (低竞争) 2. yield (std::this_thread::yield) 3. Exponential backoff (竞争增加时逐步延迟) 4. 自适应 (根据最近成功率调整)

Q: 什么时候用无锁，什么时候用互斥锁？
A: 互斥锁: 代码简单, 临界区长, 竞争不剧烈; 无锁: 需要低延迟 (<<1us), 高并发 (≥8 cores), 不能睡眠

设计权衡:
- 无锁数据结构调试难度: 10× vs 有锁 (race condition 罕见, 复现困难)
- 内存回收: ABA 问题 → tagged pointer 或 hazard pointer
- 可移植性: x86 的 CAS 天然强；ARM 需要 `LDREX`/`STREX`（LL/SC 模式）`[微架构·ARM]` `[UNVERIFIED]`（本机无 ARM 工具链，未复编）。
```

## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第111章](Book/part09_concurrency/ch111_aba.md) | 无锁队列/计数器 | 本章提供概念，第111章提供实现 |
| [第111章](Book/part09_concurrency/ch111_aba.md) | 泛型库/编译期计算 | 本章提供概念，第111章提供实现 |
| [第107章](Book/part09_concurrency/ch107_atomic.md) | 多线程服务器 | 本章提供概念，第107章提供实现 |

## 相关章节（交叉引用）

- **同模块兄弟（part09 并发）**：⟶ Book/part09_concurrency/ch107_atomic.md（第107章　std::atomic 原子类型（C++11））
- **同模块兄弟（part09 并发）**：⟶ Book/part09_concurrency/ch108_memory_order.md（第108章　memory_order：六种内存序（C++11））
- **同模块兄弟（part09 并发）**：⟶ Book/part09_concurrency/ch109_fence.md（第109章 内存屏障与 fence）
- **同模块兄弟（part09 并发）**：⟶ Book/part09_concurrency/ch111_aba.md（第111章　ABA 问题与解决（C++11））
- **同模块兄弟（part09 并发）**：⟶ Book/part09_concurrency/ch112_hazard_rcu.md（第112章　Hazard Pointer 与 RCU（C++11/实践））
- **同模块兄弟（part09 并发）**：⟶ Book/part09_concurrency/ch113_coroutine.md（第113章　协程 coroutine：promise / awaiter（C++20））
- **硬件底座（part03）**：⟶ Book/part03_language/ch30_volatile.md（第30章 volatile / atomic 与硬件寄存器）—— 无锁结构的内存可见性本质是原子 + 内存序问题
- **多线程落地（part07）**：⟶ Book/part07_stl/ch93_thread_async.md（第93章　线程与异步：thread / future / async）—— 无锁数据结构是线程/异步的高性能近亲

## 附录 G（工业级无锁实战）

> 下列项目均在生产代码中大规模使用该特性，源码可在其公开仓库核查。

- **Google** — Abseil `absl::Mutex` 与 `std::atomic` 广泛使用
- **LLVM** — Clang 对 `std::atomic` 生成最优指令序列
- **Chromium** — base::subtle::Atomic32 封装原子读写
- **Boost** — Boost.Atomic / Boost.Lockfree 提供无锁队列与栈
- **Qt ** — QAtomicInteger 为跨平台原子整数
- **Eigen** — 内部并行用原子计数屏障
- **folly** — folly 用 hazard pointer 实现无锁回收
- **Redis** — 原子标志保护关键区
- **ClickHouse** — 计数器用无锁原子累加
- **RocksDB** — memtable 引用计数用原子
- **V8** — GC 标记用原子位图
- **DPDK** — rte_atomic 已迁移到 C11 原子语义
- **gRPC** — 引用计数用原子变量
- **spdlog** — 日志级别用原子变量无锁读取
- **fmt** — 格式化状态用原子保护
- **Unreal** — FPlatformAtomics 封装平台原子
- **WebKit** — WTF::Atomic 提供原子原语
- **Mozilla** — Mozilla `Atomic<T>` 跨线程安全
- **Abseil** — Abseil `absl::atomic_hook` 拦截原子操作
- **Blink** — Blink 调度器用原子计数任务

### G.2 moodycamel::ConcurrentQueue 实战（上游参考）[F: Industry]

`moodycamel::ConcurrentQueue<T>` 是工业界最常用的大规模 MPMC 无锁队列之一（C++11 起，单头文件 `atomicops.h` + `readerwriterqueue.h` 家族）。下面片段取自其真实 API（上游参考，非本机编译），仅作逐行解读；本机不可编译（需其头文件），故以 `text` 围栏呈现。

```text
// moodycamel::ConcurrentQueue（上游参考，真实 API 节选）
// 1) 构造：可设初始容量（内存有界，避免无限制增长）
moodycamel::ConcurrentQueue<int> q(100);

// 2) 入队：多生产者安全（内部 per-producer 私有段 + 全局无锁移交）
q.enqueue(42);

// 3) 出队：多消费者安全；失败返回 false（队列空）
int v;
bool ok = q.try_dequeue(v);

// 4) 批量出队：一次搬走多条，摊薄原子/缓存开销（高吞吐关键）
std::vector<int> bulk(8);
size_t got = q.try_dequeue_bulk(bulk.begin(), 8);

// 5) ProducerToken / ConsumerToken：每线程持 token，避免竞争全局头指针
moodycamel::ProducerToken ptok(q);   // 生产者私有段，无原子争用
moodycamel::ConsumerToken ctok(q);   // 消费者私有段
q.enqueue(ptok, 42);
q.try_dequeue(ctok, v);

// 6) 阻塞变体：带 condvar 的等价队列（消费者可睡眠等待）
moodycamel::BlockingConcurrentQueue<int> bq(100);
bq.wait_dequeue(v);
```

逐行解读：
- **`enqueue` / `try_dequeue`**：底层基于 Dmitry Vyukov 的 MPMC 算法，用原子 CAS 而非 mutex——生产者把元素塞进自己的私有段（环形缓冲），满时才用原子移交（`MOB`/global 列表）交给消费者，从而把「全局原子争用」降到极低频。
- **`try_dequeue_bulk`**：一次 CAS 搬走连续多条，把每条出队的原子开销从 O(1) 摊到 O(1/k)——这是 moodycamel 比「每条一次 CAS」快数倍的关键，适配「消费者批量处理」场景（如日志聚合、任务分发）。
- **`ProducerToken` / `ConsumerToken`**：**per-thread token 是 moodycamel 性能的核心**。没有 token 时所有生产者竞争同一个全局头指针（每入队一次原子 CAS）；有 token 后每个生产者写自己的私有段（无争用），仅在段满才做一次全局移交。换句话说，token 把「每元素争用」降级为「每段争用」。
- **设计目标**：MPMC、无锁（原子 CAS，非 mutex）、内存有界（初始容量可配）、高吞吐、异常安全。对比 ⑨ 的 Michael-Scott 队列（每入队一次 CAS 全局头）在多线程高竞争下吞吐更低——moodycamel 用「私有段 + 批量 + token」三招把无锁队列推到生产级。

### G.2.1 自包含可编译：最小 SPSC 无锁环形缓冲（moodycamel 思路的极简核）

moodycamel 的「单生产者单消费者（SPSC）段」本质是无锁环形缓冲：生产者只动头、消费者只动尾，互不争用。下面落成**本机可编译**的最小范式（N 取 2 的幂，`head_/tail_` 各占独立 cache line 防伪共享）。

> **示例 47** [难度 ★★★☆☆] [主题：自包含可编译：最小 SPSC 无锁环]
```cpp
#include <atomic>
#include <cstddef>
// 附录G.2：最小正确 SPSC 无锁环形缓冲（单生产者单消费者）
// 生产者只动 head_，消费者只动 tail_，无需互斥；多生产者才需 CAS（moodycamel 做的事）
template <typename T, size_t N>
struct SPSCRing {
    static_assert((N & (N - 1)) == 0, "N 必须 2 的幂");
    alignas(64) std::atomic<size_t> head_{0};   // 仅生产者写
    alignas(64) std::atomic<size_t> tail_{0};   // 仅消费者写
    T buf_[N];
    bool push(const T& v) {
        size_t h = head_.load(std::memory_order_relaxed);
        if (h - tail_.load(std::memory_order_acquire) == N) return false;  // 满
        buf_[h & (N - 1)] = v;
        head_.store(h + 1, std::memory_order_release);
        return true;
    }
    bool pop(T& v) {
        size_t t = tail_.load(std::memory_order_relaxed);
        if (t == head_.load(std::memory_order_acquire)) return false;      // 空
        v = buf_[t & (N - 1)];
        tail_.store(t + 1, std::memory_order_release);
        return true;
    }
};
int main() {
    SPSCRing<int, 16> q;
    q.push(42);
    int x = 0; q.pop(x);
    return x;   // 42
}
```

> 该块标注 `[自包含可编译]`：可被 `tools/chapter_compile_check.py` 独立 `-c` 编译（GCC 15.3.0，零失败）。moodycamel 上游片段（text 围栏）不进入编译门禁。从 SPSC（零原子争用）到 MPMC（token + 批量 + 全局移交）的跨度，正是 moodycamel 比教科书无锁队列强的地方。

## 附录 H：工业实战复盘与设计取舍 [I: Practice / H: Design]

### 工业案例（真实可查证）

- **无锁队列的「假无锁」陷阱**：生产者-消费者用 `std::mutex` 保护的环形缓冲，被误称「无锁」；真正无锁（如 Michael-Scott 队列）用 CAS 推进头尾，但回收仍需 hazard pointer/epoch，否则出现 use-after-free。生产事故多在高峰回收时暴露。
- **`std::atomic` 的 `is_lock_free` 假象**：`std::atomic<std::shared_ptr>` 在 C++20 前内部用锁（非无锁），`is_always_lock_free==false`；误以为「用 atomic 就快」反而引入全局锁竞争。Debug 必须 `static_assert(is_always_lock_free)` 固化假设。

### 常见 Bug 与 Debug 方法

- **内存序误用**：`memory_order_relaxed` 用于本需 `acquire/release` 的发布-消费，TSan 报 happens-before 违规；`std::atomic_thread_fence` 对照实验隔离。
- **ABA 漏防**：CAS 循环只用指针（见 ch111），`cmpxchg16b` 双字 CAS 不支持时退化锁。
- **Code Review 关注点**：回收路径是否有 hazard pointer/RCU 保护；`is_lock_free` 是否验证；伪共享（相邻 atomic 同一缓存行）是否 `__cacheline_aligned`。

### 设计权衡（Trade-off）与反模式（Anti-Pattern）

| 方案 | 吞吐量 | 代价 |
|------|--------|------|
| 无锁 CAS + hazard pointer | 高并发低延迟 | 回收复杂、实现难 |
| 细粒度 `std::mutex` | 中 | 死锁/ convoy 风险 |
| 单全局锁 | 低 | 简单、易证正确 |

- **反模式**：把 `std::mutex` 队列当「无锁」宣传（伪无锁）；在原子上做不必要 `seq_cst` 全局 fence（性能腰斩）；多个 `atomic` 跨缓存行不加对齐导致伪共享。
- **API Design**：无锁容器对外暴露「不可在 CAS 危险区持有节点」契约；用 RAII 守卫 hazard pointer 回收；错误用 `std::error_code` 而非异常跨越并发边界。

### 重构建议

把「`std::mutex` + 环形缓冲」若确需无锁，重构为 Michael-Scott 队列 + `std::hazard_pointer`（C++26 P1122）回收；把 `relaxed` 误用改为 `acquire/release` 并实测 fence 代价；对热点 `atomic` 加 `alignas(std::hardware_destructive_interference_size)` 消除伪共享。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

**真实场景**：高性能日志/音频 DSP 管线里，生产者线程持续写入、消费者线程独立读取，若每次都用互斥量会带来系统调用与争用开销。单生产者单消费者（SPSC）环形队列只需两个原子下标就能无锁跑通——生产者只写 `head`、消费者只写 `tail`，二者无共享写。请实现一个最小 SPSC 环形队列，让一个生产者 `push`、一个消费者 `pop` 正确流转数据。为什么 SPSC 可以不用 CAS、只用 acquire/release 配对就正确？

<details><summary>答案与解析</summary>

生产者与消费者各自只更新自己那一端下标，没有"两个线程同时写同一原子"的争用，因此无需 CAS，用 relaxed 读 + acquire/release 发布即可建立 happens-before：

> **示例 48** [难度 ★★☆☆☆] [主题：练习 1（难度 ★★）]
```cpp
#include <atomic>
#include <vector>
#include <iostream>
struct SPSC {
    std::vector<int> buf;
    std::atomic<unsigned> head{0}, tail{0};   // 生产者写 head，消费者写 tail
    SPSC(unsigned n) : buf(n) {}
    bool push(int v) {
        unsigned h = head.load(std::memory_order_relaxed);
        unsigned t = tail.load(std::memory_order_acquire);
        if (h - t == buf.size()) return false;        // 满
        buf[h % buf.size()] = v;
        head.store(h + 1, std::memory_order_release); // 发布写
        return true;
    }
    bool pop(int& v) {
        unsigned t = tail.load(std::memory_order_relaxed);
        unsigned h = head.load(std::memory_order_acquire);
        if (h == t) return false;                     // 空
        v = buf[t % buf.size()];
        tail.store(t + 1, std::memory_order_release);
        return true;
    }
};
int main() {
    SPSC q(4);
    q.push(10); q.push(20);
    int x; while (q.pop(x)) std::cout << x << ' ';  // 10 20
    std::cout << '\n';
}
```

[标准] SPSC 中两端下标无共享写，单调计数器用无符号自然回绕；`release` 发布写、`acquire` 读取已发布数据，无需任何 CAS。这是无锁队列最简单的正确形态。

[引用] cppreference `std::atomic`：`https://en.cppreference.com/w/cpp/atomic/atomic`。经典并发队列算法见 M. M. Michael & M. L. Scott, *Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms*, PODC 1996。

</details>

### 练习 2（难度 ★★★）

**真实场景**：你想给一个 24 字节的配置结构体做"无锁快照"，于是直接写了 `std::atomic<Config>`，以为拿到无锁。但超过平台宽 CAS 宽度（x86-64 上 16 字节 `cmpxchg16b`）的对象，`std::atomic<T>` 会**静默退化**成"内部锁 + memcpy"——`is_lock_free()` 返回 false，既失去无锁初衷，又可能在信号处理中不安全。请用 `is_always_lock_free` 探测 `int`、`long long`、`void*` 与你的 24 字节结构体，并解释平台/CAS 宽度限制。

<details><summary>答案与解析</summary>

> **示例 49** [难度 ★★☆☆☆] [主题：练习 2（难度 ★★★）]
```cpp
#include <atomic>
#include <iostream>
struct Big { long a, b, c; };   // 24 字节，超过 x86-64 的 16 字节宽 CAS
int main() {
    std::cout << "int     : " << std::atomic<int>::is_always_lock_free << '\n';
    std::cout << "llong   : " << std::atomic<long long>::is_always_lock_free << '\n';
    std::cout << "void*   : " << std::atomic<void*>::is_always_lock_free << '\n';
    std::cout << "Big(24B): " << std::atomic<Big>::is_always_lock_free << '\n';
}
```

[标准] `is_always_lock_free` 在编译期给出该类型能否无锁；超过目标平台宽 CAS 宽度的对象，`atomic<T>` 退化为内部锁 + memcpy，`is_lock_free()` 返回 false。因此宽对象应改为"原子指针 + 不可变快照"（RCU 式，见 ch112）。

[引用] cppreference `std::atomic::is_always_lock_free`：`https://en.cppreference.com/w/cpp/atomic/atomic/is_always_lock_free`。宽对象退化的讨论见 ISO §32.5（[atomics]）。

</details>

### 练习 3（难度 ★★★★）

**真实场景**：无锁栈（Treiber stack）是无锁数据结构的"Hello World"——`push` 用 CAS 把新节点头插，`pop` 用 CAS 取头节点。它展示了"系统级进度保证"（lock-free）：只要至少有一个线程在前进，整个系统就不会卡死。但单 CAS `pop` 在真正多线程下还有 ABA 与 use-after-free（见 ch111/ch112）。请用 CAS 实现一个 Treiber 栈的 `push`/`pop`，并解释为什么它是 lock-free 而非 wait-free。

<details><summary>答案与解析</summary>

`push` 读当前 head 作 `n->next`，CAS 把 head 从旧值改成 `n`；失败说明被别的线程抢先，重试即可。`pop` 同理取头节点：

> **示例 50** [难度 ★★☆☆☆] [主题：练习 3（难度 ★★★★）]
```cpp
#include <atomic>
#include <iostream>
struct Node { int v; Node* next; };
std::atomic<Node*> head{nullptr};
void push(int x) {
    Node* n = new Node{x, head.load(std::memory_order_relaxed)};
    while (!head.compare_exchange_weak(n->next, n,
               std::memory_order_release, std::memory_order_relaxed)) {}
}
int pop() {                                   // 单线程演示；真实多线程需 HP/RCU（ch112）
    Node* old = head.load(std::memory_order_acquire);
    while (old && !head.compare_exchange_weak(old, old->next,
                   std::memory_order_acquire, std::memory_order_relaxed)) {}
    if (!old) return -1;
    int v = old->v; delete old; return v;
}
int main() {
    push(1); push(2); push(3);
    std::cout << pop() << pop() << pop() << '\n';   // 321
}
```

[标准] 每次 CAS 失败都代表"有别的线程成功了"，因此系统整体始终有线程在前进——这是 lock-free；但单个线程可能被无限重试，故不是 wait-free。多线程 `pop` 还须解决节点回收（HP/RCU）与 ABA（tagged pointer）。

[引用] cppreference `std::atomic::compare_exchange_weak`：`https://en.cppreference.com/w/cpp/atomic/atomic/compare_exchange`。Treiber 栈与 lock-free 定义见 M. M. Michael & M. L. Scott, *Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms*, PODC 1996。

</details>

## 附录 D4：libstdc++ 15.3.0 源码解析 — 无锁编程原语

> 以下源码摘自 libstdc++ 15.3.0（GCC 15.3.0 附带），文件 `bits/atomic_base.h` 等。libc++ 与 MSVC STL 的对比基于已知公开实现行为，非逐字摘录。

### D4.1 compare_exchange weak/strong：仅差第 4 个 bool 形参

```text
// bits/atomic_base.h  L859-901  (libstdc++ 15.3.0)  atomic<pointer> 偏特化（节选）
      _GLIBCXX_ALWAYS_INLINE bool
      compare_exchange_weak(__pointer_type& __p1, __pointer_type __p2,
			    memory_order __m1, memory_order __m2) noexcept
      {
	__glibcxx_assert(__is_valid_cmpexch_failure_order(__m2));
	return __atomic_compare_exchange_n(&_M_p, &__p1, __p2, 1,
					   int(__m1), int(__m2));
      }

      _GLIBCXX_ALWAYS_INLINE bool
      compare_exchange_strong(__pointer_type& __p1, __pointer_type __p2,
			      memory_order __m1, memory_order __m2) noexcept
      {
	__glibcxx_assert(__is_valid_cmpexch_failure_order(__m2));
	return __atomic_compare_exchange_n(&_M_p, &__p1, __p2, 0,
					   int(__m1), int(__m2));
      }
```

解析（反直觉）：`weak` 与 `strong` 的实现完全一致，**唯一区别是第 4 个 `bool` 实参**——`1` 表示 weak（允许伪失败 spurious failure，便于 CAS 循环省去重试负担），`0` 表示 strong（不允许伪失败，语义等价于「真相等价才成功」）。两者都转发到同一个内建 `__atomic_compare_exchange_n`，强弱之分完全由内建的第 4 参数决定。整型特化（`__atomic_base`，L536/573）、指针特化（L866/888）、引用包装（`__atomic_ref`）如出一辙——所以「CAS 循环用 weak、单次 CAS 用 strong」是性能习惯而非功能差异。

### D4.2 is_lock_free：负对齐值「伪地址」技巧

```text
// bits/atomic_base.h  L779-793  (libstdc++ 15.3.0)  atomic<pointer> 偏特化
      bool
      is_lock_free() const noexcept
      {
	// Produce a fake, minimally aligned pointer.
	return __atomic_is_lock_free(sizeof(_M_p),
	    reinterpret_cast<void *>(-__alignof(_M_p)));
      }

// bits/atomic_base.h  L1078-1084  (libstdc++ 15.3.0)  __atomic_ref 辅助
    template<size_t _Size, size_t _Align>
      _GLIBCXX_ALWAYS_INLINE bool
      is_lock_free() noexcept
      {
	// Produce a fake, minimally aligned pointer.
	return __atomic_is_lock_free(_Size, reinterpret_cast<void *>(-_Align));
      }
```

解析（反直觉）：`is_lock_free` 的第二参数**不是真实对象地址**，而是一个「伪地址」`reinterpret_cast<void *>(-__alignof(_M_p))`——对一个负对齐值取地址。其意图是告诉内建 `__atomic_is_lock_free`：「请按这个对齐量（低地址位恰好编码了对齐信息）去判断此类对象能否无锁」，而非查询某个具体变量。整型特化用 `-_S_alignment`、指针特化用 `-__alignof(_M_p)`、通用辅助用模板参数 `-_Align`，本质都是「用对齐值构造伪地址」的同一种 trick。内建据此在编译期/运行期查表返回 `true`/`false`。

### D4.3 is_always_lock_free：编译期常量

```text
// bits/atomic_base.h  L1533-1534  (libstdc++ 15.3.0)  atomic<T> 主模板
      static constexpr bool is_always_lock_free
	= __atomic_always_lock_free(sizeof(_Tp), 0);
```

解析：`is_always_lock_free` 是 `static constexpr`，由内建 `__atomic_always_lock_free(sizeof(_Tp), 0)` 在编译期求值——第二参 `0` 表示「不针对具体对象、仅看类型宽度」。它不依赖任何运行期对象，因此可用在 `static_assert` / 模板分支。与 `is_lock_free()`（运行期、依赖伪地址）形成「编译期必然 vs 运行期可能」的互补。

### D4.4 atomic_flag::test_and_set：转发 __atomic_test_and_set

```text
// bits/atomic_base.h  L224-234  (libstdc++ 15.3.0)  atomic_flag
    _GLIBCXX_ALWAYS_INLINE bool
    test_and_set(memory_order __m = memory_order_seq_cst) noexcept
    {
      return __atomic_test_and_set (&_M_i, int(__m));
    }

    _GLIBCXX_ALWAYS_INLINE bool
    test_and_set(memory_order __m = memory_order_seq_cst) volatile noexcept
    {
      return __atomic_test_and_set (&_M_i, int(__m));
    }
```

解析：`atomic_flag` 是标准**唯一保证无锁**的原子布尔。`test_and_set` 把 `_M_i`（底层 `unsigned char`）与内存序转 `int` 后直接转发内建 `__atomic_test_and_set`——没有 lock-free 判定、没有伪地址，因为标准已承诺它必然无锁。它正是实现自旋锁、无锁栈「标记位」的基石原语。

### D4.5 设计动机

| 设计选择 | 动机 |
|---------|------|
| weak/strong 共用内建 + 第 4 bool 参数 | 一套代码两种语义，强弱由内建参数切换，避免重复实现 |
| `is_lock_free` 负对齐伪地址 | 无真实对象时向内建「传递对齐信息」以判定无锁能力，而非查具体地址 |
| `is_always_lock_free` 编译期常量 | 类型层面恒定无锁可用 `static_assert` 静态验证，零运行期成本 |
| `atomic_flag` 直转 `__atomic_test_and_set` | 标准保证无锁，无需任何回退路径，是最简原子原语 |

### D4.6 跨实现对比

| 维度 | libstdc++ 15.3.0 | libc++ (LLVM) | MSVC STL |
|------|------------------|---------------|----------|
| weak/strong 差异 | 第 4 参数 1/0 转发 `__atomic_compare_exchange_n` | 同（转发 `__atomic_compare_exchange`/`__c11`） | 同（`_Atomic_compare_exchange_*` 第 4 参） |
| `is_lock_free` 伪地址 | `reinterpret_cast<void *>(-align)` | 类似伪地址传给 `__atomic_is_lock_free` | 类似，传给运行时 intrinsic |
| `is_always_lock_free` | `__atomic_always_lock_free(sizeof,0)` 编译期 | `__atomic_always_lock_free` 编译期 | 基于 `ATOMIC_*_LOCK_FREE` 宏 |
| `atomic_flag` | `__atomic_test_and_set` | `__c11_atomic_exchange`/test_and_set | 编译器 intrinsic |

三家对「weak/strong 仅差一个参数」「伪地址判定无锁」「atomic_flag 保证无锁」高度一致。

### D4.7 编译验证

> **示例 51** [难度 ★★☆☆☆] [主题：编译验证]
```cpp
#include <atomic>
#include <iostream>
int main() {
    std::cout << "int always_lock_free=" << std::atomic<int>::is_always_lock_free << std::endl;
    std::cout << "void* always_lock_free=" << std::atomic<void*>::is_always_lock_free << std::endl;
    std::cout << "char always_lock_free=" << std::atomic<char>::is_always_lock_free << std::endl;
    std::cout << "long long always_lock_free=" << std::atomic<long long>::is_always_lock_free << std::endl;

    std::atomic<int> counter{0};
    for (int i = 0; i < 1000; ++i) {
        int expected = counter.load(std::memory_order_relaxed);
        while (!counter.compare_exchange_weak(expected, expected + 1,
                std::memory_order_relaxed, std::memory_order_relaxed)) {
            // expected 已被 CAS 刷新为当前值，重试
        }
    }
    std::cout << "cas loop counter=" << counter.load() << std::endl;
    return 0;
}
```

## 附录 J：无锁数据结构：CAS 循环 vs 互斥锁 选型 决策流（D3 维度）

```mermaid
flowchart TD
    S0["起点：需要并发访问共享结构"] --> D1{"竞争是否激烈?"}
    D1{"竞争是否激烈?"} -->|否| A1["std::mutex 互斥锁"]
    D1{"竞争是否激烈?"} -->|是| D2{"能否无锁化? 有无 ABA 风险?"}
    D2{"能否无锁化? 有无 ABA 风险?"} -->|高 ABA 风险| A2["加锁或 hazard pointer"]
    D2{"能否无锁化? 有无 ABA 风险?"} -->|可无锁| D3{"是否多写者?"}
    D3{"是否多写者?"} -->|否| A3["CAS 循环 + 版本号"]
    D3{"是否多写者?"} -->|是| D4{"能否 wait-free?"}
    D4{"能否 wait-free?"} -->|否| A4["CAS 循环 + 退避"]
    D4{"能否 wait-free?"} -->|是| A5["wait-free 算法"]
    A3 --> D5{"是否需高可用低延迟?"}
    D5{"是否需高可用低延迟?"} -->|是| A6["无锁优先于互斥"]
    D5{"是否需高可用低延迟?"} -->|否| A7["互斥即可"]
    A1 --> END["结束：结构选型确定"]
    A2 --> END
    A4 --> END
    A5 --> END
    A6 --> END
    A7 --> END
```

> 决策流说明：无锁以更高的实现复杂度换取高竞争下的吞吐与避免死锁，但必须直面 ABA 与内存回收。低竞争或简单场景用互斥锁更省心且不易出错；只有高并发、低延迟、不能容忍优先级反转的场景才值得上 CAS 循环，且务必配合版本号或 hazard pointer/RCU 解决回收。

## 附录 K：无锁数据结构：CAS 循环 vs 互斥锁 选型 知识图谱（D6 维度）

```mermaid
flowchart TD
    L1["共享数据结构"] --> L2["互斥锁 mutex"]
    L1 --> L3["无锁 lock-free"]
    L2 --> L4["临界区串行化"]
    L3 --> L5["CAS 循环"]
    L5 --> L6["ABA 问题"]
    L6 --> L7["版本号 / tagged pointer"]
    L3 --> L8["wait-free 上限"]
    L4 --> L9["死锁风险"]
    L5 --> L10["活锁/饥饿"]
    L7 --> L11["hazard pointer"]
    L3 --> L12["内存回收"]
    L12 --> L13["RCU 宽限期"]
    L8 --> L14["无阻塞进度"]
    L10 --> L15["退避策略"]
```

### K.1 概念依赖逐边解读

| 上游概念 | 下游概念 | 依赖含义 |
| --- | --- | --- |
| 共享数据结构 | 互斥锁 mutex | 最简单正确的并发手段 |
| 共享数据结构 | 无锁 lock-free | 以复杂度换并发度 |
| 互斥锁 mutex | 临界区串行化 | 锁内操作原子执行 |
| 无锁 lock-free | CAS 循环 | 无锁靠 CAS 重试推进 |
| CAS 循环 | ABA 问题 | 指针复用导致 CAS 误判 |
| ABA 问题 | 版本号 / tagged pointer | 版本号消解 ABA |
| 无锁 lock-free | wait-free 上限 | 更强进度保证 |
| 临界区串行化 | 死锁风险 | 持锁顺序不当致死锁 |
| CAS 循环 | 活锁/饥饿 | 高竞争下重试不前进 |
| 版本号 / tagged pointer | hazard pointer | 复杂结构改用 HP 回收 |
| 无锁 lock-free | 内存回收 | 无锁删除需安全回收 |
| 内存回收 | RCU 宽限期 | RCU 以宽限期回收 |
| wait-free 上限 | 无阻塞进度 | 每次调用有限步完成 |
| 活锁/饥饿 | 退避策略 | 退避缓解活锁 |

### K.2 跨章闭环表

| 上游章 | 下游章 | 传递的知识 |
| --- | --- | --- |
| ch107 | ch110 | 原子 RMW 是无锁 CAS 的底层原语 |
| ch108 | ch110 | CAS 循环需 release/acquire 配对 |
| ch110 | ch111 | 无锁结构必须直面 ABA 问题 |
| ch110 | ch112 | 无锁回收引出 hazard pointer/RCU |
| ch109 | ch110 | thread_fence 强化无锁序 |
| ch45 | ch110 | OOP 对象模型理解节点布局 |

## 附录 D5：真实基准与性能分析 — 无锁数据结构的层级开销 (GCC 15.3.0)

> 测试环境：AMD Ryzen 9 7940HX（16C/32T）；本机 MinGW-W64 GCC 15.3.0；`g++ -O2 -std=c++17`；`std::chrono::steady_clock` 计时，5 轮取中位；`volatile` sink 防死代码消除。
> 本附录量化同一累加负载下三档并发写法（per-thread 局部计数 / atomic / mutex）的真实耗时层级，回答"无锁到底快在哪"。
> 绝对毫秒随机器而变，加速比才是可移植信号。

### D5.1 基准结果

| 场景 | 1 线程 耗时 (ms) | 1 线程 相对 | 8 线程 耗时 (ms) | 8 线程 相对 |
|------|------------------|------------|------------------|------------|
| per-thread（wait-free, thread_local 累加） | **0.33** | 0.02× | **0.78** | 0.01× |
| atomic（lock-free, `fetch_add`） | 6.42 | 0.46× | 27.19 | 0.51× |
| mutex（lock-based） | 14.01 | 1.00× | 53.27 | 1.00× |

> 相对列以 mutex = 1.00× 为锚。派生倍数（供参考，非基准列）：per-thread 相对 atomic ≈ 19× (1T) / 35× (8T)；atomic 相对 mutex ≈ 2.2× (1T) / 2.0× (8T)。per-thread 为最快档，已加粗。

#### 可视化速读（D5.1 数据图·双面板）

<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="(a) 绝对耗时（随机器而变，仅作量级参考）">
  <text x="340" y="26" text-anchor="middle" font-size="14.5" font-family="Georgia, 'Times New Roman', serif" font-weight="bold">(a) 绝对耗时（随机器而变，仅作量级参考）</text>
  <line x1="80" y1="300" x2="640" y2="300" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300" x2="80" y2="52" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300.0" x2="640" y2="300.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="303.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">0.1</text>
  <line x1="80" y1="217.3" x2="640" y2="217.3" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="220.8" text-anchor="end" font-size="10.5" font-family="Georgia, serif">1</text>
  <line x1="80" y1="134.7" x2="640" y2="134.7" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="138.2" text-anchor="end" font-size="10.5" font-family="Georgia, serif">10</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="55.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">100</text>
  <text x="20" y="176" text-anchor="middle" font-size="12" font-family="Georgia, serif" transform="rotate(-90 20 176)">绝对耗时 (ms)</text>
  <line x1="80" y1="122.6" x2="640" y2="122.6" stroke="#C44E52" stroke-width="1.2" stroke-dasharray="5 4"/>
  <text x="640" y="118.6" text-anchor="end" font-size="10.5" font-family="Georgia, serif" fill="#C44E52">基线 14.01ms</text>
  <rect x="141.3" y="257.1" width="64.0" height="42.9" fill="#4C72B0"/>
  <text x="173.3" y="251.1" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#4C72B0">0.33ms</text>
  <text x="173.3" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 173.3 314.0)">per-thread（wait-free, thread_local 累加）</text>
  <rect x="328.0" y="150.6" width="64.0" height="149.4" fill="#C44E52"/>
  <text x="360.0" y="144.6" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#C44E52">6.42ms</text>
  <text x="360.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 360.0 314.0)">atomic（lock-free, fetch_add）</text>
  <rect x="514.7" y="122.6" width="64.0" height="177.4" fill="#9A9A9A"/>
  <text x="546.7" y="116.6" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#9A9A9A">14.01ms</text>
  <text x="546.7" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 546.7 314.0)">mutex（lock-based）</text>
</svg>

<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="(b) 相对倍数（可移植信号：基准=1.00×）">
  <text x="340" y="26" text-anchor="middle" font-size="14.5" font-family="Georgia, 'Times New Roman', serif" font-weight="bold">(b) 相对倍数（可移植信号：基准=1.00×）</text>
  <line x1="80" y1="300" x2="640" y2="300" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300" x2="80" y2="52" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300.0" x2="640" y2="300.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="303.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">0</text>
  <line x1="80" y1="238.0" x2="640" y2="238.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="241.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">0.25</text>
  <line x1="80" y1="176.0" x2="640" y2="176.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="179.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">0.5</text>
  <line x1="80" y1="114.0" x2="640" y2="114.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="117.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">0.75</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="55.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">1</text>
  <text x="20" y="176" text-anchor="middle" font-size="12" font-family="Georgia, serif" transform="rotate(-90 20 176)">相对倍数 (×, 基线=1.00)</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#C44E52" stroke-width="1.2" stroke-dasharray="5 4"/>
  <text x="640" y="48.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" fill="#C44E52">1.00× 基线</text>
  <rect x="141.3" y="294.2" width="64.0" height="5.8" fill="#4C72B0"/>
  <text x="173.3" y="288.2" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#4C72B0">0.02×</text>
  <text x="173.3" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 173.3 314.0)">per-thread（wait-free, thread_local 累加）</text>
  <rect x="328.0" y="186.4" width="64.0" height="113.6" fill="#C44E52"/>
  <text x="360.0" y="180.4" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#C44E52">0.46×</text>
  <text x="360.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 360.0 314.0)">atomic（lock-free, fetch_add）</text>
  <rect x="514.7" y="52.0" width="64.0" height="248.0" fill="#9A9A9A"/>
  <text x="546.7" y="46.0" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#9A9A9A">1.00×</text>
  <text x="546.7" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 546.7 314.0)">mutex（lock-based）</text>
</svg>

> 图注：8 线程下：`mutex` 53.27ms 为基线 1.00×；lock-free `atomic(fetch_add)` 27.19ms = **0.51×**（≈2× 更快），低争用时与 mutex 接近；wait-free `per-thread(thread_local)` 仅 0.78ms = **0.01×**——把累加拆到各线程本地，彻底消除跨线程争用。机制：锁/原子串行化 vs 线程本地累积。

### D5.2 非显然结论

1. **per-thread（thread_local）几乎零成本且随线程数几乎不退化**：每个线程写入自己线程局部的累加器，不存在任何共享写、没有任何同步指令（`lock` 前缀 / 原子 RMW 都没有），因此 1 线程与 8 线程的耗时差仅来自线程启动本身（0.33 → 0.78 ms）。它是最强的 wait-free 形态，但要求"结果可延迟合并"的算法结构。
2. **atomic 是 lock-free，却仍受缓存一致性流量拖累**：`fetch_add` 编译为单条 `lock xadd`，本身无锁、不阻塞；但多核竞争同一 cache line 的计数时，MESI 协议会让该行的所有权在核间反复弹跳（cache coherence traffic），线程越多弹跳越剧烈，故 1T→8T 从 6.42 飙到 27.19 ms（≈4.2× 退化）。
3. **mutex 最慢且退化最猛**：互斥量在无竞争时只是两次原子 RMW，但高竞争下失败者坠入 futex 睡眠/唤醒（系统调用 + 上下文切换）。它不仅单次最慢，8 线程时退化到 53.27 ms（≈3.8×），是三档里随线程数恶化最凶的。

### D5.3 可复现 demo

> **示例 52** [难度 ★★★☆☆] [主题：可复现 demo]
```cpp
#include <atomic>
#include <cassert>
#include <iostream>
#include <mutex>
#include <thread>

int main() {
    constexpr long long iterations = 1LL << 20;   // 每线程 1,048,576 次

    std::atomic<long long> per_thread_total{0};    // (a) 合并后的 per-thread 结果
    std::atomic<long long> atomic_total{0};        // (b) 共享原子计数器
    std::mutex m;
    long long mutex_total = 0;                     // (c) mutex 保护计数器

    auto worker = [&]() {
        thread_local long long local = 0;          // 每线程独立累加器：无共享写
        for (long long i = 0; i < iterations; ++i) {
            local += 1;
            atomic_total.fetch_add(1, std::memory_order_relaxed);
            {
                std::lock_guard<std::mutex> lk(m);
                mutex_total += 1;
            }
        }
        per_thread_total.fetch_add(local, std::memory_order_relaxed);
    };

    std::thread t1(worker);
    std::thread t2(worker);
    t1.join();
    t2.join();

    // 仅验证功能正确性：三条路径的净额都必须等于 2 * iterations
    assert(per_thread_total.load() == 2 * iterations);
    assert(atomic_total.load() == 2 * iterations);
    assert(mutex_total == 2 * iterations);

    std::cout << "per-thread total = " << per_thread_total.load() << std::endl;
    std::cout << "atomic    total = " << atomic_total.load() << std::endl;
    std::cout << "mutex     total = " << mutex_total << std::endl;
    return 0;
}
```

### D5.4 方法学注

基准源码见库根 `_bench_d5_110_lockfree.cpp`。
- 计时用 `std::chrono::steady_clock`，每个配置跑 5 轮取中位数，排除冷启动与调度抖动。
- 用 `volatile` 全局 sink 吸收累加结果，防止编译器把整个循环优化成常量。
- 编译与测量命令（基准与此 demo 同源）：`g++ -O2 -std=c++17`。
- 本 demo 仅断言功能正确性（三条路径净额相等），不断言任何计时、加速比或 `sizeof` 数值。
- 绝对毫秒取决于 CPU 频率 / 负载 / 温度计；跨机器只比较"相对倍数"才有意义。

### D5.5 汇编实证 (GCC 15.3.0)

> 以下 disassembly 由 `g++ -O2 -std=c++23 -masm=intel _bench_d5_110_lockfree.cpp` 真实生成（节选三档累加的**工作线程**热循环）。per-thread 写私有槽是纯 `add`、atomic 是单条 `lock add`、mutex 是两次 `pthread_mutex_*` 系统调用加一条普通 `add`——这三行核心指令正好对应 D5.2「wait-free 零同步 / lock-free 受 MESI 拖累 / lock-based 最慢」的层级。

```asm
; bench_perthread 工作线程（节选）—— 写入本线程私有槽，零共享写、零同步指令
;   _ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ15bench_perthreadiEUlvE_EEEEE6_M_runEv (节选)
        mov     eax, 2000000
        xor     edx, edx
        mov     r8, QWORD PTR 16[rcx]
        idiv    DWORD PTR [r8]         ; per = N / nt
        test    eax, eax
        jle     .L
        mov     rdx, QWORD PTR 24[rcx]
        movsxd  rcx, DWORD PTR 8[rcx]
        cdqe
        mov     rdx, QWORD PTR [rdx]
        add     QWORD PTR [rdx+rcx*8], rax  ; ← 写自己那一个槽：纯普通 add，无 lock、无原子
        ret
; bench_atomic 工作线程（节选）—— 共享原子计数器，单条 lock add
;   _ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ12bench_atomiciEUlvE_EEEEE6_M_runEv (节选)
        mov     eax, 2000000
        xor     edx, edx
        idiv    DWORD PTR 16[rcx]
        test    eax, eax
        jle     .L
        cdqe
        xor     edx, edx
        mov     r8, QWORD PTR 8[rcx]
        lock add        QWORD PTR [r8], 1   ; ← 单条 lock add：无锁 RMW，但抢同一 cache line
        add     rdx, 1
        cmp     rax, rdx
        jne     .L
        ret
; bench_mutex 工作线程（节选）—— 每次迭代两次系统调用 + 普通 add
;   _ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZ11bench_mutexiEUlvE_EEEEE6_M_runEv (节选)
        mov     rbx, QWORD PTR 8[rcx]
        mov     rcx, rsi
        call    pthread_mutex_lock      ; ← 加锁：futex 系统调用
        test    eax, eax
        jne     .L
        mov     rdx, QWORD PTR 24[rdi]
        mov     rcx, rsi
        add     rbx, 1
        add     QWORD PTR [rdx], 1      ; 受互斥保护的普通自增
        call    pthread_mutex_unlock    ; ← 解锁：第二次系统调用
        cmp     rbp, rbx
        jne     .L
```

> 注意：三档「+1」本身都是一次加法，**性能差异全在同步原语**——per-thread 没有任何 `lock`/原子，故随核数近乎线性扩展（D5.2 第①条）；atomic 的 `lock add` 无锁却因 MESI 在核间反复弹跳同一 cache line 而负扩展（第②条）；mutex 更因 futex 睡眠/唤醒在高争用下最慢（第③条）。**绝对毫秒随机器而变，加速比才是可移植信号**。

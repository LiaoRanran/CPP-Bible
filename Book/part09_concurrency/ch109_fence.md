# 第109章 内存屏障与 fence

⟶ Book/part09_concurrency/ch108_memory_order.md
⟶ Book/part09_concurrency/ch107_atomic.md

⟶ Book/part09_concurrency/ch110_lockfree.md

> 标准基: C++23 / GCC 13.1 / ⟶ Book/part09_concurrency/ch107_atomic.md / 难度: ★★★★☆

## ① 学习目标 [标准]

1. 理解 memory_order 六种选项的语义
2. 区分 acquire/release/seq_cst/relaxed/consume
3. 掌握 std::atomic_thread_fence 的使用场景
4. 理解 StoreLoad/SMP/MESI 等硬件层面的内存序

## ② memory_order 六态 [标准]

```cpp
#include <atomic>
#include <iostream>
enum class MO{relaxed, consume, acquire, release, acq_rel, seq_cst};
int main(){std::cout<<"memory_order: relaxed<consume<acquire/release<acq_rel<seq_cst (strength)\n";return 0;}
```

## ③ relaxed 语义 [标准]

```cpp
#include <atomic>
#include <iostream>
std::atomic<int> x(0);
int main(){x.store(42,std::memory_order_relaxed);std::cout<<x.load(std::memory_order_relaxed)<<std::endl;return 0;}
```

## ④ acquire-release 配对 [标准]

```cpp
#include <atomic>
#include <iostream>
#include <thread>
std::atomic<bool> ready(false);int data=0;
void producer(){data=42;ready.store(true,std::memory_order_release);}
void consumer(){while(!ready.load(std::memory_order_acquire));std::cout<<data<<std::endl;}
int main(){std::thread p(producer),c(consumer);p.join();c.join();return 0;}
```

## ⑤ seq_cst 全局序 [标准]

```cpp
#include <atomic>
#include <iostream>
std::atomic<int> a(0),b(0);
int main(){a.store(1,std::memory_order_seq_cst);b.store(1,std::memory_order_seq_cst);std::cout<<a.load()+b.load()<<std::endl;return 0;}
```

## ⑥ atomic_thread_fence [标准]

```cpp
#include <atomic>
#include <iostream>
std::atomic<int> g(0);
int main(){g.store(1,std::memory_order_relaxed);std::atomic_thread_fence(std::memory_order_release);std::cout<<g.load()<<std::endl;return 0;}
```

## ⑦ 硬件内存模型 [平台·x86-64]

```cpp
#include <iostream>
int main(){std::cout<<"x86: TSO model. ARM/POWER: weak ordering. x86 seq_cst = mfence, acquire = no-op.\n";return 0;}
```

## ⑧ memory_order_consume [标准]

```cpp
#include <atomic>
#include <iostream>
std::atomic<int*> ptr(nullptr);
int main(){int v=42;ptr.store(&v,std::memory_order_release);int*p=ptr.load(std::memory_order_consume);std::cout<<*p<<std::endl;return 0;}
```

## ⑨ 跨语言对比 [经验]

```cpp
#include <iostream>
int main(){std::cout<<"C++ memory_order vs Rust Ordering vs C11 memory_order vs Java volatile+VarHandle.\n";return 0;}
```

## ⑩ 跨语言对比：内存模型 [经验]

```cpp
#include <iostream>
int main(){std::cout<<"C++ memory_order vs Rust Ordering (Acquire/Release/Relaxed/SeqCst): identical semantics.\n";return 0;}
```

## 补充完整可编译示例

```cpp
#include <atomic>
#include <iostream>
#include <thread>
std::atomic<int> counter(0);
void inc(){for(int i=0;i<1000;++i)counter.fetch_add(1,std::memory_order_relaxed);}
int main(){std::thread t1(inc),t2(inc);t1.join();t2.join();std::cout<<counter.load()<<std::endl;return 0;}
```

```cpp
#include <atomic>
#include <iostream>
std::atomic<int> flag(0);
int main(){int expected=0;flag.compare_exchange_strong(expected,1,std::memory_order_acq_rel,std::memory_order_relaxed);std::cout<<flag.load()<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <atomic>
struct alignas(64) Padded{std::atomic<int> v;};
int main(){Padded p;p.v.store(7,std::memory_order_relaxed);std::cout<<p.v.load()<<std::endl;return 0;}
```

```cpp
#include <atomic>
#include <iostream>
int main(){std::atomic<int> a;std::cout<<a.is_lock_free()<<std::endl;return 0;}
```

```cpp
#include <atomic>
#include <iostream>
int main(){std::cout<<"Dekker's algorithm needs seq_cst on non-x86 for correctness.\n";return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"StoreLoad barrier = full fence (mfence on x86, dmb on ARM). Most expensive.\n";return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"seqlock pattern: seq_cst for writer counter, acquire for reader consistency.\n";return 0;}
```

```cpp
#include <atomic>
#include <iostream>
std::atomic<int> version(0);int snapshot[2]={0,0};
int main(){version.store(1,std::memory_order_release);std::atomic_thread_fence(std::memory_order_seq_cst);std::cout<<version.load()<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"RCU pattern: readers no atomic ops, writers use release fence. Linux kernel classic.\n";return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"fence总结: seq_cst最安全也最贵, acquire-release足够大多数场景, relaxed仅计数器。"<<std::endl;return 0;}
```

## ⑪ STL 联系 [标准]
```cpp
#include <iostream>
#include <atomic>
int main(){std::atomic<int> x;x.store(1);std::cout<<x.load()<<std::endl;return 0;}
```

## ⑫ 工业案例 [经验]
```cpp
#include <iostream>
int main(){std::cout<<"Linux RCU (release+consume), Chrome base::AtomicRefCount (relaxed), ClickHouse lock-free queue.\n";return 0;}
```

## ⑬ 源码分析 [实现·GCC13]
```cpp
#include <iostream>
int main(){std::cout<<"GCC __atomic_store_n maps to lock xchg or mov+mfence depending on order in gcc/builtins.cc.\n";return 0;}
```

## ⑭ WG21 提案 [标准]
```cpp
#include <iostream>
int main(){std::cout<<"P0668: deprecating memory_order_consume. P2892: extending atomic for non-trivial types.\n";return 0;}
```

## ⑮ 面试题 [经验]
```cpp
#include <iostream>
int main(){std::cout<<"Q: acquire vs seq_cst? A: acquire=one-way barrier, seq_cst=global total order, ~10x slower on ARM.\n";return 0;}
```

## ⑯ 易错点 [经验]
```cpp
#include <iostream>
int main(){std::cout<<"Pitfall: relaxed on dependent data = UB; forgetting fence in seqlock reader; consume unreliable.\n";return 0;}
```

## ⑰ FAQ [经验]
```cpp
#include <iostream>
int main(){std::cout<<"Q: When to use fence vs atomic operation? A: fence when multiple variables need ordering together.\n";return 0;}
```

## ⑱ 最佳实践 [经验]
```cpp
#include <iostream>
int main(){std::cout<<"Best: start with seq_cst, profile, relax to acquire-release where safe. Never relax unless proven.\n";return 0;}
```

## ⑲ 性能分析 [平台·x86-64]
```cpp
#include <iostream>
int main(){std::cout<<"Perf: x86 relaxed=acquire=~1ns (free), seq_cst=~10ns (mfence). ARM: acquire=~5ns (dmb ld).\n";return 0;}
```

## ⑳ 跨语言对比 [经验]
```cpp
#include <iostream>
int main(){std::cout<<"C++ memory_order vs Rust Ordering (Acquire/Release/Relaxed/SeqCst): identical semantics.\n";return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"fence final: start seq_cst, relax to acq_rel, never consume. Profile target arch."<<std::endl;return 0;}
```

## 附录 A: 六种 memory_order 速查

| order | x86 代价 | ARM 代价 | 典型场景 |
|---|---|---|---|
| relaxed | ~1ns (free) | ~1ns | 计数器、统计 |
| consume | ~1ns | ~1ns | RCU reader（已废弃方向） |
| acquire | ~1ns (free) | ~5ns | mutex lock, consumer |
| release | ~1ns (free) | ~5ns | mutex unlock, producer |
| acq_rel | ~1ns (free) | ~10ns | CAS, fetch_add |
| seq_cst | ~10ns (mfence) | ~20ns (dmb) | Dekker, seqlock writer |

```cpp
#include <atomic>
#include <iostream>
int main(){std::cout<<"x86 acquire=free (TSO model). ARM acquire=ldar instruction. seq_cst always most expensive.\n";return 0;}
```

## 附录 B: seqlock 完整实现

```cpp
#include <atomic>
#include <iostream>
#include <thread>
struct SeqLock{std::atomic<unsigned> seq{0};int data[2]={0,0};
    void write(int a,int b){auto s=seq.load(std::memory_order_relaxed);seq.store(s+1,std::memory_order_release);data[0]=a;data[1]=b;seq.store(s+2,std::memory_order_release);}
    bool read(int&a,int&b){unsigned s1,s2;do{s1=seq.load(std::memory_order_acquire);if(s1&1)continue;a=data[0];b=data[1];s2=seq.load(std::memory_order_acquire);}while(s1!=s2);return true;}
};
int main(){SeqLock sl;sl.write(10,20);int a,b;sl.read(a,b);std::cout<<a<<" "<<b<<std::endl;return 0;}
```

## 附录 C: MESI 缓存一致性协议

```cpp
#include <iostream>
int main(){
    std::cout<<"MESI states: Modified, Exclusive, Shared, Invalid.\n";
    std::cout<<"Cache line transitions: M->S (writeback), S->I (invalidation from other core write).\n";
    std::cout<<"Release: ensures writes flushed to cache. Acquire: ensures reads see latest.\n";
    return 0;
}
```

## 附录 D: 跨平台 memory_order 开销

```cpp
#include <iostream>
int main(){
    std::cout<<"Platform costs (approximate):\n";
    std::cout<<"x86 TSO: load=1ns, store=2ns, mfence=10ns\n";
    std::cout<<"ARM weak: load=1ns, store=1ns, dmb=5ns, dmb sy=20ns\n";
    std::cout<<"POWER: sync=50ns (most expensive)\n";
    return 0;
}
```

```cpp
#include <atomic>
#include <iostream>
#include <thread>
int main(){
    std::atomic<int> a{0},b{0};
    std::thread t1([&]{a.store(1,std::memory_order_seq_cst);int r=b.load(std::memory_order_seq_cst);});
    std::thread t2([&]{b.store(1,std::memory_order_seq_cst);int r=a.load(std::memory_order_seq_cst);});
    t1.join();t2.join();
    std::cout<<"IRIW test: seq_cst guarantees both threads agree on order.\n";
    return 0;
}
```

## 附录 E: Lock-free 栈实战模式

```cpp
#include <atomic>
#include <iostream>
template<typename T>struct LFStack{struct Node{T v;Node*next;};std::atomic<Node*>head{nullptr};void push(T x){auto n=new Node{x,head.load(std::memory_order_relaxed)};while(!head.compare_exchange_weak(n->next,n,std::memory_order_release,std::memory_order_relaxed));}bool pop(T&out){Node*h=head.load(std::memory_order_acquire);while(h&&!head.compare_exchange_weak(h,h->next,std::memory_order_acquire,std::memory_order_relaxed));if(!h)return false;out=h->v;delete h;return true;}};
int main(){LFStack<int> s;s.push(1);s.push(2);int v;s.pop(v);std::cout<<v<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"LF patterns: CAS loop + acq_rel. Hazard pointers/RCU for safe reclamation beyond fences."<<std::endl;return 0;}
```

```cpp
#include <atomic>
#include <iostream>
int main(){std::atomic<int>x{0};x.store(42,std::memory_order_release);std::atomic_thread_fence(std::memory_order_acquire);std::cout<<x.load()<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"fence vs atomic: fence orders ALL subsequent ops, atomic orders just that variable."<<std::endl;return 0;}
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第108章](Book/part09_concurrency/ch108_memory_order.md) | 键值查找/缓存 | 本章提供概念，第108章提供实现 |
| [第110章](Book/part09_concurrency/ch110_lockfree.md) | 无锁队列/计数器 | 本章提供概念，第110章提供实现 |
| [第107章](Book/part09_concurrency/ch107_atomic.md) | 泛型库/编译期计算 | 本章提供概念，第107章提供实现 |

## 附录 F：fence工业与面试

```cpp
#include <iostream>
#include <atomic>
int main(){std::cout<<"acquire fence=dmb ishld(~2ns ARM); release=dmb ish(~2ns); seq_cst=mfence(~10ns x86)"<<std::endl;return 0;}
```

| fence | x86指令 | ARM指令 | 延迟 |
|---|---|---|---|
| acquire | 无(TSO) | dmb ishld | ~2ns |
| release | 无(TSO) | dmb ish | ~2ns |
| seq_cst | mfence | dmb sy | ~10ns |

面试: x86需要fence? 只有StoreLoad重排需要mfence; ARM所有order都需要dmb

## 附录 G：fence设计权衡 [H: Design / E: Lowlevel]

```asm
; x86 seq_cst fence = mfence (full memory barrier)
mfence  ; 确保所有之前的load/store在mfence之前完成
; cost: ~10ns on Skylake, ~33ns on Zen2

; ARM acquire fence = dmb ishld
dmb ishld  ; 只阻止load-load和load-store重排, 不阻止store-store
; cost: ~2ns on Cortex-A76
```

```cpp
#include <iostream>
int main(){std::cout<<"x86 mfence=10ns(seq_cst); ARM dmb=2-5ns(acquire/release)"<<std::endl;return 0;}
```

| 平台 | acquire | release | seq_cst |
|---|---|---|---|
| x86 TSO | 免费(天然) | 免费(天然) | mfence(~10ns) |
| ARM | dmb ishld(~2ns) | dmb ish(~2ns) | dmb sy(~5ns) |
| RISC-V | fence r,r(~2ns) | fence w,w(~2ns) | fence rw,rw(~5ns) |

> **延迟量级来源**：上表与各处的 `~1ns / ~2ns / ~5ns / ~10ns / ~20ns / ~33ns` 均为微架构基准的经验量级，来自 Agner Fog 指令表、LLVM 官方内存模型文档（llvm.org/docs/Atomics.html）、Intel/ARM 厂商白皮书；数值随具体微架构（Skylake / Zen2 / Cortex-A76 …）变动，前缀 `~` 表示量级而非精确值，**平台相关、不可软件实测**，故保留量级并标注来源而非编造单一数字。

## 附录 H：真实汇编证据（MinGW GCC 13.1.0 -O2）[E: Lowlevel]

> 以下为 `Examples/_ch109_fence_perf.cpp` 经 `g++ -S -O2 -m64` 真实产物的节选（AT&T 语法，完整见 `Examples/_ch109_fence_perf.asm`）。证明 x86 TSO 下：relaxed / acquire / release 免费，seq_cst 由带 lock 前缀的指令建立全局屏障。

```asm
; 来源: Examples/_ch109_fence_perf.asm  (MinGW GCC 13.1.0 -O2, x86_64)
; ① relaxed_store：普通 mov，无屏障（TSO 天然有序）
_Z13relaxed_storeRSt6atomicIiEi:
    movl    %edx, (%rcx)
    ret
; ② relaxed_load：普通 mov，无屏障
_Z12relaxed_loadRSt6atomicIiE:
    movl    (%rcx), %eax
    ret
; ③ seqcst_store：xchg 隐含 lock 前缀 → 全局总顺序（非 mfence）
_Z12seqcst_storeRSt6atomicIiEi:
    xchgl   (%rcx), %edx
    ret
; ④ seqcst_fence：lock orq 空操作 = 全屏障（GCC 13 选用，等价于 mfence）
_Z12seqcst_fencev:
    lock orq    $0, (%rsp)
    ret
; ⑤ acquire_fence：x86 TSO 下免费 → 空（无 dmb/mfence）
_Z13acquire_fencev:
    ret
; ⑥ release_fence：x86 TSO 下免费 → 空
_Z13release_fencev:
    ret
```

**关键修正**：附录 G 手写"x86 seq_cst fence = mfence"是概念性简化。真实 GCC 13.1 在 x86_64 把 `atomic_thread_fence(seq_cst)` 编译为 `lock orq $0,(%rsp)`、把 `seq_cst` store 编译为 `xchgl`（隐含 lock），二者均通过 lock 前缀提供与 mfence **等价**的全屏障语义（lock 前缀在 x86 上隐式带 full barrier）。ARM 平台则确实生成 `dmb sy`（见 LLVM 官方文档）。

## 相关章节（交叉引用）

- **同模块兄弟（part09 并发）**：⟶ Book/part09_concurrency/ch107_atomic.md（第107章　std::atomic 原子类型（C++11））
- **同模块兄弟（part09 并发）**：⟶ Book/part09_concurrency/ch108_memory_order.md（第108章　memory_order：六种内存序（C++11））
- **同模块兄弟（part09 并发）**：⟶ Book/part09_concurrency/ch110_lockfree.md（第110章　无锁编程：lock-free / wait-free（C++11））
- **同模块兄弟（part09 并发）**：⟶ Book/part09_concurrency/ch111_aba.md（第111章　ABA 问题与解决（C++11））
- **同模块兄弟（part09 并发）**：⟶ Book/part09_concurrency/ch112_hazard_rcu.md（第112章　Hazard Pointer 与 RCU（C++11/实践））
- **同模块兄弟（part09 并发）**：⟶ Book/part09_concurrency/ch113_coroutine.md（第113章　协程 coroutine：promise / awaiter（C++20））
- **硬件底座（part03）**：⟶ Book/part03_language/ch30_volatile.md（第30章 volatile / atomic 与硬件寄存器）—— x86 TSO 与 ARM 弱内存模型决定 fence 的真实成本与正确性

## 附录 I：fence 工业实现与源码对照

内存屏障在编译器后端与高性能库中的真实实现：

| 项目/库 | 技术/模式 | 使用场景 | 源码/链接 |
|---------|----------|---------|----------|
| **LLVM**（github.com/llvm/llvm-project） | `atomic_thread_fence` 降级为 X86 `MFENCE`/`lock` 或 ARM `dmb` | 编译器后端 | `llvm/lib/Target/X86/X86ISelLowering.cpp` |
| **Chromium**（chromium.googlesource.com/chromium/src） | `base::subtle::Atomic32` 操作 + 手写屏障 | 框架原子 | `base/atomicops.h` |
| **Google/Abseil**（github.com/abseil/abseil-cpp） | `absl::atomic_hook` 与内存序工具 | 库 | `absl/base/internal` |
| **DPDK**（github.com/DPDK/dpdk） | `rte_ring` 无锁环用 `__atomic_thread_fence(__ATOMIC_ACQ_REL)` | 高性能数据面 | `lib/ring/rte_ring_c11_pvt.h` |
| **folly**（github.com/facebook/folly） | `folly::atomic_shared_ptr` 用 acquire/release 屏障 | 并发库 | `folly/AtomicSharedPtr.h` |
| **Google** 性能实践 | 明确 seq_cst 在 x86 免费、ARM 昂贵，按架构选序 | 优化规范 | `google/perfguide` |
| **Boost**（github.com/boostorg/lockfree） | Boost.Lockfree 队列用 `memory_order_acquire/release` | 无锁库 | `boostorg/lockfree` |
| **Qt**（code.qt.io） | `QAtomicInt` 封装平台原子与屏障 | 框架 | `qtbase/src/corelib/thread` |

**底层深度**：LLVM 在 SelectionDAG 阶段将 `fence(seq_cst)` 降级为 `X86ISD::MFENCE` 或带 lock 前缀的指令（例如 `lock orq $0,(%rsp)`），ARM 后端生成 `dmb ish`；这与附录 H 的真实汇编证据一致——x86 TSO 下 seq_cst store 经 `xchgl`（隐含 lock）即获全屏障，无需独立 mfence。DPDK `rte_ring` 在 C11 实现里于 enqueue 末尾发 release fence、dequeue 开头发 acquire fence，配合头/尾指针保证多生产者写入对消费者可见；Chromium 在 ARM 平台用 `dmb` 指令、x86 用 `std::atomic_signal_fence` 编译器屏障阻止重排。工业界共识：x86 上能避免 seq_cst 就避免（acquire/release 在 x86 零成本），ARM/Power 上才需要显式屏障。

## 附录 J：GCC 15.3.0 真机汇编实证（ASM-109-fence）[E: Low-level]

> 工具链：`g++.exe (MinGW-W64 x86_64-msvcrt-posix-seh, Brecht Sanders r1) 15.3.0`，`-std=c++26 -O2 -c`，`objdump -d -M intel -C`。证据源码 `_asm_demo/ch109_fence_test.cpp`、汇编 `_asm_demo/ch109_fence_test.s`。各 fence 包在 `[[gnu::noinline]]` 空函数内隔离对比。与附录 H（GCC 13.1.0）结论相互印证、并补齐 `acq_rel`/`signal` 两档。

### 真机指令（节选）

```asm
; fence_seqcst()  —— 全屏障（注意：GCC 用的是 lock-or 技巧，不是 mfence）
        lock or QWORD PTR [rsp],0x0     ; locked-OR-zero：借 lock 前缀隐式全屏障，等价于 mfence
        ret
; fence_acquire() / fence_release() / fence_acq_rel() —— x86-64 TSO 下全部为空
        ret
; fence_signal()  —— 纯编译期屏障，运行时零指令
        ret
```

### 非显然事实

1. **`seq_cst` fence 生成的是 `lock or QWORD PTR [rsp],0x0`，不是 `mfence`。** 这是 GCC 长期采用的"锁或零"技巧：在栈顶对 8 字节做一条带 `lock` 前缀、操作数恒为 0 的 `OR`（对内存内容无任何影响），借 `lock` 前缀的隐式全屏障语义获得与 `mfence` **等价**的单一总顺序。`lock or` 在某些微架构比独立 `mfence` 更省端口/更短延迟。本实证（GCC 15.3.0）与附录 H（GCC 13.1.0 的 `lock orq $0,(%rsp)`）**跨主版本一致**——该手法稳定可信。
2. **`acquire` / `release` / `acq_rel` 三种 fence 在 x86-64 下全部编译为空函数（`ret` 一条）。** 原因：x86 TSO 已禁止 load-load、store-store、load-store 三类重排，GCC 只需插入**编译器级屏障**（阻止本线程指令重排）而无需任何 CPU 屏障指令；`acq_rel` 同样不生成机器码。
3. **`atomic_signal_fence(seq_cst)` 是纯编译期屏障**，仅约束同一线程内"编译器优化"与"信号处理函数"之间的可见性，对硬件**零约束、零运行时指令**——它与 `atomic_thread_fence` 的本质区别就在于此（后者至少 seq_cst 档会落一条 CPU 屏障）。
4. **跨平台警示（呼应 ch108 / 附录 H）**：上述"空"只在 x86-64 TSO 成立。ARM/AArch64 上 `seq_cst`/`acq_rel` fence 生成 `dmb ish`，`acquire`→`dmb ishld`（或 `ldar`）、`release`→`dmb ishst`（或 `stlr`）。在 x86 开发机上"fence 看起来免费"是陷阱：烧到 ARM MCU 后，指令数与正确性保证都天差地别——x86 验证过的无锁代码必须在 ARM 目标上重新用 `dmb` 语义核算。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

用 `std::atomic_thread_fence` 配合 **relaxed** 原子操作，实现与练习「release store / acquire load」等价的同步：生产者 `relaxed store 数据 → release fence → relaxed store flag`，消费者 `relaxed load flag → acquire fence → relaxed load 数据`。

<details><summary>答案与解析</summary>

独立 fence 把「序」从具体原子操作里剥离出来：release fence 挡住其**前**的写被重排到其后的 relaxed store 之后；acquire fence 挡住其**后**的读被重排到其前的 relaxed load 之前。两者配对等价于 release/acquire 操作序。

```cpp
#include <atomic>
#include <thread>
#include <cassert>
#include <iostream>
int main() {
    std::atomic<int> data{0};
    std::atomic<bool> flag{false};
    std::thread prod([&]{
        data.store(42, std::memory_order_relaxed);
        std::atomic_thread_fence(std::memory_order_release);  // release fence
        flag.store(true, std::memory_order_relaxed);
    });
    std::thread cons([&]{
        while (!flag.load(std::memory_order_relaxed)) {}
        std::atomic_thread_fence(std::memory_order_acquire);  // acquire fence
        assert(data.load(std::memory_order_relaxed) == 42);
        std::cout << data.load(std::memory_order_relaxed) << '\n';
    });
    prod.join(); cons.join();
    return 0;
}
```

[标准] fence 与原子操作的组合语义见 `[atomics.fences]`：release fence + 后续 relaxed store，配 acquire fence + 前置 relaxed load，建立 synchronizes-with。

</details>

### 练习 2（难度 ★★★）

说明「独立 fence」与「操作自带 memory_order」的区别：为什么一个 `fetch_add(acq_rel)` 不完全等同于 `relaxed fetch_add` 前后各加一个 fence？给出何时必须用独立 fence 的场景。

<details><summary>答案与解析</summary>

操作自带序只作用于**该操作本身**的那一次访问；独立 fence 作用于**当前线程该 fence 前/后的所有原子操作**，粒度更粗、影响更广。当你需要「一批 relaxed 操作整体对外发布一次」时，用一个 release fence 比给每个操作都升级序更省。

```cpp
#include <atomic>
#include <thread>
#include <iostream>
int main() {
    std::atomic<int> a{0}, b{0}, c{0};
    std::atomic<bool> pub{false};
    std::thread w([&]{
        a.store(1, std::memory_order_relaxed);      // 一批独立 relaxed 写
        b.store(2, std::memory_order_relaxed);
        c.store(3, std::memory_order_relaxed);
        std::atomic_thread_fence(std::memory_order_release);  // 一次围栏统一发布
        pub.store(true, std::memory_order_relaxed);
    });
    std::thread r([&]{
        while (!pub.load(std::memory_order_relaxed)) {}
        std::atomic_thread_fence(std::memory_order_acquire);
        std::cout << a.load(std::memory_order_relaxed)
                  << b.load(std::memory_order_relaxed)
                  << c.load(std::memory_order_relaxed) << '\n';  // 123
    });
    w.join(); r.join();
    return 0;
}
```

[标准] 单操作有序化：`x.store(v, release)`；批量有序化：一次 `atomic_thread_fence(release)` 覆盖前面所有 relaxed 写——后者是 fence 不可被操作序替代的价值点。

</details>

### 练习 3（难度 ★★★★）

对比 `std::atomic_thread_fence` 与 `std::atomic_signal_fence`：写一个「主线程与同线程信号处理函数共享 relaxed 原子」的场景，说明为什么此处应用 `atomic_signal_fence` 而非 `atomic_thread_fence`。

<details><summary>答案与解析</summary>

`atomic_signal_fence` 只阻止**编译器**在当前线程内的重排（针对同线程异步信号/中断），不生成任何 CPU 屏障指令，因此零运行时开销；`atomic_thread_fence` 还会生成硬件屏障用于**跨线程/跨核**可见性。信号处理器与被中断代码在同一核同一线程上下文，只需防编译器重排。

```cpp
#include <atomic>
#include <csignal>
#include <iostream>
std::atomic<int> g_data{0};
std::atomic<bool> g_flag{false};
extern "C" void handler(int) {
    // 信号处理器：与被中断代码同线程，只需防编译器重排
    if (g_flag.load(std::memory_order_relaxed)) {
        std::atomic_signal_fence(std::memory_order_acquire);
        (void)g_data.load(std::memory_order_relaxed);
    }
}
int main() {
    std::signal(SIGINT, handler);
    g_data.store(99, std::memory_order_relaxed);
    std::atomic_signal_fence(std::memory_order_release);  // 无 CPU 屏障，仅约束编译器
    g_flag.store(true, std::memory_order_relaxed);
    std::cout << "installed\n";
    return 0;
}
```

[平台] 同线程信号/中断场景用 `atomic_signal_fence`（零指令）即可；跨线程一律 `atomic_thread_fence`。误用后者于纯信号场景会白白付出屏障指令开销。

</details>

## 附录：用法演绎（从选型到落地）

> 本节把 fence 放进真实决策链：**选型场景 → 常见错误 → 修复代码 → 工程结论**。

### 演绎 1：该用独立 fence 还是让操作自带序？

**选型场景**：发布单个「就绪」标志，标志之前只有一处数据写。

**常见错误**：对「单操作即可有序」的场景滥用独立 fence，代码更啰嗦且易漏配对。

```cpp
#include <atomic>
#include <thread>
#include <iostream>
int main() {
    std::atomic<int> data{0};
    std::atomic<bool> flag{false};
    std::thread p([&]{
        data.store(42, std::memory_order_relaxed);
        // 冗余：只有一处发布，完全可以让 flag.store 自带 release
        std::atomic_thread_fence(std::memory_order_release);
        flag.store(true, std::memory_order_relaxed);
    });
    p.join();
    std::cout << "verbose but correct\n";
    return 0;
}
```

**修复**：单点发布直接让操作自带序，去掉 fence：

```cpp
#include <atomic>
#include <thread>
#include <iostream>
int main() {
    std::atomic<int> data{0};
    std::atomic<bool> flag{false};
    std::thread p([&]{
        data.store(42, std::memory_order_relaxed);
        flag.store(true, std::memory_order_release);  // 一步到位，配对清晰
    });
    p.join();
    std::cout << "concise\n";
    return 0;
}
```

**结论**：**单个发布点用操作自带 `release`/`acquire`**（可读、不易漏配对）；**仅当需要「一批 relaxed 操作统一发布/获取」时**才用独立 `atomic_thread_fence`。fence 是粗粒度工具，别当默认写法。

### 演绎 2：`atomic_signal_fence` 被误当跨线程屏障

**选型场景**：两个线程通过 relaxed 原子通信，开发者想「省点开销」用 `atomic_signal_fence` 代替 `atomic_thread_fence`。

**常见错误**：跨线程用 `atomic_signal_fence`。

```cpp
#include <atomic>
#include <thread>
#include <iostream>
int main() {
    std::atomic<int> data{0};
    std::atomic<bool> flag{false};
    std::thread prod([&]{
        data.store(42, std::memory_order_relaxed);
        std::atomic_signal_fence(std::memory_order_release);  // 错误：不生成 CPU 屏障
        flag.store(true, std::memory_order_relaxed);
    });
    std::thread cons([&]{
        while (!flag.load(std::memory_order_relaxed)) {}
        std::atomic_signal_fence(std::memory_order_acquire);  // 错误：跨核不可见性无保证
        std::cout << data.load(std::memory_order_relaxed) << '\n';  // 弱内存平台可能读到 0
    });
    prod.join(); cons.join();
    return 0;   // 编译通过；x86 碰巧对，ARM 上可能读到旧值
}
```

`atomic_signal_fence` 只约束编译器，不发射硬件屏障，跨核之间的写缓冲/失效队列不会被强制排空，弱内存平台上读者可能看不到 `data` 的新值。

**修复**：跨线程改用 `std::atomic_thread_fence`（生成 `dmb`/隐含屏障），或直接让 `flag` 操作自带 `release`/`acquire`。

**结论**：`atomic_signal_fence` = **同线程**防编译器重排（信号/中断）；`atomic_thread_fence` = **跨线程/跨核**可见性。二者不可互换，选错在强内存平台会被掩盖、弱内存平台才暴露。

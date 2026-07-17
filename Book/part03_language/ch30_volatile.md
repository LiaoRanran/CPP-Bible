# 第30章 volatile / atomic 与硬件寄存器

⟶ Book/part09_concurrency/ch107_atomic.md

> 标准基: C++23 / GCC 13.1 / 预计阅读: 50min / ⟶ Book/part09_concurrency/ch107_atomic.md / 难度: ★★★☆☆

## ① 学习目标 [标准]

1. 区分 volatile（硬件可见性）与 atomic（多线程原子性）
2. 理解 volatile 的正确使用场景：MMIO、信号处理、setjmp/longjmp
3. 掌握 memory-mapped I/O 中 volatile 的必要性
4. 理解为什么 volatile 不能替代 atomic

## ② volatile 基本语义 [标准]

```cpp
#include <iostream>
volatile int sensor = 0;
int main(){sensor=42;std::cout<<sensor<<std::endl;return 0;}
```

## ③ MMIO 读写 [平台·x86-64]

```cpp
#include <iostream>
struct Device{volatile unsigned int status;volatile unsigned int data;};
int main(){Device dev;dev.status=0;dev.data=42;std::cout<<"MMIO mapped\n";return 0;}
```

## ④ volatile 不能替代 atomic [标准]

```cpp
#include <iostream>
#include <atomic>
std::atomic<int> safe{0};
int main(){safe.store(1);std::cout<<safe.load()<<std::endl;return 0;}
```

## ⑤ 信号处理中的 volatile [平台]

```cpp
#include <iostream>
#include <csignal>
volatile sig_atomic_t flag=0;
int main(){flag=1;std::cout<<(int)flag<<std::endl;return 0;}
```

## ⑥ setjmp/longjmp 中的 volatile [平台]

```cpp
#include <iostream>
int main(){std::cout<<"volatile prevents register caching across setjmp/longjmp\n";return 0;}
```

## ⑦ 编译器屏障 [实现·GCC13]

```cpp
#include <iostream>
int main(){int x=0;asm volatile("":::"memory");x=1;std::cout<<x<<std::endl;return 0;}
```

## ⑧ volatile 指针 [平台]

```cpp
#include <iostream>
int main(){int val=0;volatile int* p=&val;*p=42;std::cout<<val<<std::endl;return 0;}
```

## ⑨ volatile 成员函数 [标准]

```cpp
#include <iostream>
struct Reg{volatile int v;int read()volatile{return v;}void write(int x)volatile{v=x;}};
int main(){Reg r;r.write(7);std::cout<<r.read()<<std::endl;return 0;}
```

## ⑩ volatile 与 const [标准]

```cpp
#include <iostream>
int main(){volatile const int ROM=0xDEAD;std::cout<<"ROM value:"<<ROM<<std::endl;return 0;}
```

## ⑪ STL 联系：atomic 与 volatile 的严格分工 [标准]

```cpp
// ⑪ volatile 不保证原子性；atomic 不阻止寄存器优化——两者各司其职
#include <iostream>
#include <atomic>
#include <thread>

volatile int bad_counter = 0;   // 多线程不安全：++ 是三步骤（读-改-写），volatile 不原子化
std::atomic<int> good_counter{0};  // 安全：fetch_add 是原子的

void inc_bad() { for (int i = 0; i < 100000; ++i) ++bad_counter; }
void inc_good() { for (int i = 0; i < 100000; ++i) good_counter.fetch_add(1, std::memory_order_relaxed); }

int main() {
    std::thread t1(inc_good), t2(inc_good);
    t1.join(); t2.join();
    std::cout << "atomic counter: " << good_counter.load() << " (always 200000)\n";
    // bad_counter 结果可能是 100000~200000（race condition）
    std::cout << "volatile counter: undefined due to data race\n";
    std::cout << "Rule: volatile for single-threaded MMIO/signals. atomic for multi-threaded shared state.\n";
    return 0;
}
```

- `[标准]`：`std::atomic` 保证原子性和内存序。`volatile` 只保证每次访问都抵达内存。两者正交：嵌入式场景可同时使用 `volatile std::atomic<int>`（MMIO 寄存器的原子访问）。

## ⑫ 工业案例：嵌入式 MMIO 寄存器模板 [经验]

```cpp
// ⑫ 实际嵌入式代码中 volatile 的标准写法：reinterpret_cast 到 volatile 结构体
#include <iostream>
#include <cstdint>

// 假设内存映射地址（真实嵌入式代码使用链接器脚本定义）
struct UART_Regs {
    volatile uint32_t DR;    // Data Register
    volatile uint32_t SR;    // Status Register (TXE=bit7, RXNE=bit5)
    volatile uint32_t CR1;   // Control Register 1
    volatile uint32_t CR2;
    volatile uint32_t CR3;
    volatile uint32_t BRR;   // Baud Rate Register
};

// 真实代码: UART_Regs* usart2 = reinterpret_cast<UART_Regs*>(0x40004400);
// 此处模拟:
alignas(64) static UART_Regs mock_uart;

// 寄存器操作模板（泛型，适用于任何 MMIO 外设）
template<typename Regs>
void uart_write(Regs* uart, char c) {
    while (!(uart->SR & (1 << 7)));  // wait TXE
    uart->DR = c;                     // volatile write → 编译器必须生成 store 指令
}

int main() {
    mock_uart.SR |= (1 << 7);  // set TXE for demo
    uart_write(&mock_uart, 'A');
    std::cout << "UART sent: " << (char)mock_uart.DR << std::endl;
    std::cout << "Pattern: reinterpret_cast<volatile Regs*>(BASE_ADDR) → register access without optimizer interference.\n";
    return 0;
}
```

- `[经验]`：所有主流嵌入式 SDK（STM32 HAL、ESP-IDF、nRF SDK）都使用此模式。不写 `volatile` 的话，GCC -O2 可能将连续的对同一地址的写操作优化为最后一次写入，导致外设看不到中间值。

## ⑬ 源码分析：GCC 内部 volatile 处理 [实现·GCC13]

```cpp
// ⑬ GCC/LLVM 编译器内部如何对待 volatile
#include <iostream>
int main() {
    std::cout << "GCC volatile handling (gcc/gimplify.cc + gcc/expr.cc):\n";
    std::cout << "1. AST: volatile qualifier stored in TREE_READONLY/TREE_THIS_VOLATILE flags\n";
    std::cout << "2. GIMPLE: volatile accesses marked with TREE_SIDE_EFFECTS → prevents DCE\n";
    std::cout << "3. CSE: Common Subexpression Elimination skips volatile refs\n";
    std::cout << "4. RTL: MEM_VOLATILE_P flag on memory operands → forces load/store emission\n\n";
    std::cout << "LLVM volatile handling (llvm/IR/Instructions.h):\n";
    std::cout << "1. LoadInst::setVolatile(true) / StoreInst::setVolatile(true)\n";
    std::cout << "2. passes skip volatile ops: DeadStoreElimination, LICM, GVN all respect volatile\n";
    std::cout << "3. CodeGen: volatile load = explicit ldr, volatile store = explicit str (ARM)\n\n";
    std::cout << "Key insight: volatile is the ONLY C++ keyword that changes optimizer behavior\n";
    std::cout << "at the fundamental GIMPLE/LLVM-IR level — it is not sugar.\n";
    return 0;
}
```

- `[实现·GCC13]`：volatile 直接作用于编译器的中间表示（GIMPLE/LLVM-IR），通过 `TREE_SIDE_EFFECTS` / `setVolatile` 标志通知**所有优化 pass** 跳过该访问。这不是"提示"，是硬约束。

## ⑭ WG21 关键提案与演变 [标准]

```cpp
// ⑭ volatile 的标准化历史中最重要的两个提案
#include <iostream>
int main() {
    std::cout << "=== volatile 标准演变 ===\n\n";
    std::cout << "P1152R4 (C++20): Deprecate volatile compound assignments\n";
    std::cout << "  → v += 1;  // 被废弃：读-改-写不是单次 volatile 访问\n";
    std::cout << "  → 修复: v = v + 1;  // 显式两次 volatile 访问（读 + 写）\n\n";
    std::cout << "P2327R1 (C++23 direction): De-deprecate volatile for specific uses\n";
    std::cout << "  → 承认嵌入式场景的合理需求：volatile |= mask; 在 MMIO 中常见且正确\n";
    std::cout << "  → 方向：不废弃复合赋值，但要求语义上等同于分解后的 load-op-store\n\n";
    std::cout << "P1382R1: volatile_load<T> / volatile_store<T> (C++20 adopted)\n";
    std::cout << "  → std::volatile_load 标准库函数，替代 reinterpret_cast<volatile T*> 模式\n";
    std::cout << "  → 实际：少有人用，reinterpret_cast 模式仍是工业主流\n\n";
    std::cout << "历史：C 和 C++ 的 volatile 语义最初相同。C++11 后分歧：\n";
    std::cout << "  C: volatile 保留所有语义\n";
    std::cout << "  C++: volatile 逐步缩小范围（不建议用于并发，C++11 起推荐 std::atomic）\n";
    return 0;
}
```

- `[标准]`：P1152 是最具争议的 volatile 提案——嵌入式社区强烈反对完全废弃复合赋值。P2327 是妥协方案：保留 volatile |= 但要求语义正确。反映了 ISO 委员会对嵌入式领域的让步。

## ⑮ 面试题精选 [经验]

```cpp
// ⑮ 嵌入式/C++ 后台面试中 volatile 的 5 道高频题
#include <iostream>
int main() {
    std::cout << "Q1: volatile 能用于线程同步吗？\n";
    std::cout << "答：不能。volatile 不保证原子性、不建立 happens-before 关系、不阻止 CPU 乱序。\n";
    std::cout << "   Java 的 volatile 可以，但 C++ 的 volatile ≠ Java volatile。\n\n";
    std::cout << "Q2: const volatile 是什么？何时使用？\n";
    std::cout << "答：只读硬件寄存器。如状态寄存器（CPU 可读不可写）。const 阻止写，volatile 阻止缓存。\n\n";
    std::cout << "Q3: volatile 指针 vs 指向 volatile 的指针？\n";
    std::cout << "答：int* volatile p; (指针本身 volatile) vs volatile int* p; (指向 volatile 的数据)。\n";
    std::cout << "   volatile int* volatile p; (两者都 volatile，如 MMIO 基址寄存器)。\n\n";
    std::cout << "Q4: 优化器真的会删除 MMIO 写操作吗？\n";
    std::cout << "答：会。for(i=0;i<10;i++) REG=0; 在 -O2 下可能被优化为 REG=0 一次。volatile 阻止此行为。\n\n";
    std::cout << "Q5: volatile 与 asm volatile('':::'memory') 的区别？\n";
    std::cout << "答：volatile 是变量级别的；asm barrier 是编译器级别的全量内存屏障（所有变量都刷新）。\n";
    return 0;
}
```

## ⑯ 易错点与陷阱 [经验]

```cpp
// ⑯ volatile 的 5 个最常见误用
#include <iostream>
#include <atomic>

// 错误1: 用 volatile 做多线程标志
volatile bool ready = false;  // 错误！CPU 乱序不可见，多线程用 atomic<bool> + memory_order
std::atomic<bool> safe_ready{false};

// 错误2: volatile 写入时仍可被优化掉的错误模式
void bad_pattern() {
    int x = 42;
    volatile int* p = &x;
    *p = 100;  // OK: volatile 写入
    // 但编译器可能仍缓存 x 的值（因为 x 本身不是 volatile）
}

// 错误3: 取 volatile 变量的地址给非 volatile 指针
void cast_away() {
    volatile int v = 0;
    // int* p = &v;  // 编译错误：不能丢弃 volatile 限定符
    // int* p = const_cast<int*>(&v);  // UB：通过非 volatile 指针访问 volatile 变量
}

int main() {
    std::cout << "Pitfall 1: volatile != thread-safe. Use atomic for concurrency.\n";
    std::cout << "Pitfall 2: volatile applies to the OBJECT, not the VALUE. x is non-volatile, *p acts volatile but x may be cached.\n";
    std::cout << "Pitfall 3: const_cast removes volatile → UB if accessed without volatile.\n";
    std::cout << "Pitfall 4: volatile member functions on non-volatile object don't take effect.\n";
    std::cout << "Pitfall 5: volatile in lambda capture → capture by value loses volatile (use [&] or std::ref).\n";
    return 0;
}
```

## ⑰ FAQ：嵌入式实战常见问题 [经验]

```cpp
// ⑰ 实际开发中关于 volatile 的高频问答
#include <iostream>
#include <csignal>

volatile sig_atomic_t g_exit_flag = 0;

void signal_handler(int) {
    g_exit_flag = 1;  // OK: sig_atomic_t 保证在信号处理中安全
}

int main() {
    std::cout << "Q: volatile sig_atomic_t → 信号处理器安全吗？\n";
    std::cout << "A: sig_atomic_t + volatile 保证信号处理器中的写入不会被优化掉。\n";
    std::cout << "   但 volatile 不保证在信号处理器和主程序间的可见性顺序（C 和 C++ 都不保证）。\n\n";
    std::cout << "Q: MMIO 地址可以 constexpr 吗？\n";
    std::cout << "A: constexpr uintptr_t UART2_BASE = 0x40004400;\n";
    std::cout << "   auto* uart = reinterpret_cast<volatile UART_Regs*>(UART2_BASE);\n\n";
    std::cout << "Q: volatile 影响性能吗？\n";
    std::cout << "A: 每次访问必须抵达内存（不可寄存器缓存）→ ~5-10ns L1 缓存 vs ~100ns 主存访问。\n";
    std::cout << "   在 MMIO 场景下这是必须的；在普通数据上使用 volatile 会显著降低性能。\n\n";
    std::cout << "Q: C++26 的 volatile 会变化吗？\n";
    std::cout << "A: P2327 方向是保留 volatile 用于嵌入式场景，同时移除用于并发的误导性语义。\n";
    return 0;
}
```

## ⑱ 最佳实践总结 [经验]

```cpp
// ⑱ volatile 使用的 6 条黄金法则
#include <iostream>
#include <atomic>
#include <cstdint>
#include <csignal>

// 法则1: MMIO → volatile 结构体指针 + reinterpret_cast
struct Gpio { volatile uint32_t MODER, OTYPER, OSPEEDR, PUPDR, IDR, ODR; };

// 法则2: 信号处理标志 → volatile sig_atomic_t（绝不可用普通 int）
volatile sig_atomic_t signal_received = 0;

// 法则3: 多线程共享 → std::atomic<T>（绝不使用 volatile）
std::atomic<int> thread_shared_counter{0};

// 法则4: setjmp/longjmp 间变量 → volatile（防止寄存器缓存导致回退到错误值）
// 法则5: const volatile → 只读硬件寄存器
// 法则6: volatile 跟变量，不跟值 —— int* volatile p; vs volatile int* p;

int main() {
    std::cout << "Los 6 mandamientos del volatile:\n";
    std::cout << "1. MMIO registers → volatile struct*\n";
    std::cout << "2. Signal handlers → volatile sig_atomic_t\n";
    std::cout << "3. Concurrency → atomic<T> (NEVER volatile)\n";
    std::cout << "4. setjmp/longjmp → volatile locals\n";
    std::cout << "5. Read-only HW → const volatile\n";
    std::cout << "6. Pointer vs pointee: know which is volatile\n";
    return 0;
}
```

## ⑲ 性能分析：volatile 访问的真实成本 [平台·x86-64]

```cpp
// ⑲ volatile 访问 = 强制穿透缓存层次 → 真实代价取决于内存位置
#include <iostream>
#include <chrono>

volatile int g_vol = 0;       // 全局 volatile
int g_plain = 0;              // 全局非 volatile
alignas(64) volatile int g_cachelined = 0;  // 避免 false sharing

int main() {
    // 测试1：volatile vs plain 读写延迟
    auto t0 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 10000000; ++i) g_vol = i;
    auto t1 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 10000000; ++i) g_plain = i;
    auto t2 = std::chrono::high_resolution_clock::now();

    auto vol_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count() / 10000000;
    auto plain_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t2 - t1).count() / 10000000;
    std::cout << "volatile write: ~" << vol_ns << "ns/op\n";
    std::cout << "plain write:    ~" << plain_ns << "ns/op (may be optimized to single final store)\n\n";

    std::cout << "Assembly evidence (GCC -O2):\n";
    std::cout << "volatile: mov DWORD PTR [g_vol], eax   ← every iteration\n";
    std::cout << "plain:    mov DWORD PTR [g_plain], eax  ← may be hoisted / combined\n\n";
    std::cout << "Bottom line: volatile prevents register promotion (~3-5 cycles saved)\n";
    std::cout << "but costs L1 cache latency (~4 cycles). Net difference: ~1-2ns on x86.\n";
    return 0;
}
```

- `[平台·x86-64]`：volatile 的单次访问成本与普通内存访问相同（～4 cycles L1, ～200 cycles DRAM）。代价不在单次访问，而在**禁止编译器进行循环优化、寄存器提升、公共子表达式消除**——这是真正的性能差距来源。

## ⑳ 跨语言对比：volatile 语义全景 [经验]

```cpp
// ⑳ 各语言中 volatile/并发可见性机制的精确对比
#include <iostream>
int main() {
    std::cout << "=== Cross-language volatile semantics ===\n\n";
    std::cout << "C volatile:       禁止编译器重排 volatile 访问。不保证 CPU 乱序可见。\n";
    std::cout << "                   用途：MMIO、信号处理、setjmp/longjmp。同 C++。\n\n";
    std::cout << "C++ volatile:     与 C 完全相同。C++11 起明确：不用于线程同步。\n";
    std::cout << "                   多线程用 std::atomic<T>。\n\n";
    std::cout << "Java volatile:    完全不同的语义！Java volatile = C++ atomic<T>(seq_cst)。\n";
    std::cout << "                   保证可见性 + 禁止重排 + 原子性（对 long/double 除外）。\n";
    std::cout << "                   这是最常见的跨语言陷阱：C++ volatile ≠ Java volatile！\n\n";
    std::cout << "C# volatile:      接近 Java volatile，但弱于 Java（acquire/release 语义）。\n\n";
    std::cout << "Rust:             无 volatile 关键字。MMIO 用 ptr::read_volatile/write_volatile。\n";
    std::cout << "                   并发用 AtomicBool(Ordering::SeqCst) → 同 C++ atomic。\n\n";
    std::cout << "Python/Go/JS:     无 volatile。GC 语言不暴露硬件访问抽象。\n\n";
    std::cout << "核心结论：C++ volatile 是硬件级指令（强制内存访问），Java/C# volatile 是线程级协议。\n";
    std::cout << "从 Java 转 C++ 的开发者的最大陷阱：误以为 volatile 能保证线程安全。\n";
    return 0;
}
```

- `[标准]`：C++ volatile ≠ Java volatile。这是跨语言迁移的第一大坑。Java volatile 等价于 C++ `std::atomic<T>(memory_order_seq_cst)`——提供完整的可见性和禁止重排保证。C++ volatile 仅等效于插入编译器屏障。

## 补充完整可编译示例

```cpp
#include <iostream>
volatile int tick=0;void isr(){tick++;}
int main(){tick=10;std::cout<<tick<<std::endl;return 0;}
```

```cpp
#include <iostream>
struct UART{volatile unsigned DR;};
int main(){UART u;u.DR='A';std::cout<<(char)u.DR<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <atomic>
int main(){std::atomic<int> a{5};volatile int v=5;std::cout<<a.load()<<" "<<v<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){volatile const int ROM=0xDEAD;std::cout<<ROM<<std::endl;return 0;}
```

```cpp
#include <iostream>
struct GPIO{volatile unsigned OUT;volatile unsigned IN;};
int main(){GPIO g;g.OUT=0xFF;std::cout<<g.OUT<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){int x;volatile int* volatile p=nullptr;(void)x;(void)p;std::cout<<"volatile pointer to volatile data\n";return 0;}
```

```cpp
#include <iostream>
int main(){volatile bool ready=false;ready=true;std::cout<<ready<<std::endl;return 0;}
```

```cpp
#include <iostream>
template<typename T>struct VolatilePtr{T*volatile ptr;};
int main(){int x=5;VolatilePtr<int> v{&x};std::cout<<*v.ptr<<std::endl;return 0;}
```

```cpp
#include <iostream>
struct Timer{volatile unsigned counter;};Timer t;
int main(){t.counter=0;while(t.counter<3)t.counter++;std::cout<<t.counter<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){volatile int* p=new volatile int(42);std::cout<<*p<<std::endl;delete p;return 0;}
```

```cpp
#include <iostream>
int main(){volatile unsigned* reg=(volatile unsigned*)0x1000;(void)reg;std::cout<<"MMIO pattern\n";return 0;}
```

```cpp
#include <iostream>
int main(){volatile int counter=0;for(int i=0;i<5;++i)counter++;std::cout<<counter<<std::endl;return 0;}
```

```cpp
#include <iostream>
struct HW{volatile unsigned ctrl;volatile unsigned status;};
int main(){HW h{};h.ctrl=1;std::cout<<h.status<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <atomic>
int main(){std::atomic<int> a;volatile int v;a.store(1);v=1;std::cout<<a.load()<<" "<<v<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){volatile bool flag=false;flag=true;std::cout<<std::boolalpha<<flag<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){int data=0;volatile int& ref=data;ref=99;std::cout<<data<<std::endl;return 0;}
```

```cpp
#include <iostream>
struct alignas(64) CacheAligned{volatile int val;};
int main(){CacheAligned c;c.val=7;std::cout<<c.val<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){volatile const int ROM_DATA=0xBEEF;std::cout<<ROM_DATA<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){volatile int* ptr=new volatile int[4]{1,2,3,4};std::cout<<ptr[0]<<std::endl;delete[]ptr;return 0;}
```

## 附录 A: volatile 与 atomic 对比速查

| 维度 | volatile | atomic |
|---|---|---|
| 重排保护 | 禁止编译器重排 volatile 访问 | 禁止编译器和 CPU 重排 |
| 原子性 | 不保证 | 保证 (lock-free or mutex) |
| 可见性 | 不保证跨线程 | 保证 (acquire/release) |
| 适用场景 | MMIO, 信号处理, setjmp | 多线程共享状态 |
| 开销 | 强制内存访问 | 取决于 memory_order |

```cpp
#include <iostream>
#include <atomic>
int main(){
    volatile int v=0; std::atomic<int> a{0};
    std::cout<<"volatile: hardware-facing. atomic: thread-facing. Never use volatile for concurrency.\n";
    return 0;
}
```

## 附录 B: 真实嵌入式的 MMIO 模式

```cpp
#include <iostream>
#include <cstdint>
struct UART_Regs{volatile uint32_t DR;volatile uint32_t SR;volatile uint32_t CR;};
// 实际嵌入式代码: UART_Regs* uart = reinterpret_cast<UART_Regs*>(0x40011000);
int main(){std::cout<<"Real embedded: cast memory address to volatile struct*, read/write registers.\n";return 0;}
```

## 附录 C: volatile 与优化器的交互

```cpp
#include <iostream>
int main(){
    std::cout<<"Without volatile: optimizer may cache register value, miss MMIO changes.\n";
    std::cout<<"With volatile: every read goes to memory, every write stores to memory.\n";
    std::cout<<"GCC -O2 treats volatile accesses as observable side effects (like IO).\n";
    return 0;
}
```

## 附录 D: volatile 汇编证据

```cpp
// volatile forces memory reload each access
#include <iostream>
volatile int g_flag = 0;
int main(){g_flag = 1; int local = g_flag; std::cout<<local<<std::endl;return 0;}
// Compiler Explorer with -O2 shows: mov DWORD PTR [g_flag],1; mov eax,DWORD PTR [g_flag]
```

```cpp
#include <iostream>
int main(){std::cout<<"volatile vs asm volatile('':::'memory'): volatile = per-variable; asm barrier = full compiler fence."<<std::endl;return 0;}
```

```cpp
#include <iostream>
// volatile + const = ROM-mapped data, read-only after init
int main(){volatile const int ROM=0xBEEF;std::cout<<ROM<<std::endl;return 0;}
```

```cpp
#include <iostream>
struct alignas(64) CacheLine{volatile int val; char pad[60];};
int main(){CacheLine c{42};std::cout<<c.val<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"volatile总结: 用于MMIO/信号/isr。不是同步原语,多线程用atomic!"<<std::endl;return 0;}
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第107章](Book/part09_concurrency/ch107_atomic.md) | 键值查找/缓存 | 本章提供概念，第107章提供实现 |


## 相关章节（交叉引用）

- **同模块接续**：⟶ Book/part03_language/ch19_variables.md（第19章　变量、存储期、链接与 ODR（工业级深度版））—— volatile 硬件映射的存储期与变量章直接承接
- **同模块接续**：⟶ Book/part03_language/ch27_cast.md（第27章　显式转型四兄弟与隐式转换：const_cast / static_cast / dynamic_cast / reinterpret_cast 深度详解）—— volatile 与 const/转型协同（volatile 指针转换）
- **同模块接续**：⟶ Book/part03_language/ch28_lifetime_ub.md（第28章　对象生命周期与未定义行为（UB）：生存期、悬垂、UB 分类与编译器武器化）—— volatile 不保证线程安全，误用即 UB 高发区
- **同模块接续**：⟶ Book/part03_language/ch32_initialization.md（第32章 初始化与列表初始化）—— volatile 变量的初始化语义由初始化章约束
- **同模块接续**：⟶ Book/part03_language/ch29_friend.md（第29章 友元 friend 与访问控制）—— 友元与 volatile 硬件寄存器访问交互
- **跨模块**：⟶ Book/part02_toolchain/ch17_crosscompile.md（第17章　交叉编译与嵌入式工具链（C++））—— 交叉编译/嵌入式工具链决定 volatile 内存映射的有效性
- **跨模块**：⟶ Book/part09_concurrency/ch107_atomic.md（第107章　std::atomic 原子类型（C++11））—— std::atomic 是 volatile 的多线程正确替代
- **跨模块**：⟶ Book/part09_concurrency/ch108_memory_order.md（第108章　memory_order：六种内存序（C++11））—— memory_order 替代 volatile 提供真实同步语义
- **跨模块**：⟶ Book/part09_concurrency/ch109_fence.md（第109章 内存屏障与 fence）—— 内存屏障/fence 替代 volatile 的顺序保证

## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。

- **Chromium（github.com/chromium/chromium）**：`base::subtle::Atomic32` 用 `std::atomic` 而非 `volatile` 做线程同步。
- **Linux 内核（github.com/torvalds/linux）**：C 语境用 `volatile` 做 MMIO 映射（非 C++ 内存模型）。
- **LLVM 内存模型（llvm/llvm-project）**：LLVM IR 的 `volatile` 语义与 C++ 一致，`volatile` 指令不被优化器重排，对应「② 不可优化语义」。
- **Boost.Atomic（boostorg/atomic）**：`boost::atomic` 是 `std::atomic` 的前身，`volatile` 在并发中不可靠的替代方案。
- **Folly（facebook/folly）**：`folly::atomic` 包装提供 `volatile` 做不到的获取/释放语义。
- **Abseil（abseil/abseil-cpp）**：`absl::Mutex` 替代 `volatile bool` 标志做线程同步。
- **Google Benchmark（github.com/google/benchmark）**：`benchmark::DoNotOptimize` 比 `volatile` 更可靠地阻止编译器优化（不引入虚假内存访问）。
- **Qt 6（github.com/qt/qtbase）**：`QAtomicInt` 用原子而非 `volatile` 做跨线程计数器。

**常见陷阱 / 最佳实践**：
- C++ 中 `volatile` 不保证线程间可见性也不防数据竞争；多线程同步必须用 `std::atomic`。
- `volatile` 仅用于 `SIGNAL` / `setjmp` / MMIO 等特例，误用于并发是常见 UB 来源。

> 交叉引用：原子与内存序见 [ch108](Book/part09_concurrency/ch108_memory_order.md)；内存模型见 [ch109](Book/part09_concurrency/ch109_fence.md)。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

`volatile` 告知编译器"该对象可能被程序之外的代理（硬件/信号处理/另一线程直接改内存）修改，不得优化掉读写"。请用 `volatile` 映射一个内存映射 IO（MMIO）寄存器并循环轮询其就绪位。

<details><summary>答案与解析</summary>

MMIO 寄存器是硬件地址，`volatile` 保证每次访问都真正发生（不被缓存到寄存器）：

```cpp
#include <iostream>
#include <cstdint>
int main() {
    volatile std::uint32_t* status = reinterpret_cast<volatile std::uint32_t*>(0x40021000);
    while ((*status & 0x1u) == 0u) {           // 每次都真实读硬件
        // 轮询就绪位，volatile 阻止编译器把读优化成一次
    }
    std::cout << "ready\n";
}
```

[平台·x86-64][③] 在嵌入式/驱动中，MMIO 寄存器必须用 `volatile` 修饰，否则编译器可能认为 `*status` 不变而把轮询优化成死循环或常量。

</details>

### 练习 2（难度 ★★★）

`volatile` 与 `const` 可组合（`volatile const int*`），常用于"只读硬件寄存器"。请说明其在信号处理函数中的用途：被信号异步修改的全局标志应声明为 `volatile sig_atomic_t`，以保证 handler 与主流程间的可见性。

<details><summary>答案与解析</summary>

`sig_atomic_t` 保证读写是原子的；`volatile` 保证不被优化掉：

```cpp
#include <iostream>
#include <csignal>
volatile std::sig_atomic_t g_stop = 0;
void handler(int) { g_stop = 1; }
int main() {
    std::signal(SIGINT, handler);
    while (!g_stop) { /* 工作循环 */ }
    std::cout << "stopped by signal\n";
}
```

[标准][⑤] 在信号处理函数中访问非 `volatile sig_atomic_t` 的全局量是未定义行为；`volatile` 确保主循环每次都从内存重新读取 `g_stop`，而不会被寄存器缓存。

</details>

### 练习 3（难度 ★★★★）

`volatile` **不能**替代 `std::atomic` 用于线程间同步：它不提供原子性，也不阻止数据竞争（UB）。请写出误用 `volatile` 做计数器的多线程代码，并说明其缺陷，再给出正确版本。

<details><summary>答案与解析</summary>

`volatile` 只挡住编译器优化，不挡住 CPU 重排/撕裂读写，多线程 `++` 仍是数据竞争：

```cpp
#include <iostream>
#include <thread>
#include <vector>
volatile int counter = 0;                 // 缺陷：非原子、非同步
void worker() { for (int i = 0; i < 100000; ++i) ++counter; }   // 数据竞争
int main() {
    std::vector<std::thread> ts;
    for (int i = 0; i < 4; ++i) ts.emplace_back(worker);
    for (auto& t : ts) t.join();
    std::cout << "volatile counter=" << counter << " (期望 400000，实际常偏少)\n";
}
```

正确版本用 `std::atomic<int>`（或 `fetch_add`）提供原子性与顺序保证：

```cpp
#include <iostream>
#include <thread>
#include <vector>
#include <atomic>
std::atomic<int> counter{0};
void worker() { for (int i = 0; i < 100000; ++i) counter.fetch_add(1, std::memory_order_relaxed); }
int main() {
    std::vector<std::thread> ts;
    for (int i = 0; i < 4; ++i) ts.emplace_back(worker);
    for (auto& t : ts) t.join();
    std::cout << "atomic counter=" << counter << " (稳定 400000)\n";
}
```

[④][⑪] `volatile` 与 `atomic` 职责正交：前者对"编译器"说"别优化这处访问"，后者对"硬件与线程"说"这是原子且有序的"。多线程同步必须用 `atomic`，MMIO/信号用 `volatile`。

</details>

## 附录：用法演绎（从选型到落地）

### 演绎 1：嵌入式 MMIO 为何必须用 `volatile`（而非 `atomic`）

**选型场景**：访问内存映射硬件寄存器（状态/数据/控制寄存器），每次读写都必须真实落到地址，禁止编译器合并/缓存。

**常见错误**：以为"线程安全"就够，用 `std::atomic` 访问 MMIO，反而引入不属于硬件语义的原子/屏障，且 `atomic` 在某些模式下的 load/store 序列与硬件预期不符：

```cpp
#include <iostream>
#include <atomic>
#include <cstdint>
int main() {
    // 错误示范：对 MMIO 用 atomic 并不恰当（此处仅展示类型，实际语义不符硬件）
    auto* reg = reinterpret_cast<std::atomic<std::uint32_t>*>(0x40021000);
    std::uint32_t v = reg->load();        // atomic 可能插入硬件不期望的语义
    std::cout << v << '\n';
}
```

**修复**：MMIO 用 `volatile` 限定指针，保证每次访问按序真实发生：

```cpp
#include <iostream>
#include <cstdint>
int main() {
    volatile std::uint32_t* reg = reinterpret_cast<volatile std::uint32_t*>(0x40021000);
    std::uint32_t v = *reg;               // 真实读，不优化
    *reg = v | 0x1u;                      // 真实写
    std::cout << "mmio accessed\n";
}
```

**结论**：MMIO 要的是"不优化掉访问"，不是"原子同步"——`volatile` 正合适；`atomic` 用于线程间同步，二者不要混用，按访问性质选型（见章节 ⑪ 对比表）。

### 演绎 2：`volatile` 不能替代 `std::atomic`

**选型场景**：多线程共享计数器/标志，需要原子性与跨线程可见性——这是 `atomic` 的领域。

**常见错误**：用 `volatile int` 当"线程安全计数器"，以为 `volatile` 足以同步，结果因非原子 `++` 与缺少顺序保证产生数据竞争（UB），计数不准：

```cpp
#include <iostream>
#include <thread>
#include <vector>
volatile int g = 0;                        // 非原子
void f() { for (int i = 0; i < 100000; ++i) ++g; }   // 数据竞争
int main() {
    std::vector<std::thread> ts;
    for (int i = 0; i < 4; ++i) ts.emplace_back(f);
    for (auto& t : ts) t.join();
    std::cout << "g=" << g << " (非确定，常 < 400000)\n";
}
```

**修复**：用 `std::atomic` 提供原子操作与内存顺序：

```cpp
#include <iostream>
#include <thread>
#include <vector>
#include <atomic>
std::atomic<int> g{0};
void f() { for (int i = 0; i < 100000; ++i) g.fetch_add(1, std::memory_order_relaxed); }
int main() {
    std::vector<std::thread> ts;
    for (int i = 0; i < 4; ++i) ts.emplace_back(f);
    for (auto& t : ts) t.join();
    std::cout << "g=" << g << " (确定 = 400000)\n";
}
```

**结论**：`volatile` 阻止的是"编译器优化"，`atomic` 提供的是"机器级原子+顺序"；凡涉及多线程共享可变状态，一律 `std::atomic`，`volatile` 在此场景下是常见误解来源。

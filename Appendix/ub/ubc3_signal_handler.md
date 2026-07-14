# UB-C3 non-atomic signal handler（信号处理函数内非原子访问）

**分类**：并发/生命周期 UB ｜ **检测工具**：TSan / `-Wclobbered`
**源码**：[ub_signal_handler.cpp](./ub_signal_handler.cpp)

---

## ① 真实代码

```cpp
#include <cstdio>
#include <csignal>

int counter = 0;                 // ❌ 非原子，handler 与主流程并发访问 → UB

void handler(int) {
    ++counter;                   // ❌ 在信号上下文中修改非原子全局
}

int main() {
    std::signal(SIGINT, handler);
    for (int i = 0; i < 5; ++i) std::raise(SIGINT);
    std::printf("counter = %d\n", counter);
    return 0;
}
```

## ② 编译器行为（本机实测）

**无警告**（GCC 不检验信号处理函数的原子性约束）。

## ③ 运行时表现（本机实测，无 TSan）

```
（异常终止，exit code = 3）
```

> 本例中 `std::raise(SIGINT)` 在 MinGW 下触发信号后，非原子 `counter` 的读写与
> 外部代码交错，导致进程以异常码退出。这表明 UB 已实际发作——而非"看似正常"。

## ④ 规则与根因

C++ 标准对信号处理函数有严格限制（[support.signal]）：

- 只允许调用 **`std::signal`** 与读/写 **`volatile sig_atomic_t`** 类型的对象；
- 允许调用 **`std::atomic`** 操作（C++11 起，配合恰当 memory_order）；
- **禁止**在 handler 中访问其它非原子变量、调用非 async-signal-safe 函数。

`++counter`（非原子 `int`）在 handler 与主流程间构成数据竞争 → 未定义行为。
更严重的是：若 handler 调用了 `printf` 等非 async-signal-safe 函数，还会与
主流程的 IO 缓冲竞争导致死锁/崩溃。

## ⑤ 修复

```cpp
#include <cstdio>
#include <csignal>
#include <atomic>

std::atomic<int> counter{0};                 // ✅ 原子，handler 内安全
void handler(int) { counter.fetch_add(1, std::memory_order_relaxed); }

int main() {
    std::signal(SIGINT, handler);
    while (counter.load(std::memory_order_relaxed) < 5) {
        // 主流程不并发写 counter，仅 handler 写 → 无竞争
    }
    std::printf("counter = %d\n", counter.load());
    return 0;
}
```

原则：**信号 handler 只做最少工作**——置一个 `std::atomic`/`volatile sig_atomic_t`
标志，真正的逻辑回到主流程轮询该标志后执行。

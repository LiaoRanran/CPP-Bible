# UB-C1 data race（数据竞争）

**分类**：并发 UB ｜ **检测工具**：TSan (`-fsanitize=thread`) / 硬件内存模型
**源码**：[ub_data_race.cpp](./ub_data_race.cpp)

---

## ① 真实代码

```cpp
#include <cstdio>
#include <thread>

int g = 0;                       // 非原子全局

void worker() {
    for (int i = 0; i < 1'000'000; ++i) ++g;   // ❌ 与另一线程并发写，无同步
}

int main() {
    std::thread a(worker), b(worker);
    a.join(); b.join();
    std::printf("g = %d  (期望 2000000，但可能更少)\n", g);
    return 0;
}
```

## ② 编译器行为（本机实测，GCC 15.3.0 `-O2`）

**无警告**。数据竞争是运行时/内存模型层面的 UB，静态分析通常不报（除非配合 TSan 插桩）。

## ③ 运行时表现（本机实测，无 TSan）

连续 3 次运行：

```
g = 2000000  (期望 2000000，但可能更少)
g = 2000000  (期望 2000000，但可能更少)
g = 2000000  (期望 2000000，但可能更少)
```

> **这正是 data race 最危险之处**：它本次"恰好正确"。竞争的结果取决于线程调度、
> 缓存行所有权、CPU 时序——**测试通过不代表正确**，上线换台机器/换负载就可能
> 丢更新（读到 1999998 之类）。非确定性是 UB 的本质。

## ④ TSan 报告格式（DOC-REPORT，非本机捕获）

本机 MinGW 无 `libtsan`，以下为具备 TSan 运行时的工具链**预期**格式：

```
WARNING: ThreadSanitizer: data race (pid=12345)
  Write of size 4 at 0x... by thread T2:
    #0 worker ub_data_race.cpp:8
  Previous write of size 4 at 0x... by thread T1:
    #0 worker ub_data_race.cpp:8
  Location is global 'g' of size 4 at 0x...
```

## ⑤ 根因

C++ 内存模型要求：对同一非原子对象的两次访问若至少其一为写，且不在同一线程、
且无 happens-before 关系（锁/原子/线程创建等），则为数据竞争 → 未定义行为。
`++g` 读作 load-add-store 三步，两线程交错导致更新丢失。

## ⑥ 修复

```cpp
#include <cstdio>
#include <thread>
#include <atomic>

std::atomic<int> g{0};                              // 原子：定义良好的并发计数
void worker() {
    for (int i = 0; i < 1'000'000; ++i) g.fetch_add(1, std::memory_order_relaxed);
}
int main() {
    std::thread a(worker), b(worker);
    a.join(); b.join();
    std::printf("g = %d (恒为 2000000)\n", g.load());
}
```

或用 `std::mutex` 保护临界区。计数场景首选 `std::atomic`（无锁、零开销）。

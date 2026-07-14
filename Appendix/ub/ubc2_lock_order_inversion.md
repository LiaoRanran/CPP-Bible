# UB-C2 lock-order-inversion（锁顺序反转 → 死锁）

**分类**：并发 UB ｜ **检测工具**：TSan（报 lock-order-inversion）/ 死锁复现
**源码**：[ub_lock_order_inversion.cpp](./ub_lock_order_inversion.cpp)

---

## ① 真实代码

```cpp
#include <chrono>
#include <cstdio>
#include <mutex>
#include <thread>

std::mutex m1, m2;

void threadA() {
    std::lock_guard<std::mutex> l1(m1);
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
    std::lock_guard<std::mutex> l2(m2);     // ❌ 此时 m2 可能已被 B 持有
    std::printf("threadA 完成\n");
}
void threadB() {
    std::lock_guard<std::mutex> l1(m2);     // B 先拿 m2
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
    std::lock_guard<std::mutex> l2(m1);     // ❌ 此时 m1 已被 A 持有
    std::printf("threadB 完成\n");
}
int main() {
    std::thread a(threadA), b(threadB);
    a.join(); b.join();
    std::printf("done（若看到此行说明未死锁）\n");
}
```

## ② 编译器行为（本机实测）

**无警告**。锁顺序反转是逻辑缺陷，编译器无法静态判定。

## ③ 运行时表现（本机实测，死锁复现）

用 `timeout 5 ./dead` 限制运行时间：

```
（无任何输出）
$ echo "timeout exit = $?"
timeout exit = 124        # 124 = 被 timeout 杀掉 → 程序卡死，从未打印 done → 确认死锁
```

> 进程在 `a.join()/b.join()` 处永久阻塞：A 持 m1 等 m2，B 持 m2 等 m1，循环等待。

## ④ TSan 报告格式（DOC-REPORT，非本机捕获）

```
WARNING: ThreadSanitizer: lock-order-inversion (potential deadlock)
  Cycle in lock order graph: M1 -> M2 -> M1
  Thread T1 acquired M1 then M2
  Thread T2 acquired M2 then M1
```

## ⑤ 根因

死锁四条件（Coffman）在此满足：互斥（锁）、持有等待（A 持 m1 等 m2）、
不可剥夺、循环等待（A↔B）。两线程以**相反顺序**获取同一对锁，必现循环等待。

## ⑥ 修复

```cpp
// 方案 1：全局固定加锁顺序（永远先 m1 后 m2）
void both() {
    std::scoped_lock lk(m1, m2);   // C++17：一次性锁多个，内部用避免死锁算法
    std::printf("完成\n");
}
// 方案 2：用 std::lock(m1, m2) + std::lock_guard(..., std::adopt_lock)
```

`std::scoped_lock(m1, m2)` 是首选——它用 `std::lock` 的死锁避免算法一次性获取多锁，
从根本上消除顺序反转。多锁场景**严禁手写顺序加锁**。

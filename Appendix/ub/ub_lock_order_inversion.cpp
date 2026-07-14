// UB-C2 lock-order-inversion（锁顺序反转）→ 死锁
// 两个线程以相反顺序获取同一对锁：tA 拿 m1→m2，tB 拿 m2→m1，必然互等。
// 编译: g++ -std=c++23 -O2 -pthread -o dead ub_lock_order_inversion.cpp
// 实证: timeout 5 ./dead   →  5 秒后被 timeout 杀掉（证明程序卡死，未打印 done）
#include <chrono>
#include <cstdio>
#include <mutex>
#include <thread>

std::mutex m1, m2;

void threadA() {
    std::lock_guard<std::mutex> l1(m1);
    std::this_thread::sleep_for(std::chrono::milliseconds(50));  // 给 B 时间拿到 m2
    std::lock_guard<std::mutex> l2(m2);                          // ❌ 此时 m2 已被 B 持有
    std::printf("threadA 完成\n");
}

void threadB() {
    std::lock_guard<std::mutex> l1(m2);                          // B 先拿 m2
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
    std::lock_guard<std::mutex> l2(m1);                          // ❌ 此时 m1 已被 A 持有
    std::printf("threadB 完成\n");
}

int main() {
    std::thread a(threadA), b(threadB);
    a.join(); b.join();
    std::printf("done（若看到此行说明未死锁）\n");
    return 0;
}

// ch95 示例：用 std::chrono 真实测量 STL 算法 vs 手写循环的性能
// 编译并运行（release -O2）：
//   g++ -std=c++23 -O2 _ch95_perf.cpp -o _ch95_perf.exe
//   ./_ch95_perf.exe
// 计时用 std::chrono::steady_clock，多次重复取中位数量级。
#include <algorithm>
#include <chrono>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>

static double now_ms() {
    return std::chrono::duration<double, std::milli>(
               std::chrono::steady_clock::now().time_since_epoch())
        .count();
}

int main() {
    const int N = 5'000'000;
    std::vector<int> v(N);
    std::iota(v.begin(), v.end(), 0);
    // 打乱以保证 cache 行为无特殊偏置
    std::mt19937 rng(42);
    std::shuffle(v.begin(), v.end(), rng);  // 仅取乱序，测最坏访问局部性

    // ── A：for_each vs 手写 range-for（应几乎相等）──
    {
        std::vector<int> w = v;
        double t0 = now_ms();
        long s = 0;
        for (int i = 0; i < 20; ++i)
            std::for_each(w.begin(), w.end(),
                          [&s](int x) { s += x; });
        double t1 = now_ms();
        std::cout << "[A] std::for_each  x20 : " << (t1 - t0)
                  << " ms  (校验和=" << s << ")\n";
    }
    {
        std::vector<int> w = v;
        double t0 = now_ms();
        long s = 0;
        for (int i = 0; i < 20; ++i)
            for (int x : w) s += x;
        double t1 = now_ms();
        std::cout << "[A] range-for   x20 : " << (t1 - t0)
                  << " ms  (校验和=" << s << ")\n";
    }

    // ── B：count_if vs 手写循环 ──
    {
        double t0 = now_ms();
        long c = 0;
        for (int i = 0; i < 20; ++i)
            c = std::count_if(v.begin(), v.end(),
                              [](int x) { return x % 7 == 0; });
        double t1 = now_ms();
        std::cout << "[B] std::count_if x20 : " << (t1 - t0)
                  << " ms  (个数=" << c << ")\n";
    }
    {
        double t0 = now_ms();
        long c = 0;
        for (int i = 0; i < 20; ++i) {
            long k = 0;
            for (int x : v) if (x % 7 == 0) ++k;
            c = k;
        }
        double t1 = now_ms();
        std::cout << "[B] hand-loop  x20 : " << (t1 - t0)
                  << " ms  (个数=" << c << ")\n";
    }

    // ── C：lower_bound 二分 vs 线性查找（已排序时差距巨大）──
    std::vector<int> sorted = v;
    std::sort(sorted.begin(), sorted.end());
    const int key = sorted[sorted.size() / 2];
    {
        double t0 = now_ms();
        volatile bool found = false;
        for (int i = 0; i < 200; ++i) {
            auto it = std::lower_bound(sorted.begin(), sorted.end(), key);
            found = (it != sorted.end() && *it == key);
        }
        double t1 = now_ms();
        std::cout << "[C] std::lower_bound x200 : " << (t1 - t0)
                  << " ms  (found=" << found << ")\n";
    }
    {
        double t0 = now_ms();
        volatile bool found = false;
        for (int i = 0; i < 200; ++i) {
            bool f = false;
            for (int x : sorted) if (x == key) { f = true; break; }
            found = f;
        }
        double t1 = now_ms();
        std::cout << "[C] linear-search  x200 : " << (t1 - t0)
                  << " ms  (found=" << found << ")\n";
    }
    return 0;
}

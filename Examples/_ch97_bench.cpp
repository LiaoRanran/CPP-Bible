// 文件：Examples/_ch97_bench.cpp
// 编译运行：g++ -std=c++23 -O2 _ch97_bench.cpp -o _ch97_bench && _ch97_bench.exe
#include <algorithm>
#include <vector>
#include <chrono>
#include <random>
#include <iostream>

int main() {
    const int N = 1 << 20;            // 1,048,576 个有序元素
    std::vector<int> v(N);
    for (int i = 0; i < N; ++i) v[i] = i * 2;   // 升序偶数

    std::mt19937 rng(20240707);
    std::uniform_int_distribution<int> dis(0, 2 * N);

    const int reps = 200;
    volatile int sink = 0;

    // 线性查找：std::find 逐个比较
    auto t0 = std::chrono::high_resolution_clock::now();
    for (int k = 0; k < reps; ++k) {
        int target = dis(rng);
        auto it = std::find(v.begin(), v.end(), target);
        sink = static_cast<int>(it - v.begin());
    }
    auto t1 = std::chrono::high_resolution_clock::now();

    // 二分查找：std::lower_bound
    auto t2 = std::chrono::high_resolution_clock::now();
    for (int k = 0; k < reps; ++k) {
        int target = dis(rng);
        auto it = std::lower_bound(v.begin(), v.end(), target);
        sink = static_cast<int>(it - v.begin());
    }
    auto t3 = std::chrono::high_resolution_clock::now();

    double lin = std::chrono::duration<double, std::micro>(t1 - t0).count();
    double bin = std::chrono::duration<double, std::micro>(t3 - t2).count();

    std::cout << "N=" << N << " reps=" << reps << "\n";
    std::cout << "linear(find)   : " << lin << " us  (per-op " << (lin / reps) << " us)\n";
    std::cout << "binary(lower)  : " << bin << " us  (per-op " << (bin / reps) << " us)\n";
    std::cout << "speedup        : " << (lin / bin) << "x\n";
    std::cout << "sink=" << sink << "\n";   // 防止被整体优化掉
    return 0;
}

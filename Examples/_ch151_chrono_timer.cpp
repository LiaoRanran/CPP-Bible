// ④ std::chrono 高精度计时（真实运行示例）
// 见 Examples/_ch151_chrono_timer.cpp
#include <cstdio>
#include <chrono>
#include <thread>

int main() {
    using namespace std::chrono;
    // high_resolution_clock 在 libstdc++ 中即 steady_clock 别名
    auto start = high_resolution_clock::now();
    volatile unsigned long long acc = 0;
    for (unsigned long long i = 0; i < 200'000'000ULL; ++i) acc += i;
    auto end = high_resolution_clock::now();

    auto ns = duration_cast<nanoseconds>(end - start).count();
    auto us = duration<double, std::micro>(end - start).count();
    auto ms = duration<double, std::milli>(end - start).count();
    std::printf("chrono: acc=%llu ns=%lld us=%.2f ms=%.4f\n",
                acc, (long long)ns, us, ms);
    return 0;
}

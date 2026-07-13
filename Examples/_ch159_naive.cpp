// 文件：Examples/_ch159_naive.cpp
// 行号：1
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 Examples/_ch159_naive.cpp -o Examples/_ch159_naive.exe
// 说明：反模式——每个任务都 new 一个 std::thread（开销巨大、可扩展性差）。
#include <chrono>
#include <cstdio>
#include <thread>
#include <vector>

int main() {
    const int N = 2000;
    auto t0 = std::chrono::steady_clock::now();
    std::vector<std::thread> ts;
    ts.reserve(N);
    for (int i = 0; i < N; ++i)
        ts.emplace_back([] { volatile long s = 0; for (long k = 0; k < 50000; ++k) s += k; });
    for (auto& t : ts) t.join();
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("naive per-task-thread : %.3f ms\n", ms);
}

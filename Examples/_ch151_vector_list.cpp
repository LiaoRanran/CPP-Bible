// ⑰ 真实案例：vector 顺序遍历 vs list 顺序遍历（真实数字见正文）
// 见 Examples/_ch151_vector_list.cpp
#include <cstdio>
#include <vector>
#include <list>
#include <chrono>

int main() {
    const int N = 5'000'000;
    std::vector<int> vec(N);
    std::list<int> lst(N);
    for (int i = 0; i < N; ++i) { vec[i] = i; lst.push_back(i); }

    // vector：连续内存，缓存友好
    auto t0 = std::chrono::steady_clock::now();
    volatile long long sv = 0;
    for (int x : vec) sv += x;
    auto t1 = std::chrono::steady_clock::now();

    // list：节点散落，缓存不友好
    auto t2 = std::chrono::steady_clock::now();
    volatile long long sl = 0;
    for (int x : lst) sl += x;
    auto t3 = std::chrono::steady_clock::now();

    std::printf("vector traverse: ms=%.3f\n", std::chrono::duration<double, std::milli>(t1 - t0).count());
    std::printf("list   traverse: ms=%.3f\n", std::chrono::duration<double, std::milli>(t3 - t2).count());
    return 0;
}

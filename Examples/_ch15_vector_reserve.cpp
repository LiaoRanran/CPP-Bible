// ⑤ 真实微基准：std::vector push_back 是否 reserve 的耗时对比
// 编译：g++ -std=c++23 -O2 _ch15_vector_reserve.cpp -o _ch15_vector_reserve
// 运行：./_ch15_vector_reserve
#include <vector>
#include <chrono>
#include <cstdio>

static const long N = 20'000'000;

int main() {
    // A：不 reserve，push_back 触发多次重新分配
    {
        std::vector<long> v;
        auto t0 = std::chrono::steady_clock::now();
        for (long i = 0; i < N; ++i) v.push_back(i);
        auto t1 = std::chrono::steady_clock::now();
        auto ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
        std::printf("no_reserve   : %8.2f ms   size=%ld\n", ms, (long)v.size());
    }

    // B：先 reserve(N)，push_back 无重新分配
    {
        std::vector<long> v;
        v.reserve(N);
        auto t0 = std::chrono::steady_clock::now();
        for (long i = 0; i < N; ++i) v.push_back(i);
        auto t1 = std::chrono::steady_clock::now();
        auto ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
        std::printf("with_reserve : %8.2f ms   size=%ld\n", ms, (long)v.size());
    }
    return 0;
}

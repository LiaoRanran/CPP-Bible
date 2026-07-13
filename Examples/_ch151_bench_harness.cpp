// ⑦ 自包含基准 harness（等价 Google Benchmark 的 State 循环）
// 见 Examples/_ch151_bench_harness.cpp
#include <cstdio>
#include <chrono>
#include <vector>
#include <numeric>

struct State {
    int iterations = 1000;
    void Report(const char* name, double ms_per_iter) const {
        std::printf("BM_%s: %8.4f ms/iter  (iters=%d)\n", name, ms_per_iter, iterations);
    }
};

static void BM_fill(State& st) {
    double total = 0;
    for (int it = 0; it < st.iterations; ++it) {
        std::vector<int> v(1'000'000);
        auto t0 = std::chrono::steady_clock::now();
        std::fill(v.begin(), v.end(), it);     // 被测操作
        auto t1 = std::chrono::steady_clock::now();
        total += std::chrono::duration<double, std::milli>(t1 - t0).count();
    }
    st.Report("fill", total / st.iterations);
}

int main() {
    State st; st.iterations = 200;
    BM_fill(st);
    return 0;
}

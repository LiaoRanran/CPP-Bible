// ⑯ 基准框架骨架（示意，非本机实测数字）
#include <benchmark/benchmark.h>
static void BM_dot(benchmark::State& s) {
    const int n = 1 << 16;
    double a[n], b[n];
    for (int i = 0; i < n; ++i) { a[i] = i; b[i] = 1.0 / (i + 1); }
    for (auto _ : s)
        benchmark::DoNotOptimize(dot(a, b, n));   // 防止被测代码被整体消去
}
BENCHMARK(BM_dot);
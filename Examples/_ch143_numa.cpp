#include <thread>
#include <vector>
#include <cstdio>

// ⑱ NUMA 思路（自包含示意）：让数据“在访问它的线程所在节点上首次分配”
// 真实 NUMA 绑定需要 libnuma(numactl)，此处用分块 + 线程局部累加表达 locality
void local_accumulate(const float* data, int n, int threads) {
    int chunk = n / threads;
    std::vector<std::thread> ts;
    std::vector<double> partial(threads, 0.0);
    for (int t = 0; t < threads; ++t) {
        int lo = t * chunk, hi = (t == threads - 1) ? n : lo + chunk;
        ts.emplace_back([&, t, lo, hi] {
            double s = 0.0;
            for (int i = lo; i < hi; ++i) s += data[i];  // 各线程只碰自己那块
            partial[t] = s;
        });
    }
    for (auto& th : ts) th.join();
    double total = 0;
    for (double p : partial) total += p;
    std::printf("NUMA-local sum = %.1f\n", total);
}

int main() {
    std::vector<float> d(1'000'000, 1.0f);
    local_accumulate(d.data(), static_cast<int>(d.size()), 4);
    return 0;
}

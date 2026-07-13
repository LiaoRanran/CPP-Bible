#include <thread>
#include <vector>

// ⑮ 分块并行：把连续数组切成等长的块，每线程一块，互不触碰对方内存
void chunked(float* a, const float* b, int n, float k, int threads) {
    int chunk = n / threads;
    std::vector<std::thread> ts;
    for (int t = 0; t < threads; ++t) {
        int lo = t * chunk;
        int hi = (t == threads - 1) ? n : lo + chunk;   // 最后一块补齐余数
        ts.emplace_back([=] {
            for (int i = lo; i < hi; ++i)
                a[i] = b[i] * k;
        });
    }
    for (auto& th : ts) th.join();
}

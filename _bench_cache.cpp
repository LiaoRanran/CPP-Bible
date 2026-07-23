// _bench_cache.cpp — ch154 同规格 D5 真实基准 (GCC 15.3.0 -O2, this machine)
// 复跑 ch154 正文三件套 + 打印标准常量实际值，得到可复现真实数字。
#include <iostream>
#include <vector>
#include <thread>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <algorithm>
#include <new>

using namespace std;
using namespace std::chrono;

// ---- 0) 标准常量取值（D4 实证：证明 hardware_destructive_interference_size == 64）----
void probe_constants() {
    cout << "hardware_destructive_interference_size = "
         << hardware_destructive_interference_size << "\n";
    cout << "hardware_constructive_interference_size = "
         << hardware_constructive_interference_size << "\n";
}

// ---- 1) 伪共享 bad vs good ----
struct SharedBad {
    atomic<uint64_t> a{0};
    atomic<uint64_t> b{0};                       // 与 a 同 64B 行 → 伪共享
};
struct SharedGood {
    alignas(64) atomic<uint64_t> a{0};
    alignas(64) atomic<uint64_t> b{0};           // 各占不同 64B 行
};

double bench_false_sharing(bool good) {
    constexpr uint64_t IT = 20'000'000;
    auto run = [&]() -> double {
        if (good) {
            SharedGood s;
            auto t0 = steady_clock::now();
            thread t1([&]{ for (uint64_t i=0;i<IT;++i) s.a.fetch_add(1, memory_order_relaxed); });
            thread t2([&]{ for (uint64_t i=0;i<IT;++i) s.b.fetch_add(1, memory_order_relaxed); });
            t1.join(); t2.join();
            auto t1_ = steady_clock::now();
            return duration<double, milli>(t1_ - t0).count();
        } else {
            SharedBad s;
            auto t0 = steady_clock::now();
            thread t1([&]{ for (uint64_t i=0;i<IT;++i) s.a.fetch_add(1, memory_order_relaxed); });
            thread t2([&]{ for (uint64_t i=0;i<IT;++i) s.b.fetch_add(1, memory_order_relaxed); });
            t1.join(); t2.join();
            auto t1_ = steady_clock::now();
            return duration<double, milli>(t1_ - t0).count();
        }
    };
    double best = 1e9;
    for (int k=0;k<5;++k) best = min(best, run());
    return best;
}

// ---- 2) AoS vs SoA ----
struct Vec3 { float x, y, z; };
double bench_aos() {
    constexpr int N = 4'000'000;
    vector<Vec3> aos(N, {1.0f, 2.0f, 3.0f});
    float s = 0.0f;
    auto t0 = steady_clock::now();
    for (auto& e : aos) s += e.x;                // 每读 4B 实际搬 12B
    auto t1 = steady_clock::now();
    volatile float sink = s; (void)sink;
    return duration<double, milli>(t1 - t0).count();
}
double bench_soa() {
    constexpr int N = 4'000'000;
    vector<float> x(N, 1.0f);
    float s = 0.0f;
    auto t0 = steady_clock::now();
    for (float v : x) s += v;                    // 全连续，带宽利用率 100%
    auto t1 = steady_clock::now();
    volatile float sink = s; (void)sink;
    return duration<double, milli>(t1 - t0).count();
}

// 多字段：用满 x/y/z —— 才能真正逼出 SoA 的向量化优势（单字段时预取器已抹平差距）
double bench_aos3() {
    constexpr int N = 4'000'000;
    vector<Vec3> aos(N, {1.0f, 2.0f, 3.0f});
    float sx=0, sy=0, sz=0;
    auto t0 = steady_clock::now();
    for (auto& e : aos) { sx += e.x; sy += e.y; sz += e.z; }
    auto t1 = steady_clock::now();
    volatile float sink = sx + sy + sz; (void)sink;
    return duration<double, milli>(t1 - t0).count();
}
double bench_soa3() {
    constexpr int N = 4'000'000;
    vector<float> x(N,1.0f), y(N,2.0f), z(N,3.0f);
    float sx=0, sy=0, sz=0;
    auto t0 = steady_clock::now();
    for (size_t i=0;i<N;++i) { sx += x[i]; sy += y[i]; sz += z[i]; }
    auto t1 = steady_clock::now();
    volatile float sink = sx + sy + sz; (void)sink;
    return duration<double, milli>(t1 - t0).count();
}

// ---- 3) 行优先 vs 列优先 ----
double bench_row() {
    constexpr int M = 4096;
    vector<int> a(M * M, 1);
    long s = 0;
    auto t0 = steady_clock::now();
    for (int i = 0; i < M; ++i)                  // 行优先：a[i*M+j] 连续
        for (int j = 0; j < M; ++j) s += a[i * M + j];
    auto t1 = steady_clock::now();
    volatile long sink = s; (void)sink;
    return duration<double, milli>(t1 - t0).count();
}
double bench_col() {
    constexpr int M = 4096;
    vector<int> a(M * M, 1);
    long s = 0;
    auto t0 = steady_clock::now();
    for (int j = 0; j < M; ++j)                  // 列优先：跨行，步长 M*4B
        for (int i = 0; i < M; ++i) s += a[i * M + j];
    auto t1 = steady_clock::now();
    volatile long sink = s; (void)sink;
    return duration<double, milli>(t1 - t0).count();
}

template<class F> double median_of(F f, int rounds = 5) {
    vector<double> v;
    for (int k = 0; k < rounds; ++k) v.push_back(f());
    sort(v.begin(), v.end());
    return v[rounds / 2];
}

int main() {
    probe_constants();

    cout << "\n--- 1) 伪共享 (IT=20M/线程, 2线程, 取5轮最优ms) ---\n";
    double bad  = bench_false_sharing(false);
    double good = bench_false_sharing(true);
    cout << "false-sharing bad  = " << bad  << " ms\n";
    cout << "false-sharing good = " << good << " ms\n";
    cout << "ratio bad/good = " << (bad / good) << "x\n";

    cout << "\n--- 2) AoS vs SoA (N=4M, 仅累加x, 取5轮中位ms) ---\n";
    double aos = median_of(bench_aos);
    double soa = median_of(bench_soa);
    cout << "AoS = " << aos << " ms\n";
    cout << "SoA = " << soa << " ms\n";
    cout << "ratio aos/soa = " << (aos / soa) << "x\n";

    cout << "\n--- 2b) AoS vs SoA 用满 x/y/z (逼出向量化, 取5轮中位ms) ---\n";
    double aos3 = median_of(bench_aos3);
    double soa3 = median_of(bench_soa3);
    cout << "AoS(3f) = " << aos3 << " ms\n";
    cout << "SoA(3f) = " << soa3 << " ms\n";
    cout << "ratio aos3/soa3 = " << (aos3 / soa3) << "x\n";

    cout << "\n--- 3) 行优先 vs 列优先 (M=4096, 取5轮中位ms) ---\n";
    double row = median_of(bench_row);
    double col = median_of(bench_col);
    cout << "row = " << row << " ms\n";
    cout << "col = " << col << " ms\n";
    cout << "ratio col/row = " << (col / row) << "x\n";
    return 0;
}

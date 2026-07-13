#include <thread>
#include <chrono>
#include <cstdio>

// ⑬ False Sharing：两个线程改写同一缓存行上的不同变量，互相使对方失效
struct Shared { volatile long a = 0; volatile long b = 0; };   // a、b 同处一个 64B 缓存行
struct Padded { volatile long a = 0; char pad[64]; volatile long b = 0; }; // b 隔离

static const long ITER = 30'000'000;

double bench_shared(long& out) {
    Shared s{};
    auto t0 = std::chrono::steady_clock::now();
    std::thread th1([&] { for (long i = 0; i < ITER; ++i) ++s.a; });
    std::thread th2([&] { for (long i = 0; i < ITER; ++i) ++s.b; });
    th1.join(); th2.join();
    auto tEnd = std::chrono::steady_clock::now();
    out = s.a + s.b;     // 结果被消费
    return std::chrono::duration<double>(tEnd - t0).count();
}

double bench_padded(long& out) {
    Padded s{};
    auto t0 = std::chrono::steady_clock::now();
    std::thread th1([&] { for (long i = 0; i < ITER; ++i) ++s.a; });
    std::thread th2([&] { for (long i = 0; i < ITER; ++i) ++s.b; });
    th1.join(); th2.join();
    auto tEnd = std::chrono::steady_clock::now();
    out = s.a + s.b;
    return std::chrono::duration<double>(tEnd - t0).count();
}

int main() {
    long o1, o2;
    double ts = bench_shared(o1);
    double tp = bench_padded(o2);
    std::printf("false-sharing(同线): %.4f s  (sum=%ld)\n", ts, o1);
    std::printf("padded(隔离)      : %.4f s  (sum=%ld)\n", tp, o2);
    return 0;
}

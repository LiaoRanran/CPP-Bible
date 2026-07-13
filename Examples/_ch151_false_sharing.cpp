// ⑮' 伪共享（false sharing）：相邻缓存行被多核争用 [平台]
// 见 Examples/_ch151_false_sharing.cpp
#include <cstdio>
#include <chrono>
#include <thread>
#include <vector>

struct Shared { long long a = 0, b = 0; };      // a,b 同缓存行 → 伪共享
struct Padded { alignas(64) long long a = 0; alignas(64) long long b = 0; };

template <typename T>
static double run_two_threads() {
    T s;
    auto ta = std::chrono::steady_clock::now();
    std::thread th1([&]{ for (int i=0;i<50'000'000;++i) s.a += i; });
    std::thread th2([&]{ for (int i=0;i<50'000'000;++i) s.b += i; });
    th1.join(); th2.join();
    auto tb = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::milli>(tb - ta).count();
}

int main() {
    std::printf("false_sharing(shared):  ms=%.3f\n", run_two_threads<Shared>());
    std::printf("false_sharing(padded):  ms=%.3f\n", run_two_threads<Padded>());
    return 0;
}

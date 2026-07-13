// ⑯ 性能基准：消除前后耗时对比（示意量级，本机可实测）
#include <cstdio>
#include <chrono>

struct Vec {
    double d[256];
    Vec() { for (int i = 0; i < 256; ++i) d[i] = i; }
    Vec(const Vec& o) { for (int i = 0; i < 256; ++i) d[i] = o.d[i]; }  // 昂贵拷贝
};

Vec make_vec() {
    Vec v;           // NRVO：无拷贝
    return v;
}

double sum(const Vec& v) { double s = 0; for (int i = 0; i < 256; ++i) s += v.d[i]; return s; }

int main() {
    const int N = 1000000;
    auto t0 = std::chrono::steady_clock::now();
    double acc = 0;
    for (int i = 0; i < N; ++i) {
        Vec v = make_vec();   // 无拷贝路径
        acc += sum(v);
    }
    auto t1 = std::chrono::steady_clock::now();
    std::printf("elapsed_ms=%.2f acc=%.1f\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), acc);
    return 0;
}

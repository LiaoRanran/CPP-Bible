// _bench_d5_47_virt.cpp — ch47 D5: 直接调用 vs 虚调用 vs CRTP 静态分发
// g++ -O2 -std=c++17
// 防 devirt 设计：多态数组打乱两种派生类型 + 工厂在独立翻译单元不可见? 单文件下
// 用 volatile 选择器构造对象，阻止编译器证明具体类型。
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <memory>
#include <random>
#include <vector>

using Clock = std::chrono::steady_clock;
static double ms(Clock::time_point a, Clock::time_point b) {
    return std::chrono::duration<double, std::milli>(b - a).count();
}
template <class F> static double median5(F f) {
    std::vector<double> t;
    for (int i = 0; i < 5; ++i) t.push_back(f());
    std::sort(t.begin(), t.end());
    return t[2];
}
volatile long long g_sink = 0;
volatile int g_select = 0;  // 运行期才知道的类型选择器

// ---- 虚多态 ----
struct Base {
    virtual long long f(long long x) const = 0;
    virtual ~Base() = default;
};
struct D1 : Base { long long f(long long x) const override { return x * 3 + 1; } };
struct D2 : Base { long long f(long long x) const override { return x * 5 + 7; } };

// ---- CRTP ----
template <class T> struct CB {
    long long f(long long x) const { return static_cast<const T*>(this)->impl(x); }
};
struct C1 : CB<C1> { long long impl(long long x) const { return x * 3 + 1; } };
struct C2 : CB<C2> { long long impl(long long x) const { return x * 5 + 7; } };

// ---- 直接调用 ----
static inline long long direct1(long long x) { return x * 3 + 1; }

int main() {
    std::mt19937 rng(42);
    const int N = 1'000'000, ROUNDS = 16;

    // 多态数组：两类对象各半、随机排列（分支预测器无法稳定预测 vptr 目标）
    std::vector<std::unique_ptr<Base>> objs;
    objs.reserve(N);
    for (int i = 0; i < N; ++i) {
        g_select = (int)(rng() & 1);
        if (g_select) objs.push_back(std::make_unique<D1>());
        else objs.push_back(std::make_unique<D2>());
    }

    // 同序型多态数组（全 D1）：vptr 目标恒定，间接跳转可被预测
    std::vector<std::unique_ptr<Base>> mono;
    mono.reserve(N);
    for (int i = 0; i < N; ++i) mono.push_back(std::make_unique<D1>());

    // CRTP 数组（编译期定型，无 vptr）
    std::vector<C1> crtp(N);

    // 关键：s 进入调用参数形成数据依赖链（s = f(s)），阻止闭式求值/向量化；
    // 四组同构，比较的是"调用分发机制"往依赖链上加的延迟。
    double t_virt_mix = median5([&] {
        auto a = Clock::now();
        long long s = 1;
        for (int r = 0; r < ROUNDS; ++r)
            for (auto& p : objs) s = p->f(s) & 0xFFFF;
        g_sink = s;
        return ms(a, Clock::now());
    });
    double t_virt_mono = median5([&] {
        auto a = Clock::now();
        long long s = 1;
        for (int r = 0; r < ROUNDS; ++r)
            for (auto& p : mono) s = p->f(s) & 0xFFFF;
        g_sink = s;
        return ms(a, Clock::now());
    });
    double t_crtp = median5([&] {
        auto a = Clock::now();
        long long s = 1;
        for (int r = 0; r < ROUNDS; ++r)
            for (auto& c : crtp) s = c.f(s) & 0xFFFF;
        g_sink = s;
        return ms(a, Clock::now());
    });
    double t_direct = median5([&] {
        auto a = Clock::now();
        long long s = 1;
        for (int r = 0; r < ROUNDS; ++r)
            for (int i = 0; i < N; ++i) s = direct1(s) & 0xFFFF;
        g_sink = s;
        return ms(a, Clock::now());
    });

    std::printf("call_16M,direct_inline,%.3f\n", t_direct);
    std::printf("call_16M,crtp,%.3f,ratio_vs_direct=%.2f\n", t_crtp, t_crtp / t_direct);
    std::printf("call_16M,virtual_mono,%.3f,ratio_vs_crtp=%.2f\n", t_virt_mono, t_virt_mono / t_crtp);
    std::printf("call_16M,virtual_mixed,%.3f,ratio_vs_mono=%.2f,ratio_vs_crtp=%.2f\n",
                t_virt_mix, t_virt_mix / t_virt_mono, t_virt_mix / t_crtp);

    // 附：对象尺寸证据（vptr 存在性）
    std::printf("sizeof,D1=%zu,C1=%zu\n", sizeof(D1), sizeof(C1));
    return 0;
}

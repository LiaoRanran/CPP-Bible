// _bench_template.cpp —— ch60 模板零开销实证 (GCC 15.3.0 -O2)
// 三个子基准：① 模板 vs 手写(零开销) ② 类型擦除代价(SBO 内 vs 越界堆分配) ③ NTTP 编译期展开
#include <vector>
#include <any>
#include <chrono>
#include <numeric>
#include <iostream>
#include <algorithm>
#include <cstddef>

using namespace std;
using namespace std::chrono;

static volatile double g_sink = 0;  // 防优化：强制消费结果

static long long now_us() {
    return duration_cast<microseconds>(steady_clock::now().time_since_epoch()).count();
}

template <class F>
double median_of(F f, int rounds = 5) {
    vector<double> ts;
    for (int i = 0; i < rounds; i++) {
        auto a = now_us();
        double r = f();
        auto b = now_us();
        g_sink += r;
        ts.push_back((double)(b - a));
    }
    sort(ts.begin(), ts.end());
    return ts[ts.size() / 2];
}

// 32 字节结构：超过 std::any 16 字节 SBO → 强制堆分配
struct Big { double a, b, c, d; };

// ---------- 测试1：零开销（模板 lambda vs 手写） ----------
template <typename F>
double run_template(F f, const vector<double>& v) {
    double s = 0;
    for (double x : v) s += f(x);
    return s;
}
double hand_written(const vector<double>& v) {
    double s = 0;
    for (double x : v) s += x * 2.0;
    return s;
}

// ---------- 测试2：类型擦除代价（SBO 内 double vs 越界堆 Big） ----------
double any_double(const vector<any>& v) {        // double(8B) 落在 SBO 内
    double s = 0;
    for (const auto& a : v) s += any_cast<double>(a);
    return s;
}
double direct_double(const vector<double>& v) {
    double s = 0;
    for (double x : v) s += x;
    return s;
}
double any_big(const vector<any>& v) {           // Big(32B) 越过 SBO → 堆分配
    double s = 0;
    for (const auto& a : v) s += any_cast<Big>(a).a;
    return s;
}
double direct_big(const vector<Big>& v) {
    double s = 0;
    for (const auto& x : v) s += x.a;
    return s;
}

// ---------- 测试3：NTTP 编译期展开 vs 运行期循环 ----------
template <size_t N>
double nttp_loop(const double* p) {
    double s = 0;
    for (size_t i = 0; i < N; ++i) s += p[i] * 2.0;
    return s;
}
__attribute__((noinline))
double runtime_loop(const double* p, size_t n) {
    double s = 0;
    for (size_t i = 0; i < n; ++i) s += p[i] * 2.0;
    return s;
}

int main() {
    const size_t N = 1'000'000;
    vector<double> v(N);
    for (size_t i = 0; i < N; i++) v[i] = (double)(i % 1000) * 0.5;
    vector<any> va_d(N);  for (size_t i = 0; i < N; i++) va_d[i] = v[i];
    vector<Big> vb(N);    for (size_t i = 0; i < N; i++) vb[i] = {v[i], 0, 0, 0};
    vector<any> va_b(N);  for (size_t i = 0; i < N; i++) va_b[i] = vb[i];

    auto t_tmpl = median_of([&]{ return run_template([](double x){ return x * 2.0; }, v); });
    auto t_hand = median_of([&]{ return hand_written(v); });

    auto t_anyd = median_of([&]{ return any_double(va_d); });
    auto t_dird = median_of([&]{ return direct_double(v); });

    auto t_anyb = median_of([&]{ return any_big(va_b); });
    auto t_dirb = median_of([&]{ return direct_big(vb); });

    auto t_nttp = median_of([&]{ return nttp_loop<4096>(v.data()); });
    auto t_rt   = median_of([&]{ return runtime_loop(v.data(), 4096); });

    cout.precision(3); cout << fixed;
    cout << "=== ch60 模板零开销实证 (GCC 15.3.0 -O2, N=" << N << ") ===\n";
    cout << "T1 零开销      : template=" << t_tmpl << "us hand=" << t_hand
         << "us ratio=" << (t_tmpl / t_hand) << "x\n";
    cout << "T2a SBO内(double): any=" << t_anyd << "us direct=" << t_dird
         << "us ratio=" << (t_anyd / t_dird) << "x\n";
    cout << "T2b 越界堆(Big)  : any=" << t_anyb << "us direct=" << t_dirb
         << "us ratio=" << (t_anyb / t_dirb) << "x\n";
    cout << "T3 NTTP展开    : nttp=" << t_nttp << "us runtime=" << t_rt
         << "us ratio=" << (t_rt / t_nttp) << "x\n";
    return 0;
}

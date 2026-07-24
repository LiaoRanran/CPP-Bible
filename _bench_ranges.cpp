// ch90 ranges 同规格 D5 基准：惰性管道 vs 手写融合循环 vs 贪婪物化
// 编译: g++ -std=c++20 -O2 -pthread _bench_ranges.cpp -o _bench_ranges.exe
// 仅本机实跑取数，不进 Book/ 编译门禁（库根临时文件）。
#include <vector>
#include <ranges>
#include <numeric>
#include <chrono>
#include <iostream>
#include <algorithm>
#include <cstdint>

using namespace std;

static long long now_us() {
    return chrono::duration_cast<chrono::microseconds>(
        chrono::steady_clock::now().time_since_epoch()).count();
}

// 策略 A：惰性 ranges 管道（filter+transform 融合为单遍扫描）
unsigned long long bench_lazy(const vector<int>& v) {
    auto r = v
           | views::filter([](int x) { return (x & 1) == 0; })
           | views::transform([](int x) { return (unsigned long long)(x & 0x3FF) * (x & 0x3FF); });
    return accumulate(r.begin(), r.end(), 0ULL);
}

// 策略 B：手写融合单循环（上界参考，单遍）
unsigned long long bench_hand(const vector<int>& v) {
    unsigned long long s = 0;
    for (int x : v)
        if ((x & 1) == 0)
            s += (unsigned long long)(x & 0x3FF) * (x & 0x3FF);
    return s;
}

// 策略 C：贪婪物化（filter 拷贝 -> transform 拷贝 -> 累加，三遍 + 两次分配）
unsigned long long bench_eager(const vector<int>& v) {
    vector<int> f;
    for (int x : v)
        if ((x & 1) == 0) f.push_back(x);
    vector<unsigned long long> t;
    t.reserve(f.size());
    for (int x : f) t.push_back((unsigned long long)(x & 0x3FF) * (x & 0x3FF));
    unsigned long long s = 0;
    for (unsigned long long x : t) s += x;
    return s;
}

template <class F>
double median_of(F f, int rounds = 5) {
    vector<double> ts;
    volatile unsigned long long sink = 0; // 防优化：强制消费结果
    for (int i = 0; i < rounds; i++) {
        auto a = now_us();
        unsigned long long r = f();
        auto b = now_us();
        sink += r;
        ts.push_back((double)(b - a) / 1000.0); // 转 ms
    }
    sort(ts.begin(), ts.end());
    return ts[ts.size() / 2];
}

int main() {
    const int N = 10'000'000; // 1e7 整数，偶数约占一半
    vector<int> v(N);
    for (int i = 0; i < N; i++) v[i] = i;

    // 正确性自检：三策略结果必须一致
    unsigned long long ra = bench_lazy(v), rb = bench_hand(v), rc = bench_eager(v);
    if (!(ra == rb && rb == rc)) {
        cerr << "MISMATCH ra=" << ra << " rb=" << rb << " rc=" << rc << "\n";
        return 1;
    }
    cout << "N=" << N << " expected_sum=" << ra << "\n";

    double tl = median_of([&] { return bench_lazy(v); });
    double th = median_of([&] { return bench_hand(v); });
    double te = median_of([&] { return bench_eager(v); });

    cout << "lazy  (ranges pipe) : " << tl << " ms\n";
    cout << "hand  (fused loop)  : " << th << " ms\n";
    cout << "eager (materialize) : " << te << " ms\n";
    cout << "lazy/hand  = " << (tl / th) << "x\n";
    cout << "eager/hand = " << (te / th) << "x\n";
    return 0;
}

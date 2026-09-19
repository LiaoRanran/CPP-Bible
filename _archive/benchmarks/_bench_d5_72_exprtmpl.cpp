// _bench_d5_72_exprtmpl.cpp — ch72 表达式模板：消灭临时对象与多趟遍历
// g++ -O2 -std=c++23
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <vector>
#include <algorithm>
#include <random>

static double now_ms() {
    using namespace std::chrono;
    return duration<double, std::milli>(steady_clock::now().time_since_epoch()).count();
}
template <class F>
static double bench(const char* name, F&& f) {
    std::vector<double> t;
    for (int r = 0; r < 5; ++r) { double t0 = now_ms(); f(); t.push_back(now_ms() - t0); }
    std::sort(t.begin(), t.end());
    std::printf("%-40s %10.3f ms\n", name, t[2]);
    return t[2];
}
volatile double g_dsink;

constexpr std::size_t N = 2'000'000;
constexpr int REPS = 50;

// ---------- 朴素实现：operator+ 返回新 Vec（分配 + 多趟遍历） ----------
struct NaiveVec {
    std::vector<double> d;
    explicit NaiveVec(std::size_t n = 0) : d(n) {}
};
NaiveVec operator+(const NaiveVec& a, const NaiveVec& b) {
    NaiveVec r(a.d.size());
    for (std::size_t i = 0; i < a.d.size(); ++i) r.d[i] = a.d[i] + b.d[i];
    return r;
}

// ---------- 表达式模板：惰性节点，赋值时单循环融合 ----------
template <class L, class R>
struct AddExpr {
    const L& l; const R& r;
    double operator[](std::size_t i) const { return l[i] + r[i]; }
    std::size_t size() const { return l.size(); }
};
struct EtVec {
    std::vector<double> d;
    explicit EtVec(std::size_t n = 0) : d(n) {}
    double operator[](std::size_t i) const { return d[i]; }
    std::size_t size() const { return d.size(); }
    template <class E>
    EtVec& operator=(const E& e) {
        for (std::size_t i = 0; i < d.size(); ++i) d[i] = e[i];
        return *this;
    }
};
template <class L, class R> AddExpr<L, R> operator+(const L& l, const R& r) { return {l, r}; }

int main() {
    std::mt19937_64 rng(42);
    std::uniform_real_distribution<double> dist(0.0, 1.0);

    NaiveVec na(N), nb(N), nc(N), nd(N), nr(N);
    EtVec    ea(N), eb(N), ec(N), ed(N), er(N);
    std::vector<double> ma(N), mb(N), mc(N), md(N), mr(N);
    for (std::size_t i = 0; i < N; ++i) {
        double x = dist(rng), y = dist(rng), z = dist(rng), w = dist(rng);
        na.d[i] = ea.d[i] = ma[i] = x;
        nb.d[i] = eb.d[i] = mb[i] = y;
        nc.d[i] = ec.d[i] = mc[i] = z;
        nd.d[i] = ed.d[i] = md[i] = w;
    }

    bench("naive: r = a+b+c+d (3 temps)", [&] {
        for (int r = 0; r < REPS; ++r) nr = na + nb + nc + nd;
        g_dsink = nr.d[N / 2];
    });
    bench("ET:    r = a+b+c+d (fused)", [&] {
        for (int r = 0; r < REPS; ++r) er = ea + eb + ec + ed;
        g_dsink = er.d[N / 2];
    });
    bench("manual fused loop", [&] {
        for (int r = 0; r < REPS; ++r)
            for (std::size_t i = 0; i < N; ++i)
                mr[i] = ma[i] + mb[i] + mc[i] + md[i];
        g_dsink = mr[N / 2];
    });

    std::printf("checksums: %.6f %.6f %.6f (must equal)\n",
                nr.d[N / 2], er.d[N / 2], mr[N / 2]);
    return 0;
}

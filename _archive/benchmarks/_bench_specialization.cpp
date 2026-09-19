// _bench_specialization.cpp —— ch62 模板特化真实基准 (GCC 15.3.0 -O2)
// 两个子基准：① 序列化 通用 ostringstream 路径 vs int 特化快路径
//            ② 类型分发 std::variant visit(编译期可选项) vs std::any(运行期 RTTI)
#include <vector>
#include <string>
#include <sstream>
#include <variant>
#include <any>
#include <chrono>
#include <iostream>
#include <algorithm>
#include <cstddef>

using namespace std;
using namespace std::chrono;

static volatile size_t g_sink = 0;  // 防优化

static long long now_us() {
    return duration_cast<microseconds>(steady_clock::now().time_since_epoch()).count();
}
template <class F>
double median_of(F f, int rounds = 5) {
    vector<double> ts;
    for (int i = 0; i < rounds; i++) {
        auto a = now_us(); double r = f(); auto b = now_us();
        g_sink += (size_t)r;
        ts.push_back((double)(b - a));
    }
    sort(ts.begin(), ts.end());
    return ts[ts.size() / 2];
}

// ---------- 测试1：序列化 通用 vs 特化 ----------
template <typename T>
string to_string_generic(T v) {            // 主模板：通用慢路径
    ostringstream os; os << v; return os.str();
}
template <>
string to_string_generic<int>(int v) {     // int 全特化：快路径
    return to_string(v);
}
// 强制走通用路径（无特化）的对照
template <typename T>
string to_string_nospec(T v) {             // 永远走 ostringstream
    ostringstream os; os << v; return os.str();
}

// ---------- 测试2：类型分发 variant vs any ----------
using V = variant<int, double, string>;
using A = any;
enum class Tag { Int, Double, Str };

double visit_variant(const vector<V>& vs) {   // 编译期可选项列表 → visit 生成分发
    double s = 0;
    for (const auto& v : vs)
        s += visit([](auto&& x) -> double {
            using X = decay_t<decltype(x)>;
            if constexpr (is_same_v<X, int>)    return (double)x * 1.0;
            else if constexpr (is_same_v<X, double>) return x * 2.0;
            else return (double)x.size() * 3.0;
        }, v);
    return s;
}
double visit_any(const vector<A>& as) {       // 运行期 RTTI：每次 any_cast 校验
    double s = 0;
    for (const auto& a : as) {
        if (auto p = any_cast<int>(&a))        s += (double)*p * 1.0;
        else if (auto p = any_cast<double>(&a)) s += *p * 2.0;
        else if (auto p = any_cast<string>(&a)) s += (double)p->size() * 3.0;
    }
    return s;
}

int main() {
    const size_t N = 500'000;

    // 测试1 数据
    vector<int> vi(N);
    for (size_t i = 0; i < N; i++) vi[i] = (int)(i % 1000);

    // 测试2 数据
    vector<V> vv(N); vector<A> va(N);
    for (size_t i = 0; i < N; i++) {
        int m = (int)(i % 3);
        if (m == 0) { vv[i] = (int)(i % 1000);        va[i] = (int)(i % 1000); }
        else if (m == 1) { vv[i] = (double)(i % 1000); va[i] = (double)(i % 1000); }
        else { vv[i] = string(10, 'x'); va[i] = string(10, 'x'); }
    }

    auto t_spec = median_of([&]{ double s=0; for(int x:vi) s+=to_string_generic(x).size(); return s; });
    auto t_gen  = median_of([&]{ double s=0; for(int x:vi) s+=to_string_nospec(x).size(); return s; });

    auto t_var  = median_of([&]{ return visit_variant(vv); });
    auto t_any  = median_of([&]{ return visit_any(va); });

    cout.precision(3); cout << fixed;
    cout << "=== ch62 模板特化真实基准 (GCC 15.3.0 -O2, N=" << N << ") ===\n";
    cout << "T1 序列化  : 特化快路径=" << t_spec << "us  通用ostringstream=" << t_gen
         << "us  ratio=" << (t_gen / t_spec) << "x\n";
    cout << "T2 类型分发: variant visit=" << t_var << "us  any RTTI=" << t_any
         << "us  ratio=" << (t_any / t_var) << "x\n";
    return 0;
}

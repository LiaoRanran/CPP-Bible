// _bench_d5_49_vinherit.cpp — ch49 虚继承：虚基类偏移查表的真实代价
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
volatile std::uint64_t g_sink;

// 虚继承菱形
struct VB { int x = 0; virtual ~VB() = default; };
struct VD1 : virtual VB { int d1 = 0; };
struct VD2 : virtual VB { int d2 = 0; };
struct VM : VD1, VD2 { int m = 0; };

// 非虚继承对照（同样带 vptr，隔离"虚基类偏移查表"变量）
struct NB { int x = 0; virtual ~NB() = default; };
struct ND1 : NB { int d1 = 0; };
struct NM : ND1 { int m = 0; };

int main() {
    std::printf("sizeof: VB=%zu VD1=%zu VM=%zu | NB=%zu ND1=%zu NM=%zu\n",
                sizeof(VB), sizeof(VD1), sizeof(VM),
                sizeof(NB), sizeof(ND1), sizeof(NM));

    constexpr std::size_t N = 1'000'000;
    constexpr int REPS = 100;

    // 堆上构造 + 洗牌指针，强制真实指针追逐（每次访问都需读 vptr/偏移）
    std::vector<VM*> vptrs(N);
    std::vector<NM*> nptrs(N);
    for (std::size_t i = 0; i < N; ++i) {
        vptrs[i] = new VM; vptrs[i]->x = int(i & 1023);
        nptrs[i] = new NM; nptrs[i]->x = int(i & 1023);
    }
    std::mt19937_64 rng(42);
    std::shuffle(vptrs.begin(), vptrs.end(), rng);
    std::shuffle(nptrs.begin(), nptrs.end(), rng);

    std::vector<VD1*> vd1(vptrs.begin(), vptrs.end()); // 上转到中间基类
    std::vector<ND1*> nd1(nptrs.begin(), nptrs.end());

    // 1) 经虚基类访问：VD1* → VB*（运行期读 vtable 中 vbase offset）
    bench("access x via virtual base (VD1*)", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPS; ++r)
            for (auto p : vd1) s += static_cast<VB*>(p)->x;
        g_sink = s;
    });
    // 2) 非虚继承访问：ND1* → NB*（编译期常量偏移）
    bench("access x via normal base (ND1*)", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPS; ++r)
            for (auto p : nd1) s += static_cast<NB*>(p)->x;
        g_sink = s;
    });
    // 3) 完整类型直接访问（无任何转换）
    bench("access x via exact type (VM*)", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPS; ++r)
            for (auto p : vptrs) s += p->x;
        g_sink = s;
    });

    for (auto p : vptrs) delete p;
    for (auto p : nptrs) delete p;
    std::printf("sink=%llu\n", (unsigned long long)g_sink);
    return 0;
}

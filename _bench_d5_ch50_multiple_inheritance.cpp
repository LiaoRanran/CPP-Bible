// _bench_d5_ch50_multiple_inheritance.cpp — ch50 多重继承：thunk 与虚基类的真实开销
// g++ -O2 -std=c++23 _bench_d5_ch50_multiple_inheritance.cpp -o bench50
//
// 方法学：每个子基准跑 5 轮取中位；volatile sink 防 DCE；
// 对象指针数组事先随机洗牌（多态类型混杂），使虚调用无法被去虚拟化/内联。
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <memory>
#include <random>
#include <vector>

static double now_ms() {
    using namespace std::chrono;
    return duration<double, std::milli>(steady_clock::now().time_since_epoch()).count();
}

template <class F>
static double bench(const char* name, F&& f) {
    std::vector<double> t;
    for (int r = 0; r < 5; ++r) {
        double t0 = now_ms();
        f();
        t.push_back(now_ms() - t0);
    }
    std::vector<double> raw = t;
    std::sort(t.begin(), t.end());
    std::printf("%-48s median %9.3f ms   raw:", name, t[2]);
    for (double v : raw) std::printf(" %.3f", v);
    std::printf("\n");
    return t[2];
}

volatile std::uint64_t g_sink;

// ---------- 1) 单继承：只有一个基类子对象，this 无需调整 ----------
struct SBase {
    long long a = 1;
    virtual ~SBase() = default;
    virtual long long f() const = 0;
};
struct SDerivedA : SBase {
    long long f() const override { return a + 1; }
};
struct SDerivedB : SBase {
    long long f() const override { return a + 2; }
};

// ---------- 2) 多重继承：第二基类指针需 thunk 调整 this ----------
struct L {
    long long x = 1;
    virtual ~L() = default;
    virtual long long f() const = 0;
};
struct R {
    long long y = 2;
    virtual ~R() = default;
    virtual long long g() const = 0;
};
struct MDerivedA : L, R {
    long long f() const override { return x + 1; }
    long long g() const override { return y + 1; }
};
struct MDerivedB : L, R {
    long long f() const override { return x + 2; }
    long long g() const override { return y + 2; }
};

// ---------- 3) 虚继承：菱形，访问虚基类成员需经 vbase offset 间接寻址 ----------
struct VB {
    long long z = 3;
    virtual ~VB() = default;
    virtual long long h() const = 0;
};
struct VL : virtual VB { };
struct VR : virtual VB { };
struct VDerivedA : VL, VR {
    long long h() const override { return z + 1; }
};
struct VDerivedB : VL, VR {
    long long h() const override { return z + 2; }
};

// 非虚多重继承对照组：同样两层两基类，但无 virtual 关键字
struct NB {
    long long z = 3;
    virtual ~NB() = default;
    virtual long long h() const = 0;
};
struct NL : NB { };
struct NDerivedA : NL {
    long long h() const override { return z + 1; }
};
struct NDerivedB : NL {
    long long h() const override { return z + 2; }
};

int main() {
    constexpr int OBJ = 20'000;     // 对象个数
    constexpr int REP = 4'000;      // 遍历轮数（总虚调用 = 80M，压低相对抖动）

    std::mt19937 rng(12345);       // 固定种子保证洗牌可复现
    std::uniform_int_distribution<int> coin(0, 1);

    std::printf("== ch50 multiple inheritance benchmark, OBJ=%d REP=%d ==\n", OBJ, REP);

    // ===== 组 1：单继承虚调用 =====
    std::vector<std::unique_ptr<SBase>> sown;
    std::vector<SBase*> sp;
    sown.reserve(OBJ);
    sp.reserve(OBJ);
    for (int i = 0; i < OBJ; ++i) {
        if (coin(rng)) sown.push_back(std::make_unique<SDerivedA>());
        else           sown.push_back(std::make_unique<SDerivedB>());
        sp.push_back(sown.back().get());
    }
    std::shuffle(sp.begin(), sp.end(), rng);

    double t_single = bench("1 single-inherit virtual call via Base*", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REP; ++r)
            for (SBase* p : sp) s += static_cast<std::uint64_t>(p->f());
        g_sink = s;
    });

    // ===== 组 2：多重继承，同一批对象分别经第一 / 第二基类指针遍历 =====
    std::vector<std::unique_ptr<L>> mown;   // 以 L* 持有所有权
    std::vector<L*> mp1;
    std::vector<R*> mp2;
    mown.reserve(OBJ);
    mp1.reserve(OBJ);
    mp2.reserve(OBJ);
    std::vector<int> order(OBJ);
    for (int i = 0; i < OBJ; ++i) order[i] = i;
    std::shuffle(order.begin(), order.end(), rng);

    std::vector<L*> tmp1(OBJ);
    std::vector<R*> tmp2(OBJ);
    for (int i = 0; i < OBJ; ++i) {
        if (coin(rng)) {
            auto* o = new MDerivedA;
            mown.emplace_back(static_cast<L*>(o));
            tmp1[i] = static_cast<L*>(o);
            tmp2[i] = static_cast<R*>(o);
        } else {
            auto* o = new MDerivedB;
            mown.emplace_back(static_cast<L*>(o));
            tmp1[i] = static_cast<L*>(o);
            tmp2[i] = static_cast<R*>(o);
        }
    }
    // 两个数组使用同一随机顺序，保证访存序列完全一致，只差 this 调整
    for (int i = 0; i < OBJ; ++i) {
        mp1.push_back(tmp1[order[i]]);
        mp2.push_back(tmp2[order[i]]);
    }

    double t_first = bench("2 multi-inherit via FIRST base L* (no thunk)", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REP; ++r)
            for (L* p : mp1) s += static_cast<std::uint64_t>(p->f());
        g_sink = s;
    });

    double t_second = bench("3 multi-inherit via SECOND base R* (thunk)", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REP; ++r)
            for (R* p : mp2) s += static_cast<std::uint64_t>(p->g());
        g_sink = s;
    });

    // ===== 组 3：虚继承 vs 非虚继承，虚基类成员访问 =====
    std::vector<std::unique_ptr<VB>> vown;
    std::vector<VB*> vp;
    vown.reserve(OBJ);
    vp.reserve(OBJ);
    for (int i = 0; i < OBJ; ++i) {
        if (coin(rng)) vown.push_back(std::make_unique<VDerivedA>());
        else           vown.push_back(std::make_unique<VDerivedB>());
        vp.push_back(vown.back().get());
    }
    std::shuffle(vp.begin(), vp.end(), rng);

    std::vector<std::unique_ptr<NB>> nown;
    std::vector<NB*> np;
    nown.reserve(OBJ);
    np.reserve(OBJ);
    for (int i = 0; i < OBJ; ++i) {
        if (coin(rng)) nown.push_back(std::make_unique<NDerivedA>());
        else           nown.push_back(std::make_unique<NDerivedB>());
        np.push_back(nown.back().get());
    }
    std::shuffle(np.begin(), np.end(), rng);

    double t_nonvirt = bench("4 non-virtual inherit: base member + vcall", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REP; ++r)
            for (NB* p : np) s += static_cast<std::uint64_t>(p->h() + p->z);
        g_sink = s;
    });

    double t_virt = bench("5 VIRTUAL inherit: vbase member + vcall", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REP; ++r)
            for (VB* p : vp) s += static_cast<std::uint64_t>(p->h() + p->z);
        g_sink = s;
    });

    std::printf("\n-- sizes --\n");
    std::printf("sizeof(SDerivedA) single-inherit  = %zu\n", sizeof(SDerivedA));
    std::printf("sizeof(MDerivedA) multi-inherit   = %zu\n", sizeof(MDerivedA));
    std::printf("sizeof(NDerivedA) non-virt chain  = %zu\n", sizeof(NDerivedA));
    std::printf("sizeof(VDerivedA) virtual-inherit = %zu\n", sizeof(VDerivedA));

    std::printf("\n-- ratios --\n");
    std::printf("first-base L*  %.3f / single %.3f => %.2fx\n", t_first, t_single, t_first / t_single);
    std::printf("second-base R* %.3f / first  %.3f => %.2fx\n", t_second, t_first, t_second / t_first);
    std::printf("virtual-inh    %.3f / non-virt %.3f => %.2fx\n", t_virt, t_nonvirt, t_virt / t_nonvirt);
    return 0;
}

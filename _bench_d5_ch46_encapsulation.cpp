// _bench_d5_ch46_encapsulation.cpp
// ch46 封装与继承 — 真实基准（附录 D5 基准源码）
// 编译: C:/Qt/Tools/mingw1530_64/bin/g++.EXE -O2 -std=c++23 _bench_d5_ch46_encapsulation.cpp -o bench_ch46.exe
// 维度:
//   1) public 直接成员访问 vs private + getter/setter (零成本抽象验证)
//   2) 同一批多态对象上: 非虚 getter vs 虚 getter (打乱数组, 防去虚化/防间接分支预测)
//   3) 5 层深继承链的非虚成员访问 vs 扁平结构 (零成本验证)
// 方法学: 每子基准 5 轮取中位; volatile sink 逃逸结果防 DCE;
//         数据全部来自运行期 mt19937, 防止闭式折叠;
//         维度 1/3 的数据集刻意压到 L2/L3 常驻, 避免被 DRAM 带宽掩盖抽象开销。
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <memory>
#include <random>
#include <vector>

using Clock = std::chrono::steady_clock;

static volatile std::uint64_t g_sink = 0; // 逃逸结果, 防 DCE

template <typename F>
double run_median_ms(const char* name, F&& f) {
    double times[5];
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        std::uint64_t result = f();
        auto t1 = Clock::now();
        g_sink = g_sink + result;
        times[r] = std::chrono::duration<double, std::milli>(t1 - t0).count();
    }
    std::cout << name << ": [";
    for (int r = 0; r < 5; ++r) std::cout << times[r] << (r < 4 ? " " : "");
    std::cout << "] ";
    std::sort(times, times + 5);
    std::cout << "median=" << times[2] << " ms" << std::endl;
    return times[2];
}

// ---------- 维度 1: public 成员 vs getter/setter ----------
struct PlainPoint {
    std::uint32_t x, y;
};

class EncapPoint {
public:
    std::uint32_t x() const { return x_; }
    std::uint32_t y() const { return y_; }
    void set_x(std::uint32_t v) { x_ = v; }
    void set_y(std::uint32_t v) { y_ = v; }
private:
    std::uint32_t x_ = 0, y_ = 0;
};

// ---------- 维度 2: 非虚 vs 虚 getter (同一批对象, 唯一变量是分派方式) ----------
struct ShapeBase {
    std::uint32_t v;
    explicit ShapeBase(std::uint32_t x) : v(x) {}
    virtual ~ShapeBase() = default;
    virtual std::uint32_t get() const = 0;
    std::uint32_t get_nonvirtual() const { return v; }   // 静态绑定, 可内联
};
// 三个派生体给出彼此不同的实现体, 避免 -fipa-icf 把它们折叠成同一份代码
struct Circle final : ShapeBase {
    using ShapeBase::ShapeBase;
    std::uint32_t get() const override { return v + 1; }
};
struct Square final : ShapeBase {
    using ShapeBase::ShapeBase;
    std::uint32_t get() const override { return v + 2; }
};
struct Triangle final : ShapeBase {
    using ShapeBase::ShapeBase;
    std::uint32_t get() const override { return v + 3; }
};

// ---------- 维度 3: 5 层继承链 vs 扁平 ----------
struct L1 { std::uint32_t a = 0; };
struct L2 : L1 { std::uint32_t b = 0; };
struct L3 : L2 { std::uint32_t c = 0; };
struct L4 : L3 { std::uint32_t d = 0; };
struct L5 : L4 {
    std::uint32_t e = 0;
    std::uint32_t sum() const { return a + b + c + d + e; }
};
struct Flat5 {
    std::uint32_t a = 0, b = 0, c = 0, d = 0, e = 0;
    std::uint32_t sum() const { return a + b + c + d + e; }
};

int main() {
    std::mt19937 rng(12345);

    // ============ 维度 1: 256K 元素 x 8B = 2MB (L2/L3 常驻), 重复 400 轮 ============
    constexpr std::size_t N1 = 256u * 1024u;
    constexpr int REP1 = 400;
    std::cout << "=== ch46 bench (dim1: N=" << N1 << " REP=" << REP1
              << ", 2MB working set) ===" << std::endl;

    std::vector<PlainPoint> plain(N1);
    std::vector<EncapPoint> encap(N1);
    for (std::size_t i = 0; i < N1; ++i) {
        std::uint32_t x = rng(), y = rng();
        plain[i].x = x;
        plain[i].y = y;
        encap[i].set_x(x);
        encap[i].set_y(y);
    }

    double t_public = run_median_ms("1a public member direct", [&] {
        std::uint64_t s = 0;
        for (int rep = 0; rep < REP1; ++rep)
            for (std::size_t i = 0; i < N1; ++i)
                s += plain[i].x ^ plain[i].y;
        return s;
    });
    double t_getter = run_median_ms("1b private + getter    ", [&] {
        std::uint64_t s = 0;
        for (int rep = 0; rep < REP1; ++rep)
            for (std::size_t i = 0; i < N1; ++i)
                s += encap[i].x() ^ encap[i].y();
        return s;
    });

    // ============ 维度 2: 4M 个多态对象, 类型混排 + 指针混排 ============
    constexpr std::size_t N2 = 4'000'000;
    constexpr int REP2 = 20;
    std::cout << "=== ch46 bench (dim2: N=" << N2 << " REP=" << REP2
              << ", polymorphic, shuffled) ===" << std::endl;

    std::vector<std::unique_ptr<ShapeBase>> shapes;
    shapes.reserve(N2);
    for (std::size_t i = 0; i < N2; ++i) {
        std::uint32_t x = rng();
        switch (x % 3) {
            case 0: shapes.push_back(std::make_unique<Circle>(x)); break;
            case 1: shapes.push_back(std::make_unique<Square>(x)); break;
            default: shapes.push_back(std::make_unique<Triangle>(x)); break;
        }
    }
    std::shuffle(shapes.begin(), shapes.end(), rng);

    // 2a/2b 走同一个指针数组、同一批对象、同一访问序列 —— 唯一差异是分派方式
    double t_nonvirt = run_median_ms("2a non-virtual getter  ", [&] {
        std::uint64_t s = 0;
        for (int rep = 0; rep < REP2; ++rep)
            for (std::size_t i = 0; i < N2; ++i)
                s += shapes[i]->get_nonvirtual();
        return s;
    });
    double t_virt = run_median_ms("2b virtual getter      ", [&] {
        std::uint64_t s = 0;
        for (int rep = 0; rep < REP2; ++rep)
            for (std::size_t i = 0; i < N2; ++i)
                s += shapes[i]->get();
        return s;
    });

    // ---- 维度 2 的"缓存热"对照组: 只取前 128K 个对象反复扫, 工作集 ~2MB ----
    // 目的: 把"指针追逐造成的访存并行度损失"与"间接调用本身的开销"分开
    constexpr std::size_t N2H = 128u * 1024u;
    constexpr int REP2H = 300;
    std::cout << "=== ch46 bench (dim2-hot: N=" << N2H << " REP=" << REP2H
              << ", cache-resident) ===" << std::endl;

    double t_nonvirt_hot = run_median_ms("2c non-virtual getter (hot)", [&] {
        std::uint64_t s = 0;
        for (int rep = 0; rep < REP2H; ++rep)
            for (std::size_t i = 0; i < N2H; ++i)
                s += shapes[i]->get_nonvirtual();
        return s;
    });
    double t_virt_hot = run_median_ms("2d virtual getter     (hot)", [&] {
        std::uint64_t s = 0;
        for (int rep = 0; rep < REP2H; ++rep)
            for (std::size_t i = 0; i < N2H; ++i)
                s += shapes[i]->get();
        return s;
    });

    // 释放 4M 个多态对象, 避免堆压力干扰后续维度的测量
    shapes.clear();
    shapes.shrink_to_fit();

    // ============ 维度 3: 128K 元素 x 20B = 2.5MB, 重复 400 轮 ============
    constexpr std::size_t N3 = 128u * 1024u;
    constexpr int REP3 = 400;
    std::cout << "=== ch46 bench (dim3: N=" << N3 << " REP=" << REP3
              << ", sizeof(L5)=" << sizeof(L5) << " sizeof(Flat5)=" << sizeof(Flat5)
              << ") ===" << std::endl;

    std::vector<L5> deep(N3);
    std::vector<Flat5> flat(N3);
    for (std::size_t i = 0; i < N3; ++i) {
        std::uint32_t x = rng();
        deep[i].a = flat[i].a = x;
        deep[i].b = flat[i].b = x >> 1;
        deep[i].c = flat[i].c = x >> 2;
        deep[i].d = flat[i].d = x >> 3;
        deep[i].e = flat[i].e = x >> 4;
    }

    double t_deep = run_median_ms("3a 5-level inheritance ", [&] {
        std::uint64_t s = 0;
        for (int rep = 0; rep < REP3; ++rep)
            for (std::size_t i = 0; i < N3; ++i)
                s += deep[i].sum();
        return s;
    });
    double t_flat = run_median_ms("3b flat struct         ", [&] {
        std::uint64_t s = 0;
        for (int rep = 0; rep < REP3; ++rep)
            for (std::size_t i = 0; i < N3; ++i)
                s += flat[i].sum();
        return s;
    });

    std::cout << "--- summary (medians, ms) ---" << std::endl;
    std::cout << "public=" << t_public << " getter=" << t_getter << std::endl;
    std::cout << "nonvirt=" << t_nonvirt << " virt=" << t_virt << std::endl;
    std::cout << "nonvirt_hot=" << t_nonvirt_hot << " virt_hot=" << t_virt_hot << std::endl;
    std::cout << "deep=" << t_deep << " flat=" << t_flat << std::endl;
    std::cout << "sink=" << g_sink << std::endl;
    return 0;
}

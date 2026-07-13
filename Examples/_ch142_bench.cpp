// 文件：Examples/_ch142_bench.cpp
// 行号：7
// 编译并运行：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 Examples/_ch142_bench.cpp -o Examples/_ch142_bench.exe && Examples/_ch142_bench.exe
// 真实微基准（见 ⑥）。关键结论：
//   · 当系统访问实体的"全部组件"时，AoS 因缓存行内空间局部性反而更快；
//   · 当系统只访问"部分组件"时，SoA 因只搬动所需列而显著省带宽，更快。
// 组件集放大到 32 个 float(128B/实体)，使数据集超出缓存，凸显带宽差异。
#include <chrono>
#include <iostream>
#include <vector>

// 一个实体拥有 5 类组件，共 32 个 float
struct AoS {
    float px, py, pz;          // Position (3)
    float vx, vy, vz;          // Velocity (3)
    float hp, maxhp;           // Health   (2)
    float ai[8];               // AI 状态  (8)
    float rn[16];              // 渲染数据 (16)  -> 合计 32 float = 128 B
};

struct SoA {
    std::vector<float> px, py, pz;
    std::vector<float> vx, vy, vz;
    std::vector<float> hp, maxhp;
    std::vector<float> ai0, ai1, ai2, ai3, ai4, ai5, ai6, ai7;
    std::vector<float> rn0, rn1, rn2, rn3, rn4, rn5, rn6, rn7,
                      rn8, rn9, rn10, rn11, rn12, rn13, rn14, rn15;
};

// ── 场景1：移动系统访问"全部"组件（AoS 通常更快）──────────────────────
double bench_aos_full(std::size_t n, std::size_t iters) {
    std::vector<AoS> a(n);
    auto t0 = std::chrono::steady_clock::now();
    for (std::size_t k = 0; k < iters; ++k)
        for (std::size_t i = 0; i < n; ++i) {
            a[i].px += a[i].vx * 0.016f;
            a[i].py += a[i].vy * 0.016f;
            a[i].pz += a[i].vz * 0.016f;
        }
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

double bench_soa_full(std::size_t n, std::size_t iters) {
    SoA s;
    s.px.assign(n, 0); s.py.assign(n, 0); s.pz.assign(n, 0);
    s.vx.assign(n, 1); s.vy.assign(n, 1); s.vz.assign(n, 1);
    auto t0 = std::chrono::steady_clock::now();
    for (std::size_t k = 0; k < iters; ++k)
        for (std::size_t i = 0; i < n; ++i) {
            s.px[i] += s.vx[i] * 0.016f;
            s.py[i] += s.vy[i] * 0.016f;
            s.pz[i] += s.vz[i] * 0.016f;
        }
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

// ── 场景2：剔除系统只访问 Position（SoA 只搬 3 列，AoS 仍要搬整 128B）──
struct Result { double ms; double sink; };
// 用 volatile 防止编译器把"无用累加"优化掉（避免 DCE 导致 0ms 假象）
volatile double g_sink = 0;

Result bench_aos_partial(std::size_t n, std::size_t iters) {
    std::vector<AoS> a(n, {0});
    double sink = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (std::size_t k = 0; k < iters; ++k)
        for (std::size_t i = 0; i < n; ++i) {
            float d = a[i].px * a[i].px + a[i].py * a[i].py; // 只读 px,py
            sink += d;
        }
    auto t1 = std::chrono::steady_clock::now();
    g_sink += sink;
    return { std::chrono::duration<double, std::milli>(t1 - t0).count(), sink };
}

Result bench_soa_partial(std::size_t n, std::size_t iters) {
    SoA s;
    s.px.assign(n, 2); s.py.assign(n, 3); s.pz.assign(n, 0);
    double sink = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (std::size_t k = 0; k < iters; ++k)
        for (std::size_t i = 0; i < n; ++i) {
            float d = s.px[i] * s.px[i] + s.py[i] * s.py[i]; // 只读 px,py
            sink += d;
        }
    auto t1 = std::chrono::steady_clock::now();
    g_sink += sink;
    return { std::chrono::duration<double, std::milli>(t1 - t0).count(), sink };
}

int main() {
    const std::size_t N = 1 << 18;   // 262144 实体 -> AoS 数据集 32MB，超缓存
    const std::size_t ITERS = 60;
    std::cout << "[场景1] 移动系统访问全部组件\n";
    double ta1 = bench_aos_full(N, ITERS), ts1 = bench_soa_full(N, ITERS);
    std::cout << "  AoS: " << ta1 << " ms   SoA: " << ts1 << " ms"
              << "   AoS/SoA=" << (ta1 / ts1) << "x\n";

    std::cout << "[场景2] 剔除系统只访问 Position(px,py)\n";
    auto r2a = bench_aos_partial(N, ITERS), r2s = bench_soa_partial(N, ITERS);
    std::cout << "  AoS: " << r2a.ms << " ms   SoA: " << r2s.ms << " ms"
              << "   SoA/AoS=" << (r2a.ms / r2s.ms) << "x\n";
    std::cout << "  (sink 校验，防止 DCE: " << (long)g_sink << ")\n";
    return 0;
}

// _bench_d5_ch32_initialization.cpp — D5 性能基准：初始化方式的真实代价
// 编译: g++ -O2 -std=c++23 _bench_d5_ch32_initialization.cpp -o bench_ch32.exe
// 运行: bench_ch32.exe
// 环境: AMD Ryzen 9 7940HX, GCC 15.3.0 (MinGW-w64)

#include <iostream>
#include <chrono>
#include <vector>
#include <initializer_list>
#include <random>
#include <cstring>
#include <cassert>
#include <algorithm>
#include <iomanip>

using Clock = std::chrono::high_resolution_clock;
using Ms    = std::chrono::duration<double, std::milli>;

// ===================================================================
// DCE 防护
// ===================================================================
volatile long long g_sink   = 0;
volatile void*    g_ptr_sink = nullptr;

// ===================================================================
// 场景 S1：聚合初始化 vs 构造函数调用
// ===================================================================
struct Agg4   { int a, b, c, d; };
struct Ctor4  { int a, b, c, d; Ctor4(int w, int x, int y, int z)
                : a(w), b(x), c(y), d(z) {} };

// ===================================================================
// 场景 S2：Designated initializer（C++20） vs 位置初始化
// ===================================================================
struct Big8  { int a, b, c, d, e, f, g, h; };

// ===================================================================
// 场景 S3：initializer_list vs 参数包/直接构造
// ===================================================================
struct WrapIL {
    int vals[5];
    WrapIL(std::initializer_list<int> il) {
        int i = 0;
        for (auto v : il) vals[i++] = v;
    }
    int sum() const {
        return vals[0] + vals[1] + vals[2] + vals[3] + vals[4];
    }
};
struct WrapPack {
    int vals[5];
    WrapPack(int a, int b, int c, int d, int e)
        : vals{a, b, c, d, e} {}
    int sum() const {
        return vals[0] + vals[1] + vals[2] + vals[3] + vals[4];
    }
};

// ===================================================================
// 场景 S4：零初始化 vs 默认初始化 vs 值初始化
// ===================================================================
struct ValS { int x; double y; };

// ===================================================================
// 计时辅助：运行一次函数，返回毫秒
// ===================================================================
template <typename F>
double measure_once(F&& fn) {
    auto t0 = Clock::now();
    fn();
    auto t1 = Clock::now();
    return std::chrono::duration_cast<Ms>(t1 - t0).count();
}

// ===================================================================
// main
// ===================================================================
int main() {
    constexpr int N_S1S2 = 2'000'000;   // S1/S2: 每次构造带依赖链读回
    constexpr int N_S3   = 1'000'000;   // S3: 每次构造 5 个 int
    constexpr int N_S4   = 2'000'000;   // S4: 数组元素数
    constexpr int S4_REP = 50;          // S4: 重复分配/释放次数
    constexpr int ROUNDS = 5;

    // ------------------ 为每个场景预生成独立的输入数组 ------------------
    // S1: 需要 4*N_S1S2 个 int
    std::vector<int> in_S1(4 * N_S1S2);
    // S2: 需要 8*N_S1S2 个 int
    std::vector<int> in_S2(8 * N_S1S2);
    // S3: 需要 5*N_S3 个 int
    std::vector<int> in_S3(5 * N_S3);

    {
        std::mt19937 rng(42);
        std::uniform_int_distribution<int> dist(1, 1000);
        for (auto& v : in_S1) v = dist(rng);
        for (auto& v : in_S2) v = dist(rng);
        for (auto& v : in_S3) v = dist(rng);
    }

    // S4 使用独立 rng
    std::mt19937 rng4(99);
    std::uniform_int_distribution<int> idx4(0, N_S4 - 1);

    // ---------- 结果容器 ----------
    struct BenchEntry { const char* name; double runs[ROUNDS]; };
    std::vector<BenchEntry> results;

    std::cout << "D5 Benchmark: Initialization Cost (GCC 15.3.0 -O2 -std=c++23)" << std::endl;
    std::cout << "N_S1S2=" << N_S1S2 << "  N_S3=" << N_S3
              << "  N_S4=" << N_S4 << "(" << S4_REP << " reps)" << std::endl;
    std::cout << std::endl;

    // =========== 预热 ===========
    {
        volatile long long w = 0;
        for (int i = 0; i < 100; ++i) { Agg4 a{1,2,3,4}; w += a.a; }
        g_sink = w;
    }

    // =========== S1a: 聚合初始化 ===========
    {
        BenchEntry e{"Aggregate_init", {}};
        for (int r = 0; r < ROUNDS; ++r) {
            long long s = 0;
            e.runs[r] = measure_once([&]() {
                for (int i = 0; i < N_S1S2; ++i) {
                    int j = 4*i;
                    Agg4 a{in_S1[j], in_S1[j+1], in_S1[j+2], in_S1[j+3]};
                    s += a.a + a.b + a.c + a.d;
                }
            });
            g_sink = s;
        }
        results.push_back(e);
    }

    // =========== S1b: 构造函数调用（相同输入，不同语法） ===========
    {
        BenchEntry e{"Constructor", {}};
        for (int r = 0; r < ROUNDS; ++r) {
            long long s = 0;
            e.runs[r] = measure_once([&]() {
                for (int i = 0; i < N_S1S2; ++i) {
                    int j = 4*i;
                    Ctor4 c(in_S1[j], in_S1[j+1], in_S1[j+2], in_S1[j+3]);
                    s += c.a + c.b + c.c + c.d;
                }
            });
            g_sink = s;
        }
        results.push_back(e);
    }

    // =========== S2a: 位置初始化 (Big8) ===========
    {
        BenchEntry e{"Positional_init", {}};
        for (int r = 0; r < ROUNDS; ++r) {
            long long s = 0;
            e.runs[r] = measure_once([&]() {
                for (int i = 0; i < N_S1S2; ++i) {
                    int j = 8*i;
                    Big8 b{in_S2[j], in_S2[j+1], in_S2[j+2], in_S2[j+3],
                           in_S2[j+4], in_S2[j+5], in_S2[j+6], in_S2[j+7]};
                    s += b.a + b.b + b.c + b.d + b.e + b.f + b.g + b.h;
                }
            });
            g_sink = s;
        }
        results.push_back(e);
    }

    // =========== S2b: Designated init (Big8) ===========
    {
        BenchEntry e{"Designated_init", {}};
        for (int r = 0; r < ROUNDS; ++r) {
            long long s = 0;
            e.runs[r] = measure_once([&]() {
                for (int i = 0; i < N_S1S2; ++i) {
                    int j = 8*i;
                    Big8 b{.a=in_S2[j],   .b=in_S2[j+1], .c=in_S2[j+2], .d=in_S2[j+3],
                           .e=in_S2[j+4], .f=in_S2[j+5], .g=in_S2[j+6], .h=in_S2[j+7]};
                    s += b.a + b.b + b.c + b.d + b.e + b.f + b.g + b.h;
                }
            });
            g_sink = s;
        }
        results.push_back(e);
    }

    // =========== S3a: initializer_list 构造（运行期值） ===========
    {
        BenchEntry e{"Init_list_runtime", {}};
        for (int r = 0; r < ROUNDS; ++r) {
            long long s = 0;
            e.runs[r] = measure_once([&]() {
                for (int i = 0; i < N_S3; ++i) {
                    int j = 5*i;
                    WrapIL w{in_S3[j], in_S3[j+1], in_S3[j+2], in_S3[j+3], in_S3[j+4]};
                    s += w.sum();
                }
            });
            g_sink = s;
        }
        results.push_back(e);
    }

    // =========== S3b: 参数包直接构造（运行期值） ===========
    {
        BenchEntry e{"Pack_runtime", {}};
        for (int r = 0; r < ROUNDS; ++r) {
            long long s = 0;
            e.runs[r] = measure_once([&]() {
                for (int i = 0; i < N_S3; ++i) {
                    int j = 5*i;
                    WrapPack w(in_S3[j], in_S3[j+1], in_S3[j+2], in_S3[j+3], in_S3[j+4]);
                    s += w.sum();
                }
            });
            g_sink = s;
        }
        results.push_back(e);
    }

    // =========== S3c: initializer_list 字面量常量 ===========
    {
        BenchEntry e{"Init_list_literal", {}};
        for (int r = 0; r < ROUNDS; ++r) {
            long long s = 0;
            e.runs[r] = measure_once([&]() {
                for (int i = 0; i < N_S3; ++i) {
                    WrapIL w{1, 2, 3, 4, 5};
                    s += w.sum();
                }
            });
            g_sink = s;
        }
        results.push_back(e);
    }

    // =========== S3d: 参数包常量 ===========
    {
        BenchEntry e{"Pack_literal", {}};
        for (int r = 0; r < ROUNDS; ++r) {
            long long s = 0;
            e.runs[r] = measure_once([&]() {
                for (int i = 0; i < N_S3; ++i) {
                    WrapPack w(1, 2, 3, 4, 5);
                    s += w.sum();
                }
            });
            g_sink = s;
        }
        results.push_back(e);
    }

    // =========== S4a: 零初始化 int[N]{}（分配 + 全量 memset 0） ===========
    {
        BenchEntry e{"Zero_init_array", {}};
        for (int r = 0; r < ROUNDS; ++r) {
            long long s = 0;
            e.runs[r] = measure_once([&]() {
                for (int k = 0; k < S4_REP; ++k) {
                    int* arr = new int[N_S4]();          // () 触发零初始化
                    arr[idx4(rng4) % N_S4] = k;          // 阻止整个数组被 DCE
                    s += arr[0];
                    delete[] arr;
                }
            });
            g_sink = s;
        }
        results.push_back(e);
    }

    // =========== S4b: 默认初始化 int[N]（仅分配，不置零） ===========
    {
        BenchEntry e{"Default_init_array", {}};
        for (int r = 0; r < ROUNDS; ++r) {
            long long s = 0;
            e.runs[r] = measure_once([&]() {
                for (int k = 0; k < S4_REP; ++k) {
                    int* arr = new int[N_S4];             // 默认初始化（值不确定）
                    arr[0] = k;                           // 写入后才能合法读取
                    arr[idx4(rng4) % N_S4] = k + 1;
                    s += arr[0];
                    delete[] arr;
                }
            });
            g_sink = s;
        }
        results.push_back(e);
    }

    // =========== S4c: 值初始化 struct ValS{} ===========
    {
        BenchEntry e{"Value_init_struct", {}};
        for (int r = 0; r < ROUNDS; ++r) {
            long long s = 0;
            e.runs[r] = measure_once([&]() {
                for (int i = 0; i < N_S3; ++i) {
                    ValS obj{};                            // x=0, y=0.0
                    s += obj.x + static_cast<int>(obj.y);
                }
            });
            g_sink = s;
        }
        results.push_back(e);
    }

    // =========== S4d: 默认初始化 struct（不写任何值→读未定义行为，这里仅计分配成本） ===========
    {
        BenchEntry e{"Default_init_struct", {}};
        for (int r = 0; r < ROUNDS; ++r) {
            long long s = 0;
            e.runs[r] = measure_once([&]() {
                for (int i = 0; i < N_S3; ++i) {
                    ValS obj;                              // x, y 未初始化
                    obj.x = in_S3[i % (5*N_S3)];           // 写入后合法读取
                    s += obj.x;
                }
            });
            g_sink = s;
        }
        results.push_back(e);
    }

    // =========== 输出表格 ===========
    std::cout << std::left;
    std::cout << "=== Benchmark Results (5 rounds, median) ===" << std::endl;
    std::cout << std::endl;

    std::vector<double> medians;
    for (auto& e : results) {
        std::sort(e.runs, e.runs + ROUNDS);
        medians.push_back(e.runs[ROUNDS / 2]);
    }

    double baseline = medians.empty() ? 1.0 : medians[0];
    for (size_t i = 0; i < results.size(); ++i) {
        double ratio = medians[i] / baseline;
        std::cout << std::setw(22) << results[i].name
                  << "  " << std::setw(9) << std::fixed << std::setprecision(3)
                  << medians[i] << " ms"
                  << "  " << std::setprecision(3) << ratio << "x";
        if (i == 0) std::cout << " (baseline)";
        std::cout << std::endl;
    }

    std::cout << std::endl;
    std::cout << "=== Key Comparisons ===" << std::endl;
    std::cout << "S1 Aggregate vs Constructor: "
              << (std::abs(medians[0] - medians[1]) < 1.0 ? "IDENTICAL" : "DIFFERS")
              << " (delta=" << std::setprecision(3) << (medians[0] - medians[1]) << " ms)" << std::endl;
    std::cout << "S2 Positional vs Designated: "
              << (std::abs(medians[2] - medians[3]) < 1.0 ? "IDENTICAL" : "DIFFERS")
              << " (delta=" << std::setprecision(3) << (medians[2] - medians[3]) << " ms)" << std::endl;
    std::cout << "S3 InitList runtime vs Pack runtime: "
              << "pack faster by " << std::setprecision(3)
              << (medians[4] - medians[5]) << " ms" << std::endl;
    std::cout << "S3 InitList literal vs Pack literal: "
              << "delta=" << std::setprecision(3)
              << (medians[6] - medians[7]) << " ms" << std::endl;
    std::cout << "S4 Zero-init array vs Default-init array: "
              << "ratio=" << std::setprecision(3)
              << (medians[8] / medians[9]) << "x" << std::endl;
    std::cout << "S4 Value-init struct vs Default-init struct: "
              << "delta=" << std::setprecision(3)
              << (medians[10] - medians[11]) << " ms" << std::endl;

    std::cout << std::endl << "Done." << std::endl;
    return 0;
}

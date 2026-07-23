// 真实基准: libstdc++ std::sort(introsort) vs naive quicksort 在四种输入分布下
// 编译器: mingw1530 GCC 15.3.0 ; 编译: -O2 -std=c++17 -static
// 目的: 实证 introsort 存在的根本理由:
//   (1) std::sort 在所有分布下均 O(n log n) 稳定;
//   (2) 朴素 quicksort(固定首元素 pivot, 无深度限制) 在已排序/逆序输入下
//       退化为 O(n^2) —— introsort 的 median-of-three + 深度限制 heap fallback 正是解药.
//
// 注: 朴素 quicksort 此处用"显式栈迭代版"实现, 目的是彻底消除真实调用栈溢出,
//     让 O(n^2) 退化以"耗时"形式被干净测量(不依赖不可靠的大栈链接标志).
//     真实递归版在已排序输入下递归深度=n, 实测 M>=~12000 即触发 0xC00000FD 栈溢出(见附文).
#include <algorithm>
#include <vector>
#include <random>
#include <chrono>
#include <cstdio>
#include <utility>

static double now() {
    return std::chrono::duration<double, std::milli>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}

// naive quicksort: 固定首元素 pivot(经典 Lomuto), 无随机化, 无深度限制 -> 已排序输入 O(n^2)
// 迭代式(显式堆栈), 仅用于隔离"调用栈溢出"变量, 干净测量退化耗时.
// 注: Lomuto 保证必然终止(最坏 O(n^2) 但有限); 若用"首元素 pivot 的 Hoare 变体"且不做
//     median-of-three, 当首元素恰为区间最大值时 partition 会返回整个区间 -> 死循环.
//     这正是 libstdc++ 必须先 __move_median_to_first 的根本原因(见附录源码解析).
template<typename It>
void naive_qs(It a, It b) {
    std::vector<std::pair<It, It>> st;
    if (b - a > 1) st.push_back({a, b});
    while (!st.empty()) {
        auto [lo, hi] = st.back();
        st.pop_back();
        if (hi - lo <= 1) continue;
        auto pivot = *lo;                 // 固定首元素 pivot —— 朴素快排的退化之源
        It i = lo;
        for (It k = lo + 1; k != hi; ++k) {
            if (*k < pivot) { ++i; std::iter_swap(i, k); }
        }
        std::iter_swap(lo, i);            // pivot 落位: [lo,i) < pivot, [i+1,hi) >= pivot
        st.push_back({lo, i});            // 左段
        st.push_back({i + 1, hi});         // 右段
    }
}

enum Dist { RANDOM, ASC, DESC, FEWUNIQ };

void fill(std::vector<int>& v, Dist d, unsigned seed) {
    size_t n = v.size();
    if (d == RANDOM) {
        std::mt19937 rng(seed);
        for (size_t k = 0; k < n; ++k) v[k] = (int)rng();
    } else if (d == ASC) {
        for (size_t k = 0; k < n; ++k) v[k] = (int)k;
    } else if (d == DESC) {
        for (size_t k = 0; k < n; ++k) v[k] = (int)(n - k);
    } else {
        std::mt19937 rng(seed);
        std::uniform_int_distribution<int> ud(0, (int)(n / 10 + 1));
        for (size_t k = 0; k < n; ++k) v[k] = ud(rng);
    }
}

const char* name(Dist d) {
    return d == RANDOM ? "random    " : d == ASC ? "ascending " :
           d == DESC ? "descending" : "few-unique";
}

int main() {
    const size_t N = 2'000'000;   // std::sort 全量(= introsort 真实战场); 取单次实测, 控制总耗时
    const int RUNS = 1;
    std::printf("=== 基准: GCC 15.3.0 -O2 x86-64, 单次实测 ===\n\n");

    std::printf("表1. std::sort(introsort) @ N=%zu 四种分布\n", N);
    std::printf("dist       | std::sort(ms)\n");
    std::printf("-----------+-------------\n");
    double sort_t[4];
    for (int di = 0; di < 4; ++di) {
        Dist d = (Dist)di;
        double best = 1e9;
        for (int r = 0; r < RUNS; ++r) {
            std::vector<int> v(N);
            fill(v, d, 42 + r);
            double t0 = now();
            std::sort(v.begin(), v.end());
            double t1 = now();
            best = std::min(best, t1 - t0);
            if (!std::is_sorted(v.begin(), v.end())) { std::printf("SORT FAIL\n"); return 1; }
        }
        sort_t[di] = best;
        std::printf("  %-10s | %11.2f\n", name(d), best);
    }

    std::printf("\n表2. naive quicksort(首元素pivot,无深度限制,迭代式) @ 见列 M\n");
    std::printf("dist       | naive_qs(ms) |   M     | 相对 random 倍率\n");
    std::printf("-----------+-------------+--------+------------------\n");
    size_t M[4];
    // ASC/DESC/FEW_UNIQUE 在"固定首元素 pivot + 无深度限制"下均会退化:
    //  - ASC/DESC: 必然 O(n^2)(pivot 恒为极值, 每轮仅剔除 1 个元素)
    //  - FEW_UNIQUE: 低基数数据下若首元素恰为最大值, 同样退化为 O(n^2)
    // 三者统一取 M=50'000, 使其 O(n^2) 工作量(≈1.25e9)在数秒内可测且绝不溢出.
    // RANDOM: 真随机分布, 朴素快排约为 O(n log n), 取大 M 凸显"它只在随机时看似可用".
    M[RANDOM] = 200'000; M[ASC] = 30'000; M[DESC] = 30'000; M[FEWUNIQ] = 30'000;
    double naive_t[4];
    for (int di = 0; di < 4; ++di) {
        Dist d = (Dist)di;
        double best = 1e9;
        for (int r = 0; r < RUNS; ++r) {
            std::vector<int> w(M[di]);
            fill(w, d, 7 + r);
            double t0 = now();
            naive_qs(w.begin(), w.end());
            double t1 = now();
            best = std::min(best, t1 - t0);
            if (!std::is_sorted(w.begin(), w.end())) { std::printf("QS FAIL\n"); return 1; }
        }
        naive_t[di] = best;
        double ratio = naive_t[di] / naive_t[RANDOM];
        std::printf("  %-10s | %11.2f | %7zu | %.1fx\n", name(d), best, M[di], ratio);
    }

    std::printf("\n关键对比(同规模 N=%zu 外推):\n", N);
    std::printf("  std::sort 最坏分布(%.2f ms) vs naive_qs 若按各自复杂度外推到 N=%zu:\n",
                *std::max_element(sort_t, sort_t+4), N);
    // naive ASC/DESC 为 O(n^2): t(N) ≈ t(M) * (N/M)^2
    double proj_asc = naive_t[ASC] * double(N*N) / double(M[ASC]*M[ASC]);
    double proj_desc = naive_t[DESC] * double(N*N) / double(M[DESC]*M[DESC]);
    std::printf("    naive_qs ascending  外推 t(20M) ≈ %.1f ms (%.1f 秒)  [O(n^2)]\n",
                proj_asc, proj_asc/1000.0);
    std::printf("    naive_qs descending 外推 t(20M) ≈ %.1f ms (%.1f 秒)  [O(n^2)]\n",
                proj_desc, proj_desc/1000.0);
    double sort_worst = *std::max_element(sort_t, sort_t+4);
    std::printf("    std::sort 实测最慢    t(20M) =   %.2f ms\n", sort_worst);
    std::printf("    => introsort 比朴素 quicksort 在退化输入上快约 %.0f 倍(量级)\n",
                std::max(proj_asc, proj_desc) / sort_worst);
    return 0;
}

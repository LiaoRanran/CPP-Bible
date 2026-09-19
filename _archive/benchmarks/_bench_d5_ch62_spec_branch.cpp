// _bench_d5_ch62_spec_branch.cpp
// D5 角度: 模板特化路由(if constexpr 消除分支) vs 运行期 if/else 类型标签分支链
// 实测: AMD Ryzen 9 7940HX, g++ 15.3.0 -O2 -std=c++23
//
// 关键公平性:
//   - constexpr 路由: 数据按 tag 预分区到 3 个同构 batch, 每批单态化循环
//     3 循环总迭代 = N, 无分支预测抖动
//   - if/else 链: 在随机洗排的 tag 数组上单次扫描(N 迭代), 每元素一次 if/else
//     分支 —— 随机 tag 令分支预测器无法学习 → 高 misprediction 率
//   两侧总迭代均 = N.
//   修复: 随机洗牌 tag 排列, 令 if/else 分支不可预测, 放大 branch misprediction
#include <chrono>
#include <cstdio>
#include <vector>
#include <cstdint>
#include <random>
#include <algorithm>

static volatile long long g_sink = 0;

enum OpType : int { OP_ADD = 0, OP_MUL = 1, OP_XOR = 2 };

static inline int do_add(int x) { return x + 7; }
static inline int do_mul(int x) { return x * 3; }
static inline int do_xor(int x) { return x ^ 0x55; }

// ---- A. 编译期路由: if constexpr 消除分支, 单态化内联 ----
template <OpType Tag>
long long run_constexpr_route(std::vector<int> const& v) {
    long long acc = 0;
    for (int x : v) {
        if constexpr (Tag == OP_ADD)      acc += do_add(x);
        else if constexpr (Tag == OP_MUL) acc += do_mul(x);
        else                              acc += do_xor(x);
    }
    return acc;
}

// ---- B. 运行期 if/else 链: 随机 tag → 分支 misprediction ----
long long run_ifelse_chain(std::vector<int> const& v, std::vector<int> const& tags) {
    long long acc = 0;
    for (size_t i = 0; i < v.size(); ++i) {
        int x = v[i], t = tags[i];
        if      (t == OP_ADD) acc += do_add(x);
        else if (t == OP_MUL) acc += do_mul(x);
        else                  acc += do_xor(x);
    }
    return acc;
}

int main() {
    const long long N = 20000000LL;        // 2e7
    std::vector<int> v(N);
    std::vector<int> tags(N);
    for (long long i = 0; i < N; ++i) {
        v[i]    = static_cast<int>(i & 0xFF);
        tags[i] = static_cast<int>(i % 3);  // 初始: 均匀交织
    }

    // 随机洗牌 tag: 让分支预测器无法学习 → 放大 misprediction 开销
    std::mt19937 rng(42);
    std::shuffle(tags.begin(), tags.end(), rng);

    // 预分区: 按 tag 把元素分配到 3 个同构 batch (一次性 setup, 不计入计时)
    std::vector<int> add_v, mul_v, xor_v;
    add_v.reserve(N / 3 + 1); mul_v.reserve(N / 3 + 1); xor_v.reserve(N / 3 + 1);
    for (long long i = 0; i < N; ++i) {
        if (tags[i] == OP_ADD)      add_v.push_back(v[i]);
        else if (tags[i] == OP_MUL) mul_v.push_back(v[i]);
        else                        xor_v.push_back(v[i]);
    }

    // 5 轮中位计时
    for (int trial = 0; trial < 5; ++trial) {
        // A: 3 个单态化循环, 总迭代 = N
        auto t0 = std::chrono::steady_clock::now();
        long long r1 = run_constexpr_route<OP_ADD>(add_v) +
                       run_constexpr_route<OP_MUL>(mul_v) +
                       run_constexpr_route<OP_XOR>(xor_v);
        auto t1 = std::chrono::steady_clock::now();

        // B: 单次 if/else 扫描, 迭代 = N (随机 tag → misprediction)
        long long r2 = run_ifelse_chain(v, tags);
        auto t2 = std::chrono::steady_clock::now();

        g_sink = r1 + r2;
        double dt_c = std::chrono::duration<double, std::milli>(t1 - t0).count();
        double dt_r = std::chrono::duration<double, std::milli>(t2 - t1).count();
        std::printf("trial %d: constexpr_route=%.3f ms  ifelse_chain=%.3f ms  ratio=%.2fx\n",
                    trial, dt_c, dt_r, dt_r / dt_c);
    }
    std::printf("SUMMARY constexpr_vs_ifelse\n");
    return 0;
}

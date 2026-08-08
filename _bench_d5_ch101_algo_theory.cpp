// _bench_d5_ch101_algo_theory.cpp — 附录 D5 基准：算法复杂度在实际硬件上的表现（ch101）
// 编译:
//   C:/Qt/Tools/mingw1530_64/bin/g++.EXE -O2 -std=c++23 _bench_d5_ch101_algo_theory.cpp -o _bench_d5_ch101_algo_theory.exe -Wl,--stack,33554432 -lwinmm
//   注意: memoized 斐波那契递归深度达 40000，远超 Windows 默认 1MB 线程栈，必须用
//         -Wl,--stack,33554432 (32MB) 扩大栈，否则运行期触发 STATUS_STACK_OVERFLOW (0xC00000FD)。
//         -lwinmm 必须在源文件之后（提供 timeBeginPeriod/timeEndPeriod 导入）。
// 方法学:
//   - 每个场景跑 5 轮取中位数，单轮 >= 数十 ms
//   - 数据用运行期随机数填充，防止编译器闭式折叠
//   - 结果累加到 volatile sink，防止 DCE
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <queue>
#include <random>
#include <unordered_map>
#include <vector>

#ifdef _WIN32
#include <windows.h>
#endif

using Clock = std::chrono::steady_clock;

static volatile std::uint64_t g_sink = 0;

static double ms_since(Clock::time_point t0) {
    return std::chrono::duration<double, std::milli>(Clock::now() - t0).count();
}

static double median5(double a[5]) {
    std::sort(a, a + 5);
    return a[2];
}

// ==================== 场景 1：DP 自底向上 vs 记忆化递归 ====================
// 斐波那契数列：两种 DP 实现的缓存局部性差异
// 理论复杂度均为 O(n)，但 tabulated 顺序访问数组 vs memoized 递归+哈希/数组随机访问

static long long fib_tabulated(int n) {
    if (n < 2) return n;
    std::vector<long long> dp(n + 1);
    dp[0] = 0;
    dp[1] = 1;
    for (int i = 2; i <= n; ++i)
        dp[i] = dp[i - 1] + dp[i - 2];
    return dp[n];
}

// 直接递归（不用 std::function，减小栈帧）+ memo 数组
static long long fib_memo_helper(int k, std::vector<long long>& memo) {
    if (k < 2) return k;
    if (memo[k] != -1) return memo[k];
    long long a = fib_memo_helper(k - 1, memo);
    long long b = fib_memo_helper(k - 2, memo);
    memo[k] = a + b;
    return memo[k];
}

static long long fib_memoized(int n) {
    std::vector<long long> memo(n + 1, -1);
    return fib_memo_helper(n, memo);
}

// ==================== 场景 2：哈希表 vs 排序数组+二分查找 ====================
// 查找性能：理论均摊 O(1) vs O(log n)
// 关键洞察：大数据量下哈希表的随机内存访问 vs 排序数组的连续内存+二分

static void bench_hash_vs_sorted() {
    constexpr int N = 2'000'000;
    constexpr int Q = 5'000'000;
    std::mt19937 rng(12345);
    std::uniform_int_distribution<int> dist(0, N * 10);

    // 构建数据集
    std::vector<int> keys(N);
    for (auto& k : keys) k = dist(rng);
    std::sort(keys.begin(), keys.end());
    keys.erase(std::unique(keys.begin(), keys.end()), keys.end());

    // 构建 unordered_map
    std::unordered_map<int, int> umap;
    umap.reserve(keys.size());
    for (int i = 0; i < (int)keys.size(); ++i)
        umap[keys[i]] = i;

    // 查询序列（含命中和未命中）
    std::vector<int> queries(Q);
    std::uniform_int_distribution<int> qdist(0, (int)keys.size() * 2 - 1);
    for (auto& q : queries) q = qdist(rng);

    // 基准：unordered_map
    double t_hash[5];
    for (int r = 0; r < 5; ++r) {
        volatile long long sum = 0;
        auto t0 = Clock::now();
        for (auto q : queries) {
            auto it = umap.find(q);
            sum += (it != umap.end()) ? it->second : -1;
        }
        g_sink += static_cast<std::uint64_t>(sum);
        t_hash[r] = ms_since(t0);
    }

    // 基准：排序数组 + 二分查找
    double t_bsearch[5];
    for (int r = 0; r < 5; ++r) {
        volatile long long sum = 0;
        auto t0 = Clock::now();
        for (auto q : queries) {
            auto it = std::lower_bound(keys.begin(), keys.end(), q);
            int val = (it != keys.end() && *it == q)
                          ? static_cast<int>(it - keys.begin())
                          : -1;
            sum += val;
        }
        g_sink += static_cast<std::uint64_t>(sum);
        t_bsearch[r] = ms_since(t0);
    }

    double mh = median5(t_hash);
    double mb = median5(t_bsearch);
    std::printf("场景2: unordered_map vs sorted_array+bsearch (N=%d, Q=%d)\n", N, Q);
    std::printf("  unordered_map     : %.3f ms\n", mh);
    std::printf("  sorted+bsearch    : %.3f ms\n", mb);
    std::printf("  speedup(map/bs)   : %.2fx\n", mb / mh);
    std::printf("\n");
}

// ==================== 场景 3：BFS vs DFS 图遍历 ====================
// 理论均为 O(V+E)，但访问模式不同导致缓存行为差异
// BFS：队列 + 顺序访问邻接表（较友好）
// DFS：递归栈 + 深入访问（可能跳跃远）

static void bench_bfs_vs_dfs() {
    constexpr int V = 1'000'000;
    constexpr int AVG_DEG = 8;

    // 构建随机图（邻接表）
    std::vector<std::vector<int>> adj(V);
    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(0, V - 1);
    for (int u = 0; u < V; ++u) {
        for (int d = 0; d < AVG_DEG; ++d)
            adj[u].push_back(dist(rng));
        // 去重并排序以改善缓存
        std::sort(adj[u].begin(), adj[u].end());
        adj[u].erase(std::unique(adj[u].begin(), adj[u].end()), adj[u].end());
    }

    // BFS
    double t_bfs[5];
    for (int r = 0; r < 5; ++r) {
        volatile long long sum = 0;
        std::vector<int> dist_arr(V, -1);
        auto t0 = Clock::now();
        std::queue<int> q;
        dist_arr[0] = 0;
        q.push(0);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            sum += u;
            for (int v : adj[u]) {
                if (dist_arr[v] == -1) {
                    dist_arr[v] = dist_arr[u] + 1;
                    q.push(v);
                }
            }
        }
        g_sink += static_cast<std::uint64_t>(sum);
        t_bfs[r] = ms_since(t0);
    }

    // DFS（迭代式，避免深递归爆栈）
    double t_dfs[5];
    for (int r = 0; r < 5; ++r) {
        volatile long long sum = 0;
        std::vector<bool> vis(V, false);
        auto t0 = Clock::now();
        std::vector<int> stk;
        stk.reserve(V);
        stk.push_back(0);
        vis[0] = true;
        while (!stk.empty()) {
            int u = stk.back(); stk.pop_back();
            sum += u;
            for (int v : adj[u]) {
                if (!vis[v]) {
                    vis[v] = true;
                    stk.push_back(v);
                }
            }
        }
        g_sink += static_cast<std::uint64_t>(sum);
        t_dfs[r] = ms_since(t0);
    }

    double mbfs = median5(t_bfs);
    double mdfs = median5(t_dfs);
    std::printf("场景3: BFS vs DFS (V=%d, E~%dK)\n", V, V * AVG_DEG / 1000);
    std::printf("  BFS (queue)       : %.3f ms\n", mbfs);
    std::printf("  DFS (stack)       : %.3f ms\n", mdfs);
    std::printf("  speedup(DFS/BFS)  : %.2fx\n", mbfs / mdfs);
    std::printf("\n");
}

// ==================== 场景 4：贪心 vs DP —— 同一问题的不同解法 ====================
// 0/1 背包：DP 解法 O(nW) vs 贪心解法 O(n log n)
// 贪心不保证最优但快得多；DP 保证最优但慢
// 关键洞察：当问题允许贪心时（如分数背包），速度差是阶数级的

static void bench_greedy_vs_dp() {
    constexpr int N = 2000;
    constexpr int W = 100000;

    std::mt19937 rng(777);
    std::uniform_int_distribution<int> wdist(1, 1000);
    std::uniform_int_distribution<int> vdist(1, 1000);

    std::vector<int> weights(N), values(N);
    for (int i = 0; i < N; ++i) {
        weights[i] = wdist(rng);
        values[i] = vdist(rng);
    }

    // DP 解法：0/1 背包，保证最优解
    double t_dp[5];
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        std::vector<int> dp(W + 1, 0);
        for (int i = 0; i < N; ++i)
            for (int w = W; w >= weights[i]; --w)
                dp[w] = std::max(dp[w], dp[w - weights[i]] + values[i]);
        g_sink += static_cast<std::uint64_t>(dp[W]);
        t_dp[r] = ms_since(t0);
    }

    // 贪心解法：按价值密度排序，依次取（不保证最优但极快）
    double t_greedy[5];
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        std::vector<std::pair<double, int>> order(N);
        for (int i = 0; i < N; ++i)
            order[i] = { (double)values[i] / weights[i], i };
        std::sort(order.begin(), order.end(), [](auto& a, auto& b) {
            return a.first > b.first;
        });
        int remaining = W;
        long long total = 0;
        for (auto& [ratio, idx] : order) {
            if (weights[idx] <= remaining) {
                remaining -= weights[idx];
                total += values[idx];
            }
        }
        g_sink += static_cast<std::uint64_t>(total);
        t_greedy[r] = ms_since(t0);
    }

    double mdp = median5(t_dp);
    double mg = median5(t_greedy);
    std::printf("场景4: 贪心 vs DP 0/1背包 (N=%d, W=%d)\n", N, W);
    std::printf("  DP (0/1 knapsack) : %.3f ms\n", mdp);
    std::printf("  greedy (by ratio)  : %.3f ms\n", mg);
    std::printf("  speedup(DP/greedy) : %.2fx\n", mdp / mg);
    std::printf("\n");
}

int main() {
#ifdef _WIN32
    // 提高计时精度
    timeBeginPeriod(1);
#endif

    std::printf("=== ch101 D5 基准：算法复杂度在实际硬件上的表现 ===\n");
    std::printf("环境: AMD Ryzen 9 7940HX, GCC 15.3.0 (MinGW-w64), -O2 -std=c++23\n");
    std::printf("方法: 5轮取中位, volatile sink\n\n");

    // ---------- 场景 1：DP tabulated vs memoized ----------
    constexpr int FIB_N = 5'000'000;  // 足够大以放大缓存差异
    double t_tab[5], t_memo[5];
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        volatile long long res = fib_tabulated(FIB_N);
        g_sink += static_cast<std::uint64_t>(res);
        t_tab[r] = ms_since(t0);
    }
    // memoized 版本受递归深度限制，用较小的 n（需大栈编译）
    constexpr int FIB_MEMO = 40000;
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        volatile long long res = fib_memoized(FIB_MEMO);
        g_sink += static_cast<std::uint64_t>(res);
        t_memo[r] = ms_since(t0);
    }

    double mt = median5(t_tab);
    double mm = median5(t_memo);
    std::printf("场景1: DP tabulated vs memoized (fib)\n");
    std::printf("  tabulated (n=%d)  : %.3f ms\n", FIB_N, mt);
    std::printf("  memoized  (n=%d) : %.3f ms\n", FIB_MEMO, mm);
    std::printf("  注意: n 不同因递归深度限制; 关注每元素吞吐\n");
    std::printf("  tabulated ns/elem : %.2f ns\n", mt * 1e6 / FIB_N);
    std::printf("  memoized  ns/elem : %.2f ns\n", mm * 1e6 / FIB_MEMO);
    std::printf("  per-element ratio : %.2fx\n",
                (mm * 1e6 / FIB_MEMO) / (mt * 1e6 / FIB_N));
    std::printf("\n");

    // ---------- 场景 2：哈希表 vs 排序数组+二分 ----------
    bench_hash_vs_sorted();

    // ---------- 场景 3：BFS vs DFS ----------
    bench_bfs_vs_dfs();

    // ---------- 场景 4：贪心 vs DP ----------
    bench_greedy_vs_dp();

#ifdef _WIN32
    timeEndPeriod(1);
#endif
    return 0;
}

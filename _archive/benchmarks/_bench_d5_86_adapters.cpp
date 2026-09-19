// _bench_d5_86_adapters.cpp — ch86 容器适配器：底层容器选择的真实代价
// g++ -O2 -std=c++23
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <vector>
#include <deque>
#include <list>
#include <stack>
#include <queue>
#include <set>
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

int main() {
    constexpr int M = 10'000'000;  // stack/queue 元素数
    constexpr int P = 2'000'000;   // priority_queue/multiset 元素数

    std::vector<int> data(P);
    std::mt19937 rng(42);
    for (auto& v : data) v = int(rng());

    // ---- stack：默认 deque vs vector ----
    bench("stack<int,deque> push+pop x10M", [&] {
        std::stack<int> s;
        for (int i = 0; i < M; ++i) s.push(i);
        std::uint64_t acc = 0;
        while (!s.empty()) { acc += s.top(); s.pop(); }
        g_sink = acc;
    });
    bench("stack<int,vector> push+pop x10M", [&] {
        std::stack<int, std::vector<int>> s;
        for (int i = 0; i < M; ++i) s.push(i);
        std::uint64_t acc = 0;
        while (!s.empty()) { acc += s.top(); s.pop(); }
        g_sink = acc;
    });

    // ---- queue：默认 deque vs list ----
    bench("queue<int,deque> push+pop x10M", [&] {
        std::queue<int> q;
        for (int i = 0; i < M; ++i) q.push(i);
        std::uint64_t acc = 0;
        while (!q.empty()) { acc += q.front(); q.pop(); }
        g_sink = acc;
    });
    bench("queue<int,list> push+pop x10M", [&] {
        std::queue<int, std::list<int>> q;
        for (int i = 0; i < M; ++i) q.push(i);
        std::uint64_t acc = 0;
        while (!q.empty()) { acc += q.front(); q.pop(); }
        g_sink = acc;
    });

    // ---- priority_queue vs multiset（同为"有序取最大"语义） ----
    std::uint64_t s1 = 0, s2 = 0;
    bench("priority_queue push+popall x2M", [&] {
        std::priority_queue<int> pq;
        for (int v : data) pq.push(v);
        std::uint64_t acc = 0;
        while (!pq.empty()) { acc += std::uint64_t(std::uint32_t(pq.top())); pq.pop(); }
        s1 = acc; g_sink = acc;
    });
    bench("multiset insert+eraseall x2M", [&] {
        std::multiset<int> ms;
        for (int v : data) ms.insert(v);
        std::uint64_t acc = 0;
        while (!ms.empty()) {
            auto it = std::prev(ms.end());
            acc += std::uint64_t(std::uint32_t(*it));
            ms.erase(it);
        }
        s2 = acc; g_sink = acc;
    });
    std::printf("checksums: %llu %llu (must equal)\n",
                (unsigned long long)s1, (unsigned long long)s2);
    return 0;
}

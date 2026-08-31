// _bench_unv2.cpp — 真实复测 ch79(vector/list 遍历) 与 ch40(异常开销 / noexcept 4x) 的「本机实测」声明
// 复现：g++ -O2 -std=c++20
#include <iostream>
#include <vector>
#include <list>
#include <chrono>
#include <cstring>
#include <random>

volatile int64_t g_sink = 0;

double ms_of(void (*f)(int), int N, int R) {
    double best = 1e18;
    for (int r = 0; r < R; ++r) {
        auto a = std::chrono::steady_clock::now();
        f(N);
        auto b = std::chrono::steady_clock::now();
        double ms = std::chrono::duration<double, std::milli>(b - a).count();
        if (ms < best) best = ms;
    }
    return best;
}

std::vector<int> g_v;
std::list<int>  g_l;

void f_vec(int N) {
    g_v.assign(N, 0);
    for (int i = 0; i < N; ++i) g_v[i] = i;
    int64_t s = 0;
    for (int x : g_v) s += x;
    g_sink += s;
}
void f_lst(int N) {
    g_l.clear();
    for (int i = 0; i < N; ++i) g_l.push_back(i);
    int64_t s = 0;
    for (int x : g_l) s += x;
    g_sink += s;
}

// ch40: throw+catch 单次代价
double throw_cost_ns(int K, int R) {
    double best = 1e18;
    for (int r = 0; r < R; ++r) {
        auto a = std::chrono::steady_clock::now();
        for (int i = 0; i < K; ++i) {
            try { throw i; } catch (int& e) { g_sink += e; }
        }
        auto b = std::chrono::steady_clock::now();
        double ns = std::chrono::duration<double, std::nano>(b - a).count() / K;
        if (ns < best) best = ns;
    }
    return best;
}

struct BufN { int* p; BufN(){ p=new int[64]; } BufN(const BufN& o){ p=new int[64]; std::memcpy(p,o.p,256); } BufN(BufN&& o) noexcept { p=o.p; o.p=nullptr; } ~BufN(){ delete[] p; } };
struct BufT { int* p; BufT(){ p=new int[64]; } BufT(const BufT& o){ p=new int[64]; std::memcpy(p,o.p,256); } BufT(BufT&& o){ p=o.p; o.p=nullptr; } ~BufT(){ delete[] p; } };

double build_buf(bool noexcept_move, int N, int R) {
    double best = 1e18;
    for (int r = 0; r < R; ++r) {
        std::vector<BufN> vn; std::vector<BufT> vt;
        auto a = std::chrono::steady_clock::now();
        if (noexcept_move) { vn.reserve(1); for (int i=0;i<N;++i) vn.push_back(BufN()); }
        else               { vt.reserve(1); for (int i=0;i<N;++i) vt.push_back(BufT()); }
        auto b = std::chrono::steady_clock::now();
        double ms = std::chrono::duration<double, std::milli>(b - a).count();
        if (ms < best) best = ms;
    }
    return best;
}

int main() {
    const int N = 1'000'000, R = 10;
    double vec = ms_of(f_vec, N, R);
    double lst = ms_of(f_lst, N, R);
    std::cout << "vector traversal (" << N << " int): " << vec << " ms\n";
    std::cout << "list   traversal (" << N << " int): " << lst << " ms  (ratio " << (lst/vec) << "x)\n";

    double thr = throw_cost_ns(2'000'000, 12);
    std::cout << "throw+catch single: " << thr << " ns\n";

    double nN = build_buf(true, 50000, 8);
    double nT = build_buf(false, 50000, 8);
    std::cout << "build vector<Buf> N=50000  noexcept-move: " << nN << " ms ; throwing-move: " << nT
              << " ms  (ratio " << (nT/nN) << "x)\n";
    return 0;
}

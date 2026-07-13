#include <vector>
#include <chrono>
#include <cstdio>

// ⑤ 真实基准：只访问单个字段时，SoA 的缓存密度优势
struct EnemyAoS { float hp; float x, y; int kind; bool alive; };
struct EnemySoA {
    std::vector<float> hp;
    std::vector<float> x, y;
    std::vector<int>   kind;
    std::vector<char>  alive;
};

static const int N = 2'000'000;
static const int REPEAT = 50;

long bench_aos(double& secs) {
    std::vector<EnemyAoS> e(N);
    for (int i = 0; i < N; ++i) { e[i].hp = 1.0f; e[i].alive = (i % 3) != 0; }
    long c = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int r = 0; r < REPEAT; ++r)
        for (int i = 0; i < N; ++i)
            if (e[i].alive) c += static_cast<long>(e[i].hp);
    auto t1 = std::chrono::steady_clock::now();
    secs = std::chrono::duration<double>(t1 - t0).count();
    return c;   // 结果被消费，编译器无法消除循环
}

long bench_soa(double& secs) {
    EnemySoA e; e.hp.assign(N, 1.0f); e.alive.resize(N);
    for (int i = 0; i < N; ++i) e.alive[i] = (i % 3) != 0;
    long c = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int r = 0; r < REPEAT; ++r)
        for (int i = 0; i < N; ++i)
            if (e.alive[i]) c += static_cast<long>(e.hp[i]);
    auto t1 = std::chrono::steady_clock::now();
    secs = std::chrono::duration<double>(t1 - t0).count();
    return c;
}

int main() {
    double ta, ts;
    long ca = bench_aos(ta);
    long cs = bench_soa(ts);
    std::printf("AoS count(alive)+hp : %.4f s  (c=%ld)\n", ta, ca);
    std::printf("SoA count(alive)+hp : %.4f s  (c=%ld)\n", ts, cs);
    return 0;
}

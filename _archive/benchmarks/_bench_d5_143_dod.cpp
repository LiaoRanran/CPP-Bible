// _bench_d5_143_dod.cpp — ch143 面向数据设计：AoS vs SoA 的内存流量差
// g++ -O2 -std=c++23
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <vector>
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
volatile double g_dsink;

// AoS：一个实体的全部字段连续（64B = 整缓存行）
struct Particle {
    float x, y, z, mass;
    float vx, vy, vz, charge;
    float ax, ay, az, life;
    float r, g, b, a;
};
// SoA：每个字段独立数组
struct ParticlesSoA {
    std::vector<float> x, y, z, mass, vx, vy, vz, charge,
                       ax, ay, az, life, r, g, b, a;
};

int main() {
    constexpr std::size_t N = 4'000'000;
    constexpr int REPS = 20;
    constexpr float DT = 0.016f;
    std::printf("sizeof(Particle)=%zu\n", sizeof(Particle));

    std::mt19937 rng(42);
    std::uniform_real_distribution<float> d(0.0f, 1.0f);
    std::vector<Particle> aos(N);
    ParticlesSoA soa;
    for (auto* v : {&soa.x, &soa.y, &soa.z, &soa.mass, &soa.vx, &soa.vy, &soa.vz,
                    &soa.charge, &soa.ax, &soa.ay, &soa.az, &soa.life,
                    &soa.r, &soa.g, &soa.b, &soa.a}) v->resize(N);
    for (std::size_t i = 0; i < N; ++i) {
        float px = d(rng), vx = d(rng);
        aos[i].x = px; aos[i].vx = vx;
        aos[i].y = aos[i].z = aos[i].mass = 1.0f;
        soa.x[i] = px; soa.vx[i] = vx;
    }

    // 1) 部分字段更新：只动 x/vx（每实体只需 8B，AoS 却拖入 64B 整行）
    bench("partial update AoS (x+=vx*dt)", [&] {
        for (int r = 0; r < REPS; ++r)
            for (std::size_t i = 0; i < N; ++i)
                aos[i].x += aos[i].vx * DT;
        g_dsink = aos[N / 2].x;
    });
    bench("partial update SoA (x+=vx*dt)", [&] {
        for (int r = 0; r < REPS; ++r)
            for (std::size_t i = 0; i < N; ++i)
                soa.x[i] += soa.vx[i] * DT;
        g_dsink = soa.x[N / 2];
    });

    // 2) 单字段归约：sum(x)
    bench("reduce AoS sum(x)", [&] {
        double s = 0;
        for (int r = 0; r < REPS; ++r)
            for (std::size_t i = 0; i < N; ++i) s += aos[i].x;
        g_dsink = s;
    });
    bench("reduce SoA sum(x)", [&] {
        double s = 0;
        for (int r = 0; r < REPS; ++r)
            for (std::size_t i = 0; i < N; ++i) s += soa.x[i];
        g_dsink = s;
    });

    // 3) 全字段更新：位置三轴 += 速度三轴（触碰大部分行，差距应收窄）
    bench("full update AoS (xyz+=v*dt)", [&] {
        for (int r = 0; r < REPS; ++r)
            for (std::size_t i = 0; i < N; ++i) {
                aos[i].x += aos[i].vx * DT;
                aos[i].y += aos[i].vy * DT;
                aos[i].z += aos[i].vz * DT;
            }
        g_dsink = aos[N / 2].y;
    });
    bench("full update SoA (xyz+=v*dt)", [&] {
        for (int r = 0; r < REPS; ++r)
            for (std::size_t i = 0; i < N; ++i) {
                soa.x[i] += soa.vx[i] * DT;
                soa.y[i] += soa.vy[i] * DT;
                soa.z[i] += soa.vz[i] * DT;
            }
        g_dsink = soa.y[N / 2];
    });
    return 0;
}

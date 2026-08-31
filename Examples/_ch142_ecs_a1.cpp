#include <iostream>
#include <cstdint>
#include <vector>
#include <cassert>
#include <cstddef>

// ── 组件定义（纯数据，trivially copyable） ──
struct Position { float x, y, z; };
struct Velocity { float vx, vy, vz; };
struct Health   { int hp; int max_hp; };
struct Render   { std::uint32_t mesh_id; std::uint32_t material_id; };

// ── Archetype 存储：每个组件类型一个独立连续数组（SoA） ──
struct ArchetypeStorage {
    std::vector<Position> pos;
    std::vector<Velocity> vel;
    std::size_t count = 0;
    void resize(std::size_t n) { pos.resize(n); vel.resize(n); count = n; }
};

// ── Naive AoS：每实体一个堆对象，所有组件打包 ──
struct NaiveEntity {
    Position pos;
    Velocity vel;
    Health   hp;
    Render   rend;
};

// ── volatile sink 防止 DCE ──
static volatile double g_sink = 0.0;

int main() {
    constexpr std::size_t N = 100'000;

    // 1) Archetype (SoA)：Position 和 Velocity 各自连续存储
    ArchetypeStorage arch;
    arch.resize(N);
    for (std::size_t i = 0; i < N; ++i) {
        arch.pos[i] = { (float)i, (float)(i * 2), (float)(i * 3) };
        arch.vel[i] = { 0.1f, 0.2f, 0.3f };
    }

    // 2) Naive AoS：每实体一个堆对象（含未使用的 Health/Render）
    std::vector<NaiveEntity*> naive(N);
    for (std::size_t i = 0; i < N; ++i) {
        naive[i] = new NaiveEntity();
        naive[i]->pos = { (float)i, (float)(i * 2), (float)(i * 3) };
        naive[i]->vel = { 0.1f, 0.2f, 0.3f };
        naive[i]->hp  = { 100, 100 };
        naive[i]->rend = { (std::uint32_t)i, (std::uint32_t)(i + 1) };
    }

    // 3) 遍历 Archetype：只碰 Position+Velocity 两列连续数组
    double sink_a = 0;
    for (std::size_t i = 0; i < arch.count; ++i) {
        arch.pos[i].x += arch.vel[i].vx;
        arch.pos[i].y += arch.vel[i].vy;
        arch.pos[i].z += arch.vel[i].vz;
        sink_a += arch.pos[i].x;
    }
    g_sink += sink_a;

    // 4) 遍历 Naive AoS：每步跨 40 字节结构体，缓存行含无用 Health/Render
    double sink_b = 0;
    for (auto* e : naive) {
        e->pos.x += e->vel.vx;
        e->pos.y += e->vel.vy;
        e->pos.z += e->vel.vz;
        sink_b += e->pos.x;
    }
    g_sink += sink_b;

    // 5) 单组件查询演示：只遍历 Position 列，不碰 Velocity
    double sink_c = 0;
    for (std::size_t i = 0; i < arch.count; ++i) {
        sink_c += arch.pos[i].x;
    }
    g_sink += sink_c;

    // 功能正确性断言（不断言时间/倍数）
    assert(arch.count == N);
    assert(naive.size() == N);
    assert(arch.pos[0].x > 0);  // 数据已写入且被触碰
    assert(naive[0]->pos.x > 0);

    // 清理
    for (auto* e : naive) delete e;

    std::cout << "archetype entities : " << arch.count << std::endl;
    std::cout << "naive entities     : " << naive.size() << std::endl;
    std::cout << "sink (arch+naive)  : " << (sink_a + sink_b) << std::endl;
    std::cout << "sink (pos-only)    : " << sink_c << std::endl;
    std::cout << "all assertions passed" << std::endl;
    return 0;
}
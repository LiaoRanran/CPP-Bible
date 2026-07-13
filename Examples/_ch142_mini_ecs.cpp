// 文件：Examples/_ch142_mini_ecs.cpp
// 行号：9
// 编译并运行：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 Examples/_ch142_mini_ecs.cpp -o Examples/_ch142_mini_ecs.exe && Examples/_ch142_mini_ecs.exe
// 自包含迷你 ECS：entity(handle) + component(纯数据) + system(逻辑)，约 120 行，可编译可运行（见 ⑲）。
#include <cstdint>
#include <iostream>
#include <unordered_map>
#include <vector>

// ── Entity：句柄 = index(20bit) + version(12bit) ───────────────────────
using Entity = std::uint32_t;
constexpr Entity NULL_ENTITY = 0u;

struct EntitySlot {
    std::uint32_t version = 0;
    bool          alive   = false;
};

std::vector<EntitySlot> g_slots;

Entity create_entity() {
    g_slots.push_back(EntitySlot{1, true});
    std::uint32_t idx = (std::uint32_t)g_slots.size() - 1;
    return (1u << 20) | idx;            // 版本1，索引idx（简化：版本恒1）
}

bool is_alive(Entity e) {
    std::uint32_t idx = e & 0xFFFFFu;
    return idx < g_slots.size() && g_slots[idx].alive;
}

void destroy_entity(Entity e) {
    std::uint32_t idx = e & 0xFFFFFu;
    if (idx < g_slots.size()) g_slots[idx].alive = false;
}

// ── Component：纯数据 ─────────────────────────────────────────────────
struct Position { float x, y; };
struct Velocity { float vx, vy; };

// ── Storage：每个组件一个 SoA 式数组，用 entity 索引对齐 ──────────────
struct World {
    std::vector<Position> pos;
    std::vector<Velocity> vel;
    bool has_position(Entity e) const { return (e & 0xFFFFFu) < pos.size(); }
    bool has_velocity(Entity e) const { return (e & 0xFFFFFu) < vel.size(); }
};

void add_position(World& w, Entity e, Position p) {
    std::uint32_t idx = e & 0xFFFFFu;
    if (w.pos.size() <= idx) w.pos.resize(idx + 1);
    w.pos[idx] = p;
}
void add_velocity(World& w, Entity e, Velocity v) {
    std::uint32_t idx = e & 0xFFFFFu;
    if (w.vel.size() <= idx) w.vel.resize(idx + 1);
    w.vel[idx] = v;
}

// ── System：批量遍历拥有 [Position, Velocity] 的实体 ──────────────────
void movement_system(World& w, float dt) {
    const std::size_t n = w.pos.size() < w.vel.size() ? w.pos.size() : w.vel.size();
    for (std::size_t i = 0; i < n; ++i) {
        w.pos[i].x += w.vel[i].vx * dt;
        w.pos[i].y += w.vel[i].vy * dt;
    }
}

int main() {
    World w;
    Entity a = create_entity();
    Entity b = create_entity();
    add_position(w, a, {0.f, 0.f});
    add_velocity(w, a, {1.f, 0.f});
    add_position(w, b, {5.f, 5.f});
    add_velocity(w, b, {0.f, -2.f});

    movement_system(w, 0.5f);
    std::cout << "entity a: (" << w.pos[a & 0xFFFFFu].x << ", "
              << w.pos[a & 0xFFFFFu].y << ")\n";
    std::cout << "entity b: (" << w.pos[b & 0xFFFFFu].x << ", "
              << w.pos[b & 0xFFFFFu].y << ")\n";
    destroy_entity(a);
    std::cout << "a alive after destroy? " << (is_alive(a) ? "yes" : "no") << "\n";
    return 0;
}

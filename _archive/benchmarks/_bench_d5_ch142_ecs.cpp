// _bench_d5_ch142_ecs.cpp
// D5 benchmark for ch142 ECS: data layout impact on traversal performance.
// GCC 15.3.0 -O2 -std=c++23, AMD Ryzen 9 7940HX, 5 rounds median.
//
// Scenarios:
//   S1: Archetype-based (SoA) vs Naive (AoS heap objects) traversal
//   S2: Dense (SoA contiguous) vs Sparse (AoS pointer-chase) traversal
//   S3: Single-component query (Position only) vs full-entity traversal
//   S4: ECS entity->component indirection vs direct array index
//   S5: Component add/remove: archetype migration vs in-place flag toggle

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <random>
#include <vector>

// ── Timing helpers ──────────────────────────────────────────────
static volatile double g_sink = 0.0;

template <typename F>
static double run_bench(F&& fn, int rounds) {
    std::vector<double> times;
    times.reserve(rounds);
    for (int r = 0; r < rounds; ++r) {
        auto t0 = std::chrono::steady_clock::now();
        fn();
        auto t1 = std::chrono::steady_clock::now();
        double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
        times.push_back(ms);
    }
    std::sort(times.begin(), times.end());
    return times[rounds / 2]; // median
}

// ── Components ──────────────────────────────────────────────────
struct Position { float x, y, z; };
struct Velocity { float vx, vy, vz; };
struct Health   { int hp; int max_hp; };
struct Render   { std::uint32_t mesh_id; std::uint32_t material_id; };

// ── S1: Archetype (SoA) vs Naive (AoS heap) ─────────────────────
// Archetype: Position and Velocity stored in separate contiguous arrays.
struct ArchetypeStorage {
    std::vector<Position>  pos;
    std::vector<Velocity>  vel;
    std::size_t count = 0;
    void resize(std::size_t n) {
        pos.resize(n);
        vel.resize(n);
        count = n;
    }
};

// Naive: each entity is a heap-allocated object with all components packed.
struct NaiveEntity {
    Position pos;
    Velocity vel;
    Health   hp;
    Render   rend;
};

static double bench_archetype_traverse(ArchetypeStorage& arch, float dt) {
    double sink = 0;
    for (std::size_t i = 0; i < arch.count; ++i) {
        arch.pos[i].x += arch.vel[i].vx * dt;
        arch.pos[i].y += arch.vel[i].vy * dt;
        arch.pos[i].z += arch.vel[i].vz * dt;
        sink += arch.pos[i].x;
    }
    g_sink += sink;
    return 0; // timing done by run_bench
}

static double bench_naive_traverse(std::vector<NaiveEntity*>& entities, float dt) {
    double sink = 0;
    for (auto* e : entities) {
        e->pos.x += e->vel.vx * dt;
        e->pos.y += e->vel.vy * dt;
        e->pos.z += e->vel.vz * dt;
        sink += e->pos.x;
    }
    g_sink += sink;
    return 0;
}

// ── S2: Dense (SoA contiguous) vs Sparse (AoS pointer-chase) ────
// Dense: all N entities have Position in one contiguous array.
// Sparse: only ~10% of entities have Position, stored as pointers in a vector
//         (simulates pointer-chasing through scattered heap objects).

static double bench_dense_traverse(std::vector<Position>& dense) {
    double sink = 0;
    for (auto& p : dense) {
        p.x += 0.001f;
        p.y += 0.002f;
        p.z += 0.003f;
        sink += p.x;
    }
    g_sink += sink;
    return 0;
}

static double bench_sparse_traverse(std::vector<Position*>& sparse) {
    double sink = 0;
    for (auto* p : sparse) {
        p->x += 0.001f;
        p->y += 0.002f;
        p->z += 0.003f;
        sink += p->x;
    }
    g_sink += sink;
    return 0;
}

// ── S3: Single-component query vs full-entity traversal ─────────
// In an Archetype ECS, querying [Position] only touches the Position array.
// Full-entity traversal touches Position + Velocity + Health + Render.

struct FullEntitySoA {
    std::vector<Position>  pos;
    std::vector<Velocity>  vel;
    std::vector<Health>    hp;
    std::vector<Render>    rend;
    std::size_t count = 0;
    void resize(std::size_t n) {
        pos.resize(n);
        vel.resize(n);
        hp.resize(n);
        rend.resize(n);
        count = n;
    }
};

static double bench_single_component(FullEntitySoA& esoa) {
    // Only touch Position array — other arrays cold
    double sink = 0;
    for (std::size_t i = 0; i < esoa.count; ++i) {
        esoa.pos[i].x += 0.001f;
        esoa.pos[i].y += 0.002f;
        esoa.pos[i].z += 0.003f;
        sink += esoa.pos[i].x;
    }
    g_sink += sink;
    return 0;
}

static double bench_full_traversal(FullEntitySoA& esoa) {
    // Touch all component arrays — pollutes cache with Health/Render data
    double sink = 0;
    for (std::size_t i = 0; i < esoa.count; ++i) {
        esoa.pos[i].x += esoa.vel[i].vx * 0.001f;
        esoa.pos[i].y += esoa.vel[i].vy * 0.001f;
        esoa.pos[i].z += esoa.vel[i].vz * 0.001f;
        esoa.hp[i].hp -= 1;
        esoa.rend[i].mesh_id ^= (esoa.hp[i].hp & 1);
        sink += esoa.pos[i].x + (float)esoa.hp[i].hp;
    }
    g_sink += sink;
    return 0;
}

// ── S4: ECS entity->component indirection vs direct array ───────
// ECS indirection: entity_id -> entity_row -> archetype -> component pointer
// Direct: just index into a flat array with entity_id

struct ECSRegistry {
    // entity_id maps to row in the archetype
    std::vector<std::uint32_t> entity_to_row;   // entity -> row index
    std::vector<std::uint32_t> row_to_entity;   // row -> entity
    std::vector<Position>     pos_data;
    std::size_t count = 0;
    void resize(std::size_t n) {
        entity_to_row.resize(n);
        row_to_entity.resize(n);
        pos_data.resize(n);
        count = n;
        for (std::size_t i = 0; i < n; ++i) {
            entity_to_row[i] = (std::uint32_t)i;
            row_to_entity[i] = (std::uint32_t)i;
        }
    }
};

static double bench_ecs_indirection(ECSRegistry& reg) {
    // Indirection: for each entity, look up its row, then access component
    double sink = 0;
    for (std::size_t e = 0; e < reg.count; ++e) {
        std::uint32_t row = reg.entity_to_row[e];
        reg.pos_data[row].x += 0.001f;
        reg.pos_data[row].y += 0.002f;
        reg.pos_data[row].z += 0.003f;
        sink += reg.pos_data[row].x;
    }
    g_sink += sink;
    return 0;
}

static double bench_direct_array(std::vector<Position>& direct) {
    // Direct: just index with the loop counter, no indirection
    double sink = 0;
    for (std::size_t i = 0; i < direct.size(); ++i) {
        direct[i].x += 0.001f;
        direct[i].y += 0.002f;
        direct[i].z += 0.003f;
        sink += direct[i].x;
    }
    g_sink += sink;
    return 0;
}

// ── S5: Component add/remove: archetype migration vs in-place flag ─
// Archetype migration: move entity data from one archetype array to another
// In-place: just toggle a bit/flag in a bitset

struct ArchetypeA { // [Position, Velocity]
    std::vector<Position> pos;
    std::vector<Velocity> vel;
    std::size_t count = 0;
};

struct ArchetypeB { // [Position, Velocity, Health]
    std::vector<Position> pos;
    std::vector<Velocity> vel;
    std::vector<Health>   hp;
    std::size_t count = 0;
};

static double bench_archetype_migration(ArchetypeA& src, ArchetypeB& dst,
                                         std::size_t n_migrate) {
    // Migrate n_migrate entities from A to B: copy components, add Health
    std::size_t to_migrate = std::min(n_migrate, src.count);
    for (std::size_t i = 0; i < to_migrate; ++i) {
        std::size_t dst_idx = dst.count;
        if (dst_idx >= dst.pos.size()) {
            dst.pos.resize(dst.pos.size() + 1024);
            dst.vel.resize(dst.vel.size() + 1024);
            dst.hp.resize(dst.hp.size() + 1024);
        }
        dst.pos[dst_idx] = src.pos[i];
        dst.vel[dst_idx] = src.vel[i];
        dst.hp[dst_idx] = {100, 100};
        dst.count++;
    }
    // Migrate back (for fairness, restore state)
    for (std::size_t i = 0; i < to_migrate; ++i) {
        dst.count--;
    }
    g_sink += (double)dst.count;
    return 0;
}

static double bench_inplace_flag_toggle(std::vector<std::uint8_t>& flags,
                                         std::size_t n_toggle) {
    // In-place: just toggle a flag, no data movement
    std::size_t to_toggle = std::min(n_toggle, flags.size());
    for (std::size_t i = 0; i < to_toggle; ++i) {
        flags[i] ^= 1; // toggle has_health flag
    }
    g_sink += (double)flags[0];
    return 0;
}

// ── Main ────────────────────────────────────────────────────────
int main() {
    constexpr int ROUNDS = 5;
    constexpr std::size_t N = 500'000;  // 500K entities
    constexpr float DT = 0.016f;        // ~60fps frame time

    std::printf("=== D5 Benchmark: ECS Data Layout Performance ===\n");
    std::printf("Entities: %zu, Rounds: %d (median)\n\n", N, ROUNDS);

    // ── S1: Archetype vs Naive ──────────────────────────────────
    {
        ArchetypeStorage arch;
        arch.resize(N);
        // Initialize with non-trivial data
        for (std::size_t i = 0; i < N; ++i) {
            arch.pos[i] = {(float)i, (float)(i*2), (float)(i*3)};
            arch.vel[i] = {0.1f, 0.2f, 0.3f};
        }

        std::vector<NaiveEntity*> naive(N);
        for (std::size_t i = 0; i < N; ++i) {
            naive[i] = new NaiveEntity();
            naive[i]->pos = {(float)i, (float)(i*2), (float)(i*3)};
            naive[i]->vel = {0.1f, 0.2f, 0.3f};
            naive[i]->hp = {100, 100};
            naive[i]->rend = {(std::uint32_t)i, (std::uint32_t)(i+1)};
        }

        double t_arch = run_bench([&](){ bench_archetype_traverse(arch, DT); }, ROUNDS);
        double t_naive = run_bench([&](){ bench_naive_traverse(naive, DT); }, ROUNDS);

        std::printf("[S1] Archetype (SoA) vs Naive (AoS heap) — movement system\n");
        std::printf("     Archetype : %.3f ms\n", t_arch);
        std::printf("     Naive AoS : %.3f ms\n", t_naive);
        std::printf("     Ratio     : %.2fx\n\n", t_naive / t_arch);

        for (auto* e : naive) delete e;
    }

    // ── S2: Dense vs Sparse ─────────────────────────────────────
    {
        // Dense: N positions in one contiguous vector
        std::vector<Position> dense(N);
        for (std::size_t i = 0; i < N; ++i) {
            dense[i] = {(float)i, (float)(i*2), (float)(i*3)};
        }

        // Sparse: N positions scattered on heap, collected as pointers
        // Simulates AoS pointer-chasing through non-contiguous objects
        std::vector<Position*> sparse(N);
        for (std::size_t i = 0; i < N; ++i) {
            sparse[i] = new Position{(float)i, (float)(i*2), (float)(i*3)};
        }

        double t_dense = run_bench([&](){ bench_dense_traverse(dense); }, ROUNDS);
        double t_sparse = run_bench([&](){ bench_sparse_traverse(sparse); }, ROUNDS);

        std::printf("[S2] Dense (SoA contiguous) vs Sparse (AoS pointer-chase)\n");
        std::printf("     Dense  : %.3f ms\n", t_dense);
        std::printf("     Sparse : %.3f ms\n", t_sparse);
        std::printf("     Ratio  : %.2fx\n\n", t_sparse / t_dense);

        for (auto* p : sparse) delete p;
    }

    // ── S3: Single-component query vs full traversal ────────────
    {
        FullEntitySoA esoa;
        esoa.resize(N);
        for (std::size_t i = 0; i < N; ++i) {
            esoa.pos[i] = {(float)i, (float)(i*2), (float)(i*3)};
            esoa.vel[i] = {0.1f, 0.2f, 0.3f};
            esoa.hp[i] = {100, 100};
            esoa.rend[i] = {(std::uint32_t)i, (std::uint32_t)(i+1)};
        }

        double t_single = run_bench([&](){ bench_single_component(esoa); }, ROUNDS);
        double t_full = run_bench([&](){ bench_full_traversal(esoa); }, ROUNDS);

        std::printf("[S3] Single-component query (Position) vs full traversal (Pos+Vel+HP+Render)\n");
        std::printf("     Single-comp : %.3f ms\n", t_single);
        std::printf("     Full        : %.3f ms\n", t_full);
        std::printf("     Ratio       : %.2fx\n\n", t_full / t_single);
    }

    // ── S4: ECS indirection vs direct array ─────────────────────
    {
        ECSRegistry reg;
        reg.resize(N);
        for (std::size_t i = 0; i < N; ++i) {
            reg.pos_data[i] = {(float)i, (float)(i*2), (float)(i*3)};
        }

        // Shuffle the entity_to_row mapping to simulate realistic indirection
        std::mt19937 rng(42);
        std::vector<std::uint32_t> perm(N);
        for (std::size_t i = 0; i < N; ++i) perm[i] = (std::uint32_t)i;
        std::shuffle(perm.begin(), perm.end(), rng);
        for (std::size_t i = 0; i < N; ++i) {
            reg.entity_to_row[i] = perm[i];
            reg.row_to_entity[perm[i]] = (std::uint32_t)i;
        }

        std::vector<Position> direct(N);
        for (std::size_t i = 0; i < N; ++i) {
            direct[i] = {(float)i, (float)(i*2), (float)(i*3)};
        }

        double t_ecs = run_bench([&](){ bench_ecs_indirection(reg); }, ROUNDS);
        double t_direct = run_bench([&](){ bench_direct_array(direct); }, ROUNDS);

        std::printf("[S4] ECS entity->component indirection vs direct array index\n");
        std::printf("     ECS indirection : %.3f ms\n", t_ecs);
        std::printf("     Direct array   : %.3f ms\n", t_direct);
        std::printf("     Ratio          : %.2fx\n\n", t_ecs / t_direct);
    }

    // ── S5: Archetype migration vs in-place flag toggle ─────────
    {
        constexpr std::size_t N_MIGRATE = 50'000;  // 50K entities to migrate

        ArchetypeA srcA;
        ArchetypeB dstB;
        srcA.pos.resize(N_MIGRATE + 1024);
        srcA.vel.resize(N_MIGRATE + 1024);
        srcA.count = N_MIGRATE;
        dstB.pos.resize(1024);
        dstB.vel.resize(1024);
        dstB.hp.resize(1024);
        dstB.count = 0;

        for (std::size_t i = 0; i < N_MIGRATE; ++i) {
            srcA.pos[i] = {(float)i, (float)(i*2), (float)(i*3)};
            srcA.vel[i] = {0.1f, 0.2f, 0.3f};
        }

        std::vector<std::uint8_t> flags(N_MIGRATE, 0);

        double t_migrate = run_bench([&](){
            // Reset dst for each round
            dstB.count = 0;
            bench_archetype_migration(srcA, dstB, N_MIGRATE);
        }, ROUNDS);

        double t_flag = run_bench([&](){
            bench_inplace_flag_toggle(flags, N_MIGRATE);
        }, ROUNDS);

        std::printf("[S5] Component add/remove: archetype migration vs in-place flag\n");
        std::printf("     Migrate %zu entities : %.3f ms\n", N_MIGRATE, t_migrate);
        std::printf("     Flag toggle %zu      : %.3f ms\n", N_MIGRATE, t_flag);
        std::printf("     Ratio                : %.2fx\n\n", t_migrate / t_flag);
    }

    std::printf("(sink: %f)\n", (double)g_sink);
    return 0;
}

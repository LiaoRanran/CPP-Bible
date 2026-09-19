// _bench_d5_ch130_chromium_abseil.cpp
// D5 benchmark: flat hash map (open-addressing) vs std::unordered_map (chaining) vs sorted vector+binary_search
#include <cstdio>
#include <chrono>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <cstring>

volatile int g_sink = 0;

// --- Simple flat hash map (open addressing, linear probing) ---
struct FlatMap {
    static constexpr int CAP = 1 << 16; // 64K slots
    static constexpr int MASK = CAP - 1;
    struct Slot { uint32_t key; int val; bool used; };
    Slot slots[CAP];

    FlatMap() { memset(this, 0, sizeof(*this)); }

    void insert(uint32_t k, int v) {
        uint32_t h = k * 2654435761u; // Knuth multiplicative hash
        int idx = h & MASK;
        while (slots[idx].used && slots[idx].key != k) idx = (idx + 1) & MASK;
        slots[idx].key = k;
        slots[idx].val = v;
        slots[idx].used = true;
    }

    int find(uint32_t k) {
        uint32_t h = k * 2654435761u;
        int idx = h & MASK;
        while (slots[idx].used) {
            if (slots[idx].key == k) return slots[idx].val;
            idx = (idx + 1) & MASK;
        }
        return -1;
    }
};

// --- Pre-populated flat map for lookup benchmark ---
FlatMap g_flat;
std::unordered_map<uint32_t, int> g_umap;
std::vector<std::pair<uint32_t, int>> g_sorted_vec;

void init_maps(int count) {
    g_flat = FlatMap();
    g_umap.clear();
    g_umap.reserve(count);
    g_sorted_vec.clear();
    g_sorted_vec.reserve(count);
    for (int i = 0; i < count; i++) {
        uint32_t key = (uint32_t)(i * 7919 + 1); // spread keys
        g_flat.insert(key, i);
        g_umap[key] = i;
        g_sorted_vec.push_back({key, i});
    }
    std::sort(g_sorted_vec.begin(), g_sorted_vec.end());
}

[[gnu::noinline]] int bench_flatmap(const std::vector<uint32_t>& keys) {
    int acc = 0;
    for (auto k : keys) acc += g_flat.find(k);
    return acc;
}

[[gnu::noinline]] int bench_unordered_map(const std::vector<uint32_t>& keys) {
    int acc = 0;
    for (auto k : keys) {
        auto it = g_umap.find(k);
        acc += (it != g_umap.end()) ? it->second : -1;
    }
    return acc;
}

[[gnu::noinline]] int bench_sorted_vec(const std::vector<uint32_t>& keys) {
    int acc = 0;
    for (auto k : keys) {
        auto it = std::lower_bound(g_sorted_vec.begin(), g_sorted_vec.end(), std::make_pair(k, 0),
            [](const auto& a, const auto& b) { return a.first < b.first; });
        acc += (it != g_sorted_vec.end() && it->first == k) ? it->second : -1;
    }
    return acc;
}

int main() {
    const int MAP_SIZE = 10000;
    const int LOOKUP_COUNT = 100000;
    init_maps(MAP_SIZE);

    // Generate lookup keys (mix of hits and misses)
    std::vector<uint32_t> lookup_keys(LOOKUP_COUNT);
    for (int i = 0; i < LOOKUP_COUNT; i++) {
        lookup_keys[i] = (uint32_t)((i * 7919 + 1) % (MAP_SIZE * 2)); // half miss
    }

    volatile int w = bench_flatmap(lookup_keys);

    struct { const char* name; int (*fn)(const std::vector<uint32_t>&); double median; } tests[] = {
        {"flat hash map (open)", bench_flatmap,        0},
        {"std::unordered_map",   bench_unordered_map,  0},
        {"sorted vec + bsearch", bench_sorted_vec,     0},
    };

    for (auto& t : tests) {
        double times[5];
        for (int trial = 0; trial < 5; trial++) {
            auto s = std::chrono::high_resolution_clock::now();
            volatile int r = t.fn(lookup_keys);
            (void)r;
            auto e = std::chrono::high_resolution_clock::now();
            times[trial] = std::chrono::duration<double, std::milli>(e - s).count();
        }
        for (int i = 0; i < 5; i++)
            for (int j = i+1; j < 5; j++)
                if (times[j] < times[i]) { double tmp = times[i]; times[i] = times[j]; times[j] = tmp; }
        t.median = times[2];
    }

    printf("=== ch130 abseil D5 benchmark (map=%d lookups=%d, 5-trial median) ===\n", MAP_SIZE, LOOKUP_COUNT);
    for (auto& t : tests)
        printf("  %-25s  %8.3f ms  (%5.2fx)\n", t.name, t.median, t.median / tests[0].median);

    g_sink = tests[2].median > 0 ? 1 : 0;
    return 0;
}

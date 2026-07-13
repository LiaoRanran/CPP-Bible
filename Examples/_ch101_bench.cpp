// 文件：Examples/_ch101_bench.cpp
// 行号：1
#include <unordered_map>
#include <chrono>
#include <cstddef>
#include <cstdlib>
#include <cstdio>

struct Entry { int key; int val; bool used; bool deleted; };
struct OAHMap { Entry* slots; size_t cap; size_t size; };

static size_t hash_fn(int k, size_t cap) {
    return ((size_t)(unsigned(k) * 2654435761u)) % cap;
}
static Entry* oah_find(OAHMap* m, int key) {
    size_t h = hash_fn(key, m->cap);
    for (size_t i = 0; i < m->cap; ++i) {
        size_t idx = (h + i) & (m->cap - 1);
        Entry* e = &m->slots[idx];
        if (!e->used) return nullptr;
        if (!e->deleted && e->key == key) return e;
    }
    return nullptr;
}
static void oah_insert(OAHMap* m, int key, int val) {
    size_t h = hash_fn(key, m->cap);
    for (size_t i = 0; i < m->cap; ++i) {
        size_t idx = (h + i) & (m->cap - 1);
        Entry* e = &m->slots[idx];
        if (!e->used || (e->deleted && e->key == key)) {
            e->key = key; e->val = val;
            e->used = true; e->deleted = false;
            ++m->size; return;
        }
    }
}

int main() {
    const int N = 300000;

    // —— 手写开放寻址哈希表 ——
    OAHMap m;
    m.cap = 1u << 19;
    m.size = 0;
    m.slots = (Entry*)std::calloc(m.cap, sizeof(Entry));

    auto t0 = std::chrono::steady_clock::now();
    for (int k = 0; k < N; ++k) oah_insert(&m, k, k);
    volatile long long sum = 0;
    for (int k = 0; k < N; ++k) {
        Entry* e = oah_find(&m, k);
        sum += e ? e->val : -1;
    }
    auto t1 = std::chrono::steady_clock::now();

    // —— std::unordered_map ——
    std::unordered_map<int, int> um;
    um.reserve(N);
    auto t2 = std::chrono::steady_clock::now();
    for (int k = 0; k < N; ++k) um[k] = k;
    for (int k = 0; k < N; ++k) sum += um.find(k)->second;
    auto t3 = std::chrono::steady_clock::now();

    double ms_hand = std::chrono::duration<double, std::milli>(t1 - t0).count();
    double ms_std  = std::chrono::duration<double, std::milli>(t3 - t2).count();
    std::printf("handwritten=%.1f ms  std_unordered=%.1f ms  N=%d  checksum=%lld\n",
                ms_hand, ms_std, N, (long long)sum);
    std::printf("speedup(hand/std)=%.2fx\n", ms_std / ms_hand);
    return 0;
}

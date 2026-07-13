// 文件：Examples/_ch101_open_addressing.cpp
// 行号：1
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <cstdio>

struct Entry {
    int  key;
    int  val;
    bool used;
    bool deleted;
};

struct OAHMap {
    Entry* slots;
    size_t cap;
    size_t size;
};

// 乘性哈希（Knuth）：key * 2^32 黄金比例常数，取模容量
static size_t hash_fn(int k, size_t cap) {
    return ((size_t)(unsigned(k) * 2654435761u)) % cap;
}

// 线性探测查找：在 [0, cap) 内逐个试探槽位
static Entry* oah_find(OAHMap* m, int key) {
    size_t h = hash_fn(key, m->cap);
    for (size_t i = 0; i < m->cap; ++i) {
        size_t idx = (h + i) & (m->cap - 1);   // cap 为 2 的幂，掩码取模
        Entry* e = &m->slots[idx];
        if (!e->used) return nullptr;          // 遇到空槽说明链已断
        if (!e->deleted && e->key == key) return e;
    }
    return nullptr;
}

// 线性探测插入（含墓碑复用）
static void oah_insert(OAHMap* m, int key, int val) {
    size_t h = hash_fn(key, m->cap);
    for (size_t i = 0; i < m->cap; ++i) {
        size_t idx = (h + i) & (m->cap - 1);
        Entry* e = &m->slots[idx];
        if (!e->used || (e->deleted && e->key == key)) {
            e->key = key; e->val = val;
            e->used = true; e->deleted = false;
            ++m->size;
            return;
        }
    }
}

int main() {
    OAHMap m;
    m.cap  = 1u << 16;
    m.size = 0;
    m.slots = (Entry*)std::calloc(m.cap, sizeof(Entry));
    for (int k = 0; k < 10000; ++k) oah_insert(&m, k, k * 2);
    Entry* e = oah_find(&m, 7777);
    std::printf("%d\n", e ? e->val : -1);
    return 0;
}

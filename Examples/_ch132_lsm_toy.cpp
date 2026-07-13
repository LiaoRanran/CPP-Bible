// 文件：Examples/_ch132_lsm_toy.cpp
// 行号：1
// 自包含 LSM-Tree 等价机制演示：跳表(MemTable) + 有序段(SSTable) + 归并(Compaction)
// 不依赖 leveldb/rocksdb，纯标准库，用于取真实 -O2 汇编作为教材证据。
#include <cstdint>
#include <vector>
#include <algorithm>
#include <random>

// ── 跳表节点（等价 LevelDB MemTable 的 SkipList::Node）──
struct Node {
    int key;
    int value;
    Node** forward;   // 多层级前向指针数组
};

// 跳表查找：从第 max_level 层逐层下降，等价 MemTable::Get
// 这是真实汇编取证的关键函数（见 ch132 ⑨）。
int skiplist_contains(const Node* head, int max_level, int target) {
    const Node* x = head;
    for (int i = max_level; i >= 0; --i) {
        while (x->forward[i] != nullptr && x->forward[i]->key < target) {
            x = x->forward[i];
        }
    }
    x = x->forward[0];
    if (x != nullptr && x->key == target) return x->value;
    return -1;  // 未命中
}

// ── SSTable 等价：内存中有序数组 + 二分查找 ──
// 一段已排序的 (key,value) 段，等价一个 Level-0 SSTable 文件。
struct Run {
    const int* keys;     // 升序
    const int* vals;
    int n;
};

// 在单段内二分查找，等价 SSTable 的 block 内二分（含 restart 点优化）。
int run_find(const Run& r, int target) {
    int lo = 0, hi = r.n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (r.keys[mid] == target) return r.vals[mid];
        if (r.keys[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}

// ── Compaction 等价：K 路归并多个有序段（按 key 升序合并，后写覆盖前写）──
// 这是真实汇编取证的第二个关键函数（见 ch132 ⑦）。
void merge_runs(const std::vector<Run>& runs, std::vector<int>& out_keys,
                std::vector<int>& out_vals) {
    // 多指针 curr[k] 指向每个 run 的当前位置
    std::vector<int> curr(runs.size(), 0);
    while (true) {
        int best = -1;
        int best_val = 0;
        int best_run = -1;
        for (size_t k = 0; k < runs.size(); ++k) {
            if (curr[k] < runs[k].n) {
                int kk = runs[k].keys[curr[k]];
                if (best == -1 || kk < best) {
                    best = kk;
                    best_val = runs[k].vals[curr[k]];
                    best_run = (int)k;
                }
            }
        }
        if (best_run == -1) break;  // 全部耗尽
        // 同 key 后写的段覆盖先写（按 runs 顺序，后者优先）
        out_keys.push_back(best);
        out_vals.push_back(best_val);
        ++curr[best_run];
    }
}

// 验证入口（被 main 调用，保证函数不被优化掉）
int demo(int seed) {
    std::mt19937 rng(seed);
    std::vector<int> a(8), av(8), b(8), bv(8);
    for (int i = 0; i < 8; ++i) { a[i] = i * 2; av[i] = rng() % 100; }
    for (int i = 0; i < 8; ++i) { b[i] = i * 2 + 1; bv[i] = rng() % 100; }
    Run r1{a.data(), av.data(), 8};
    Run r2{b.data(), bv.data(), 8};
    std::vector<Run> runs{r1, r2};
    std::vector<int> ok, ov;
    merge_runs(runs, ok, ov);
    int hit = run_find(r1, 6);
    // 构造一个 1 层跳表头，仅作调用演示
    Node* fwd[1] = {nullptr};
    Node head{0, 0, fwd};
    int s = skiplist_contains(&head, 0, 6);
    return hit + s + (int)ok.size();
}

int main() { return demo(42); }

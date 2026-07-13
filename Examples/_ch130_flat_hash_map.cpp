// 自包含开放寻址哈希表（flat_hash_map 的等价机制：连续数组 + 线性探测）
// 展示 Abseil absl::flat_hash_map 的核心思想：无链表、无指针、缓存友好。
#include <cstddef>
#include <cstdint>

template <typename K, typename V, size_t N>
class FlatMap {
    static_assert((N & (N - 1)) == 0, "N 必须为 2 的幂");
    alignas(64) K keys_[N];
    alignas(64) V vals_[N];
    bool used_[N] = {};
public:
    // 线性探测查找（返回指向 value 的指针，未命中返回 nullptr）
    const V* find(K k) const {
        const size_t mask = N - 1;
        size_t i = (size_t)(uintptr_t)k & mask;   // 简易哈希
        for (;;) {
            if (!used_[i]) return nullptr;
            if (keys_[i] == k) return &vals_[i];
            i = (i + 1) & mask;
        }
    }
    // 插入（假设 key 不存在；简化版不处理扩容）
    void insert(K k, V v) {
        const size_t mask = N - 1;
        size_t i = (size_t)(uintptr_t)k & mask;
        while (used_[i]) i = (i + 1) & mask;
        keys_[i] = k; vals_[i] = v; used_[i] = true;
    }
};

// 热点：遍历查找偶数 key 并求和（用于观察编译器生成的探测循环汇编）
int sum_even(const FlatMap<int, int, 1024>& m, int n) {
    int s = 0;
    for (int i = 0; i < n; ++i)
        if (auto* p = m.find(i * 2)) s += *p;
    return s;
}

int main() {
    FlatMap<int, int, 1024> m;
    for (int i = 0; i < 512; ++i) m.insert(i * 2, i);
    return sum_even(m, 512);
}

// ch115 move 汇编实证 —— 移动 vs 拷贝的真实指令差异
#include <cstring>
#include <utility>

struct Big {
    char* data;
    size_t sz;
    Big(size_t n) : data(new char[n]), sz(n) {
        std::memset(data, 0, n);
    }
    Big(const Big& other) : data(new char[other.sz]), sz(other.sz) {
        std::memcpy(data, other.data, sz);            // 复制 —— 深拷贝
    }
    Big(Big&& other) noexcept : data(other.data), sz(other.sz) {
        other.data = nullptr; other.sz = 0;           // 移动 —— 指针搬
    }
    ~Big() { delete[] data; }
};

// 观测 1: RVO 下调用方零开销
Big make_big_rvo() {
    return Big(1024);  // RVO → 直接在调用方栈槽构造
}

// 观测 2: std::move 实际 cost
void consume_big(Big b) {
    int sum = 0;
    for (size_t i = 0; i < b.sz; ++i) sum += b.data[i];
}

void move_into_consume(Big&& src) {
    consume_big(std::move(src));  // move 构造 → 只搬 2 个字段
}

// 观测 3: vector<Big> push_back move
#include <vector>
void emplace_vs_push(std::vector<Big>& v) {
    v.emplace_back(512);          // 原地构造
    Big tmp(256);
    v.push_back(std::move(tmp));  // move 进 vector
}

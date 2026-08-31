#include <iostream>
#include <vector>

static inline int op_add(int x) { return x + 7; }
static inline int op_mul(int x) { return x * 3; }

template <int Tag>
long long run_constexpr(std::vector<int> const& v) {
    long long acc = 0;
    for (int x : v) {
        if constexpr (Tag == 0) acc += op_add(x);
        else if constexpr (Tag == 1) acc += op_mul(x);
    }
    return acc;
}

using FnPtr = int (*)(int);
static FnPtr table[2] = { &op_add, &op_mul };

long long run_ptrtable(std::vector<int> const& v, std::vector<int> const& tags) {
    long long acc = 0;
    for (size_t i = 0; i < v.size(); ++i) acc += table[tags[i]](v[i]);
    return acc;
}

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    std::vector<int> tags = {0, 1, 0, 1, 0};
    std::cout << "constexpr=" << run_constexpr<0>(v) + run_constexpr<1>(v)
              << " ptrtable=" << run_ptrtable(v, tags) << std::endl;
    return 0;
}
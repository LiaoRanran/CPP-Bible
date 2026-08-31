#include <iostream>
#include <vector>

enum OpType : int { OP_ADD = 0, OP_MUL = 1 };
static inline int do_add(int x) { return x + 7; }
static inline int do_mul(int x) { return x * 3; }

template <OpType Tag>
long long run_constexpr_route(std::vector<int> const& v) {
    long long acc = 0;
    for (int x : v) {
        if constexpr (Tag == OP_ADD) acc += do_add(x);
        else if constexpr (Tag == OP_MUL) acc += do_mul(x);
    }
    return acc;
}

long long run_ifelse_chain(std::vector<int> const& v, std::vector<int> const& tags) {
    long long acc = 0;
    for (size_t i = 0; i < v.size(); ++i) {
        int x = v[i], t = tags[i];
        if (t == OP_ADD) acc += do_add(x);
        else             acc += do_mul(x);
    }
    return acc;
}

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    std::vector<int> add_v = {1, 3, 5};
    std::vector<int> mul_v = {2, 4};
    std::vector<int> tags = {0, 1, 0, 1, 0};
    std::cout << "constexpr=" << run_constexpr_route<OP_ADD>(add_v) + run_constexpr_route<OP_MUL>(mul_v)
              << " ifelse=" << run_ifelse_chain(v, tags) << std::endl;
    return 0;
}
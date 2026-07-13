// _ch139_constexpr.cpp
// 取证目的：CRTP 链在编译期求值（constexpr）。
#include <iostream>

template <typename Derived>
struct VectorOps {
    constexpr int dot(const Derived& o) const {
        const auto& self = *static_cast<const Derived*>(this);
        int s = 0;
        for (int i = 0; i < Derived::N; ++i) s += self.data[i] * o.data[i];
        return s;
    }
};

template <int N_>
struct Vec : VectorOps<Vec<N_>> {
    static constexpr int N = N_;
    int data[N];
    constexpr Vec(int a, int b, int c) : data{a, b, c} {}
};

int main() {
    constexpr Vec<3> a{1, 2, 3};
    constexpr Vec<3> b{4, 5, 6};
    static_assert(a.dot(b) == 32);  // 1*4 + 2*5 + 3*6 = 32
    std::cout << a.dot(b) << "\n";
}

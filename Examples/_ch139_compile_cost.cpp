// _ch139_compile_cost.cpp
// 取证目的：构造一个「深度 CRTP 模板实例化」场景，用于测量编译时间成本。
// 编译：g++ -std=c++23 -O2 -c -o /dev/null _ch139_compile_cost.cpp （计时）
template <typename Derived>
struct Unit {
    int run() const { return static_cast<const Derived*>(this)->step(); }
};

template <int N>
struct Chain;

template <>
struct Chain<0> : Unit<Chain<0>> {
    int step() const { return 1; }
};

template <int N>
struct Chain : Unit<Chain<N>> {
    int step() const { return 1 + Chain<N - 1>{}.run(); }
};

int main() { return Chain<120>{}.run(); }

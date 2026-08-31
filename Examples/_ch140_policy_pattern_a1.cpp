// ⑮ N 个二元 policy 组合 => C(N,2) 份独立实例化
template <typename P1, typename P2>
struct Combo {
    static int f() { return (int)(sizeof(P1) + sizeof(P2)); }
};
struct A{}; struct B{}; struct C{}; struct D{};
template struct Combo<A,B>;   // 显式实例化
template struct Combo<A,C>;
template struct Combo<A,D>;
template struct Combo<B,C>;
template struct Combo<B,D>;
template struct Combo<C,D>;
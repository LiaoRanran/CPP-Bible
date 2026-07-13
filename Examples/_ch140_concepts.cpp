#include <concepts>
template <typename P>
concept CheckPolicy = requires { P::check(0); };
struct R { static void check(int){} };
template <CheckPolicy P> struct W { void set(int v){ P::check(v); } };
int main(){ W<R> w; w.set(1); return 0; }

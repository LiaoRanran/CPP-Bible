#include <cstdio>
struct Tracer {
    int v;
    Tracer(int x) : v(x) {}
    Tracer(const Tracer& o) : v(o.v) { puts("copy"); }
    Tracer(Tracer&& o) noexcept : v(o.v) { puts("move"); }
};
[[gnu::noinline]] Tracer make_prvalue() { return Tracer(42); }
[[gnu::noinline]] Tracer make_nrvo()    { Tracer t(7); return t; }
struct NoMove { NoMove()=default; NoMove(const NoMove&)=delete; NoMove(NoMove&&)=delete; };
[[gnu::noinline]] NoMove make_nomove() { return NoMove{}; }
int main(){ auto a=make_prvalue(); auto b=make_nrvo(); auto c=make_nomove(); (void)a;(void)b;(void)c; return 0; }

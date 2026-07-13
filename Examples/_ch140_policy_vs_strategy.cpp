#include <cstdio>

// ---- Policy-based (compile-time, zero-cost) ----
template <typename CheckingPolicy>
struct PolicyWidget {
    int value{};
    void set(int v) { CheckingPolicy::check(v); value = v; }
    int  get() const { return value; }
};

struct RangeCheck { static void check(int v) { if (v < 0 || v > 100) std::puts("OOR"); } };
struct NoCheck    { static void check(int)   {} };

// ---- Strategy-based (runtime, virtual dispatch) ----
struct Strategy {
    virtual ~Strategy() = default;
    virtual void check(int) const = 0;
};
struct RangeStrategy : Strategy { void check(int v) const override { if (v < 0 || v > 100) std::puts("OOR"); } };
struct NoneStrategy  : Strategy { void check(int) const override {} };

struct StrategyWidget {
    int value{};
    const Strategy* s;
    StrategyWidget(const Strategy* p) : s(p) {}
    void set(int v) { s->check(v); value = v; }
    int  get() const { return value; }
};

int policy_demo(int x) {
    PolicyWidget<RangeCheck> w;
    w.set(x);
    return w.get();
}
int policy_demo_nocheck(int x) {
    PolicyWidget<NoCheck> w;
    w.set(x);
    return w.get();
}
int strategy_demo(int x, const Strategy* s) {
    StrategyWidget w(s);
    w.set(x);
    return w.get();
}
int main() {
    RangeStrategy rs;
    NoneStrategy  ns;
    return policy_demo(42) + policy_demo_nocheck(7)
         + strategy_demo(42, &rs) + strategy_demo(7, &ns);
}

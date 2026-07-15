// ASM-88-variant: std::variant + std::visit 的类型索引分派 —— GCC 15.3.0 真机实证
// 重点：std::visit 的底层是「按 index 跳表」而非虚函数 vtable 间接调用。
#include <variant>
#include <cstdint>

struct A { int x; int compute() const { return x; } };
struct B { int x; int compute() const { return x * 2; } };
struct C { int x; int compute() const { return x * 3; } };
using V = std::variant<A, B, C>;

// 访问者：对每个备选类型调用 compute()
[[gnu::noinline]] int dispatch_visit(const V& v) {
    return std::visit([](const auto& e) -> int { return e.compute(); }, v);
}

// 对照：手写 index 分派（编译器同样生成跳表，用于对比 std::visit）
[[gnu::noinline]] int dispatch_manual(const V& v) {
    switch (v.index()) {
        case 0: return std::get<0>(v).compute();
        case 1: return std::get<1>(v).compute();
        case 2: return std::get<2>(v).compute();
    }
    return 0;
}

int main() {
    V v = A{7};
    volatile int sink = 0;
    sink = dispatch_visit(v);
    sink = dispatch_manual(v);
    return sink;
}

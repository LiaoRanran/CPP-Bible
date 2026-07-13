// _ch138_variant_opaque.cpp
// 第138章 ⑲ 辅助：当 variant 的判别值来自外部（不可在编译期确定）时，
// std::visit 在 -O2 下生成的真实跳转表（jump table）取证。
#include <variant>

struct VAdd { int eval() const { return 1; } };
struct VSub { int eval() const { return 2; } };
using Arith = std::variant<VAdd, VSub>;

// 判别值经 opaque 传入，优化器无法静态确定
int via_variant_opaque(const Arith& v) {
    return std::visit([](const auto& x) -> int { return x.eval(); }, v);
}

Arith make_opaque(int which);  // 定义不在此 TU，强制跨 TU，阻止常量折叠

int use(int which) {
    Arith v = make_opaque(which);
    return via_variant_opaque(v);
}

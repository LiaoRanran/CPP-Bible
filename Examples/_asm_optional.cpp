// optional 取证：nullopt 不分配堆，值与 engaged 标志同存储
// 编译：g++ -std=c++23 -O2 -S -masm=intel _asm_optional.cpp -o _asm_optional.asm
#include <optional>
int use_optional() {
    std::optional<int> o = 42;
    std::optional<int> n = std::nullopt;
    return (o.has_value() ? *o : 0) + (n.has_value() ? 1 : 0);
}

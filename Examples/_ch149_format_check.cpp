// ⑫ 格式化门禁：clang-format 风格一致性（此处以可读风格呈现）
#include <cstdio>

namespace calc {
inline int add(int a, int b) { return a + b; }
}  // namespace calc

int main() { std::printf("%d\n", calc::add(1, 2)); }

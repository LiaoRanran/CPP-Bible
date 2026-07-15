// ASM-89-tuple : std::tuple get<N> / 结构化绑定 代价 (GCC 15.3.0, x86-64, -O2)
// 目标：验证 tuple 元素访问是否为编译期偏移(零运行时索引计算)，与裸 struct 成员访问是否逐字节相同。
#include <tuple>
#include <cstddef>

volatile int g_obs;

using T3 = std::tuple<int, double, char>;

// (1) std::get<N>：N 是编译期常量，访问应为直接偏移 mov。
int use_get(const T3& t) {
    return std::get<0>(t) + (int)std::get<1>(t) + std::get<2>(t);
}

// (2) 结构化绑定：应等价于 (1)，编译期把 a/b/c 别名为 t 的对应偏移。
int use_bind(const T3& t) {
    auto& [a, b, c] = t;
    return a + (int)b + c;
}

// (3) 裸聚合 struct 基线。
struct P { int a; double b; char c; };
int use_agg(const P& p) { return p.a + (int)p.b + p.c; }

// (4) 布局：tuple 元素偏移由编译器钉死，sizeof 折叠为立即数。
void emit_size() { g_obs = (int)sizeof(T3); }

int main() {
    T3 t{1, 2.0, 'x'};
    emit_size();
    return use_get(t);
}

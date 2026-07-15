// ASM-88-optional : std::optional 布局与访问代价 (GCC 15.3.0, x86-64, -O2)
// 目标：验证「optional 是零开销包装」的边界——访问本身是否零额外间接？空间代价几何？
#include <optional>
#include <cstddef>

volatile int g_obs;  // 强制 sizeof / 访问结果不被 O2 抹平

// (1) 取值：先判 engaged 标志，再读值。与裸指针判空取址对比。
int get_opt(std::optional<int> o) {
    if (o) return *o;
    return -1;
}
int get_raw(const int* p) {
    if (p) return *p;
    return -1;
}

// (2) 值访问：是否引入二次解引用？对比 has_value() 标志读取。
int opt_use(std::optional<int> o) {
    return *o + (o.has_value() ? 1 : 0);
}

// (3) 布局真相：把各 sizeof 折叠为立即数写 volatile 全局，便于 objdump 直接读数。
void emit_sizes() {
    g_obs = (int)sizeof(std::optional<int>);
    g_obs = (int)sizeof(int);
    g_obs = (int)sizeof(std::optional<long long>);
    g_obs = (int)sizeof(std::optional<char>);
}

int main() {
    std::optional<int> o{42};
    emit_sizes();
    return get_opt(o);
}

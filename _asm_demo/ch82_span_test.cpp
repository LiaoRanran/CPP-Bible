// ASM-82-span : std::span 零成本视图 (GCC 15.3.0, x86-64, -O2)
// 目标：验证 span 是否真的只是 {ptr, size} 对、访问与裸指针等价、operator[] 不检查边界。
#include <span>
#include <cstddef>

volatile int g_obs;

// (1) 范围 for 遍历：与裸指针+长度基线对比，应生成逐字节相同循环。
int sum_span(std::span<const int> s) {
    int t = 0;
    for (int x : s) t += x;
    return t;
}
int sum_ptr(const int* p, std::size_t n) {
    int t = 0;
    for (std::size_t i = 0; i < n; ++i) t += p[i];
    return t;
}

// (2) operator[]：是否带运行时边界检查？(对比 vector::at 会抛)
int at_span(std::span<const int> s, std::size_t i) {
    return s[i];   // 不检查边界
}

// (3) 布局：span 携带 size_t，按值传递拷贝 16 字节。
void emit_size() { g_obs = (int)sizeof(std::span<const int>); }

int main() {
    int a[4] = {1, 2, 3, 4};
    emit_size();
    return sum_span(a);
}

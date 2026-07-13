// 文件：Examples/_ch17_sizeopt.cpp
// 体积优化实证：未引用函数应被 --gc-sections 丢弃。
// 编译对比见正文 ⑭；此处给出可被裁剪的源码。
#include <cstdint>

// 被 main 调用的“在线”函数
uint32_t active(uint32_t x) { return x * 3u + 1u; }

// 死代码：不被任何路径引用，期望被 GC 掉
uint32_t dead(uint32_t x) { return x * x + 12345u; }

// 独立数据段，便于 --gc-sections 丢弃
int used_var = 7;
int unused_var = 99;

int main() {
    volatile uint32_t v = active(11u);
    return (int)(v + (uint32_t)used_var);
}

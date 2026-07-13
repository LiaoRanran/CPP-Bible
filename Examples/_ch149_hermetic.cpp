// 见 Examples/_ch149_hermetic.cpp
// ② 封闭构建：固定依赖来源，避免宿主机污染（仅打印声明）
#include <cstdio>
int main() {
    std::printf("hermetic: pinned deps from mirror, no network to pypi/npm\n");
    return 0;
}

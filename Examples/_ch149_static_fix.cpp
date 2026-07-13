// 见 Examples/_ch149_static_fix.cpp
// ⑥ 修复后：去掉未用参数，静态门禁通过
#include <cstdio>
int compute(int x) { return x * 2; }
int main() {
    std::printf("compute=%d\n", compute(21));
    return 0;
}

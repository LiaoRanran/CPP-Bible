// ⑧ 覆盖率驱动：故意只覆盖部分分支，演示未覆盖行
#include <cstdio>
int classify(int);
int main() {
    std::printf("classify(5)=%d\n", classify(5));
    std::printf("classify(0)=%d\n", classify(0));
    // 注：classify(-3) 未调用 → 负分支为"未覆盖"
    return 0;
}

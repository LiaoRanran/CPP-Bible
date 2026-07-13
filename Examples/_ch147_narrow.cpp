#include <cstdio>
void sink(double d) { std::printf("%f\n", d); }
int main() {
    int x = 70000;
    sink(x);                    // int->double 安全，但演示 -Wconversion 场景
    double big = 3.9;
    int y = big;                // 浮点到整数：实现定义截断，审查应改显式
    std::printf("%d\n", y);
}

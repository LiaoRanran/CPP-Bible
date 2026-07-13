#include <cstdio>
int compute(int flag) {
    int result;                 // 未初始化
    if (flag > 0) result = 1;
    return result;              // 可能使用未初始化值
}
int main() { std::printf("%d\n", compute(0)); }

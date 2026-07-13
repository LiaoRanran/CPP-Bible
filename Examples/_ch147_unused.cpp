#include <cstdio>
int main() {
    int debug = 42;             // 从未使用
    std::printf("hi\n");
    (void)debug;                // 抑制：仅显式 void 后才用
}

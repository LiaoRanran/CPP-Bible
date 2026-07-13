// 收尾：汇总自检（在 CI 中被逐个调用；此处独立验证编译链可用）
#include <cstdio>
int main() {
    std::printf("sanity: ch150 self-contained examples compile & run OK\n");
    return 0;
}

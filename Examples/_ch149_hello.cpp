// 见 Examples/_ch149_hello.cpp
// ① 最小 CI 冒烟程序：构建通过即说明工具链可用
#include <cstdio>
int main() {
    std::printf("CI pipeline: build OK\n");
    return 0;
}

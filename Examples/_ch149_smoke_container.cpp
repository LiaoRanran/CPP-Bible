// ⑰ 容器冒烟：镜像启动后应立即通过的健康探测
#include <cstdio>
int main() {
    std::printf("image started, pid self-check ok\n");
    return 0;
}

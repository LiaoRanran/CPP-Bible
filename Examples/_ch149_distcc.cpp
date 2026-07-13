// 见 Examples/_ch149_distcc.cpp
// ⑤ 分布式编译：把 .o 的编译派发到编译集群（仅打印说明）
#include <cstdio>
int main() {
    std::printf("distcc: dispatching translation units to 4 hosts\n");
    return 0;
}

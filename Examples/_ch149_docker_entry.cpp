// ⑪ 容器入口：容器化构建后运行的可执行
#include <cstdio>
int main(int argc, char** argv) {
    std::printf("container entry: argc=%d argv0=%s\n",
                argc, argc > 0 ? argv[0] : "");
    return 0;
}

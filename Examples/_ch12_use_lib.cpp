// ⑮ 文件：Examples/_ch12_use_lib.cpp，行号：1
#include <cstdio>
#include "_ch12_mylib.h"

int main() {
    std::printf("%d %d\n", ch12::square(4), ch12::cube(3));
    return 0;
}

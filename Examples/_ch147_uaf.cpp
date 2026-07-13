// _ch147_uaf.cpp —— 悬垂指针 / 释放后使用（UB）
// 取证命令:
//   g++ -std=c++23 -fsanitize=address -g _ch147_uaf.cpp -o /tmp/uaf
#include <cstdio>

int* leak_dangling() {
    int local = 7;
    return &local;        // 返回栈上对象地址：悬垂
}

int main() {
    int* p = leak_dangling();
    std::printf("%d\n", *p);   // UB：访问已销毁栈帧
    return 0;
}

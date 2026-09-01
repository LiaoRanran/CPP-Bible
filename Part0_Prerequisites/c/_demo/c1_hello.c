/* c1_hello.c — C1 示例：一个最小可编译 C 程序（对照 C++） */
/* 编译: gcc -std=c11 -O2 -Wall -Wextra -o c1_hello.exe c1_hello.c */
/* 运行: ./c1_hello.exe */
#include <stdio.h>

int main(void) {
    int nums[5] = {1, 2, 3, 4, 5};
    int sum = 0;
    for (int i = 0; i < 5; ++i) {
        sum += nums[i];
    }
    printf("sum = %d\n", sum);   /* 期望输出 sum = 15 */
    return 0;
}

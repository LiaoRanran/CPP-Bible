/* C3 类型系统演示：sizeof / 整数提升 / 有符号无符号陷阱 / 数组退化 / 浮点精度
 *
 * 复现命令（gcc 为 MinGW GCC 15.3.0）：
 *   gcc -std=c11 -O2 -Wall -Wextra -o c3_types.exe c3_types.c && ./c3_types.exe
 */
#include <stdio.h>

/* 数组作为函数参数：形参 int arr[5] 完全等价于 int *arr，
 * 因此函数内 sizeof(arr) 是指针大小，写 [5] 只是给人看的注释。 */
static void probe(int arr[5]) {
    printf("inside probe: sizeof(arr)=%zu (已退化为指针，[5] 无意义)\n",
           sizeof(arr));
}

int main(void) {
    /* 1. 基本类型尺寸：本机 MinGW = LLP64（long 4 字节，指针 8 字节） */
    printf("== sizeof (LLP64) ==\n");
    printf("char=%zu short=%zu int=%zu long=%zu long long=%zu\n",
           sizeof(char), sizeof(short), sizeof(int),
           sizeof(long), sizeof(long long));
    printf("float=%zu double=%zu void*=%zu size_t=%zu\n",
           sizeof(float), sizeof(double), sizeof(void *), sizeof(size_t));

    /* 2. 整数提升：char 参与运算先提升为 int */
    char c = 100, d = 100;
    printf("\n== integer promotion ==\n");
    printf("sizeof(char)=%zu  sizeof(c+d)=%zu  c+d=%d\n",
           sizeof(char), sizeof(c + d), c + d);

    /* 3. 有符号 / 无符号混用陷阱（-Wextra 会警告 -Wsign-compare） */
    int s = -1;
    unsigned u = 1;
    printf("\n== signed/unsigned trap ==\n");
    printf("-1 < 1u ? %s\n", (s < u) ? "true" : "false");
    printf("(unsigned)(-1) = %u\n", (unsigned)s);

    /* 4. 数组退化：数组名在多数语境退化为首元素指针 */
    int a[5] = {0};
    int *p = a;
    printf("\n== array decay ==\n");
    printf("sizeof(a)=%zu (数组本身)  sizeof(p)=%zu (退化后的指针)\n",
           sizeof(a), sizeof(p));
    probe(a); /* 传数组名进去 → 形参已退化为指针 */

    /* 5. 浮点精度：二进制浮点无法精确表示 0.1 */
    printf("\n== float precision ==\n");
    printf("0.1+0.2 == 0.3 ? %s\n", (0.1 + 0.2 == 0.3) ? "true" : "false");
    printf("0.1+0.2 = %.17g\n", 0.1 + 0.2);

    /* 6. 整数除法截断 */
    printf("\n== integer division ==\n");
    printf("1/2 = %d ; 1.0/2 = %g\n", 1 / 2, 1.0 / 2);

    /* 7. char 的符号性是实现定义的（x86 GCC 默认 signed） */
    signed char sc = 200; /* 200 超出 signed char 范围：实现定义 */
    printf("\n== char signedness (implementation-defined) ==\n");
    printf("(signed char)200 = %d\n", sc);

    return 0;
}

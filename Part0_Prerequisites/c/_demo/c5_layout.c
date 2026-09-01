/* C5 进程内存布局：把五个区域钉在地址上
 *
 * 编译: gcc -std=c11 -O0 -Wall -Wextra -o c5_layout.exe c5_layout.c
 * 连跑两次：绝对地址会变（ASLR），但相对顺序（栈 >> 堆 > data > code）不变。
 */
#include <stdio.h>
#include <stdlib.h>

int g_init = 42;              /* .data：已初始化全局 */
int g_zero;                   /* .bss ：零初始化全局（不占 exe 空间，见 C2） */
static int s_init = 7;        /* .data：静态已初始化 */

int main(void) {
    static int s_zero;        /* .bss ：静态零初始化 */
    int local = 1;            /* 栈   ：自动存储期 */
    char *h1 = malloc(64);    /* 堆   ：自由存储期 */
    char *h2 = malloc(16);

    printf("code  main    = %p\n", (void *)main);
    printf("code  printf  = %p\n", (void *)&printf);
    printf("data  g_init  = %p\n", (void *)&g_init);
    printf("data  s_init  = %p\n", (void *)&s_init);
    printf("bss   g_zero  = %p\n", (void *)&g_zero);
    printf("bss   s_zero  = %p\n", (void *)&s_zero);
    printf("heap  #1      = %p\n", (void *)h1);
    printf("heap  #2      = %p\n", (void *)h2);
    printf("heap  gap     = %ld bytes（= 用户要的 64 + 分配器元数据/对齐）\n",
           (long)(h2 - h1));
    printf("stack &local  = %p\n", (void *)&local);

    free(h1);
    free(h2);
    return 0;
}

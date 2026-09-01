/* C5 事故现场：use-after-free / double-free —— 真实未定义行为演示。
 * 输出因机器/编译器而异，这正是 UB 的定义：任何事都可能发生。
 *
 * 编译: gcc -std=c11 -O0 -o c5_uaf.exe c5_uaf.c
 * ⚠️ 仅作教学演示（[cert:MEM30-C] 生产代码禁止访问已释放内存）。
 */
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *p = malloc(sizeof(int) * 4);
    for (int i = 0; i < 4; ++i) {
        p[i] = i * 10;
    }
    printf("before free : p[0..3] = %d %d %d %d\n", p[0], p[1], p[2], p[3]);
    fflush(stdout);   /* 每个 printf 后强刷：否则进程异常终止时缓冲区丢失 */

    free(p);                       /* 内存归还分配器 */

    /* ---- 以下全是未定义行为，只为演示"UB 不等于必崩" ---- */
    printf("after  free : p[0] = %d（UB：可能原值/被改/崩）\n", *p);
    fflush(stdout);

    int *q = malloc(sizeof(int) * 4);
    printf("new alloc   : q = %p, p = %p（同址即悬垂炸弹）\n", (void *)q, (void *)p);
    fflush(stdout);

    free(q);
    free(p);                       /* double free：又一次 UB */
    printf("survived    : 能打印到此不代表安全——UB 的定义就是'任何事'。\n");
    fflush(stdout);
    return 0;
}

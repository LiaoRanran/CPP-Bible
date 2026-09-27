#include <stdio.h>

static int add2(int a, int b) { return a + b; }

typedef int (*FnVoid)(void);

static void fnptr_probe(void) {
    int (*good)(int, int) = add2;
    FnVoid bad = (FnVoid)add2;           /* 直接强转（不经 void*）：类型不兼容，调用即 UB（本卡不调用） */
    printf("fnptr_sizeof=%zu\n", sizeof good);
    printf("good_call=%d\n", good(2, 3));
    printf("bad_addr_nonzero=%d\n", bad != NULL);
}

int main(void) {
    fnptr_probe();
    return 0;
}

#include <stdio.h>
#include <limits.h>

static void blk_shift(void) {
    unsigned u = 1u; int neg = -1; int r;
    r = (int)(u << 31);                 /* 有符号解释实现定义 */
    printf("shift.u31=%d\n", r);
    printf("shift.neg_shift=%d\n", (neg << 1) == -2 ? 1 : 0);  /* 左移负数是 UB */
}


struct bf_t { unsigned a:3; unsigned b:5; signed c:2; };
static void blk_bitfield(void) {
    struct bf_t v; v.a=5; v.b=21; v.c=-1;
    printf("bitfield.size=%d\n", (int)sizeof(struct bf_t));
    printf("bitfield.a=%d\n", (int)v.a);
    printf("bitfield.c=%d\n", (int)v.c);
}


struct al_t { char c; double d; };
static void blk_alignof_(void) {
    printf("alignof_.size=%d\n", (int)sizeof(struct al_t));
    printf("alignof_.ptr=%d\n", (int)sizeof(void*));
}


static void blk_volatile_(void) {
    volatile int sink = 0; int i;
    for (i = 0; i < 3; i++) { sink = i; }
    printf("volatile_.sink=%d\n", (int)sink);
}


static void blk_intpromo(void) {
    char a = 100, b = 100;
    printf("intpromo.char_sum=%d\n", (int)(a + b));
    printf("intpromo.cmp=%d\n", (-1 < 1u) ? 1 : 0);
}


#define SQ(x) ((x)*(x))
#define MAX_BAD(a, b) ((a) > (b) ? (a) : (b))
static void blk_macro(void) {
    int i = 1;
    printf("macro.sq_good=%d\n", SQ(i + 3));
    printf("macro.max_bad=%d\n", MAX_BAD(i++, 1));  /* 双求值副作用 */
    printf("macro.i_after=%d\n", i);
}

int main(void){
    blk_shift();
    blk_bitfield();
    blk_alignof_();
    blk_volatile_();
    blk_intpromo();
    blk_macro();
    return 0;
}

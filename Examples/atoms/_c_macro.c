#include <stdio.h>

#define SQ_BAD(x)   x * x
#define SQ_GOOD(x)  ((x) * (x))
#define MAX_BAD(a, b) ((a) > (b) ? (a) : (b))

static void macro_probe(void) {
    int v = 3;
    printf("sq_bad=%d\n", SQ_BAD(v + 1));
    printf("sq_good=%d\n", SQ_GOOD(v + 1));

    int i = 0;
    int m = MAX_BAD(0, i++);   /* 走 else 分支 ⇒ i++ 被求值第二次 */
    printf("max_bad_result=%d\n", m);
    printf("i_after=%d\n", i);
}

int main(void) {
    macro_probe();
    return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stddef.h>

static uintptr_t malloc_lifecycle_probe(void) {
    void *p = malloc(0);
    int zero_is_null = (p == NULL);
    free(p);

    int *q = malloc(sizeof(int) * 4);
    int aligned = (((uintptr_t)q % _Alignof(max_align_t)) == 0);
    uintptr_t before = (uintptr_t)q;
    free(q);                       /* 只释放；变量 q 本身不会被清零 */

    free(NULL);                    /* 标准：空操作 */
    printf("malloc0_null=%d\n", zero_is_null);
    printf("alloc_aligned=%d\n", aligned);
    printf("dangling_value_nonzero=%d\n", before != 0);
    printf("reached_after_free_null=1\n");
    return before;
}

int main(void) {
    (void)malloc_lifecycle_probe();
    return 0;
}

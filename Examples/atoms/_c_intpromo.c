#include <stdio.h>

static void intpromo_probe(void) {
    int i = -1;
    unsigned u = 1u;
    printf("cmp_signed_unsigned=%d\n", i < u);
    printf("minus1_as_unsigned=%u\n", (unsigned)-1);

    signed char c = 100;
    signed char d = 100;
    printf("char_promoted_sum=%d\n", c + d);
    printf("char_sum_type_size=%zu\n", sizeof(c + d));
}

int main(void) {
    intpromo_probe();
    return 0;
}

#include <stdio.h>

static void decay_param_sizeof(int p[10]) {
    printf("decay_sizeof_param=%zu\n", sizeof p);
    printf("decay_len_wrong_inside=%zu\n", sizeof p / sizeof p[0]);
}

int main(void) {
    int a[10];
    printf("decay_sizeof_array=%zu\n", sizeof a);
    printf("decay_len_true=%zu\n", sizeof a / sizeof a[0]);
    decay_param_sizeof(a);
    return 0;
}

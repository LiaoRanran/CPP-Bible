#include <stdio.h>
#include <limits.h>

static void signedovf_probe(void) {
    int i = INT_MAX;
    printf("signed_plus1_gt=%d\n", (i + 1) > i);

    unsigned u = UINT_MAX;
    printf("unsigned_plus1_gt=%d\n", (u + 1) > u);
    printf("unsigned_wrapped=%u\n", u + 1);
}

int main(void) {
    signedovf_probe();
    return 0;
}

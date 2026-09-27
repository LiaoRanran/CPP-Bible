#include <stdio.h>
#include <string.h>

struct BF { unsigned a : 3; unsigned b : 5; int c : 4; };

static void bitfield_probe(void) {
    struct BF s;
    memset(&s, 0, sizeof s);
    s.a = 5;
    s.b = 21;
    s.c = -1;
    printf("bf_sizeof=%zu\n", sizeof s);
    printf("bf_a=%u\n", s.a);
    printf("bf_b=%u\n", s.b);
    printf("bf_c_signed_readback=%d\n", s.c);
    unsigned char raw[sizeof s];
    memcpy(raw, &s, sizeof s);
    printf("bf_byte0=%u\n", (unsigned)raw[0]);
    printf("bf_byte1=%u\n", (unsigned)raw[1]);
}

int main(void) {
    bitfield_probe();
    return 0;
}

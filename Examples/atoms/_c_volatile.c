#include <stdio.h>

static int plain_flag = 0;
static volatile int vol_flag = 0;

static int volatile_probe(void) {
    int sink = 0;
    for (int i = 0; i < 3; i++) { sink += plain_flag; }
    for (int i = 0; i < 3; i++) { sink += vol_flag; }
    return sink;
}

int main(void) {
    printf("sink=%d\n", volatile_probe());
    return 0;
}

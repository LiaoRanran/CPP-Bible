#include <stdio.h>
#include <setjmp.h>

static jmp_buf env;

static void jump_back(void) { longjmp(env, 1); }

static void setjmp_probe(void) {
    volatile int vol_local = 0;
    int plain_local = 0;
    if (setjmp(env) == 0) {
        vol_local = 5;
        plain_local = 5;
        jump_back();
    }
    printf("after_longjmp_plain=%d\n", plain_local);
    printf("after_longjmp_volatile=%d\n", vol_local);
}

int main(void) {
    setjmp_probe();
    return 0;
}

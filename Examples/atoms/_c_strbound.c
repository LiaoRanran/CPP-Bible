#include <stdio.h>
#include <string.h>

static void strbound_probe(void) {
    char buf[8];
    int n = snprintf(buf, sizeof buf, "%s", "1234567890");
    printf("snprintf_ret=%d\n", n);
    printf("snprintf_written=%d\n", (int)strlen(buf));
    printf("snprintf_truncated=%d\n", n >= (int)sizeof buf);

    char dst[8];
    memset(dst, 'X', sizeof dst);
    strncpy(dst, "12345678", sizeof dst);
    int terminated = 0;
    for (size_t i = 0; i < sizeof dst; i++) {
        if (dst[i] == '\0') { terminated = 1; }
    }
    printf("strncpy_nul_terminated=%d\n", terminated);
    printf("strncpy_last_byte=%d\n", (int)(unsigned char)dst[7]);
}

int main(void) {
    strbound_probe();
    return 0;
}

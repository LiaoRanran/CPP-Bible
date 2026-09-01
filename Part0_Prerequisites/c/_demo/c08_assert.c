/* C8 佐证：assert 在 NDEBUG 关闭时的行为。GCC 15.3.0 -std=c11。 */
#include <stdio.h>
#include <assert.h>

int main(void) {
    assert(1 == 2);          /* 必然失败 */
    printf("never reached\n");
    return 0;
}

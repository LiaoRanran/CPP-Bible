/* C8 标准库：固定宽度、snprintf/strncpy、qsort、memmove。GCC 15.3.0 -std=c11。 */
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>

static int cmp_int(const void *pa, const void *pb) {
    int a = *(const int*)pa, b = *(const int*)pb;
    return (a > b) - (a < b);
}

int main(void) {
    /* 固定宽度整型：跨平台稳定（接 C6 LLP64） */
    printf("sizeof int32_t=%zu uint64_t=%zu intptr_t=%zu\n",
        sizeof(int32_t), sizeof(uint64_t), sizeof(intptr_t));

    /* snprintf：安全截断，返回本应写入的长度 */
    char buf[8];
    int n = snprintf(buf, sizeof buf, "%s", "hello world");
    printf("snprintf(\"hello world\"->buf[8]) 返回=%d 实际写入=\"%s\"\n", n, buf);

    /* strncpy 不补 \\0 的坑 */
    char b2[5];
    strncpy(b2, "hello", 5);   /* 恰好 5 字符，无空间放终止符 */
    printf("strncpy(\"hello\",5)->b2[5] 逐字节: ");
    for (int k = 0; k < 5; k++) printf("%c", b2[k]);
    printf("  (无 \\0 -> %%s 会越界读到内存里下一个 \\0)\n");

    /* qsort + 函数指针（C 的“泛型”） */
    int arr[] = {5, 2, 9, 1, 5, 6};
    qsort(arr, 6, sizeof(int), cmp_int);
    printf("qsort -> ");
    for (int k = 0; k < 6; k++) printf("%d ", arr[k]);
    printf("\n");

    /* memmove 能处理重叠；memcpy 重叠是 UB */
    int m[6] = {0, 1, 2, 3, 4, 5};
    memmove(m + 1, m, 3 * sizeof(int));
    printf("memmove 重叠后 m = ");
    for (int k = 0; k < 6; k++) printf("%d ", m[k]);
    printf("\n");
    return 0;
}

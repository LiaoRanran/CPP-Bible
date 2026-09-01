/* C9 互操作：错误做法——缺 extern "C"，C++ 把 cadd 改名，链接失败。G++ 15.3.0。 */
#include <stdio.h>
int cadd(int, int);          /* 没有 extern "C" -> 编译器按 C++ 改名 */
int main() {
    printf("cadd(3,4)=%d\n", cadd(3, 4));
    return 0;
}

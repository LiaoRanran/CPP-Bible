/* C9 互操作：正确做法——extern "C" 关闭改名，链接 C 编译的符号。G++ 15.3.0。 */
#include <stdio.h>
extern "C" {
    int cadd(int, int);
    struct Point { int x; int y; };
    int point_sum(struct Point);
}
int main() {
    printf("cadd(3,4)=%d\n", cadd(3, 4));
    struct Point p{1, 2};
    printf("point_sum{1,2}=%d\n", point_sum(p));
    return 0;
}

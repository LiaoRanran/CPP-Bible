/* C7 预处理：宏展开、文本替换、# 与 ##、可变宏、条件编译。GCC 15.3.0 -std=c11。 */
#include <stdio.h>

#define SQUARE(x) ((x)*(x))
#define MAX_BAD(a,b) a>b?a:b
#define MAX_OK(a,b)  ((a)>(b)?(a):(b))
#define CONCAT(a,b)  a##b
#define STR(x)       #x
#define LOG(fmt, ...) printf("[LOG] " fmt "\n", __VA_ARGS__)

#define FEAT_A
#ifdef FEAT_A
#define MODE "FEAT_A on"
#else
#define MODE "FEAT_A off"
#endif

int main(void) {
    /* 1) 多次求值 -> 未定义行为 */
    int i = 3;
    int r = SQUARE(i++);     /* 展开为 ((i++)*(i++))，i 被求值两次 */
    printf("SQUARE(i++) 初值 i=3 -> r=%d, i=%d  (期望 r=9,i=4；实为 UB)\n", r, i);

    /* 2) 缺括号的优先级坑 */
    int a = 3, b = 4;
    printf("2*MAX_BAD(3,4) = %d  (人期望 2*4=8；展开为 (2*3)>4?3:4)\n", 2*MAX_BAD(a,b));
    printf("2*MAX_OK (3,4) = %d\n", 2*MAX_OK(a,b));

    /* 3) 字符串化 # 与记号粘贴 ## */
    int CONCAT(num,7) = 42;
    printf("CONCAT(num,7)=%d ; STR(Hello)=%s\n", num7, STR(Hello));

    /* 4) 可变宏 */
    LOG("x=%d y=%d", 10, 20);

    /* 5) 条件编译 */
    printf("MODE=%s\n", MODE);
    return 0;
}

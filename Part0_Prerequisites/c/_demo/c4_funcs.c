/* C4 函数与栈帧演示：传参（寄存器/栈）、变参 stdarg、递归栈帧
 *
 * 复现命令（gcc 为 MinGW GCC 15.3.0）：
 *   gcc -std=c11 -O0 -Wall -Wextra -o c4_funcs.exe c4_funcs.c && ./c4_funcs.exe
 *   gcc -std=c11 -O0 -c c4_funcs.c -o c4_o0.o
 *   gcc -std=c11 -O2 -c c4_funcs.c -o c4_o2.o
 *   objdump -d -M intel c4_o0.o | sed -n '/<add5>:/,/^$/p'
 *   objdump -d -M intel c4_o0.o | sed -n '/<sum_all>:/,/^$/p'
 */
#include <stdio.h>
#include <stdarg.h>

/* 5 个整数参数：Microsoft x64 下前 4 个走寄存器（rcx,rdx,r8,r9），
 * 第 5 个由调用者压到栈上（紧邻 32 字节影子空间之后）。 */
int add5(int a, int b, int c, int d, int e) {
    return a + b + c + d + e;
}

/* 变参函数：count 之后的参数用 stdarg 逐个取。
 * 关键：调用者对 float 做「默认实参提升」为 double，对 char/short 提升为 int。 */
int sum_all(int count, ...) {
    va_list ap;
    va_start(ap, count);
    int total = 0;
    for (int i = 0; i < count; ++i) {
        total += va_arg(ap, int);
    }
    va_end(ap);
    return total;
}

/* 变参里读 double：与传 float 的调用者配对——float 已被提升为 double */
double avg_f(int count, ...) {
    va_list ap;
    va_start(ap, count);
    double total = 0;
    for (int i = 0; i < count; ++i) {
        total += va_arg(ap, double);
    }
    va_end(ap);
    return count > 0 ? total / count : 0.0;
}

/* 递归：每一层一个栈帧（-O0 下可看到完整链；-O2 可能被改写成循环） */
static long factorial(int n) {
    return n <= 1 ? 1 : n * (long)factorial(n - 1);
}

int main(void) {
    printf("add5 = %d\n", add5(1, 2, 3, 4, 5));
    printf("sum  = %d\n", sum_all(4, 10, 20, 30, 40));
    printf("avg  = %.2f\n", avg_f(3, 1.5f, 2.5f, 3.0f)); /* float 提升为 double */
    printf("fact = %ld\n", factorial(10));
    return 0;
}

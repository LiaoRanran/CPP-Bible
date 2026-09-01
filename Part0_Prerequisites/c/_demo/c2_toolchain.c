/* C2 工具链演示：GCC 四阶段（预处理 / 编译 / 汇编 / 链接）
 *
 * 复现命令（在 _demo 目录下，gcc 为 MinGW GCC 15.3.0）：
 *   gcc -std=c11 -E c2_toolchain.c -o c2.i     # 阶段1 预处理
 *   gcc -std=c11 -O0 -S c2_toolchain.c -o c2.s # 阶段2 编译（生成汇编）
 *   gcc -std=c11 -O0 -c c2_toolchain.c -o c2.o # 阶段3 汇编（生成目标文件）
 *   gcc c2.o -o c2.exe                          # 阶段4 链接
 *   objdump -h c2.o                             # 查看节区表
 *   objdump -d -M intel c2.o                    # 反汇编目标文件
 *   objdump -r c2.o                             # 查看重定位项（未解析符号）
 */
#include <stdio.h>

#define SQUARE(x) ((x) * (x))   /* 预处理阶段被文本替换 */

static int counter = 0;          /* 初值为 0 → 放入 .bss（不占文件空间） */
int          g_value = 42;       /* 已初始化 → 放入 .data */

int add(int a, int b) {          /* 函数体 → .text */
    return a + b;
}

int main(void) {
    int x = 5;
    int y = SQUARE(x);           /* 展开为 ((5) * (5)) */
    counter = counter + 1;
    printf("x=%d sq=%d add=%d counter=%d g=%d\n",
           x, y, add(x, y), counter, g_value);
    return 0;
}

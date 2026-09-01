/* C9 互操作：被 C++ 调用的 C 实现（不依赖任何 C++ 特性）。GCC 15.3.0。 */
int cadd(int a, int b) { return a + b; }

struct Point { int x; int y; };
int point_sum(struct Point p) { return p.x + p.y; }

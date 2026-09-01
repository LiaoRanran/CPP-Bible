// a5_layout.cpp — A5 结构体/数组字段访问（用于 objdump）
// 编译: g++ -std=c++23 -O2 -c -o a5_layout.o a5_layout.cpp
// 反汇编: objdump -d -M intel a5_layout.o
struct Point { int x; int y; long id; };
struct Padded { char a; int b; short c; };

__attribute__((noinline))
long manhattan(const Point* p) { return (long)p->x + p->y; }   // x@0, y@4
__attribute__((noinline))
long arr_at(const int* a, long i) { return a[i]; }             // [a + i*4]
__attribute__((noinline))
long field_b(const Padded* p) { return p->b; }                 // b@4

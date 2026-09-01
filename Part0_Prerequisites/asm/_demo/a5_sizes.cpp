// a5_sizes.cpp — A5 真实尺寸/偏移（offsetof + sizeof，GCC15.3 真机）
// 编译运行: g++ -std=c++23 a5_sizes.cpp -o a5_sizes.exe && ./a5_sizes.exe
#include <cstddef>
#include <cstdio>
struct Point { int x; int y; long id; };
struct Padded { char a; int b; short c; };
int main() {
    printf("sizeof(Point)=%zu alignof(Point)=%zu\n", sizeof(Point), alignof(Point));
    printf("Point.x@%zu y@%zu id@%zu\n", offsetof(Point,x), offsetof(Point,y), offsetof(Point,id));
    printf("sizeof(Padded)=%zu alignof(Padded)=%zu\n", sizeof(Padded), alignof(Padded));
    printf("Padded.a@%zu b@%zu c@%zu\n", offsetof(Padded,a), offsetof(Padded,b), offsetof(Padded,c));
    return 0;
}

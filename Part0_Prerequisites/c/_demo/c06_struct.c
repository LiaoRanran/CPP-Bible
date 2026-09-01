/* C6 结构体与内存布局：对齐、填充与重排。GCC 15.3.0 -std=c11，本机 MinGW x64 (LLP64)。 */
#include <stdio.h>
#include <stddef.h>
#include <string.h>

struct S1 { char   a; int b; };                       /* 经典 1+4 */
struct S2 { int    a; char b; };
struct S3 { char   a; char b; int c; };               /* 两个 char 相邻 */
struct S4 { char   a; int b; char c; };               /* 被 int 隔开 */
struct S5 { int    b; char a; char c; };              /* S4 的重排版 */
struct S6 { double a; char  b; };
struct Aligned { _Alignas(16) char tag; int x; };

struct BF       { unsigned int a:1; unsigned int b:1; unsigned int c:30; };
struct ThreeInt { unsigned int a;  unsigned int b;  unsigned int c;  };

/* 含 long：跨 LLP64/LP64 布局会分叉 */
struct Header { char magic; int len; short flags; long id; };

int main(void) {
    printf("=== 基础对齐（本机 LLP64, MinGW x64）===\n");
    printf("  alignof  char=%zu short=%zu int=%zu long=%zu double=%zu void*=%zu\n",
        _Alignof(char), _Alignof(short), _Alignof(int),
        _Alignof(long),  _Alignof(double), _Alignof(void*));

    printf("=== 尺寸与字段偏移 ===\n");
    printf("S1{char;int}            sizeof=%2zu  a@%zu b@%zu\n",
        sizeof(struct S1), offsetof(struct S1,a), offsetof(struct S1,b));
    printf("S2{int;char}            sizeof=%2zu  a@%zu b@%zu\n",
        sizeof(struct S2), offsetof(struct S2,a), offsetof(struct S2,b));
    printf("S3{char;char;int}       sizeof=%2zu  a@%zu b@%zu c@%zu\n",
        sizeof(struct S3), offsetof(struct S3,a), offsetof(struct S3,b), offsetof(struct S3,c));
    printf("S4{char;int;char}       sizeof=%2zu  a@%zu b@%zu c@%zu\n",
        sizeof(struct S4), offsetof(struct S4,a), offsetof(struct S4,b), offsetof(struct S4,c));
    printf("S5{int;char;char} 重排  sizeof=%2zu  b@%zu a@%zu c@%zu\n",
        sizeof(struct S5), offsetof(struct S5,b), offsetof(struct S5,a), offsetof(struct S5,c));
    printf("S6{double;char}         sizeof=%2zu  a@%zu b@%zu  align=%zu\n",
        sizeof(struct S6), offsetof(struct S6,a), offsetof(struct S6,b), _Alignof(struct S6));
    printf("Aligned{_Alignas(16)char;int} sizeof=%2zu tag@%zu x@%zu  align=%zu\n",
        sizeof(struct Aligned), offsetof(struct Aligned,tag), offsetof(struct Aligned,x), _Alignof(struct Aligned));

    printf("=== 位域打包 ===\n");
    printf("  BF{三个 1-bit 位域}    sizeof=%zu   （等价只占 1 个 unsigned int）\n", sizeof(struct BF));
    printf("  ThreeInt{三个 unsigned int} sizeof=%zu\n", sizeof(struct ThreeInt));

    printf("=== 事故现场1：padding 字节是不确定的 ===\n");
    struct Header h;
    h.magic='P'; h.len=7; h.flags=1; h.id=42;       /* 只给字段赋值 */
    unsigned char *p = (unsigned char*)&h;
    printf("  Header sizeof=%zu 原始字节:", sizeof h);
    for (size_t i=0; i<sizeof h; i++) printf("%02x ", p[i]);
    printf("\n  (3 字节 padding 在第 1 字节后、2 字节 padding 在第 9 字节后 = 栈上残留)\n");

    printf("=== 事故现场2：跨平台 sizeof 分叉 ===\n");
    printf("  本机(LLP64)  Header sizeof=%zu  id@%zu\n", sizeof(struct Header), offsetof(struct Header,id));
    printf("  LP64(Linux)   long=8 字节 -> id 需 8 对齐 -> id@16, sizeof=24（布局不再兼容）\n");
    printf("  朴素缓冲 char raw[%zu] 装不下 -> memcpy 越界；raw 字节发网络对方解错\n",
        sizeof(int)+sizeof(char)+sizeof(short)+sizeof(long));

    printf("=== #pragma pack 的代价 ===\n");
    printf("  #pragma pack(1) 可消除 padding（Header->9 字节），\n");
    printf("  但字段不再按自然对齐：读 int/long 在部分架构 SIGBUS，且破坏 ABI 互传。\n");
    return 0;
}

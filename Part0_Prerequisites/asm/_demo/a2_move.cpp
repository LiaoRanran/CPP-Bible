// a2_move.cpp — A2 数据移动原语示例
// 编译: g++ -std=c++23 -O2 -c -o a2_move.o a2_move.cpp
// 反汇编: objdump -d -M intel a2_move.o
long f(long a, long b, long* p) {
    long t = a + b;   // 期望 lea
    *p = t;           // 期望 mov store
    long q = *p + 1;  // 期望 mov load + add
    return q;
}

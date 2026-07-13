// ① RVO（返回值优化）：单局部对象直接构造于调用者栈槽
#include <cstdio>

struct Big {
    long a[8];
    Big() { a[0] = 0xCAFEBABE; }
    Big(const Big&) { std::printf("copy!\n"); }   // 有副作用，便于 -O0 观测
};

Big make() {
    Big b;          // 这个对象会被直接构造在调用者的返回槽
    return b;       // RVO：不拷贝
}

int main() {
    Big x = make(); // 调用处直接得到构造结果，无 mov 复制
    return (int)x.a[0];
}

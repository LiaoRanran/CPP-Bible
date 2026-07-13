// _ch139_ebo.cpp
// 取证目的：CRTP 基类是空类，依赖 EBO 让派生类 sizeof 不膨胀。
#include <iostream>

struct EmptyPolicy {};

struct NoEBO {
    EmptyPolicy p;   // 作为成员，至少占 1 字节
    int v;
};

template <typename Policy>
struct WithEBO : Policy {  // 作为基类 -> 空基类优化
    int v;
};

struct MyPolicy {};  // 空类

int main() {
    std::cout << "sizeof(NoEBO)=" << sizeof(NoEBO)
              << " sizeof(WithEBO)=" << sizeof(WithEBO<MyPolicy>) << "\n";
}

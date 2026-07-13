// _ch138_iterator.cpp
// 第138章 ⑧⑨：迭代器——自定义容器 + 标准迭代器接口 + 范围 for
#include <iostream>

template <typename T, int N>
struct FixedArray {
    T data[N];
    T* begin() { return data; }
    T* end()   { return data + N; }
    const T* begin() const { return data; }
    const T* end()   const { return data + N; }
};

int main() {
    FixedArray<int, 4> a{1, 2, 3, 4};
    int s = 0;
    for (int x : a) s += x;     // 范围 for 依赖 begin()/end()
    std::cout << s << '\n';
    return 0;
}

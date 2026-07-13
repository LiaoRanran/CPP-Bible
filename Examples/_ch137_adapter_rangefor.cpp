// 文件: Examples/_ch137_adapter_rangefor.cpp
// 迭代器适配器：让 C 风格数组支持范围 for（提供 begin/end）
#include <iostream>

template <typename T, std::size_t N>
struct ArrayAdapter {
    T* begin() { return data_; }
    T* end()   { return data_ + N; }
    const T* begin() const { return data_; }
    const T* end()   const { return data_ + N; }
    T data_[N];
};

int main() {
    ArrayAdapter<int, 3> a{{1, 2, 3}};
    for (int x : a) std::cout << x << ' ';   // 范围 for 依赖 ADL begin/end
    std::cout << '\n';
}

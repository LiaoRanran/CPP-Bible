// ch144 ⑦ auto 类型推断无运行时开销：显式类型与 auto& 生成相同机器码
// 编译：g++ -std=c++23 -O2 -S -masm=intel _ch144_auto.cpp -o _ch144_auto_O2.asm
#include <vector>
#include <numeric>

// 写法 A：显式写出元素类型
long explicit_sum(const std::vector<long>& v) {
    long s = 0;
    for (const long& x : v) s += x;   // 显式 const long&
    return s;
}

// 写法 B：用 auto& 让编译器推断
long auto_sum(const std::vector<long>& v) {
    long s = 0;
    for (auto& x : v) s += x;          // ✅ auto& 推断为 const long&
    return s;
}

long demo() {
    std::vector<long> v(1024, 3);
    return explicit_sum(v) + auto_sum(v);
}

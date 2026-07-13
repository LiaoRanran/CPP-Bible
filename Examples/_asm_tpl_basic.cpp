// 模板基础与实例化：显式实例化发射 mangled 符号 + 实例化点
// 编译：g++ -std=c++23 -O2 -S -masm=intel _asm_tpl_basic.cpp -o _asm_tpl_basic.asm
#include <utility>

template <typename T>
T max_val(T a, T b) {
    return (a < b) ? b : a;
}

// 显式实例化定义：强制在翻译单元内生成 max_val<int> 与 max_val<double>
template int max_val<int>(int, int);
template double max_val<double>(double, double);

// 隐式实例化：调用处触发的实例化点
int use_implicit(int x, int y) {
    return max_val(x, y);          // 隐式实例化 max_val<int>
}

double use_implicit_d(double a, double b) {
    return max_val(a, b);          // 隐式实例化 max_val<double>
}

// 非类型模板参数：编译期常量
template <typename T, int N>
T get_nth(T arr[N], int i) {
    return arr[i];
}

int main() {
    return use_implicit(3, 7) + static_cast<int>(use_implicit_d(1.0, 2.0));
}

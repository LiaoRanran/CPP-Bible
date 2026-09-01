// ch05 §⑩ 汇编验证：C++14 泛型 lambda「编译为独立模板实例函数、与手写等价（零开销）」
// 证据工件：本 .cpp 用仓库权威 GCC 15.3.0 编译出 ch05_generic_lambda_o0.s（-O0，看实例化符号）
// 与 ch05_generic_lambda_o2.s（-O2，看零调用内联）。
int twice_i(int x) { return x * 2; }            // 手写基线

int use_generic() {
    auto gl = [](auto x) { return x * 2; };     // C++14 泛型 lambda
    return gl(7) + (int)gl(2.5);                // 两个实例：int / double
}

int main() { return use_generic(); }

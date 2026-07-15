// ASM-std_function: std::function 类型擦除的调用代价 —— GCC 15.3.0 真机实证
// 关键：std::function 调用 = 经对象内存储的 invoker 指针间接调用（类型擦除），
//       无法内联；对照裸函数指针（同样间接）与模板/无捕获 lambda（可内联）。
#include <functional>
#include <cstdint>

int square(int x) { return x * x; }

// 经 std::function 类型擦除调用
[[gnu::noinline]] int via_std_function(const std::function<int(int)>& f, int x) {
    return f(x);
}
// 经模板调用（函数指针实参）
[[gnu::noinline]] int via_template_fp(int (*f)(int), int x) {
    return f(x);
}
// 经模板调用（无捕获 lambda 实参）
template <typename F>
[[gnu::noinline]] int via_template(F f, int x) {
    return f(x);
}

int main() {
    std::function<int(int)> f = square;
    volatile int s = 0;
    s = via_std_function(f, 5);                 // 类型擦除：间接调用
    s = via_template_fp(square, 5);             // 裸函数指针：间接调用
    s = via_template([](int x) { return x * x; }, 5);  // 无捕获 lambda：可内联
    return s;
}

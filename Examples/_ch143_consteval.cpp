// ⑪ 编译期折叠取证：consteval 使计算在编译期完成，运行期无循环
constexpr int fib(int n) {
    return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

consteval int compile_time() {
    return fib(15);   // 610，编译期定值
}

int runtime_use() {
    return compile_time();   // 期望折叠为常量 mov eax, 610
}

// ⑯ 反模式：为不存在的变化点建过度抽象（对比"按需抽象"）
// 本机 g++ -std=c++23 -O2 编译运行通过
#include <iostream>
#include <string>

// ❌ 反模式：三层继承只为"打印一行"，纯属噪音
struct IPrinter { virtual ~IPrinter() = default; virtual void print() = 0; };
struct IConsolePrinter : IPrinter { virtual ~IConsolePrinter() = default; };
struct ConsolePrinter : IConsolePrinter { void print() override { std::cout << "hi\n"; } };

// ✅ 正确：除非真有第二种实现，否则直接一个函数
void print_simple() { std::cout << "hi\n"; }

int main() {
    ConsolePrinter bad; bad.print();
    print_simple();
    std::cout << "[anti] 两种都输出 hi，但前者多 2 个无用类型\n";
    return 0;
}

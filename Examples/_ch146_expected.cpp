// 取证示例：std::expected (C++23) 替代异常做值/错误表征
// 编译：g++ -std=c++23 -O2 -Wall -Wextra _ch146_expected.cpp -o _ch146_expected.exe
#include <expected>
#include <string>
#include <iostream>

std::expected<int, std::string> parse_int(const char* s) {
    try {
        return std::stoi(s);
    } catch (...) {
        return std::unexpected(std::string("not an int: ") + s);
    }
}

int main() {
    auto good = parse_int("42");
    auto bad  = parse_int("oops");
    if (good) std::cout << "value=" << *good << '\n';
    if (!bad)  std::cout << "error=" << bad.error() << '\n';
}

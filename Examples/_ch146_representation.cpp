// _ch146_representation.cpp
// ② 返回值 vs 异常 vs 枚举：三种表征方式的最小对照。
#include <cstdio>
#include <stdexcept>
#include <string>

// (A) 返回值：调用方必须显式检查，无隐式控制流
int parse_int_return(const char* s, bool& ok) {
    try {
        int v = std::stoi(s);
        ok = true;
        return v;
    } catch (...) {
        ok = false;
        return 0;
    }
}

// (B) 异常：错误沿调用栈自动传播，可携带丰富上下文
int parse_int_throw(const char* s) {
    return std::stoi(s); // 非法输入抛 std::invalid_argument
}

// (C) 枚举 + 输出参数：零分配、可预测
enum class ParseErr { Ok, BadFormat, Overflow };
ParseErr parse_int_enum(const char* s, int& out) {
    char* end = nullptr;
    long v = std::strtol(s, &end, 10);
    if (end == s || *end != '\0') return ParseErr::BadFormat;
    if (v > 2147483647L || v < -2147483648L) return ParseErr::Overflow;
    out = static_cast<int>(v);
    return ParseErr::Ok;
}

int main() {
    bool ok = false;
    int a = parse_int_return("42", ok);
    int b = 0;
    ParseErr e = parse_int_enum("17", b);
    std::printf("return=%d(%d) enum=%d out=%d\n", a, (int)ok, (int)e, b);
    try { (void)parse_int_throw("xyz"); }
    catch (const std::exception& ex) { std::printf("throw: %s\n", ex.what()); }
    return 0;
}

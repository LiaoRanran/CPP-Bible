// 取证示例：自定义 std::error_code / error_category（自包含）
// 编译：g++ -std=c++23 -O2 -Wall -Wextra _ch146_errorcode.cpp -o _ch146_errorcode.exe
#include <system_error>
#include <type_traits>
#include <iostream>
#include <string>

enum class db_err { ok = 0, timeout = 1, closed = 2 };

struct db_err_category : std::error_category {
    const char* name() const noexcept override { return "db"; }
    std::string message(int ev) const override {
        switch (static_cast<db_err>(ev)) {
            case db_err::timeout: return "connection timeout";
            case db_err::closed:  return "connection closed";
            default:              return "ok";
        }
    }
    // 默认映射：db 错误不归类为任何 POSIX 条件
    std::error_condition default_error_condition(int ev) const noexcept override {
        return std::error_condition(ev, *this);
    }
};

const db_err_category& db_err_cat() { static db_err_category c; return c; }

// 自由函数 + is_error_code_enum 特化 => 隐式转换为 error_code
std::error_code make_error_code(db_err e) { return {static_cast<int>(e), db_err_cat()}; }
namespace std {
    template<> struct is_error_code_enum<db_err> : std::true_type {};
}

int main() {
    std::error_code ec = db_err::timeout;       // 隐式转换
    std::cout << ec.category().name() << ':' << ec.value()
              << ' ' << ec.message() << '\n';
    if (ec == db_err::timeout) std::cout << "timeout detected\n";
    if (ec) std::cout << "ec is in error state\n";
}

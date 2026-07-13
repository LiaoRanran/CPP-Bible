// _ch146_throw_try_catch.cpp
// ③ 异常机制：throw / try / catch 与 catch-by-reference。
#include <cstdio>
#include <stdexcept>
#include <string>

void validate_age(int age) {
    if (age < 0)
        throw std::invalid_argument("age 不能为负"); // 抛出派生自 std::exception 的对象
    if (age > 150)
        throw std::out_of_range("age 超出合理上限");
}

int main() {
    for (int a : {-1, 20, 200}) {
        try {
            validate_age(a);
            std::printf("age=%d OK\n", a);
        } catch (const std::invalid_argument& e) {        // 精确捕获
            std::printf("invalid_argument: %s\n", e.what());
        } catch (const std::out_of_range& e) {
            std::printf("out_of_range: %s\n", e.what());
        } catch (const std::exception& e) {               // 兜底基类
            std::printf("std::exception: %s\n", e.what());
        }
    }
    return 0;
}

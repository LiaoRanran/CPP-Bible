// 文件：Examples/_ch128_crtp.cpp
// 说明：CRTP（Curiously Recurring Template Pattern）自包含示例，
//       演示 Boost 大量使用的编译期多态（零虚函数开销），
//       类似 Boost.Operators / Boost.Iterator 的风格。
#include <cstdio>

template <typename Derived>
struct Addable {
    int value;                       // 唯一的 value 成员（基类持有）
    Derived operator+(const Derived& o) const {
        const auto& self = static_cast<const Derived&>(*this);
        return Derived{ self.value + o.value };
    }
};

struct Vec2 : Addable<Vec2> {
    Vec2() = default;
    explicit Vec2(int v) { value = v; }   // 仅设置基类持有的 value
};

int main() {
    Vec2 a{3}, b{4};
    Vec2 c = a + b;            // 编译期决议 operator+，无虚表调用
    return c.value;            // 返回 7
}

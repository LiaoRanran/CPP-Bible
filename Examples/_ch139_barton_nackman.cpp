// _ch139_barton_nackman.cpp
// 取证目的：Barton-Nackman 技巧——把友元比较运算符定义在 CRTP 基类模板里。
#include <iostream>

template <typename T>
struct Equality {
    friend bool operator==(const T& lhs, const T& rhs) {
        return lhs.equal_to(rhs);
    }
};

struct Point : Equality<Point> {
    int x, y;
    Point(int x_, int y_) : x(x_), y(y_) {}
    bool equal_to(const Point& o) const { return x == o.x && y == o.y; }
};

int main() {
    Point a{1, 2}, b{1, 2}, c{3, 4};
    std::cout << std::boolalpha
              << (a == b) << " " << (a == c) << "\n";
}

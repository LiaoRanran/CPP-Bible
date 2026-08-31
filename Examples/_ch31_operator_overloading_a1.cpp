#include <iostream>

struct Vec { double x, y, z; };
Vec operator+(const Vec& a, const Vec& b) { return { a.x + b.x, a.y + b.y, a.z + b.z }; }
Vec& operator+=(Vec& a, const Vec& b) { a.x += b.x; a.y += b.y; a.z += b.z; return a; }

int main() {
    Vec a{ 1, 2, 3 }, b{ 4, 5, 6 }, c{ 7, 8, 9 }, d{ 1, 1, 1 };
    Vec v1 = a; v1 = v1 + b + c + d;          // 链式（可能生成临时）
    Vec v2 = a; v2 += b; v2 += c; v2 += d;    // 原地（无临时）
    std::cout << "chained: " << v1.x << "," << v1.y << "," << v1.z << std::endl;
    std::cout << "in-place: " << v2.x << "," << v2.y << "," << v2.z << std::endl;
    return 0;
}
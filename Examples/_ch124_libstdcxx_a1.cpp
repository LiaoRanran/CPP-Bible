#include <iostream>
#include <string>
#include <cassert>

int main() {
    std::string a(15, 'x');   // 在 libstdc++ SSO 容量内
    std::string b(40, 'x');   // 超出 SSO → 堆分配
    std::string c = a;        // SSO 内拷贝：零分配
    std::string d = b;        // 堆拷贝：深拷贝
    assert(c == a && d == b);
    std::cout << "a.size=" << a.size() << " b.size=" << b.size() << "\n";
    return 0;
}
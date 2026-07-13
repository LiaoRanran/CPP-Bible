// _ch124_vector.cpp — 用于取证 libstdc++ 内联与符号（第124章 ⑨⑪）
#include <vector>
#include <string>

int sum_vector(const std::vector<int>& v) {
    int s = 0;
    for (int x : v) s += x;
    return s;
}

std::string make_greeting(const char* name) {
    std::string g = "Hello, ";
    g += name;            // 触发 SSO / 基本字符串操作
    return g;
}

int main() {
    std::vector<int> v{1, 2, 3, 4, 5};
    std::string who = make_greeting("world");
    return sum_vector(v) + (int)who.size();
}

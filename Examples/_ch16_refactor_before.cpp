// 重构前：巨型函数 + 魔法数 + 重复逻辑（clang-tidy 会报 readability 问题）
#include <string>
#include <vector>
std::string before(const std::vector<int>& xs) {
    std::string s;
    for (int i = 0; i < xs.size(); i++) {
        if (xs[i] > 10) {
            s += std::to_string(xs[i]);
            s += ";";
        } else {
            s += std::to_string(xs[i]);
            s += ";";
        }
    }
    return s;
}
int main() { return before({1, 20, 3}).size(); }

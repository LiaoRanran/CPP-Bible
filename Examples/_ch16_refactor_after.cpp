// 重构后：提取谓词 + 消除分支重复 + 命名常量（[实现]真实差异见第⑪节）
#include <string>
#include <vector>
namespace {
constexpr int kThreshold = 10;
bool passes(int x) { return x > kThreshold; }
}
std::string after(const std::vector<int>& xs) {
    std::string s;
    for (int x : xs)
        if (passes(x)) (s += std::to_string(x)) += ";";
    return s;
}
int main() { return after({1, 20, 3}).size(); }

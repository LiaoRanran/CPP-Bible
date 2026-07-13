// 文件：Examples/_ch162_format.cpp
// 行号：10-18（std::format 构造 JSON 片段）
// ⑮ 与 std::format 衔接：用格式化库安全地拼 JSON（需 C++20 <format>）。
#include <format>
#include <iostream>
#include <string>

int main() {
    std::string name = "小明";
    int age = 30;
    double score = 9.5;
    // 注意：字符串值仍需手动转义，format 不替你转义 JSON 特殊字符
    std::string json = std::format(
        R"({{"name":"{}","age":{},"score":{:.2f}}})", name, age, score);
    std::cout << json << "\n";

    // 用 std::format 生成带类型的诊断信息
    std::cout << std::format("[diag] type=string len={}", name.size()) << "\n";
    return 0;
}

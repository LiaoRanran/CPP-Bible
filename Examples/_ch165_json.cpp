// _ch165_json.cpp : 手写 JSON 解析片段（从零项目，见第162章 JSON）
#include <iostream>
#include <memory>
#include <string>
#include <variant>
#include <vector>

struct JsonValue;
using Json = std::shared_ptr<JsonValue>;
struct JsonValue {
    std::variant<std::nullptr_t, bool, double, std::string,
                 std::vector<Json>, std::shared_ptr<std::vector<std::pair<std::string, Json>>>> data;
};

// 极简分词：跳过空白，读取下一个 token 首字符
char peek(const std::string& s, size_t& i) {
    while (i < s.size() && std::isspace((unsigned char)s[i])) ++i;
    return i < s.size() ? s[i] : '\0';
}

// 练习：实现 parse_value / parse_object / parse_array 递归下降
int main() {
    std::string doc = R"({"name":"cpp","ver":23,"ok":true})";
    size_t i = 0;
    std::cout << "first token = '" << peek(doc, i) << "'\n";  // '{'
    return 0;
}

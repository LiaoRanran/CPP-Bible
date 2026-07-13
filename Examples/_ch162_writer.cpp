// 文件：Examples/_ch162_writer.cpp
// 行号：8-16（Value 的 variant 定义 + write 序列化）
// ⑧ 序列化（writer）：把内存中的 Value 写回 JSON 文本（自包含可编译）。
#include <cstdio>
#include <iostream>
#include <map>
#include <string>
#include <variant>
#include <vector>

struct Value;
using JsonArray  = std::vector<Value>;
using JsonObject = std::map<std::string, Value>;

struct Value {
    using Storage = std::variant<std::nullptr_t, bool, double,
                                 std::string, JsonArray, JsonObject>;
    Storage data = nullptr;
};

std::string write(const Value& v);

std::string write(const Value& v) {
    if (std::holds_alternative<std::nullptr_t>(v.data)) return "null";
    if (std::holds_alternative<bool>(v.data))
        return std::get<bool>(v.data) ? "true" : "false";
    if (std::holds_alternative<double>(v.data)) {
        char b[32]; std::snprintf(b, sizeof(b), "%.17g",
                                  std::get<double>(v.data)); return b;
    }
    if (std::holds_alternative<std::string>(v.data))
        return "\"" + std::get<std::string>(v.data) + "\"";
    if (std::holds_alternative<JsonArray>(v.data)) {
        std::string s = "[";
        for (const auto& e : std::get<JsonArray>(v.data)) s += write(e) + ",";
        if (s.back() == ',') s.pop_back();
        return s + "]";
    }
    std::string s = "{";
    for (const auto& kv : std::get<JsonObject>(v.data))
        s += "\"" + kv.first + "\":" + write(kv.second) + ",";
    if (s.back() == ',') s.pop_back();
    return s + "}";
}

int main() {
    JsonObject obj;
    obj["x"] = Value{1.5};
    obj["ok"] = Value{true};
    obj["list"] = Value{JsonArray{Value{1.0}, Value{2.0}}};
    Value root{std::move(obj)};
    std::cout << write(root) << "\n";
    return 0;
}

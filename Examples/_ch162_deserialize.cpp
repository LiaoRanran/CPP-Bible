// 文件：Examples/_ch162_deserialize.cpp
// 行号：22-34（from_object 反序列化到 struct）
// ⑯ 反序列化到 struct：把解析出的 Object 映射为强类型 C++ 结构。
#include <cstdint>
#include <iostream>
#include <map>
#include <string>
#include <variant>
#include <vector>

struct JsonValue;
using JsonArray  = std::vector<JsonValue>;
using JsonObject = std::map<std::string, JsonValue>;
struct JsonValue {
    std::variant<std::nullptr_t, bool, double, std::string, JsonArray, JsonObject> d{nullptr};
    bool        as_bool()   const { return std::get<bool>(d); }
    double      as_number() const { return std::get<double>(d); }
    std::string as_string() const { return std::get<std::string>(d); }
    const JsonObject& as_object() const { return std::get<JsonObject>(d); }
    const JsonArray&  as_array()  const { return std::get<JsonArray>(d); }
};

struct User {
    int64_t id;
    std::string name;
    double score;
};

// 反序列化：从 JsonObject 逐个字段取出并做类型校验
User from_object(const JsonObject& o) {
    User u;
    u.id    = static_cast<int64_t>(o.at("id").as_number());
    u.name  = o.at("name").as_string();
    u.score = o.at("score").as_number();
    return u;
}

int main() {
    // 模拟已解析好的对象
    JsonObject o;
    o["id"]    = JsonValue{1.0};
    o["name"]  = JsonValue{std::string("alice")};
    o["score"] = JsonValue{9.81};
    User u = from_object(o);
    std::cout << "id=" << u.id << " name=" << u.name << " score=" << u.score << "\n";
    return 0;
}

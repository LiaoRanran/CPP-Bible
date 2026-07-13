// 文件：Examples/_ch162_variant.cpp
// 行号：12-20（Value 的 variant 定义）
// ③ 值表示：用 std::variant 表达 JSON 的 6 种类型，类型安全、无继承开销。
#include <iostream>
#include <map>
#include <string>
#include <variant>
#include <vector>

struct JsonValue;
using JsonArray  = std::vector<JsonValue>;
using JsonObject = std::map<std::string, JsonValue>;

struct JsonValue {
    using Storage = std::variant<std::nullptr_t, bool, double,
                                 std::string, JsonArray, JsonObject>;
    Storage data = nullptr;

    // 访问：用 std::holds_alternative / std::get 做类型安全读取
    bool is_object() const { return std::holds_alternative<JsonObject>(data); }
};

int main() {
    JsonValue v;
    std::cout << "默认构造为 null: "
              << std::holds_alternative<std::nullptr_t>(v.data) << "\n";

    JsonObject obj;
    obj["k"] = JsonValue{};          // 暂存 null
    v.data = std::move(obj);
    std::cout << "赋值 object 后 is_object(): " << v.is_object() << "\n";

    // variant 的 index() 可用于调试打印当前活跃类型
    std::cout << "当前活跃类型 index: " << v.data.index() << "\n";
    return 0;
}

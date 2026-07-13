// 文件: Examples/_ch137_flyweight_intern.cpp
// string interning 思路：相等字符串字面量指向同一份存储
#include <iostream>
#include <string>
#include <string_view>
#include <unordered_set>

struct StringPool {
    std::string_view intern(std::string_view s) {
        std::string key(s);                          // 统一为 key_type 再查找
        auto it = set_.find(key);
        if (it != set_.end()) return *it;            // 命中：返回已有存储
        auto [ins, _] = set_.emplace(std::move(key));
        return *ins;
    }
private:
    std::unordered_set<std::string> set_;
};

int main() {
    StringPool pool;
    auto a = pool.intern("hello");
    auto b = pool.intern("hello");
    std::cout << (a.data() == b.data() ? "shared\n" : "dup\n");
}

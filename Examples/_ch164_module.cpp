// ⑦ 模块化：接口（抽象基类）与实现分离，框架只依赖接口
// 本机 g++ -std=c++23 -O2 编译运行通过
#include <iostream>
#include <string>
#include <memory>
#include <unordered_map>

// 接口层：稳定的契约（放在 framework 头，很少改动）
struct IStorage {
    virtual ~IStorage() = default;
    virtual bool save(const std::string& key, const std::string& val) = 0;
    virtual std::string load(const std::string& key) = 0;
};

// 实现层：可独立替换、独立测试，不影响接口使用者
struct MemoryStorage : IStorage {
    std::unordered_map<std::string, std::string> data;
    bool save(const std::string& k, const std::string& v) override { data[k] = v; return true; }
    std::string load(const std::string& k) override {
        auto it = data.find(k); return it == data.end() ? "" : it->second;
    }
};

// 消费者只认接口
void use(IStorage& s) {
    s.save("user", "alice");
    std::cout << "[module] load(user) = " << s.load("user") << "\n";
}

int main() {
    MemoryStorage store;
    use(store);
    return 0;
}

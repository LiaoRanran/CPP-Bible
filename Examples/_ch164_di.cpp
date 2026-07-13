// ⑥ 依赖注入容器：类型擦除到 std::shared_ptr<void>，按 key 解析（关联 第141章）
// 本机 g++ -std=c++23 -O2 编译运行通过
#include <iostream>
#include <string>
#include <unordered_map>
#include <memory>

struct IService { virtual ~IService() = default; virtual std::string who() = 0; };
struct DbService : IService { std::string who() override { return "DbService"; } };
struct CacheService : IService { std::string who() override { return "CacheService"; } };

struct Container {
    std::unordered_map<std::string, std::shared_ptr<void>> m;
    template <class T> void add(const std::string& k, std::shared_ptr<T> p) {
        m[k] = std::static_pointer_cast<void>(p);
    }
    template <class T> std::shared_ptr<T> get(const std::string& k) const {
        auto it = m.find(k);
        return it == m.end() ? nullptr : std::static_pointer_cast<T>(it->second);
    }
};

int main() {
    Container c;
    c.add<IService>("db", std::make_shared<DbService>());
    c.add<IService>("cache", std::make_shared<CacheService>());
    auto s = c.get<IService>("db");
    std::cout << "[di] resolved db -> " << (s ? s->who() : "?") << "\n";
    auto miss = c.get<IService>("nope");
    std::cout << "[di] missing key -> " << (miss ? "found" : "nullptr (safe)") << "\n";
    return 0;
}

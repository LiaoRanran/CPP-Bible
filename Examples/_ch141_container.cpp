// Examples/_ch141_container.cpp
// 手写简易 DI 容器：按类型登记工厂，按需解析（resolve）并自动注入依赖图。
#include <iostream>
#include <memory>
#include <string>
#include <unordered_map>
#include <functional>

struct IRepo { virtual ~IRepo() = default; virtual std::string load() = 0; };
struct DbRepo : IRepo { std::string load() override { return "row"; } };

struct Controller {
    std::unique_ptr<IRepo> repo;
    std::string act() { return repo->load(); }
};

class Container {
    std::unordered_map<std::string, std::function<std::unique_ptr<IRepo>()>> factories_;
public:
    void registerRepo(std::function<std::unique_ptr<IRepo>()> f) { factories_["repo"] = std::move(f); }
    std::unique_ptr<Controller> resolve() {
        auto c = std::make_unique<Controller>();
        c->repo = factories_.at("repo")();   // 容器负责装配依赖
        return c;
    }
};

int main() {
    Container c;
    c.registerRepo([] { return std::make_unique<DbRepo>(); });
    auto ctrl = c.resolve();
    std::cout << ctrl->act() << "\n";
}

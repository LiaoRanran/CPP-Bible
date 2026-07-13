// Examples/_ch141_boost_di_mimic.cpp
// 上游参考：Boost.DI（非本书编译，需 boost 1.80+）。下面给出其“自动装配”风格的最小自包含模仿，
// 用于说明“基于构造签名的自动依赖解析”思想。该模仿体本身可独立编译。
#include <iostream>
#include <memory>
#include <type_traits>

struct IRepository { virtual ~IRepository() = default; virtual int id() = 0; };
struct Repository : IRepository { int id() override { return 1; } };

struct Service {
    std::unique_ptr<IRepository> repo;
    explicit Service(std::unique_ptr<IRepository> r) : repo(std::move(r)) {}
    int run() { return repo->id(); }
};

// Boost.DI 的 make_injector().create<Service>() 会按构造签名自动 new 依赖；
// 这里用手写工厂表模拟“自动解析”。
class Injector {
public:
    std::unique_ptr<Service> create() {
        return std::make_unique<Service>(std::make_unique<Repository>());
    }
};

int main() {
    Injector inj;
    auto s = inj.create();
    std::cout << s->run() << "\n";
}

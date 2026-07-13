// ⑧ 宏与代码生成：用 X 宏/注册宏削减样板（关联 第148章 工具链）
// 本机 g++ -std=c++23 -O2 编译运行通过
#include <iostream>
#include <string>
#include <unordered_map>
#include <functional>
#include <memory>

// 宏生成组件骨架：声明 class + 自注册，省去重复手写
#define COMPONENT(Cls, Key, Msg)                       \
    struct Cls : IUnit {                               \
        std::string name() const override { return Key; } \
        std::string msg()  const override { return Msg; }  \
    };                                                 \
    static AutoRegX _x_##Cls { Key, [] { return std::make_shared<Cls>(); } }

struct IUnit {
    virtual ~IUnit() = default;
    virtual std::string name() const = 0;
    virtual std::string msg()  const = 0;
};
struct AutoRegX {
    AutoRegX(const std::string& k, std::function<std::shared_ptr<IUnit>()> f) { regX()[k] = std::move(f); }
    static std::unordered_map<std::string, std::function<std::shared_ptr<IUnit>()>>& regX() {
        static std::unordered_map<std::string, std::function<std::shared_ptr<IUnit>()>> r; return r;
    }
};

COMPONENT(CpuProbe,   "cpu",    "cpu 12%");
COMPONENT(MemProbe,   "mem",    "mem 512MB");
COMPONENT(DiskProbe,  "disk",   "disk ok");

int main() {
    std::cout << "[macro] generated " << AutoRegX::regX().size() << " probes\n";
    for (auto& [k, f] : AutoRegX::regX()) {
        auto u = f(); std::cout << "  " << u->name() << " -> " << u->msg() << "\n";
    }
    return 0;
}

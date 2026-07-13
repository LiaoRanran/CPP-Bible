// Examples/_ch141_test_strategy.cpp
// 测试策略：用依赖注入实现“端口/适配器（六边形）”架构，测试中用内存适配器替换外部端口。
#include <cassert>
#include <memory>
#include <string>
#include <unordered_map>

struct IEventBus { virtual ~IEventBus() = default; virtual void publish(const std::string&) = 0; };
struct KafkaBus : IEventBus { void publish(const std::string&) override {} };
struct InMemBus : IEventBus {                                  // 测试用内存总线
    std::string last;
    void publish(const std::string& s) override { last = s; }
};

class Aggregate {
    std::unique_ptr<IEventBus> bus_;
public:
    explicit Aggregate(std::unique_ptr<IEventBus> b) : bus_(std::move(b)) {}
    void onOrder() { bus_->publish("OrderPlaced"); }
};

int main() {
    auto mem = std::make_unique<InMemBus>();
    auto* raw = mem.get();
    Aggregate a(std::move(mem));     // ✅ 注入内存总线，断言可观测
    a.onOrder();
    assert(raw->last == "OrderPlaced");
}

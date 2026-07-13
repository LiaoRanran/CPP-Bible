// Examples/_ch141_interface.cpp
// DI 与接口（抽象基类）：面向接口编程，运行时多态解耦高层与低层。
#include <iostream>
#include <memory>
#include <string>

struct INotifier {                     // 抽象接口（接口隔离）
    virtual ~INotifier() = default;
    virtual void send(const std::string&) = 0;
};
struct EmailNotifier : INotifier {
    void send(const std::string& s) override { std::cout << "email:" << s << "\n"; }
};
struct SmsNotifier : INotifier {
    void send(const std::string& s) override { std::cout << "sms:" << s << "\n"; }
};

class OrderService {
    std::unique_ptr<INotifier> notifier_;   // 依赖接口，而非具体类
public:
    explicit OrderService(std::unique_ptr<INotifier> n) : notifier_(std::move(n)) {}
    void place() { notifier_->send("ordered"); }
};

int main() {
    OrderService a(std::make_unique<EmailNotifier>());  // 注入 Email 实现
    OrderService b(std::make_unique<SmsNotifier>());    // 注入 Sms 实现
    a.place(); b.place();
}

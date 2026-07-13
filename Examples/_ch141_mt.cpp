// Examples/_ch141_mt.cpp
// DI 与多线程：注入的依赖需明确线程安全边界。不可变（const）依赖可安全共享。
#include <iostream>
#include <memory>
#include <thread>
#include <vector>

struct IWork { virtual ~IWork() = default; virtual int run(int x) = 0; };
struct Square : IWork { int run(int x) override { return x * x; } };  // 无状态→线程安全

class Worker {
    std::shared_ptr<IWork> work_;      // 共享只读依赖（线程安全）
public:
    explicit Worker(std::shared_ptr<IWork> w) : work_(std::move(w)) {}
    int go(int x) const { return work_->run(x); }
};

int main() {
    auto w = std::make_shared<Square>();
    std::vector<std::thread> ts;
    for (int i = 0; i < 4; ++i)
        ts.emplace_back([w, i] { Worker x(w); std::cout << x.go(i) << " "; });
    for (auto& t : ts) t.join();
}

// 文件: Examples/_ch137_decorator_bench.cpp
// 装饰链调用开销微基准（std::chrono）：逐层叠加 Decorator 测单次调用延迟
#include <chrono>
#include <cstdio>
#include <memory>

struct I {
    virtual ~I() = default;
    virtual int f(int) = 0;
};

struct Impl : I {
    int f(int x) override { return x + 1; }
};

struct Deco : I {
    explicit Deco(std::unique_ptr<I> n) : n_(std::move(n)) {}
    int f(int x) override { return n_->f(x) + 1; }   // 多一次虚调用 + 包裹
private:
    std::unique_ptr<I> n_;
};

int main() {
    auto base = std::make_unique<Impl>();
    std::unique_ptr<I> chain = std::move(base);
    for (int i = 0; i < 5; ++i)
        chain = std::make_unique<Deco>(std::move(chain));   // 叠 5 层装饰

    const int N = 10'000'000;
    auto t0 = std::chrono::steady_clock::now();
    volatile int sink = 0;
    for (int i = 0; i < N; ++i) sink = chain->f(i);
    auto t1 = std::chrono::steady_clock::now();

    double ns = std::chrono::duration<double, std::nano>(t1 - t0).count() / N;
    std::printf("5 层装饰开销 ~%.2f ns/调用 (sink=%d)\n", ns, sink);
}

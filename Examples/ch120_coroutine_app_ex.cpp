// ③-a 最小 generator<T> —— 支持 co_yield + 范围迭代
#include <coroutine>
#include <iostream>
#include <exception>

template <typename T>
struct Generator {
    struct promise_type {
        T value_;
        Generator get_return_object() { return Generator{std::coroutine_handle<promise_type>::from_promise(*this)}; }
        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(T v) { value_ = v; return {}; }
        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };
    using handle = std::coroutine_handle<promise_type>;
    handle h_;
    explicit Generator(handle h) : h_(h) {}
    ~Generator() { if (h_) h_.destroy(); }
    Generator(const Generator&) = delete;
    Generator& operator=(const Generator&) = delete;
    Generator(Generator&& o) noexcept : h_(std::exchange(o.h_, nullptr)) {}
    Generator& operator=(Generator&& o) noexcept { if (this != &o) { if (h_) h_.destroy(); h_ = std::exchange(o.h_, nullptr); } return *this; }
    bool next() { h_.resume(); return !h_.done(); }
    T value() const { return h_.promise().value_; }
};

Generator<int> range(int n) {
    for (int i = 0; i < n; ++i) co_yield i;
}

int main() {
    auto g = range(5);
    while (g.next()) std::cout << g.value() << " ";
    std::cout << std::endl;
    return 0;
}
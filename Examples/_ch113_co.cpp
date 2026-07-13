// 文件：Examples/_ch113_co.cpp
// 行号：1
// 本文件是 ch113 协程章的可编译取证样本（C++20）。
// 编译取证命令见各节 asm 块。
#include <coroutine>
#include <cstdint>
#include <exception>
#include <utility>

// ───────────────────────── task（future-like，run-to-completion） ─────────
struct task {
    struct promise_type {
        task get_return_object() noexcept {
            return task{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        void return_void() noexcept {}
        void unhandled_exception() { std::terminate(); }
    };
    std::coroutine_handle<promise_type> h_{};
    explicit task(std::coroutine_handle<promise_type> h) : h_(h) {}
    ~task() { if (h_) h_.destroy(); }
    bool resume() {
        if (!h_ || h_.done()) return false;
        h_.resume();
        return !h_.done();
    }
};

// ───────────────────────── generator（yield 整数序列） ───────────────────
struct generator {
    struct promise_type {
        int current_{};
        generator get_return_object() noexcept {
            return generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_always initial_suspend() noexcept { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(int v) noexcept {
            current_ = v;
            return {};
        }
        void return_void() noexcept {}
        void unhandled_exception() { std::terminate(); }
    };
    std::coroutine_handle<promise_type> h_{};
    explicit generator(std::coroutine_handle<promise_type> h) : h_(h) {}
    ~generator() { if (h_) h_.destroy(); }
    bool next() {
        if (!h_ || h_.done()) return false;
        h_.resume();
        return !h_.done();
    }
    int value() const { return h_.promise().current_; }
};

// ───────────────────────── 协程函数 ─────────────────────────
generator range(int n) {
    for (int i = 0; i < n; ++i)
        co_yield i;
}

task count_up() {
    for (int i = 0; i < 3; ++i)
        co_await std::suspend_always{};
}

int main() {
    auto g = range(5);
    int sum = 0;
    while (g.next()) sum += g.value();
    return sum;
}

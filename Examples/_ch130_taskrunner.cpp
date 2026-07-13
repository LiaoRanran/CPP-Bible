// 自包含 TaskRunner / MessageLoop 等价：任务队列 + PostTask + RunOne
// 展示 Chromium base::TaskRunner 的核心机制（类型擦除的回调队列，单线程执行）。
#include <cstddef>
#include <utility>
#include <functional>

struct TaskRunner {
    using Task = std::function<void()>;
    static constexpr int CAP = 64;
    Task queue[CAP];
    int head = 0, tail = 0, count = 0;
    // 等价于 base::TaskRunner::PostTask：把回调入队（环形缓冲）
    void PostTask(Task t) {
        if (count < CAP) {
            queue[tail] = std::move(t);
            tail = (tail + 1) % CAP;
            ++count;
        }
    }
    // 等价于 MessageLoop::Run 的单步：取出并执行一个任务
    void RunOne() {
        if (count > 0) {
            Task t = std::move(queue[head]);
            head = (head + 1) % CAP;
            --count;
            t();   // 执行任务（类型擦除调用）
        }
    }
};

static int g_counter = 0;

// 热点：投递若干任务后驱动消息循环执行
int run_loop(TaskRunner& r, int n) {
    for (int i = 0; i < n; ++i)
        r.PostTask([i] { g_counter += i; });
    for (int i = 0; i < n; ++i)
        r.RunOne();
    return g_counter;
}

int main() {
    TaskRunner r;
    return run_loop(r, 8);
}

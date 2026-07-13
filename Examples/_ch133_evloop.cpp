// 文件：Examples/_ch133_evloop.cpp
// 行号：1
// 自包含示例：模拟 Redis ae.c 的「单线程 Reactor 事件循环」。
// 用 std::vector 管理文件描述符事件，主循环 select 式轮询并分发。

#include <cstdint>
#include <cstddef>
#include <vector>
#include <functional>

struct FileEvent {
    int fd;
    std::function<void(int)> read_cb;   // 读就绪回调（等价 aeFileProc）
};

// 单线程事件循环（无锁、无多线程）：注册 fd + 回调，loop() 轮询分发。
struct EventLoop {
    std::vector<FileEvent> files;
    bool stop = false;

    void add(int fd, std::function<void(int)> cb) {
        files.push_back(FileEvent{fd, std::move(cb)});
    }
    // 等价 aeProcessEvents：遍历就绪 fd 并调用回调（此处简化为单轮分发，
    // 真实 ae.c 用多路复用拿到 ready 集合后再分发，单线程顺序执行）。
    void loop() {
        for (auto& fe : files) {
            if (fe.read_cb) fe.read_cb(fe.fd);   // 单线程顺序处理
        }
        stop = true;     // 演示用：单轮即止（真实循环由 IO 多路复用驱动）
    }
};

int g_counter = 0;
extern "C" int run_loop() {
    EventLoop el;
    el.add(3, [](int fd){ g_counter += fd; });
    el.add(5, [](int fd){ g_counter += fd * 2; });
    el.loop();
    return g_counter;   // 期望 3 + 5*2 = 13
}

#include <cstdio>
int main() {
    printf("g_counter=%d\n", run_loop());   // 期望 13
    return 0;
}

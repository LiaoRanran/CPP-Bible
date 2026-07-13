// RCU 取证源：写者复制-替换 + 读者免锁读取
#include <atomic>

struct Config { int timeout; int workers; };
std::atomic<Config*> g_config{nullptr};

// 写者：复制旧对象 -> 修改 -> 原子替换指针
extern "C" void rcu_update(int t, int w) {
    Config* old = g_config.load(std::memory_order_acquire);
    Config* nw = new Config{t, w};
    g_config.store(nw, std::memory_order_release);
    delete old;   // 真实工程里应在宽限期后删除，这里仅取证指针替换
}

// 读者：免锁，仅一次原子 load
extern "C" Config* rcu_read() {
    return g_config.load(std::memory_order_acquire);
}

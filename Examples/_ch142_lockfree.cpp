// 文件：Examples/_ch142_lockfree.cpp
// 行号：3
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 -S -masm=intel Examples/_ch142_lockfree.cpp -o Examples/_ch142_lockfree.asm
// 无锁读：写线程独占更新 entity 记录，读线程用 acquire/relaxed 原子做无锁读取（见 ⑮）。
#include <atomic>
#include <cstdint>

struct EntityRecord {
    std::atomic<std::uint32_t> version;  // 代际，写时递增
    std::atomic<bool>           alive;   // 存活标志
};

// 无锁读：只读一个 atomic，不需要加锁
bool is_alive(const EntityRecord& r) {
    return r.alive.load(std::memory_order_acquire);
}

// 写：先置 false 再推进版本（发布-订阅式）
void kill(EntityRecord& r) {
    r.alive.store(false, std::memory_order_release);
    r.version.fetch_add(1, std::memory_order_relaxed);
}

int main() {
    EntityRecord r;
    r.alive.store(true, std::memory_order_relaxed);
    bool a = is_alive(r);
    kill(r);
    return a ? 1 : 0;
}

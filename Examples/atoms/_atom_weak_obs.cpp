// Examples/_atom_weak_obs.cpp
// 服务 ATOM-MEM-WEAK-001：weak_ptr 是非拥有观察者——不增加引用计数；.lock() 临时提升为 shared_ptr，
// 对象已销毁则 .lock() 返回空（expired）。用来安全"看一眼"共享对象而不延长其寿命。
#include <memory>
#include <iostream>

volatile int g_destroy = 0;                 // volatile：防折叠（M2 §5）
struct Box { ~Box() { g_destroy = g_destroy + 1; } };

int main() {
    std::shared_ptr<Box> a = std::make_shared<Box>();
    std::weak_ptr<Box> w = a;                                       // 不增加计数
    std::cout << "use_count with weak=" << a.use_count() << "\n";   // 1
    std::cout << "weak expired before=" << w.expired() << "\n";     // 0（对象活着）
    {
        auto locked = w.lock();                                      // 提升为 shared_ptr
        std::cout << "use_count after lock=" << a.use_count() << "\n";   // 2
        std::cout << "locked bool=" << (bool)locked << "\n";             // 1（提升成功）
    }                                                                // locked 析构 -1
    std::cout << "use_count after lock scope=" << a.use_count() << "\n";   // 1
    a.reset();                                                       // 释放对象
    std::cout << "weak expired after reset=" << w.expired() << "\n";     // 1（对象已销毁）
    std::cout << "box destroyed count=" << g_destroy << "\n";             // 1
    return 0;
}

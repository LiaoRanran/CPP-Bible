// Examples/_atom_shared_count.cpp
// 服务 ATOM-MEM-SHARED-001：shared_ptr 用引用计数实现共享所有权——拷贝 +1、析构 -1、归零才释放。
#include <memory>
#include <iostream>

volatile int g_destroy = 0;                 // volatile：防折叠（M2 §5）
struct Box { ~Box() { g_destroy = g_destroy + 1; } };

int main() {
    {
        std::shared_ptr<Box> a = std::make_shared<Box>();
        std::cout << "use_count after make=" << a.use_count() << "\n";   // 1
        std::shared_ptr<Box> b = a;                                        // 拷贝 +1
        std::cout << "use_count after copy=" << a.use_count() << "\n";    // 2
        {
            std::shared_ptr<Box> c = a;                                    // 再 +1
            std::cout << "use_count in scope=" << a.use_count() << "\n";   // 3
        }                                                                  // c 析构 -1
        std::cout << "use_count after scope=" << a.use_count() << "\n";    // 2
    }                                                                      // a,b 析构 -> 3->2->1->0 -> Box 析构一次
    std::cout << "box destroyed count=" << g_destroy << "\n";              // 1 => 归零才释放（共享所有权）
    return 0;
}

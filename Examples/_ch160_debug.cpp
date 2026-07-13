// 文件：Examples/_ch160_debug.cpp
// 行号：1
// 调试：内存泄漏检测——在分配器里记录未释放指针集合（简化版）
#include <cstddef>
#include <cstdio>
#include <unordered_set>
#include <mutex>
#include <new>

namespace dbg {
    std::mutex mtx;
    std::unordered_set<void*> live;
    void* alloc(std::size_t n) {
        void* p = ::operator new(n);
        std::lock_guard<std::mutex> lk(mtx);
        live.insert(p);
        return p;
    }
    void free(void* p) noexcept {
        std::lock_guard<std::mutex> lk(mtx);
        live.erase(p);
        ::operator delete(p);
    }
    void report() {
        std::lock_guard<std::mutex> lk(mtx);
        std::printf("[leak report] live pointers = %zu\n", live.size());
    }
}

int main() {
    void* a = dbg::alloc(64);
    void* b = dbg::alloc(128);
    dbg::free(a);
    // b 故意不释放 -> 泄漏
    dbg::report(); // 应报告 1 个泄漏
    return 0;
}

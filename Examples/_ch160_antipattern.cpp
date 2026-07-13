// 文件：Examples/_ch160_antipattern.cpp
// 行号：1
// 反模式：双重释放 / 越界 的"错误示例"与"安全检测版"
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <unordered_set>
#include <mutex>

// ❌ 错误示例（仅作注释展示，切勿编译运行）：
//   int* p = (int*)malloc(sizeof(int)*10);
//   p[10] = 0;            // 越界写，UB
//   free(p); free(p);     // 双重释放，UB
// 这些 UB 在 MinGW/GCC 下可能"看似正常"，实则破坏堆元数据。

// ✅ 安全检测版：用登记集合拦截双重释放
namespace safe {
    std::mutex mtx;
    std::unordered_set<void*> live;
    void* malloc_tagged(std::size_t n) {
        void* p = std::malloc(n);
        std::lock_guard<std::mutex> lk(mtx); live.insert(p); return p;
    }
    void free_guarded(void* p) {
        std::lock_guard<std::mutex> lk(mtx);
        if (!live.count(p)) { std::printf("DOUBLE-FREE detected @ %p\n", p); return; }
        live.erase(p); std::free(p);
    }
}

int main() {
    void* p = safe::malloc_tagged(64);
    safe::free_guarded(p);
    safe::free_guarded(p); // 第二次被拦截，不崩溃
    std::printf("antipattern guard OK\n");
    return 0;
}

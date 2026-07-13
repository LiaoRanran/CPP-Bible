// _ch135_raii.cpp
// 取证目标（第⑥节）：RAII 把资源生命周期绑定到对象作用域。
#include <cstdio>
#include <cstdlib>

struct FileGuard {
    FILE* f;
    explicit FileGuard(const char* p) : f(std::fopen(p, "wb")) {
        if (!f) std::abort();
    }
    ~FileGuard() { if (f) std::fclose(f); }          // 自动释放
    FileGuard(const FileGuard&) = delete;            // 禁止拷贝
    FileGuard& operator=(const FileGuard&) = delete;
};

int main() {
    { FileGuard g("demo.bin"); /* 作用域结束自动 fclose */ }
}

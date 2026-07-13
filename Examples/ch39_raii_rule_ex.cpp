// [示例 1] 最小 RAII 包装器骨架：构造获取、析构释放
#include <cstdio>
#include <stdexcept>

class FileRAII {
    FILE* f_;
public:
    explicit FileRAII(const char* path, const char* mode)
        : f_(std::fopen(path, mode)) {
        if (!f_) throw std::runtime_error("fopen failed");  // 构造失败→无资源泄漏
    }
    ~FileRAII() noexcept {                    // 析构 noexcept：异常安全基石
        if (f_) std::fclose(f_);              // 释放资源
    }
    FILE* get() const noexcept { return f_; }
    // 禁止拷贝（见 Rule of Three），允许移动（见 Rule of Five）
    FileRAII(const FileRAII&) = delete;
    FileRAII& operator=(const FileRAII&) = delete;
};

int main() {
    FileRAII log("app.log", "w");   // 构造即获取
    std::fprintf(log.get(), "hello RAII\n");
    // 离开 main 作用域时 ~FileRAII() 自动 fclose，无需手写清理
}
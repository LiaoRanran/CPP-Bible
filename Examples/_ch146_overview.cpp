// _ch146_overview.cpp
// ① 概述：错误处理策略。三种主流表征的并列对比骨架。
#include <cstdio>
#include <string>

// 用枚举表达"领域错误"，避免抛异常；调用方必须检查。
enum class ReadResult { Ok, Eof, WouldBlock, IoError };

ReadResult read_one(int fd) {
    (void)fd;
    return ReadResult::Eof; // 示意：真实实现取决于平台 API
}

int main() {
    ReadResult r = read_one(0);
    if (r != ReadResult::Ok) {
        std::printf("read stopped: enum=%d\n", static_cast<int>(r));
    }
    return static_cast<int>(r);
}

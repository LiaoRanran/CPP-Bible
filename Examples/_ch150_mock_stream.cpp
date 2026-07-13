// ④' Mock 输出流：截获被测代码的写行为做断言
#include <cstdio>
#include <cstring>
#include <cassert>
struct ILog { virtual ~ILog() = default; virtual void write(const char*) = 0; };
struct CapturingLog : ILog {
    char sink[256]; int n = 0;
    void write(const char* s) override { std::snprintf(sink + n, sizeof(sink) - n, "%s", s); n += (int)std::strlen(s); }
};
int main() {
    CapturingLog log;
    log.write("error:42");
    assert(std::strstr(log.sink, "error") != nullptr);
    std::printf("mock-stream: captured=\"%s\"\n", log.sink);
    return 0;
}

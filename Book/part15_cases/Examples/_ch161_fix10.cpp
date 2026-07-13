// 文件：Examples/_ch161_fix10.cpp
// 主题：⑪ 源码定位 —— C++20 std::source_location 取代手写 __FILE__/__LINE__ 宏
#include <cstdio>
#include <source_location>
#include <string>
#include <string_view>

void log_at(std::string_view msg,
            std::source_location loc = std::source_location::current()) {
    std::printf("%s:%d %s\n", loc.file_name(), loc.line(),
                std::string(msg).c_str());
}

void deep() { log_at("inside deep"); }

int main() {
    log_at("main start");
    deep();
    return 0;
}

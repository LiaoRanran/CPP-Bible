// 文件：Examples/_ch161_json.cpp
// 取证：g++ -std=c++20 -O2 真实编译运行（本机）；结构化 JSON 日志（机器可解析）
#include <cstdio>
#include <string>

// ⑮ 结构化日志：输出 JSON，便于 ELK/Loki 等系统采集与查询
// 简化转义：仅处理双引号与反斜杠（演示核心思想）
std::string jstr(const std::string& s) {
    std::string o = "\"";
    for (char c : s) {
        if (c == '"' || c == '\\') o += '\\';
        o += c;
    }
    return o + "\"";
}

void log_json(const char* level, const char* evt, int code) {
    std::printf("{\"level\":%s,\"event\":%s,\"code\":%d}\n",
                jstr(level).c_str(), jstr(evt).c_str(), code);
}

int main() {
    log_json("info", "request", 200);
    log_json("error", "timeout", 504);
    return 0;
}

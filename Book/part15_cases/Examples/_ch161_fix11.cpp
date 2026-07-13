// 文件：Examples/_ch161_fix11.cpp
// 主题：⑮ 结构化日志（JSON）—— 含数组字段，机器可直接索引
#include <cstdio>
#include <string>
#include <vector>

std::string jstr(const std::string& s) {
    std::string o = "\"";
    for (char c : s) { if (c == '"' || c == '\\') o += '\\'; o += c; }
    return o + "\"";
}

int main() {
    std::vector<int> tags{7, 8, 9};
    std::string arr = "[";
    for (std::size_t i = 0; i < tags.size(); ++i) {
        if (i) arr += ",";
        arr += std::to_string(tags[i]);
    }
    arr += "]";
    std::printf("{\"level\":%s,\"event\":%s,\"tags\":%s}\n",
                jstr("info").c_str(), jstr("batch").c_str(), arr.c_str());
    return 0;
}

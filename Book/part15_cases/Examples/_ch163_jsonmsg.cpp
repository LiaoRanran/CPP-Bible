// _ch163_jsonmsg.cpp  [跨平台, 纯 C++23]
// 编译: g++ -std=c++23 -O2 _ch163_jsonmsg.cpp -o _ch163_jsonmsg.exe
// 作用: 用 长度前缀 包裹 JSON 载荷（关联 第162章 的 JSON 思想，本例自实现最小化序列化）。
#include <iostream>
#include <vector>
#include <string>
#include <cstdint>

// 极简 JSON 对象序列化（仅演示字段拼接，非完整 RFC 8259 解析器）。
std::string to_json(const std::string& who, int seq) {
    return "{\"who\":\"" + who + "\",\"seq\":" + std::to_string(seq) + "}";
}

int main() {
    std::string payload = to_json("client", 163);
    std::vector<char> frame(4);
    uint32_t len = (uint32_t)payload.size();
    frame[0] = (char)((len >> 24) & 0xFF);
    frame[1] = (char)((len >> 16) & 0xFF);
    frame[2] = (char)((len >> 8) & 0xFF);
    frame[3] = (char)(len & 0xFF);
    frame.insert(frame.end(), payload.begin(), payload.end());
    std::cout << "[jsonmsg] 载荷: " << payload << "\n";
    std::cout << "[jsonmsg] 帧: " << std::string(frame.begin(), frame.end()) << "\n";
    return 0;
}

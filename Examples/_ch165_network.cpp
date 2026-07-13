// _ch165_network.cpp : 网络项目核心——消息成帧/序列化（从零项目，见第163章 网络）
// 不用具体 socket 库，聚焦"长度前缀帧"这一工程难点，跨平台可编译
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

// 帧格式: [4字节大端长度][payload]
void encode(std::vector<uint8_t>& out, const std::string& payload) {
    uint32_t len = static_cast<uint32_t>(payload.size());
    out.push_back((len >> 24) & 0xFF);
    out.push_back((len >> 16) & 0xFF);
    out.push_back((len >> 8) & 0xFF);
    out.push_back(len & 0xFF);
    out.insert(out.end(), payload.begin(), payload.end());
}

bool decode(const std::vector<uint8_t>& buf, size_t& pos, std::string& out) {
    if (buf.size() - pos < 4) return false;
    uint32_t len = (buf[pos] << 24) | (buf[pos + 1] << 16) |
                   (buf[pos + 2] << 8) | buf[pos + 3];
    pos += 4;
    if (buf.size() - pos < len) return false;
    out.assign(buf.begin() + pos, buf.begin() + pos + len);
    pos += len;
    return true;
}

int main() {
    std::vector<uint8_t> frame;
    encode(frame, "hello");
    encode(frame, "world");
    size_t pos = 0; std::string s;
    while (decode(frame, pos, s)) std::cout << s << "\n";
    return 0;
}

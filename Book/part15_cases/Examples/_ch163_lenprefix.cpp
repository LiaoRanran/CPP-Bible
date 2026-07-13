// _ch163_lenprefix.cpp  [跨平台, 纯 C++23]
// 编译: g++ -std=c++23 -O2 _ch163_lenprefix.cpp -o _ch163_lenprefix.exe
// 作用: 长度前缀协议编解码（⑪）：[uint32 大端长度][payload]，附自描述校验。
#include <iostream>
#include <vector>
#include <cstring>
#include <cstdint>

std::vector<char> encode(const std::string& s) {
    std::vector<char> out(4);
    uint32_t len = (uint32_t)s.size();
    out[0] = (char)((len >> 24) & 0xFF);
    out[1] = (char)((len >> 16) & 0xFF);
    out[2] = (char)((len >> 8) & 0xFF);
    out[3] = (char)(len & 0xFF);
    out.insert(out.end(), s.begin(), s.end());
    return out;
}

std::string decode(const std::vector<char>& in) {
    uint32_t len = ((uint8_t)in[0] << 24) | ((uint8_t)in[1] << 16) |
                   ((uint8_t)in[2] << 8) | (uint8_t)in[3];
    return std::string(in.begin() + 4, in.begin() + 4 + len);
}

int main() {
    auto frame = encode("net-bible-163");
    std::cout << "[lenprefix] 帧字节数=" << frame.size() << " (4 头 + "
              << frame.size() - 4 << " 负载)\n";
    std::cout << "[lenprefix] 解码=" << decode(frame) << "\n";
    return 0;
}

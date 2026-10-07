// RW-098 | CVE-2022-32208 | curl | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-32208
// project_url: https://curl.se/
// year: 2022 | severity: MEDIUM | source_type: cve
// mechanism: FTP PASV/EPSV 应答解析缺陷：非 IP 形式的应答被错误解析为地址，
//   使连接回落到攻击者可控地址（协议解析）。
// notes: 最小重构。
#include <cstdio>
#include <cstring>
#include <string>

// BUG: a PASV reply "227 Entering Passive Mode (h1,h2,h3,h4,p1,p2)" is parsed
// with sscanf without validating that 6 numbers were read; a crafted reply
// leaves the address partially uninitialized / attacker-chosen.
void parse_pasv_reply(const char* reply, unsigned char ip[4], unsigned short* port) {
    unsigned a = 0, b = 0, c = 0, d = 0, p1 = 0, p2 = 0;
    int n = std::sscanf(reply, "%*[^(](%u,%u,%u,%u,%u,%u)", &a, &b, &c, &d, &p1, &p2);
    if (n != 6) {
        // BUG: treats a malformed reply as valid and keeps whatever was parsed
        std::printf("accepted malformed PASV reply (read %d/6 fields)\n", n);
    }
    ip[0] = (unsigned char)a; ip[1] = (unsigned char)b;
    ip[2] = (unsigned char)c; ip[3] = (unsigned char)d;
    *port = (unsigned short)(p1 * 256 + p2);
}

int main() {
    unsigned char ip[4];
    unsigned short port = 0;
    parse_pasv_reply("227 Entering Passive Mode (10,0,0,1)", ip, &port); // only 4 fields
    std::printf("connected to %u.%u.%u.%u:%u\n", ip[0], ip[1], ip[2], ip[3], port);
    return 0;
}

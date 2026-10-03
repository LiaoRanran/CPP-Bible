// sample_G042
// defect_type: logic_error
// severity: medium
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2020-8284 (https://nvd.nist.gov/vuln/detail/CVE-2020-8284) [curl]
// (authoritative annotation in sample_G042.json)
#include <cstdio>
#include <string>
// CVE-2020-8284: FTP PASV 响应中的地址被无条件信任
struct FtpConn {
    std::string host;        // 用户连接的主机
    std::string data_ip;     // 数据通道 IP(应来自 host)
    int         data_port;
};

static void ftp_parse_pasv(FtpConn* c, const std::string& pasv_reply) {
    // PASV 回复: "227 Entering Passive Mode (h1,h2,h3,h4,p1,p2)"
    int h1, h2, h3, h4, p1, p2;
    /* DEFECT */ // 原始缺陷: 不校验回复 IP 与控制连接主机是否一致
    std::sscanf(pasv_reply.c_str(), "227 Entering Passive Mode (%d,%d,%d,%d,%d,%d)",
                &h1, &h2, &h3, &h4, &p1, &p2);
    char ip[32];
    std::snprintf(ip, sizeof(ip), "%d.%d.%d.%d", h1, h2, h3, h4);
    c->data_ip = ip;
    c->data_port = p1 * 256 + p2;
}

int main() {
    FtpConn c{ "ftp.victim.example", "", 0 };
    // 恶意服务器的 PASV 响应: 指向攻击者的内网扫描地址
    ftp_parse_pasv(&c, "227 Entering Passive Mode (10,0,0,169,1,144)");
    std::printf("数据通道连接: %s:%d (用户意图: 连接 %s)\n",
                c.data_ip.c_str(), c.data_port, c.host.c_str());
    std::printf("(正确行为: 拒绝与控制连接主机不一致的 PASV 地址)\n");
    return 0;
}

// sample_G041
// defect_type: info_leak
// severity: medium
// planted: false
// expected_verdict: miss
// expected_detectors: asan
// source: CVE-2021-22898 (https://nvd.nist.gov/vuln/detail/CVE-2021-22898) [curl]
// (authoritative annotation in sample_G041.json)
#include <cstdio>
#include <cstring>
#include <string>
// CVE-2021-22898: TELNET NEW_ENV 解析器把本机环境变量发给服务器
static const char* k_machine_env[] = {
    "USER=alice", "HOME=/home/alice", "SECRET_TOKEN=s3cr3t-value", 0
};

static std::string telnet_send_new_env(const char* user_opt) {
    // 用户指定的变量对: user_opt = "TERM=xterm"
    std::string payload = "NEW_ENV:";
    payload += user_opt;
    /* DEFECT */ // 原始缺陷: 选项解析器把环境块中的变量也当作用户选项装入 payload
    for (int i = 0; k_machine_env[i]; ++i) {
        payload += ";";
        payload += k_machine_env[i];
    }
    return payload;
}

int main() {
    std::string sent = telnet_send_new_env("TERM=xterm");
    std::printf("TELNET 发送: %s\n", sent.c_str());
    std::printf("(正确行为: 仅发送 TERM=xterm, SECRET_TOKEN 不应离开本机)\n");
    return 0;
}

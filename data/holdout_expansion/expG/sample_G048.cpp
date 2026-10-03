// sample_G048
// defect_type: logic_error
// severity: medium
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2022-27780 (https://nvd.nist.gov/vuln/detail/CVE-2022-27780) [curl]
// (authoritative annotation in sample_G048.json)
#include <cstdio>
#include <string>
// CVE-2022-27780: 主机名百分号解码产生与解析时不同的 URL
static std::string percent_decode_host(const std::string& host) {
    std::string out;
    for (size_t i = 0; i < host.size(); ++i) {
        /* DEFECT */ // 原始缺陷: 主机名部分的 %2F 被解码为 '/', 生成另一个 URL
        if (host[i] == '%' && i + 2 < host.size() &&
            host[i + 1] == '2' && (host[i + 2] == 'F' || host[i + 2] == 'f')) {
            out += '/';
            i += 2;
        } else {
            out += host[i];
        }
    }
    return out;
}

int main() {
    std::string parsed_host = "example.com%2F127.0.0.1";   // 解析时视作单一主机
    std::string used_host = percent_decode_host(parsed_host);
    std::printf("解析时主机: %s\n实际连接主机: %s\n(正确行为: 两者必须一致)\n",
                parsed_host.c_str(), used_host.c_str());
    return 0;
}

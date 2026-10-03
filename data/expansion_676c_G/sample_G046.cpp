// sample_G046
// defect_type: logic_error
// severity: medium
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2023-27534 (https://nvd.nist.gov/vuln/detail/CVE-2023-27534) [curl]
// (authoritative annotation in sample_G046.json)
#include <cstdio>
#include <string>
// CVE-2023-27534: SFTP ~ 前缀错误展开 → 路径穿越
static std::string sftp_resolve(const std::string& remote_path, const std::string& home) {
    if (!remote_path.empty() && remote_path[0] == '~') {
        /* DEFECT */ // 原始缺陷: 首元素 ~ 与后续 /.. 组合时未按安全规则展开
        // "~~~poor-~/../../etc/passwd" → ~ 之后整段拼接, .. 未规范化
        return home + remote_path.substr(1);
    }
    return remote_path;
}

int main() {
    std::string resolved = sftp_resolve("~~~poor-~/../../etc/passwd", "/home/victim");
    std::printf("SFTP 实际访问: %s\n", resolved.c_str());
    std::printf("(正确行为: 不应展开到 /home/victim 之外)\n");
    return 0;
}

// RW-099 | CVE-2023-27534 | curl | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2023-27534
// project_url: https://curl.se/
// year: 2023 | severity: HIGH | source_type: cve
// mechanism: SFTP 路径中 "~" 展开缺陷 —— 构造的路径使 curl 相对攻击者选择的
//   绝对路径操作（文件系统越界访问）。
// notes: 最小重构（路径展开逻辑）。
#include <cstdio>
#include <string>

// BUG: "~" handling splits on the *last* tilde and re-roots the path; crafted
// "~/../../etc" style input escapes the intended base directory.
std::string sftp_expand_path(const std::string& base, const std::string& path) {
    if (!path.empty() && path[0] == '~') {
        size_t slash = path.find('/');
        std::string user_home = "/home/deploy";          // attacker influences the name
        std::string rest = (slash == std::string::npos) ? "" : path.substr(slash);
        // BUG: `..` segments in `rest` are not normalized against user_home
        return user_home + rest;
    }
    return base + "/" + path;
}

int main() {
    std::string target = sftp_expand_path("/srv/data", "~/../../../etc/shadow");
    std::printf("SFTP will operate on: %s\n", target.c_str());
    return 0;
}

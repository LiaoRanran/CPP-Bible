// RW-047 | CVE-2016-3714 | ImageMagick | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2016-3714
// project_url: https://imagemagick.org/
// year: 2016 | severity: CRITICAL | source_type: cve
// mechanism: ImageTragick —— 委托（delegate）命令模板中把用户控制的 URL/文件名
//   直接拼接进 shell 命令，引号/分号逃逸导致命令注入。
// notes: 最小重构（只演示字符串拼接缺陷，不执行任何真实命令）。
#include <cstdio>
#include <string>

struct ImageInfo {
    std::string magick;    // detected format, e.g. "https"
    std::string filename;  // attacker-controlled
};

// BUG: template substitution without escaping shell metacharacters.
std::string build_delegate_command(const ImageInfo& info) {
    std::string cmd = "curl -s '";
    cmd += info.filename;   // craft: https://x/";touch /tmp/pwned;"a
    cmd += "' > /tmp/out.img";
    return cmd;
}

// "safe" variant: strict allow-list on the filename charset.
bool looks_safe(const std::string& s) {
    for (char c : s) {
        if (!(std::isalnum(static_cast<unsigned char>(c)) || c == '.' || c == '/' ||
              c == ':' || c == '-' || c == '_')) return false;
    }
    return true;
}

int main() {
    ImageInfo info{"https", "https://evil.example/\";touch /tmp/pwned;\"a"};
    std::string cmd = build_delegate_command(info);
    std::printf("delegate cmd = %s\n", cmd.c_str());
    std::printf("charset check would have rejected: %s\n", looks_safe(info.filename) ? "no" : "YES");
    return 0;
}

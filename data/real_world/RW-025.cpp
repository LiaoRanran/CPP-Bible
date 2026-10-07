// RW-025 | CVE-2021-41773 | Apache HTTP Server | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-41773
// project_url: https://httpd.apache.org/
// year: 2021 | severity: HIGH | source_type: cve
// mechanism: 路径规范化（"." 处理）缺陷：%2e 编码的点使规范化函数返回失败但
//   后续仍按字面路径映射，导致目录穿越（应用 CVE 修复的反面教材）。
// notes: 最小重构。逻辑缺陷类。
#include <cstdio>
#include <string>

// BUG: normalization failure is ignored; unnormalized path is used for mapping.
std::string normalize_path(const std::string& in, bool* ok) {
    std::string out;
    for (size_t i = 0; i < in.size(); ++i) {
        if (in.compare(i, 3, "%2e") == 0 || in.compare(i, 3, "%2E") == 0) {
            out.push_back('.');
            i += 2;
        } else if (in.compare(i, 3, "%2f") == 0 || in.compare(i, 3, "%2F") == 0) {
            *ok = false;   // encoded slash: normalization refused
            out.push_back('/');
            i += 2;
        } else {
            out.push_back(in[i]);
        }
    }
    return out;
}

int main() {
    bool ok = true;
    std::string req = "/cgi-bin/.%2e/.%2e/.%2e/.%2e/etc/passwd";
    std::string path = normalize_path(req, &ok);
    if (!ok) {
        // BUG: falls back to using the raw (still traversable) path
        std::printf("maps to filesystem path: %s\n", req.c_str());
    }
    std::printf("normalized form would be: %s\n", path.c_str());
    return 0;
}

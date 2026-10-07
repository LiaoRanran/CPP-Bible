// RW-026 | CVE-2021-42013 | Apache HTTP Server | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-42013
// project_url: https://httpd.apache.org/
// year: 2021 | severity: CRITICAL | source_type: cve
// mechanism: 对 CVE-2021-41773 修复的不完整：双编码 %%32%65 组合在二次解码后
//   重新引入穿越（修复只覆盖单次编码）。
// notes: 最小重构。逻辑缺陷（"修复绕过"模式）。
#include <cstdio>
#include <string>

std::string single_decode(const std::string& in) {
    std::string out;
    for (size_t i = 0; i < in.size(); ++i) {
        if (in[i] == '%' && i + 2 < in.size()) {
            auto hex = [](char c) -> int {
                if (c >= '0' && c <= '9') return c - '0';
                if (c >= 'a' && c <= 'f') return c - 'a' + 10;
                if (c >= 'A' && c <= 'F') return c - 'A' + 10;
                return -1;
            };
            int hi = hex(in[i + 1]), lo = hex(in[i + 2]);
            if (hi >= 0 && lo >= 0) {
                out.push_back(static_cast<char>(hi * 16 + lo));
                i += 2;
                continue;
            }
        }
        out.push_back(in[i]);
    }
    return out;
}

// BUG: the 41773 fix rejects after ONE decode; "%%32%65" survives as "%2e"
// and becomes "." after the *second* decode performed by a lower layer.
bool patched_check(const std::string& raw) {
    std::string once = single_decode(raw);
    if (once.find("../") != std::string::npos) return false;  // catches single-encoding only
    std::string twice = single_decode(once);                  // lower layer decodes again
    return twice.find("../") == std::string::npos;            // returns true -> bypass!
}

int main() {
    std::string req = "/cgi-bin/%%32%65%%32%65/%%32%65%%32%65/bin/sh";
    bool safe = patched_check(req);
    std::printf("request deemed safe = %s (bug: bypass)\n", safe ? "YES" : "no");
    return 0;
}

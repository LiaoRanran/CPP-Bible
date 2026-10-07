// RW-067 | CVE-2022-1941 | protobuf | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-1941
// project_url: https://protobuf.dev/
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: 解析深度/递归限制在 C++ 实现中可被绕过，超长嵌套消息造成
//   栈耗尽/DoS（解析器拒绝服务）。
// notes: 最小重构：展示"递归深度限制被 1 层绕过"的逻辑缺陷（无危险递归，
//   用手工计数模拟）。
#include <cstdio>
#include <string>

struct ParseLimits {
    int max_depth;
};

// BUG: the depth check happens *after* recursing one more level; crafted nesting
// of max_depth+1 layers passes the check (limitation bypass).
bool parse_message(const std::string& input, ParseLimits lim, int depth) {
    if (input.empty()) return true;
    if (depth > lim.max_depth) return false;        // checked too late
    // nested message marker (length-delimited field 0x2A)
    if (input[0] == 0x2A) {
        // recursion happens BEFORE the caller-side check in the vulnerable layout
        return parse_message(input.substr(1), lim, depth + 1);
    }
    return true;
}

int main() {
    std::string crafted(4096, 0x2A);                // 4096 nested messages
    crafted.push_back('E');
    ParseLimits lim{100};                           // the documented limit
    bool ok = parse_message(crafted, lim, 0);
    std::printf("parse accepted nesting far beyond limit: %s\n", ok ? "YES (bug)" : "no");
    return 0;
}

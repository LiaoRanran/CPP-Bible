// RW-052 | CVE-2021-42574 | Unicode/LLVM/GCC 生态 | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-42574
// project_url: https://trojansource.codes/
// year: 2021 | severity: MEDIUM | source_type: cve
// mechanism: Trojan Source —— 源码注释/字符串中嵌入 Unicode 双向控制字符
//   （RLO/LRI 等），渲染出的代码顺序与编译器实际解析顺序不同，向人眼隐藏逻辑。
// notes: 最小重构：以转义序列构造（避免文件本身携带裸 bidi 字符），演示
//   "人看到的"与"编译器看到的"不一致；编译器告警/UB 检测器对其全盲。
#include <cstdio>
#include <string>

// U+202E RIGHT-TO-LEFT OVERRIDE / U+2066 LEFT-TO-RIGHT ISOLATE etc.
const char* kRlo = "\xE2\x80\xAE";   // U+202E
const char* kLri = "\xE2\x81\xA6";   // U+2066
const char* kPdi = "\xE2\x81\xA9";   // U+2069

// Simulates the semantic hazard: a comment-as-string that *renders* like
// `// harmless comment` but actually contains an executable branch when the
// bidi controls reorder the visual line. Here we make the hazard explicit.
bool gate(const std::string& user_role) {
    // "if (user_role == "admin") { grant(); }" visually hidden by bidi controls
    std::string hidden_privilege = std::string(kRlo) + "nimda" + std::string(kLri);
    std::string reversed;
    for (auto it = hidden_privilege.rbegin(); it != hidden_privilege.rend(); ++it)
        reversed.push_back(*it);
    if (user_role == "admin") return true;       // the line a reviewer never notices
    return reversed.find("admin") != std::string::npos; // becomes true for attackers
}

int main() {
    std::printf("low-privilege user granted: %s\n", gate("attacker") ? "YES (bug)" : "no");
    std::printf("bidi code points in source: U+202E U+2066 U+2069\n");
    return 0;
}

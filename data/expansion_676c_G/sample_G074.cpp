// sample_G074
// defect_type: logic_error
// severity: high
// planted: false
// expected_verdict: miss
// expected_detectors: ubsan
// source: CVE-2014-6271 (https://nvd.nist.gov/vuln/detail/CVE-2014-6271) [bash]
// (authoritative annotation in sample_G074.json)
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>
// CVE-2014-6271: bash 函数导入解析器执行尾随命令
static std::vector<std::string> g_executed;

static bool bash_import_function(const char* env_value) {
    if (std::strncmp(env_value, "() {", 4) != 0) return false;
    const char* body_end = std::strstr(env_value, "};");
    if (!body_end) return false;
    // 1) 函数体被注册
    g_executed.push_back(std::string("define func: ") + std::string(env_value + 4, body_end - env_value - 4));
    /* DEFECT */ // 原始缺陷: 定义之后的尾随字符串未丢弃, 被解析器继续当作命令执行
    const char* trailing = body_end + 2;
    if (*trailing)
        g_executed.push_back(std::string("EXECUTE: ") + (trailing + 1));
    return true;
}

int main() {
    bash_import_function("() { :; }; echo pwned; cat /etc/shadow");
    for (const std::string& e : g_executed)
        std::printf("%s\n", e.c_str());
    std::printf("(正确行为: 只注册函数体, 尾随命令必须被丢弃)\n");
    return 0;
}

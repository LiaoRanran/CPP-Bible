// sample_G072
// defect_type: heap_overflow
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2021-3156 (https://nvd.nist.gov/vuln/detail/CVE-2021-3156) [sudo]
// (authoritative annotation in sample_G072.json)
#include <cstdio>
#include <cstring>
#include <string>
// CVE-2021-3156: user_args 分配尺寸未计入反斜杠转义翻倍 → 堆溢出
static char* sudo_set_cmnd(const char* args) {
    size_t size = std::strlen(args) + 1;      // 原始缺陷: 未按转义后长度计算
    char* user_args = new char[size];
    size_t j = 0;
    for (size_t i = 0; args[i]; ++i) {
        user_args[j++] = args[i];
        /* DEFECT */ if (args[i] == '\\')
            user_args[j++] = '\\';            // sudoedit 模式: 反斜杠翻倍 → j 超过 size
    }
    return user_args;
}

int main() {
    // crafted 参数: 100 组 "\\x" (200 字符, 含 100 个反斜杠)
    std::string args;
    for (int i = 0; i < 100; ++i) args += "\\x";
    char* ua = sudo_set_cmnd(args.c_str());   // 分配 201, 写入 ~300 → 溢出
    std::printf("user_args=%.10s...\n", ua);
    delete[] ua;
    return 0;
}

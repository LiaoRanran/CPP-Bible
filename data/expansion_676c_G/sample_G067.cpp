// sample_G067
// defect_type: heap_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2018-1124 (https://nvd.nist.gov/vuln/detail/CVE-2018-1124) [procps-ng]
// (authoritative annotation in sample_G067.json)
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2018-1124: file2strvec 整数溢出 → 堆损坏(用户态等价重构)
static char** file2strvec(const unsigned char* buf, size_t buf_len) {
    char** vec = new char*[4];
    size_t start = 0;
    /* DEFECT */ // 原始缺陷: 段长按 int 计算/分配, 巨大段长溢出为负
    int len = (int)(buf_len - start);          // 巨大长度 → (int) 截断为负
    char* dst = new char[len > 0 ? len + 1 : 1];   // 分配 1 字节
    std::memcpy(dst, buf, buf_len);            // 按真实长度拷贝 → 堆越界写
    vec[0] = dst;
    vec[1] = 0;
    return vec;
}

int main() {
    // crafted procfs 条目: 段长 2^31 + 8(运行时变量绕过常量折叠)
    volatile size_t seg = 0x80000008ULL;
    unsigned char* buf = new unsigned char[16];
    std::memset(buf, 'A', 16);
    char** v = file2strvec(buf, seg);
    std::printf("vec[0]=%s\n", v[0]);
    delete[] buf;
    return 0;
}

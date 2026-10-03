// sample_G069
// defect_type: heap_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2015-0235 (https://nvd.nist.gov/vuln/detail/CVE-2015-0235) [glibc]
// (authoritative annotation in sample_G069.json)
#include <cstdio>
#include <cstring>
// CVE-2015-0235 (GHOST): 缓冲尺寸计算缺少 NUL 的 +1 → 边界处越界写 1 字节
static const size_t HOST_BUF_SIZE = 1024;

static bool digits_dots(const char* name, char* buffer, size_t buffer_size) {
    /* DEFECT */ size_t size_needed = std::strlen(name);   // 原始缺陷: 未 +1 给 '\0'
    if (size_needed > buffer_size) return false;
    std::memcpy(buffer, name, size_needed);
    buffer[size_needed] = '\0';   // size_needed == buffer_size 时写 buffer[buffer_size] → 越界
    return true;
}

int main() {
    char* hostbuf = new char[HOST_BUF_SIZE];
    // crafted 主机名: 恰好 1024 个 'a'
    char* name = new char[HOST_BUF_SIZE + 1];
    std::memset(name, 'a', HOST_BUF_SIZE);
    name[HOST_BUF_SIZE] = '\0';
    if (digits_dots(name, hostbuf, HOST_BUF_SIZE))
        std::printf("hostname accepted: %.8s...\n", hostbuf);
    delete[] name;
    delete[] hostbuf;
    return 0;
}

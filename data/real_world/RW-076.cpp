// RW-076 | CVE-2022-0185 | Linux kernel | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-0185
// project_url: https://www.kernel.org/
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: legacy_parse_param（fs_context 字符串选项）长度计算不当 —— 超长
//   选项字符串堆缓冲区溢出（容器逃逸面）。
// notes: 最小重构 —— **用户态复刻** fs_context 参数拼接逻辑。
#include <cstdio>
#include <cstdlib>
#include <cstring>

// BUG: `remaining` underflows because PAGE_SIZE - 1 - size is computed when
// size > PAGE_SIZE - 1; huge option string copies past the buffer.
void legacy_parse_param(char* page, size_t page_size, const char* param) {
    size_t size = std::strlen(param);
    size_t remaining = page_size - 1 - size;   // underflow for long param
    if (remaining < page_size) {               // check passes due to wrap
        std::memcpy(page, param, size + 1);    // heap overflow
    }
}

int main() {
    const size_t page = 4096;
    char* buf = static_cast<char*>(std::malloc(page));
    static char long_param[8192];
    std::memset(long_param, 'o', sizeof(long_param) - 1);
    long_param[sizeof(long_param) - 1] = '\0';
    // crafted: "-o " + ~4096 bytes of option text
    char* p = long_param; p += 0;
    std::printf("option length = %zu\n", std::strlen(p));
    legacy_parse_param(buf, page, p);
    std::printf("parsed oversized fs_context option\n");
    std::free(buf);
    return 0;
}

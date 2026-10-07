// RW-012 | CVE-2023-4911 | glibc | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2023-4911
// project_url: https://www.gnu.org/software/libc/
// year: 2023 | severity: HIGH | source_type: cve
// mechanism: Looney Tunables —— ld.so 解析 GLIBC_TUNABLES 时对 "tunable=value"
//   分割后拷贝进 256 字节栈缓冲，多个 tunable 串联时越界写。
// notes: 最小重构（解析器逻辑复刻，不提权步骤）。ASan 应报栈越界写。
#include <cstdio>
#include <cstring>

// BUG: `buf` is 256 bytes; parsing loops over ':' separated tunables and copies
// each value without checking the remaining space.
void parse_tunables_into(char* buf256, const char* val) {
    size_t used = 0;
    const char* p = val;
    while (*p && used < 512) {           // loop bound is wrong (512 > 256)
        const char* colon = std::strchr(p, ':');
        size_t n = colon ? static_cast<size_t>(colon - p) : std::strlen(p);
        std::memcpy(buf256 + used, p, n);    // no remaining-space check
        used += n;
        buf256[used++] = '\0';
        if (!colon) break;
        p = colon + 1;
    }
}

int main() {
    char buf[256];
    // crafted environment variable: long chain of tunables
    const char* glibc_tunables =
        "glibc.malloc.mxfast=aaaa:glibc.malloc.tcache_max=bbbb:glibc.malloc.top_pad=cccc:"
        "glibc.malloc.trim_threshold=dddd:glibc.cpu.hwcaps=eeee:glibc.malloc.mmap_max=ffff:"
        "glibc.malloc.check=gggg:glibc.cpu.prefer_map_32bit_exec=hhhh";
    parse_tunables_into(buf, glibc_tunables); // overflows the 256-byte stack buffer
    std::printf("tunables parsed: %.32s...\n", buf);
    return 0;
}

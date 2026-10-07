// RW-108 | CVE-2015-0235 | glibc | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2015-0235
// project_url: https://www.gnu.org/software/libc/
// year: 2015 | severity: CRITICAL | source_type: cve
// mechanism: GHOST —— gethostbyname 系列对超长（>255）主机名整数长度溢出，
//   堆缓冲区溢出（远程代码执行面）。
// notes: 最小重构。ASan 应报 heap-buffer-overflow write。
#include <cstdio>
#include <cstdlib>
#include <cstring>

// BUG: h_length stored in a 1-byte field; strlen() result truncated -> heap
// buffer allocated too small, then name copied in full.
struct HostLookup {
    unsigned char h_length;      // 8-bit length field (wraps for long names)
    char h_name[8];
};

char* gethostbyname_sim(const char* name) {
    size_t len = std::strlen(name);
    HostLookup* hl = static_cast<HostLookup*>(std::malloc(sizeof(HostLookup) - 8 + len + 1));
    hl->h_length = (unsigned char)len;                    // truncates: 512 -> 0
    std::memcpy(hl->h_name, name, len);                   // writes full 512 bytes
    hl->h_name[len] = '\0';
    std::printf("h_length=%u\n", hl->h_length);
    return reinterpret_cast<char*>(hl);
}

int main() {
    char long_name[512];
    std::memset(long_name, 'h', 511);
    long_name[511] = '\0';
    char* r = gethostbyname_sim(long_name);                // 511-byte hostname
    std::free(r);
    return 0;
}

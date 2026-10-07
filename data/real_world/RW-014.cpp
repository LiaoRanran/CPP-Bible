// RW-014 | CVE-2022-23218 | glibc | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-23218
// project_url: https://www.gnu.org/software/libc/
// year: 2022 | severity: CRITICAL | source_type: cve
// mechanism: svcunix_create 对调用者提供的路径直接 strcpy 进固定栈缓冲，
//   超长路径越界写。
// notes: 最小重构。ASan 应报 stack-buffer-overflow write。
#include <cstdio>
#include <cstring>

#define MAXPATHLEN 108  // sun_path in sockaddr_un

// BUG: strcpy without length check into a fixed-size stack path buffer
int svcunix_create_sim(const char* caller_path) {
    char path[MAXPATHLEN];
    std::strcpy(path, caller_path);          // overflow for long caller_path
    return static_cast<int>(std::strlen(path));
}

int main() {
    char long_path[256];
    std::memset(long_path, 'p', sizeof(long_path) - 1);
    long_path[sizeof(long_path) - 1] = '\0'; // 255-byte path from RPC caller
    int n = svcunix_create_sim(long_path);
    std::printf("path len = %d\n", n);
    return 0;
}

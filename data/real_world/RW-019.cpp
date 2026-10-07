// RW-019 | CVE-2016-8618 | curl | defect_type: double_free
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2016-8618
// project_url: https://curl.se/
// year: 2016 | severity: HIGH | source_type: cve
// mechanism: curl_maprintf 出错路径与调用者清理路径对同一缓冲二次释放。
// notes: 最小重构。ASan 应报 double-free（或 UAF）。
#include <cstdarg>
#include <cstdio>
#include <cstdlib>
#include <cstring>

// Simplified curl_maprintf: on allocation failure both this function and the
// caller free the same buffer.
char* curl_maprintf_sim(const char* fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    char tmp[128];
    int n = std::vsnprintf(tmp, sizeof(tmp), fmt, ap);
    va_end(ap);
    if (n < 0) return nullptr;

    char* out = static_cast<char*>(std::malloc(static_cast<size_t>(n) + 1));
    if (!out) return nullptr;
    std::memcpy(out, tmp, static_cast<size_t>(n) + 1);

    if (n > 100) {          // "too long" error path
        std::free(out);     // freed here...
        return out;         // ...but returned anyway (caller frees again)
    }
    return out;
}

int main() {
    char big[120];
    std::memset(big, 'x', sizeof(big));
    big[sizeof(big) - 1] = '\0';
    char* s = curl_maprintf_sim("prefix:%s", big); // triggers the error path
    if (s) {
        std::free(s);       // second free
    }
    return 0;
}

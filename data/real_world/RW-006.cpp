// RW-006 | CVE-2022-4450 | OpenSSL | defect_type: double_free
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-4450
// project_url: https://www.openssl.org/
// year: 2023 | severity: HIGH | source_type: cve
// mechanism: PEM_read_bio_ex 在特定畸形输入下对同一缓冲释放两次。
// notes: 最小重构。ASan/LeakSanitizer 应报 double-free。
#include <cstdio>
#include <cstdlib>
#include <cstring>

// Simplified PEM reader: error paths both free the decoded buffer.
char* pem_decode(const char* input, size_t in_len, bool* ok) {
    char* buf = static_cast<char*>(std::malloc(in_len + 1));
    std::memcpy(buf, input, in_len);
    buf[in_len] = '\0';

    if (in_len > 0 && input[0] == '-') { // crafted marker triggers the error path
        std::free(buf);
        *ok = false;
        // BUG: falls through to the common cleanup which frees again
    }
    *ok = true;
    return buf; // caller frees buf ... but the error path already freed it
}

int main() {
    bool ok = false;
    const char* crafted = "--BROKEN PEM HEADER--";
    char* out = pem_decode(crafted, std::strlen(crafted), &ok);
    if (!ok) {
        std::free(out); // second free of the same pointer
    }
    std::printf("decoded=%p\n", (void*)out);
    return 0;
}

// RW-007 | CVE-2023-0215 | OpenSSL | defect_type: use_after_free
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2023-0215
// project_url: https://www.openssl.org/
// year: 2023 | severity: HIGH | source_type: cve
// mechanism: BIO 链清理顺序错误——对已被释放的 BIO 再次执行读取/清理。
// notes: 最小重构。ASan 应报 heap-use-after-free。
#include <cstdio>
#include <cstring>

struct BIO {
    char* data;
    BIO* next;
};

BIO* bio_new(const char* s) {
    BIO* b = new BIO{};
    b->data = new char[std::strlen(s) + 1];
    std::strcpy(b->data, s);
    b->next = nullptr;
    return b;
}

// BUG: frees the BIO but leaves the caller's pointer dangling; the error path
// then performs one more read on it (cleanup-after-free order).
int bio_read_callback(BIO* b, char* out, size_t n) {
    delete[] b->data;
    delete b;                       // node freed here ...
    if (out) {
        std::memcpy(out, b->data, n); // ... then read through the dangling pointer
    }
    return 0;
}

int main() {
    BIO* b = bio_new("certificate-bytes");
    char buf[32];
    bio_read_callback(b, buf, 8);   // use-after-free read
    std::printf("read %d bytes after free\n", 8);
    return 0;
}

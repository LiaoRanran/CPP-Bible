// RW-046 | CVE-2022-40674 | expat | defect_type: use_after_free
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-40674
// project_url: https://libexpat.github.io/
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: doContent 中实体内容处理：缓冲 realloc 失败/重入路径保留旧指针，
//   之后的引用触及已释放块。
// notes: 最小重构。ASan 应报 heap-use-after-free。
#include <cstdio>
#include <cstdlib>
#include <cstring>

struct XmlBuf {
    char* data;
    size_t len, cap;
};

// BUG: buffer grows via realloc, but `old` (kept by a pending parse frame)
// is used afterwards.
XmlBuf* buf_grow(XmlBuf* b, size_t need) {
    if (b->cap >= need) return b;
    char* old = b->data;
    b->data = static_cast<char*>(std::realloc(b->data, need * 2));
    b->cap = need * 2;
    (void)old;
    return b;
}

int main() {
    XmlBuf* b = static_cast<XmlBuf*>(std::malloc(sizeof(XmlBuf)));
    b->data = static_cast<char*>(std::malloc(16));
    b->len = 4;
    b->cap = 16;
    std::strcpy(b->data, "root");

    char* pending = b->data;         // parse frame keeps the pre-grow pointer
    buf_grow(b, 1024);               // data moved; pending now dangling
    std::strcpy(pending, "frame");   // use-after-free write
    std::printf("buf=%s\n", b->data);
    std::free(b->data);
    std::free(b);
    return 0;
}

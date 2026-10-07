// RW-042 | CVE-2022-0562 | libtiff | defect_type: null_pointer_deref
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-0562
// project_url: https://libtiff.gitlab.io/libtiff/
// year: 2022 | severity: MEDIUM | source_type: cve
// mechanism: TIFFReadDirectory 再一个空指针路径：畸形目录项使 codec 挂钩表为空
//   （与 0561 不同的 IFD 组合）。
// notes: 最小重构。ASan/UBSan 命中空指针。
#include <cstdio>
#include <cstring>

struct Codec {
    const char* name;
    int (*decode)(const char*);
};

struct TiffContext {
    Codec* codec;          // may be left null by malformed IFD
    int compression;       // crafted: unknown compression id
};

int read_encoded_strip(TiffContext* ctx, const char* data) {
    // BUG: unknown compression leaves ctx->codec null, but the strip reader
    // calls through it unconditionally.
    return ctx->codec->decode(data);   // NULL function pointer deref
}

int unused_decode(const char* s) { return static_cast<int>(std::strlen(s)); }

int main() {
    TiffContext ctx{};
    ctx.codec = nullptr;               // malformed directory left it null
    ctx.compression = 9999;
    int n = read_encoded_strip(&ctx, "strip-data");
    std::printf("decoded %d\n", n);
    return 0;
}

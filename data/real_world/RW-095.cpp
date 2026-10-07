// RW-095 | CVE-2021-45943 | expat | defect_type: null_pointer_deref
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-45943
// project_url: https://libexpat.github.io/
// year: 2022 | severity: MEDIUM | source_type: cve
// mechanism: XML_GetBuffer 在指定长度下返回 NULL 的分支未被调用方处理，
//   畸形输入路径空指针解引用。
// notes: 最小重构。ASan/UBSan 命中。
#include <cstdio>
#include <cstdlib>
#include <cstring>

// BUG: caller passes a huge size; GetBuffer returns NULL; caller memcpys into it.
void xml_parse_chunk_raw(long requested) {
    char* buf = nullptr;
    if (requested > 0 && requested < 1024 * 1024) {    // synthetic limit
        buf = static_cast<char*>(std::malloc((size_t)requested));
    }
    // BUG: no NULL check before use
    std::memcpy(buf, "chunk", 5);                      // NULL deref for huge request
    std::free(buf);
}

int main() {
    // crafted: internal request length larger than the allowed window
    xml_parse_chunk_raw(0x7FFFFFF0L);
    std::printf("chunk parsed\n");
    return 0;
}

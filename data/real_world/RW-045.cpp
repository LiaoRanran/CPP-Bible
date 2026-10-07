// RW-045 | CVE-2016-0718 | expat | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2016-0718
// project_url: https://libexpat.github.io/
// year: 2016 | severity: CRITICAL | source_type: cve
// mechanism: 对恶意 UTF-8 编码的 XML 内容，多字节解码循环中输出缓冲推进越界
//   （"UTF-8 序列边界"处理缺陷），堆越界写。
// notes: 最小重构。ASan 应报 heap-buffer-overflow write。
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>

// BUG: decoder advances the output pointer per *byte* of a multi-byte sequence
// but the capacity check only counts sequences (mismatch -> overflow).
void decode_utf8_into(const uint8_t* in, size_t n, char* out, size_t out_cap) {
    size_t produced = 0;
    for (size_t i = 0; i < n; ++i) {
        uint8_t c = in[i];
        if ((c & 0x80) == 0) {
            out[produced++] = static_cast<char>(c);         // 1 byte
        } else if ((c & 0xE0) == 0xC0) {
            out[produced++] = static_cast<char>(c);
            out[produced++] = static_cast<char>(in[i + 1]); // 2 bytes, i advances once
        } else {
            out[produced++] = static_cast<char>(c);
            out[produced++] = static_cast<char>(in[i + 1]);
            out[produced++] = static_cast<char>(in[i + 2]); // 3 bytes
        }
        if (produced >= out_cap) break;
    }
}

int main() {
    // crafted: many overlapping multi-byte sequences (invalid UTF-8 boundary)
    std::vector<uint8_t> in(24, 0xE0);
    in.push_back(0x80);
    in.push_back(0x80);
    std::vector<char> out(16);       // capacity smaller than decode output
    decode_utf8_into(in.data(), in.size(), out.data(), out.size());
    std::printf("decoded\n");
    return 0;
}

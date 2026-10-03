// sample_G061
// defect_type: pointer_overflow
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2016-9841 (https://nvd.nist.gov/vuln/detail/CVE-2016-9841) [zlib]
// (authoritative annotation in sample_G061.json)
#include <cstdio>
#include <cstdint>
// CVE-2016-9841: inffast.c 输出指针 unchecked 推进 → 指针回绕
static unsigned inflate_fast_out(const unsigned char* in, int in_len, unsigned char* out, int out_cap) {
    unsigned char* o = out;
    unsigned char* out_end = out + out_cap;
    int i = 0;
    while (i + 1 < in_len) {
        unsigned dist = in[i + 1];            // crafted: 距离字段
        /* DEFECT */ o += dist;               // 原始缺陷: 推进量未按 out_end 校验
        if (o >= out_end)
            *o = 'X';                         // 越过窗口末尾仍写入 → 堆越界写
        i += 2;
    }
    return (unsigned)(o - out);
}

int main() {
    unsigned char* out = new unsigned char[64];
    // crafted 解压流: 距离字段 0x46(70) → 首次写入落在 out+70, 越过 64 字节缓冲 6 字节
    unsigned char in[4] = { 0x00, 0x46, 0x00, 0x30 };
    std::printf("produced=%u\n", inflate_fast_out(in, 4, out, 64));
    delete[] out;
    return 0;
}

// sample_G066
// defect_type: heap_overread
// severity: medium
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2019-11036 (https://nvd.nist.gov/vuln/detail/CVE-2019-11036) [php]
// (authoritative annotation in sample_G066.json)
#include <cstdio>
#include <cstdint>
// CVE-2019-11036: components 计数未校验 → 偏移远超缓冲 → 越界读
static int exif_read_signed_short(const unsigned char* data, size_t size, unsigned components) {
    /* DEFECT */ unsigned offset = 8 + components * 2;   // 未检查 offset + 2 <= size
    return (short)((data[offset] << 8) | data[offset + 1]);   // 野指针读 → SEGV
}

int main() {
    // crafted EXIF: 文件 64 字节, IFD 条目声明 components=100000 (LONG 格式)
    unsigned char* file = new unsigned char[64]();
    std::printf("value=%d\n", exif_read_signed_short(file, 64, 100000));   // offset=200008 → 越界
    delete[] file;
    return 0;
}

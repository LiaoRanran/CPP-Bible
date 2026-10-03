// sample_G065
// defect_type: heap_overread
// severity: medium
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2019-11034 (https://nvd.nist.gov/vuln/detail/CVE-2019-11034) [php]
// (authoritative annotation in sample_G065.json)
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2019-11034: exif_process_IFD_TAG 偏移+长度未按文件大小校验 → 堆越界读
static int exif_process_IFD_TAG(const unsigned char* data, size_t size,
                                unsigned value_offset, unsigned byte_count) {
    unsigned char value[64];
    size_t copy = byte_count < sizeof(value) ? byte_count : sizeof(value);
    /* DEFECT */ // 原始缺陷: 未检查 value_offset + byte_count <= size
    std::memcpy(value, data + value_offset, copy);
    return value[0];
}

int main() {
    // crafted EXIF: 文件缓冲 100 字节, IFD 条目指向 offset=90, 长度 64
    unsigned char* file = new unsigned char[100]();
    std::memset(file, 0x41, 100);
    std::printf("value[0]=%d\n", exif_process_IFD_TAG(file, 100, 90, 64));   // 读 90..154 → 越界
    delete[] file;
    return 0;
}

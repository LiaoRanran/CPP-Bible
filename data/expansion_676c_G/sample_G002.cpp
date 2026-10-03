// sample_G002
// defect_type: heap_overread
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2014-3508 (https://nvd.nist.gov/vuln/detail/CVE-2014-3508) [openssl]
// (authoritative annotation in sample_G002.json)
#include <cstdio>
#include <cstring>
// CVE-2014-3508: OBJ_obj2txt(pretty print) 不保证 '\0' → 调用方按 C 字符串读 → 越界读
static char* OBJ_obj2txt_pretty(const unsigned char* oid, size_t oid_len) {
    // 原始缺陷: 缓冲按解码后文本精确大小分配, 不含 '\0'
    char* buf = new char[oid_len];
    for (size_t i = 0; i < oid_len; ++i)
        buf[i] = (char)('0' + (oid[i] % 10));
    return buf;
}

int main() {
    unsigned char* oid = new unsigned char[16]
        { 42, 1, 2, 84, 113, 1, 1, 11, 5, 0, 3, 13, 1, 4, 7, 9 };
    char* text = OBJ_obj2txt_pretty(oid, 16);
    /* DEFECT */ std::printf("oid=%s\n", text);   // printf/%s 需要 strlen → 越过 16 字节缓冲
    delete[] text;
    delete[] oid;
    return 0;
}
